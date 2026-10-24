from datetime import date, datetime
from zoneinfo import ZoneInfo

import numpy as np
import pytest

from smc import timez
from smc.data.bars import resample
from smc.data.histdata import M1_DTYPE
from smc.strategy_h import SLIPPAGE_SPREADS, SPECS, CfdSpec
from fomc.model import ny_utc
from orb.model import EOD, LEVER_CAP, NONE, RISK, STOP, TARGET, dn, run_model_o, trade_day

SPEC = CfdSpec(**{**SPECS["NSXUSD"].__dict__, "rel_spread": 1e-4})
D = date(2023, 7, 12)


def _m5(fn, day=D):
    """One day of M1 bars from 00:00 UTC; fn(minutes after 09:30 New York) -> price (constant before)."""
    t0 = int(datetime(day.year, day.month, day.day, tzinfo=ZoneInfo("UTC")).timestamp())
    t = t0 + 60 * np.arange(1440)
    k = (t - ny_utc(dn(day), 9, 30)) // 60
    c = np.array([fn(int(x)) for x in k], float)
    m1 = np.empty(len(t), M1_DTYPE)
    m1["t"], m1["o"], m1["c"] = t, c, c
    m1["h"], m1["l"] = c, c
    return resample(m1, "M5")


def test_long_to_target():
    # first bar 10000 -> 10010 (low 10000), then steady rise far beyond 10 R
    m5 = _m5(lambda k: 10000 if k < 0 else (10000 + 2 * k if k < 5 else 10010 + 3 * (k - 5)))
    r = trade_day(m5, SPEC, D)
    assert r[1] == 1 and r[2] == TARGET
    ref = 10010.0
    entry = ref * (1 + 1e-4 * (1 + SLIPPAGE_SPREADS))
    risk = entry - 10000.0
    assert r[3] == pytest.approx(risk / ref * 1e4)
    assert r[5] == pytest.approx(10.0)                          # net R at a limit fill = exactly 10
    assert r[4] == pytest.approx(min(RISK / (risk / ref), LEVER_CAP))


def test_short_stopped():
    # first bar falls 10000 -> 9990 (high 10000), then rallies through the high
    m5 = _m5(lambda k: 10000 if k < 0 else (10000 - 2 * k if k < 5 else 9990 + 4 * (k - 5)))
    r = trade_day(m5, SPEC, D)
    assert r[1] == -1 and r[2] == STOP and r[5] < -1.0 and r[10]


def test_flat_day_end_of_day_exit_and_doji():
    m5 = _m5(lambda k: 10000 if k < 0 else (10000 + k if k < 5 else 10004))
    r = trade_day(m5, SPEC, D)
    assert r[2] == EOD and r[1] == 1
    doji = trade_day(_m5(lambda k: 10000), SPEC, D)
    assert doji[2] == NONE and doji[7] == 0.0


def test_run_skips_early_close_days():
    days = run_model_o(_m5(lambda k: 10000, day=date(2023, 11, 24)), SPEC, date(2023, 11, 24), date(2023, 11, 24))
    assert len(days) == 0
