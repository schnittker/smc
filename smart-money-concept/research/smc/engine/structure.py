"""Market-structure state machine per timeframe.

Two layers like LuxAlgo SMC: INT (internal pivots) and EXT (swing pivots). A break is a
close crossing a confirmed, not yet crossed pivot level (one break per pivot). The tag is
CHOCH when it goes against the layer's bias, otherwise BOS. An INT break whose level equals
the current EXT level is suppressed (LuxAlgo duplicate filter).

On top of the LuxAlgo EXT bias there is a *strict* trend that only flips on a close beyond
the protected level (the extreme that produced the last break in trend direction).

Everything known at bar k is derived from bars 0..k and pivots with pivot.k <= k.
"""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np

INT, EXT = 0, 1
BOS, CHOCH, CHOCH_STRICT = 1, 2, 3
EVENT_DTYPE = np.dtype([("k", "i8"), ("layer", "i1"), ("type", "i1"), ("dir", "i1"),
                        ("level", "f8"), ("piv_i", "i8"), ("ref_i", "i8")])


@dataclass
class _Level:
    px: float = np.nan
    i: int = -1
    crossed: bool = True


@dataclass
class StructureResult:
    events: np.ndarray        # EVENT_DTYPE, sorted by k
    bias_int: np.ndarray      # int8 per bar: LuxAlgo internal bias after bar k
    bias_ext: np.ndarray      # int8 per bar: LuxAlgo swing bias after bar k
    trend: np.ndarray         # int8 per bar: strict swing trend (0 = unknown)
    transition: np.ndarray    # bool per bar: internal CHoCH against the strict trend is active
    trail_top: np.ndarray     # dealing-range top (swing trailing extreme)
    trail_bot: np.ndarray
    prot_high: np.ndarray     # protected high while trend is bearish, else NaN
    prot_low: np.ndarray      # protected low while trend is bullish, else NaN
    int_high: np.ndarray      # current internal pivot levels (for inducement, targets)
    int_low: np.ndarray
    ext_high: np.ndarray
    ext_low: np.ndarray


def _latest_argmin(x: np.ndarray, lo: int, hi: int) -> int:
    """Index of the last minimum of x[lo..hi] (inclusive)."""
    return hi - int(np.argmin(x[lo:hi + 1][::-1]))


def _latest_argmax(x: np.ndarray, lo: int, hi: int) -> int:
    return hi - int(np.argmax(x[lo:hi + 1][::-1]))


def _by_confirm(pivots: np.ndarray, n: int) -> list[list[tuple]]:
    slots: list[list[tuple]] = [[] for _ in range(n)]
    for p in pivots:
        if p["k"] < n:
            slots[int(p["k"])].append((int(p["side"]), int(p["i"]), float(p["px"])))
    return slots


def run_structure(h: np.ndarray, l: np.ndarray, c: np.ndarray,
                  piv_int: np.ndarray, piv_ext: np.ndarray, brk_buf: np.ndarray | float = 0.0) -> StructureResult:
    n = len(c)
    buf = np.broadcast_to(np.asarray(brk_buf, dtype=float), (n,))
    ext_slots, int_slots = _by_confirm(piv_ext, n), _by_confirm(piv_int, n)
    lv = {(INT, 1): _Level(), (INT, -1): _Level(), (EXT, 1): _Level(), (EXT, -1): _Level()}
    bias = {INT: 0, EXT: 0}
    trend, transition = 0, False
    prot_hi = prot_lo = np.nan
    prot_hi_i = prot_lo_i = -1
    t_top = t_bot = np.nan

    out = {name: np.zeros(n, np.int8) for name in ("bias_int", "bias_ext", "trend")}
    out["transition"] = np.zeros(n, bool)
    for name in ("trail_top", "trail_bot", "prot_high", "prot_low", "int_high", "int_low", "ext_high", "ext_low"):
        out[name] = np.full(n, np.nan)
    events = []

    for k in range(n):
        # 1) pivots confirmed by this bar (swing first, then internal, as in LuxAlgo)
        for side, i, px in ext_slots[k]:
            lv[(EXT, side)] = _Level(px, i, False)
            if side == 1:
                t_top = px
            else:
                t_bot = px
        for side, i, px in int_slots[k]:
            lv[(INT, side)] = _Level(px, i, False)

        # 2) trailing extremes of the swing dealing range
        if not np.isnan(t_top):
            t_top = max(t_top, h[k])
        if not np.isnan(t_bot):
            t_bot = min(t_bot, l[k])

        # 3) breaks: internal first, then swing (crossover semantics)
        prev_c = c[k - 1] if k else c[k]
        for layer in (INT, EXT):
            for side in (1, -1):
                p = lv[(layer, side)]
                if p.crossed or np.isnan(p.px):
                    continue
                if side == 1:
                    crossed = c[k] > p.px + buf[k] and prev_c <= p.px + buf[k]
                else:
                    crossed = c[k] < p.px - buf[k] and prev_c >= p.px - buf[k]
                if not crossed:
                    continue
                if layer == INT and p.px == lv[(EXT, side)].px:
                    continue  # duplicate of the swing level
                p.crossed = True
                typ = CHOCH if bias[layer] == -side else BOS
                bias[layer] = side
                events.append((k, layer, typ, side, p.px, p.i, -1))
                if layer == EXT and trend in (0, side):
                    # strict trend: (re)anchor the protected level on breaks in trend direction;
                    # it is the extreme between the broken pivot and the break bar
                    trend = side
                    if side == 1:
                        j = _latest_argmin(l, p.i, k)
                        prot_lo, prot_lo_i, prot_hi, prot_hi_i = l[j], j, np.nan, -1
                    else:
                        j = _latest_argmax(h, p.i, k)
                        prot_hi, prot_hi_i, prot_lo, prot_lo_i = h[j], j, np.nan, -1

        # 4) strict trend flip on a close beyond the protected level; the new protected level
        #    is the opposite extreme between the old protected level and this bar
        if trend == 1 and not np.isnan(prot_lo) and c[k] < prot_lo - buf[k]:
            j = _latest_argmax(h, prot_lo_i, k)
            events.append((k, EXT, CHOCH_STRICT, -1, prot_lo, prot_lo_i, j))
            trend = -1
            prot_hi, prot_hi_i, prot_lo, prot_lo_i = h[j], j, np.nan, -1
        elif trend == -1 and not np.isnan(prot_hi) and c[k] > prot_hi + buf[k]:
            j = _latest_argmin(l, prot_hi_i, k)
            events.append((k, EXT, CHOCH_STRICT, 1, prot_hi, prot_hi_i, j))
            trend = 1
            prot_lo, prot_lo_i, prot_hi, prot_hi_i = l[j], j, np.nan, -1

        # internal structure running against the strict swing trend
        transition = trend != 0 and bias[INT] == -trend

        out["bias_int"][k], out["bias_ext"][k], out["trend"][k] = bias[INT], bias[EXT], trend
        out["transition"][k] = transition
        out["trail_top"][k], out["trail_bot"][k] = t_top, t_bot
        out["prot_high"][k], out["prot_low"][k] = prot_hi, prot_lo
        out["int_high"][k], out["int_low"][k] = lv[(INT, 1)].px, lv[(INT, -1)].px
        out["ext_high"][k], out["ext_low"][k] = lv[(EXT, 1)].px, lv[(EXT, -1)].px

    return StructureResult(events=np.array(events, dtype=EVENT_DTYPE), **out)
