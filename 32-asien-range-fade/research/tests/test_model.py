from datetime import date

import numpy as np
import pytest

from smc.data.bars import resample
from smc.data.histdata import M1_DTYPE
from mer.events import london_utc
from arf.model import bands, night

D = date(2023, 7, 12)
DAY = (D - date(1970, 1, 1)).days


def _m5(fn):
    t0 = int(london_utc(DAY, 0, 0)) - 3 * 3600
    t = t0 + 60 * np.arange(10 * 60)
    k = (t - int(london_utc(DAY, 0, 0))) // 60
    c = np.array([fn(int(x)) for x in k], float)
    m1 = np.empty(len(t), M1_DTYPE)
    m1["t"], m1["o"], m1["c"], m1["h"], m1["l"] = t, c, c, c, c
    return resample(m1, "M5")


def test_bands():
    c = np.r_[np.ones(19), [2.0]]
    sma, up, lo = bands(c)
    assert sma[-1] == pytest.approx(1.05) and up[-1] > 2.0 - 1e-9 - 1 and np.isnan(sma[0])


def test_fade_spike_and_revert_to_mean():
    base = lambda k: 0.9500 + 0.0002 * np.sin(k / 3.0)
    f = lambda k: base(k) + (0.0015 if 60 <= k < 65 else 0.0)            # short spike at 01:00
    row, trades = night(_m5(f), "EURCHF", D)
    assert trades and trades[0][1] == -1 and not trades[0][4]           # short, exited at the mean
    assert trades[0][3] > 0                                              # profitable before costs


def test_stop_when_spike_continues():
    f = lambda k: 0.9500 + 0.0002 * np.sin(k / 3.0) + (0.0015 if 60 <= k < 65 else (0.0015 + 0.0002 * (k - 64) if k >= 65 else 0.0))
    row, trades = night(_m5(f), "EURCHF", D)
    assert trades[0][1] == -1 and trades[0][4] and trades[0][2] < -1.0
