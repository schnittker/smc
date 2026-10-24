import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import dmom  # noqa: E402,F401  (puts smc and carry on sys.path)
