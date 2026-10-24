from datetime import date, datetime
from zoneinfo import ZoneInfo

import numpy as np
import pytest

from smc.costs import effective_spread, slippage_price
from smc.data.bars import resample
from smc.data.histdata import M1_DTYPE
from mer.events import london_utc
from lbo.model import EOD, NONE, STOP, trade_day

D = date(2023, 7, 12)
DAY = (D - date(1970, 1, 1)).days
LON = ZoneInfo("Europe/London")


def _m5(fn):
    """One day of M1 bars; fn(minutes since 00:00 London) -> price."""
    t0 = int(london_utc(DAY, 0, 0))
    t = t0 + 60 * np.arange(20 * 60)
    k = (t - t0) // 60
    c = np.array([fn(int(x)) for x in k], float)
    m1 = np.empty(len(t), M1_DTYPE)
    m1["t"], m1["o"], m1["c"], m1["h"], m1["l"] = t, c, c, c, c
    return resample(m1, "M5")


def test_london_utc_summer():
    assert int(london_utc(DAY, 7, 0)) == int(datetime(2023, 7, 12, 7, 0, tzinfo=LON).timestamp())


def test_long_breakout_held_to_1600():
    # Asia oscillates 1.2700-1.2730; at 08:00 rises to 1.2760 and stays
    f = lambda k: 1.2715 + 0.0015 * np.sin(k / 20.0) if k < 480 else 1.2760
    r = trade_day(_m5(f), "GBPUSD", D)
    assert r[1] == 1 and r[2] == EOD
    spread, slip = effective_spread("GBPUSD"), slippage_price("GBPUSD")
    entry = 1.2760 + spread + slip                       # gap through the buy stop: filled at the open
    assert r[4] == pytest.approx((entry - (1.2715 - 0.0015)) / entry * 1e4, rel=1e-3)


def test_short_breakout_stopped():
    f = lambda k: 1.2715 + 0.0015 * np.sin(k / 20.0) if k < 480 else (1.2690 if k < 600 else 1.2740)
    r = trade_day(_m5(f), "GBPUSD", D)
    assert r[1] == -1 and r[2] == STOP and r[6] < -1.0


def test_no_breakout_flat_day():
    r = trade_day(_m5(lambda k: 1.2715 + 0.0015 * np.sin(k / 20.0) * (1 if k < 420 else 0.5)), "GBPUSD", D)
    assert r[2] == NONE and r[8] == 0.0
