#!/usr/bin/env python3
"""Download HistData.com M1 bars for the whole instrument universe (resumable).

Usage: research/.venv/bin/python -I research/scripts/download_histdata.py [--symbols EURUSD,GBPUSD]
"""
import argparse
import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from smc.config import RAW_HISTDATA_DIR, SYMBOLS  # noqa: E402
from smc.data.histdata import download_all  # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--symbols", default=",".join(SYMBOLS))
    ap.add_argument("--first-year", type=int, default=2014)
    ap.add_argument("--current-year", type=int, default=2026)
    ap.add_argument("--last-month", type=int, default=10, help="last month to try for the current year")
    ap.add_argument("--delay", type=float, default=3.0)
    args = ap.parse_args()

    log_path = RAW_HISTDATA_DIR / "_download.log"
    RAW_HISTDATA_DIR.mkdir(parents=True, exist_ok=True)

    def log(msg):
        line = f"{datetime.now():%Y-%m-%d %H:%M:%S} {msg}"
        print(line, flush=True)
        with log_path.open("a") as fh:
            fh.write(line + "\n")

    download_all(
        symbols=args.symbols.split(","),
        years=range(args.first_year, args.current_year),
        current_year=args.current_year,
        current_months=range(1, args.last_month + 1),
        out_dir=RAW_HISTDATA_DIR,
        delay_s=args.delay,
        log=log,
    )
    log("done")


if __name__ == "__main__":
    main()
