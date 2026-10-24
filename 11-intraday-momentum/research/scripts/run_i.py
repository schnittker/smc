#!/usr/bin/env python3
"""Strategy no. 11, model I (intraday momentum US500): in-sample runs T39 (I-ONFH) and T40 (I-ROD) with the
pre-registered acceptance check and descriptive tables, and - only for a variant that passed - the one-time
hold-out run T41 (docs/01_Vorregistrierung.md).

Usage:
  ../smart-money-concept/research/.venv/bin/python -I research/scripts/run_i.py                   # T39 + T40
  ../smart-money-concept/research/.venv/bin/python -I research/scripts/run_i.py --holdout I-ONFH  # T41, once
"""
import argparse
import sys
from datetime import date
from pathlib import Path

import numpy as np
import pyarrow as pa
import pyarrow.parquet as pq

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from imom import DATA_DIR, RESULTS_DIR  # noqa: E402
from imom.model import EPOCH, ROW_DTYPE, VARIANTS, IndexBars, run_model_i  # noqa: E402
from smc.data.bars import load_bars  # noqa: E402
from smc.report import cluster_bootstrap_ci, cluster_t  # noqa: E402
from smc.strategy_h import spec_for  # noqa: E402

IS_YEARS, HO_YEARS = range(2015, 2024), range(2024, 2027)
OUT_DIR = DATA_DIR / "i"


def to_date(d: int) -> date:
    return date.fromordinal(EPOCH.toordinal() + int(d))


def tval(x: np.ndarray) -> float:
    return float(x.mean() / (x.std(ddof=1) / np.sqrt(len(x)))) if len(x) > 2 else np.nan


def load_index(symbol: str) -> IndexBars:
    m5 = load_bars(symbol, "M5")
    return IndexBars(spec_for(symbol, m5), m5, load_bars(symbol, "H1"))


