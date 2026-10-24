"""Shared project configuration: instrument universe and data paths."""
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "data"
RAW_HISTDATA_DIR = DATA_DIR / "raw" / "histdata"
M1_DIR = DATA_DIR / "m1"
BARS_DIR = DATA_DIR / "bars"

SYMBOLS = [
    "EURUSD", "GBPUSD", "USDJPY", "AUDUSD", "NZDUSD", "USDCAD", "USDCHF",
    "EURJPY", "GBPJPY", "AUDJPY", "NZDJPY", "CADJPY", "CHFJPY",
    "EURCAD", "EURCHF", "EURNZD", "EURAUD",
    "GBPCHF", "GBPNZD", "GBPCAD", "GBPAUD",
    "AUDNZD", "AUDCAD", "CADCHF",
    "XAUUSD",
]

# Price digits as quoted by FTMO-style MT5 servers (5/3-digit FX, 2-digit gold).
DIGITS = {s: (3 if s.endswith("JPY") else 5) for s in SYMBOLS}
DIGITS["XAUUSD"] = 2
