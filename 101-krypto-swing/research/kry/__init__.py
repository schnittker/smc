"""Strategy no. 101 "crypto swing trend following" (model K).

Statistics come from ../smart-money-concept (`smc`), the FTMO simulation from ../100-swing-portfolio (`swp`);
importing this package puts both on sys.path."""
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
for _p in ("smart-money-concept", "100-swing-portfolio"):
    _path = str(PROJECT_ROOT.parent / _p / "research")
    if _path not in sys.path:
        sys.path.insert(0, _path)

DATA_DIR = PROJECT_ROOT / "data"
RAW_DIR = DATA_DIR / "raw" / "binance"
RESULTS_DIR = PROJECT_ROOT / "research" / "results"
