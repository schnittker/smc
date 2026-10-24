"""Strategy no. 11 "intraday momentum US500" (model I).

Data, time and cost models come from ../smart-money-concept (package `smc`), the NYSE calendar from
../10-turn-of-the-month (package `tom`) and New York time helpers from ../09-pre-fomc-drift (package `fomc`);
importing this package puts all three on sys.path.
"""
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
for _p in ("smart-money-concept", "09-pre-fomc-drift", "10-turn-of-the-month"):
    _path = str(PROJECT_ROOT.parent / _p / "research")
    if _path not in sys.path:
        sys.path.insert(0, _path)

DATA_DIR = PROJECT_ROOT / "data"
RESULTS_DIR = PROJECT_ROOT / "research" / "results"
