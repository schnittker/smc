#!/usr/bin/env python3
"""Strategies no. 46 and 47, model Y (currency strength): in-sample runs T156 (Y-ASIA), T157 (Y-LDN) and T158
(Y-USDB) with the pre-registered acceptance check and descriptive tables, and - only for a variant that passed - the
one-time hold-out run (docs/01_Vorregistrierung.md).

Usage:
  ../smart-money-concept/research/.venv/bin/python -I research/scripts/run_y.py                   # T156-T158
  ../smart-money-concept/research/.venv/bin/python -I research/scripts/run_y.py --holdout Y-ASIA  # once
"""
import argparse
import sys
from collections import Counter
from datetime import date
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from cst import DATA_DIR, RESULTS_DIR  # noqa: E402
from cst.model import CCYS, PAIRS, STOP, VARIANTS, run_basket, run_session  # noqa: E402
from dbo.model import EPOCH, Costs  # noqa: E402
from smc.data.bars import load_bars  # noqa: E402
from smc.report import cluster_bootstrap_ci, cluster_t  # noqa: E402
from smc.swaps import RateTable  # noqa: E402

IS_YEARS, HO_YEARS = range(2015, 2024), range(2024, 2027)
IS, HO = (date(2015, 1, 1), date(2023, 12, 31)), (date(2024, 1, 1), date(2026, 12, 31))
OUT_DIR = DATA_DIR / "y"


def to_date(d: int) -> date:
    return date.fromordinal(EPOCH.toordinal() + int(d))


def tval(x: np.ndarray) -> float:
    return float(x.mean() / (x.std(ddof=1) / np.sqrt(len(x)))) if len(x) > 2 else np.nan


def load_all() -> dict:
    return {s: (load_bars(s, "H1"), Costs("fx", s)) for s in PAIRS}


def run(variant: str, data: dict, rates: RateTable, period: tuple[date, date]) -> np.ndarray:
    if variant == "Y-USDB":
        return run_basket(data, rates, (period[0] - EPOCH).days, (period[1] - EPOCH).days + 1)
    lim = (period[1] - EPOCH).days + 1
    cut = {s: (b[b["ts"] < lim * 86400], c) for s, (b, c) in data.items()}
    return run_session(variant, cut, rates, *period)


