"""Model X 'FX cross-sectional momentum G8', as pre-registered in docs/01_Vorregistrierung.md.

Identical to model K (../06-fx-carry, carry.model) except for the ranking: on the first trading day of each
month the eight currencies are ranked by their past excess return against the USD - log USD value from the
16:50 New York prices plus the accrued rate differential (last month's rates, 1/261 per trading day).
X-1 uses the last 21 trading days, X-12 the 252 days before the last 21. Positions (1/8), (2/7), (3/6),
sizing, rebalancing and accounting as K-3.
"""
from __future__ import annotations

import numpy as np

from carry.model import (CURRENCIES, FX, VOL_START, VOL_TARGET, CarrySpec, apply_days, ewma_sigma, legs,
                         rebalance_days, run_weights, usd_log_prices)
from smc import timez
from smc.strategy_g import ANNUAL
from smc.swaps import MARKUP, RateTable, month_index

VARIANTS = {"X-1": (21, 0), "X-12": (252, 21)}          # (lookback, skip) in common trading days
POSITIONS = ((0, 7), (1, 6), (2, 5))


def excess_values(common: np.ndarray, logp: dict[str, np.ndarray], rates: RateTable) -> dict[str, np.ndarray]:
    """Cumulative log excess value of each currency against the USD per common trading day."""
    months = month_index(common * timez.DAY) - 1
    out = {}
    for c in CURRENCIES:
        diff = np.array([rates.rate(c, int(m)) - rates.rate("USD", int(m)) for m in months])
        carry_ = np.r_[0.0, np.cumsum(diff[1:] / ANNUAL)]
        out[c] = logp[c] + carry_ if c != "USD" else np.zeros(len(common))
    return out


def ranking(scores: dict[str, float]) -> list[str]:
    """Currencies by formation return, highest first, ties alphabetical."""
    return sorted(CURRENCIES, key=lambda c: (-scores[c], c))


def schedule(px: dict[str, dict], rates: RateTable, variant: str) -> tuple[dict[str, dict[int, float]], list]:
    """Target weight per instrument and rebalance day, and a log (day, long currencies, short currencies)."""
    look, skip = VARIANTS[variant]
    common, logp = usd_log_prices(px)
    xv = excess_values(common, logp, rates)
    sigma = {}
    targets: dict[str, dict[int, float]] = {s: {} for s in FX}
    log = []
    for z in rebalance_days(common):
        if z < max(look, VOL_START):
            continue
        day = int(common[z])
        rank = ranking({c: float(xv[c][z - skip] - xv[c][z - look]) for c in CURRENCIES})
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


def run_model_x(px: dict[str, dict], rates: RateTable, variant: str, markup: float = MARKUP) -> tuple[np.ndarray, list]:
    """Rows of all instruments that are ever held, and the rebalance log."""
    targets, log = schedule(px, rates, variant)
    parts = [run_weights(CarrySpec(sym, markup=markup), px[sym], apply_days(px[sym], targets[sym]), rates)
             for sym in FX if any(v != 0.0 for v in targets[sym].values())]
    return np.concatenate(parts), log
