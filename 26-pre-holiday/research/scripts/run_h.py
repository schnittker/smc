#!/usr/bin/env python3
"""Strategy no. 26, model H (pre-holiday US indices): in-sample runs T88 (H-SPX) and T89 (H-NDX) with the
pre-registered acceptance check and descriptive tables, and - only for a variant that passed - the one-time
hold-out run T90 (docs/01_Vorregistrierung.md).

Usage:
  ../smart-money-concept/research/.venv/bin/python -I research/scripts/run_h.py                   # T88 + T89
  ../smart-money-concept/research/.venv/bin/python -I research/scripts/run_h.py --holdout H-SPX    # T90, once
"""
import argparse
import sys
from datetime import date, timedelta
from pathlib import Path

import numpy as np
import pyarrow as pa
import pyarrow.parquet as pq

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from preh import DATA_DIR, RESULTS_DIR  # noqa: E402
from preh.model import VARIANTS, dn, events, run_model_h  # noqa: E402
from fomc.model import EPOCH, ROW_DTYPE, Index, ny_utc, window_bp  # noqa: E402
from tom import nyse  # noqa: E402
from smc.data.bars import load_bars  # noqa: E402
from smc.report import cluster_bootstrap_ci, cluster_t  # noqa: E402
from smc.strategy_h import spec_for  # noqa: E402
from smc.swaps import RateTable  # noqa: E402

IS_YEARS, HO_YEARS = range(2015, 2024), range(2024, 2027)
OUT_DIR = DATA_DIR / "h"


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
    return [("Mittleres Netto-Ergebnis je Ereignis > 0 mit t ≥ 3,0 (kleinster aus iid / Quartal)",
             f"{m['E']:+.1f} bp/Ereignis, t = {m['t']:.2f}", m["E"] > 0 and m["t"] >= 3.0),
            (f"≥ 6 von {len(years)} Jahren positiv", f"{m['years_pos']} von {len(years)}", m["years_pos"] >= 6),
            ("beide Teilzeiträume 2015–2019 und 2020–2023 positiv", f"{a:+.1f} / {b:+.1f} bp", a > 0 and b > 0),
            ("bei doppelten Kosten > 0", f"{m['E_2x']:+.1f} bp/Ereignis", m["E_2x"] > 0)]


def variant_lines(name: str, m: dict, checks: list) -> list[str]:
    passed = all(ok for _, _, ok in checks)
    out = [f"## {name}\n", "| Kennzahl | Wert |", "|---|---|",
           f"| Ereignisse | {m['n']} |",
           f"| Netto je Ereignis | {m['E']:+.1f} bp (σ {m['sd']:.1f} bp) |",
           f"| vor Kosten je Ereignis | {m['gross']:+.1f} bp |",
           f"| Kosten je Ereignis (davon Swap) | {m['cost']:.1f} bp ({-m['swap']:.1f} bp) |",
           f"| Sharpe Ratio p. a. (netto) | {m['sharpe']:.2f} |",
           f"| t-Wert iid / Quartal | {m['t_iid']:.2f} / {m['t_q']:.2f} |",
           f"| Anteil positiver Ereignisse | {m['hit']:.0%} |",
           f"| Notfall-Stops | {m['stops']} |",
           f"| bei doppelten Kosten | {m['E_2x']:+.1f} bp/Ereignis |", "",
           "| Kriterium | Ergebnis | erfüllt |", "|---|---|---|"]
    out += [f"| {c} | {v} | {'ja' if ok else '**nein**'} |" for c, v, ok in checks]
    out += ["", f"**{name}: {'alle Kriterien erfüllt' if passed else 'nicht bestanden'}.**\n",
            "| Jahr | Ereignisse | Netto Summe bp |", "|---|---|---|"]
    out += [f"| {y} | {k} | {tot:+.1f} |" for y, (k, tot) in m["by_year"].items()]
    return out + [""]