def stats(tr: np.ndarray, period: tuple[date, date], years) -> dict:
    lo, hi = (period[0] - EPOCH).days, (period[1] - EPOCH).days + 1
    all_days = np.arange(lo, hi)
    all_days = all_days[(all_days + 3) % 7 < 5]
    idx = np.searchsorted(all_days, np.clip(tr["exit_day"], all_days[0], all_days[-1]))
    net, cost, gross = (np.bincount(idx, tr[k], len(all_days)) for k in ("net_bp", "cost_bp", "gross_bp"))
    ds = [to_date(d) for d in all_days]
    yr = np.array([d.year for d in ds])
    month = np.array([d.year * 12 + d.month for d in ds])
    m = {"n": len(net), "trades": len(tr), "E": float(net.mean()), "sd": float(net.std(ddof=1)),
         "gross": float(gross.mean()), "cost": float(cost.mean()), "E_2x": float((net - cost).mean()),
         "t_iid": tval(net), "t_week": cluster_t(net, (all_days + 3) // 7), "t_month": cluster_t(net, month),
         "hit": float((tr["net_bp"] > 0).mean()), "stops": float((tr["exit_type"] == STOP).mean()),
         "R_net": float(tr["r_net"].mean()), "R_gross": float(np.mean(tr["gross_bp"] / (tr["notional"] * tr["r_bp"]))),
         "bars": float(tr["bars"].mean())}
    m["t"] = min(m["t_iid"], m["t_week"], m["t_month"])
    nyears = max(1, len(set(yr.tolist())))
    m["ann"] = m["E"] * len(net) / nyears / 100
    m["sharpe"] = m["E"] / m["sd"] * np.sqrt(len(net) / nyears)
    m["by_year"] = {y: (int((yr == y).sum()), float(net[yr == y].sum()) / 100) for y in years}
    m["years_pos"] = sum(1 for k, s in m["by_year"].values() if k and s > 0)
    m["by_ccy"] = {}
    for ci, c in enumerate(CCYS):
        sel = (tr["buy"] == ci) | (tr["sell"] == ci)
        m["by_ccy"][c] = (int(sel.sum()), int((tr["buy"] == ci).sum()), int((tr["sell"] == ci).sum()),
                          float(tr["net_bp"][sel].sum()) / 100 / len(years))
    m["ccy_pos"] = sum(1 for _, _, _, p in m["by_ccy"].values() if p > 0)
    m["pairs"] = Counter(PAIRS[i] for i in tr["pair"]).most_common(8)
    m["net_arr"], m["month_arr"] = net, month
    return m


def checks_is(m: dict, years) -> list:
    return [("Mittleres Netto-Tagesergebnis > 0 mit t ≥ 3,0 (kleinster aus iid / Woche / Monat)",
             f"{m['E']:+.2f} bp/Tag, t = {m['t']:.2f}", m["E"] > 0 and m["t"] >= 3.0),
            (f"≥ 6 von {len(years)} Jahren positiv", f"{m['years_pos']} von {len(years)}", m["years_pos"] >= 6),
            ("≥ 60 % der 8 Währungen positiv", f"{m['ccy_pos']} von 8", m["ccy_pos"] >= 0.6 * 8),
            ("bei doppelten Kosten > 0", f"{m['E_2x']:+.2f} bp/Tag", m["E_2x"] > 0)]


def variant_lines(name: str, m: dict, checks: list) -> list[str]:
    passed = all(ok for _, _, ok in checks)
    out = [f"## {name}\n", "| Kennzahl | Wert |", "|---|---|",
           f"| Werktage / Trades | {m['n']:,} / {m['trades']:,} |",
           f"| Netto je Tag (bp des Kapitals, Portfolio) | {m['E']:+.2f} bp (σ {m['sd']:.1f} bp) |",
           f"| vor Kosten je Tag | {m['gross']:+.2f} bp |",
           f"| Handelskosten + Swap-Belastung je Tag | {m['cost']:.2f} bp |",
           f"| Rendite p. a. (netto, 0,25 % Risiko je Trade) | {m['ann']:+.2f} % |",
           f"| Sharpe Ratio p. a. (netto) | {m['sharpe']:.2f} |",
           f"| t-Wert iid / Woche / Monat | {m['t_iid']:.2f} / {m['t_week']:.2f} / {m['t_month']:.2f} |",
           f"| Ø R je Trade vor / nach Kosten | {m['R_gross']:+.3f} / {m['R_net']:+.3f} |",
           f"| Trefferquote / Anteil Stops | {m['hit']:.0%} / {m['stops']:.0%} |",
           f"| Ø Haltedauer | {m['bars']:.1f} H1-Kerzen |",
           f"| bei doppelten Kosten | {m['E_2x']:+.2f} bp/Tag |", "",
           "| Kriterium | Ergebnis | erfüllt |", "|---|---|---|"]
    out += [f"| {c} | {v} | {'ja' if ok else '**nein**'} |" for c, v, ok in checks]
    out += ["", f"**{name}: {'alle Kriterien erfüllt' if passed else 'nicht bestanden'}.**\n",
            "| Jahr | Tage | Netto % |", "|---|---|---|"]
    out += [f"| {y} | {k} | {s:+.2f} |" for y, (k, s) in m["by_year"].items()]
    out += ["", "| Währung | Trades | gekauft | verkauft | Netto % p. a. |", "|---|---|---|---|---|"]
    out += [f"| {c} | {k} | {b} | {s} | {p:+.2f} |" for c, (k, b, s, p) in m["by_ccy"].items()]
    out += ["", "Häufigste Paare: " + ", ".join(f"{p} ({k})" for p, k in m["pairs"]), ""]
    return out


def in_sample():
    data, rates = load_all(), RateTable.load()
    lines = ["# Modell Y (Währungsstärke), In-Sample 2015–2023 (Trial T156 Y-ASIA, T157 Y-LDN, T158 Y-USDB)\n",
             f"Lauf vom {date.today():%d.%m.%Y}. Regeln laut `docs/01_Vorregistrierung.md`, Code `research/cst/`. "
             "Stärke der 8 Währungen aus den 7 USD-Paaren; Y-ASIA/Y-LDN: stärkste gegen schwächste Währung bis 16:00 "
             "London; Y-USDB: Fade währungsspezifischer Abweichungen (|z| > 2). Stop 2 ATR14 H1, 0,25 % Risiko je "
             "Trade. Netto = nach Spread, Slippage, Kommission und Swaps; Ergebnis am Tag des Ausstiegs.\n"]
    verdict = {}
    for v in VARIANTS:
        m = stats(run(v, data, rates, IS), IS, IS_YEARS)
        checks = checks_is(m, IS_YEARS)
        verdict[v] = all(ok for _, _, ok in checks)
        lines += variant_lines(v, m, checks)
    passed = [v for v, ok in verdict.items() if ok]
    lines.append(f"**Ergebnis:** bestanden: {', '.join(passed)}; Artefakt-Prüfung und Hold-out folgen." if passed else
                 "**Ergebnis: Keine Variante erfüllt alle In-Sample-Kriterien. Strategien Nr. 46 und 47 sind "
                 "gescheitert; der Hold-out bleibt unberührt.**")
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    (RESULTS_DIR / "y_in_sample.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))


def holdout(variant: str):
    marker = OUT_DIR / "ho" / f"DONE_{variant}"
    if marker.exists():
        sys.exit(f"Hold-out für {variant} wurde bereits ausgewertet ({marker}) – kein zweiter Lauf.")
    data, rates = load_all(), RateTable.load()
    m_is = stats(run(variant, data, rates, IS), IS, IS_YEARS)
    if not all(ok for _, _, ok in checks_is(m_is, IS_YEARS)):
        sys.exit(f"{variant} hat die In-Sample-Kriterien nicht erfüllt – kein Hold-out.")
    marker.parent.mkdir(parents=True, exist_ok=True)
    marker.write_text(f"{variant} {date.today().isoformat()}\n")
    m = stats(run(variant, data, rates, HO), HO, HO_YEARS)
    lo, hi = cluster_bootstrap_ci(m_is["net_arr"], m_is["month_arr"])
    checks = [("Mittleres Netto-Tagesergebnis > 0", f"{m['E']:+.2f} bp", m["E"] > 0),
              ("≥ untere 95-%-Grenze von In-Sample (Cluster-Bootstrap nach Monat)",
               f"{m['E']:+.2f} vs. IS {m_is['E']:+.2f} [{lo:+.2f}; {hi:+.2f}] bp", m["E"] >= lo)]
    lines = [f"# Modell Y, Hold-out 2024–2026 ({variant})\n",
             f"Einmaliger Lauf vom {date.today():%d.%m.%Y}.\n"] + variant_lines(variant, m, checks)
    (RESULTS_DIR / f"y_holdout_{variant}.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
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
