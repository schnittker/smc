"""Strategies no. 54, 55 and 60 (model PA: price action).

Data, cost models and swaps come from ../smart-money-concept (`smc`), server days and per-trade costs from
../33-35-tagesausbruch (`dbo`), ATR / swap accrual from ../36-38-h4-kanalausbruch (`hkb`) and swings plus the
trade engine from ../50-51-sr-trendlinien (`chart`); importing this package puts all of them on sys.path.
"""
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
for _p in ("smart-money-concept", "33-35-tagesausbruch", "36-38-h4-kanalausbruch", "50-51-sr-trendlinien"):
    _path = str(PROJECT_ROOT.parent / _p / "research")
    if _path not in sys.path:
        sys.path.insert(0, _path)

DATA_DIR = PROJECT_ROOT / "data"
RESULTS_DIR = PROJECT_ROOT / "research" / "results"
