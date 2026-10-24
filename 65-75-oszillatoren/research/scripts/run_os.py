#!/usr/bin/env python3
"""Strategies no. 65-68, 74 and 75, model OS (oscillators, divergences, Renko): in-sample runs T249-T254 with the
pre-registered acceptance check and descriptive tables, and - only for a variant that passed - the one-time
hold-out run (docs/01_Vorregistrierung.md).

Usage:
  ../smart-money-concept/research/.venv/bin/python -I research/scripts/run_os.py                   # T249-T254
  ../smart-money-concept/research/.venv/bin/python -I research/scripts/run_os.py --holdout OS-RSI  # once
"""
import argparse
import sys
from datetime import date
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from osc import DATA_DIR, RESULTS_DIR  # noqa: E402
from osc.model import LIST_NO, MAX_BARS, VARIANTS, divergence_signals, flag_signals, renko_state, run_flags  # noqa: E402
from tind.engine import DAY, run_state  # noqa: E402
from chart.engine import STOP, run_trades  # noqa: E402
from hkb.model import atr  # noqa: E402
from smc.strategy_h import SPECS, spec_for  # noqa: E402
from dbo.model import EPOCH, UNIVERSE, costs_for  # noqa: E402
from smc.data.bars import load_bars  # noqa: E402
from smc.report import cluster_bootstrap_ci, cluster_t  # noqa: E402
from smc.swaps import RateTable  # noqa: E402

IS_YEARS, HO_YEARS = range(2015, 2024), range(2024, 2027)
IS_FROM, IS_TO = (date(2015, 1, 1) - EPOCH).days, (date(2024, 1, 1) - EPOCH).days
HO_TO = (date(2027, 1, 1) - EPOCH).days
OUT_DIR = DATA_DIR / "os"
SEC = {"D1": 86400, "H1": 3600, "H4": 14400}
NAMES = {"SPXUSD": "US500", "NSXUSD": "US100", "FRXEUR": "FRA40", "UKXGBP": "UK100", "JPXJPY": "JP225",
         "HKXHKD": "HK50", "AUXAUD": "AUS200", "BCOUSD": "Brent", "XAGUSD": "Silber"}
CLASS = {**{s: "FX" for s in UNIVERSE[:7]}, "XAUUSD": "Metalle", "XAGUSD": "Metalle", "BCOUSD": "Öl",
         **{s: "Indizes" for s in ("SPXUSD", "NSXUSD", "FRXEUR", "UKXGBP", "JPXJPY", "HKXHKD", "AUXAUD")}}


def to_date(d: int) -> date:
    return date.fromordinal(EPOCH.toordinal() + int(d))


def tval(x: np.ndarray) -> float:
    return float(x.mean() / (x.std(ddof=1) / np.sqrt(len(x)))) if len(x) > 2 else np.nan


def load_all() -> dict:
    out = {}
    for s in UNIVERSE:
        m5 = load_bars(s, "M5")
        out[s] = ({"H1": load_bars(s, "H1"), "H4": load_bars(s, "H4")}, m5, costs_for(s, m5))
    return out


def run_symbol(variant: str, symbol: str, bars: dict, m5: np.ndarray, cost, rates: RateTable, day_from: int,
               day_to: int) -> np.ndarray:
    tf = VARIANTS[variant]
    b = bars[tf][bars[tf]["ts"] < day_to * DAY]
    cfd = spec_for(symbol, m5) if symbol in SPECS else None
    if variant == "OS-RENKO":
        return run_state(symbol, b, SEC[tf], cost, rates, cfd, renko_state(b["c"], atr(b["h"], b["l"], b["c"], 14)),
                         day_from)
    if variant == "OS-DIV":
        sig, stop, a = divergence_signals(b)
        return run_trades(symbol, b, SEC[tf], cost, rates, cfd, sig, stop, a, day_from, 2.0, 30)
    sig, xl, xs = flag_signals(variant, b)
    return run_flags(symbol, b, SEC[tf], cost, rates, cfd, sig, xl, xs, MAX_BARS[variant], day_from)


