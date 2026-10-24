"""Strategy no. 24 "USD on FOMC days" (model F).

Data, time and cost models come from ../smart-money-concept (`smc`), the daily bookkeeping from ../06-fx-carry
(`carry`) and the FOMC dates from ../09-pre-fomc-drift (`fomc`); importing this package puts all of them on
sys.path.
"""
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
for _p in ("smart-money-concept", "06-fx-carry", "09-pre-fomc-drift"):
    _path = str(PROJECT_ROOT.parent / _p / "research")
    if _path not in sys.path:
        sys.path.insert(0, _path)

DATA_DIR = PROJECT_ROOT / "data"
RESULTS_DIR = PROJECT_ROOT / "research" / "results"
