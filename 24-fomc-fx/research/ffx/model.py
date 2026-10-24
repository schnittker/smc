"""Model F 'USD on FOMC days', as pre-registered in docs/01_Vorregistrierung.md.

For each scheduled FOMC announcement day t: short USD from 16:50 New York on the weekday before t to 16:50 on t,
against all seven majors (F-USD) or against the (up to) three currencies whose last-month rate is highest above
the USD rate (F-CARRY). Size per pair 10 % / sigma (EWMA as model G); a pair without exact 16:50 bars on both days
is skipped for that event. Accounting per pair with carry.model.run_weights.
"""
from __future__ import annotations

import numpy as np

from carry.model import USD_PAIRS, CarrySpec, ewma_sigma, run_weights
from fomc.model import prev_weekday
from smc import timez
from smc.strategy_g import VOL_TARGET
from smc.swaps import RateTable, month_index

VARIANTS = ("F-USD", "F-CARRY")


def short_usd_sign(sym: str) -> int:
    """+1 if short USD means buying the symbol (EURUSD), -1 for USD-base pairs (USDJPY)."""
    return -1 if sym.startswith("USD") else 1


def currencies(variant: str, rates: RateTable, day: int) -> list[str]:
    if variant == "F-USD":
        return list(USD_PAIRS)
    m = int(month_index(day * timez.DAY)) - 1
    usd = rates.rate("USD", m)
    above = sorted((c for c in USD_PAIRS if rates.rate(c, m) > usd), key=lambda c: (-rates.rate(c, m), c))
    return above[:3]


def run_model_f(variant: str, pxs: dict, events: np.ndarray, rates: RateTable) -> tuple[np.ndarray, list]:
    """Rows of all pairs (carry DAY_DTYPE) and per event the (entry day, exit day, pairs traded)."""
    tg = {sym: {} for sym in USD_PAIRS.values()}
    log = []
    sig = {s: ewma_sigma(np.r_[np.nan, np.diff(np.log(px["p_mark"]))]) for s, px in pxs.items()}
    for t in events:
        d0, d1 = prev_weekday(int(t)), int(t)
        traded = []
        for ccy in currencies(variant, rates, d1):
            sym = USD_PAIRS[ccy]
            px = pxs[sym]
            i0, i1 = np.searchsorted(px["day"], [d0, d1])
            if i1 >= len(px["day"]) or px["day"][i0] != d0 or px["day"][i1] != d1:
                continue
            if not (px["exact"][i0] and px["exact"][i1]) or not np.isfinite(sig[sym][i0]):
                continue
            tg[sym][d0] = short_usd_sign(sym) * VOL_TARGET / sig[sym][i0]
            tg[sym][d1] = 0.0
            traded.append(sym)
        log.append((d0, d1, traded))
    rows = [run_weights(CarrySpec(sym), pxs[sym], tg[sym], rates) for sym in USD_PAIRS.values()]
    return np.concatenate(rows), log


def per_event(rows: np.ndarray, log: list) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Exit day, net and cost per event (sum over pairs of the entry- and exit-day rows)."""
    days, net, cost = [], [], []
    for d0, d1, traded in log:
        if not traded:
            continue
        sel = np.isin(rows["symbol"], traded) & np.isin(rows["day"], [d0, d1])
        days.append(d1)
        net.append(rows["net"][sel].sum())
        cost.append(rows["cost"][sel].sum())
    return np.array(days), np.array(net), np.array(cost)
