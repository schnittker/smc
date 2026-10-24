"""Model HP 'harmonic patterns, Wyckoff spring, M5 scalping' (strategies no. 77, 79 and 80), as pre-registered in
docs/01_Vorregistrierung.md."""
from __future__ import annotations

import numpy as np

from chart.swings import K, swings
from hkb.model import atr, ema
from smc.timez import eu_dst

VARIANTS = {"HP-HARM": "H4", "HP-SPRING": "H4", "HP-SCALP": "M5"}
LIST_NO = {"HP-HARM": 77, "HP-SPRING": 79, "HP-SCALP": 80}
PATTERNS = {"Gartley": ((0.568, 0.668), (0.382, 0.886), (0.736, 0.836)),
            "Bat": ((0.382, 0.500), (0.382, 0.886), (0.836, 0.936))}
PAD, TGT_FIB, RANGE_N, RANGE_ATR = 0.25, 0.618, 40, 6.0
SCALP_FROM, SCALP_TO, SCALP_STOP, SCALP_BARS = 7 * 60, 15 * 60 + 55, 1.5, 12


def _ok(x, lo_hi):
    return lo_hi[0] <= x <= lo_hi[1]


def harmonic_signals(bars):
    """(signal, stop, minimum distance = 1 ATR, target) per H4 bar."""
    h, l, c = bars["h"], bars["l"], bars["c"]
    n = len(c)
    a = atr(h, l, c, 14)
    sh, sl = swings(h, l)
    sig, stop, tgt = np.zeros(n, np.int8), np.full(n, np.nan), np.full(n, np.nan)
    seq: list[tuple[int, int, float]] = []          # (bar, +1 high / -1 low, price), alternating
    for j in range(n - K):
        if sh[j] == sl[j]:                          # no swing, or an outside bar that is both (skipped)
            continue
        typ, price = (1, h[j]) if sh[j] else (-1, l[j])
        if seq and seq[-1][1] == typ:
            if (typ == 1 and price > seq[-1][2]) or (typ == -1 and price < seq[-1][2]):
                seq[-1] = (j, typ, price)
            else:
                continue
        else:
            seq.append((j, typ, price))
        i = j + K
        if len(seq) < 5 or not np.isfinite(a[i]):
            continue
        (_, tx, X), (_, _, A), (_, _, B), (_, _, C), (_, _, D) = seq[-5:]
        if tx == -1:                                # bullish: X low, A high, B low, C high, D low
            xa, ab, bc, ad = A - X, A - B, C - B, A - D
        else:                                       # bearish: X high, A low, B high, C low, D high
            xa, ab, bc, ad = X - A, B - A, B - C, D - A
        if min(xa, ab, bc, ad) <= 0:
            continue
        if any(_ok(ab / xa, r1) and _ok(bc / ab, r2) and _ok(ad / xa, r3) for r1, r2, r3 in PATTERNS.values()):
            if tx == -1:
                sig[i], stop[i], tgt[i] = 1, X - PAD * a[i], D + TGT_FIB * (A - D)
            else:
                sig[i], stop[i], tgt[i] = -1, X + PAD * a[i], D - TGT_FIB * (D - A)
    return sig, stop, a, tgt


def spring_signals(bars):
    h, l, c = bars["h"], bars["l"], bars["c"]
    n = len(c)
    a = atr(h, l, c, 14)
    sig, stop, tgt = np.zeros(n, np.int8), np.full(n, np.nan), np.full(n, np.nan)
    if n <= RANGE_N:
        return sig, stop, a, tgt
    rh = np.r_[np.full(RANGE_N, np.nan), np.lib.stride_tricks.sliding_window_view(h, RANGE_N).max(axis=1)[:-1]]
    rl = np.r_[np.full(RANGE_N, np.nan), np.lib.stride_tricks.sliding_window_view(l, RANGE_N).min(axis=1)[:-1]]
    ok = np.isfinite(a) & (rh - rl <= RANGE_ATR * a)
    long_ = ok & (l < rl) & (c > rl)
    short_ = ok & (h > rh) & (c < rh)
    both = long_ & short_
    long_, short_ = long_ & ~both, short_ & ~both
    sig[long_], stop[long_], tgt[long_] = 1, (l - PAD * a)[long_], rh[long_]
    sig[short_], stop[short_], tgt[short_] = -1, (h + PAD * a)[short_], rl[short_]
    return sig, stop, a, tgt


def scalp_signals(bars):
    """(signal, exit flag long, exit flag short, entry allowed) per M5 bar."""
    c = bars["c"]
    e9, e21 = ema(c, 9), ema(c, 21)
    p9, p21 = np.r_[np.nan, e9[:-1]], np.r_[np.nan, e21[:-1]]
    sig = np.zeros(len(c), np.int8)
    sig[(p9 <= p21) & (e9 > e21)] = 1
    sig[(p9 >= p21) & (e9 < e21)] = -1
    t = bars["t"]
    lon_min = ((t + 3600 * eu_dst(t).astype(np.int64)) % 86400) // 60
    allow = (lon_min >= SCALP_FROM) & (lon_min <= SCALP_TO)
    return sig, e9 < e21, e9 > e21, allow
