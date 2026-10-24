"""Model R 'short-term reversal US500 (Connors)', as pre-registered in docs/01_Vorregistrierung.md.

From the daily 15:45 New York prices C: R-RSI2 buys when C > SMA200 and RSI2 < 10 and sells when C > SMA5;
R-7S buys when C > SMA200 and C is the lowest close of the last 7 days and sells when C is the highest close
of the last 7 days (Connors & Alvarez 2008). Position 1 x capital long or flat, traded at 15:50 on days with an
exact 15:50 bar; accounting by carry.model.run_weights with the index cost and swap model H.
"""
from __future__ import annotations

import numpy as np

from carry.model import run_weights
from smc.swaps import RateTable

VARIANTS = ("R-RSI2", "R-7S")


def sma(x: np.ndarray, n: int) -> np.ndarray:
    out = np.full(len(x), np.nan)
    c = np.cumsum(np.r_[0.0, x])
    out[n - 1:] = (c[n:] - c[:-n]) / n
    return out


def rsi_wilder(x: np.ndarray, n: int = 2) -> np.ndarray:
    d = np.diff(x)
    g, l_ = np.maximum(d, 0.0), np.maximum(-d, 0.0)
    out = np.full(len(x), np.nan)
    if len(d) < n:
        return out
    ag, al = g[:n].mean(), l_[:n].mean()
    for i in range(n, len(x)):
        if i > n:
            ag = (ag * (n - 1) + g[i - 1]) / n
            al = (al * (n - 1) + l_[i - 1]) / n
        out[i] = 100.0 if al == 0 else 100.0 - 100.0 / (1.0 + ag / al)
    return out


def rolling_extreme(x: np.ndarray, n: int, fn) -> np.ndarray:
    out = np.full(len(x), np.nan)
    for i in range(n - 1, len(x)):
        out[i] = fn(x[i - n + 1:i + 1])
    return out


def targets(px: dict, variant: str) -> dict[int, float]:
    c = px["p_sig"]
    trend = c > sma(c, 200)
    if variant == "R-RSI2":
        entry, exit_ = trend & (rsi_wilder(c, 2) < 10), c > sma(c, 5)
    else:
        entry = trend & (c <= rolling_extreme(c, 7, np.min))
        exit_ = c >= rolling_extreme(c, 7, np.max)
    out, pos = {}, 0
    for z in range(199, len(c)):
        if not px["exact"][z]:
            continue
        if pos == 0 and entry[z]:
            pos = 1
            out[int(px["day"][z])] = 1.0
        elif pos == 1 and exit_[z]:
            pos = 0
            out[int(px["day"][z])] = 0.0
    return out


def run_model_r(variant: str, spec, px: dict, rates: RateTable) -> np.ndarray:
    if variant == "HALTEN":
        return run_weights(spec, px, {int(px["day"][int(np.argmax(px["exact"]))]): 1.0}, rates)
    return run_weights(spec, px, targets(px, variant), rates)


def trades(rows: np.ndarray) -> list[tuple[int, int, float]]:
    """(entry day, holding days, net result) per completed or open long episode."""
    out, start, acc = [], None, 0.0
    for k in range(len(rows)):
        w_prev = rows["w"][k - 1] if k else 0.0
        if w_prev > 0 or rows["w"][k] > 0:
            acc += rows["net"][k]
        if w_prev == 0 and rows["w"][k] > 0:
            start = k
        if w_prev > 0 and rows["w"][k] == 0 and start is not None:
            out.append((int(rows["day"][start]), k - start, acc))
            start, acc = None, 0.0
        elif w_prev == 0 and rows["w"][k] == 0:
            acc = 0.0
    if start is not None:
        out.append((int(rows["day"][start]), len(rows) - start, acc))
    return out