def comparison(idx: Index, years) -> list[str]:
    """15:55-to-15:55 return of pre-holiday days vs all other trading days, before costs."""
    days = nyse.trading_days(date(min(years), 1, 1) - timedelta(days=10), date(max(years), 12, 31))
    pre = {p for _, p, _ in events(date(min(years), 1, 1), date(max(years) + 1, 1, 31))}
    f, o = [], []
    for q, d in zip(days[:-1], days[1:]):
        if d.year not in years:
            continue
        x = window_bp(idx.m5, int(ny_utc(dn(q), 15, 55)), int(ny_utc(dn(d), 15, 55)))
        if np.isfinite(x):
            (f if d in pre else o).append(x)
    f, o = np.array(f), np.array(o)
    t_diff = (f.mean() - o.mean()) / np.sqrt(f.var(ddof=1) / len(f) + o.var(ddof=1) / len(o))
    return [f"| {idx.spec.symbol} | {len(f)} | {f.mean():+.1f} | {o.mean():+.1f} | {f.mean() - o.mean():+.1f} | {t_diff:+.2f} |"]


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
    lines = ["# Modell H (Pre-Holiday US-Indizes), In-Sample 2015–2023 (Trial T88 H-SPX, T89 H-NDX)\n",
             f"Lauf vom {date.today():%d.%m.%Y}. Regeln laut `docs/01_Vorregistrierung.md`, Code `research/preh/`. "
             "Reguläre NYSE-Feiertage 2015–2023; Long von 15:55 New York am Tag vor dem Vortag bis 15:55 am Vortag "
             "(12:55 an verkürzten Tagen). Netto = nach Spread, Slippage und Swaps; Ergebnisse in Basispunkten.\n"]
    verdict, idxs = {}, {}
    for v, sym in VARIANTS.items():
        idxs[v] = load_index(sym)
        rows = run_model_h(idxs[v], date(2015, 1, 1), date(2023, 12, 31), rates)
        save(rows, "is", v)
        m = stats(rows, IS_YEARS)
        checks = checks_is(m, IS_YEARS)
        verdict[v] = (m, all(ok for _, _, ok in checks))
        lines += variant_lines(v, m, checks)
    lines += ["## Beschreibend: Vortage gegen übrige Handelstage (15:55 bis 15:55, vor Kosten)\n",
              "| Index | Vortage | Ø Vortag bp | Ø übrige bp | Differenz | t |", "|---|---|---|---|---|---|"]
    for v in VARIANTS:
        lines += comparison(idxs[v], IS_YEARS)
    lines.append("")
    passed = [v for v, (_, ok) in verdict.items() if ok]
    if passed:
        best = max(passed, key=lambda v: verdict[v][0]["t"])
        lines.append(f"**Ergebnis:** bestanden: {', '.join(passed)}; gewählt für den Hold-out: **{best}**.")
    else:
        lines.append("**Ergebnis: Keine Variante erfüllt alle In-Sample-Kriterien. Strategie Nr. 26 ist gescheitert; "
                     "der Hold-out bleibt unberührt.**")
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    (RESULTS_DIR / "h_in_sample.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))


def holdout(variant: str):
    marker = OUT_DIR / "ho" / "DONE"
    if marker.exists():
        sys.exit("Hold-out wurde bereits ausgewertet (data/h/ho/DONE) – kein zweiter Lauf.")
    m_is = stats(load("is", variant), IS_YEARS)
    if not all(ok for _, _, ok in checks_is(m_is, IS_YEARS)):
        sys.exit(f"{variant} hat die In-Sample-Kriterien nicht erfüllt – kein Hold-out.")
    marker.parent.mkdir(parents=True, exist_ok=True)
    marker.write_text(f"T90 {variant} {date.today().isoformat()}\n")
    rows = run_model_h(load_index(VARIANTS[variant]), date(2024, 1, 1), date(2026, 12, 31), RateTable.load())
    save(rows, "ho", variant)
    m = stats(rows, HO_YEARS)
    lo, hi = cluster_bootstrap_ci(m_is["net_arr"], m_is["days_arr"])
    checks = [("Mittleres Netto-Ergebnis je Ereignis > 0", f"{m['E']:+.1f} bp", m["E"] > 0),
              ("≥ untere 95-%-Grenze von In-Sample (Bootstrap über Ereignisse)",
               f"{m['E']:+.1f} vs. IS {m_is['E']:+.1f} [{lo:+.1f}; {hi:+.1f}] bp", m["E"] >= lo)]
    lines = [f"# Modell H, Hold-out 2024–2026 (Trial T90, {variant})\n",
             f"Einmaliger Lauf vom {date.today():%d.%m.%Y}.\n"] + variant_lines(variant, m, checks)
    (RESULTS_DIR / "h_holdout.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
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