def run_all(variant: str, data: dict, rates: RateTable, day_from: int, day_to: int) -> tuple[dict, np.ndarray]:
    by_sym = {s: run_symbol(variant, s, b, m5, cost, rates, day_from, day_to) for s, (b, m5, cost) in data.items()}
    days = np.unique(np.concatenate([b["H4"]["ts"] // DAY for b, _, _ in data.values()]))
    days = days[(days >= day_from) & (days < day_to) & ((days + 3) % 7 < 5)]
    return by_sym, days


def stats(by_sym: dict, all_days: np.ndarray, years) -> dict:
    tr = np.concatenate(list(by_sym.values()))
    idx = np.searchsorted(all_days, np.clip(tr["exit_day"], all_days[0], all_days[-1]))
    net, cost, gross, swap = (np.bincount(idx, tr[k], len(all_days)) for k in ("net_bp", "cost_bp", "gross_bp", "swap_bp"))
    ds = [to_date(d) for d in all_days]
    yr = np.array([d.year for d in ds])
    month = np.array([d.year * 12 + d.month for d in ds])
    m = {"n": len(net), "trades": len(tr), "E": float(net.mean()), "sd": float(net.std(ddof=1)),
         "gross": float(gross.mean()), "cost": float(cost.mean()), "swap": float(swap.mean()),
         "E_2x": float((net - cost).mean()), "t_iid": tval(net), "t_week": cluster_t(net, (all_days + 3) // 7),
         "t_month": cluster_t(net, month), "hit": float((tr["net_bp"] > 0).mean()),
         "stops": float((tr["exit_type"] == STOP).mean()), "R_net": float(tr["r_net"].mean()),
         "R_gross": float(np.mean(tr["gross_bp"] / (tr["notional"] * tr["r_bp"]))),
         "bars": float(tr["bars"].mean()), "long": float((tr["dir"] == 1).mean())}
    m["t"] = min(m["t_iid"], m["t_week"], m["t_month"])
    nyears = max(1, len(set(yr.tolist())))
    m["ann"] = m["E"] * len(net) / nyears / 100
    m["sharpe"] = m["E"] / m["sd"] * np.sqrt(len(net) / nyears)
    m["by_year"] = {y: (int((yr == y).sum()), float(net[yr == y].sum()) / 100) for y in years}
    m["years_pos"] = sum(1 for k, s in m["by_year"].values() if k and s > 0)
    m["by_sym"] = {s: (len(r), float(r["net_bp"].sum()) / 100 / len(years),
                       float(r["r_net"].mean()) if len(r) else np.nan) for s, r in by_sym.items()}
    m["sym_pos"] = sum(1 for _, s, _ in m["by_sym"].values() if s > 0)
    m["by_class"] = {}
    for s, (k, p, _) in m["by_sym"].items():
        a = m["by_class"].setdefault(CLASS[s], [0, 0.0])
        a[0] += k
        a[1] += p
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
    out = [f"## {name} (Nr. {LIST_NO[name]}, {VARIANTS[name]})\n", "| Kennzahl | Wert |", "|---|---|",
           f"| Handelstage / Trades | {m['n']:,} / {m['trades']:,} |",
           f"| Netto je Tag (bp des Kapitals, Portfolio) | {m['E']:+.2f} bp (σ {m['sd']:.1f} bp) |",
           f"| vor Kosten je Tag | {m['gross']:+.2f} bp |",
           f"| Handelskosten + Swap-Belastung je Tag (Swap netto) | {m['cost']:.2f} bp ({m['swap']:+.2f} bp) |",
           f"| Rendite p. a. (netto, 0,25 % Risiko je Trade) | {m['ann']:+.2f} % |",
           f"| Sharpe Ratio p. a. (netto) | {m['sharpe']:.2f} |",
           f"| t-Wert iid / Woche / Monat | {m['t_iid']:.2f} / {m['t_week']:.2f} / {m['t_month']:.2f} |",
           f"| Ø R je Trade vor / nach Kosten | {m['R_gross']:+.3f} / {m['R_net']:+.3f} |",
           f"| Trefferquote / Anteil Stops / Anteil Long | {m['hit']:.0%} / {m['stops']:.0%} / {m['long']:.0%} |",
           f"| Ø Haltedauer | {m['bars']:.1f} Kerzen ({VARIANTS[name]}) |",
           f"| bei doppelten Kosten | {m['E_2x']:+.2f} bp/Tag |", "",
           "| Kriterium | Ergebnis | erfüllt |", "|---|---|---|"]
    out += [f"| {c} | {v} | {'ja' if ok else '**nein**'} |" for c, v, ok in checks]
    out += ["", f"**{name}: {'alle Kriterien erfüllt' if passed else 'nicht bestanden'}.**\n",
            "| Jahr | Tage | Netto % |", "|---|---|---|"]
    out += [f"| {y} | {k} | {s:+.2f} |" for y, (k, s) in m["by_year"].items()]
    out += ["", "| Anlageklasse | Trades | Netto % p. a. |", "|---|---|---|"]
    out += [f"| {c} | {k} | {p:+.2f} |" for c, (k, p) in m["by_class"].items()]
    out += ["", "| Instrument | Trades | Netto % p. a. | Ø R netto |", "|---|---|---|---|"]
    out += [f"| {NAMES.get(s, s)} | {k} | {p:+.2f} | {r:+.3f} |" for s, (k, p, r) in m["by_sym"].items()]
    return out + [""]


def in_sample():
    data, rates = load_all(), RateTable.load()
    lines = ["# Modell OS (Oszillatoren, Divergenzen, Renko), In-Sample 2015–2023 (Trial T249–T254)\n",
             f"Lauf vom {date.today():%d.%m.%Y}. Regeln laut `docs/01_Vorregistrierung.md`, Code `research/osc/`. "
             f"{len(UNIVERSE)} Instrumente; Einstieg zur nächsten Eröffnung, Stop 2 ATR14 (Renko: Notfall-Stop 3 ATR14, "
             "Divergenz: hinter dem Swing, Ziel 2R); 0,25 % Risiko je Trade. Netto = nach Spread, Slippage, Kommission und Swaps; Ergebnis "
             "eines Trades am Tag des Ausstiegs; Portfolio = Summe aller Instrumente je Tag.\n"]
    verdict = {}
    for v in VARIANTS:
        m = stats(*run_all(v, data, rates, IS_FROM, IS_TO), IS_YEARS)
        checks = checks_is(m, IS_YEARS)
        verdict[v] = (m, all(ok for _, _, ok in checks))
        lines += variant_lines(v, m, checks)
    lines += ["## Übersicht\n", "| Variante | Nr. | TF | Trades | Netto bp/Tag | vor Kosten bp/Tag | Ø R vor / nach Kosten | t | Jahre + | Instr. + |",
              "|---|---|---|---|---|---|---|---|---|---|"]
    for v, (m, _) in verdict.items():
        lines.append(f"| {v} | {LIST_NO[v]} | {VARIANTS[v]} | {m['trades']:,} | {m['E']:+.2f} | {m['gross']:+.2f} | "
                     f"{m['R_gross']:+.3f} / {m['R_net']:+.3f} | {m['t']:+.2f} | {m['years_pos']} | {m['sym_pos']} |")
    lines.append("")
    passed = [v for v, (_, ok) in verdict.items() if ok]
    if passed:
        lines.append(f"**Ergebnis:** bestanden: {', '.join(passed)}; Hold-out je bestandener Variante.")
    else:
        lines.append("**Ergebnis: Keine Variante erfüllt alle In-Sample-Kriterien. Strategien Nr. 65–68, 74 und 75 sind "
                     "gescheitert; der Hold-out bleibt unberührt.**")
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    (RESULTS_DIR / "os_in_sample.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))


def holdout(variant: str):
    marker = OUT_DIR / "ho" / f"DONE_{variant}"
    if marker.exists():
        sys.exit(f"Hold-out für {variant} wurde bereits ausgewertet ({marker}) – kein zweiter Lauf.")
    data, rates = load_all(), RateTable.load()
    m_is = stats(*run_all(variant, data, rates, IS_FROM, IS_TO), IS_YEARS)
    if not all(ok for _, _, ok in checks_is(m_is, IS_YEARS)):
        sys.exit(f"{variant} hat die In-Sample-Kriterien nicht erfüllt – kein Hold-out.")
    marker.parent.mkdir(parents=True, exist_ok=True)
    marker.write_text(f"{variant} {date.today().isoformat()}\n")
    m = stats(*run_all(variant, data, rates, IS_TO, HO_TO), HO_YEARS)
    lo, hi = cluster_bootstrap_ci(m_is["net_arr"], m_is["month_arr"])
    checks = [("Mittleres Netto-Tagesergebnis > 0", f"{m['E']:+.2f} bp", m["E"] > 0),
              ("≥ untere 95-%-Grenze von In-Sample (Cluster-Bootstrap nach Monat)",
               f"{m['E']:+.2f} vs. IS {m_is['E']:+.2f} [{lo:+.2f}; {hi:+.2f}] bp", m["E"] >= lo)]
    lines = [f"# Modell OS, Hold-out 2024–2026 ({variant})\n",
             f"Einmaliger Lauf vom {date.today():%d.%m.%Y}.\n"] + variant_lines(variant, m, checks)
    (RESULTS_DIR / f"os_holdout_{variant}.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
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
