"""Liquidity pools and their sweep / break outcome on the trigger timeframe.

A pool is a price where resting stops are assumed: buy stops above highs (side +1, BSL)
or sell stops below lows (side -1, SSL). It becomes known at `t_avail` (UTC) and is
watched until `t_expire`. On the evaluation bars (normally M5) the first wick beyond the
level decides the outcome:
  SWEPT  - the bar closes back inside, or a later close returns inside before acceptance
  BROKEN - n_accept consecutive closes beyond the level
Buy stops trigger on the ask: a BSL counts as pierced when high + spread exceeds it.
"""
from __future__ import annotations

import numpy as np

from smc import timez

POOL_DTYPE = np.dtype([("side", "i1"), ("kind", "i1"), ("px", "f8"), ("t_avail", "i8"), ("t_expire", "i8")])
# pool kinds, ordered by significance (blueprint 6.3)
SWING_INT, SESSION_ASIA, SESSION_PRELDN, SESSION_LDN, SWING_EXT, EQ, PDHL, PWHL, PMHL = range(1, 10)
KIND_NAMES = {SWING_INT: "swing_int", SESSION_ASIA: "asia", SESSION_PRELDN: "pre_london", SESSION_LDN: "london",
              SWING_EXT: "swing_ext", EQ: "eq", PDHL: "pdhl", PWHL: "pwhl", PMHL: "pmhl"}
KIND_WEIGHT = {SWING_INT: 1.0, SESSION_ASIA: 1.5, SESSION_PRELDN: 1.5, SESSION_LDN: 1.5, SWING_EXT: 2.0,
               EQ: 3.0, PDHL: 3.0, PWHL: 4.0, PMHL: 5.0}

SWEPT, BROKEN = 1, 2
OUTCOME_DTYPE = np.dtype([("pool", "i8"), ("side", "i1"), ("kind", "i1"), ("px", "f8"), ("pierce", "i8"),
                          ("k", "i8"), ("outcome", "i1"), ("extreme", "f8")])


def pools_from_pivots(pivots: np.ndarray, t_close: np.ndarray, kind: int, ttl_seconds: int) -> np.ndarray:
    out = np.empty(len(pivots), POOL_DTYPE)
    out["side"] = pivots["side"]
    out["kind"] = kind
    out["px"] = pivots["px"]
    out["t_avail"] = t_close[pivots["k"]]
    out["t_expire"] = out["t_avail"] + ttl_seconds
    return out


def equal_level_pools(pivots: np.ndarray, t_close: np.ndarray, atr_long: np.ndarray, atr_short: np.ndarray,
                      tol_atr: float = 0.1, min_pullback_atr: float = 0.5, min_sep: int = 6,
                      ttl_seconds: int = 5 * 86400) -> np.ndarray:
    """EQH/EQL: two consecutive same-side pivots within tol_atr * ATR(long), with a real pullback between."""
    rows = []
    last = {1: None, -1: None}
    last_opp_px = {1: None, -1: None}
    for p in pivots:
        side = int(p["side"])
        prev = last[side]
        k = int(p["k"])
        if prev is not None and np.isfinite(atr_long[k]):
            opp = last_opp_px[side]
            pull = abs(prev["px"] - opp) if opp is not None else 0.0
            if (abs(p["px"] - prev["px"]) <= tol_atr * atr_long[k] and p["i"] - prev["i"] >= min_sep
                    and pull >= min_pullback_atr * atr_short[k]):
                px = max(p["px"], prev["px"]) if side == 1 else min(p["px"], prev["px"])
                rows.append((side, EQ, px, t_close[k], t_close[k] + ttl_seconds))
        last[side] = p
        last_opp_px[-side] = p["px"]  # the opposite pivot after the previous same-side pivot
    return np.array(rows, dtype=POOL_DTYPE)


def period_pools(bars: np.ndarray, tf_seconds: int, kind: int, ttl_periods: int = 1) -> np.ndarray:
    """High/low of each completed period bar (e.g. D1 -> PDH/PDL), valid for the next ttl_periods periods."""
    t_close = bars["t"] + tf_seconds
    hi = np.empty(len(bars), POOL_DTYPE)
    lo = np.empty(len(bars), POOL_DTYPE)
    for arr, side, px in ((hi, 1, bars["h"]), (lo, -1, bars["l"])):
        arr["side"], arr["kind"], arr["px"] = side, kind, px
        arr["t_avail"], arr["t_expire"] = t_close, t_close + ttl_periods * tf_seconds
    return np.concatenate([hi, lo])


def calendar_period_bars(d1: np.ndarray, period: str) -> tuple[np.ndarray, np.ndarray]:
    """Aggregate D1 bars into weeks ('W') or months ('M'); returns (period high/low rows, close times)."""
    day = d1["ts"] // 86400
    if period == "W":
        key = (day + 3) // 7          # weeks starting Monday (server days)
    else:
        key = np.array([int(str(np.datetime64(int(s), "s"))[:7].replace("-", "")) for s in d1["ts"]])
    starts = np.flatnonzero(np.r_[True, key[1:] != key[:-1]])
    ends = np.r_[starts[1:], len(d1)] - 1
    hi = np.maximum.reduceat(d1["h"], starts)
    lo = np.minimum.reduceat(d1["l"], starts)
    t_close = d1["t"][ends] + 86400
    return np.stack([hi, lo], axis=1), t_close


