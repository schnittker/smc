"""Model N 'NFP straddle' (strategy no. 94), as pre-registered in docs/01_Vorregistrierung.md.

NFP release = third Friday after the Saturday ending the reference week (the week with the 12th); on a federal
holiday one week later in January, otherwise the Thursday before. Reference P = open of the 08:29 New York M1 bar,
k = 0.10 % of P; buy stop P + k (ask) / sell stop P - k (bid), OCO, 08:30-08:39; stop 2k beyond the entry; exit at
the 09:30 open. Fills 08:30-08:34 pay 5x the effective spread and 0.03 % slippage. Entry and stop in the same bar
count as stopped. Notional = min(0.25 % / (R / entry), 10) x capital.
"""
from __future__ import annotations

from datetime import date, timedelta

import numpy as np

from dbo.model import EPOCH, Costs
from fomc.model import ny_utc

SYMBOLS = ("EURUSD", "GBPUSD", "USDJPY", "XAUUSD")
K, NEWS_SPREAD, NEWS_SLIP, RISK, LEVER_CAP = 0.0010, 5.0, 0.0003, 0.0025, 10.0
STOP, TIME, NONE = 0, 4, 3

ROW_DTYPE = np.dtype([
    ("day", "i8"), ("dir", "i1"), ("exit_type", "i1"), ("r_bp", "f8"), ("notional", "f8"), ("r_net", "f8"),
    ("net_bp", "f8"), ("cost_bp", "f8"), ("gross_bp", "f8"),
])


def _friday_holiday(d: date) -> bool:
    if d.month == 1 and d.day == 1:
        return True
    if d.month == 7 and (d.day == 4 or (d.day == 3 and d.weekday() == 4)):
        return True
    return d.month == 12 and d.day == 31 and d.weekday() == 4      # New Year's Day observed on Friday


def nfp_date(year: int, month: int) -> date:
    """Release date of the employment report for the data month (year, month)."""
    d12 = date(year, month, 12)
    saturday = d12 + timedelta(days=(5 - d12.weekday()) % 7)
    rel = saturday + timedelta(days=20)
    if _friday_holiday(rel):
        rel = rel + timedelta(days=7) if rel.month == 1 else rel - timedelta(days=1)
    return rel


def nfp_dates(first: date, last: date) -> list[date]:
    out, y, m = [], first.year - 1, 11
    while True:
        d = nfp_date(y, m)
        if d > last:
            return out
        if d >= first:
            out.append(d)
        y, m = (y + 1, 1) if m == 12 else (y, m + 1)


def bar_exact(t: np.ndarray, x: int) -> int:
    i = int(np.searchsorted(t, x))
    return i if i < len(t) and t[i] == x else -1


def straddle(m1: np.ndarray, t1: np.ndarray, d: date, cost: Costs, spread_mult: float = NEWS_SPREAD,
             news_slip: float = NEWS_SLIP):
    day = (d - EPOCH).days
    i0 = bar_exact(t1, int(ny_utc(day, 8, 29)))
    i_end = bar_exact(t1, int(ny_utc(day, 9, 30)))
    t_last_entry = int(ny_utc(day, 8, 39))
    t_news_end = int(ny_utc(day, 8, 34))
    if i0 < 0 or i_end < 0:
        return None
    o, h, l = m1["o"], m1["h"], m1["l"]
    p = o[i0]
    k = K * p
    base_sp, base_slip = cost.spread(p), cost.slip(p)

    def sp_slip(j):
        news = t1[j] <= t_news_end
        return (spread_mult * base_sp, news_slip * p) if news else (base_sp, base_slip)
    up, dn = p + k, p - k
    e = int(np.searchsorted(t1, t_last_entry, side="right"))
    entry_bar = None
    for j in range(i0 + 1, e):
        sp, _ = sp_slip(j)
        hu, hd = h[j] + sp >= up, l[j] <= dn
        if hu or hd:
            entry_bar, d_ = j, (1 if hu and (not hd or abs(o[j] + sp - up) <= abs(o[j] - dn)) else -1)
            break
    if entry_bar is None:
        return (day, 0, NONE, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
    j = entry_bar
    sp, slip = sp_slip(j)
    if d_ == 1:
        entry = max(up, o[j] + sp) + slip
        bid_in = entry - sp - slip
        stop = entry - 2 * k
    else:
        entry = min(dn, o[j]) - slip
        bid_in = entry + slip
        stop = entry + 2 * k
    risk = 2 * k
    exit_type, px, bid_out = TIME, None, None
    for q in range(j, i_end):
        sq, slq = sp_slip(q)
        if d_ == 1 and l[q] <= stop:
            b = stop if q == j else min(stop, o[q])
            exit_type, px, bid_out = STOP, b - slq, b
            break
        if d_ == -1 and h[q] + sq >= stop:
            a = (stop if q == j else max(stop, o[q] + sq)) + slq
            exit_type, px, bid_out = STOP, a, a - sq - slq
            break
    if px is None:
        bid_out = o[i_end]
        px = bid_out - base_slip if d_ == 1 else bid_out + base_sp + base_slip
    comm = cost.commission(entry)
    move = d_ * (px - entry) - comm
    gross = d_ * (bid_out - bid_in)
    notional = min(RISK / (risk / entry), LEVER_CAP)
    return (day, d_, exit_type, risk / entry * 1e4, notional, move / risk, notional * move / entry * 1e4,
            notional * (gross - move) / entry * 1e4, notional * gross / entry * 1e4)


def run_symbol(symbol: str, m1: np.ndarray, first: date, last: date, spread_mult: float = NEWS_SPREAD,
               news_slip: float = NEWS_SLIP) -> np.ndarray:
    t1 = np.ascontiguousarray(m1["t"])
    cost = Costs("fx", symbol)
    rows = [r for r in (straddle(m1, t1, d, cost, spread_mult, news_slip) for d in nfp_dates(first, last))
            if r is not None]
    return np.array(rows, dtype=ROW_DTYPE)
