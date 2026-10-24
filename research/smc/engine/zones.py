"""PD-array zones: fair value gaps, order blocks, and their lifecycle on any evaluation series.

Zone convention: dir = +1 support (bullish, long), -1 resistance. `top`/`bot` are the trade
zone, `mid` its CE / mean threshold, `stop` the invalidation reference beyond the zone.
`k` is the bar whose close makes the zone known; lifecycle starts with the next bar.
"""
from __future__ import annotations

import numpy as np

from smc.engine.displacement import DisplacementIndex, body_ratio

ZONE_DTYPE = np.dtype([
    ("kind", "i1"), ("dir", "i1"), ("k", "i8"), ("origin", "i8"),
    ("top", "f8"), ("bot", "f8"), ("mid", "f8"), ("stop", "f8"),
    ("size_atr", "f8"), ("flags", "i4"),
])
FVG, OB = 1, 2
# flags
F_STRONG = 1          # FVG: middle candle is a full displacement / OB: FVG adjacent to the block
F_NO_OPPOSITE = 2     # OB: no opposite-colour candle found, fell back to the leg extreme
F_EXT = 4             # OB: created by a swing (external) break, else internal
F_FVG_IN_LEG = 8      # OB: a same-direction FVG exists inside the displacement leg


def detect_fvg(o, h, l, c, atr14, k_fvg: float = 0.2, min_abs: float = 0.0, min_body: float = 0.5,
               kd: float = 1.2) -> np.ndarray:
    """3-candle gaps: bullish when low[k] > high[k-2] and candle k-1 closed above high[k-2]."""
    n = len(c)
    if n < 3:
        return np.empty(0, ZONE_DTYPE)
    k = np.arange(2, n)
    ref = atr14[k - 2]
    min_gap = np.maximum(k_fvg * ref, min_abs)
    ratio = body_ratio(o[k - 1], h[k - 1], l[k - 1], c[k - 1])
    bull = (l[k] > h[k - 2]) & (c[k - 1] > h[k - 2]) & (ratio >= min_body) & (l[k] - h[k - 2] >= min_gap)
    bear = (h[k] < l[k - 2]) & (c[k - 1] < l[k - 2]) & (ratio >= min_body) & (l[k - 2] - h[k] >= min_gap)
    rows = []
    for kk in k[(bull | bear) & np.isfinite(ref)]:
        d = 1 if l[kk] > h[kk - 2] else -1
        top, bot = (l[kk], h[kk - 2]) if d == 1 else (l[kk - 2], h[kk])
        a = atr14[kk - 2]
        strong = abs(c[kk - 1] - o[kk - 1]) >= kd * a
        rows.append((FVG, d, kk, kk - 1, top, bot, (top + bot) / 2, bot if d == 1 else top,
                     (top - bot) / a, F_STRONG if strong else 0))
    return np.array(rows, dtype=ZONE_DTYPE)


