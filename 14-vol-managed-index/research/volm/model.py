"""Model V 'volatility-managed US500 long', as pre-registered in docs/01_Vorregistrierung.md.

V-VOL: every trading day w = 15 % / sigma (standard deviation of the last 21 daily log returns of the 15:45
New York price, annualised with sqrt(261)). V-MM: on the first trading day of each month w = (15 %)^2 / RV with
RV = 12 x sum of squared daily returns of the previous month (Moreira & Muir 2017). Both long only, w <= 3.
Accounting: model G's daily bookkeeping (carry.model.run_weights) with the index cost and swap model H.
"""
from __future__ import annotations

import numpy as np

from carry.model import run_weights
from smc import timez
from smc.strategy_g import ANNUAL
from smc.swaps import RateTable, month_index

VARIANTS = ("V-VOL", "V-MM")
TARGET, CAP, WINDOW = 0.15, 3.0, 21


def log_returns(px: dict) -> np.ndarray:
    return np.r_[np.nan, np.diff(np.log(px["p_sig"]))]


def targets_vol(px: dict) -> dict[int, float]:
    r = log_returns(px)
    out = {}
    for z in range(WINDOW, len(r)):
        if px["exact"][z]:
            sigma = float(np.std(r[z - WINDOW + 1:z + 1], ddof=1)) * np.sqrt(ANNUAL)
            out[int(px["day"][z])] = min(TARGET / sigma, CAP) if sigma > 0 else CAP
    return out


def targets_mm(px: dict) -> dict[int, float]:
    r = log_returns(px)
    months = month_index(px["day"] * timez.DAY)
    out = {}
    for m in np.unique(months)[1:]:
        prev = (months == m - 1) & np.isfinite(r)
        here = np.flatnonzero((months == m) & px["exact"])
        if prev.sum() < 15 or not len(here):
            continue
        rv = 12.0 * float((r[prev] ** 2).sum())
        out[int(px["day"][here[0]])] = min(TARGET ** 2 / rv, CAP) if rv > 0 else CAP
    return out


def constant(px: dict, w: float = 1.0) -> dict[int, float]:
    return {int(px["day"][int(np.argmax(px["exact"]))]): w}


def run_model_v(variant: str, spec, px: dict, rates: RateTable) -> np.ndarray:
    targets = {"V-VOL": targets_vol, "V-MM": targets_mm, "KONSTANT": constant}[variant](px)
    return run_weights(spec, px, targets, rates)
