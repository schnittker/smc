"""Strategy no. 22 "gold/silver ratio" (model G).

Data, time and cost models come from ../smart-money-concept (`smc`), the daily bookkeeping from ../06-fx-carry
(`carry`) and the z-score and trade list from ../21-pairs-mean-reversion (`pmr`); importing this package puts all
of them on sys.path.
"""
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
for _p in ("smart-money-concept", "06-fx-carry", "21-pairs-mean-reversion"):
    _path = str(PROJECT_ROOT.parent / _p / "research")
    if _path not in sys.path:
        sys.path.insert(0, _path)

DATA_DIR = PROJECT_ROOT / "data"
RESULTS_DIR = PROJECT_ROOT / "research" / "results"
