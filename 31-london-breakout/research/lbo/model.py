"""Model L 'London breakout', as pre-registered in docs/01_Vorregistrierung.md.

Asian range = bid high H and low L of the M5 bars 00:00-07:00 London. From 07:00 to 12:00 a buy stop (ask reaches H)
and a sell stop (bid reaches L), one-cancels-other; stop at the other end of the range; exit at the 16:00 open.
Entry and stop in the same bar count as stopped. Notional = min(0.5 % / (R / price), 10) x capital. FX costs of the
SMC cost model (effective spread, commission, 0.1 pip slippage per market fill).
"""
from __future__ import annotations

from datetime import date, timedelta

import numpy as np

from mer.events import EPOCH, london_utc
from smc.costs import commission_price, effective_spread, slippage_price

VARIANTS = {"L-GBP": "GBPUSD", "L-EUR": "EURUSD"}
RISK, LEVER_CAP, MIN_ASIA_BARS = 0.005, 10.0, 72
STOP, EOD, NONE = 0, 2, 3

ROW_DTYPE = np.dtype([
    ("day", "i8"), ("dir", "i1"), ("exit_type", "i1"), ("range_bp", "f8"), ("r_bp", "f8"), ("notional", "f8"),
    ("r_net", "f8"), ("r_gross", "f8"), ("net_bp", "f8"), ("cost_bp", "f8"), ("gross_bp", "f8"), ("stopped", "?"),
])


def trading_days(first: date, last: date) -> list[date]:
    out, d = [], first
    while d <= last:
        if d.weekday() < 5 and not ((d.month == 12 and d.day >= 24) or (d.month == 1 and d.day == 1)):
            out.append(d)
        d += timedelta(days=1)
    return out


def trade_day(m5: np.ndarray, symbol: str, d: date):
    o, h, l, c, t5 = m5["o"], m5["h"], m5["l"], m5["c"], m5["t"]
    day = (d - EPOCH).days
    t0, t7, t12, t16 = (int(london_utc(day, hh, 0)) for hh in (0, 7, 12, 16))
    a, b = np.searchsorted(t5, [t0, t7])
    if b - a < MIN_ASIA_BARS:
        return None
    hi, lo = float(h[a:b].max()), float(l[a:b].min())
    e = int(np.searchsorted(t5, t12))
    j = int(np.searchsorted(t5, t16))
    if j >= len(t5) or t5[j] != t16:
        j = -1
    last = int(np.searchsorted(t5, t16)) - 1
    if last < b:
        return None
    spread, slip = effective_spread(symbol), slippage_price(symbol)
    flat = (day, 0, NONE, (hi - lo) / lo * 1e4, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, False)
    k = next((i for i in range(b, e) if h[i] >= hi or l[i] <= lo), None)
    if k is None:
        return flat
    up, down = h[k] >= hi, l[k] <= lo
    direction = 1 if up and (not down or abs(o[k] - hi) <= abs(o[k] - lo)) else -1
    if direction == 1:
        entry = max(hi, o[k]) + spread + slip
        stop_level = lo
        risk = entry - stop_level
    else:
        entry = min(lo, o[k]) - slip
        stop_level = hi + spread
        risk = stop_level - entry
    exit_type, px = EOD, np.nan
    for i in range(k, last + 1):
        if direction == 1 and l[i] <= lo:
            exit_type, px = STOP, min(lo, o[i] if i > k else lo) - slip
            break
        if direction == -1 and h[i] >= hi:
            exit_type, px = STOP, max(stop_level, (o[i] + spread) if i > k else stop_level) + slip
            break
    if exit_type == EOD:
        bid = o[j] if j >= 0 else c[last]
        px = bid - slip if direction == 1 else bid + spread + slip
    comm = commission_price(symbol, entry)
    move = direction * (px - entry) - comm
    notional = min(RISK / (risk / entry), LEVER_CAP)
    cost = spread + 2 * slip + comm
    return (day, direction, exit_type, (hi - lo) / lo * 1e4, risk / entry * 1e4, notional, move / risk,
            (move + cost) / risk, notional * move / entry * 1e4, notional * cost / entry * 1e4,
            notional * (move + cost) / entry * 1e4, exit_type == STOP)


def run_model_l(m5: np.ndarray, symbol: str, first: date, last: date) -> np.ndarray:
    rows = [r for r in (trade_day(m5, symbol, d) for d in trading_days(first, last)) if r is not None]
    return np.array(rows, dtype=ROW_DTYPE)
