"""Time model: UTC epoch seconds <-> New York, FTMO server time, Prague.

FTMO's MT5 servers run on GMT+2 / GMT+3 following the US DST calendar, so
server time = New York time + 7 h all year and the D1 bar closes at 17:00 NY.
The FTMO day used by the Max Daily Loss rule is the Prague calendar day; its
reset is 01:00 server time, or 02:00 while US DST is on but EU DST is off.

All functions take and return int64 epoch seconds (scalars or numpy arrays).
"""
from __future__ import annotations

import calendar

import numpy as np

HOUR = 3600
DAY = 86400


def _nth_sunday(year: int, month: int, n: int) -> int:
    first_weekday, _ = calendar.monthrange(year, month)  # Monday=0
    day = 1 + (6 - first_weekday) % 7 + 7 * (n - 1)
    return calendar.timegm((year, month, day, 0, 0, 0))


def _last_sunday(year: int, month: int) -> int:
    first_weekday, ndays = calendar.monthrange(year, month)
    last_weekday = (first_weekday + ndays - 1) % 7
    return calendar.timegm((year, month, ndays - (last_weekday - 6) % 7, 0, 0, 0))


_YEARS = range(1990, 2061)
# US: 2nd Sunday of March 02:00 EST (07:00 UTC) to 1st Sunday of November 02:00 EDT (06:00 UTC)
_US = np.array([(_nth_sunday(y, 3, 2) + 7 * HOUR, _nth_sunday(y, 11, 1) + 6 * HOUR) for y in _YEARS], dtype=np.int64)
# EU: last Sunday of March 01:00 UTC to last Sunday of October 01:00 UTC
_EU = np.array([(_last_sunday(y, 3) + HOUR, _last_sunday(y, 10) + HOUR) for y in _YEARS], dtype=np.int64)


def _in_dst(t, table: np.ndarray):
    t = np.asarray(t, dtype=np.int64)
    edges = table.ravel()  # start0, end0, start1, end1, ... (sorted)
    return (np.searchsorted(edges, t, side="right") % 2) == 1


def us_dst(t_utc):
    return _in_dst(t_utc, _US)


def eu_dst(t_utc):
    return _in_dst(t_utc, _EU)


def utc_to_ny(t_utc):
    t = np.asarray(t_utc, dtype=np.int64)
    return t - (5 * HOUR - us_dst(t) * HOUR)


def utc_to_server(t_utc):
    t = np.asarray(t_utc, dtype=np.int64)
    return t + 2 * HOUR + us_dst(t) * HOUR


def server_to_utc(t_srv):
    """Inverse of utc_to_server; in the repeated autumn hour the DST interpretation wins."""
    s = np.asarray(t_srv, dtype=np.int64)
    dst_guess = s - 3 * HOUR
    return np.where(utc_to_server(dst_guess) == s, dst_guess, s - 2 * HOUR)


def utc_to_prague(t_utc):
    t = np.asarray(t_utc, dtype=np.int64)
    return t + HOUR + eu_dst(t) * HOUR


def ftmo_day(t_utc):
    """Prague calendar day number (days since 1970-01-01) = FTMO trading day for MDL and day counting."""
    return utc_to_prague(t_utc) // DAY


def ny_minute_of_day(t_utc):
    return (utc_to_ny(t_utc) % DAY) // 60


def ny_weekday(t_utc):
    """Monday = 0 ... Sunday = 6 (1970-01-01 was a Thursday)."""
    return (utc_to_ny(t_utc) // DAY + 3) % 7


def fx_day(t_utc):
    """Trading day that closes at 17:00 NY (= server midnight), as a server-day number."""
    return utc_to_server(t_utc) // DAY