def stats(rows: np.ndarray, years) -> dict:
    net, cost = rows["net_bp"], rows["cost_bp"]
    ds = [to_date(d) for d in rows["day"]]
    yr = np.array([d.year for d in ds])
    month = np.array([d.year * 12 + d.month for d in ds])
    m = {"n": len(net), "E": float(net.mean()), "sd": float(net.std(ddof=1)), "gross": float(rows["gross_bp"].mean()),
         "cost": float(cost.mean()), "E_2x": float((net - cost).mean()), "t_iid": tval(net),
         "t_week": cluster_t(net, (rows["day"] + 3) // 7), "t_month": cluster_t(net, month),
         "hit": float((net > 0).mean()), "stops": int(rows["stopped"].sum())}
    m["t"] = min(m["t_iid"], m["t_week"], m["t_month"])
    m["sharpe"] = m["E"] / m["sd"] * np.sqrt(len(net) / max(1, len(set(yr.tolist()))))
    m["by_year"] = {y: (int((yr == y).sum()), float(net[yr == y].mean()) if (yr == y).any() else np.nan,
                        tval(net[yr == y])) for y in years}
    m["years_pos"] = sum(1 for k, e, _ in m["by_year"].values() if k and e > 0)
    first, second = net[yr <= 2019], net[yr >= 2020]
    m["halves"] = (float(first.mean()) if len(first) else np.nan, float(second.mean()) if len(second) else np.nan)
    m["net_arr"], m["month_arr"] = net, month
    return m


def checks_is(m: dict, years) -> list:
    a, b = m["halves"]
    return [("Mittleres Netto-Tagesergebnis > 0 mit t ≥ 3,0 (kleinster aus iid / Woche / Monat)",
             f"{m['E']:+.2f} bp/Tag, t = {m['t']:.2f}", m["E"] > 0 and m["t"] >= 3.0),
            (f"≥ 6 von {len(years)} Jahren positiv", f"{m['years_pos']} von {len(years)}", m["years_pos"] >= 6),
            ("beide Teilzeiträume 2015–2019 und 2020–2023 positiv", f"{a:+.2f} / {b:+.2f} bp", a > 0 and b > 0),
            ("bei doppelten Kosten > 0", f"{m['E_2x']:+.2f} bp/Tag", m["E_2x"] > 0)]


def variant_lines(name: str, m: dict, checks: list) -> list[str]:
    passed = all(ok for _, _, ok in checks)
    out = [f"## {name}\n", "| Kennzahl | Wert |", "|---|---|",
           f"| Handelstage | {m['n']:,} |",
           f"| Netto je Tag | {m['E']:+.2f} bp (σ {m['sd']:.1f} bp) |",
           f"| vor Kosten je Tag | {m['gross']:+.2f} bp |",
           f"| Kosten je Tag | {m['cost']:.2f} bp |",
           f"| Sharpe Ratio p. a. (netto) | {m['sharpe']:.2f} |",
           f"| t-Wert iid / Woche / Monat | {m['t_iid']:.2f} / {m['t_week']:.2f} / {m['t_month']:.2f} |",
           f"| Trefferquote | {m['hit']:.0%} |",
           f"| Notfall-Stops | {m['stops']} |",
           f"| bei doppelten Kosten | {m['E_2x']:+.2f} bp/Tag |", "",
           "| Kriterium | Ergebnis | erfüllt |", "|---|---|---|"]
    out += [f"| {c} | {v} | {'ja' if ok else '**nein**'} |" for c, v, ok in checks]
    out += ["", f"**{name}: {'alle Kriterien erfüllt' if passed else 'nicht bestanden'}.**\n",
            "| Jahr | Tage | Netto Ø bp | t |", "|---|---|---|---|"]
    out += [f"| {y} | {k} | {e:+.2f} | {t:+.2f} |" for y, (k, e, t) in m["by_year"].items()]
    return out + [""]


def regression(x: np.ndarray, y: np.ndarray, months: np.ndarray) -> tuple[float, float, float]:
    xc = x - x.mean()
    b = float((xc * (y - y.mean())).sum() / (xc ** 2).sum())
    u = y - y.mean() - b * xc
    _, inv = np.unique(months, return_inverse=True)
    g = np.bincount(inv, xc * u)
    se = np.sqrt(len(g) / (len(g) - 1) * (g ** 2).sum()) / (xc ** 2).sum()
    return b, b / se, float(1 - (u ** 2).sum() / ((y - y.mean()) ** 2).sum())


def descriptive(rows: np.ndarray, months: np.ndarray) -> list[str]:
    out = ["### Beschreibend\n", "| Regression von r_LAST auf | Steigung | t (Cluster Monat) | R² |", "|---|---|---|---|"]
    for col in ("r_onfh_bp", "r_rod_bp"):
        b, t, r2 = regression(rows[col], rows["r_last_bp"], months)
        out.append(f"| {col[:-3]} | {b:+.4f} | {t:+.2f} | {r2:.4f} |")
    net = rows["net_bp"]
    big = np.abs(rows["signal_bp"]) >= np.quantile(np.abs(rows["signal_bp"]), 2 / 3)
    out += ["", "| Teilmenge | Tage | Netto Ø bp | vor Kosten Ø bp | t |", "|---|---|---|---|---|"]
    for lbl, sel in (("Long", rows["dir"] == 1), ("Short", rows["dir"] == -1),
                     ("großes Signal (oberstes Drittel)", big), ("übrige", ~big)):
        out.append(f"| {lbl} | {sel.sum()} | {net[sel].mean():+.2f} | {rows['gross_bp'][sel].mean():+.2f} | {tval(net[sel]):+.2f} |")
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
    spx, ndx = load_index("SPXUSD"), load_index("NSXUSD")
    first, last = date(2015, 1, 1), date(2023, 12, 31)
    lines = ["# Modell I (Intraday-Momentum US500), In-Sample 2015–2023 (Trial T39 I-ONFH, T40 I-ROD)\n",
             f"Lauf vom {date.today():%d.%m.%Y}. Regeln laut `docs/01_Vorregistrierung.md`, Code `research/imom/`. "
             "Volle NYSE-Handelstage; Position 15:30–16:00 New York in Richtung des Signals. Netto = nach Spread "
             "(FTMO-Durchschnitt) und Slippage (¼ Spread je Ausführung); Ergebnisse in Basispunkten.\n"]
    verdict = {}
    for v in VARIANTS:
        rows = run_model_i(v, spx, first, last)
        save(rows, "is", v)
        m = stats(rows, IS_YEARS)
        checks = checks_is(m, IS_YEARS)
        verdict[v] = (m, all(ok for _, _, ok in checks))
        lines += variant_lines(v, m, checks) + descriptive(rows, m["month_arr"])
    lines += ["## US100 (beschreibend)\n", "| Variante | Tage | Netto Ø bp | vor Kosten Ø bp | t | Jahre positiv |",
              "|---|---|---|---|---|---|"]
    for v in VARIANTS:
        rows = run_model_i(v, ndx, first, last)
        m = stats(rows, IS_YEARS)
        lines.append(f"| {v} | {m['n']} | {m['E']:+.2f} | {m['gross']:+.2f} | {m['t']:+.2f} | {m['years_pos']} von 9 |")
    lines.append("")
    passed = [v for v, (_, ok) in verdict.items() if ok]
    if passed:
        best = max(passed, key=lambda v: verdict[v][0]["t"])
        lines.append(f"**Ergebnis:** bestanden: {', '.join(passed)}; gewählt für den Hold-out: **{best}**.")
    else:
        lines.append("**Ergebnis: Keine Variante erfüllt alle In-Sample-Kriterien. Strategie Nr. 11 ist gescheitert; "
                     "der Hold-out bleibt unberührt.**")
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    (RESULTS_DIR / "i_in_sample.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))


def holdout(variant: str):
    marker = OUT_DIR / "ho" / "DONE"
    if marker.exists():
        sys.exit("Hold-out wurde bereits ausgewertet (data/i/ho/DONE) – kein zweiter Lauf.")
    m_is = stats(load("is", variant), IS_YEARS)
    if not all(ok for _, _, ok in checks_is(m_is, IS_YEARS)):
        sys.exit(f"{variant} hat die In-Sample-Kriterien nicht erfüllt – kein Hold-out.")
    marker.parent.mkdir(parents=True, exist_ok=True)
    marker.write_text(f"T41 {variant} {date.today().isoformat()}\n")
    rows = run_model_i(variant, load_index("SPXUSD"), date(2024, 1, 1), date(2026, 12, 31))
    save(rows, "ho", variant)
    m = stats(rows, HO_YEARS)
    lo, hi = cluster_bootstrap_ci(m_is["net_arr"], m_is["month_arr"])
    checks = [("Mittleres Netto-Tagesergebnis > 0", f"{m['E']:+.2f} bp", m["E"] > 0),
              ("≥ untere 95-%-Grenze von In-Sample (Cluster-Bootstrap nach Monat)",
               f"{m['E']:+.2f} vs. IS {m_is['E']:+.2f} [{lo:+.2f}; {hi:+.2f}] bp", m["E"] >= lo)]
    lines = [f"# Modell I, Hold-out 2024–2026 (Trial T41, {variant})\n",
             f"Einmaliger Lauf vom {date.today():%d.%m.%Y}.\n"] + variant_lines(variant, m, checks)
    (RESULTS_DIR / "i_holdout.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
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
