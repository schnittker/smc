"""Swing pivots with explicit confirmation index (no lookahead when used via `k`).

Each pivot row: side (+1 high / -1 low), i (pivot bar), k (bar whose close confirms it), px.
A consumer at bar k may only use pivots with pivot.k <= k.
"""
from __future__ import annotations

import numpy as np
from numpy.lib.stride_tricks import sliding_window_view

PIVOT_DTYPE = np.dtype([("side", "i1"), ("i", "i8"), ("k", "i8"), ("px", "f8")])
BEARISH_LEG, BULLISH_LEG = 0, 1


def leg_pivots(h: np.ndarray, l: np.ndarray, size: int) -> np.ndarray:
    """LuxAlgo SMC `leg(size)` pivots.

    At bar k the candidate is c = k - size: it starts a bearish leg if high[c] exceeds all
    highs of the following `size` bars, a bullish leg if low[c] undercuts all following lows
    (high wins on outside bars). A change of leg emits the pivot of bar c, so highs and lows
    alternate; the very first pivot is always a low because the initial leg is bearish.
    """
    n = len(h)
    if n <= size:
        return np.empty(0, PIVOT_DTYPE)
    fmax = sliding_window_view(h[1:], size).max(axis=1)  # fmax[c] = max(h[c+1 .. c+size])
    fmin = sliding_window_view(l[1:], size).min(axis=1)
    m = n - size
    new_hi = h[:m] > fmax[:m]
    new_lo = l[:m] < fmin[:m]
    out = []
    leg = BEARISH_LEG
    for c in np.flatnonzero(new_hi | new_lo):
        new_leg = BEARISH_LEG if new_hi[c] else BULLISH_LEG
        if new_leg != leg:
            leg = new_leg
            if leg == BULLISH_LEG:
                out.append((-1, c, c + size, l[c]))
            else:
                out.append((1, c, c + size, h[c]))
    return np.array(out, dtype=PIVOT_DTYPE)


def fractal_pivots(h: np.ndarray, l: np.ndarray, n: int = 1) -> np.ndarray:
    """ICT short-term pivots for n=1 (3-candle swing); MT5 tie rule: strict to the right, >= to the left.

    A bar can be both a high and a low pivot (outside bar); both are returned, high first.
    """
    size = len(h)
    if size < 2 * n + 1:
        return np.empty(0, PIVOT_DTYPE)
    c = np.arange(n, size - n)
    hi = np.ones(len(c), bool)
    lo = np.ones(len(c), bool)
    for j in range(1, n + 1):
        hi &= (h[c] > h[c + j]) & (h[c] >= h[c - j])
        lo &= (l[c] < l[c + j]) & (l[c] <= l[c - j])
    rows = [(1, i, i + n, h[i]) for i in c[hi]] + [(-1, i, i + n, l[i]) for i in c[lo]]
    out = np.array(rows, dtype=PIVOT_DTYPE)
    return out[np.lexsort((-out["side"], out["i"]))] if len(out) else out
