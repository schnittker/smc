from datetime import datetime
from zoneinfo import ZoneInfo

import numpy as np

from smc import timez
from smc.data.bars import resample
from smc.data.histdata import M1_DTYPE, parse_csv

NY = ZoneInfo("America/New_York")


def _ny(*args):
    return int(datetime(*args, tzinfo=NY).timestamp())


def _m1(start_utc, n, base=1.1):
    a = np.empty(n, dtype=M1_DTYPE)
    a["t"] = start_utc + 60 * np.arange(n)
    px = base + 1e-4 * np.arange(n)
    a["o"], a["c"] = px, px + 5e-5
    a["h"], a["l"] = px + 1e-4, px - 1e-4
    return a


def test_parse_csv_converts_fixed_est_to_utc():
    raw = b"20160103 170000;1.087010;1.087130;1.087010;1.087130;0\n20160103 170100;1.087130;1.087200;1.087100;1.087150;0\n"
    a = parse_csv(raw)
    assert a["t"][0] == int(datetime(2016, 1, 3, 22, 0, tzinfo=ZoneInfo("UTC")).timestamp())
    assert a["t"][1] - a["t"][0] == 60
    assert a["h"][1] == 1.0872


def test_d1_rolls_at_17_ny_and_sunday_open_belongs_to_monday():
    # FX opens Sunday 17:00 NY; those bars belong to Monday's D1 (server Monday 00:00)
    m1 = _m1(_ny(2026, 10, 18, 17, 0), 60 * 30)  # Sunday 17:00 NY, 30 hours of minutes
    d1 = resample(m1, "D1")
    assert len(d1) == 2
    assert timez.ny_minute_of_day(d1["t"][0]) == 17 * 60
    assert timez.ny_weekday(d1["t"][0] + 7 * 3600) == 0  # open at Sunday 17:00 NY, i.e. server Monday
    assert d1["n"][0] == 24 * 60
    assert d1["o"][0] == m1["o"][0] and d1["c"][0] == m1["c"][24 * 60 - 1]
    assert d1["h"][0] == m1["h"][: 24 * 60].max() and d1["l"][0] == m1["l"][: 24 * 60].min()


def test_h4_opens_at_server_multiples_of_four_hours():
    m1 = _m1(_ny(2026, 10, 20, 0, 0), 60 * 24)
    h4 = resample(m1, "H4")
    assert set(timez.ny_minute_of_day(h4["t"]) // 60) <= {17, 21, 1, 5, 9, 13}
    assert np.all(h4["ts"] % 14400 == 0)


def test_bar_grid_is_stable_across_us_dst_switch():
    # Friday before and Monday after the US DST end (2026-11-01): D1 still opens at 17:00 NY
    fri = _m1(_ny(2026, 10, 29, 17, 0), 60 * 24)
    mon = _m1(_ny(2026, 11, 1, 17, 0), 60 * 24)
    d1 = resample(np.concatenate([fri, mon]), "D1")
    assert np.all(timez.ny_minute_of_day(d1["t"]) == 17 * 60)
