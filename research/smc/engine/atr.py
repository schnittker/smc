"""Wilder ATR, seeded with the simple mean of the first n true ranges (as MT5 iATR and Pine ta.atr)."""
from __future__ import annotations

import numpy as np


def true_range(h: np.ndarray, l: np.ndarray, c: np.ndarray) -> np.ndarray:
    prev_c = np.r_[c[0], c[:-1]]
    return np.maximum(h - l, np.maximum(np.abs(h - prev_c), np.abs(l - prev_c)))


def atr(h: np.ndarray, l: np.ndarray, c: np.ndarray, n: int = 14) -> np.ndarray:
    """ATR value at index i uses bars 0..i only; NaN until n bars are available."""
    tr = true_range(h, l, c)
    out = np.full(len(tr), np.nan)
    if len(tr) < n:
        return out
    a = tr[:n].mean()
    out[n - 1] = a
    k = (n - 1) / n
    for i in range(n, len(tr)):
        a = a * k + tr[i] / n
        out[i] = a
    return out
