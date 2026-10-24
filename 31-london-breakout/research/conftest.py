import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import lbo  # noqa: E402,F401  (puts smc and mer on sys.path)
