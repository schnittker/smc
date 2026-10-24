"""NYSE trading days: weekdays without the exchange's regular holidays and two special closures.

Regular holidays: New Year's Day, Martin Luther King Jr. Day, Washington's Birthday, Good Friday, Memorial Day,
Juneteenth (from 2022), Independence Day, Labor Day, Thanksgiving, Christmas. A holiday on Saturday is observed
on Friday, on Sunday on Monday - except New Year's Day on a Saturday, which is not observed.
"""
from __future__ import annotations

from datetime import date, timedelta
from functools import lru_cache

SPECIAL_CLOSURES = {date(2018, 12, 5), date(2025, 1, 9)}     # national days of mourning (Bush, Carter)


def easter(year: int) -> date:
    """Gregorian Easter Sunday (anonymous Gregorian algorithm)."""
    a, b, c = year % 19, year // 100, year % 100
    d, e = b // 4, b % 4
    f = (b + 8) // 25
    g = (b - f + 1) // 3
    h = (19 * a + b - d - g + 15) % 30
    i, k = c // 4, c % 4
    l_ = (32 + 2 * e + 2 * i - h - k) % 7
    m = (a + 11 * h + 22 * l_) // 451
    return date(year, (h + l_ - 7 * m + 114) // 31, (h + l_ - 7 * m + 114) % 31 + 1)


def _nth_weekday(year: int, month: int, weekday: int, n: int) -> date:
    d = date(year, month, 1)
    d += timedelta(days=(weekday - d.weekday()) % 7)
    return d + timedelta(weeks=n - 1)


def _last_weekday(year: int, month: int, weekday: int) -> date:
    d = date(year + month // 12, month % 12 + 1, 1) - timedelta(days=1)
    return d - timedelta(days=(d.weekday() - weekday) % 7)


def _observed(d: date) -> date:
    return d - timedelta(days=1) if d.weekday() == 5 else d + timedelta(days=1) if d.weekday() == 6 else d


@lru_cache(maxsize=None)
def holidays(year: int) -> frozenset[date]:
    out = {
        _nth_weekday(year, 1, 0, 3), _nth_weekday(year, 2, 0, 3), easter(year) - timedelta(days=2),
        _last_weekday(year, 5, 0), _observed(date(year, 7, 4)), _nth_weekday(year, 9, 0, 1),
        _nth_weekday(year, 11, 3, 4), _observed(date(year, 12, 25)),
    }
    if date(year, 1, 1).weekday() != 5:
        out.add(_observed(date(year, 1, 1)))
    if year >= 2022:
        out.add(_observed(date(year, 6, 19)))
    return frozenset(out | {d for d in SPECIAL_CLOSURES if d.year == year})


def is_trading_day(d: date) -> bool:
    return d.weekday() < 5 and d not in holidays(d.year)


def trading_days(first: date, last: date) -> list[date]:
    out, d = [], first
    while d <= last:
        if is_trading_day(d):
            out.append(d)
        d += timedelta(days=1)
    return out
