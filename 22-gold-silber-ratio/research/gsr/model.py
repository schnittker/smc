"""Model G 'gold/silver ratio', as pre-registered in docs/01_Vorregistrierung.md.

q = ln(XAU) - ln(XAG) from the 15:45 New York prices on days with both metals; z over the last n days (G-60,
G-250). Flat and z >= 2: short gold, long silver; z <= -2: the reverse; exit when z crosses zero. Equal notional
N = 10 % / sigma_q in both legs (EWMA of daily changes of q as model G), set at entry; trades only on days with an
exact 15:50 bar for both. Accounting per leg with carry.model.run_weights and cost model H.
"""
from __future__ import annotations

import numpy as np

from carry.model import ewma_sigma, run_weights
from pmr.model import zscore
from smc.strategy_g import VOL_TARGET
from smc.swaps import RateTable

VARIANTS = {"G-60": 60, "G-250": 250}
ENTRY_Z = 2.0


def common_series(px_g: dict, px_s: dict) -> dict:
    days = np.intersect1d(px_g["day"], px_s["day"])
    ig, is_ = np.searchsorted(px_g["day"], days), np.searchsorted(px_s["day"], days)
    return {"day": days, "q_sig": np.log(px_g["p_sig"][ig]) - np.log(px_s["p_sig"][is_]),
            "q_mark": np.log(px_g["p_mark"][ig]) - np.log(px_s["p_mark"][is_]),
            "exact": px_g["exact"][ig] & px_s["exact"][is_]}


def targets(c: dict, n: int) -> tuple[dict[int, float], dict[int, float]]:
    """Gold and silver target weights on the days the ratio position changes."""
    z = zscore(np.exp(c["q_sig"]), n)
    sigma = ewma_sigma(np.r_[np.nan, np.diff(c["q_mark"])])
    gold, silver, pos = {}, {}, 0
    for i in range(len(z)):
        if not c["exact"][i] or not np.isfinite(z[i]):
            continue
        day = int(c["day"][i])
        if pos == 0 and np.isfinite(sigma[i]) and abs(z[i]) >= ENTRY_Z:
            pos = -1 if z[i] > 0 else 1                      # -1 = short the ratio (short gold, long silver)
            size = VOL_TARGET / sigma[i]
            gold[day], silver[day] = pos * size, -pos * size
        elif (pos == -1 and z[i] <= 0) or (pos == 1 and z[i] >= 0):
            pos = 0
            gold[day], silver[day] = 0.0, 0.0
    return gold, silver


def run_model_g(variant: str, specs: dict, pxs: dict, rates: RateTable) -> np.ndarray:
    c = common_series(pxs["XAUUSD"], pxs["XAGUSD"])
    t_g, t_s = targets(c, VARIANTS[variant])
    return np.concatenate([run_weights(specs["XAUUSD"], pxs["XAUUSD"], t_g, rates),
                           run_weights(specs["XAGUSD"], pxs["XAGUSD"], t_s, rates)])
