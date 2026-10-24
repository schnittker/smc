"""Model Z 'interest-rate momentum G8', as pre-registered in docs/01_Vorregistrierung.md.

Identical to model K-3 (../06-fx-carry, carry.model) except for the ranking: on the first trading day of month m
the eight currencies are ranked by the change of their short-term rate, r(m-1) - r(m-1-L), with L = 12 (Z-12)
or 3 (Z-3); ties by the rate level, then alphabetically. Positions (1/8), (2/7), (3/6), sizing, rebalancing and
accounting as K-3.
"""
from __future__ import annotations

import numpy as np

from carry.model import (CURRENCIES, FX, VARIANTS as K_VARIANTS, VOL_TARGET, CarrySpec, apply_days, ewma_sigma,
                         legs, rebalance_days, run_weights, usd_log_prices)
from smc import timez
from smc.swaps import MARKUP, RateTable, month_index

VARIANTS = {"Z-12": 12, "Z-3": 3}
POSITIONS = K_VARIANTS["K-3"]


def ranking(rates: RateTable, month: int, lag: int) -> list[str]:
    """Currencies by the rate change from month-lag to month, then by the level, then alphabetically."""
    def key(c):
        level = rates.rate(c, month)
        return (-(level - rates.rate(c, month - lag)), -level, c)
    return sorted(CURRENCIES, key=key)


def schedule(px: dict[str, dict], rates: RateTable, variant: str) -> tuple[dict[str, dict[int, float]], list]:
    lag = VARIANTS[variant]
    common, logp = usd_log_prices(px)
    sigma = {}
    targets: dict[str, dict[int, float]] = {s: {} for s in FX}
    log = []
    for z in rebalance_days(common):
        day = int(common[z])
        rank = ranking(rates, int(month_index(day * timez.DAY)) - 1, lag)
        w: dict[str, float] = {}
        for hi, lo in POSITIONS:
            h, l_ = rank[hi], rank[lo]
            if (h, l_) not in sigma:
                sigma[(h, l_)] = ewma_sigma(np.r_[np.nan, np.diff(logp[h] - logp[l_])])
            n = VOL_TARGET / sigma[(h, l_)][z]
            for sym, sgn in legs(h, l_).items():
                w[sym] = w.get(sym, 0.0) + sgn * n
        for sym in FX:
            targets[sym][day] = w.get(sym, 0.0)
        log.append((day, [rank[i] for i, _ in POSITIONS], [rank[j] for _, j in POSITIONS]))
    return targets, log


def run_model_z(px: dict[str, dict], rates: RateTable, variant: str, markup: float = MARKUP) -> tuple[np.ndarray, list]:
    targets, log = schedule(px, rates, variant)
    parts = [run_weights(CarrySpec(sym, markup=markup), px[sym], apply_days(px[sym], targets[sym]), rates)
             for sym in FX if any(v != 0.0 for v in targets[sym].values())]
    return np.concatenate(parts), log

