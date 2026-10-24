"""Swing points: bar j is a swing high if H(j) > max H(j-k .. j-1) and H(j) >= max H(j+1 .. j+k) (lows mirrored);
it is known from the close of bar j+k on."""
from __future__ import annotations

import numpy as np

K = 3


def swings(h: np.ndarray, l: np.ndarray, k: int = K) -> tuple[np.ndarray, np.ndarray]:
    n = len(h)
    hi, lo = np.zeros(n, bool), np.zeros(n, bool)
    for j in range(k, n - k):
        if h[j] > h[j - k:j].max() and h[j] >= h[j + 1:j + k + 1].max():
            hi[j] = True
        if l[j] < l[j - k:j].min() and l[j] <= l[j + 1:j + k + 1].min():
            lo[j] = True
    return hi, lo