def session_pools(m5: np.ndarray, windows: dict[int, tuple[int, int]]) -> np.ndarray:
    """High/low of NY-time windows inside each FX day, known at the window end.

    windows: kind -> (start_minute, end_minute) in NY time, e.g. ASIA (20*60, 24*60).
    FX days run 17:00-17:00 NY, so 20:00-24:00 NY belongs to the following trading day.
    """
    ny_min = timez.ny_minute_of_day(m5["t"])
    fxday = m5["ts"] // 86400
    rows = []
    for kind, (a, b) in windows.items():
        sel = (ny_min >= a) & (ny_min < b) if a < b else ((ny_min >= a) | (ny_min < b))
        idx = np.flatnonzero(sel)
        if not len(idx):
            continue
        days = fxday[idx]
        starts = np.flatnonzero(np.r_[True, days[1:] != days[:-1]])
        ends = np.r_[starts[1:], len(idx)] - 1
        hi = np.maximum.reduceat(m5["h"][idx], starts)
        lo = np.minimum.reduceat(m5["l"][idx], starts)
        # window end in server time: FX-day start (00:00 server = 17:00 NY) + offset of the end minute
        end_srv = days[starts] * 86400 + ((b - 17 * 60) % 1440) * 60
        t_end = timez.server_to_utc(end_srv)
        t_exp = timez.server_to_utc(days[starts] * 86400 + 86400)  # until the end of this FX day
        for j in range(len(starts)):
            rows.append((1, kind, hi[j], t_end[j], t_exp[j]))
            rows.append((-1, kind, lo[j], t_end[j], t_exp[j]))
    return np.array(rows, dtype=POOL_DTYPE)


def evaluate_pools(pools: np.ndarray, t_open: np.ndarray, h, l, c, spread: float | np.ndarray = 0.0,
                   n_accept: int = 2, n_reclaim: int = 3) -> np.ndarray:
    """First interaction of every pool with the evaluation bars (sorted by t_open)."""
    spread_arr = np.broadcast_to(np.asarray(spread, dtype=float), (len(h),))
    start = np.searchsorted(t_open, pools["t_avail"], side="left")
    stop = np.searchsorted(t_open, pools["t_expire"], side="left")
    rows = []
    for z, (s, e) in enumerate(zip(start, stop)):
        if s >= e:
            continue
        side, px = int(pools["side"][z]), float(pools["px"][z])
        pierce = (h[s:e] + spread_arr[s:e] > px) if side == 1 else (l[s:e] < px)
        if not pierce.any():
            continue
        j = s + int(np.argmax(pierce))
        beyond = (lambda i: c[i] > px) if side == 1 else (lambda i: c[i] < px)
        outcome, k, run = None, j, 0
        for i in range(j, min(len(c), j + n_reclaim + 1)):
            if beyond(i):
                run += 1
                if run >= n_accept:
                    outcome, k = BROKEN, i
                    break
            else:
                outcome, k = SWEPT, i
                break
        if outcome is None:
            continue
        ext = h[j:k + 1].max() if side == 1 else l[j:k + 1].min()
        rows.append((z, side, pools["kind"][z], px, j, k, outcome, ext))
    return np.array(rows, dtype=OUTCOME_DTYPE)


GROUP_DTYPE = np.dtype([("k", "i8"), ("side", "i1"), ("outcome", "i1"), ("kinds", "i4"), ("top_kind", "i1"),
                        ("px", "f8"), ("extreme", "f8"), ("pierce", "i8"), ("n_pools", "i2")])


def group_outcomes(outcomes: np.ndarray) -> np.ndarray:
    """One event per (bar, side, outcome); keeps the most significant pool's level."""
    if not len(outcomes):
        return np.empty(0, GROUP_DTYPE)
    order = np.lexsort((outcomes["outcome"], outcomes["side"], outcomes["k"]))
    o = outcomes[order]
    key = np.stack([o["k"], o["side"], o["outcome"]], axis=1)
    starts = np.flatnonzero(np.r_[True, np.any(key[1:] != key[:-1], axis=1)])
    ends = np.r_[starts[1:], len(o)]
    rows = []
    for a, b in zip(starts, ends):
        g = o[a:b]
        w = np.array([KIND_WEIGHT[int(x)] for x in g["kind"]])
        top = int(np.argmax(w))
        kinds = int(np.bitwise_or.reduce(1 << g["kind"].astype(np.int64)))
        ext = g["extreme"].max() if g["side"][0] == 1 else g["extreme"].min()
        rows.append((g["k"][0], g["side"][0], g["outcome"][0], kinds, g["kind"][top], g["px"][top], ext,
                     g["pierce"].min(), len(g)))
    return np.array(rows, dtype=GROUP_DTYPE)
