"""Indicator states (+1 long, -1 short, 0 flat) of model TI, as pre-registered in docs/01_Vorregistrierung.md."""
from __future__ import annotations

import numpy as np

from hkb.model import atr, ema


def sma(x: np.ndarray, n: int) -> np.ndarray:
    out = np.full(len(x), np.nan)
    if len(x) >= n:
        cs = np.r_[0.0, np.cumsum(x)]
        out[n - 1:] = (cs[n:] - cs[:-n]) / n
    return out


def _sign_state(diff: np.ndarray) -> np.ndarray:
    out = np.zeros(len(diff), np.int8)
    out[diff > 0] = 1
    out[diff < 0] = -1
    return out


def _wilder_sum(x: np.ndarray, n: int, start: int) -> np.ndarray:
    out = np.full(len(x), np.nan)
    if len(x) < start + n:
        return out
    acc = x[start:start + n].sum()
    out[start + n - 1] = acc
    for i in range(start + n, len(x)):
        acc = acc - acc / n + x[i]
        out[i] = acc
    return out


def dmi(h, l, c, n: int = 14) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """ADX, +DI, -DI after Wilder (as hmr.model.adx in no. 37)."""
    up, dn = np.r_[0.0, np.diff(h)], np.r_[0.0, -np.diff(l)]
    pdm = np.where((up > dn) & (up > 0), up, 0.0)
    mdm = np.where((dn > up) & (dn > 0), dn, 0.0)
    tr = np.r_[h[0] - l[0], np.maximum(h[1:], c[:-1]) - np.minimum(l[1:], c[:-1])]
    s_tr, s_p, s_m = (_wilder_sum(x, n, 1) for x in (tr, pdm, mdm))
    with np.errstate(invalid="ignore", divide="ignore"):
        pdi, mdi = 100 * s_p / s_tr, 100 * s_m / s_tr
        dx = 100 * np.abs(pdi - mdi) / (pdi + mdi)
    adx = np.full(len(c), np.nan)
    if len(c) >= 2 * n:
        acc = np.nanmean(dx[n:2 * n])
        adx[2 * n - 1] = acc
        for i in range(2 * n, len(c)):
            acc = (acc * (n - 1) + (dx[i] if np.isfinite(dx[i]) else acc)) / n
            adx[i] = acc
    return adx, pdi, mdi


def psar(h, l, start=0.02, step=0.02, cap=0.2) -> np.ndarray:
    """Parabolic SAR trend: +1 while the SAR is below price, -1 while above."""
    n = len(h)
    out = np.zeros(n, np.int8)
    if n < 2:
        return out
    up = h[1] >= h[0]
    sar = l[0] if up else h[0]
    ep = h[1] if up else l[1]
    af = start
    out[1] = 1 if up else -1
    for i in range(2, n):
        sar = sar + af * (ep - sar)
        if up:
            sar = min(sar, l[i - 1], l[i - 2])
            if l[i] < sar:
                up, sar, ep, af = False, ep, l[i], start
            elif h[i] > ep:
                ep, af = h[i], min(af + step, cap)
        else:
            sar = max(sar, h[i - 1], h[i - 2])
            if h[i] > sar:
                up, sar, ep, af = True, ep, h[i], start
            elif l[i] < ep:
                ep, af = l[i], min(af + step, cap)
        out[i] = 1 if up else -1
    return out


def supertrend(h, l, c, n: int = 10, k: float = 3.0) -> np.ndarray:
    a = atr(h, l, c, n)
    mid = (h + l) / 2
    ub, lb = mid + k * a, mid - k * a
    out = np.zeros(len(c), np.int8)
    fu, fl, d = np.nan, np.nan, 1
    for i in range(len(c)):
        if not np.isfinite(a[i]):
            continue
        if np.isnan(fu):
            fu, fl = ub[i], lb[i]
        else:
            fu = ub[i] if (ub[i] < fu or c[i - 1] > fu) else fu
            fl = lb[i] if (lb[i] > fl or c[i - 1] < fl) else fl
        if d == 1 and c[i] < fl:
            d = -1
        elif d == -1 and c[i] > fu:
            d = 1
        out[i] = d
    return out


def _mid_range(h, l, n):
    out = np.full(len(h), np.nan)
    if len(h) >= n:
        out[n - 1:] = (np.lib.stride_tricks.sliding_window_view(h, n).max(axis=1)
                       + np.lib.stride_tricks.sliding_window_view(l, n).min(axis=1)) / 2
    return out


