#!/usr/bin/env python3
"""Strategy no. 9, model P (pre-FOMC drift): in-sample runs T31 (P-SPX) and T32 (P-NDX) with the
pre-registered acceptance check and descriptive tables, and - only for a variant that passed - the
one-time hold-out run T33 (docs/01_Vorregistrierung.md).

Usage:
  ../smart-money-concept/research/.venv/bin/python -I research/scripts/run_p.py                   # T31 + T32
  ../smart-money-concept/research/.venv/bin/python -I research/scripts/run_p.py --holdout P-SPX   # T33, once
"""
import argparse
import sys
from datetime import date
from pathlib import Path

import numpy as np
import pyarrow as pa
import pyarrow.parquet as pq

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from fomc import DATA_DIR, RESULTS_DIR  # noqa: E402
from fomc.model import (EPOCH, ROW_DTYPE, VARIANTS, Index, load_dates, ny_utc, prev_weekday,  # noqa: E402
                        run_model_p, window_bp)
from smc.data.bars import load_bars  # noqa: E402
from smc.report import cluster_bootstrap_ci, cluster_t  # noqa: E402
from smc.strategy_h import spec_for  # noqa: E402
from smc.swaps import RateTable  # noqa: E402

IS_YEARS, HO_YEARS = range(2015, 2024), range(2024, 2027)
OUT_DIR = DATA_DIR / "p"


def year_of(days) -> np.ndarray:
    return np.array([date.fromordinal(EPOCH.toordinal() + int(d)).year for d in days])


def month_of(days) -> np.ndarray:
    return np.array([date.fromordinal(EPOCH.toordinal() + int(d)).month for d in days])


def tval(x: np.ndarray) -> float:
    return float(x.mean() / (x.std(ddof=1) / np.sqrt(len(x)))) if len(x) > 2 else np.nan


def load_index(symbol: str) -> Index:
    m5 = load_bars(symbol, "M5")
    return Index(spec_for(symbol, m5), m5, load_bars(symbol, "D1"))


def stats(rows: np.ndarray, years) -> dict:
    net, cost = rows["net_bp"], rows["cost_bp"]
    yr = year_of(rows["day"])
    quarter = yr * 4 + (month_of(rows["day"]) - 1) // 3
    m = {"n": len(net), "E": float(net.mean()), "sd": float(net.std(ddof=1)), "gross": float(rows["gross_bp"].mean()),
         "cost": float(cost.mean()), "swap": float(rows["swap_bp"].mean()), "E_2x": float((net - cost).mean()),
         "t_iid": tval(net), "t_q": cluster_t(net, quarter), "hit": float((net > 0).mean()),
         "stops": int(rows["stopped"].sum())}
    m["t"] = min(m["t_iid"], m["t_q"])
    m["sharpe"] = m["E"] / m["sd"] * np.sqrt(len(net) / max(1, len(set(yr.tolist()))))
    m["by_year"] = {y: (int((yr == y).sum()), float(net[yr == y].sum())) for y in years}
    m["years_pos"] = sum(1 for k, tot in m["by_year"].values() if k and tot > 0)
    first, second = net[yr <= 2019], net[yr >= 2020]
    m["halves"] = (float(first.mean()) if len(first) else np.nan, float(second.mean()) if len(second) else np.nan)
    m["net_arr"], m["days_arr"] = net, rows["day"]
    return m


def checks_is(m: dict, years) -> list:
    a, b = m["halves"]
    return [("Mittleres Netto-Ergebnis je Termin > 0 mit t ≥ 3,0 (kleinster aus iid / Quartal)",
             f"{m['E']:+.1f} bp/Termin, t = {m['t']:.2f}", m["E"] > 0 and m["t"] >= 3.0),
            (f"≥ 6 von {len(years)} Jahren positiv", f"{m['years_pos']} von {len(years)}", m["years_pos"] >= 6),
            ("beide Teilzeiträume 2015–2019 und 2020–2023 positiv", f"{a:+.1f} / {b:+.1f} bp", a > 0 and b > 0),
            ("bei doppelten Kosten > 0", f"{m['E_2x']:+.1f} bp/Termin", m["E_2x"] > 0)]


