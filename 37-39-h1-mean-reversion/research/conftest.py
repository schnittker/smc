import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import hmr  # noqa: E402,F401  (puts smc, dbo and hkb on sys.path)
