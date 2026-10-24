"""Model A 'Asian range fade', as pre-registered in docs/01_Vorregistrierung.md.

M5 Bollinger bands (SMA20 +- 2 sd of the last 20 bid closes). Signals from bars closing between 00:00 and 05:55
London: close above the upper band -> short, below the lower band -> long, at the next bar's open when flat. Exit at
the next open once the close reaches the SMA, at the stop (band width from the entry) or at 06:00. Notional
min(0.25 % / (stop / price), 10) x capital. FX costs of the SMC cost model.
"""
from __future__ import annotations

from datetime import date

import numpy as np

from lbo.model import trading_days
from mer.events import EPOCH, london_utc
from smc.costs import commission_price, effective_spread, slippage_price

VARIANTS = {"A-EURCHF": "EURCHF", "A-AUDCAD": "AUDCAD"}
N, K, RISK, LEVER_CAP = 20, 2.0, 0.0025, 10.0
NIGHT_DTYPE = np.dtype([("day", "i8"), ("trades", "i4"), ("net_bp", "f8"), ("cost_bp", "f8"), ("gross_bp", "f8"),
                        ("stopped", "?")])
TRADE_DTYPE = np.dtype([("day", "i8"), ("dir", "i1"), ("r_net", "f8"), ("r_gross", "f8"), ("stopped", "?")])


def bands(c: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    sma, sd = np.full(len(c), np.nan), np.full(len(c), np.nan)
    for i in range(N - 1, len(c)):
        w = c[i - N + 1:i + 1]
        sma[i], sd[i] = w.mean(), w.std(ddof=0)
    return sma, sma + K * sd, sma - K * sd


def night(m5: np.ndarray, symbol: str, d: date) -> tuple[tuple, list[tuple]] | None:
    day = (d - EPOCH).days
    t0, t6 = int(london_utc(day, 0, 0)), int(london_utc(day, 6, 0))
    a = int(np.searchsorted(m5["t"], t0 - 30 * 300))
    b = int(np.searchsorted(m5["t"], t6))
    if b - a < N + 12:
        return None
    o, h, l, c, t5 = (m5[k][a:b + 1] for k in ("o", "h", "l", "c", "t"))
    sma, up, lo = bands(c)
    spread, slip = effective_spread(symbol), slippage_price(symbol)
    trades, pos, entry, stop, ref, width = [], 0, 0.0, 0.0, 0.0, 0.0

    def close_at(px: float, stopped: bool):
        comm = commission_price(symbol, ref)
        move = pos * (px - entry) - comm
        cost = spread + 2 * slip + comm
        notional = min(RISK / (width / ref), LEVER_CAP)
        trades.append((day, pos, move / width, (move + cost) / width, stopped, notional * move / ref,
                       notional * cost / ref))

    n = len(c)
    for i in range(n):
        if t5[i] >= t6:
            if pos:
                bid = o[i]
                close_at(bid - slip if pos == 1 else bid + spread + slip, False)
                pos = 0
            break
        if pos:
            if pos == 1 and l[i] <= stop:
                close_at(min(stop, o[i]) - slip, True)
                pos = 0
            elif pos == -1 and h[i] + spread >= stop:
                close_at(max(stop, o[i] + spread) + slip, True)
                pos = 0
        closes_in_window = t0 <= t5[i] + 300 <= t6 - 300
        if not closes_in_window or not np.isfinite(sma[i]) or i + 1 >= n or t5[i + 1] >= t6:
            continue
        if pos and ((pos == 1 and c[i] >= sma[i]) or (pos == -1 and c[i] <= sma[i])):
            bid = o[i + 1]
            close_at(bid - slip if pos == 1 else bid + spread + slip, False)
            pos = 0
            continue
        if pos == 0 and (c[i] > up[i] or c[i] < lo[i]) and up[i] > lo[i]:
            pos = -1 if c[i] > up[i] else 1
            ref, width = o[i + 1], up[i] - lo[i]
            if pos == 1:
                entry = ref + spread + slip
                stop = ref - width
            else:
                entry = ref - slip
                stop = ref + spread + width
    if pos:                                                  # data ended before 06:00
        close_at(c[-1] - slip if pos == 1 else c[-1] + spread + slip, False)
    net = sum(x[5] for x in trades)
    cost = sum(x[6] for x in trades)
    row = (day, len(trades), net * 1e4, cost * 1e4, (net + cost) * 1e4, any(x[4] for x in trades))
    return row, [x[:5] for x in trades]


def run_model_a(m5: np.ndarray, symbol: str, first: date, last: date) -> tuple[np.ndarray, np.ndarray]:
    nights, trades = [], []
    for d in trading_days(first, last):
        r = night(m5, symbol, d)
        if r is not None:
            nights.append(r[0])
            trades += r[1]
    return np.array(nights, dtype=NIGHT_DTYPE), np.array(trades, dtype=TRADE_DTYPE)
