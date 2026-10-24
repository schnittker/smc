"""Strategy no. 40 "Hurst regime switch" (model W).

Data, the FX / CFD cost models and swaps come from ../smart-money-concept (`smc`), the universe and per-trade costs
from ../33-35-tagesausbruch (`dbo`), indicators and swaps from ../36-38-h4-kanalausbruch (`hkb`); importing
this package puts all of them on sys.path.
"""
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
for _p in ("smart-money-concept", "33-35-tagesausbruch", "36-38-h4-kanalausbruch"):
    _path = str(PROJECT_ROOT.parent / _p / "research")
    if _path not in sys.path:
        sys.path.insert(0, _path)

DATA_DIR = PROJECT_ROOT / "data"
RESULTS_DIR = PROJECT_ROOT / "research" / "results"
