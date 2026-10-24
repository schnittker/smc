"""Model W 'Hurst regime switch' (strategy no. 40), as pre-registered in docs/01_Vorregistrierung.md.

H(i) from the aggregated variance of overlapping k-bar log returns (k = 1, 2, 4, 8, 16) over the last 500 H4 closes:
H = slope(ln Var_k on ln k) / 2. Signal at the close of bar i, execution at the open of bar i+1:
  trend regime    H > 0.55: C outside EMA20 +- 2 ATR10 -> with the break; exit when C crosses back over EMA20
  reversal regime H < 0.45: C outside SMA20 +- 2 sigma20 -> fade; exit when C reaches SMA20 or after 12 bars held
Fixed stop at entry -+ 2 ATR14(i) checked intrabar (gap fills at the open; the stop wins). One position per
instrument; a new signal is possible from the bar after the exit bar; no new entries on server days 24.12.-01.01.
Notional = min(0.25 % / (2 ATR14 / price), 10) x capital. W-TREND and W-MR are the unfiltered rules (descriptive).
"""
from __future__ import annotations

import numpy as np

from dbo.model import Costs, holiday
from hkb.model import atr, ema, sma_std, swap_frac
from smc.strategy_h import SPECS, spec_for
from smc.swaps import RateTable

VARIANTS = ("W-HURST",)
DESCRIPTIVE = ("W-TREND", "W-MR")
RISK, LEVER_CAP, STOP_ATR, MR_MAX_BARS = 0.0025, 10.0, 2.0, 12
H_N, H_KS, H_TREND, H_MR = 500, (1, 2, 4, 8, 16), 0.55, 0.45
DAY, H4 = 86400, 14400
STOP, SIGNAL, END, TIME = 0, 1, 2, 4
TREND, MR = 1, -1

ROW_DTYPE = np.dtype([
    ("entry_day", "i8"), ("exit_day", "i8"), ("dir", "i1"), ("mode", "i1"), ("exit_type", "i1"), ("bars", "i4"),
    ("r_bp", "f8"), ("notional", "f8"), ("r_net", "f8"), ("net_bp", "f8"), ("cost_bp", "f8"), ("swap_bp", "f8"),
    ("gross_bp", "f8"),
])


def hurst(c: np.ndarray, w: int = H_N, ks=H_KS) -> np.ndarray:
    """Aggregated-variance Hurst exponent of the last w closes (NaN before w closes exist)."""
    lp = np.log(c)
    n = len(c)
    out = np.full(n, np.nan)
    if n < w:
        return out
    logv = []
    for k in ks:
        r = lp[k:] - lp[:-k]                      # r[t - k] = return ending at t
        m = w - k                                 # returns ending at t = i-w+1+k .. i
        cs, cs2 = np.r_[0.0, np.cumsum(r)], np.r_[0.0, np.cumsum(r * r)]
        s, s2 = cs[m:] - cs[:-m], cs2[m:] - cs2[:-m]
        var = (s2 - s * s / m) / (m - 1)          # window ending at return index q -> close index q + k
        v = np.full(n, np.nan)
        v[m - 1 + k:] = var
        logv.append(np.log(v))
    x = np.log(np.array(ks, float))
    xc = x - x.mean()
    y = np.array(logv)
    out = (xc[:, None] * (y - y.mean(axis=0))).sum(axis=0) / (xc ** 2).sum() / 2
    out[:w - 1] = np.nan
    return out


