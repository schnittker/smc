"""Model R 'commodity lead-lag', as pre-registered in docs/01_Vorregistrierung.md.

Signal: log return of the commodity's 15:45 New York price (Brent for R-OEL, gold for R-GOLD) against its last
previous price. Position from 16:50 New York the same day: long the commodity currency when the return is positive
(short USDCAD, long AUDUSD), short when negative; size 10 % / sigma (EWMA as model G), reset every signal day.
Accounting with carry.model.run_weights.
"""
from __future__ import annotations

import numpy as np

from carry.model import CarrySpec, ewma_sigma, run_weights
from smc.strategy_g import VOL_TARGET
from smc.swaps import RateTable

VARIANTS = {"R-OEL": ("BCOUSD", "USDCAD", -1), "R-GOLD": ("XAUUSD", "AUDUSD", 1)}


def targets(px_c: dict, px_fx: dict, sign: int) -> dict[int, float]:
    r = np.r_[np.nan, np.diff(np.log(px_c["p_sig"]))]
    sig_by_day = dict(zip(px_c["day"].tolist(), r.tolist()))
    sigma = ewma_sigma(np.r_[np.nan, np.diff(np.log(px_fx["p_mark"]))])
    out = {}
    for i, d in enumerate(px_fx["day"].tolist()):
        x = sig_by_day.get(d)
        if x is None or not np.isfinite(x) or x == 0 or not px_fx["exact"][i] or not np.isfinite(sigma[i]):
            continue
        out[d] = sign * np.sign(x) * VOL_TARGET / sigma[i]
    return out


def run_model_r(variant: str, px_c: dict, px_fx: dict, rates: RateTable) -> np.ndarray:
    _, fx, sign = VARIANTS[variant]
    return run_weights(CarrySpec(fx), px_fx, targets(px_c, px_fx, sign), rates)
