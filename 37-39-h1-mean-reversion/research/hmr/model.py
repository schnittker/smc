"""Model U 'H1 mean reversion' (strategies no. 37 and 39), as pre-registered in docs/01_Vorregistrierung.md.

Signals at the close of H1 bar i, execution at the open of bar i+1:
  U-BB  ADX14 < 20 and C(i) outside SMA20 +- 2 sigma20 -> fade; middle line SMA20
  U-OU  OU half-life (OLS of dC on C(t-1) over 500 bars) <= 24 h and |z| > 2, z = (C - SMA100) / sigma100 -> fade;
        middle line SMA100
Exit at the next open once the close reaches the middle line, or after 48 bars held; fixed stop at entry -+ 2 ATR14(i)
checked intrabar (gap fills at the open; the stop wins over an exit signal in the same bar). One position per pair; a
new signal is possible from the bar after the exit bar. No new entries on server days 24.12.-01.01. Notional =
min(0.25 % / (2 ATR14 / price), 10) x capital. FX costs per market fill and swaps per rollover.
"""
from __future__ import annotations

import numpy as np

from dbo.model import Costs, holiday
from hkb.model import atr, sma_std, swap_frac
from smc.swaps import RateTable

VARIANTS = ("U-BB", "U-OU")
CROSSES = ("EURJPY", "GBPJPY", "AUDJPY", "NZDJPY", "CADJPY", "CHFJPY", "EURCAD", "EURCHF", "EURNZD", "EURAUD",
           "GBPCHF", "GBPNZD", "GBPCAD", "GBPAUD", "AUDNZD", "AUDCAD", "CADCHF")
RISK, LEVER_CAP, STOP_ATR, MAX_BARS = 0.0025, 10.0, 2.0, 48
BB_N, BB_K, ADX_N, ADX_MAX = 20, 2.0, 14, 20.0
Z_N, Z_K, HL_N, HL_MAX = 100, 2.0, 500, 24.0
DAY, H1 = 86400, 3600
STOP, SIGNAL, TIME, END = 0, 1, 4, 2

ROW_DTYPE = np.dtype([
    ("entry_day", "i8"), ("exit_day", "i8"), ("dir", "i1"), ("exit_type", "i1"), ("bars", "i4"), ("r_bp", "f8"),
    ("notional", "f8"), ("r_net", "f8"), ("net_bp", "f8"), ("cost_bp", "f8"), ("swap_bp", "f8"), ("gross_bp", "f8"),
])


def _wilder_sum(x: np.ndarray, n: int, start: int) -> np.ndarray:
    """Wilder's running sum: first value = sum of x[start:start+n], then S - S/n + x."""
    out = np.full(len(x), np.nan)
    if len(x) < start + n:
        return out
    acc = x[start:start + n].sum()
    out[start + n - 1] = acc
    for i in range(start + n, len(x)):
        acc = acc - acc / n + x[i]
        out[i] = acc
    return out


def adx(h: np.ndarray, l: np.ndarray, c: np.ndarray, n: int = ADX_N) -> np.ndarray:
    up, dn = np.r_[0.0, np.diff(h)], np.r_[0.0, -np.diff(l)]
    pdm = np.where((up > dn) & (up > 0), up, 0.0)
    mdm = np.where((dn > up) & (dn > 0), dn, 0.0)
    tr = np.r_[h[0] - l[0], np.maximum(h[1:], c[:-1]) - np.minimum(l[1:], c[:-1])]
    s_tr, s_p, s_m = (_wilder_sum(x, n, 1) for x in (tr, pdm, mdm))
    with np.errstate(invalid="ignore", divide="ignore"):
        pdi, mdi = 100 * s_p / s_tr, 100 * s_m / s_tr
        dx = 100 * np.abs(pdi - mdi) / (pdi + mdi)
    out = np.full(len(c), np.nan)
    first = n                                       # first DX index
    if len(c) >= first + n:
        acc = np.nanmean(dx[first:first + n])
        out[first + n - 1] = acc
        for i in range(first + n, len(c)):
            acc = (acc * (n - 1) + (dx[i] if np.isfinite(dx[i]) else acc)) / n
            out[i] = acc
    return out


