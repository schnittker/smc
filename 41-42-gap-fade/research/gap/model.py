"""Model Q 'gap fade' (strategies no. 41 and 42), as pre-registered in docs/01_Vorregistrierung.md.

Prior close P, entry at the open O of a fixed M5 bar against the gap g = (O - P) / P: target P (limit, no slippage),
stop one gap beyond O (long: bid <= O - |O - P|; short: ask >= O + |O - P|), time exit at market. Target and stop in
the same bar count as stopped. Notional = min(0.25 % / (R / entry), 10) x capital.
  Q-IDX  US500 / US100 (09:30-16:00 New York, NYSE calendar, 13:00 on early-close days), FRA40 (09:00-17:30 Paris),
         UK100 (08:00-16:30 London); trade if 0.10 % <= |g| <= 1.00 %
  Q-FXW  7 majors; P = close of the last M5 bar of server Friday, entry at server Monday 01:00 with 3x the effective
         spread, exit at the close of the last M5 bar of server Monday; trade if |g| >= 0.10 %
No trades on days 24.12.-01.01.
"""
from __future__ import annotations

from datetime import date, timedelta

import numpy as np

from dbo.model import EPOCH, Costs, holiday
from fomc.model import ny_utc
from imom.model import is_early_close
from mer.events import london_utc
from tom.nyse import trading_days

VARIANTS = ("Q-IDX", "Q-FXW")
IDX = ("SPXUSD", "NSXUSD", "FRXEUR", "UKXGBP")
FXW = ("EURUSD", "GBPUSD", "USDJPY", "AUDUSD", "NZDUSD", "USDCAD", "USDCHF")
RISK, LEVER_CAP = 0.0025, 10.0
IDX_MIN, IDX_MAX, FXW_MIN, FXW_SPREAD_MULT = 0.001, 0.010, 0.001, 3.0
DAY = 86400
STOP, TIME, TARGET, NONE = 0, 4, 5, 3

ROW_DTYPE = np.dtype([
    ("day", "i8"), ("dir", "i1"), ("exit_type", "i1"), ("gap_bp", "f8"), ("r_bp", "f8"), ("notional", "f8"),
    ("r_net", "f8"), ("net_bp", "f8"), ("cost_bp", "f8"), ("gross_bp", "f8"),
])


def fade(m5: np.ndarray, a: int, end: int, exit_bid: float, p: float, cost: Costs, entry_mult: float = 1.0):
    """Fade trade entered at the open of bar a; bars a .. end-1 are watched, then the time exit at exit_bid.
    Returns (dir, exit_type, entry, risk, net move per unit, gross move per unit)."""
    o, h, l = m5["o"], m5["h"], m5["l"]
    po = o[a]
    d = 1 if po < p else -1
    sp, slip = cost.spread(po), cost.slip(po)
    gap = abs(po - p)
    if d == 1:
        entry, stop = po + entry_mult * sp + slip, po - gap
        risk = entry - stop
    else:
        entry, stop = po - slip, po + gap
        risk = stop - entry
    exit_type, bid_out, px = TIME, exit_bid, None
    for j in range(a, end):
        if d == 1:
            if l[j] <= stop:
                bid_out = min(stop, o[j])
                exit_type, px = STOP, bid_out - slip
                break
            if h[j] >= p:
                bid_out = max(p, o[j])
                exit_type, px = TARGET, bid_out
                break
        else:
            if h[j] + sp >= stop:
                px = max(stop, o[j] + sp) + slip
                exit_type, bid_out = STOP, px - sp - slip
                break
            if l[j] + sp <= p:
                px = min(p, o[j] + sp)
                exit_type, bid_out = TARGET, px - sp
                break
    if px is None:
        px = exit_bid - slip if d == 1 else exit_bid + sp + slip
    comm = cost.commission(entry)
    return d, exit_type, entry, risk, d * (px - entry) - comm, d * (bid_out - po)


def _row(day, gap, res):
    d, exit_type, entry, risk, move, gross = res
    notional = min(RISK / (risk / entry), LEVER_CAP)
    return (day, d, exit_type, gap * 1e4, risk / entry * 1e4, notional, move / risk, notional * move / entry * 1e4,
            notional * (gross - move) / entry * 1e4, notional * gross / entry * 1e4)


