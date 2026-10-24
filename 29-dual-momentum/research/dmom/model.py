"""Model D 'dual momentum', as pre-registered in docs/01_Vorregistrierung.md.

On the first trading day of each month (first weekday with an exact US500 bar): R12 per asset = signal price as of
that day / signal price 252 of the asset's trading days earlier - 1. D-TOP1 holds the asset with the highest R12,
D-TOP2 the two highest, each only if its R12 exceeds last month's USD rate; size 10 % / sigma (EWMA as model G),
reset monthly. Targets move to each asset's first exactly marked day on or after the decision day. Accounting with
carry.model.run_weights and cost model H.
"""
from __future__ import annotations

import numpy as np

from carry.model import apply_days, ewma_sigma, run_weights
from smc import timez
from smc.strategy_g import VOL_TARGET
from smc.swaps import RateTable, month_index

ASSETS = ("SPXUSD", "NSXUSD", "FRXEUR", "UKXGBP", "JPXJPY", "HKXHKD", "AUXAUD", "XAUUSD")
VARIANTS = {"D-TOP1": 1, "D-TOP2": 2}
LOOKBACK = 252


def decision_days(px_ref: dict) -> list[int]:
    months = month_index(px_ref["day"] * timez.DAY)
    out, seen = [], set()
    for i in np.flatnonzero(px_ref["exact"]):
        if months[i] not in seen:
            seen.add(months[i])
            out.append(int(px_ref["day"][i]))
    return out


def r12(px: dict, day: int) -> float:
    i = int(np.searchsorted(px["day"], day, side="right")) - 1
    if i < LOOKBACK:
        return np.nan
    return float(px["p_sig"][i] / px["p_sig"][i - LOOKBACK] - 1)


def schedule(pxs: dict, rates: RateTable, top: int) -> tuple[dict[str, dict[int, float]], list]:
    sig = {a: ewma_sigma(np.r_[np.nan, np.diff(np.log(px["p_mark"]))]) for a, px in pxs.items()}
    targets = {a: {} for a in pxs}
    log = []
    for d in decision_days(pxs["SPXUSD"]):
        mom = {a: r12(px, d) for a, px in pxs.items()}
        if not all(np.isfinite(v) for v in mom.values()):
            continue
        hurdle = rates.rate("USD", int(month_index(d * timez.DAY)) - 1)
        chosen = [a for a in sorted(mom, key=lambda a: (-mom[a], a))[:top] if mom[a] > hurdle]
        for a, px in pxs.items():
            i = int(np.searchsorted(px["day"], d, side="right")) - 1
            s = sig[a][i] if i >= 0 else np.nan
            targets[a][d] = VOL_TARGET / s if a in chosen and np.isfinite(s) else 0.0
        log.append((d, chosen))
    return targets, log


def run_model_d(variant: str, specs: dict, pxs: dict, rates: RateTable) -> tuple[np.ndarray, list]:
    targets, log = schedule(pxs, rates, VARIANTS[variant])
    rows = [run_weights(specs[a], pxs[a], apply_days(pxs[a], targets[a]), rates) for a in pxs]
    return np.concatenate(rows), log
