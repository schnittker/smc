"""Model P 'z-score mean reversion AUDNZD / EURCHF', as pre-registered in docs/01_Vorregistrierung.md.

z = (ln p - mean) / sd over the last 60 daily 16:45 New York prices (including today). Flat and z >= 2: short;
flat and z <= -2: long; a short closes at z <= 0, a long at z >= 0. Size 10 % / sigma (EWMA as model G) at entry,
traded at 16:50 on days with an exact bar; accounting with carry.model.run_weights.
"""
from __future__ import annotations

import numpy as np

from carry.model import CarrySpec, ewma_sigma, run_weights
from smc.strategy_g import VOL_TARGET
from smc.swaps import RateTable

VARIANTS = {"P-AUDNZD": "AUDNZD", "P-EURCHF": "EURCHF"}
WINDOW, ENTRY_Z = 60, 2.0


def zscore(p: np.ndarray, n: int = WINDOW) -> np.ndarray:
    x = np.log(p)
    out = np.full(len(x), np.nan)
    for i in range(n - 1, len(x)):
        w = x[i - n + 1:i + 1]
        sd = w.std(ddof=1)
        out[i] = (x[i] - w.mean()) / sd if sd > 0 else 0.0
    return out


def targets(px: dict) -> dict[int, float]:
    z = zscore(px["p_sig"])
    sigma = ewma_sigma(np.r_[np.nan, np.diff(np.log(px["p_mark"]))])
    out, pos = {}, 0
    for i in range(len(z)):
        if not px["exact"][i] or not np.isfinite(z[i]):
            continue
        if pos == 0 and np.isfinite(sigma[i]) and abs(z[i]) >= ENTRY_Z:
            pos = -1 if z[i] > 0 else 1
            out[int(px["day"][i])] = pos * VOL_TARGET / sigma[i]
        elif (pos == -1 and z[i] <= 0) or (pos == 1 and z[i] >= 0):
            pos = 0
            out[int(px["day"][i])] = 0.0
    return out


def run_model_p(variant: str, px: dict, rates: RateTable) -> np.ndarray:
    return run_weights(CarrySpec(VARIANTS[variant]), px, targets(px), rates)


def trades(rows: np.ndarray) -> list[tuple[int, int, float]]:
    """(entry day, holding days, net result) per position episode (long or short)."""
    out, start, acc = [], None, 0.0
    w = rows["w"]
    for k in range(len(rows)):
        prev = w[k - 1] if k else 0.0
        if prev != 0.0:
            acc += rows["net"][k]
        if prev == 0.0 and w[k] != 0.0:
            start, acc = k, rows["net"][k]
        elif prev != 0.0 and (w[k] == 0.0 or np.sign(w[k]) != np.sign(prev)) and start is not None:
            out.append((int(rows["day"][start]), k - start, acc))
            start, acc = (k, 0.0) if w[k] != 0.0 else (None, 0.0)
    if start is not None:
        out.append((int(rows["day"][start]), len(rows) - start, acc))
    return out