def ichimoku(h, l, c) -> np.ndarray:
    tenkan, kijun, sb_raw = _mid_range(h, l, 9), _mid_range(h, l, 26), _mid_range(h, l, 52)
    sa_raw = (tenkan + kijun) / 2
    sa, sb = np.full(len(c), np.nan), np.full(len(c), np.nan)
    sa[26:], sb[26:] = sa_raw[:-26], sb_raw[:-26]
    top, bot = np.maximum(sa, sb), np.minimum(sa, sb)
    out = np.zeros(len(c), np.int8)
    out[(c > top) & (tenkan > kijun)] = 1
    out[(c < bot) & (tenkan < kijun)] = -1
    return out


def heikin_ashi(o, h, l, c) -> np.ndarray:
    hc = (o + h + l + c) / 4
    ho = np.empty(len(c))
    ho[0] = (o[0] + c[0]) / 2
    for i in range(1, len(c)):
        ho[i] = (ho[i - 1] + hc[i - 1]) / 2
    green = hc > ho
    out = np.zeros(len(c), np.int8)
    for i in range(1, len(c)):
        if green[i] and green[i - 1]:
            out[i] = 1
        elif not green[i] and not green[i - 1]:
            out[i] = -1
        else:
            out[i] = out[i - 1]
    return out


def kalman_slope(c, window: int = 500, q_ratio: float = 1e-3) -> np.ndarray:
    """Filtered slope of a local linear trend on ln C (R = variance of the last `window` log returns)."""
    y = np.log(c)
    r = np.r_[np.nan, np.diff(y)]
    var = np.full(len(c), np.nan)
    if len(c) > window:
        var[window:] = np.lib.stride_tricks.sliding_window_view(r[1:], window).var(axis=1)
    slope = np.full(len(c), np.nan)
    x = np.array([y[0], 0.0])
    p = np.diag([1.0, 1.0])
    for i in range(1, len(c)):
        R = var[i] if np.isfinite(var[i]) else np.nanvar(r[1:i + 1]) if i > 2 else 1e-6
        Q = np.diag([0.0, q_ratio * R])
        x = np.array([x[0] + x[1], x[1]])
        p = np.array([[p[0, 0] + 2 * p[0, 1] + p[1, 1], p[0, 1] + p[1, 1]], [p[0, 1] + p[1, 1], p[1, 1]]]) + Q
        s = p[0, 0] + R
        k = p[:, 0] / s
        x = x + k * (y[i] - x[0])
        p = p - np.outer(k, p[0, :])
        if np.isfinite(var[i]):
            slope[i] = x[1]
    return slope


def state(variant: str, bars) -> np.ndarray:
    o, h, l, c = bars["o"], bars["h"], bars["l"], bars["c"]
    if variant == "TI-MA200":
        return _sign_state(sma(c, 50) - sma(c, 200))
    if variant == "TI-EMA921":
        return _sign_state(ema(c, 9) - ema(c, 21))
    if variant == "TI-TRIPLE":
        e10, e20, e50 = ema(c, 10), ema(c, 20), ema(c, 50)
        out = np.zeros(len(c), np.int8)
        out[(e10 > e20) & (e20 > e50)] = 1
        out[(e10 < e20) & (e20 < e50)] = -1
        return out
    if variant == "TI-MACD":
        macd = ema(c, 12) - ema(c, 26)
        sig = np.full(len(c), np.nan)
        ok = np.flatnonzero(np.isfinite(macd))
        if len(ok) > 9:
            sig[ok] = ema(macd[ok], 9)
        return _sign_state(macd - sig)
    if variant == "TI-ADX":
        adx, pdi, mdi = dmi(h, l, c)
        out = np.zeros(len(c), np.int8)
        out[(adx > 25) & (pdi > mdi)] = 1
        out[(adx > 25) & (mdi > pdi)] = -1
        return out
    if variant == "TI-PSAR":
        return psar(h, l)
    if variant == "TI-SUPER":
        return supertrend(h, l, c)
    if variant == "TI-ICHI":
        return ichimoku(h, l, c)
    if variant == "TI-HA":
        return heikin_ashi(o, h, l, c)
    if variant == "TI-KALMAN":
        return _sign_state(np.nan_to_num(kalman_slope(c), nan=0.0))
    raise ValueError(variant)