def variant_lines(name: str, m: dict, checks: list) -> list[str]:
    passed = all(ok for _, _, ok in checks)
    out = [f"## {name}\n", "| Kennzahl | Wert |", "|---|---|",
           f"| Termine | {m['n']} |",
           f"| Netto je Termin | {m['E']:+.1f} bp (σ {m['sd']:.1f} bp) |",
           f"| vor Kosten je Termin | {m['gross']:+.1f} bp |",
           f"| Kosten je Termin (davon Swap) | {m['cost']:.1f} bp ({-m['swap']:.1f} bp) |",
           f"| Sharpe Ratio p. a. (netto) | {m['sharpe']:.2f} |",
           f"| t-Wert iid / Quartal | {m['t_iid']:.2f} / {m['t_q']:.2f} |",
           f"| Anteil positiver Termine | {m['hit']:.0%} |",
           f"| Notfall-Stops | {m['stops']} |",
           f"| bei doppelten Kosten | {m['E_2x']:+.1f} bp/Termin |", "",
           "| Kriterium | Ergebnis | erfüllt |", "|---|---|---|"]
    out += [f"| {c} | {v} | {'ja' if ok else '**nein**'} |" for c, v, ok in checks]
    out += ["", f"**{name}: {'alle Kriterien erfüllt' if passed else 'nicht bestanden'}.**\n",
            "| Jahr | Termine | Netto Summe bp |", "|---|---|---|"]
    out += [f"| {y} | {k} | {tot:+.1f} |" for y, (k, tot) in m["by_year"].items()]
    return out + [""]


def descriptive(idx: Index, fomc_days: np.ndarray, years) -> list[str]:
    """Gross bid returns of the same clock window on FOMC and on all other days, and sub-windows."""
    all_fomc = set(load_dates().tolist())
    first, last = (date(min(years), 1, 1) - EPOCH).days, (date(max(years) + 1, 1, 1) - EPOCH).days
    other = [d for d in range(first, last) if date.fromordinal(EPOCH.toordinal() + d).weekday() < 5
             and d not in all_fomc]

    def win(days, a_off, a_hm, b_off, b_hm):
        out = []
        for d in days:
            da = prev_weekday(d) if a_off else d
            db = prev_weekday(d) if b_off else d
            out.append(window_bp(idx.m5, int(ny_utc(da, *a_hm)), int(ny_utc(db, *b_hm))))
        x = np.array(out)
        return x[np.isfinite(x)]

    f, o = win(fomc_days, 1, (14, 0), 0, (13, 55)), win(other, 1, (14, 0), 0, (13, 55))
    diff = f.mean() - o.mean()
    t_diff = diff / np.sqrt(f.var(ddof=1) / len(f) + o.var(ddof=1) / len(o))
    out = ["### Vergleich mit allen anderen Handelstagen (vor Kosten, Bid zu Bid)\n",
           "| Fenster 14:00 Vortag – 13:55 | Tage | Ø bp | t |", "|---|---|---|---|",
           f"| FOMC-Termine | {len(f)} | {f.mean():+.1f} | {tval(f):+.2f} |",
           f"| übrige Handelstage | {len(o)} | {o.mean():+.1f} | {tval(o):+.2f} |",
           f"| **Differenz (FOMC-Effekt)** | | **{diff:+.1f}** | **{t_diff:+.2f}** |", "",
           "### Teilfenster an FOMC-Terminen (vor Kosten)\n", "| Fenster | Termine | Ø bp | t |", "|---|---|---|---|"]
    for lbl, spec in (("14:00–16:00 Vortag", (1, (14, 0), 1, (16, 0))),
                      ("16:00 Vortag – 09:30 Entscheidungstag", (1, (16, 0), 0, (9, 30))),
                      ("09:30–13:55 Entscheidungstag", (0, (9, 30), 0, (13, 55))),
                      ("nach der Entscheidung 14:00–16:00", (0, (14, 0), 0, (16, 0)))):
        x = win(fomc_days, *spec)
        out.append(f"| {lbl} | {len(x)} | {x.mean():+.1f} | {tval(x):+.2f} |")
    return out + [""]


