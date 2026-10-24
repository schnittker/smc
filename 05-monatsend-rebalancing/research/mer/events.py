"""Month-end event days (last London business day of each month) and London clock times.

Days are day numbers since 1970-01-01 (calendar dates). England-and-Wales bank holidays that can
fall on a month's last weekday are covered: Good Friday, Easter Monday, the last Mondays of May and
August, 25/26 December and 1 January.
"""
from __future__ import annotations

from datetime import date, timedelta

import numpy as np

from smc import timez

EPOCH = date(1970, 1, 1)
HOUR, MIN = 3600, 60


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
    month = (h + l_ - 7 * m + 114) // 31
    day = (h + l_ - 7 * m + 114) % 31 + 1
    return date(year, month, day)


def _last_monday(year: int, month: int) -> date:
    d = date(year + month // 12, month % 12 + 1, 1) - timedelta(days=1)
    return d - timedelta(days=d.weekday())


def uk_holidays(year: int) -> set[date]:
    e = easter(year)
    return {e - timedelta(days=2), e + timedelta(days=1), _last_monday(year, 5), _last_monday(year, 8),
            date(year, 12, 25), date(year, 12, 26), date(year, 1, 1)}


def is_london_business_day(d: date) -> bool:
    return d.weekday() < 5 and d not in uk_holidays(d.year)


def last_business_day(year: int, month: int) -> date:
    d = date(year + month // 12, month % 12 + 1, 1) - timedelta(days=1)
    while not is_london_business_day(d):
        d -= timedelta(days=1)
    return d


def next_business_day(d: date) -> date:
    d += timedelta(days=1)
    while not is_london_business_day(d):
        d += timedelta(days=1)
    return d


def day_number(d: date) -> int:
    return (d - EPOCH).days


def to_date(day: int) -> date:
    return EPOCH + timedelta(days=int(day))


def event_days(first: tuple[int, int], last: tuple[int, int]) -> np.ndarray:
    """Event day numbers for the months first..last (inclusive), each given as (year, month)."""
    (y, m), out = first, []
    while (y, m) <= last:
        out.append(day_number(last_business_day(y, m)))
        y, m = (y + 1, 1) if m == 12 else (y, m + 1)
    return np.array(out, dtype=np.int64)


def london_utc(day, hh: int, mm: int = 0):
    """UTC epoch seconds of hh:mm London time on calendar day number(s) `day`."""
    t0 = np.asarray(day, dtype=np.int64) * timez.DAY
    return t0 + hh * HOUR + mm * MIN - timez.eu_dst(t0 + 12 * HOUR).astype(np.int64) * HOUR
