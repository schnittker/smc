"""Strategy no. 100 "swing portfolio" (ensemble of models P-SPX, T-FRÜH, V-VOL and F-CARRY).

The four building blocks are used unchanged from their projects; importing this package puts smc and the
component packages (fomc, tom, volm, carry, ffx) on sys.path.
"""
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
for _p in ("smart-money-concept", "06-fx-carry", "09-pre-fomc-drift", "10-turn-of-the-month", "14-vol-managed-index",
           "24-fomc-fx"):
    _path = str(PROJECT_ROOT.parent / _p / "research")
    if _path not in sys.path:
        sys.path.insert(0, _path)

DATA_DIR = PROJECT_ROOT / "data"
RESULTS_DIR = PROJECT_ROOT / "research" / "results"
