"""Model SR 'S/R zones and trend lines' (strategies no. 50 and 51), as pre-registered in docs/01_Vorregistrierung.md.

Confirmed swings (3 bars each side, known 3 bars later) of the last 120 H4 bars. A swing level is a zone if another
swing lies within +-0.25 ATR14. SR-BOUNCE: rejection at the nearest support / resistance zone; SR-BREAK: close
through a zone; SR-TLINE: close through the line of the last two falling swing highs / rising swing lows. Stops 1 ATR
behind the zone (0.5 ATR behind the last opposite swing for SR-TLINE), at least 1 ATR from the entry; target 2 R;
time exit after 30 bars (engine in chart.engine).
"""
from __future__ import annotations

import numpy as np

from chart.swings import K, swings
from hkb.model import atr

VARIANTS = ("SR-BOUNCE", "SR-BREAK", "SR-TLINE")
WINDOW, TOL, ZONE_STOP, TL_STOP, R_MULT, MAX_BARS = 120, 0.25, 1.0, 0.5, 2.0, 30


def signals(variant: str, bars: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """(signal, stop level, minimum stop distance) per bar."""
    h, l, c = bars["h"], bars["l"], bars["c"]
    n = len(c)
    a = atr(h, l, c, 14)
    sh, sl = swings(h, l)
    sig, stop = np.zeros(n, np.int8), np.full(n, np.nan)
    hi_idx, lo_idx = np.flatnonzero(sh), np.flatnonzero(sl)
    for i in range(WINDOW, n):
        if not np.isfinite(a[i]):
            continue
        tol = TOL * a[i]
        lo_b, hi_b = i - WINDOW, i - K                 # swings j with i-120 <= j <= i-3
        hs = hi_idx[(hi_idx >= lo_b) & (hi_idx <= hi_b)]
        ls = lo_idx[(lo_idx >= lo_b) & (lo_idx <= hi_b)]
        if variant == "SR-TLINE":
            if len(hs) >= 2 and h[hs[-1]] < h[hs[-2]] and len(ls):
                j1, j2 = hs[-2], hs[-1]
                slope = (h[j2] - h[j1]) / (j2 - j1)
                line_i, line_p = h[j2] + slope * (i - j2), h[j2] + slope * (i - 1 - j2)
                if c[i] > line_i and c[i - 1] <= line_p:
                    sig[i], stop[i] = 1, l[ls[-1]] - TL_STOP * a[i]
                    continue
            if len(ls) >= 2 and l[ls[-1]] > l[ls[-2]] and len(hs):
                j1, j2 = ls[-2], ls[-1]
                slope = (l[j2] - l[j1]) / (j2 - j1)
                line_i, line_p = l[j2] + slope * (i - j2), l[j2] + slope * (i - 1 - j2)
                if c[i] < line_i and c[i - 1] >= line_p:
                    sig[i], stop[i] = -1, h[hs[-1]] + TL_STOP * a[i]
            continue
        levels = np.sort(np.r_[h[hs], l[ls]])
        if len(levels) < 2:
            continue
        gaps_ok = np.zeros(len(levels), bool)
        d = np.diff(levels)
        gaps_ok[1:] |= d <= tol
        gaps_ok[:-1] |= d <= tol
        zones = levels[gaps_ok]
        if not len(zones):
            continue
        if variant == "SR-BOUNCE":
            below, above = zones[zones < c[i]], zones[zones > c[i]]
            if len(below):
                s = below.max()
                if l[i] <= s + tol and c[i] > s + tol:
                    sig[i], stop[i] = 1, s - ZONE_STOP * a[i]
                    continue
            if len(above):
                r = above.min()
                if h[i] >= r - tol and c[i] < r - tol:
                    sig[i], stop[i] = -1, r + ZONE_STOP * a[i]
        elif variant == "SR-BREAK":
            up = zones[(zones >= c[i - 1] - tol) & (zones < c[i] - tol)]
            dn = zones[(zones <= c[i - 1] + tol) & (zones > c[i] + tol)]
            if len(up):
                z = up.max()
                sig[i], stop[i] = 1, z - ZONE_STOP * a[i]
            elif len(dn):
                z = dn.min()
                sig[i], stop[i] = -1, z + ZONE_STOP * a[i]
        else:
            raise ValueError(variant)
    return sig, stop, a
