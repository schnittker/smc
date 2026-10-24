#!/usr/bin/env python3
"""HistData zips -> consolidated M1 parquet -> server-time bars (M5..D1) + data-quality report.

Usage: research/.venv/bin/python -I research/scripts/build_data.py [--symbols EURUSD,...]
"""
import argparse
import sys
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from smc import timez  # noqa: E402
from smc.config import PROJECT_ROOT, SYMBOLS  # noqa: E402
from smc.data.bars import consolidate_m1, resample, write_bars, write_m1  # noqa: E402

TFS = ("M5", "M15", "H1", "H4", "D1")


def build(symbol: str) -> dict:
    m1, info = consolidate_m1(symbol)
    write_m1(symbol, m1)
    for tf in TFS:
        write_bars(symbol, tf, resample(m1, tf))
    t = m1["t"]
    # weekday gaps longer than one hour (outside the weekend close) hint at missing data
    gap = np.diff(t)
    wd = timez.ny_weekday(t[:-1])
    ny_min = timez.ny_minute_of_day(t[:-1])
    weekend = (wd == 4) & (ny_min >= 16 * 60) | (wd == 5) | ((wd == 6) & (ny_min < 17 * 60))
    big = (gap > 3600) & ~weekend
    lr = np.abs(np.diff(np.log(m1["c"])))
    med = np.median(lr[lr > 0]) if (lr > 0).any() else 0.0
    spikes = int((lr > 50 * med).sum()) if med > 0 else 0
    first = str(np.datetime64(int(t[0]), "s"))
    last = str(np.datetime64(int(t[-1]), "s"))
    return dict(symbol=symbol, first=first, last=last, **info, gaps_over_1h=int(big.sum()),
                max_gap_h=round(float(gap[~weekend[:len(gap)]].max()) / 3600, 1) if len(gap) else 0.0,
                spikes_50x=spikes)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--symbols", default=",".join(SYMBOLS))
    ap.add_argument("--workers", type=int, default=6)
    args = ap.parse_args()
    symbols = args.symbols.split(",")
    with ProcessPoolExecutor(args.workers) as ex:
        rows = list(ex.map(build, symbols))
    lines = ["# Datenqualität HistData M1 (Bid, UTC)\n",
             "| Symbol | Erste | Letzte | M1-Bars | Duplikate | OHLC repariert | Lücken > 1 h (werktags) | Max. Lücke (h) | Ausreißer > 50× Median |",
             "|---|---|---|---|---|---|---|---|---|"]
    for r in rows:
        lines.append(f"| {r['symbol']} | {r['first']} | {r['last']} | {r['rows']:,} | {r['duplicates']} | "
                     f"{r['repaired_ohlc']} | {r['gaps_over_1h']} | {r['max_gap_h']} | {r['spikes_50x']} |")
    out = PROJECT_ROOT / "research" / "results" / "data_quality.md"
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
