"""Model H 'pre-holiday US indices', as pre-registered in docs/01_Vorregistrierung.md.

For every regular NYSE holiday h on a weekday: p = last trading day before h, q = trading day before p. Long the
index from 15:55 New York on q to 15:55 on p (12:55 if p is an early-close day), 1 x capital, emergency stop
3 x ATR14(D1); mechanics, costs and swaps of strategy no. 9 (fomc.model.Index.trade_long).
"""
from __future__ import annotations

from datetime import date, timedelta

import numpy as np

from fomc.model import EPOCH, ROW_DTYPE, Index, ny_utc
from imom.model import is_early_close
from smc.swaps import RateTable
from tom import nyse

VARIANTS = {"H-SPX": "SPXUSD", "H-NDX": "NSXUSD"}


def dn(d: date) -> int:
    return (d - EPOCH).days


def events(first: date, last: date) -> list[tuple[date, date, date]]:
    """(holiday, pre-holiday day p, day q before p) for regular weekday holidays in first..last."""
    out = []
    for y in range(first.year, last.year + 1):
        for h in sorted(nyse.holidays(y) - nyse.SPECIAL_CLOSURES):
            if not (first <= h <= last) or h.weekday() >= 5:
                continue
            p = h - timedelta(days=1)
            while not nyse.is_trading_day(p):
                p -= timedelta(days=1)
            q = p - timedelta(days=1)
            while not nyse.is_trading_day(q):
                q -= timedelta(days=1)
            out.append((h, p, q))
    return out


def run_model_h(idx: Index, first: date, last: date, rates: RateTable) -> np.ndarray:
    rows = []
    for h, p, q in events(first, last):
        exit_hm = (12, 55) if is_early_close(p) else (15, 55)
        r = idx.trade_long(int(ny_utc(dn(q), 15, 55)), int(ny_utc(dn(p), *exit_hm)), rates)
        if r is not None:
            rows.append((idx.spec.symbol, dn(h), *r))
    return np.array(rows, dtype=ROW_DTYPE)
