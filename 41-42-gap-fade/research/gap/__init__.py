"""Strategies no. 41 and 42 "gap fade" (model Q: index cash-open gap, FX weekend gap).

Data and cost models come from ../smart-money-concept (`smc`), per-trade costs from ../33-35-tagesausbruch (`dbo`),
London clock times from ../05-monatsend-rebalancing (`mer`), New York clock times from ../09-pre-fomc-drift
(`fomc`), the NYSE calendar from ../10-turn-of-the-month (`tom`) and early closes from ../11-intraday-momentum
(`imom`); importing this package puts all of them on sys.path.
"""
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
for _p in ("smart-money-concept", "33-35-tagesausbruch", "05-monatsend-rebalancing", "09-pre-fomc-drift",
           "10-turn-of-the-month", "11-intraday-momentum"):
    _path = str(PROJECT_ROOT.parent / _p / "research")
    if _path not in sys.path:
        sys.path.insert(0, _path)

DATA_DIR = PROJECT_ROOT / "data"
RESULTS_DIR = PROJECT_ROOT / "research" / "results"
