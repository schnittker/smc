"""Strategy no. 10 "turn of the month US500" (model T).

Data, time and cost models come from ../smart-money-concept (package `smc`), the index position mechanics
from ../09-pre-fomc-drift (package `fomc`); importing this package puts both on sys.path.
"""
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
for _p in (PROJECT_ROOT.parent / "smart-money-concept" / "research", PROJECT_ROOT.parent / "09-pre-fomc-drift" / "research"):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))

DATA_DIR = PROJECT_ROOT / "data"
RESULTS_DIR = PROJECT_ROOT / "research" / "results"
