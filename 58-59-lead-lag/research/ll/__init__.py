"""Strategies no. 58 and 59 "lead-lag" (model LL: US500 -> AUDJPY, US 10-year yield -> USDJPY).

Data and cost models come from ../smart-money-concept (`smc`), per-trade costs from ../33-35-tagesausbruch (`dbo`),
ATR / swaps from ../36-38-h4-kanalausbruch (`hkb`), the trade engine from ../50-51-sr-trendlinien (`chart`) and the
daily accounting from ../06-fx-carry (`carry`); importing this package puts all of them on sys.path.
"""
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
for _p in ("smart-money-concept", "33-35-tagesausbruch", "36-38-h4-kanalausbruch", "50-51-sr-trendlinien",
           "06-fx-carry"):
    _path = str(PROJECT_ROOT.parent / _p / "research")
    if _path not in sys.path:
        sys.path.insert(0, _path)

DATA_DIR = PROJECT_ROOT / "data"
RESULTS_DIR = PROJECT_ROOT / "research" / "results"
