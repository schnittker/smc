from datetime import date, datetime
from zoneinfo import ZoneInfo

import numpy as np
import pytest

from smc import timez
from smc.data.bars import resample
from smc.data.histdata import M1_DTYPE
from smc.strategy_h import SLIPPAGE_SPREADS, SPECS, CfdSpec
from fomc.model import ny_utc
from imom.model import IndexBars, dn, full_days, is_early_close, run_model_i

SPEC = CfdSpec(**{**SPECS["SPXUSD"].__dict__, "rel_spread": 1e-4})
NY = ZoneInfo("America/New_York")


@pytest.mark.parametrize("d, early", [(date(2023, 11, 24), True), (date(2019, 12, 24), True), (date(2023, 7, 3), True),
                                      (date(2020, 7, 3), False), (date(2021, 12, 24), False), (date(2023, 7, 5), False)])
def test_early_close(d, early):
    assert is_early_close(d) is early


def test_full_days_skip_early_close_and_its_next_day():
    pairs = full_days(date(2023, 11, 20), date(2023, 11, 30))
    days = [d for _, d in pairs]
    assert date(2023, 11, 24) not in days and date(2023, 11, 27) not in days      # Fri half day, Mon after it
    assert date(2023, 11, 22) in days and (date(2023, 11, 22), date(2023, 11, 28)) not in pairs


def _bars(price_fn, start=(2023, 6, 1), days=60):
    t0 = int(datetime(*start, tzinfo=ZoneInfo("UTC")).timestamp())
    t = t0 + 60 * np.arange(days * 1440)
    t = t[(t // timez.DAY + 3) % 7 < 5]
    c = price_fn(t)
    m1 = np.empty(len(t), M1_DTYPE)
    m1["t"], m1["c"], m1["o"] = t, c, c                       # every minute opens at its own price
    m1["h"], m1["l"] = c + 0.1, c - 0.1
    return IndexBars(SPEC, resample(m1, "M5"), resample(m1, "H1"))


def _piecewise(day: date, moves: dict[tuple[int, int], float]):
    """Price 4000 with jumps (in points) at given New York times on `day`."""
    def f(t):
        p = np.full(len(t), 4000.0)
        for hm, dp in moves.items():
            p += np.where(t >= ny_utc(dn(day), *hm), dp, 0.0)
        return p
    return f


def test_signal_direction_and_result():
    d = date(2023, 7, 12)
    # up into 10:00, down into 15:30, up 4 points in the last half hour
    idx = _bars(_piecewise(d, {(9, 45): 8.0, (13, 0): -20.0, (15, 45): 4.0}))
    onfh = run_model_i("I-ONFH", idx, d, d)[0]
    rod = run_model_i("I-ROD", idx, d, d)[0]
    assert onfh["dir"] == 1 and rod["dir"] == -1
    assert onfh["r_last_bp"] == pytest.approx(4 / 3988 * 1e4)
    spread = 1.0                                             # bp of the entry price
    assert onfh["net_bp"] == pytest.approx(onfh["r_last_bp"] - spread * (1 + 2 * SLIPPAGE_SPREADS), abs=0.02)
    assert rod["net_bp"] == pytest.approx(-rod["r_last_bp"] - spread * (1 + 2 * SLIPPAGE_SPREADS), abs=0.02)
    assert onfh["cost_bp"] == pytest.approx(1.5, abs=1e-3)


def test_signal_uses_previous_day_1600_close():
    d = date(2023, 7, 12)
    prev = date(2023, 7, 11)
    idx = _bars(_piecewise(prev, {(16, 30): -10.0}))          # drop after the previous close: counts as overnight
    r = run_model_i("I-ONFH", idx, d, d)[0]
    assert r["r_onfh_bp"] == pytest.approx(-10 / 4000 * 1e4) and r["dir"] == -1


def test_missing_bar_skips_day():
    d = date(2023, 7, 12)
    idx = _bars(_piecewise(d, {(9, 45): 8.0}))
    idx.m5 = idx.m5[idx.m5["t"] != ny_utc(dn(d), 15, 30)]
    assert len(run_model_i("I-ONFH", idx, d, d)) == 0


def test_stop_on_crash_in_last_half_hour():
    d = date(2023, 7, 12)
    idx = _bars(lambda t: 4000.0 + 2 * np.sin(t / 900.0) + _piecewise(d, {(9, 45): 8.0, (15, 45): -300.0})(t) - 4000)
    r = run_model_i("I-ONFH", idx, d, d)[0]
    assert r["dir"] == 1 and r["stopped"] and r["net_bp"] < -500       # gap through the stop: filled at the open
