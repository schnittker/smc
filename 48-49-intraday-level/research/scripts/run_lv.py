#!/usr/bin/env python3
"""Strategies no. 48 and 49, model LV (intraday levels): in-sample runs T165 (LV-VA80), T166 (LV-PFADE) and T167
(LV-PBRK) with the
pre-registered acceptance check and descriptive tables, and - only for a variant that passed - the one-time
hold-out run (docs/01_Vorregistrierung.md).

Usage:
  ../smart-money-concept/research/.venv/bin/python -I research/scripts/run_lv.py                    # T165-T167
  ../smart-money-concept/research/.venv/bin/python -I research/scripts/run_lv.py --holdout LV-VA80  # once
"""
import argparse
import sys
from datetime import date
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from lvl import DATA_DIR, RESULTS_DIR  # noqa: E402
from lvl.model import EOD, PIV, STOP, TARGET, VA_IDX, VARIANTS, run_pivots, run_va80  # noqa: E402
from dbo.model import EPOCH, costs_for  # noqa: E402
from smc.data.bars import load_bars  # noqa: E402
from smc.report import cluster_bootstrap_ci, cluster_t  # noqa: E402

IS_YEARS, HO_YEARS = range(2015, 2024), range(2024, 2027)
IS = (date(2015, 1, 1), date(2023, 12, 31))
HO = (date(2024, 1, 1), date(2026, 12, 31))
OUT_DIR = DATA_DIR / "lv"
NAMES = {"SPXUSD": "US500", "NSXUSD": "US100", "FRXEUR": "FRA40", "UKXGBP": "UK100", "JPXJPY": "JP225",
         "HKXHKD": "HK50", "AUXAUD": "AUS200"}


def to_date(d: int) -> date:
    return date.fromordinal(EPOCH.toordinal() + int(d))


def tval(x: np.ndarray) -> float:
    return float(x.mean() / (x.std(ddof=1) / np.sqrt(len(x)))) if len(x) > 2 else np.nan


def load(variant: str) -> dict:
    out = {}
    for s in (VA_IDX if variant == "LV-VA80" else PIV):
        m5 = load_bars(s, "M5")
        out[s] = (m5, costs_for(s, m5))
    return out


def run(variant: str, data: dict, period: tuple[date, date]) -> dict:
    if variant == "LV-VA80":
        return {s: run_va80(s, m5, cost, *period) for s, (m5, cost) in data.items()}
    lo, hi = (period[0] - EPOCH).days, (period[1] - EPOCH).days + 1
    return {s: run_pivots(variant, m5[m5["ts"] < hi * 86400], cost, lo, hi) for s, (m5, cost) in data.items()}


