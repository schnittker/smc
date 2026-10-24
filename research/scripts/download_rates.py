#!/usr/bin/env python3
"""Download the monthly short-term interest rates for the swap model (FRED graph CSV, no API key).

Usage: research/.venv/bin/python -I research/scripts/download_rates.py
Files land in data/raw/rates/<series>.csv and are only parsed, never executed.
"""
import sys
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from smc.swaps import RATE_SERIES, RATES_DIR, parse_fred_csv  # noqa: E402

URL = "https://fred.stlouisfed.org/graph/fredgraph.csv?id={}"


def main():
    RATES_DIR.mkdir(parents=True, exist_ok=True)
    for ccy, sid in RATE_SERIES.items():
        req = urllib.request.Request(URL.format(sid), headers={"User-Agent": "smcea-research/0.1"})
        with urllib.request.urlopen(req, timeout=60) as resp:
            text = resp.read().decode("utf-8")
        months, rates = parse_fred_csv(text)
        if not len(months):
            raise SystemExit(f"{sid}: no data")
        (RATES_DIR / f"{sid}.csv").write_text(text, encoding="utf-8")
        last = str(months[-1].astype("datetime64[M]"))
        print(f"{ccy} {sid}: {len(months)} months, last {last} = {rates[-1] * 100:.2f} %")


if __name__ == "__main__":
    main()
