"""Model K 'H4 channel breakout' (strategies no. 36 and 38), as pre-registered in docs/01_Vorregistrierung.md.

Signals at the close of H4 bar i, execution at the open of bar i+1:
  K-BBSQ  squeeze (a 125-bar low of the band width 4 sigma20 / SMA20 within bars i-5..i-1) and C(i) outside
          SMA20 +- 2 sigma20; exit when C crosses back over SMA20
  K-KELT  C(i) outside EMA20 +- 2 ATR10 on the side of EMA200; exit when C crosses back over EMA20
Fixed stop at entry -+ 2 ATR14(i), checked intrabar on the H4 high / low (a gap fills at the open; stop wins over an
exit signal in the same bar). One position per instrument; a new signal is possible from the bar after the exit.
No new entries on server days 24.12.-01.01. Notional = min(0.25 % / (2 ATR14 / price), 10) x capital. Costs:
spread, commission and slippage per market fill (dbo.model.Costs) and swaps per rollover (Wednesday triple).
"""
from __future__ import annotations

import numpy as np

from dbo.model import Costs, holiday
from smc.strategy_h import SPECS, spec_for
from smc.swaps import MARKUP, RateTable, month_index, rollovers

VARIANTS = ("K-BBSQ", "K-KELT")
RISK, LEVER_CAP, STOP_ATR = 0.0025, 10.0, 2.0
BB_N, BB_K, SQ_LOOK, SQ_RECENT = 20, 2.0, 125, 5
KC_N, KC_ATR, KC_K, TREND_N = 20, 10, 2.0, 200
DAY, H4 = 86400, 14400
STOP, SIGNAL, END = 0, 1, 2

ROW_DTYPE = np.dtype([
    ("entry_day", "i8"), ("exit_day", "i8"), ("dir", "i1"), ("exit_type", "i1"), ("bars", "i4"), ("r_bp", "f8"),
    ("notional", "f8"), ("r_net", "f8"), ("net_bp", "f8"), ("cost_bp", "f8"), ("swap_bp", "f8"), ("gross_bp", "f8"),
])


def sma_std(c: np.ndarray, n: int) -> tuple[np.ndarray, np.ndarray]:
    m, s = np.full(len(c), np.nan), np.full(len(c), np.nan)
    if len(c) >= n:
        w = np.lib.stride_tricks.sliding_window_view(c, n)
        m[n - 1:], s[n - 1:] = w.mean(axis=1), w.std(axis=1)
    return m, s


def ema(x: np.ndarray, n: int) -> np.ndarray:
    out, a = np.empty(len(x)), 2.0 / (n + 1)
    acc = x[0]
    for i, v in enumerate(x):
        acc = v if i == 0 else acc + a * (v - acc)
        out[i] = acc
    out[:n - 1] = np.nan
    return out


def atr(h: np.ndarray, l: np.ndarray, c: np.ndarray, n: int) -> np.ndarray:
    tr = np.r_[h[0] - l[0], np.maximum(h[1:], c[:-1]) - np.minimum(l[1:], c[:-1])]
    out = np.full(len(c), np.nan)
    if len(c) >= n:
        acc = tr[:n].mean()
        out[n - 1] = acc
        for i in range(n, len(c)):
            acc = (acc * (n - 1) + tr[i]) / n
            out[i] = acc
    return out


