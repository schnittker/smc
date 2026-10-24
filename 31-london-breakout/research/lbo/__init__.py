"""Strategy no. 31 "London breakout" (model L).

Data and the FX cost model come from ../smart-money-concept (`smc`), London clock times from
../05-monatsend-rebalancing (`mer`); importing this package puts both on sys.path.
"""
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
for _p in ("smart-money-concept", "05-monatsend-rebalancing"):
    _path = str(PROJECT_ROOT.parent / _p / "research")
    if _path not in sys.path:
        sys.path.insert(0, _path)

DATA_DIR = PROJECT_ROOT / "data"
RESULTS_DIR = PROJECT_ROOT / "research" / "results"
