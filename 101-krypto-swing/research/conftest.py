import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import kry  # noqa: E402,F401  (puts smc and swp on sys.path)
