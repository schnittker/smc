#!/usr/bin/env python3
"""Strategies no. 81, 82, 85 and 90, model ST (statistical models): in-sample runs T276-T279 with the pre-registered
acceptance check, and - only for a variant that passed - the one-time hold-out run (docs/01_Vorregistrierung.md).

Usage:
  ../smart-money-concept/research/.venv/bin/python -I research/scripts/run_st.py                  # T276-T279
  ../smart-money-concept/research/.venv/bin/python -I research/scripts/run_st.py --holdout ST-HMM  # once
"""
import argparse
import sys
from concurrent.futures import ProcessPoolExecutor
from datetime import date
from functools import partial
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from stm import DATA_DIR, RESULTS_DIR  # noqa: E402
from stm.model import VARIANTS, run_symbol, year_of  # noqa: E402
from brk.model import CFDS  # noqa: E402
from carry.model import CarrySpec  # noqa: E402
from smc.config import SYMBOLS  # noqa: E402
from smc.data.bars import load_bars  # noqa: E402
from smc.report import cluster_bootstrap_ci, cluster_t  # noqa: E402
from smc.strategy_g import ANNUAL, daily_prices  # noqa: E402
from smc.strategy_h import spec_for  # noqa: E402
from smc.swaps import RateTable  # noqa: E402

IS_FROM, IS_TO = (date(2015, 1, 1) - date(1970, 1, 1)).days, (date(2024, 1, 1) - date(1970, 1, 1)).days
HO_TO = (date(2027, 1, 1) - date(1970, 1, 1)).days
IS_YEARS, HO_YEARS = range(2015, 2024), range(2024, 2027)
OUT_DIR = DATA_DIR / "st"
UNIVERSE = tuple(SYMBOLS) + CFDS
LIST_NO = {"ST-HMM": 81, "ST-GARCH": 82, "ST-KNN": 85, "ST-GOLD": 90}
MIN_POSITION_DAYS = 250


def prices(symbol: str):
    m5 = load_bars(symbol, "M5")
    if symbol in CFDS:
        spec = spec_for(symbol, m5)
        return spec, daily_prices(m5, spec.signal_time, spec.mark_time)
    return CarrySpec(symbol), daily_prices(m5)


def load_prices(day_to: int) -> tuple[dict, dict]:
    with ProcessPoolExecutor(6) as ex:
        res = dict(zip(UNIVERSE, ex.map(prices, UNIVERSE)))
    specs = {s: r[0] for s, r in res.items()}
    px = {s: {k: v[r[1]["day"] < day_to] for k, v in r[1].items()} for s, r in res.items()}
    return specs, px


def _one(args, variant, rates, years):
    spec, px = args
    return run_symbol(variant, spec, px, rates, years[0], years[-1])


def run_all(variant: str, specs: dict, px: dict, rates: RateTable, years) -> np.ndarray:
    syms = ("XAUUSD",) if variant == "ST-GOLD" else UNIVERSE
    with ProcessPoolExecutor(6) as ex:
        parts = list(ex.map(partial(_one, variant=variant, rates=rates, years=list(years)),
                            [(specs[s], px[s]) for s in syms]))
    return np.concatenate(parts)


