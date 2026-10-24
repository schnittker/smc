"""Strategies no. 46 and 47 "currency strength" (model Y: session strength ranking, USD-basket mean reversion).

Data, the FX cost model and swaps come from ../smart-money-concept (`smc`), per-trade costs from
../33-35-tagesausbruch (`dbo`), ATR and swap accrual from ../36-38-h4-kanalausbruch (`hkb`) and London clock times
from ../05-monatsend-rebalancing (`mer`); importing this package puts all of them on sys.path.
"""
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
for _p in ("smart-money-concept", "33-35-tagesausbruch", "36-38-h4-kanalausbruch", "05-monatsend-rebalancing"):
    _path = str(PROJECT_ROOT.parent / _p / "research")
    if _path not in sys.path:
        sys.path.insert(0, _path)

DATA_DIR = PROJECT_ROOT / "data"
RESULTS_DIR = PROJECT_ROOT / "research" / "results"
