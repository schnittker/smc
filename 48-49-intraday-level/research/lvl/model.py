"""Model LV 'intraday levels' (strategies no. 48 and 49), as pre-registered in docs/01_Vorregistrierung.md.

LV-VA80   value area (70 % of the TPOs of the 30-minute blocks of the previous cash session, step 0.02 % of its
          close); open outside, two consecutive block closes inside (the second ending >= 2 h before the close) ->
          market order at the next block towards the other edge (limit target), stop at the session extreme so far
          (at least 0.1 %), time exit at the session close
LV-PFADE  classic pivots of the previous server day: buy limit S1 / sell limit R1 (OCO), stop S2 / R2, target P
LV-PBRK   buy stop R3 / sell stop S3 (OCO), stop R2 / S2, no target
Pivot orders are active until 1 h before the end of the server day; exit at the close of its last M5 bar. Entry and
stop (or stop and target) in the same M5 bar count as stopped; a target is not checked in the entry bar. Notional =
min(0.25 % / (R / entry), 10) x capital. No trades on days 24.12.-01.01.
"""
from __future__ import annotations

from datetime import date

import numpy as np

from dbo.model import Costs, holiday, server_days
from gap.model import bar_exact, index_days, session

VARIANTS = ("LV-VA80", "LV-PFADE", "LV-PBRK")
VA_IDX = ("SPXUSD", "NSXUSD", "FRXEUR", "UKXGBP")
PIV = ("EURUSD", "GBPUSD", "USDJPY", "AUDUSD", "NZDUSD", "USDCAD", "USDCHF",
       "SPXUSD", "NSXUSD", "FRXEUR", "UKXGBP", "JPXJPY", "HKXHKD", "AUXAUD")
RISK, LEVER_CAP = 0.0025, 10.0
STEP, VA_SHARE, BLOCK, LAST_SIGNAL, MIN_STOP = 0.0002, 0.70, 1800, 7200, 0.001
DAY, ORDER_END = 86400, 23 * 3600
STOP, TARGET, EOD, NONE = 0, 5, 2, 3

ROW_DTYPE = np.dtype([
    ("day", "i8"), ("dir", "i1"), ("exit_type", "i1"), ("r_bp", "f8"), ("notional", "f8"), ("r_net", "f8"),
    ("net_bp", "f8"), ("cost_bp", "f8"), ("gross_bp", "f8"),
])


def value_area(highs: np.ndarray, lows: np.ndarray, step: float) -> tuple[float, float]:
    base = int(np.floor(lows.min() / step))
    lo_i = (np.floor(lows / step).astype(int) - base)
    hi_i = (np.floor(highs / step).astype(int) - base)
    counts = np.zeros(int(hi_i.max()) + 1)
    for a, b in zip(lo_i, hi_i):
        counts[a:b + 1] += 1
    mid = (len(counts) - 1) / 2
    top = np.flatnonzero(counts == counts.max())
    poc = int(top[np.argmin(np.abs(top - mid))])
    lo = hi = poc
    acc, need = counts[poc], VA_SHARE * counts.sum()
    while acc < need:
        up = counts[hi + 1] if hi + 1 < len(counts) else -1
        dn = counts[lo - 1] if lo > 0 else -1
        if up >= dn:
            hi += 1
            acc += up
        else:
            lo -= 1
            acc += dn
    return (base + lo) * step, (base + hi + 1) * step


def simulate(m5, k, end, d, entry, bid_in, stop, target, sp, slip, exit_bid):
    """Bars k .. end-1 after an entry in bar k; the time exit at exit_bid. Returns (exit_type, px, bid_out)."""
    o, h, l = m5["o"], m5["h"], m5["l"]
    for j in range(k, end):
        if d == 1:
            if l[j] <= stop:
                b = stop if j == k else min(stop, o[j])
                return STOP, b - slip, b
            if target is not None and j > k and h[j] >= target:
                b = max(target, o[j])
                return TARGET, b, b
        else:
            if h[j] + sp >= stop:
                px = (stop if j == k else max(stop, o[j] + sp)) + slip
                return STOP, px, px - sp - slip
            if target is not None and j > k and l[j] + sp <= target:
                px = min(target, o[j] + sp)
                return TARGET, px, px - sp
    if d == 1:
        return EOD, exit_bid - slip, exit_bid
    return EOD, exit_bid + sp + slip, exit_bid


def _row(day, d, exit_type, entry, bid_in, px, bid_out, risk, cost: Costs):
    comm = cost.commission(entry)
    move = d * (px - entry) - comm
    gross = d * (bid_out - bid_in)
    notional = min(RISK / (risk / entry), LEVER_CAP)
    return (day, d, exit_type, risk / entry * 1e4, notional, move / risk, notional * move / entry * 1e4,
            notional * (gross - move) / entry * 1e4, notional * gross / entry * 1e4)


def _flat(day):
    return (day, 0, NONE, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0)


def blocks(m5, t5: np.ndarray, t_open: int, t_close: int):
    """(start time, high, low, close) of the 30-minute blocks of a session (blocks without bars are skipped).
    t5 = contiguous copy of m5["t"] (searchsorted on the strided field copies it on every call)."""
    out = []
    for s in range(t_open, t_close, BLOCK):
        a, b = np.searchsorted(t5, [s, min(s + BLOCK, t_close)])
        if b > a:
            out.append((s, m5["h"][a:b].max(), m5["l"][a:b].min(), m5["c"][b - 1]))
    return out


