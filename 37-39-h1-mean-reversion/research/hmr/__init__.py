"""Strategies no. 37 and 39 "H1 mean reversion" (model U: Bollinger in ranges, z-score with OU half-life).

Data, the FX cost model and swaps come from ../smart-money-concept (`smc`), per-trade costs from
../33-35-tagesausbruch (`dbo`) and indicators / swap accrual from ../36-38-h4-kanalausbruch (`hkb`); importing this
package puts all of them on sys.path.
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