def stats(by_sym: dict, years) -> dict:
    rows = np.concatenate(list(by_sym.values()))
    days, inv = np.unique(rows["day"], return_inverse=True)
    net, cost, gross = (np.bincount(inv, rows[k]) for k in ("net_bp", "cost_bp", "gross_bp"))
    ds = [to_date(d) for d in days]
    yr = np.array([d.year for d in ds])
    month = np.array([d.year * 12 + d.month for d in ds])
    tr = rows[rows["dir"] != 0]
    m = {"n": len(net), "trades": len(tr), "E": float(net.mean()), "sd": float(net.std(ddof=1)),
         "gross": float(gross.mean()), "cost": float(cost.mean()), "E_2x": float((net - cost).mean()),
         "t_iid": tval(net), "t_week": cluster_t(net, (days + 3) // 7), "t_month": cluster_t(net, month),
         "hit": float((tr["net_bp"] > 0).mean()), "R_net": float(tr["r_net"].mean()),
         "R_gross": float(np.mean(tr["gross_bp"] / (tr["notional"] * tr["r_bp"]))),
         "exits": {k: float((tr["exit_type"] == v).mean()) for k, v in (("Ziel", TARGET), ("Stop", STOP), ("Zeit", EOD))}}
    m["t"] = min(m["t_iid"], m["t_week"], m["t_month"])
    nyears = max(1, len(set(yr.tolist())))
    m["ann"] = m["E"] * len(net) / nyears / 100
    m["sharpe"] = m["E"] / m["sd"] * np.sqrt(len(net) / nyears)
    m["by_year"] = {y: (int((yr == y).sum()), float(net[yr == y].sum()) / 100) for y in years}
    m["years_pos"] = sum(1 for k, s in m["by_year"].values() if k and s > 0)
    m["by_sym"] = {s: (int((r["dir"] != 0).sum()), float(r["net_bp"].sum()) / 100 / len(years),
                       float(r["r_net"][r["dir"] != 0].mean()) if (r["dir"] != 0).any() else np.nan)
                   for s, r in by_sym.items()}
    m["sym_pos"] = sum(1 for _, s, _ in m["by_sym"].values() if s > 0)
    m["net_arr"], m["month_arr"] = net, month
    return m


def checks_is(m: dict, years) -> list:
    k = len(m["by_sym"])
    return [("Mittleres Netto-Tagesergebnis > 0 mit t ≥ 3,0 (kleinster aus iid / Woche / Monat)",
             f"{m['E']:+.2f} bp/Tag, t = {m['t']:.2f}", m["E"] > 0 and m["t"] >= 3.0),
            (f"≥ 6 von {len(years)} Jahren positiv", f"{m['years_pos']} von {len(years)}", m["years_pos"] >= 6),
            ("≥ 60 % der Instrumente positiv", f"{m['sym_pos']} von {k}", m["sym_pos"] >= 0.6 * k),
            ("bei doppelten Kosten > 0", f"{m['E_2x']:+.2f} bp/Tag", m["E_2x"] > 0)]


def variant_lines(name: str, m: dict, checks: list) -> list[str]:
    passed = all(ok for _, _, ok in checks)
    ex = m["exits"]
    out = [f"## {name}\n", "| Kennzahl | Wert |", "|---|---|",
           f"| Handelstage / Trades | {m['n']:,} / {m['trades']:,} |",
           f"| Netto je Tag (bp des Kapitals, Portfolio) | {m['E']:+.2f} bp (σ {m['sd']:.1f} bp) |",
           f"| vor Kosten je Tag | {m['gross']:+.2f} bp |",
           f"| Kosten je Tag | {m['cost']:.2f} bp |",
           f"| Rendite p. a. (netto, 0,25 % Risiko je Trade) | {m['ann']:+.2f} % |",
           f"| Sharpe Ratio p. a. (netto) | {m['sharpe']:.2f} |",
           f"| t-Wert iid / Woche / Monat | {m['t_iid']:.2f} / {m['t_week']:.2f} / {m['t_month']:.2f} |",
           f"| Ø R je Trade vor / nach Kosten | {m['R_gross']:+.3f} / {m['R_net']:+.3f} |",
           f"| Trefferquote | {m['hit']:.0%} |",
           f"| Ausstiege Ziel / Stop / Zeit | {ex['Ziel']:.0%} / {ex['Stop']:.0%} / {ex['Zeit']:.0%} |",
           f"| bei doppelten Kosten | {m['E_2x']:+.2f} bp/Tag |", "",
           "| Kriterium | Ergebnis | erfüllt |", "|---|---|---|"]
    out += [f"| {c} | {v} | {'ja' if ok else '**nein**'} |" for c, v, ok in checks]
    out += ["", f"**{name}: {'alle Kriterien erfüllt' if passed else 'nicht bestanden'}.**\n",
            "| Jahr | Tage | Netto % |", "|---|---|---|"]
    out += [f"| {y} | {k} | {s:+.2f} |" for y, (k, s) in m["by_year"].items()]
    out += ["", "| Instrument | Trades | Netto % p. a. | Ø R netto |", "|---|---|---|---|"]
    out += [f"| {NAMES.get(s, s)} | {k} | {p:+.2f} | {r:+.3f} |" for s, (k, p, r) in m["by_sym"].items()]
    return out + [""]


def in_sample():
    lines = ["# Modell LV (Intraday-Level), In-Sample 2015–2023 (Trial T165 LV-VA80, T166 LV-PFADE, T167 LV-PBRK)\n",
             f"Lauf vom {date.today():%d.%m.%Y}. Regeln laut `docs/01_Vorregistrierung.md`, Code `research/lvl/`. "
             "LV-VA80: 80-%-Regel der Value Area auf US500, US100, FRA40, UK100; LV-PFADE/LV-PBRK: klassische Pivots "
             "auf 7 Majors und 7 Indizes. 0,25 % Risiko je Trade. Netto = nach Spread, Slippage und Kommission; "
             "Portfolio = Summe je Tag.\n"]
    verdict = {}
    for v in VARIANTS:
        m = stats(run(v, load(v), IS), IS_YEARS)
        checks = checks_is(m, IS_YEARS)
        verdict[v] = all(ok for _, _, ok in checks)
        lines += variant_lines(v, m, checks)
    passed = [v for v, ok in verdict.items() if ok]
    lines.append(f"**Ergebnis:** bestanden: {', '.join(passed)}; Hold-out je bestandener Variante." if passed else
                 "**Ergebnis: Keine Variante erfüllt alle In-Sample-Kriterien. Strategien Nr. 48 und 49 sind "
                 "gescheitert; der Hold-out bleibt unberührt.**")
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    (RESULTS_DIR / "lv_in_sample.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))


def holdout(variant: str):
    marker = OUT_DIR / "ho" / f"DONE_{variant}"
    if marker.exists():
        sys.exit(f"Hold-out für {variant} wurde bereits ausgewertet ({marker}) – kein zweiter Lauf.")
    data = load(variant)
    m_is = stats(run(variant, data, IS), IS_YEARS)
    if not all(ok for _, _, ok in checks_is(m_is, IS_YEARS)):
        sys.exit(f"{variant} hat die In-Sample-Kriterien nicht erfüllt – kein Hold-out.")
    marker.parent.mkdir(parents=True, exist_ok=True)
    marker.write_text(f"{variant} {date.today().isoformat()}\n")
    m = stats(run(variant, data, HO), HO_YEARS)
    lo, hi = cluster_bootstrap_ci(m_is["net_arr"], m_is["month_arr"])
    checks = [("Mittleres Netto-Tagesergebnis > 0", f"{m['E']:+.2f} bp", m["E"] > 0),
              ("≥ untere 95-%-Grenze von In-Sample (Cluster-Bootstrap nach Monat)",
               f"{m['E']:+.2f} vs. IS {m_is['E']:+.2f} [{lo:+.2f}; {hi:+.2f}] bp", m["E"] >= lo)]
    lines = [f"# Modell LV, Hold-out 2024–2026 ({variant})\n",
             f"Einmaliger Lauf vom {date.today():%d.%m.%Y}.\n"] + variant_lines(variant, m, checks)
    (RESULTS_DIR / f"lv_holdout_{variant}.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
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
