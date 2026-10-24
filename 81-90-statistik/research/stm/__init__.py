"""Strategies no. 81, 82, 85 and 90 "statistical models" (model ST: HMM, GARCH, k-NN, gold seasonality).

Data and cost models come from ../smart-money-concept (`smc`), the daily accounting from ../06-fx-carry (`carry`) and
the 34-instrument universe from ../28-30-kanal-ausbruch (`brk`); importing this package puts all of them on sys.path.
"""
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
for _p in ("smart-money-concept", "06-fx-carry", "28-30-kanal-ausbruch"):
    _path = str(PROJECT_ROOT.parent / _p / "research")
    if _path not in sys.path:
        sys.path.insert(0, _path)

DATA_DIR = PROJECT_ROOT / "data"
RESULTS_DIR = PROJECT_ROOT / "research" / "results"
