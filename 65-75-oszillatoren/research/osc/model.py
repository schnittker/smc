"""Model OS 'oscillators, divergences, Renko' (strategies no. 65-68, 74 and 75), as pre-registered in
docs/01_Vorregistrierung.md."""
from __future__ import annotations

import numpy as np

from chart.engine import END, ROW_DTYPE, STOP
from chart.swings import K, swings
from dbo.model import Costs, holiday
from hkb.model import atr, swap_frac
from smc.swaps import RateTable
from tind.indicators import sma

VARIANTS = {"OS-RSI": "H1", "OS-STOCH": "H1", "OS-WPR": "H1", "OS-CCI": "H4", "OS-RENKO": "H1", "OS-DIV": "H4"}
LIST_NO = {"OS-RSI": 65, "OS-STOCH": 66, "OS-WPR": 67, "OS-CCI": 68, "OS-RENKO": 74, "OS-DIV": 75}
MAX_BARS = {"OS-RSI": 48, "OS-STOCH": 48, "OS-WPR": 48, "OS-CCI": 30}
DAY = 86400
SIGNAL, TIME = 1, 4
RISK, LEVER_CAP, STOP_ATR = 0.0025, 10.0, 2.0


def rsi(c: np.ndarray, n: int = 14) -> np.ndarray:
    d = np.diff(c)
    up, dn = np.maximum(d, 0.0), np.maximum(-d, 0.0)
    out = np.full(len(c), np.nan)
    if len(c) <= n:
        return out
    au, ad = up[:n].mean(), dn[:n].mean()
    for i in range(n, len(c)):
        if i > n:
            au = (au * (n - 1) + up[i - 1]) / n
            ad = (ad * (n - 1) + dn[i - 1]) / n
        out[i] = 100.0 if ad == 0 else 100 - 100 / (1 + au / ad)
    return out


def _hh_ll(h, l, n):
    hh, ll = np.full(len(h), np.nan), np.full(len(h), np.nan)
    if len(h) >= n:
        hh[n - 1:] = np.lib.stride_tricks.sliding_window_view(h, n).max(axis=1)
        ll[n - 1:] = np.lib.stride_tricks.sliding_window_view(l, n).min(axis=1)
    return hh, ll


def stoch(h, l, c, n=14, k_s=3, d_s=3):
    hh, ll = _hh_ll(h, l, n)
    with np.errstate(invalid="ignore", divide="ignore"):
        fast = 100 * (c - ll) / (hh - ll)
    k = np.full(len(c), np.nan)
    ok = np.flatnonzero(np.isfinite(fast))
    if len(ok) >= k_s:
        k[ok] = sma(fast[ok], k_s)
    d = np.full(len(c), np.nan)
    ok = np.flatnonzero(np.isfinite(k))
    if len(ok) >= d_s:
        d[ok] = sma(k[ok], d_s)
    return k, d


def wpr(h, l, c, n=14):
    hh, ll = _hh_ll(h, l, n)
    with np.errstate(invalid="ignore", divide="ignore"):
        return -100 * (hh - c) / (hh - ll)


def cci(h, l, c, n=20):
    tp = (h + l + c) / 3
    out = np.full(len(c), np.nan)
    if len(c) >= n:
        w = np.lib.stride_tricks.sliding_window_view(tp, n)
        m = w.mean(axis=1)
        md = np.abs(w - m[:, None]).mean(axis=1)
        with np.errstate(invalid="ignore", divide="ignore"):
            out[n - 1:] = (tp[n - 1:] - m) / (0.015 * md)
    return out


def flag_signals(variant: str, bars) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """(entry signal, exit flag for longs, exit flag for shorts) per bar."""
    h, l, c = bars["h"], bars["l"], bars["c"]
    n = len(c)
    sig = np.zeros(n, np.int8)
    prev = lambda x: np.r_[np.nan, x[:-1]]
    if variant == "OS-RSI":
        x = rsi(c)
        sig[(prev(x) < 30) & (x >= 30)] = 1
        sig[(prev(x) > 70) & (x <= 70)] = -1
        return sig, x >= 50, x <= 50
    if variant == "OS-STOCH":
        k, d = stoch(h, l, c)
        up = (prev(k) <= prev(d)) & (k > d)
        dn = (prev(k) >= prev(d)) & (k < d)
        sig[up & (k < 20) & (d < 20)] = 1
        sig[dn & (k > 80) & (d > 80)] = -1
        return sig, k >= 50, k <= 50
    if variant == "OS-WPR":
        x = wpr(h, l, c)
        sig[(prev(x) < -80) & (x >= -80)] = 1
        sig[(prev(x) > -20) & (x <= -20)] = -1
        return sig, x >= -50, x <= -50
    if variant == "OS-CCI":
        x = cci(h, l, c)
        sig[(prev(x) <= 100) & (x > 100)] = 1
        sig[(prev(x) >= -100) & (x < -100)] = -1
        return sig, x < 0, x > 0
    raise ValueError(variant)


