"""Strategy no. 94 "news straddle" (model N: NFP).

Data and the FX cost model come from ../smart-money-concept (`smc`), New York clock times from ../09-pre-fomc-drift
(`fomc`) and per-trade costs from ../33-35-tagesausbruch (`dbo`); importing this package puts all of them on sys.path.
"""
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
for _p in ("smart-money-concept", "09-pre-fomc-drift", "33-35-tagesausbruch"):
    _path = str(PROJECT_ROOT.parent / _p / "research")
    if _path not in sys.path:
        sys.path.insert(0, _path)

DATA_DIR = PROJECT_ROOT / "data"
RESULTS_DIR = PROJECT_ROOT / "research" / "results"
