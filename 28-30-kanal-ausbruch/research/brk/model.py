"""Model B 'channel breakout' (strategies no. 28 and 30), as pre-registered in docs/01_Vorregistrierung.md.

Per instrument from the daily signal prices C (5 minutes before the mark): enter long when C exceeds the maximum of
the previous n_in closes, short when it falls below their minimum; a long exits when C falls below the minimum of
the previous n_out closes, a short when it rises above their maximum. B-52W: n_in 252, n_out 126; B-TURTLE: 55 and
20. Size 10 % / sigma at entry (EWMA as model G). Accounting with carry.model.run_weights.
"""
from __future__ import annotations

import numpy as np

from carry.model import ewma_sigma, run_weights
from smc.strategy_g import VOL_TARGET
from smc.swaps import RateTable

VARIANTS = {"B-52W": (252, 126), "B-TURTLE": (55, 20)}
CFDS = ("SPXUSD", "NSXUSD", "FRXEUR", "UKXGBP", "JPXJPY", "HKXHKD", "AUXAUD", "BCOUSD", "XAGUSD")


def channels(c: np.ndarray, n: int) -> tuple[np.ndarray, np.ndarray]:
    """Max and min of the previous n values (excluding today); NaN before n values exist."""
    hi, lo = np.full(len(c), np.nan), np.full(len(c), np.nan)
    for i in range(n, len(c)):
        w = c[i - n:i]
        hi[i], lo[i] = w.max(), w.min()
    return hi, lo


def targets(px: dict, n_in: int, n_out: int) -> dict[int, float]:
    c = px["p_sig"]
    hi_in, lo_in = channels(c, n_in)
    hi_out, lo_out = channels(c, n_out)
    sigma = ewma_sigma(np.r_[np.nan, np.diff(np.log(px["p_mark"]))])
    out, pos = {}, 0
    for i in range(len(c)):
        if not px["exact"][i] or not np.isfinite(hi_in[i]):
            continue
        new = pos
        if pos == 1 and c[i] < lo_out[i]:
            new = 0
        elif pos == -1 and c[i] > hi_out[i]:
            new = 0
        if new == 0:
            if c[i] > hi_in[i]:
                new = 1
            elif c[i] < lo_in[i]:
                new = -1
        if new != pos:
            if new != 0 and not np.isfinite(sigma[i]):
                continue
            out[int(px["day"][i])] = new * VOL_TARGET / sigma[i] if new else 0.0
            pos = new
    return out


def run_model_b(variant: str, spec, px: dict, rates: RateTable) -> np.ndarray:
    n_in, n_out = VARIANTS[variant]
    return run_weights(spec, px, targets(px, n_in, n_out), rates)
