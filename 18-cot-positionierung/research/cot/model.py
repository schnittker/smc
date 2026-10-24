"""Model C 'COT extremes', as pre-registered in docs/01_Vorregistrierung.md.

Per CFTC legacy futures-only report (as of Tuesday): N = non-commercial long - short; COT index over the last 156
reports; >= 0.9 speculators extremely long, <= 0.1 extremely short. C-KONTRA trades against, C-FOLGE with the
speculators (long / short the foreign currency or gold against USD), flat otherwise. Orders on the Monday after
the report date at 16:50 New York; size 10 % / sigma (EWMA as model G), fixed until the signal state changes.
Accounting with carry.model.run_weights (model G's bookkeeping, FX costs, swaps, 0.7 % fee).
"""
from __future__ import annotations

import csv
import io
import zipfile
from datetime import date
from pathlib import Path

import numpy as np

from carry.model import CarrySpec, apply_days, ewma_sigma, run_weights
from smc.strategy_g import VOL_TARGET
from smc.swaps import RateTable

EPOCH = date(1970, 1, 1)
CONTRACTS = {"099741": ("EURUSD", 1), "096742": ("GBPUSD", 1), "097741": ("USDJPY", -1), "232741": ("AUDUSD", 1),
             "090741": ("USDCAD", -1), "092741": ("USDCHF", -1), "112741": ("NZDUSD", 1), "088691": ("XAUUSD", 1)}
VARIANTS = {"C-KONTRA": -1, "C-FOLGE": 1}
WINDOW, HIGH, LOW, EXEC_LAG = 156, 0.9, 0.1, 6
SHUTDOWN = ((date(2018, 12, 24) - EPOCH).days, (date(2019, 3, 4) - EPOCH).days)


def load_cot(files: list[Path]) -> dict[str, tuple[np.ndarray, np.ndarray]]:
    """Report day numbers and non-commercial net positions per contract code (sorted, de-duplicated)."""
    data: dict[str, dict[int, float]] = {c: {} for c in CONTRACTS}
    for f in files:
        with zipfile.ZipFile(f) as z:
            text = z.read(z.namelist()[0]).decode("latin-1")
        rows = csv.reader(io.StringIO(text))
        hdr = [h.strip() for h in next(rows)]
        ci, di = hdr.index("CFTC Contract Market Code"), hdr.index("As of Date in Form YYYY-MM-DD")
        li, si = hdr.index("Noncommercial Positions-Long (All)"), hdr.index("Noncommercial Positions-Short (All)")
        for r in rows:
            code = r[ci].strip()
            if code in data:
                day = (date.fromisoformat(r[di].strip()) - EPOCH).days
                data[code][day] = float(r[li]) - float(r[si])
    return {c: (np.array(sorted(v), np.int64), np.array([v[k] for k in sorted(v)], float)) for c, v in data.items()}


def cot_index(net: np.ndarray, window: int = WINDOW) -> np.ndarray:
    out = np.full(len(net), np.nan)
    for i in range(window - 1, len(net)):
        w = net[i - window + 1:i + 1]
        lo, hi = w.min(), w.max()
        out[i] = 0.5 if hi == lo else (net[i] - lo) / (hi - lo)
    return out


def signals(days: np.ndarray, net: np.ndarray) -> list[tuple[int, int]]:
    """(execution day, state) per usable report: state +1 extremely long, -1 extremely short, 0 neutral."""
    idx = cot_index(net)
    out = []
    for d, x in zip(days, idx):
        if not np.isfinite(x) or SHUTDOWN[0] <= d <= SHUTDOWN[1]:
            continue
        out.append((int(d) + EXEC_LAG, 1 if x >= HIGH else (-1 if x <= LOW else 0)))
    return out


def targets(px: dict, sig: list[tuple[int, int]], direction: int, foreign: int) -> dict[int, float]:
    """Target weights on the execution days where the position state changes."""
    sigma = ewma_sigma(np.r_[np.nan, np.diff(np.log(px["p_mark"]))])
    out, state = {}, 0
    for exec_day, s in sig:
        want = s * direction * foreign
        if want == state:
            continue
        i = int(np.searchsorted(px["day"], exec_day))
        if i >= len(px["day"]) or not np.isfinite(sigma[i]):
            continue
        out[exec_day] = want * VOL_TARGET / sigma[i] if want else 0.0
        state = want
    return out


def run_model_c(variant: str, code: str, px: dict, cot: dict, rates: RateTable) -> np.ndarray:
    sym, foreign = CONTRACTS[code]
    sig = signals(*cot[code])
    return run_weights(CarrySpec(sym), px, apply_days(px, targets(px, sig, VARIANTS[variant], foreign)), rates)