def detect_order_blocks(o, h, l, c, atr14, events, fvgs, kd: float = 1.2, max_run: int = 3,
                        max_height_atr: float = 1.5, require_fvg: bool = True,
                        disp: DisplacementIndex | None = None) -> np.ndarray:
    """Hybrid ICT/LuxAlgo order blocks for structure breaks (blueprint 6.4).

    For a bullish break of the pivot at bar s on bar b: leg low = last minimum in (s, b];
    the block is the last down-close candle (plus up to max_run-1 adjacent ones) before the
    displacement that starts from the leg low; it needs a displacement, a close above the
    block high inside the leg and (by default) a bullish FVG inside the leg.
    """
    from smc.engine.structure import CHOCH_STRICT, EXT

    rows = []
    disp = disp or DisplacementIndex(o, h, l, c, atr14, kd)
    fvg_by_dir = {d: fvgs[fvgs["dir"] == d] for d in (1, -1)}  # sorted by origin
    fvg_origin = {d: np.ascontiguousarray(fvg_by_dir[d]["origin"]) for d in (1, -1)}
    opposite_of = {1: c < o, -1: c > o}   # the block is the last candle against the move
    for e in events:
        if e["type"] == CHOCH_STRICT:
            continue
        d, s, b = int(e["dir"]), int(e["piv_i"]), int(e["k"])
        if b - s < 2:
            continue
        seg_lo, seg_hi = s + 1, b
        if d == 1:
            leg = seg_hi - int(np.argmin(l[seg_lo:seg_hi + 1][::-1]))
        else:
            leg = seg_hi - int(np.argmax(h[seg_lo:seg_hi + 1][::-1]))
        found = disp.first(leg, b, d)
        if found is None:
            continue
        start = found[0]
        opposite = opposite_of[d]
        k_ob = -1
        for j in range(start - 1, max(s + 1, leg - 2) - 1, -1):
            if opposite[j]:
                k_ob = j
                break
        flags = F_EXT if e["layer"] == EXT else 0
        if k_ob < 0:
            k_ob, flags = leg, flags | F_NO_OPPOSITE
        k0 = k_ob
        while k_ob - k0 < max_run - 1 and k0 - 1 > s and opposite[k0 - 1] and not flags & F_NO_OPPOSITE:
            k0 -= 1
        blk = slice(k0, k_ob + 1)
        hi_full, lo_full = h[blk].max(), l[blk].min()
        body_hi = np.maximum(o[blk], c[blk]).max()
        body_lo = np.minimum(o[blk], c[blk]).min()
        # trade-through: some close inside the leg beyond the far side of the block
        after = c[k_ob + 1:b + 1]
        traded_through = (after > hi_full).any() if d == 1 else (after < lo_full).any()
        if not traded_through:
            continue
        f = fvg_by_dir[d]
        lo_i, hi_i = np.searchsorted(fvg_origin[d], [k_ob, b], side="right")
        in_leg = f[lo_i:hi_i]
        if len(in_leg):
            flags |= F_FVG_IN_LEG
            if (in_leg["origin"] == k_ob + 1).any() or (in_leg["origin"] == k_ob + 2).any():
                flags |= F_STRONG
        elif require_fvg:
            continue
        a = atr14[k_ob - 1] if k_ob > 0 else np.nan
        if d == 1:
            top = body_hi
            bot = lo_full if (hi_full - lo_full) <= max_height_atr * a else body_lo
            stop = min(lo_full, l[leg])
        else:
            bot = body_lo
            top = hi_full if (hi_full - lo_full) <= max_height_atr * a else body_hi
            stop = max(hi_full, h[leg])
        mid = (body_hi + body_lo) / 2
        rows.append((OB, d, b, k_ob, top, bot, mid, stop, (top - bot) / a if a > 0 else np.nan, flags))
    out = np.array(rows, dtype=ZONE_DTYPE)
    return out[np.argsort(out["k"], kind="stable")] if len(out) else out


LIFE_DTYPE = np.dtype([("touch", "i8"), ("mid", "i8"), ("far", "i8"), ("invalid", "i8")])


def lifecycle(zones: np.ndarray, start_idx: np.ndarray, o, h, l, c, max_bars: int) -> np.ndarray:
    """First bar index (in the evaluation series) of touch, mid reached, far edge reached, invalidation.

    start_idx[z] = first evaluation bar that opens after the zone is known. -1 = never within max_bars.
    Invalidation: FVG -> body beyond the far edge; OB -> close beyond the stop reference.
    """
    out = np.full(len(zones), -1, dtype=LIFE_DTYPE)
    n = len(c)
    for z, s in enumerate(start_idx):
        if s < 0 or s >= n:
            continue
        e = min(n, s + max_bars)
        zz = zones[z]
        if zz["dir"] == 1:
            wick = l[s:e]
            prox, mid, far = zz["top"], zz["mid"], zz["bot"]
            touch, midr, farr = wick <= prox, wick <= mid, wick <= far
            if zz["kind"] == FVG:
                inval = np.minimum(o[s:e], c[s:e]) < far
            else:
                inval = c[s:e] < zz["stop"]
        else:
            wick = h[s:e]
            prox, mid, far = zz["bot"], zz["mid"], zz["top"]
            touch, midr, farr = wick >= prox, wick >= mid, wick >= far
            if zz["kind"] == FVG:
                inval = np.maximum(o[s:e], c[s:e]) > far
            else:
                inval = c[s:e] > zz["stop"]
        for name, arr in (("touch", touch), ("mid", midr), ("far", farr), ("invalid", inval)):
            if arr.any():
                out[name][z] = s + int(np.argmax(arr))
    return out
