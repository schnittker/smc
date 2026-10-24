"""Model T 'daily breakout' (strategies no. 33-35), as pre-registered in docs/01_Vorregistrierung.md.

D1 bars are the FTMO server days Monday-Friday (17:00-17:00 New York) built from the M5 bid bars; a server day counts
as a D1 bar when it holds at least MIN_BARS M5 bars. (HistData has a one-hour Friday 17:00-18:00 New York stub in
summer that falls on server Saturday; it is not a D1 bar - fixed after the first run.) On server day i, from the bars up to i-1:
  T-NR7     range(i-1) is the smallest of the last 7 ranges          -> levels high(i-1) / low(i-1)
  T-INSIDE  high(i-1) < high(i-2) and low(i-1) > low(i-2)            -> levels high(i-1) / low(i-1)
  T-LW      every day                                                -> open(i) +- 0.5 x range(i-1)
Buy stop (ask reaches the upper level) and sell stop (bid reaches the lower level), one-cancels-other, active from
the first bar of the day until 1 hour before its end; a gap through a level fills at the bar open. Stop at the other
level, exit at the close of the last M5 bar of the day. A bar that touches both levels after (or with) the entry
counts as stopped; if the entry bar touches both levels, the side nearer the bar open is taken. Notional =
min(0.25 % / (R / entry), 10) x capital. No trading on server days 24.12.-01.01.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import date

import numpy as np

from smc.costs import commission_price, effective_spread, slippage_price
from smc.strategy_h import SLIPPAGE_SPREADS, SPECS, spec_for

VARIANTS = ("T-NR7", "T-INSIDE", "T-LW")
FX = ("EURUSD", "GBPUSD", "USDJPY", "AUDUSD", "NZDUSD", "USDCAD", "USDCHF", "XAUUSD")
CFDS = ("SPXUSD", "NSXUSD", "FRXEUR", "UKXGBP", "JPXJPY", "HKXHKD", "AUXAUD", "BCOUSD", "XAGUSD")
UNIVERSE = FX + CFDS
RISK, LEVER_CAP, MIN_BARS, NR, LW_K = 0.0025, 10.0, 12, 7, 0.5
DAY, ORDER_END = 86400, 23 * 3600        # orders until 16:00 New York = 23:00 server
EPOCH = date(1970, 1, 1)
STOP, EOD, NONE = 0, 2, 3

ROW_DTYPE = np.dtype([
    ("day", "i8"), ("dir", "i1"), ("exit_type", "i1"), ("r_bp", "f8"), ("notional", "f8"), ("r_net", "f8"),
    ("net_bp", "f8"), ("cost_bp", "f8"), ("gross_bp", "f8"), ("stopped", "?"),
])


@dataclass(frozen=True)
class Costs:
    """Per-instrument trading costs in price units at a given price."""
    kind: str                 # "fx" or "cfd"
    symbol: str
    rel_spread: float = 0.0   # CFD only
    comm_side: float = 0.0    # CFD only, fraction of notional per side

    def spread(self, p: float) -> float:
        return effective_spread(self.symbol) if self.kind == "fx" else self.rel_spread * p

    def slip(self, p: float) -> float:
        return slippage_price(self.symbol) if self.kind == "fx" else SLIPPAGE_SPREADS * self.rel_spread * p

    def commission(self, p: float) -> float:
        """Round turn."""
        return commission_price(self.symbol, p) if self.kind == "fx" else 2 * self.comm_side * p


def costs_for(symbol: str, m5: np.ndarray) -> Costs:
    if symbol in SPECS:
        s = spec_for(symbol, m5)
        return Costs("cfd", symbol, s.rel_spread, s.commission_side)
    return Costs("fx", symbol)


def server_days(m5: np.ndarray) -> dict:
    """D1 bars of the server days with at least MIN_BARS M5 bars: day, slice bounds, open, high, low, close."""
    sday = m5["ts"] // DAY
    starts = np.flatnonzero(np.r_[True, sday[1:] != sday[:-1]])
    ends = np.r_[starts[1:], len(m5)]
    keep = ((ends - starts) >= MIN_BARS) & ((sday[starts] + 3) % 7 < 5)     # 1970-01-01 was a Thursday
    a, b = starts[keep], ends[keep]
    return {"day": sday[a], "a": a, "b": b, "o": m5["o"][a], "h": np.maximum.reduceat(m5["h"], starts)[keep],
            "l": np.minimum.reduceat(m5["l"], starts)[keep], "c": m5["c"][b - 1]}


def levels(variant: str, d1: dict) -> tuple[np.ndarray, np.ndarray]:
    """Upper and lower level for each D1 bar i (NaN where variant gives no signal)."""
    n = len(d1["day"])
    h, l, rng = d1["h"], d1["l"], d1["h"] - d1["l"]
    up, dn = np.full(n, np.nan), np.full(n, np.nan)
    for i in range(1, n):
        if variant == "T-NR7":
            if i >= NR and rng[i - 1] <= rng[i - NR:i].min():
                up[i], dn[i] = h[i - 1], l[i - 1]
        elif variant == "T-INSIDE":
            if i >= 2 and h[i - 1] < h[i - 2] and l[i - 1] > l[i - 2]:
                up[i], dn[i] = h[i - 1], l[i - 1]
        elif variant == "T-LW":
            up[i], dn[i] = d1["o"][i] + LW_K * rng[i - 1], d1["o"][i] - LW_K * rng[i - 1]
        else:
            raise ValueError(variant)
    return up, dn


def holiday(day: int) -> bool:
    d = date.fromordinal(EPOCH.toordinal() + int(day))
    return (d.month == 12 and d.day >= 24) or (d.month == 1 and d.day == 1)


def trade(m5: np.ndarray, a: int, b: int, up: float, dn: float, cost: Costs):
    """One server day [a, b) of M5 bars with levels up / dn. Returns (dir, exit_type, entry, risk, exit, cost_px)."""
    o, h, l, c, ts = m5["o"], m5["h"], m5["l"], m5["c"], m5["ts"]
    p = 0.5 * (up + dn)
    spread, slip = cost.spread(p), cost.slip(p)
    e = a + int(np.searchsorted(ts[a:b] % DAY, ORDER_END))
    hit_up = h[a:e] + spread >= up
    hit_dn = l[a:e] <= dn
    trig = np.flatnonzero(hit_up | hit_dn)
    if not len(trig):
        return None
    k = a + int(trig[0])
    u, d = bool(hit_up[k - a]), bool(hit_dn[k - a])
    direction = 1 if u and (not d or abs(o[k] + spread - up) <= abs(o[k] - dn)) else -1
    if direction == 1:
        entry = max(up, o[k] + spread) + slip
        risk = entry - dn
        hits = np.flatnonzero(l[k:b] <= dn)
    else:
        entry = min(dn, o[k]) - slip
        risk = up - entry
        hits = np.flatnonzero(h[k:b] + spread >= up)
    if len(hits):
        j = k + int(hits[0])
        if direction == 1:
            px = (dn if j == k else min(dn, o[j])) - slip
        else:
            px = (up if j == k else max(up, o[j] + spread)) + slip
        exit_type = STOP
    else:
        bid = c[b - 1]
        px = bid - slip if direction == 1 else bid + spread + slip
        exit_type = EOD
    return direction, exit_type, entry, risk, px, spread + 2 * slip


def run_symbol(variant: str, m5: np.ndarray, cost: Costs, day_from: int, day_to: int) -> np.ndarray:
    """One row per eligible server day in [day_from, day_to) - flat days included with zeros."""
    d1 = server_days(m5)
    up, dn = levels(variant, d1)
    rows = []
    for i in range(1, len(d1["day"])):
        day = int(d1["day"][i])
        if day < day_from or day >= day_to or holiday(day):
            continue
        if not (np.isfinite(up[i]) and up[i] > dn[i]):
            rows.append((day, 0, NONE, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, False))
            continue
        r = trade(m5, int(d1["a"][i]), int(d1["b"][i]), up[i], dn[i], cost)
        if r is None:
            rows.append((day, 0, NONE, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, False))
            continue
        direction, exit_type, entry, risk, px, cost_px = r
        comm = cost.commission(entry)
        move = direction * (px - entry) - comm
        notional = min(RISK / (risk / entry), LEVER_CAP)
        all_cost = cost_px + comm
        rows.append((day, direction, exit_type, risk / entry * 1e4, notional, move / risk,
                     notional * move / entry * 1e4, notional * all_cost / entry * 1e4,
                     notional * (move + all_cost) / entry * 1e4, exit_type == STOP))
    return np.array(rows, dtype=ROW_DTYPE)
