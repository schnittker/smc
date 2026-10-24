"""Strategies no. 48 and 49 "intraday levels" (model LV: market profile 80 % rule, pivot points).

Data and cost models come from ../smart-money-concept (`smc`), server days and per-trade costs from
../33-35-tagesausbruch (`dbo`), cash sessions from ../41-42-gap-fade (`gap`, which in turn needs `mer`, `fomc`,
`tom` and `imom`); importing this package puts all of them on sys.path.
"""
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
for _p in ("smart-money-concept", "33-35-tagesausbruch", "41-42-gap-fade", "05-monatsend-rebalancing",
           "09-pre-fomc-drift", "10-turn-of-the-month", "11-intraday-momentum"):
    _path = str(PROJECT_ROOT.parent / _p / "research")
    if _path not in sys.path:
        sys.path.insert(0, _path)

DATA_DIR = PROJECT_ROOT / "data"
RESULTS_DIR = PROJECT_ROOT / "research" / "results"
