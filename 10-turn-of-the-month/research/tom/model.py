"""Model T 'turn of the month US500', as pre-registered in docs/01_Vorregistrierung.md.

Long US500 over the NYSE trading days around each month turn: T-KLASSIK days -1..+3 (in at the 15:55 New York
price of day -2, out at day +3), T-FRUEH days -4..+2 (in at day -5, out at day +2). Day -1 is the last trading
day of the month, day +1 the first of the next. Position mechanics, emergency stop, costs and swaps are those of
strategy no. 9 (fomc.model.Index).
"""
from __future__ import annotations

from datetime import date, timedelta

import numpy as np

from fomc.model import EPOCH, ROW_DTYPE, Index, ny_utc
from smc.swaps import RateTable
from tom import nyse

VARIANTS = {"T-KLASSIK": (-2, 3), "T-FRÜH": (-5, 2)}     # (entry day, exit day), relative trading days
CLOSE = (15, 55)


def day_number(d: date) -> int:
    return (d - EPOCH).days


def month_turns(first: tuple[int, int], last: tuple[int, int]) -> list[tuple[date, list[date], list[date]]]:
    """Per month turn into the months first..last ((year, month), inclusive): day +1 and the trading days
    before (day -1, -2, ...) and from (day +1, +2, ...) the turn."""
    days = nyse.trading_days(date(*first, 1) - timedelta(days=40), date(*last, 1) + timedelta(days=20))
    out = []
    (y, m) = first
    while (y, m) <= last:
        k = next(i for i, d in enumerate(days) if (d.year, d.month) == (y, m))
        out.append((days[k], days[:k][::-1], days[k:]))
        y, m = (y + 1, 1) if m == 12 else (y, m + 1)
    return out


def event_days(entry: int, exit_: int, before: list[date], after: list[date]) -> tuple[date, date]:
    """Calendar dates of relative trading days entry (< 0) and exit_ (> 0)."""
    return before[-entry - 1], after[exit_ - 1]


def run_model_t(variant: str, idx: Index, first: tuple[int, int], last: tuple[int, int], rates: RateTable) -> np.ndarray:
    """One row per month turn (ROW_DTYPE of strategy no. 9; `day` = day +1)."""
    entry, exit_ = VARIANTS[variant]
    rows = []
    for plus1, before, after in month_turns(first, last):
        d_in, d_out = event_days(entry, exit_, before, after)
        r = idx.trade_long(int(ny_utc(day_number(d_in), *CLOSE)), int(ny_utc(day_number(d_out), *CLOSE)), rates)
        if r is not None:
            rows.append((idx.spec.symbol, day_number(plus1), *r))
    return np.array(rows, dtype=ROW_DTYPE)
