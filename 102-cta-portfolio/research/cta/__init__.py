"""Strategy no. 102 "multi-asset trend (CTA)" (model C).

Data, cost models and statistics come from ../smart-money-concept (`smc`), the weight accounting from ../06-fx-carry
(`carry`), the crypto data and costs from ../101-krypto-swing (`kry`) and the FTMO simulation from
../100-swing-portfolio (`swp`); importing this package puts all of them on sys.path."""
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
for _p in ("smart-money-concept", "06-fx-carry", "101-krypto-swing", "100-swing-portfolio"):
    _path = str(PROJECT_ROOT.parent / _p / "research")
    if _path not in sys.path:
        sys.path.insert(0, _path)

DATA_DIR = PROJECT_ROOT / "data"
RESULTS_DIR = PROJECT_ROOT / "research" / "results"
