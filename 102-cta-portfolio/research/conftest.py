import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import cta  # noqa: E402,F401  (puts smc, carry, kry and swp on sys.path)
