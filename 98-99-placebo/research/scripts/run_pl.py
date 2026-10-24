#!/usr/bin/env python3
"""Controls no. 98 and 99, model PL (placebo): in-sample runs T297 (PL-RANDOM) and T298 (PL-MOON).

Usage:
  ../smart-money-concept/research/.venv/bin/python -I research/scripts/run_pl.py
"""
import sys
from datetime import date
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from plc import RESULTS_DIR  # noqa: E402
from plc.model import random_signals, run_moon  # noqa: E402
from chart.engine import DAY, run_trades  # noqa: E402
from dbo.model import UNIVERSE, costs_for  # noqa: E402
from hkb.model import atr  # noqa: E402
from brk.model import CFDS  # noqa: E402
from carry.model import CarrySpec  # noqa: E402
from smc.config import SYMBOLS  # noqa: E402
from smc.data.bars import load_bars  # noqa: E402
from smc.report import cluster_t  # noqa: E402
from smc.strategy_g import ANNUAL, daily_prices  # noqa: E402
from smc.strategy_h import SPECS, spec_for  # noqa: E402
from smc.swaps import RateTable  # noqa: E402

IS_FROM, IS_TO = (date(2015, 1, 1) - date(1970, 1, 1)).days, (date(2024, 1, 1) - date(1970, 1, 1)).days
YEARS = range(2015, 2024)


def year_of(days):
    return np.asarray(days * 86400, dtype="datetime64[s]").astype("datetime64[Y]").astype(int) + 1970


def tval(x):
    return float(x.mean() / (x.std(ddof=1) / np.sqrt(len(x))))


def random_run(rates) -> list[str]:
    by_sym = {}
    for k, s in enumerate(UNIVERSE):
        m5 = load_bars(s, "M5")
        h4 = load_bars(s, "H4")
        h4 = h4[h4["ts"] < IS_TO * DAY]
        sig = random_signals(len(h4), 98 + k)
        stop = np.where(sig == 1, 1e12, np.where(sig == -1, 0.0, np.nan))
        a = 2.0 * atr(h4["h"], h4["l"], h4["c"], 14)
        by_sym[s] = run_trades(s, h4, 14400, costs_for(s, m5), rates, spec_for(s, m5) if s in SPECS else None,
                               sig, stop, a, IS_FROM, 2.0, 30)
    tr = np.concatenate(list(by_sym.values()))
    days = np.arange(IS_FROM, IS_TO)
    days = days[(days + 3) % 7 < 5]
    idx = np.searchsorted(days, np.clip(tr["exit_day"], days[0], days[-1]))
    net, cost = np.bincount(idx, tr["net_bp"], len(days)), np.bincount(idx, tr["cost_bp"], len(days))
    month = np.asarray(days * 86400, dtype="datetime64[s]").astype("datetime64[M]").astype(np.int64)
    t = min(tval(net), cluster_t(net, (days + 3) // 7), cluster_t(net, month))
    yr = year_of(days)
    years_pos = sum(1 for y in YEARS if net[yr == y].sum() > 0)
    sym_pos = sum(1 for r in by_sym.values() if r["net_bp"].sum() > 0)
    rg = tr["gross_bp"] / (tr["notional"] * tr["r_bp"])
    ci = 1.96 * rg.std(ddof=1) / np.sqrt(len(rg))
    ok = net.mean() > 0 and t >= 3 and years_pos >= 6 and sym_pos >= 0.6 * len(by_sym) and (net - cost).mean() > 0
    return ["## PL-RANDOM (Nr. 98)\n", "| Kennzahl | Wert |", "|---|---|",
            f"| Trades | {len(tr):,} |", f"| Netto je Tag | {net.mean():+.2f} bp (t = {t:.2f}) |",
            f"| Ø R je Trade vor Kosten (95-%-Intervall) | {rg.mean():+.4f} [{rg.mean() - ci:+.4f}; {rg.mean() + ci:+.4f}] |",
            f"| Ø R je Trade netto | {tr['r_net'].mean():+.4f} |", f"| Jahre positiv / Instrumente positiv | {years_pos} von 9 / {sym_pos} von {len(by_sym)} |",
            "", f"**PL-RANDOM: {'BESTANDEN – Warnsignal für die Pipeline!' if ok else 'nicht bestanden (wie erwartet)'}.**", ""]


def moon_run(rates) -> list[str]:
    rows = []
    for s in tuple(SYMBOLS) + CFDS:
        m5 = load_bars(s, "M5")
        if s in CFDS:
            spec = spec_for(s, m5)
            px = daily_prices(m5, spec.signal_time, spec.mark_time)
        else:
            spec, px = CarrySpec(s), daily_prices(m5)
        px = {k: v[px["day"] < IS_TO] for k, v in px.items()}
        rows.append(run_moon(spec, px, rates))
    rows = np.concatenate(rows)
    rows = rows[(rows["day"] >= IS_FROM) & (rows["day"] < IS_TO)]
    days, inv = np.unique(rows["day"], return_inverse=True)
    net, cost = np.bincount(inv, rows["net"]), np.bincount(inv, rows["cost"])
    month = np.asarray(days * 86400, dtype="datetime64[s]").astype("datetime64[M]").astype(np.int64)
    t = min(tval(net), cluster_t(net, (days + 3) // 7), cluster_t(net, month))
    sharpe = net.mean() / net.std(ddof=1) * np.sqrt(ANNUAL)
    yr = year_of(days)
    years_pos = sum(1 for y in YEARS if net[yr == y].sum() > 0)
    syms = np.unique(rows["symbol"])
    sym_pos = sum(1 for s in syms if rows["net"][rows["symbol"] == s].sum() > 0)
    scale = 0.10 / (net.std(ddof=1) * np.sqrt(ANNUAL))
    pnl = rows["pnl"].sum() * scale / (len(net) / ANNUAL)
    ok = net.mean() > 0 and t >= 3 and years_pos >= 6 and sym_pos >= 0.6 * len(syms) and (net - cost).mean() > 0
    return ["## PL-MOON (Nr. 99)\n", "| Kennzahl | Wert |", "|---|---|",
            f"| Handelstage | {len(net):,} |", f"| Sharpe Ratio p. a. (netto) | {sharpe:+.2f} (t = {t:.2f}) |",
            f"| Kurs-Ergebnis p. a. bei 10 % Vol. (vor Kosten) | {pnl:+.2%} |",
            f"| Jahre positiv / Instrumente positiv | {years_pos} von 9 / {sym_pos} von {len(syms)} |", "",
            f"**PL-MOON: {'BESTANDEN – Warnsignal für die Pipeline!' if ok else 'nicht bestanden (wie erwartet)'}.**", ""]


def main():
    rates = RateTable.load()
    lines = ["# Modell PL (Placebo-Kontrollen), In-Sample 2015–2023 (Trial T297 PL-RANDOM, T298 PL-MOON)\n",
             f"Lauf vom {date.today():%d.%m.%Y}. Regeln laut `docs/01_Vorregistrierung.md`, Code `research/plc/`.\n"]
    lines += random_run(rates) + moon_run(rates)
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    (RESULTS_DIR / "pl_in_sample.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
