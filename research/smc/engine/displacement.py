"""Displacement: an energetic 1-3 bar move, measured against the ATR *before* the impulse.

Blueprint 6.5: sum of bodies >= kd * ATR (one bar) or >= 1.5 * kd * ATR (2-3 bars), every
body/range >= 0.5 and the mean >= 0.6, all bars closing in the move's direction.
"""
from __future__ import annotations

import numpy as np


def body_ratio(o, h, l, c):
    rng = h - l
    return np.where(rng > 0, np.abs(c - o) / np.where(rng > 0, rng, 1.0), 0.0)


def is_displacement(o, h, l, c, atr_ref: float, a: int, b: int, direction: int, kd: float = 1.2) -> bool:
    if a < 0 or b < a or b - a > 2 or not np.isfinite(atr_ref) or atr_ref <= 0:
        return False
    seg = slice(a, b + 1)
    body = c[seg] - o[seg]
    if np.any(np.sign(body) != direction):
        return False
    ratio = body_ratio(o[seg], h[seg], l[seg], c[seg])
    if ratio.min() < 0.5 or ratio.mean() < 0.6:
        return False
    need = kd * atr_ref * (1.0 if b == a else 1.5)
    return float(np.abs(body).sum()) >= need


class DisplacementIndex:
    """Precomputed displacement windows for one bar series.

    end[d][a] = smallest b in {a, a+1, a+2} such that bars a..b form a displacement in
    direction d (ATR taken at a-1), or -1. Equivalent to calling is_displacement for
    every start bar, but vectorised.
    """

    def __init__(self, o, h, l, c, atr14, kd: float = 1.2):
        n = len(c)
        body = c - o
        absb = np.abs(body)
        rr = body_ratio(o, h, l, c)
        ref = np.r_[np.nan, atr14[:-1]]
        ok_ref = np.isfinite(ref) & (ref > 0)
        self.end = {}
        for d in (1, -1):
            sd = np.sign(body) == d
            ends = np.full(n, -1, dtype=np.int64)
            for m in (3, 2, 1):  # assign longer windows first so the shortest valid one wins
                if n < m:
                    continue
                idx = np.arange(n - m + 1)
                same = np.ones(len(idx), bool)
                rmin = np.full(len(idx), np.inf)
                rsum = np.zeros(len(idx))
                bsum = np.zeros(len(idx))
                for j in range(m):
                    same &= sd[idx + j]
                    rmin = np.minimum(rmin, rr[idx + j])
                    rsum += rr[idx + j]
                    bsum += absb[idx + j]
                need = kd * ref[idx] * (1.0 if m == 1 else 1.5)
                ok = same & (rmin >= 0.5) & (rsum / m >= 0.6) & ok_ref[idx] & (bsum >= need)
                ends[idx[ok]] = idx[ok] + m - 1
            ends[0] = -1  # no ATR before the first bar
            self.end[d] = ends

    def first(self, lo: int, hi: int, direction: int):
        """First (start, end) of a displacement fully inside [lo, hi], or None."""
        lo = max(lo, 1)
        if hi < lo:
            return None
        e = self.end[direction][lo:hi + 1]
        ok = np.flatnonzero((e >= 0) & (e <= hi))
        if not len(ok):
            return None
        a = lo + int(ok[0])
        return a, int(self.end[direction][a])


def first_displacement(o, h, l, c, atr14: np.ndarray, lo: int, hi: int, direction: int, kd: float = 1.2):
    """Reference (slow) implementation; same result as DisplacementIndex.first."""
    for a in range(max(lo, 1), hi + 1):
        ref = atr14[a - 1]
        for b in (a, a + 1, a + 2):
            if b > hi:
                break
            if is_displacement(o, h, l, c, ref, a, b, direction, kd):
                return a, b
    return None
