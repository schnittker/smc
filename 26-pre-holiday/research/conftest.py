import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import preh  # noqa: E402,F401  (puts smc, fomc, tom and imom on sys.path)
