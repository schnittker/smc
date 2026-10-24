"""Strategy no. 16 "opening range breakout 5 minutes" (model O).

Data, time and cost models come from ../smart-money-concept (`smc`), New York time helpers from
../09-pre-fomc-drift (`fomc`), the NYSE calendar from ../10-turn-of-the-month (`tom`) and the early-close rule
from ../11-intraday-momentum (`imom`); importing this package puts all of them on sys.path.
"""
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
for _p in ("smart-money-concept", "09-pre-fomc-drift", "10-turn-of-the-month", "11-intraday-momentum"):
    _path = str(PROJECT_ROOT.parent / _p / "research")
    if _path not in sys.path:
        sys.path.insert(0, _path)

DATA_DIR = PROJECT_ROOT / "data"
RESULTS_DIR = PROJECT_ROOT / "research" / "results"
