"""Strategy no. 32 "Asian range fade" (model A).

Data and the FX cost model come from ../smart-money-concept (`smc`), London clock times from
../05-monatsend-rebalancing (`mer`) and the trading-day calendar from ../31-london-breakout (`lbo`); importing this
package puts all of them on sys.path.
"""
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
for _p in ("smart-money-concept", "05-monatsend-rebalancing", "31-london-breakout"):
    _path = str(PROJECT_ROOT.parent / _p / "research")
    if _path not in sys.path:
        sys.path.insert(0, _path)

DATA_DIR = PROJECT_ROOT / "data"
RESULTS_DIR = PROJECT_ROOT / "research" / "results"
