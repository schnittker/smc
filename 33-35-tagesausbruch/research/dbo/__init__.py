"""Strategies no. 33-35 "daily breakout" (model T: NR7, inside bar, volatility breakout).

Data and the FX / CFD cost models come from ../smart-money-concept (`smc`); importing this package puts it on
sys.path.
"""
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
for _p in ("smart-money-concept",):
    _path = str(PROJECT_ROOT.parent / _p / "research")
    if _path not in sys.path:
        sys.path.insert(0, _path)

DATA_DIR = PROJECT_ROOT / "data"
RESULTS_DIR = PROJECT_ROOT / "research" / "results"
