import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import gsr  # noqa: E402,F401  (puts smc, carry and pmr on sys.path)
