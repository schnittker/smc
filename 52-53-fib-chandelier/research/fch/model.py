"""Model FC (strategies no. 52 and 53), as pre-registered in docs/01_Vorregistrierung.md.

FC-FIB    H4: last confirmed swing low L before the last confirmed swing high H with H - L >= 3 ATR14 -> long at the
          first close in [H - 0.618 (H - L), H - 0.5 (H - L)] since H; stop L - 0.25 ATR, target H (limit),
          time exit after 30 bars (chart.engine); mirrored for down impulses
FC-CHAND  D1 server days: close above the max (below the min) of the previous 55 closes -> entry at the next open;
          chandelier stop max(prev, HH since entry - 3 ATR22) (long; short mirrored), set at each close, working
          from the next bar as a stop order; no target, no time exit
"""
from __future__ import annotations

import numpy as np

from chart.engine import DAY, END, ROW_DTYPE, STOP, run_trades
from chart.swings import K, swings
from dbo.model import Costs, holiday, server_days
from hkb.model import atr, swap_frac
from smc.swaps import RateTable

VARIANTS = ("FC-FIB", "FC-CHAND")
FIB_LO, FIB_HI, IMPULSE_ATR, FIB_PAD, FIB_MAX_BARS = 0.5, 0.618, 3.0, 0.25, 30
DON_N, CH_ATR_N, CH_MULT = 55, 22, 3.0
RISK, LEVER_CAP = 0.0025, 10.0


def fib_signals(bars: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """(signal, stop level, minimum distance = 1 ATR, target level) per H4 bar."""
    h, l, c = bars["h"], bars["l"], bars["c"]
    n = len(c)
    a = atr(h, l, c, 14)
    sh, sl = swings(h, l)
    hi_idx, lo_idx = np.flatnonzero(sh), np.flatnonzero(sl)
    sig, stop, tgt = np.zeros(n, np.int8), np.full(n, np.nan), np.full(n, np.nan)
    for i in range(K + 1, n):
        if not np.isfinite(a[i]):
            continue
        hk = hi_idx[hi_idx <= i - K]
        lk = lo_idx[lo_idx <= i - K]
        if not len(hk) or not len(lk):
            continue
        jh, jl = hk[-1], lk[-1]
        hh, ll = h[jh], l[jl]
        rng = hh - ll
        if rng < IMPULSE_ATR * a[i]:
            continue
        if jl < jh:                                            # impulse up
            zlo, zhi = hh - FIB_HI * rng, hh - FIB_LO * rng
            prev = c[jh + 1:i]
            if zlo <= c[i] <= zhi and not ((prev >= zlo) & (prev <= zhi)).any():
                sig[i], stop[i], tgt[i] = 1, ll - FIB_PAD * a[i], hh
        else:                                                  # impulse down
            zlo, zhi = ll + FIB_LO * rng, ll + FIB_HI * rng
            prev = c[jl + 1:i]
            if zlo <= c[i] <= zhi and not ((prev >= zlo) & (prev <= zhi)).any():
                sig[i], stop[i], tgt[i] = -1, hh + FIB_PAD * a[i], ll
    return sig, stop, a, tgt


def run_fib(symbol: str, h4: np.ndarray, cost: Costs, rates: RateTable, cfd, day_from: int, day_to: int) -> np.ndarray:
    bars = h4[h4["ts"] < day_to * DAY]
    sig, stop, a, tgt = fib_signals(bars)
    return run_trades(symbol, bars, 14400, cost, rates, cfd, sig, stop, a, day_from, 0.0, FIB_MAX_BARS,
                      target_lvl=tgt)


def run_chandelier(symbol: str, m5: np.ndarray, cost: Costs, rates: RateTable, cfd, day_from: int,
                   day_to: int) -> np.ndarray:
    d1 = server_days(m5[m5["ts"] < day_to * DAY])
    o, h, l, c, days = d1["o"], d1["h"], d1["l"], d1["c"], d1["day"]
    t_open = m5["t"][d1["a"]]
    n = len(c)
    a = atr(h, l, c, CH_ATR_N)
    rows, i = [], DON_N
    while i < n - 1:
        hi, lo = c[i - DON_N:i].max(), c[i - DON_N:i].min()
        d = 1 if c[i] > hi else (-1 if c[i] < lo else 0)
        k = i + 1
        day_k = int(days[k])
        if d == 0 or not np.isfinite(a[i]) or day_k < day_from or holiday(day_k):
            i += 1
            continue
        p = o[k]
        sp, slip = cost.spread(p), cost.slip(p)
        entry = p + sp + slip if d == 1 else p - slip
        stop = entry - CH_MULT * a[i] if d == 1 else entry + CH_MULT * a[i]
        r = abs(entry - stop)
        ext = h[k] if d == 1 else l[k]
        exit_type, px = END, None
        for j in range(k, n):
            if j > k:                                          # the stop set at the previous close works from bar j on
                if d == 1 and l[j] <= stop:
                    exit_type, px = STOP, min(stop, o[j]) - slip
                    break
                if d == -1 and h[j] + sp >= stop:
                    exit_type, px = STOP, max(stop, o[j] + sp) + slip
                    break
            elif (d == 1 and l[j] <= stop) or (d == -1 and h[j] + sp >= stop):
                exit_type, px = STOP, (stop - slip if d == 1 else stop + slip)
                break
            ext = max(ext, h[j]) if d == 1 else min(ext, l[j])
            if np.isfinite(a[j]):
                stop = max(stop, ext - CH_MULT * a[j]) if d == 1 else min(stop, ext + CH_MULT * a[j])
        if px is None:
            j = n - 1
            px = c[j] - slip if d == 1 else c[j] + sp + slip
        t_exit = int(t_open[j]) if exit_type == STOP else int(t_open[j]) + DAY
        comm = cost.commission(entry)
        move = d * (px - entry) - comm
        trade_cost = sp + 2 * slip + comm
        notional = min(RISK / (r / entry), LEVER_CAP)
        swap = swap_frac(symbol, d, int(t_open[k]), t_exit, rates, cfd)
        rows.append((day_k, int(days[j]), d, exit_type, j - k + 1, r / entry * 1e4, notional,
                     (move + swap * entry) / r, notional * (move / entry + swap) * 1e4,
                     notional * (trade_cost / entry + max(-swap, 0.0)) * 1e4, notional * swap * 1e4,
                     notional * (move + trade_cost) / entry * 1e4))
        i = n if exit_type == END else j + 1
    return np.array(rows, dtype=ROW_DTYPE)