def run_flags(symbol: str, bars: np.ndarray, bar_sec: int, cost: Costs, rates: RateTable, cfd, sig, exit_l, exit_s,
              max_bars: int, day_from: int, stop_atr: float = STOP_ATR, allow=None) -> np.ndarray:
    """Entry at the next open, fixed stop stop_atr x ATR14 (intrabar, wins), exit at the next open after a bar whose
    exit flag (for the direction) is set or after max_bars held. allow[k]: entry allowed in bar k (default: all)."""
    o, h, l, c, t, ts = bars["o"], bars["h"], bars["l"], bars["c"], bars["t"], bars["ts"]
    n = len(bars)
    a14 = atr(h, l, c, 14)
    rows, i = [], 0
    while i < n - 1:
        d = int(sig[i])
        k = i + 1
        day_k = int(ts[k] // DAY)
        if d == 0 or not np.isfinite(a14[i]) or day_k < day_from or holiday(day_k) or \
                (allow is not None and not allow[k]):
            i += 1
            continue
        p = o[k]
        sp, slip = cost.spread(p), cost.slip(p)
        entry = p + sp + slip if d == 1 else p - slip
        dist = stop_atr * a14[i]
        stop = entry - dist if d == 1 else entry + dist
        flags = exit_l if d == 1 else exit_s
        exit_type, px = END, None
        for j in range(k, n):
            if d == 1 and l[j] <= stop:
                exit_type, px = STOP, min(stop, o[j]) - slip
                break
            if d == -1 and h[j] + sp >= stop:
                exit_type, px = STOP, max(stop, o[j] + sp) + slip
                break
            if j + 1 < n and (bool(flags[j]) or j - k + 1 >= max_bars):
                exit_type = SIGNAL if flags[j] else TIME
                px = o[j + 1] - slip if d == 1 else o[j + 1] + sp + slip
                break
        if px is None:
            j = n - 1
            px = c[j] - slip if d == 1 else c[j] + sp + slip
        at_open = exit_type in (SIGNAL, TIME)
        t_exit = int(t[j + 1]) if at_open else (int(t[j]) if exit_type == STOP else int(t[j]) + bar_sec)
        comm = cost.commission(entry)
        move = d * (px - entry) - comm
        trade_cost = sp + 2 * slip + comm
        notional = min(RISK / (dist / entry), LEVER_CAP)
        swap = swap_frac(symbol, d, int(t[k]), t_exit, rates, cfd)
        exit_day = int(ts[j + 1] // DAY) if at_open else int(ts[j] // DAY)
        rows.append((day_k, exit_day, d, exit_type, j - k + 1, dist / entry * 1e4, notional,
                     (move + swap * entry) / dist, notional * (move / entry + swap) * 1e4,
                     notional * (trade_cost / entry + max(-swap, 0.0)) * 1e4, notional * swap * 1e4,
                     notional * (move + trade_cost) / entry * 1e4))
        i = n if exit_type == END else j + 1
    return np.array(rows, dtype=ROW_DTYPE)


def divergence_signals(bars) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """OS-DIV: (signal, stop level, minimum distance = 1 ATR) per H4 bar."""
    h, l, c = bars["h"], bars["l"], bars["c"]
    n = len(c)
    a, r = atr(h, l, c, 14), rsi(c)
    sh, sl = swings(h, l)
    hi_idx, lo_idx = np.flatnonzero(sh), np.flatnonzero(sl)
    sig, stop = np.zeros(n, np.int8), np.full(n, np.nan)
    for i in range(K + 1, n):
        if not np.isfinite(a[i]):
            continue
        j2 = i - K
        if sl[j2]:
            prior = lo_idx[lo_idx < j2]
            if len(prior):
                j1 = prior[-1]
                if 5 <= j2 - j1 <= 60 and l[j2] < l[j1] and r[j2] > r[j1] and r[j1] < 30:
                    sig[i], stop[i] = 1, l[j2] - 0.25 * a[i]
        if sh[j2]:
            prior = hi_idx[hi_idx < j2]
            if len(prior):
                j1 = prior[-1]
                if 5 <= j2 - j1 <= 60 and h[j2] > h[j1] and r[j2] < r[j1] and r[j1] > 70:
                    if sig[i] == 1:
                        sig[i], stop[i] = 0, np.nan
                    else:
                        sig[i], stop[i] = -1, h[j2] + 0.25 * a[i]
    return sig, stop, a


def renko_state(c: np.ndarray, a: np.ndarray, mult: float = 2.0) -> np.ndarray:
    """Direction of the last Renko brick on closes (brick = mult x ATR at the last brick; reversal needs 2 bricks)."""
    out = np.zeros(len(c), np.int8)
    ref, d, size = np.nan, 0, np.nan
    for i in range(len(c)):
        if not np.isfinite(a[i]):
            continue
        if np.isnan(ref):
            ref, size = c[i], mult * a[i]
            continue
        if d >= 0 and c[i] >= ref + size:
            k = int((c[i] - ref) // size)
            ref, d, size = ref + k * size, 1, mult * a[i]
        elif d <= 0 and c[i] <= ref - size:
            k = int((ref - c[i]) // size)
            ref, d, size = ref - k * size, -1, mult * a[i]
        elif d == 1 and c[i] <= ref - 2 * size:
            k = int((ref - c[i]) // size) - 1
            ref, d, size = ref - (k + 1) * size, -1, mult * a[i]
        elif d == -1 and c[i] >= ref + 2 * size:
            k = int((c[i] - ref) // size) - 1
            ref, d, size = ref + (k + 1) * size, 1, mult * a[i]
        out[i] = d
    return out
