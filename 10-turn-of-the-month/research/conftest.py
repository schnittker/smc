import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import tom  # noqa: E402,F401  (puts smc and fomc on sys.path)
