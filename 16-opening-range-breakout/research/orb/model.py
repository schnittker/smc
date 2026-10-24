"""Model O 'opening range breakout 5 minutes', as pre-registered in docs/01_Vorregistrierung.md.

On full NYSE trading days: direction of the 09:30-09:35 New York M5 bar (close vs open); market entry at the open
of the 09:35 bar, stop at the other end of the first bar, target 10 R, otherwise exit at the 16:00 open (or the
15:55 close). Stop before target within a bar. Notional = min(1 % / (R / price), 4) x capital (Zarattini & Aziz
2023). Costs: FTMO average spread and a quarter spread slippage per market fill (cost model H); the target is a
limit fill without slippage; no swaps.
"""
from __future__ import annotations

from datetime import date

import numpy as np

from fomc.model import EPOCH, bar_at, ny_utc
from imom.model import is_early_close
from smc.strategy_h import SLIPPAGE_SPREADS, CfdSpec
from tom import nyse

VARIANTS = {"O-NDX": "NSXUSD", "O-SPX": "SPXUSD"}
RISK, LEVER_CAP, TARGET_R = 0.01, 4.0, 10.0
STOP, TARGET, EOD, NONE = 0, 1, 2, 3

ROW_DTYPE = np.dtype([
    ("day", "i8"), ("dir", "i1"), ("exit_type", "i1"), ("r_bp", "f8"), ("notional", "f8"), ("r_net", "f8"),
    ("r_gross", "f8"), ("net_bp", "f8"), ("cost_bp", "f8"), ("gross_bp", "f8"), ("stopped", "?"),
])


def dn(d: date) -> int:
    return (d - EPOCH).days


def trade_day(m5: np.ndarray, spec: CfdSpec, d: date):
    """One row tuple for day d, a no-trade row (exit_type NONE) for a doji / invalid range, or None if bars are
    missing."""
    o, h, l, c, t5 = m5["o"], m5["h"], m5["l"], m5["c"], m5["t"]
    i1 = bar_at(m5, int(ny_utc(dn(d), 9, 30)))
    i2 = bar_at(m5, int(ny_utc(dn(d), 9, 35)))
    if i1 < 0 or i2 != i1 + 1:
        return None
    t_end = int(ny_utc(dn(d), 16, 0))
    j = bar_at(m5, t_end)
    last = (j - 1) if j >= 0 else int(np.searchsorted(t5, t_end)) - 1
    if last < i2 or t5[last] < ny_utc(dn(d), 15, 30):
        return None
    flat = (dn(d), 0, NONE, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, False)
    direction = int(np.sign(c[i1] - o[i1]))
    if direction == 0:
        return flat
    ref = o[i2]
    spread = spec.rel_spread * ref
    slip = SLIPPAGE_SPREADS * spread
    if direction == 1:
        entry, stop = ref + spread + slip, l[i1]
        risk = entry - stop
    else:
        entry, stop = ref - slip, h[i1]
        risk = stop - entry
    if risk <= 0:
        return flat
    target = entry + direction * TARGET_R * risk
    exit_type, px, cost = EOD, np.nan, spread + 2 * slip
    for k in range(i2, last + 1):
        if direction == 1:
            if l[k] <= stop:
                exit_type, px = STOP, min(stop, o[k]) - slip
                break
            if h[k] >= target:
                exit_type, px, cost = TARGET, max(target, o[k]), spread + slip
                break
        else:
            if h[k] + spread >= stop:
                exit_type, px = STOP, max(stop, o[k] + spread) + slip
                break
            if l[k] + spread <= target:
                exit_type, px, cost = TARGET, min(target, o[k] + spread), spread + slip
                break
    if exit_type == EOD:
        close_bid = o[j] if j >= 0 else c[last]
        px = close_bid - slip if direction == 1 else close_bid + spread + slip
    move = direction * (px - entry)
    notional = min(RISK / (risk / ref), LEVER_CAP)
    net = notional * move / ref
    cost_frac = notional * cost / ref
    return (dn(d), direction, exit_type, risk / ref * 1e4, notional, move / risk, (move + cost) / risk,
            net * 1e4, cost_frac * 1e4, (net + cost_frac) * 1e4, exit_type == STOP)


def run_model_o(m5: np.ndarray, spec: CfdSpec, first: date, last: date) -> np.ndarray:
    rows = []
    for d in nyse.trading_days(first, last):
        if is_early_close(d):
            continue
        r = trade_day(m5, spec, d)
        if r is not None:
            rows.append(r)
    return np.array(rows, dtype=ROW_DTYPE)