def stats(rows: np.ndarray, lo: int, hi: int, years) -> dict:
    rows = rows[(rows["day"] >= lo) & (rows["day"] < hi)]
    days, inv = np.unique(rows["day"], return_inverse=True)
    net, cost = np.bincount(inv, rows["net"]), np.bincount(inv, rows["cost"])
    n, sd = len(net), net.std(ddof=1)
    scale = 0.10 / (sd * np.sqrt(ANNUAL)) if sd > 0 else np.nan
    month = np.asarray(days * 86400, dtype="datetime64[s]").astype("datetime64[M]").astype(np.int64)
    m = {"days": n, "E": float(net.mean()), "sd": float(sd), "E_2x": float((net - cost).mean()),
         "t_iid": float(net.mean() / (sd / np.sqrt(n))), "t_week": cluster_t(net, (days + 3) // 7),
         "t_month": cluster_t(net, month), "sharpe": float(net.mean() / sd * np.sqrt(ANNUAL)),
         "ret10": float(net.mean() * scale * ANNUAL), "scale": scale,
         "pnl10": float(rows["pnl"].sum() * scale / (n / ANNUAL)), "swap10": float(rows["swap"].sum() * scale / (n / ANNUAL)),
         "trade10": float(rows["trade_cost"].sum() * scale / (n / ANNUAL)),
         "gross_exposure": float(np.bincount(inv, np.abs(rows["w"])).mean()), "net_arr": net, "month_arr": month}
    m["t"] = min(m["t_iid"], m["t_week"], m["t_month"])
    yr = year_of(days)
    m["by_year"] = {y: float(net[yr == y].sum() * scale) for y in years}
    m["years_pos"] = sum(1 for v in m["by_year"].values() if v > 0)
    m["halves"] = (float(net[yr <= 2019].mean()) if (yr <= 2019).any() else np.nan,
                   float(net[yr >= 2020].mean()) if (yr >= 2020).any() else np.nan)
    m["by_symbol"] = {}
    for s in np.unique(rows["symbol"]):
        sel = rows["symbol"] == s
        if (sel & (rows["w"] != 0)).sum() >= MIN_POSITION_DAYS:
            m["by_symbol"][str(s)] = float(rows["net"][sel].sum() * scale)
    m["sym_pos"] = sum(1 for v in m["by_symbol"].values() if v > 0)
    return m


def checks_is(variant: str, m: dict, years) -> list:
    out = [("Mittleres Netto-Tagesergebnis > 0 mit t ≥ 3,0 (kleinster aus iid / Woche / Monat)",
            f"t = {m['t']:.2f} (Sharpe {m['sharpe']:.2f})", m["E"] > 0 and m["t"] >= 3.0),
           (f"≥ 6 von {len(years)} Jahren positiv", f"{m['years_pos']} von {len(years)}", m["years_pos"] >= 6)]
    if variant == "ST-GOLD":
        a, b = m["halves"]
        out.append(("beide Teilzeiträume 2015–2019 und 2020–2023 positiv", f"{a * 1e4:+.2f} / {b * 1e4:+.2f} bp/Tag",
                    a > 0 and b > 0))
    else:
        k = len(m["by_symbol"])
        out.append((f"≥ 60 % der Instrumente (≥ {MIN_POSITION_DAYS} Positionstage) positiv", f"{m['sym_pos']} von {k}",
                    k > 0 and m["sym_pos"] >= 0.6 * k))
    out.append(("bei doppelten Kosten > 0", f"{m['E_2x'] * m['scale'] * ANNUAL:+.2%} p. a. bei 10 % Vol.", m["E_2x"] > 0))
    return out


def report(name: str, m: dict, checks: list) -> list[str]:
    ok = all(c for _, _, c in checks)
    out = [f"## {name} (Nr. {LIST_NO[name]})\n", "| Kennzahl | Wert |", "|---|---|",
           f"| Handelstage | {m['days']:,} |", f"| Sharpe Ratio p. a. (netto) | {m['sharpe']:.2f} |",
           f"| t-Wert iid / Woche / Monat | {m['t_iid']:.2f} / {m['t_week']:.2f} / {m['t_month']:.2f} |",
           f"| Rendite p. a. bei 10 % Volatilität | {m['ret10']:+.2%} |",
           f"| Zerlegung p. a. bei 10 % Vol.: Kurs / Swaps / Handel | {m['pnl10']:+.2%} / {m['swap10']:+.2%} / {-m['trade10']:+.2%} |",
           f"| Ø Brutto-Exposure (unskaliert) | {m['gross_exposure']:.2f} |", "",
           "| Kriterium | Ergebnis | erfüllt |", "|---|---|---|"]
    out += [f"| {c} | {v} | {'ja' if k else '**nein**'} |" for c, v, k in checks]
    out += ["", f"**{name}: {'alle Kriterien erfüllt' if ok else 'nicht bestanden'}.**\n", "| Jahr | Rendite bei 10 % Vol. |",
            "|---|---|"]
    out += [f"| {y} | {v:+.1%} |" for y, v in m["by_year"].items()]
    return out + [""]


def in_sample():
    rates = RateTable.load()
    specs, px = load_prices(IS_TO)
    lines = ["# Modell ST (Statistische Modelle), In-Sample 2015–2023 (Trial T276–T279)\n",
             f"Lauf vom {date.today():%d.%m.%Y}. Regeln laut `docs/01_Vorregistrierung.md`, Code `research/stm/`. "
             "Tagesbuchhaltung wie Nr. 28/30 (34 Instrumente; Gold-Saison nur XAUUSD), Modelle jährlich nur mit "
             "Vorjahresdaten geschätzt. Netto = nach Handelskosten, Swaps und Gebühr.\n"]
    verdict = {}
    for v in VARIANTS:
        m = stats(run_all(v, specs, px, rates, IS_YEARS), IS_FROM, IS_TO, IS_YEARS)
        checks = checks_is(v, m, IS_YEARS)
        verdict[v] = (m, all(c for _, _, c in checks))
        lines += report(v, m, checks)
    lines += ["## Übersicht\n", "| Variante | Nr. | Sharpe | t | Rendite p. a. bei 10 % Vol. | Jahre + | Instr. + |",
              "|---|---|---|---|---|---|---|"]
    for v, (m, _) in verdict.items():
        lines.append(f"| {v} | {LIST_NO[v]} | {m['sharpe']:+.2f} | {m['t']:+.2f} | {m['ret10']:+.2%} | {m['years_pos']} | "
                     f"{m['sym_pos']} von {len(m['by_symbol'])} |")
    passed = [v for v, (_, ok) in verdict.items() if ok]
    lines += ["", f"**Ergebnis:** bestanden: {', '.join(passed)}; Artefakt-Prüfung und Hold-out folgen." if passed else
              "**Ergebnis: Keine Variante erfüllt alle In-Sample-Kriterien. Strategien Nr. 81, 82, 85 und 90 sind "
              "gescheitert; der Hold-out bleibt unberührt.**"]
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    (RESULTS_DIR / "st_in_sample.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))


def holdout(variant: str):
    marker = OUT_DIR / "ho" / f"DONE_{variant}"
    if marker.exists():
        sys.exit(f"Hold-out für {variant} wurde bereits ausgewertet ({marker}) – kein zweiter Lauf.")
    rates = RateTable.load()
    specs, px = load_prices(IS_TO)
    m_is = stats(run_all(variant, specs, px, rates, IS_YEARS), IS_FROM, IS_TO, IS_YEARS)
    if not all(c for _, _, c in checks_is(variant, m_is, IS_YEARS)):
        sys.exit(f"{variant} hat die In-Sample-Kriterien nicht erfüllt – kein Hold-out.")
    marker.parent.mkdir(parents=True, exist_ok=True)
    marker.write_text(f"{variant} {date.today().isoformat()}\n")
    specs, px = load_prices(HO_TO)
    m = stats(run_all(variant, specs, px, rates, HO_YEARS), IS_TO, HO_TO, HO_YEARS)
    lo, hi = cluster_bootstrap_ci(m_is["net_arr"], m_is["month_arr"])
    checks = [("Mittleres Netto-Tagesergebnis > 0", f"{m['E'] * 1e4:+.2f} bp", m["E"] > 0),
              ("≥ untere 95-%-Grenze von In-Sample", f"{m['E'] * 1e4:+.2f} vs. [{lo * 1e4:+.2f}; {hi * 1e4:+.2f}] bp",
               m["E"] >= lo)]
    lines = [f"# Modell ST, Hold-out 2024–2026 ({variant})\n", f"Einmaliger Lauf vom {date.today():%d.%m.%Y}.\n"]
    lines += report(variant, m, checks)
    (RESULTS_DIR / f"st_holdout_{variant}.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
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
