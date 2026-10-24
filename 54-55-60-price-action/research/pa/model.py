"""Model PA 'price action' (strategies no. 54, 55 and 60), as pre-registered in docs/01_Vorregistrierung.md.

H4 signals at the close of bar i (ATR = ATR14(i), R = high - low); zones as in model SR (no. 50).
  PA-PIN  pin bar (range >= 1 ATR, wick >= 2/3, body in the far third) rejecting the nearest zone
  PA-ENG  engulfing pattern whose two-bar extreme touches the nearest zone and closes beyond it
  PA-DT   double bottom / top (last two confirmed swings within 0.5 ATR, >= 6 bars apart, neckline >= 2 ATR away)
          broken by the close; target = measured move
  PA-SD   first retest of a demand / supply zone (base bar with R <= 0.8 ATR before an impulse body >= 2 ATR,
          within 120 bars) that holds on the close
Stops behind the pattern (+0.25 ATR, at least 1 ATR from the entry), target 2 R unless stated, time exit after 30
bars (chart.engine). Opposite signals in the same bar cancel each other.
"""
from __future__ import annotations

import numpy as np

from chart.swings import K, swings
from hkb.model import atr

VARIANTS = ("PA-PIN", "PA-ENG", "PA-DT", "PA-SD")
WINDOW, TOL, PAD, R_MULT, MAX_BARS = 120, 0.25, 0.25, 2.0, 30
PIN_MIN_ATR, WICK, BASE_ATR, IMPULSE_ATR, DT_TOL, DT_GAP, DT_DEPTH = 1.0, 2 / 3, 0.8, 2.0, 0.5, 6, 2.0


def zones(levels: np.ndarray, tol: float) -> np.ndarray:
    lv = np.sort(levels)
    if len(lv) < 2:
        return lv[:0]
    d = np.diff(lv)
    ok = np.zeros(len(lv), bool)
    ok[1:] |= d <= tol
    ok[:-1] |= d <= tol
    return lv[ok]


def signals(variant: str, bars: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """(signal, stop level, minimum stop distance = 1 ATR, target level or NaN for 2 R) per bar."""
    o, h, l, c = bars["o"], bars["h"], bars["l"], bars["c"]
    n = len(c)
    a = atr(h, l, c, 14)
    sig, stop, tgt = np.zeros(n, np.int8), np.full(n, np.nan), np.full(n, np.nan)
    if variant == "PA-SD":
        _supply_demand(o, h, l, c, a, sig, stop)
        return sig, stop, a, tgt
    sh, sl = swings(h, l)
    hi_idx, lo_idx = np.flatnonzero(sh), np.flatnonzero(sl)
    for i in range(WINDOW, n):
        if not np.isfinite(a[i]):
            continue
        tol = TOL * a[i]
        hs = hi_idx[(hi_idx >= i - WINDOW) & (hi_idx <= i - K)]
        ls = lo_idx[(lo_idx >= i - WINDOW) & (lo_idx <= i - K)]
        long_ = short_ = None
        if variant in ("PA-PIN", "PA-ENG"):
            z = zones(np.r_[h[hs], l[ls]], tol)
            below, above = z[z < c[i]], z[z > c[i]]
            s = below.max() if len(below) else np.nan
            w = above.min() if len(above) else np.nan
            rng = h[i] - l[i]
            if variant == "PA-PIN":
                if rng >= PIN_MIN_ATR * a[i]:
                    if min(o[i], c[i]) >= l[i] + WICK * rng and l[i] <= s + tol < c[i]:
                        long_ = l[i] - PAD * a[i]
                    if max(o[i], c[i]) <= h[i] - WICK * rng and h[i] >= w - tol > c[i]:
                        short_ = h[i] + PAD * a[i]
            else:
                lo2, hi2 = min(l[i - 1], l[i]), max(h[i - 1], h[i])
                if c[i - 1] < o[i - 1] and c[i] > o[i] and o[i] <= c[i - 1] and c[i] >= o[i - 1] \
                        and lo2 <= s + tol < c[i]:
                    long_ = lo2 - PAD * a[i]
                if c[i - 1] > o[i - 1] and c[i] < o[i] and o[i] >= c[i - 1] and c[i] <= o[i - 1] \
                        and hi2 >= w - tol > c[i]:
                    short_ = hi2 + PAD * a[i]
        elif variant == "PA-DT":
            lk, hk = lo_idx[lo_idx <= i - K], hi_idx[hi_idx <= i - K]
            if len(lk) >= 2:
                j1, j2 = lk[-2], lk[-1]
                if abs(l[j1] - l[j2]) <= DT_TOL * a[i] and j2 - j1 >= DT_GAP:
                    neck = h[j1:j2 + 1].max()
                    low = min(l[j1], l[j2])
                    if neck - max(l[j1], l[j2]) >= DT_DEPTH * a[i] and c[i] > neck >= c[i - 1]:
                        long_ = low - PAD * a[i]
                        tgt_long = neck + (neck - low)
            if len(hk) >= 2:
                j1, j2 = hk[-2], hk[-1]
                if abs(h[j1] - h[j2]) <= DT_TOL * a[i] and j2 - j1 >= DT_GAP:
                    neck = l[j1:j2 + 1].min()
                    top = max(h[j1], h[j2])
                    if min(h[j1], h[j2]) - neck >= DT_DEPTH * a[i] and c[i] < neck <= c[i - 1]:
                        short_ = top + PAD * a[i]
                        tgt_short = neck - (top - neck)
        else:
            raise ValueError(variant)
        if long_ is not None and short_ is None:
            sig[i], stop[i] = 1, long_
            if variant == "PA-DT":
                tgt[i] = tgt_long
        elif short_ is not None and long_ is None:
            sig[i], stop[i] = -1, short_
            if variant == "PA-DT":
                tgt[i] = tgt_short
    return sig, stop, a, tgt


def _supply_demand(o, h, l, c, a, sig, stop):
    n = len(c)
    hits: dict[int, list[tuple[int, int, float]]] = {}       # retest bar -> [(zone bar k, direction, stop)]
    for k in range(1, n - 2):
        if not (np.isfinite(a[k]) and np.isfinite(a[k + 1])) or h[k] - l[k] > BASE_ATR * a[k]:
            continue
        body = c[k + 1] - o[k + 1]
        lo_i, hi_i = k + 2, min(n, k + WINDOW + 1)
        if abs(body) < IMPULSE_ATR * a[k + 1] or lo_i >= hi_i:
            continue
        if body > 0:                                       # demand: proximal = top of the base body, distal = low
            prox, dist = max(o[k], c[k]), l[k]
            touch = np.flatnonzero(l[lo_i:hi_i] <= prox)
            if len(touch):
                i = lo_i + int(touch[0])
                if c[i] > dist and np.isfinite(a[i]):
                    hits.setdefault(i, []).append((k, 1, dist - PAD * a[i]))
        else:                                              # supply: proximal = bottom of the base body, distal = high
            prox, dist = min(o[k], c[k]), h[k]
            touch = np.flatnonzero(h[lo_i:hi_i] >= prox)
            if len(touch):
                i = lo_i + int(touch[0])
                if c[i] < dist and np.isfinite(a[i]):
                    hits.setdefault(i, []).append((k, -1, dist + PAD * a[i]))
    for i, zs in hits.items():
        if len({d for _, d, _ in zs}) == 1:                # opposite retests in the same bar cancel each other
            k, d, s = max(zs)                              # the most recent zone
            sig[i], stop[i] = d, s