def save(rows: np.ndarray, phase: str, name: str):
    (OUT_DIR / phase).mkdir(parents=True, exist_ok=True)
    pq.write_table(pa.table({n: rows[n] for n in rows.dtype.names}), OUT_DIR / phase / f"{name}.parquet",
                   compression="zstd")


def load(phase: str, name: str) -> np.ndarray:
    t = pq.read_table(OUT_DIR / phase / f"{name}.parquet")
    rows = np.empty(t.num_rows, ROW_DTYPE)
    for n in ROW_DTYPE.names:
        rows[n] = t.column(n).to_numpy(zero_copy_only=False)
    return rows


def in_sample():
    rates = RateTable.load()
    days = load_dates()
    days = days[np.isin(year_of(days), list(IS_YEARS))]
    lines = ["# Modell P (Pre-FOMC-Drift), In-Sample 2015–2023 (Trial T31 P-SPX, T32 P-NDX)\n",
             f"Lauf vom {date.today():%d.%m.%Y}. Regeln laut `docs/01_Vorregistrierung.md`, Code `research/fomc/`. "
             f"{len(days)} planmäßige FOMC-Entscheide; Long von 14:00 New York am Vortag bis 13:55 am "
             "Entscheidungstag. Netto = nach Spread (FTMO-Durchschnitt), Slippage (¼ Spread je Ausführung) und "
             "Swap; Ergebnisse in Basispunkten.\n"]
    verdict = {}
    for v, sym in VARIANTS.items():
        idx = load_index(sym)
        rows = run_model_p(v, idx, days, rates)
        save(rows, "is", v)
        m = stats(rows, IS_YEARS)
        checks = checks_is(m, IS_YEARS)
        verdict[v] = (m, all(ok for _, _, ok in checks))
        lines += variant_lines(v, m, checks) + descriptive(idx, days, IS_YEARS)
    passed = [v for v, (_, ok) in verdict.items() if ok]
    if passed:
        best = max(passed, key=lambda v: verdict[v][0]["t"])
        lines.append(f"**Ergebnis:** bestanden: {', '.join(passed)}; gewählt für den Hold-out: **{best}**.")
    else:
        lines.append("**Ergebnis: Keine Variante erfüllt alle In-Sample-Kriterien. Strategie Nr. 9 ist gescheitert; "
                     "der Hold-out bleibt unberührt.**")
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    (RESULTS_DIR / "p_in_sample.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))


def holdout(variant: str):
    marker = OUT_DIR / "ho" / "DONE"
    if marker.exists():
        sys.exit("Hold-out wurde bereits ausgewertet (data/p/ho/DONE) – kein zweiter Lauf.")
    m_is = stats(load("is", variant), IS_YEARS)
    if not all(ok for _, _, ok in checks_is(m_is, IS_YEARS)):
        sys.exit(f"{variant} hat die In-Sample-Kriterien nicht erfüllt – kein Hold-out.")
    marker.parent.mkdir(parents=True, exist_ok=True)
    marker.write_text(f"T33 {variant} {date.today().isoformat()}\n")
    days = load_dates()
    days = days[year_of(days) >= 2024]
    rows = run_model_p(variant, load_index(VARIANTS[variant]), days, RateTable.load())
    save(rows, "ho", variant)
    m = stats(rows, HO_YEARS)
    lo, hi = cluster_bootstrap_ci(m_is["net_arr"], m_is["days_arr"])
    checks = [("Mittleres Netto-Ergebnis je Termin > 0", f"{m['E']:+.1f} bp", m["E"] > 0),
              ("≥ untere 95-%-Grenze von In-Sample (Bootstrap über Termine)",
               f"{m['E']:+.1f} vs. IS {m_is['E']:+.1f} [{lo:+.1f}; {hi:+.1f}] bp", m["E"] >= lo)]
    lines = [f"# Modell P, Hold-out 2024–2026 (Trial T33, {variant})\n",
             f"Einmaliger Lauf vom {date.today():%d.%m.%Y}.\n"] + variant_lines(variant, m, checks)
    (RESULTS_DIR / "p_holdout.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--holdout", choices=list(VARIANTS))
    args = ap.parse_args()
    if args.holdout:
        holdout(args.holdout)
    else:
        in_sample()


if __name__ == "__main__":
    main()
