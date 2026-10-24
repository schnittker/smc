import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import ffx  # noqa: E402,F401  (puts smc, carry and fomc on sys.path)
