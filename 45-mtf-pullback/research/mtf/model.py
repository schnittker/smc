"""Model J 'multi-timeframe pullback' (strategy no. 45), as pre-registered in docs/01_Vorregistrierung.md.

Trend from the last completed D1 server day (close vs EMA50 of D1 closes) and the last completed H4 bar (EMA20 vs
EMA50 of H4 closes); both must agree. Signal at the close of H1 bar i: C(i-1) on the wrong side of EMA20_H1 and C(i)
back on the trend side -> entry at the open of bar i+1. Stop at the 10-bar extreme -+ 0.5 ATR14_H1(i), at least
1 ATR from the entry; target 2 R (limit, no slippage); time exit at the open after 48 bars held. Intrabar on the H1
high / low, the stop wins over the target in the same bar. One position per instrument; a new signal from the bar
after the exit bar; no new entries on server days 24.12.-01.01. Notional = min(0.25 % / (R / entry), 10) x capital.
"""
from __future__ import annotations

import numpy as np

from dbo.model import Costs, holiday, server_days
from hkb.model import atr, ema, swap_frac
from smc.strategy_h import SPECS, spec_for
from smc.swaps import RateTable

VARIANTS = ("J-MTF",)
RISK, LEVER_CAP, R_MULT, MAX_BARS, LOOK, PAD_ATR, MIN_ATR = 0.0025, 10.0, 2.0, 48, 10, 0.5, 1.0
DAY, H1, H4 = 86400, 3600, 14400
STOP, TARGET, TIME, END = 0, 5, 4, 2

ROW_DTYPE = np.dtype([
    ("entry_day", "i8"), ("exit_day", "i8"), ("dir", "i1"), ("exit_type", "i1"), ("bars", "i4"), ("r_bp", "f8"),
    ("notional", "f8"), ("r_net", "f8"), ("net_bp", "f8"), ("cost_bp", "f8"), ("swap_bp", "f8"), ("gross_bp", "f8"),
])


def trend(h1: np.ndarray, h4: np.ndarray, d1: dict) -> np.ndarray:
    """+1 / -1 / 0 per H1 bar from the D1 and H4 bars completed by the close of that H1 bar."""
    close_t = h1["ts"] + H1
    d_up = d1["c"] > ema(d1["c"], 50)
    d_dn = d1["c"] < ema(d1["c"], 50)
    e20, e50 = ema(h4["c"], 20), ema(h4["c"], 50)
    h_up, h_dn = e20 > e50, e20 < e50
    di = np.searchsorted(d1["day"], close_t // DAY, side="left") - 1          # last day ending by close_t
    hi = np.searchsorted(h4["ts"] + H4, close_t, side="right") - 1           # last H4 bar ending by close_t
    ok = (di >= 0) & (hi >= 0)
    di, hi = np.clip(di, 0, None), np.clip(hi, 0, None)
    out = np.zeros(len(h1), np.int8)
    out[ok & d_up[di] & h_up[hi]] = 1
    out[ok & d_dn[di] & h_dn[hi]] = -1
    return out


def signals(h1: np.ndarray, h4: np.ndarray, d1: dict) -> tuple[np.ndarray, np.ndarray]:
    c = h1["c"]
    e20 = ema(c, 20)
    tr = trend(h1, h4, d1)
    sig = np.zeros(len(c), np.int8)
    prev_c, prev_e = np.r_[np.nan, c[:-1]], np.r_[np.nan, e20[:-1]]
    sig[(tr == 1) & (prev_c < prev_e) & (c > e20)] = 1
    sig[(tr == -1) & (prev_c > prev_e) & (c < e20)] = -1
    sig[:LOOK] = 0
    return sig, atr(h1["h"], h1["l"], c, 14)


def run_symbol(symbol: str, h1: np.ndarray, h4: np.ndarray, m5: np.ndarray, cost: Costs, rates: RateTable,
               day_from: int, day_to: int) -> np.ndarray:
    """Trades with an entry bar on server days [day_from, day_to); prices only before day_to."""
    lim = day_to * DAY
    h1, h4, m5c = h1[h1["ts"] < lim], h4[h4["ts"] < lim], m5[m5["ts"] < lim]
    cfd = spec_for(symbol, m5) if symbol in SPECS else None
    sig, a14 = signals(h1, h4, server_days(m5c))
    o, h, l, c, t, ts = h1["o"], h1["h"], h1["l"], h1["c"], h1["t"], h1["ts"]
    n, rows, i = len(h1), [], 0
    while i < n - 1:
        d = int(sig[i])
        k = i + 1
        day_k = int(ts[k] // DAY)
        if d == 0 or not np.isfinite(a14[i]) or day_k < day_from or holiday(day_k):
            i += 1
            continue
        p = o[k]
        sp, slip = cost.spread(p), cost.slip(p)
        if d == 1:
            entry = o[k] + sp + slip
            stop = min(l[i - LOOK + 1:i + 1].min() - PAD_ATR * a14[i], entry - MIN_ATR * a14[i])
            risk = entry - stop
            target = entry + R_MULT * risk
        else:
            entry = o[k] - slip
            stop = max(h[i - LOOK + 1:i + 1].max() + PAD_ATR * a14[i], entry + MIN_ATR * a14[i])
            risk = stop - entry
            target = entry - R_MULT * risk
        exit_type, px = END, None
        for j in range(k, n):
            if d == 1:
                if l[j] <= stop:
                    exit_type, px = STOP, min(stop, o[j]) - slip
                    break
                if h[j] >= target:
                    exit_type, px = TARGET, max(target, o[j])
                    break
            else:
                if h[j] + sp >= stop:
                    exit_type, px = STOP, max(stop, o[j] + sp) + slip
                    break
                if l[j] + sp <= target:
                    exit_type, px = TARGET, min(target, o[j] + sp)
                    break
            if j + 1 < n and j - k + 1 >= MAX_BARS:
                exit_type = TIME
                px = o[j + 1] - slip if d == 1 else o[j + 1] + sp + slip
                break
        if px is None:
            j = n - 1
            px = c[j] - slip if d == 1 else c[j] + sp + slip
        t_exit = int(t[j + 1]) if exit_type == TIME else (int(t[j]) if exit_type in (STOP, TARGET) else int(t[j]) + H1)
        comm = cost.commission(entry)
        move = d * (px - entry) - comm
        exit_cost = 0.0 if exit_type == TARGET else slip
        if d == -1:
            exit_cost += sp
        trade_cost = (sp + slip if d == 1 else slip) + exit_cost + comm
        notional = min(RISK / (risk / entry), LEVER_CAP)
        swap = swap_frac(symbol, d, int(t[k]), t_exit, rates, cfd)
        exit_day = int(ts[j + 1] // DAY) if exit_type == TIME else int(ts[j] // DAY)
        rows.append((day_k, exit_day, d, exit_type, j - k + 1, risk / entry * 1e4, notional,
                     (move + swap * entry) / risk, notional * (move / entry + swap) * 1e4,
                     notional * (trade_cost / entry + max(-swap, 0.0)) * 1e4, notional * swap * 1e4,
                     notional * (move + trade_cost) / entry * 1e4))
        i = n if exit_type == END else j + 1       # next possible signal: close of the bar after the exit bar j
    return np.array(rows, dtype=ROW_DTYPE)
