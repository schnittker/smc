import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import cal  # noqa: E402,F401  (puts smc, fomc and tom on sys.path)