def run_va80(symbol: str, m5: np.ndarray, cost: Costs, first: date, last: date) -> np.ndarray:
    t5 = np.ascontiguousarray(m5["t"])
    rows = []
    for day, prev, early, prev_early in index_days(symbol, m5, first, last):
        if holiday(day):
            continue
        p_open, p_close = session(symbol, prev, prev_early)
        prev_blocks = blocks(m5, t5, p_open, p_close)
        t_open, t_close = session(symbol, day, early)
        a, e = bar_exact(t5, t_open), bar_exact(t5, t_close)
        if len(prev_blocks) < 4 or a < 0 or e < 0:
            continue
        ph = np.array([x[1] for x in prev_blocks])
        pl = np.array([x[2] for x in prev_blocks])
        val, vah = value_area(ph, pl, STEP * prev_blocks[-1][3])
        po = m5["o"][a]
        if val <= po <= vah:
            rows.append(_flat(day))
            continue
        d = -1 if po > vah else 1
        bl = blocks(m5, t5, t_open, t_close)
        sig = None
        for j in range(1, len(bl)):
            if bl[j][0] + BLOCK > t_close - LAST_SIGNAL:
                break
            if val <= bl[j - 1][3] <= vah and val <= bl[j][3] <= vah and bl[j][0] == bl[j - 1][0] + BLOCK:
                sig = bl[j][0] + BLOCK
                break
        k = bar_exact(t5, sig) if sig is not None else -1
        if k < 0:
            rows.append(_flat(day))
            continue
        sp, slip = cost.spread(m5["o"][k]), cost.slip(m5["o"][k])
        if d == 1:
            entry, bid_in = m5["o"][k] + sp + slip, m5["o"][k]
            stop = min(m5["l"][a:k].min(), entry * (1 - MIN_STOP))
            risk, target = entry - stop, vah
        else:
            entry, bid_in = m5["o"][k] - slip, m5["o"][k]
            stop = max(m5["h"][a:k].max(), entry * (1 + MIN_STOP))
            risk, target = stop - entry, val
        if d * (target - entry) <= 0:
            rows.append(_flat(day))
            continue
        ex, px, bid_out = simulate(m5, k, e, d, entry, bid_in, stop, target, sp, slip, m5["o"][e])
        rows.append(_row(day, d, ex, entry, bid_in, px, bid_out, risk, cost))
    return np.array(rows, dtype=ROW_DTYPE)


def pivots(h: float, l: float, c: float) -> dict:
    p = (h + l + c) / 3
    return {"P": p, "R1": 2 * p - l, "S1": 2 * p - h, "R2": p + (h - l), "S2": p - (h - l),
            "R3": h + 2 * (p - l), "S3": l - 2 * (h - p)}


def run_pivots(variant: str, m5: np.ndarray, cost: Costs, day_from: int, day_to: int) -> np.ndarray:
    d1 = server_days(m5)
    o, h, l, c, ts = m5["o"], m5["h"], m5["l"], m5["c"], m5["ts"]
    rows = []
    for i in range(1, len(d1["day"])):
        day = int(d1["day"][i])
        if day < day_from or day >= day_to or holiday(day):
            continue
        lv = pivots(d1["h"][i - 1], d1["l"][i - 1], d1["c"][i - 1])
        a, b = int(d1["a"][i]), int(d1["b"][i])
        e = a + int(np.searchsorted(ts[a:b] % DAY, ORDER_END))
        sp, slip = cost.spread(lv["P"]), cost.slip(lv["P"])
        if variant == "LV-PFADE":
            hit_l = l[a:e] + sp <= lv["S1"]
            hit_s = h[a:e] >= lv["R1"]
        else:
            hit_l = h[a:e] + sp >= lv["R3"]
            hit_s = l[a:e] <= lv["S3"]
        trig = np.flatnonzero(hit_l | hit_s)
        if not len(trig):
            rows.append(_flat(day))
            continue
        k = a + int(trig[0])
        bl, bs = bool(hit_l[k - a]), bool(hit_s[k - a])
        if variant == "LV-PFADE":
            d = 1 if bl and (not bs or abs(o[k] - lv["S1"]) <= abs(o[k] - lv["R1"])) else -1
            if d == 1:
                entry = min(lv["S1"], o[k] + sp)
                bid_in, stop, target = entry - sp, lv["S2"], lv["P"]
                risk = entry - stop
            else:
                entry = max(lv["R1"], o[k])
                bid_in, stop, target = entry, lv["R2"], lv["P"]
                risk = stop - entry
        else:
            d = 1 if bl and (not bs or abs(o[k] - lv["R3"]) <= abs(o[k] - lv["S3"])) else -1
            if d == 1:
                entry = max(lv["R3"], o[k] + sp) + slip
                bid_in, stop, target = entry - sp - slip, lv["R2"], None
                risk = entry - stop
            else:
                entry = min(lv["S3"], o[k]) - slip
                bid_in, stop, target = entry + slip, lv["S2"], None
                risk = stop - entry
        if risk <= 0:
            rows.append(_flat(day))
            continue
        ex, px, bid_out = simulate(m5, k, b, d, entry, bid_in, stop, target, sp, slip, c[b - 1])
        rows.append(_row(day, d, ex, entry, bid_in, px, bid_out, risk, cost))
    return np.array(rows, dtype=ROW_DTYPE)
