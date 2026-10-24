"""Model X 'VIX regime', as pre-registered in docs/01_Vorregistrierung.md.

Risk-off on VIX trading day t when the VIX close is at or above the 90 % quantile of the 252 closes before t.
X-HAVEN: long JPY (short USDJPY), long CHF (short USDCHF) and long XAUUSD from 16:50 New York on day t while
risk-off; X-FEAR: long US500 from 15:50 New York on the next US500 trading day. Each position 10 % / sigma
(EWMA as model G) set at entry; flat otherwise. Accounting with carry.model.run_weights.
"""
from __future__ import annotations

import csv
from datetime import date
from pathlib import Path

import numpy as np

from carry.model import apply_days, ewma_sigma, run_weights
from smc.strategy_g import VOL_TARGET
from smc.swaps import RateTable

EPOCH = date(1970, 1, 1)
LOOKBACK, QUANTILE = 252, 0.9
HAVEN = {"USDJPY": -1, "USDCHF": -1, "XAUUSD": 1}
VARIANTS = {"X-HAVEN": HAVEN, "X-FEAR": {"SPXUSD": 1}}


def load_vix(path: Path) -> tuple[np.ndarray, np.ndarray]:
    days, close = [], []
    with path.open(encoding="utf-8") as f:
        for r in csv.DictReader(f):
            m, d, y = (int(x) for x in r["DATE"].split("/"))
            days.append((date(y, m, d) - EPOCH).days)
            close.append(float(r["CLOSE"]))
    return np.array(days, np.int64), np.array(close)


def risk_off(close: np.ndarray) -> np.ndarray:
    out = np.zeros(len(close), bool)
    for i in range(LOOKBACK, len(close)):
        out[i] = close[i] >= np.quantile(close[i - LOOKBACK:i], QUANTILE)
    return out


def regime_changes(days: np.ndarray, flag: np.ndarray) -> list[tuple[int, bool]]:
    """(VIX day, new state) whenever the regime switches, starting from the first day with a full lookback."""
    out, state = [], False
    for d, f in zip(days[LOOKBACK:], flag[LOOKBACK:]):
        if f != state:
            out.append((int(d), bool(f)))
            state = bool(f)
    return out


def targets(px: dict, changes: list[tuple[int, bool]], sign: int, next_day: bool) -> dict[int, float]:
    """Target weights on the execution days of regime changes (same day, or the next px day for X-FEAR)."""
    sigma = ewma_sigma(np.r_[np.nan, np.diff(np.log(px["p_mark"]))])
    out = {}
    for d, on in changes:
        i = int(np.searchsorted(px["day"], d, side="right" if next_day else "left"))
        if i >= len(px["day"]):
            continue
        if on and not np.isfinite(sigma[i]):
            continue
        out[int(px["day"][i])] = sign * VOL_TARGET / sigma[i] if on else 0.0
    return out


def run_model_x(variant: str, specs: dict, pxs: dict, vix: tuple[np.ndarray, np.ndarray], rates: RateTable) -> np.ndarray:
    days, close = vix
    changes = regime_changes(days, risk_off(close))
    parts = []
    for sym, sign in VARIANTS[variant].items():
        t = targets(pxs[sym], changes, sign, next_day=(variant == "X-FEAR"))
        parts.append(run_weights(specs[sym], pxs[sym], apply_days(pxs[sym], t), rates))
    return np.concatenate(parts)
