"""Generic trade engine for bar-close signals: entry at the next open, fixed stop, limit target at r_mult R,
time exit at the open after max_bars held. Intrabar on the bar high / low (long: bid; short: bid + spread); a gap
fills at the open; the stop wins over the target in the same bar, and in the entry bar only the stop is checked.
Notional = min(risk / (R / entry), 10) x capital; costs per market fill (dbo.model.Costs) and swaps per rollover.
"""
from __future__ import annotations

import numpy as np

from dbo.model import Costs, holiday
from hkb.model import swap_frac
from smc.swaps import RateTable

DAY = 86400
STOP, TARGET, TIME, END = 0, 5, 4, 2

ROW_DTYPE = np.dtype([
    ("entry_day", "i8"), ("exit_day", "i8"), ("dir", "i1"), ("exit_type", "i1"), ("bars", "i4"), ("r_bp", "f8"),
    ("notional", "f8"), ("r_net", "f8"), ("net_bp", "f8"), ("cost_bp", "f8"), ("swap_bp", "f8"), ("gross_bp", "f8"),
])


def run_trades(symbol: str, bars: np.ndarray, bar_sec: int, cost: Costs, rates: RateTable, cfd,
               sig: np.ndarray, stop_lvl: np.ndarray, min_dist: np.ndarray, day_from: int, r_mult: float,
               max_bars: int, risk: float = 0.0025, lever_cap: float = 10.0,
               target_lvl: np.ndarray | None = None) -> np.ndarray:
    """sig[i] = +1 / -1 / 0 at the close of bar i; stop_lvl[i] its stop level; min_dist[i] the minimum stop distance
    from the entry. Bars must already be cut at the end of the period. With target_lvl the target is that level
    instead of r_mult R (no trade if it is not beyond the entry)."""
    o, h, l, c, t, ts = bars["o"], bars["h"], bars["l"], bars["c"], bars["t"], bars["ts"]
    n, rows, i = len(bars), [], 0
    while i < n - 1:
        d = int(sig[i])
        k = i + 1
        day_k = int(ts[k] // DAY)
        if d == 0 or not np.isfinite(stop_lvl[i]) or not np.isfinite(min_dist[i]) or day_k < day_from \
                or holiday(day_k):
            i += 1
            continue
        p = o[k]
        sp, slip = cost.spread(p), cost.slip(p)
        if d == 1:
            entry = p + sp + slip
            stop = min(stop_lvl[i], entry - min_dist[i])
            r = entry - stop
            target = entry + r_mult * r if target_lvl is None else target_lvl[i]
        else:
            entry = p - slip
            stop = max(stop_lvl[i], entry + min_dist[i])
            r = stop - entry
            target = entry - r_mult * r if target_lvl is None else target_lvl[i]
        if (target - entry) * d <= 0:
            i += 1
            continue
        exit_type, px = END, None
        for j in range(k, n):
            if d == 1:
                if l[j] <= stop:
                    exit_type, px = STOP, min(stop, o[j]) - slip
                    break
                if j > k and h[j] >= target:
                    exit_type, px = TARGET, max(target, o[j])
                    break
            else:
                if h[j] + sp >= stop:
                    exit_type, px = STOP, max(stop, o[j] + sp) + slip
                    break
                if j > k and l[j] + sp <= target:
                    exit_type, px = TARGET, min(target, o[j] + sp)
                    break
            if j + 1 < n and j - k + 1 >= max_bars:
                exit_type = TIME
                px = o[j + 1] - slip if d == 1 else o[j + 1] + sp + slip
                break
        if px is None:
            j = n - 1
            px = c[j] - slip if d == 1 else c[j] + sp + slip
        t_exit = int(t[j + 1]) if exit_type == TIME else (int(t[j]) if exit_type in (STOP, TARGET) else int(t[j]) + bar_sec)
        comm = cost.commission(entry)
        move = d * (px - entry) - comm
        exit_cost = (0.0 if exit_type == TARGET else slip) + (sp if d == -1 else 0.0)
        trade_cost = (sp + slip if d == 1 else slip) + exit_cost + comm
        notional = min(risk / (r / entry), lever_cap)
        swap = swap_frac(symbol, d, int(t[k]), t_exit, rates, cfd)
        exit_day = int(ts[j + 1] // DAY) if exit_type == TIME else int(ts[j] // DAY)
        rows.append((day_k, exit_day, d, exit_type, j - k + 1, r / entry * 1e4, notional,
                     (move + swap * entry) / r, notional * (move / entry + swap) * 1e4,
                     notional * (trade_cost / entry + max(-swap, 0.0)) * 1e4, notional * swap * 1e4,
                     notional * (move + trade_cost) / entry * 1e4))
        i = n if exit_type == END else j + 1       # next possible signal: close of the bar after the exit bar j
    return np.array(rows, dtype=ROW_DTYPE)