def half_life(c: np.ndarray, w: int = HL_N) -> np.ndarray:
    """OU half-life in bars from the OLS slope of dC(t) on C(t-1) over t = i-w+1 .. i (inf if the slope >= 0)."""
    x, y = c[:-1], np.diff(c)
    cs = [np.r_[0.0, np.cumsum(v)] for v in (x, y, x * x, x * y)]
    out = np.full(len(c), np.nan)
    if len(x) < w:
        return out
    sx, sy, sxx, sxy = ((s[w:] - s[:-w]) for s in cs)
    beta = (w * sxy - sx * sy) / (w * sxx - sx * sx)
    with np.errstate(invalid="ignore", divide="ignore"):
        hl = np.where((beta < 0) & (beta > -1), -np.log(2) / np.log1p(beta), np.inf)
    out[w:] = hl                                    # pairs t-1,t with t = i-w+1 .. i  ->  i = w .. len(c)-1
    return out


def signals(variant: str, bars: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Per bar: fade direction (+1 / -1 / 0), middle line, ATR14."""
    h, l, c = bars["h"], bars["l"], bars["c"]
    entry = np.zeros(len(c), np.int8)
    if variant == "U-BB":
        mid, sd = sma_std(c, BB_N)
        a = adx(h, l, c)
        calm = a < ADX_MAX
        entry[calm & (c < mid - BB_K * sd)] = 1
        entry[calm & (c > mid + BB_K * sd)] = -1
    elif variant == "U-OU":
        mid, sd = sma_std(c, Z_N)
        with np.errstate(invalid="ignore", divide="ignore"):
            z = (c - mid) / sd
        ok = half_life(c) <= HL_MAX
        entry[ok & (z < -Z_K)] = 1
        entry[ok & (z > Z_K)] = -1
    else:
        raise ValueError(variant)
    return entry, mid, atr(h, l, c, 14)


def run_symbol(variant: str, symbol: str, bars: np.ndarray, cost: Costs, rates: RateTable,
               day_from: int, day_to: int) -> np.ndarray:
    """Trades with an entry bar on server days [day_from, day_to); prices only before day_to."""
    bars = bars[bars["ts"] < day_to * DAY]
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
        exit_type, px = END, None
        for j in range(k, n):
            if d == 1 and l[j] <= stop:
                exit_type, px = STOP, min(stop, o[j]) - slip
                break
            if d == -1 and h[j] + spread >= stop:
                exit_type, px = STOP, max(stop, o[j] + spread) + slip
                break
            if j + 1 < n and ((c[j] - mid[j]) * d >= 0 or j - k + 1 >= MAX_BARS):
                exit_type = SIGNAL if (c[j] - mid[j]) * d >= 0 else TIME
                px = o[j + 1] - slip if d == 1 else o[j + 1] + spread + slip
                break
        if px is None:
            j = n - 1
            px = c[j] - slip if d == 1 else c[j] + spread + slip
        at_open = exit_type in (SIGNAL, TIME)
        t_exit = int(t[j + 1]) if at_open else (int(t[j]) if exit_type == STOP else int(t[j]) + H1)
        comm = cost.commission(entry)
        move = d * (px - entry) - comm
        trade_cost = spread + 2 * slip + comm
        notional = min(RISK / (dist / entry), LEVER_CAP)
        swap = swap_frac(symbol, d, int(t[k]), t_exit, rates, None)
        exit_day = int(ts[j + 1] // DAY) if at_open else int(ts[j] // DAY)
        rows.append((day_k, exit_day, d, exit_type, j - k + 1, dist / entry * 1e4, notional,
                     (move + swap * entry) / dist, notional * (move / entry + swap) * 1e4,
                     notional * (trade_cost / entry + max(-swap, 0.0)) * 1e4, notional * swap * 1e4,
                     notional * (move + trade_cost) / entry * 1e4))
        i = n if exit_type == END else j + 1       # next possible signal: close of the bar after the exit bar j
    return np.array(rows, dtype=ROW_DTYPE)