def _flat(day, gap=0.0):
    return (day, 0, NONE, gap * 1e4, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0)


def bar_exact(t5: np.ndarray, t: int) -> int:
    i = int(np.searchsorted(t5, t))
    return i if i < len(t5) and t5[i] == t else -1


def session(symbol: str, day: int, early: bool = False) -> tuple[int, int]:
    """UTC open and close of the cash session on calendar day number `day`."""
    if symbol in ("SPXUSD", "NSXUSD"):
        return int(ny_utc(day, 9, 30)), int(ny_utc(day, 13 if early else 16, 0))
    if symbol == "FRXEUR":                       # 09:00-17:30 Paris = 08:00-16:30 London all year
        return int(london_utc(day, 8, 0)), int(london_utc(day, 16, 30))
    if symbol == "UKXGBP":                       # 08:00-16:30 London
        return int(london_utc(day, 8, 0)), int(london_utc(day, 16, 30))
    raise ValueError(symbol)


def index_days(symbol: str, m5: np.ndarray, first: date, last: date) -> list[tuple[int, int, bool, bool]]:
    """(day, previous day, day is early close, previous is early close) for the cash sessions of `symbol`."""
    if symbol in ("SPXUSD", "NSXUSD"):
        days = trading_days(first - timedelta(days=10), last)
        out = [((d - EPOCH).days, (p - EPOCH).days, is_early_close(d), is_early_close(p))
               for p, d in zip(days[:-1], days[1:]) if d >= first]
        return out
    t5 = m5["t"]
    ok = []
    d = first - timedelta(days=10)
    while d <= last:
        n = (d - EPOCH).days
        if d.weekday() < 5:
            t_open, t_close = session(symbol, n)
            if bar_exact(t5, t_open) >= 0 and bar_exact(t5, t_close) >= 0:
                ok.append(n)
        d += timedelta(days=1)
    first_n = (first - EPOCH).days
    return [(d, p, False, False) for p, d in zip(ok[:-1], ok[1:]) if d >= first_n]


def run_index(symbol: str, m5: np.ndarray, cost: Costs, first: date, last: date) -> np.ndarray:
    t5 = m5["t"]
    rows = []
    for day, prev, early, prev_early in index_days(symbol, m5, first, last):
        if holiday(day):
            continue
        t_open, t_close = session(symbol, day, early)
        _, t_pclose = session(symbol, prev, prev_early)
        a, e, pc = bar_exact(t5, t_open), bar_exact(t5, t_close), bar_exact(t5, t_pclose)
        if a < 0 or e < 0 or pc < 0:
            continue
        p = m5["o"][pc]
        g = (m5["o"][a] - p) / p
        if not IDX_MIN <= abs(g) <= IDX_MAX:
            rows.append(_flat(day, g))
            continue
        rows.append(_row(day, g, fade(m5, a, e, m5["o"][e], p, cost)))
    return np.array(rows, dtype=ROW_DTYPE)


def run_weekend(symbol: str, m5: np.ndarray, cost: Costs, first: date, last: date, entry_sec: int = 3600,
                spread_mult: float = FXW_SPREAD_MULT) -> np.ndarray:
    """entry_sec / spread_mult other than the defaults are used only by the descriptive robustness checks."""
    ts = m5["ts"]
    sday = ts // DAY
    rows = []
    for monday in range((first - EPOCH).days, (last - EPOCH).days + 1):
        if (monday + 3) % 7 != 0 or holiday(monday):
            continue
        lo, hi = np.searchsorted(sday, [monday - 3, monday - 2])
        if hi == lo:
            continue
        a = bar_exact(ts, monday * DAY + entry_sec)
        m_lo, m_hi = np.searchsorted(sday, [monday, monday + 1])
        if a < 0 or m_hi - m_lo < 12:
            continue
        p = m5["c"][hi - 1]
        g = (m5["o"][a] - p) / p
        if abs(g) < FXW_MIN:
            rows.append(_flat(monday, g))
            continue
        rows.append(_row(monday, g, fade(m5, a, m_hi, m5["c"][m_hi - 1], p, cost, spread_mult)))
    return np.array(rows, dtype=ROW_DTYPE)
