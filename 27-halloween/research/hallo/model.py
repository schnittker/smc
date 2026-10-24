"""Model S 'Halloween US indices', as pre-registered in docs/01_Vorregistrierung.md.

Long 1 x capital from the first trading day of November (with an exact 15:50 New York bar) to the first trading
day of May, flat otherwise. Accounting with carry.model.run_weights and the index cost and swap model H.
"""
from __future__ import annotations

import numpy as np

from carry.model import run_weights
from smc import timez
from smc.swaps import RateTable

VARIANTS = {"S-SPX": "SPXUSD", "S-NDX": "NSXUSD"}


def targets(px: dict) -> dict[int, float]:
    month = (np.asarray(px["day"] * timez.DAY, dtype="datetime64[s]").astype("datetime64[M]").astype(int) % 12) + 1
    ym = np.asarray(px["day"] * timez.DAY, dtype="datetime64[s]").astype("datetime64[M]").astype(int)
    out, seen = {}, set()
    for i in np.flatnonzero(px["exact"]):
        if month[i] in (11, 5) and ym[i] not in seen:
            seen.add(ym[i])
            out[int(px["day"][i])] = 1.0 if month[i] == 11 else 0.0
    return out


def run_model_s(spec, px: dict, rates: RateTable, hold: bool = False) -> np.ndarray:
    t = {int(px["day"][int(np.argmax(px["exact"]))]): 1.0} if hold else targets(px)
    return run_weights(spec, px, t, rates)
