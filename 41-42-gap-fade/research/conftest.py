import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import gap  # noqa: E402,F401  (puts the neighbour packages on sys.path)
