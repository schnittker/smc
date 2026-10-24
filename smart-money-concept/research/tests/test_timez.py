import calendar
from datetime import datetime, timezone
from zoneinfo import ZoneInfo

import numpy as np

from smc import timez

NY = ZoneInfo("America/New_York")
PRAGUE = ZoneInfo("Europe/Prague")


def _offset(tz, t):
    return int(datetime.fromtimestamp(int(t), tz=timezone.utc).astimezone(tz).utcoffset().total_seconds())


def test_matches_zoneinfo_for_random_instants():
    rng = np.random.default_rng(1)
    lo = calendar.timegm((2014, 1, 1, 0, 0, 0))
    hi = calendar.timegm((2027, 12, 31, 0, 0, 0))
    ts = rng.integers(lo, hi, 20000)
    ny = timez.utc_to_ny(ts)
    pr = timez.utc_to_prague(ts)
    for t, a, b in zip(ts, ny, pr):
        assert a - t == _offset(NY, t)
        assert b - t == _offset(PRAGUE, t)


def test_server_is_new_york_plus_seven_hours():
    ts = np.arange(calendar.timegm((2025, 1, 1, 0, 0, 0)), calendar.timegm((2027, 1, 1, 0, 0, 0)), 3571)
    assert np.all(timez.utc_to_server(ts) - timez.utc_to_ny(ts) == 7 * 3600)


def test_server_round_trip():
    ts = np.arange(calendar.timegm((2025, 1, 1, 0, 0, 0)), calendar.timegm((2027, 1, 1, 0, 0, 0)), 997)
    back = timez.server_to_utc(timez.utc_to_server(ts))
    # Only the repeated server hour after the US DST end (Sunday 06:00-07:00 UTC, market closed) is ambiguous.
    repeated = np.zeros(len(ts), bool)
    for y in (2025, 2026):
        end = timez._nth_sunday(y, 11, 1) + 6 * 3600
        repeated |= (ts >= end) & (ts < end + 3600)
    assert np.all(back[~repeated] == ts[~repeated])
    assert np.all(timez.ny_weekday(ts[repeated]) == 6)


def _server_hour_of_prague_midnight(y, m, d):
    # Prague midnight of the given date, expressed in FTMO server time
    local = datetime(y, m, d, tzinfo=PRAGUE)
    t = int(local.timestamp())
    return int(timez.utc_to_server(t) % 86400 // 3600)


def test_ftmo_daily_reset_hour():
    assert _server_hour_of_prague_midnight(2026, 10, 20) == 1   # both on summer time
    assert _server_hour_of_prague_midnight(2026, 10, 27) == 2   # EU winter, US summer (gap week)
    assert _server_hour_of_prague_midnight(2026, 11, 3) == 1    # both on winter time
    assert _server_hour_of_prague_midnight(2026, 3, 16) == 2    # spring gap week
    assert _server_hour_of_prague_midnight(2027, 11, 2) == 2    # autumn gap week 2027


def test_fx_day_rolls_at_17_ny():
    before = int(datetime(2026, 10, 21, 16, 59, tzinfo=NY).timestamp())
    after = int(datetime(2026, 10, 21, 17, 0, tzinfo=NY).timestamp())
    assert timez.fx_day(after) == timez.fx_day(before) + 1


def test_weekday_and_minute():
    t = int(datetime(2026, 10, 23, 9, 30, tzinfo=NY).timestamp())  # Friday 09:30 NY
    assert timez.ny_weekday(t) == 4
    assert timez.ny_minute_of_day(t) == 9 * 60 + 30
