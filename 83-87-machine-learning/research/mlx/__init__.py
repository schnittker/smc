"""Strategies no. 83, 84 and 86 "machine learning" (model ML).

Data, the FX / CFD cost models and swaps come from ../smart-money-concept (`smc`), the universe and per-trade costs
from ../33-35-tagesausbruch (`dbo`), EMA / ATR / swaps from ../36-38-h4-kanalausbruch (`hkb`) and the
trade engines from ../50-51-sr-trendlinien (`chart`) and ../61-76-trendindikatoren (`tind`), ../65-75-oszillatoren (`osc`); importing this
package puts all of them on sys.path.
"""
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
for _p in ("smart-money-concept", "33-35-tagesausbruch", "36-38-h4-kanalausbruch", "50-51-sr-trendlinien", "61-76-trendindikatoren", "65-75-oszillatoren"):
    _path = str(PROJECT_ROOT.parent / _p / "research")
    if _path not in sys.path:
        sys.path.insert(0, _path)

DATA_DIR = PROJECT_ROOT / "data"
RESULTS_DIR = PROJECT_ROOT / "research" / "results"
