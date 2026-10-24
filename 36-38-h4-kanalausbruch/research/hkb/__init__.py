"""Strategies no. 36 and 38 "H4 channel breakout" (model K: Bollinger squeeze, Keltner channel).

Data, the FX / CFD cost models and swaps come from ../smart-money-concept (`smc`), the universe and per-trade costs
from ../33-35-tagesausbruch (`dbo`); importing this package puts both on sys.path.
"""
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
for _p in ("smart-money-concept", "33-35-tagesausbruch"):
    _path = str(PROJECT_ROOT.parent / _p / "research")
    if _path not in sys.path:
        sys.path.insert(0, _path)

DATA_DIR = PROJECT_ROOT / "data"
RESULTS_DIR = PROJECT_ROOT / "research" / "results"
