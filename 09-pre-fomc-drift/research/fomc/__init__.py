"""Strategy no. 9 "pre-FOMC drift" (model P).

Data, time model, bars, cost model and statistics come from the sibling project
../smart-money-concept (package `smc`); importing this package puts it on sys.path.
"""
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
SMC_RESEARCH = PROJECT_ROOT.parent / "smart-money-concept" / "research"
if str(SMC_RESEARCH) not in sys.path:
    sys.path.insert(0, str(SMC_RESEARCH))

DATA_DIR = PROJECT_ROOT / "data"
RESULTS_DIR = PROJECT_ROOT / "research" / "results"
