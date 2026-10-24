import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import swp  # noqa: E402,F401  (puts smc and the component packages on sys.path)
