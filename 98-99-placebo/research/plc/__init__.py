"""Controls no. 98 and 99 "placebo" (model PL: random entries, moon phases).

Imports put ../smart-money-concept (`smc`), ../33-35-tagesausbruch (`dbo`), ../36-38-h4-kanalausbruch (`hkb`),
../50-51-sr-trendlinien (`chart`), ../06-fx-carry (`carry`), ../28-30-kanal-ausbruch (`brk`) and ../81-90-statistik
(`stm`) on sys.path.
"""
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
for _p in ("smart-money-concept", "33-35-tagesausbruch", "36-38-h4-kanalausbruch", "50-51-sr-trendlinien",
           "06-fx-carry", "28-30-kanal-ausbruch", "81-90-statistik"):
    _path = str(PROJECT_ROOT.parent / _p / "research")
    if _path not in sys.path:
        sys.path.insert(0, _path)

DATA_DIR = PROJECT_ROOT / "data"
RESULTS_DIR = PROJECT_ROOT / "research" / "results"
