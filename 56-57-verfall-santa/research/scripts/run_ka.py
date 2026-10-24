#!/usr/bin/env python3
"""Strategies no. 56 and 57, model KA (options expiry, Santa rally): in-sample runs T201 (K-OPEX), T202 (K-POST) and
T203 (K-SANTA) with the pre-registered acceptance check and descriptive tables, and - only for a variant that
passed - the one-time hold-out run (docs/01_Vorregistrierung.md).

Usage:
  ../smart-money-concept/research/.venv/bin/python -I research/scripts/run_ka.py                  # T201-T203
  ../smart-money-concept/research/.venv/bin/python -I research/scripts/run_ka.py --holdout K-OPEX  # once
"""
import argparse
import sys
from datetime import date
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from cal import DATA_DIR, RESULTS_DIR  # noqa: E402
from cal.model import VARIANTS, run_model_ka  # noqa: E402
from fomc.model import EPOCH, Index  # noqa: E402
from smc.data.bars import load_bars  # noqa: E402
from smc.report import cluster_bootstrap_ci, cluster_t  # noqa: E402
from smc.strategy_h import spec_for  # noqa: E402
from smc.swaps import RateTable  # noqa: E402

IS_YEARS, HO_YEARS = range(2015, 2024), range(2024, 2027)
OUT_DIR = DATA_DIR / "ka"


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


def in_sample():
    rates = RateTable.load()
    lines = ["# Modell KA (Verfall, Santa Rally), In-Sample 2015–2023 (Trial T201 K-OPEX, T202 K-POST, T203 K-SANTA)\n",
             f"Lauf vom {date.today():%d.%m.%Y}. Regeln laut `docs/01_Vorregistrierung.md`, Code `research/cal/`. "
             "US500, NYSE-Handelstage, Kurse um 15:55 New York, Position 1 × Kapital mit Notfall-Stop 3 ATR14 (D1). "
             "Netto = nach Spread (FTMO-Durchschnitt), Slippage (¼ Spread je Ausführung) und Swaps; Ergebnisse in "
             "Basispunkten.\n"]
    spx, ndx = load_index("SPXUSD"), load_index("NSXUSD")
    verdict = {}
    for v in VARIANTS:
        rows = run_model_ka(v, spx, 2015, 2023, rates)
        m = stats(rows, IS_YEARS)
        checks = checks_is(m, IS_YEARS)
        verdict[v] = (m, all(ok for _, _, ok in checks))
        lines += variant_lines(v, m, checks)
    lines += ["## Beschreibend\n", "| Auswertung | Ereignisse | Netto Ø bp | vor Kosten Ø bp | t | Jahre positiv |",
              "|---|---|---|---|---|---|"]
    for v in VARIANTS:
        m = stats(run_model_ka(v, ndx, 2015, 2023, rates), IS_YEARS)
        lines.append(f"| US100 {v} | {m['n']} | {m['E']:+.1f} | {m['gross']:+.1f} | {m['t_iid']:+.2f} | {m['years_pos']} von 9 |")
    for v in ("K-OPEX", "K-POST"):
        rows = run_model_ka(v, spx, 2015, 2023, rates)
        q = np.isin(month_of(rows["day"]) if v == "K-OPEX" else month_of(rows["day"] - 7), [3, 6, 9, 12])
        for lbl, sel in (("Quartalsverfall", q), ("übrige Monate", ~q)):
            x = rows[sel]
            lines.append(f"| US500 {v}, {lbl} | {len(x)} | {x['net_bp'].mean():+.1f} | {x['gross_bp'].mean():+.1f} | "
                         f"{tval(x['net_bp']):+.2f} | – |")
    lines.append("")
    passed = [v for v, (_, ok) in verdict.items() if ok]
    lines.append(f"**Ergebnis:** bestanden: {', '.join(passed)}; Artefakt-Prüfung und Hold-out folgen." if passed else
                 "**Ergebnis: Keine Variante erfüllt alle In-Sample-Kriterien. Strategien Nr. 56 und 57 sind "
                 "gescheitert; der Hold-out bleibt unberührt.**")
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    (RESULTS_DIR / "ka_in_sample.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))


def holdout(variant: str):
    marker = OUT_DIR / "ho" / f"DONE_{variant}"
    if marker.exists():
        sys.exit(f"Hold-out für {variant} wurde bereits ausgewertet ({marker}) – kein zweiter Lauf.")
    rates = RateTable.load()
    spx = load_index("SPXUSD")
    m_is = stats(run_model_ka(variant, spx, 2015, 2023, rates), IS_YEARS)
    if not all(ok for _, _, ok in checks_is(m_is, IS_YEARS)):
        sys.exit(f"{variant} hat die In-Sample-Kriterien nicht erfüllt – kein Hold-out.")
    marker.parent.mkdir(parents=True, exist_ok=True)
    marker.write_text(f"{variant} {date.today().isoformat()}\n")
    m = stats(run_model_ka(variant, spx, 2024, 2026, rates), HO_YEARS)
    lo, hi = cluster_bootstrap_ci(m_is["net_arr"], m_is["days_arr"])
    checks = [("Mittleres Netto-Ergebnis je Ereignis > 0", f"{m['E']:+.1f} bp", m["E"] > 0),
              ("≥ untere 95-%-Grenze von In-Sample (Bootstrap über Ereignisse)",
               f"{m['E']:+.1f} vs. IS {m_is['E']:+.1f} [{lo:+.1f}; {hi:+.1f}] bp", m["E"] >= lo)]
    lines = [f"# Modell KA, Hold-out 2024–2026 ({variant})\n",
             f"Einmaliger Lauf vom {date.today():%d.%m.%Y}.\n"] + variant_lines(variant, m, checks)
    (RESULTS_DIR / f"ka_holdout_{variant}.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
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