def signals(variant: str, bars: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Per bar: entry direction (+1 / -1 / 0) and the middle line for the exit; plus ATR14 for the stop."""
    h, l, c = bars["h"], bars["l"], bars["c"]
    n = len(c)
    entry = np.zeros(n, np.int8)
    if variant == "K-BBSQ":
        mid, sd = sma_std(c, BB_N)
        bw = 2 * BB_K * sd / mid
        for i in range(SQ_LOOK + BB_N, n):
            if np.nanmin(bw[i - SQ_RECENT:i]) <= np.nanmin(bw[i - SQ_LOOK:i]):
                if c[i] > mid[i] + BB_K * sd[i]:
                    entry[i] = 1
                elif c[i] < mid[i] - BB_K * sd[i]:
                    entry[i] = -1
    elif variant == "K-KELT":
        mid, trend, a = ema(c, KC_N), ema(c, TREND_N), atr(h, l, c, KC_ATR)
        up, dn = mid + KC_K * a, mid - KC_K * a
        entry[(c > up) & (c > trend)] = 1
        entry[(c < dn) & (c < trend)] = -1
    else:
        raise ValueError(variant)
    return entry, mid, atr(h, l, c, 14)


def swap_frac(symbol: str, d: int, t_entry: int, t_exit: int, rates: RateTable, cfd) -> float:
    """Sum of swaps as a fraction of notional (+ = credit)."""
    r, nights = rollovers(t_entry, t_exit)
    total = 0.0
    for month, k in zip(month_index(r), nights):
        if cfd is not None:
            rate = cfd.swap_rate(d, int(month), rates)
        else:
            rate = d * (rates.rate(symbol[:3], int(month)) - rates.rate(symbol[3:], int(month))) - MARKUP
        total += k * rate
    return total / 365.0


def run_symbol(variant: str, symbol: str, bars: np.ndarray, m5: np.ndarray, cost: Costs, rates: RateTable,
               day_from: int, day_to: int) -> np.ndarray:
    """Trades with an entry bar on server days [day_from, day_to); prices only before day_to."""
    bars = bars[bars["ts"] < day_to * DAY]
    cfd = spec_for(symbol, m5) if symbol in SPECS else None
    entry_sig, mid, atr14 = signals(variant, bars)
    o, h, l, c, t, ts = bars["o"], bars["h"], bars["l"], bars["c"], bars["t"], bars["ts"]
    n, rows, i = len(bars), [], 0
    while i < n - 1:
        d = int(entry_sig[i])
        k = i + 1
        day_k = int(ts[k] // DAY)
        if d == 0 or not np.isfinite(atr14[i]) or day_k < day_from or holiday(day_k):
            i += 1
            continue
        p = o[k]
        spread, slip = cost.spread(p), cost.slip(p)
        entry = o[k] + spread + slip if d == 1 else o[k] - slip
        dist = STOP_ATR * atr14[i]
        stop = entry - dist if d == 1 else entry + dist
        exit_type, j, px = END, n - 1, None
        for j in range(k, n):
            if d == 1 and l[j] <= stop:
                exit_type, px = STOP, min(stop, o[j]) - slip
                break
            if d == -1 and h[j] + spread >= stop:
                exit_type, px = STOP, max(stop, o[j] + spread) + slip
                break
            if j + 1 < n and (c[j] - mid[j]) * d < 0:
                exit_type, px = SIGNAL, (o[j + 1] - slip if d == 1 else o[j + 1] + spread + slip)
                break
        if px is None:
            j = n - 1
            px = c[j] - slip if d == 1 else c[j] + spread + slip
        t_exit = int(t[j + 1]) if exit_type == SIGNAL else (int(t[j]) if exit_type == STOP else int(t[j]) + H4)
        comm = cost.commission(entry)
        move = d * (px - entry) - comm
        trade_cost = spread + 2 * slip + comm
        notional = min(RISK / (dist / entry), LEVER_CAP)
        swap = swap_frac(symbol, d, int(t[k]), t_exit, rates, cfd)
        exit_day = int(ts[j + 1] // DAY) if exit_type == SIGNAL else int(ts[j] // DAY)
        net = notional * (move / entry + swap) * 1e4
        rows.append((day_k, exit_day, d, exit_type, j - k + 1,
                     dist / entry * 1e4, notional, (move + swap * entry) / dist, net,
                     notional * (trade_cost / entry + max(-swap, 0.0)) * 1e4, notional * swap * 1e4,
                     notional * (move + trade_cost) / entry * 1e4))
        i = n if exit_type == END else j + 1      # next possible signal: close of the bar after the exit bar j
    return np.array(rows, dtype=ROW_DTYPE)
