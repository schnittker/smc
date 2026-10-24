"""Strategy no. 19 "VIX regime" (model X).

Data, time model and cost model come from ../smart-money-concept (package `smc`), the portfolio engine from
../06-fx-carry (package `carry`); importing this package puts both on sys.path.
"""
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
for _p in (PROJECT_ROOT.parent / "smart-money-concept" / "research", PROJECT_ROOT.parent / "06-fx-carry" / "research"):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))

DATA_DIR = PROJECT_ROOT / "data"
RESULTS_DIR = PROJECT_ROOT / "research" / "results"
