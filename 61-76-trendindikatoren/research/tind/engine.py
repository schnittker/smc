"""Stop-and-reverse engine of model TI: on a state change at the close of bar j the open position is closed and,
for a non-zero new state, a position in that direction opened at the open of bar j+1. Fixed emergency stop
3 ATR14(j) intrabar (long: bid; short: bid + spread; gap fills at the open); after a stop the next entry waits for
the next state change. Notional = min(0.25 % / (3 ATR14 / price), 10) x capital; costs per market fill and swaps.
"""
from __future__ import annotations

import numpy as np

from chart.engine import ROW_DTYPE, STOP, END
from dbo.model import Costs, holiday
from hkb.model import atr, swap_frac
from smc.swaps import RateTable

DAY = 86400
SIGNAL = 1
RISK, LEVER_CAP, STOP_ATR = 0.0025, 10.0, 3.0


def run_state(symbol: str, bars: np.ndarray, bar_sec: int, cost: Costs, rates: RateTable, cfd, st: np.ndarray,
              day_from: int) -> np.ndarray:
    o, h, l, c, t, ts = bars["o"], bars["h"], bars["l"], bars["c"], bars["t"], bars["ts"]
    n = len(bars)
    a14 = atr(h, l, c, 14)
    rows = []
    pos = None                                     # (dir, k, entry, stop, dist, sp, slip)

    def close(j_last, px, exit_type, t_exit, exit_day):
        d, k, entry, stop, dist, sp, slip = pos
        comm = cost.commission(entry)
        move = d * (px - entry) - comm
        trade_cost = sp + 2 * slip + comm
        notional = min(RISK / (dist / entry), LEVER_CAP)
        swap = swap_frac(symbol, d, int(t[k]), t_exit, rates, cfd)
        rows.append((int(ts[k] // DAY), exit_day, d, exit_type, j_last - k + 1, dist / entry * 1e4, notional,
                     (move + swap * entry) / dist, notional * (move / entry + swap) * 1e4,
                     notional * (trade_cost / entry + max(-swap, 0.0)) * 1e4, notional * swap * 1e4,
                     notional * (move + trade_cost) / entry * 1e4))

    for j in range(1, n):
        if pos is not None and pos[1] <= j:
            d, _, _, stop, _, sp, slip = pos
            if d == 1 and l[j] <= stop:
                close(j, min(stop, o[j]) - slip, STOP, int(t[j]), int(ts[j] // DAY))
                pos = None
            elif d == -1 and h[j] + sp >= stop:
                close(j, max(stop, o[j] + sp) + slip, STOP, int(t[j]), int(ts[j] // DAY))
                pos = None
        if j + 1 >= n or st[j] == st[j - 1]:
            continue
        k = j + 1
        if pos is not None:
            d, _, _, _, _, sp, slip = pos
            close(j, o[k] - slip if d == 1 else o[k] + sp + slip, SIGNAL, int(t[k]), int(ts[k] // DAY))
            pos = None
        d = int(st[j])
        day_k = int(ts[k] // DAY)
        if d == 0 or not np.isfinite(a14[j]) or day_k < day_from or holiday(day_k):
            continue
        p = o[k]
        sp, slip = cost.spread(p), cost.slip(p)
        entry = p + sp + slip if d == 1 else p - slip
        dist = STOP_ATR * a14[j]
        pos = (d, k, entry, entry - dist if d == 1 else entry + dist, dist, sp, slip)
    if pos is not None:
        d, _, _, _, _, sp, slip = pos
        close(n - 1, c[-1] - slip if d == 1 else c[-1] + sp + slip, END, int(t[-1]) + bar_sec, int(ts[-1] // DAY))
    return np.array(rows, dtype=ROW_DTYPE)