def signals(variant: str, bars: np.ndarray) -> dict:
    h, l, c = bars["h"], bars["l"], bars["c"]
    n = len(c)
    ema20, a10 = ema(c, 20), atr(h, l, c, 10)
    sma20, sd20 = sma_std(c, 20)
    trend = np.zeros(n, np.int8)
    trend[c > ema20 + 2 * a10] = 1
    trend[c < ema20 - 2 * a10] = -1
    mr = np.zeros(n, np.int8)
    mr[c < sma20 - 2 * sd20] = 1
    mr[c > sma20 + 2 * sd20] = -1
    H = hurst(c)
    if variant == "W-HURST":
        use_t, use_m = H > H_TREND, H < H_MR
    elif variant == "W-TREND":
        use_t, use_m = np.ones(n, bool), np.zeros(n, bool)
    elif variant == "W-MR":
        use_t, use_m = np.zeros(n, bool), np.ones(n, bool)
    else:
        raise ValueError(variant)
    entry = np.where(use_t, trend, np.where(use_m, mr, 0)).astype(np.int8)
    mode = np.where(use_t, TREND, MR).astype(np.int8)
    return {"entry": entry, "mode": mode, "ema20": ema20, "sma20": sma20, "atr14": atr(h, l, c, 14), "H": H}


def run_symbol(variant: str, symbol: str, bars: np.ndarray, m5, cost: Costs, rates: RateTable,
               day_from: int, day_to: int) -> np.ndarray:
    """Trades with an entry bar on server days [day_from, day_to); prices only before day_to."""
    bars = bars[bars["ts"] < day_to * DAY]
    cfd = spec_for(symbol, m5) if symbol in SPECS else None
    sg = signals(variant, bars)
    entry_sig, mode_arr, atr14 = sg["entry"], sg["mode"], sg["atr14"]
    o, h, l, c, t, ts = bars["o"], bars["h"], bars["l"], bars["c"], bars["t"], bars["ts"]
    n, rows, i = len(bars), [], 0
    while i < n - 1:
        d, mode = int(entry_sig[i]), int(mode_arr[i])
        k = i + 1
        day_k = int(ts[k] // DAY)
        if d == 0 or not np.isfinite(atr14[i]) or day_k < day_from or holiday(day_k):
            i += 1
            continue
        mid = sg["ema20"] if mode == TREND else sg["sma20"]
        p = o[k]
        spread, slip = cost.spread(p), cost.slip(p)
        entry = o[k] + spread + slip if d == 1 else o[k] - slip
        dist = STOP_ATR * atr14[i]
        stop = entry - dist if d == 1 else entry + dist
        exit_type, px = END, None
        for j in range(k, n):
            if d == 1 and l[j] <= stop:
                exit_type, px = STOP, min(stop, o[j]) - slip
                break
            if d == -1 and h[j] + spread >= stop:
                exit_type, px = STOP, max(stop, o[j] + spread) + slip
                break
            if j + 1 < n:
                if mode == TREND and (c[j] - mid[j]) * d < 0:
                    exit_type = SIGNAL
                elif mode == MR and (c[j] - mid[j]) * d >= 0:
                    exit_type = SIGNAL
                elif mode == MR and j - k + 1 >= MR_MAX_BARS:
                    exit_type = TIME
                if exit_type != END:
                    px = o[j + 1] - slip if d == 1 else o[j + 1] + spread + slip
                    break
        if px is None:
            j = n - 1
            px = c[j] - slip if d == 1 else c[j] + spread + slip
        at_open = exit_type in (SIGNAL, TIME)
        t_exit = int(t[j + 1]) if at_open else (int(t[j]) if exit_type == STOP else int(t[j]) + H4)
        comm = cost.commission(entry)
        move = d * (px - entry) - comm
        trade_cost = spread + 2 * slip + comm
        notional = min(RISK / (dist / entry), LEVER_CAP)
        swap = swap_frac(symbol, d, int(t[k]), t_exit, rates, cfd)
        exit_day = int(ts[j + 1] // DAY) if at_open else int(ts[j] // DAY)
        rows.append((day_k, exit_day, d, mode, exit_type, j - k + 1, dist / entry * 1e4, notional,
                     (move + swap * entry) / dist, notional * (move / entry + swap) * 1e4,
                     notional * (trade_cost / entry + max(-swap, 0.0)) * 1e4, notional * swap * 1e4,
                     notional * (move + trade_cost) / entry * 1e4))
        i = n if exit_type == END else j + 1       # next possible signal: close of the bar after the exit bar j
    return np.array(rows, dtype=ROW_DTYPE)
