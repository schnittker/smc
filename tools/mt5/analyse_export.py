#!/usr/bin/env python3
"""Real FTMO trading costs from the ExportFtmoData CSV files: spreads (ticks and bar history) and swaps per symbol.

Usage: analyse_export.py <export dir> <output markdown>
"""
import csv
import sys
from pathlib import Path

import numpy as np
import pandas as pd

EXPORT, OUT = Path(sys.argv[1]), Path(sys.argv[2])
FOCUS = ["EURUSD", "GBPUSD", "USDJPY", "AUDUSD", "NZDUSD", "USDCAD", "USDCHF", "EURJPY", "GBPJPY", "EURCHF",
         "US500.cash", "US100.cash", "US30.cash", "GER40.cash", "FRA40.cash", "UK100.cash", "JP225.cash", "HK50.cash",
         "AUS200.cash", "XAUUSD", "XAGUSD", "USOIL.cash", "UKOIL.cash", "NATGAS.cash",
         "BTCUSD", "ETHUSD", "LTCUSD", "XRPUSD", "ADAUSD", "SOLUSD", "DOGEUSD", "AAPL", "MSFT", "NVDA", "TSLA"]

spec = {r["symbol"]: r for r in csv.DictReader(open(EXPORT / "symbols.csv"))}


def rates(sym, tf):
    p = EXPORT / "rates" / f"{sym}_{tf}.csv"
    if not p.exists():
        return None
    d = pd.read_csv(p)
    d["time"] = pd.to_datetime(d["time"], format="%Y.%m.%d %H:%M")
    return d


def swap_pa(s, price):
    """Annual swap (long, short) as a fraction of notional, 365 charges a year (Mon-Thu 1, triple day 3)."""
    mode, lo, sh = int(s["swap_mode"]), float(s["swap_long"]), float(s["swap_short"])
    if mode == 5:                       # interest of the current price, % p.a.
        return lo / 100, sh / 100
    if mode == 1 and price > 0:         # points per day
        pt = float(s["point"])
        return lo * pt / price * 365, sh * pt / price * 365
    return np.nan, np.nan


def tick_spread(sym):
    p = EXPORT / "ticks" / f"{sym}.csv"
    if not p.exists():
        return None
    t = pd.read_csv(p)
    t = t[(t.bid > 0) & (t.ask > t.bid)]
    rel = (t.ask - t.bid) / ((t.ask + t.bid) / 2)
    ts = pd.to_datetime(t.time_msc, unit="ms")
    # time-weighted: each quote counts for the time until the next one (capped at 60 s)
    dt = np.minimum(np.diff(t.time_msc.to_numpy(), append=t.time_msc.iloc[-1]), 60_000)
    return {"n": len(t), "from": ts.min(), "to": ts.max(), "median": rel.median(), "tw_mean": np.average(rel, weights=dt + 1),
            "p90": rel.quantile(0.9), "by_hour": (rel.groupby(ts.dt.hour).median())}


rows = []
for sym in FOCUS:
    if sym not in spec:
        continue
    s = spec[sym]
    d1, h1 = rates(sym, "D1"), rates(sym, "H1")
    price = float(d1["close"].iloc[-1]) if d1 is not None and len(d1) else np.nan
    pt = float(s["point"])
    sp = None
    if h1 is not None:
        last = h1[h1.time >= h1.time.max() - pd.Timedelta(days=365)]
        nz = last[last.spread_points > 0]
        sp = (nz.spread_points * pt / nz.close).median() if len(nz) else np.nan
        first_spread = h1.loc[h1.spread_points > 0, "time"].min()
    lo, sh = swap_pa(s, price)
    rows.append({"symbol": sym, "path": s["path"].split("\\")[0], "price": price, "contract": float(s["contract_size"]),
                 "h1_spread_rel": sp, "spread_history_from": first_spread if h1 is not None else None,
                 "swap_long_pa": lo, "swap_short_pa": sh, "swap_mode": int(s["swap_mode"]),
                 "triple_day": int(s["swap_3days"]), "history_from": d1["time"].min() if d1 is not None else None})

ticks = {sym: tick_spread(sym) for sym in ("BTCUSD", "ETHUSD", "EURUSD", "US500.cash", "XAUUSD")}

L = ["# Echte FTMO-Handelskosten (Export vom 25.10.2026, FTMO-Demo, Swing-relevant)\n",
     "Quelle: `tools/mt5/ExportFtmoData.mq5`, ausgewertet mit `tools/mt5/analyse_export.py`. Spread relativ zum Kurs; "
     "Swap in % des Nominals pro Jahr (365 Belastungen: Mo–Do einfach, ein Tag dreifach). Negativ = Belastung.\n",
     "## Spreads aus Ticks (letzte 30 Tage, Bid/Ask)\n",
     "| Symbol | Ticks | Median | zeitgewichtet Ø | 90 %-Quantil |", "|---|---|---|---|---|"]
for sym, t in ticks.items():
    if t:
        L.append(f"| {sym} | {t['n']:,} | {t['median']:.4%} | {t['tw_mean']:.4%} | {t['p90']:.4%} |")
L += ["", "## Spreads aus der Bar-Historie und Swaps\n",
      "Bar-Spread = Median des Spread-Felds der H1-Bars im letzten Jahr (MT5 speichert je Bar den kleinsten Spread, "
      "daher eher eine Untergrenze; Vergleich mit den Ticks oben).\n",
      "| Symbol | Gruppe | Historie ab | Spread H1 (Median, 12 M.) | Swap long p. a. | Swap short p. a. | Swap-Art | 3-fach |",
      "|---|---|---|---|---|---|---|---|"]
days = ["So", "Mo", "Di", "Mi", "Do", "Fr", "Sa"]
for r in rows:
    L.append(f"| {r['symbol']} | {r['path']} | {r['history_from']:%Y-%m} | {r['h1_spread_rel']:.4%} | "
             f"{r['swap_long_pa']:+.2%} | {r['swap_short_pa']:+.2%} | {'Zins' if r['swap_mode'] == 5 else 'Punkte'} | "
             f"{days[r['triple_day']]} |")
OUT.write_text("\n".join(L) + "\n", encoding="utf-8")
print("\n".join(L))
for sym, t in ticks.items():
    if t:
        print(sym, "Median-Spread je Stunde (UTC):", " ".join(f"{h}:{v:.4%}" for h, v in t["by_hour"].items()))
