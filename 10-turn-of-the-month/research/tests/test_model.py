from datetime import date, datetime
from zoneinfo import ZoneInfo

import numpy as np
import pytest

from smc import timez
from smc.data.bars import resample
from smc.data.histdata import M1_DTYPE
from smc.strategy_h import SPECS, CfdSpec
from smc.swaps import RateTable
from fomc.model import Index, ny_utc
from tom import nyse
from tom.model import day_number, event_days, month_turns, run_model_t

RATES = RateTable.constant({"USD": 0.05})
SPEC = CfdSpec(**{**SPECS["SPXUSD"].__dict__, "rel_spread": 1e-4})


@pytest.mark.parametrize("d", [date(2015, 4, 3), date(2016, 12, 26), date(2017, 1, 2), date(2018, 12, 5),
                               date(2020, 7, 3), date(2021, 7, 5), date(2022, 6, 20), date(2022, 12, 26),
                               date(2023, 1, 2), date(2023, 1, 16), date(2023, 2, 20), date(2023, 5, 29),
                               date(2023, 9, 4), date(2023, 11, 23), date(2024, 6, 19), date(2025, 1, 9)])
def test_nyse_holidays(d):
    assert not nyse.is_trading_day(d)


@pytest.mark.parametrize("d", [date(2021, 12, 31), date(2021, 6, 18), date(2023, 11, 24), date(2015, 4, 6),
                               date(2020, 12, 31), date(2019, 6, 19)])
def test_nyse_open_days(d):
    assert nyse.is_trading_day(d)


def test_month_turn_relative_days():
    turns = {p.isoformat(): (b, a) for p, b, a in month_turns((2021, 1), (2023, 9))}
    before, after = turns["2023-09-01"]
    assert before[0] == date(2023, 8, 31) and after[:3] == [date(2023, 9, 1), date(2023, 9, 5), date(2023, 9, 6)]
    assert event_days(-2, 3, before, after) == (date(2023, 8, 30), date(2023, 9, 6))      # Labor Day skipped
    assert event_days(-5, 2, before, after) == (date(2023, 8, 25), date(2023, 9, 5))
    before, after = turns["2022-01-03"]                     # New Year on Saturday: 31.12.2021 is open
    assert before[0] == date(2021, 12, 31) and after[0] == date(2022, 1, 3)


def _index(start=(2023, 7, 3), days=120, price_fn=None):
    t0 = int(datetime(*start, tzinfo=ZoneInfo("UTC")).timestamp())
    t = t0 + 60 * np.arange(days * 1440)
    t = t[(t // timez.DAY + 3) % 7 < 5]
    c = price_fn(t) if price_fn else 4000.0 + 0 * t
    m1 = np.empty(len(t), M1_DTYPE)
    m1["t"], m1["c"], m1["o"] = t, c, np.r_[c[0], c[:-1]]
    m1["h"], m1["l"] = np.maximum(m1["o"], c) + 0.2, np.minimum(m1["o"], c) - 0.2
    return Index(SPEC, resample(m1, "M5"), resample(m1, "D1"))


def test_run_model_t_times_and_swaps():
    idx = _index()
    rows = run_model_t("T-KLASSIK", idx, (2023, 9), (2023, 10), RATES)
    assert len(rows) == 2
    r = rows[0]
    assert r["day"] == day_number(date(2023, 9, 1))
    assert r["t_entry"] == ny_utc(day_number(date(2023, 8, 30)), 15, 55)
    assert r["t_exit"] == ny_utc(day_number(date(2023, 9, 6)), 15, 55)
    # rollovers Wed 30.8. (3 nights), Thu, Fri (weekend counted on Wednesday), Mon 4.9., Tue 5.9. -> 7 nights
    assert r["swap_bp"] == pytest.approx(7 * (0.018 - 0.05 - 0.025) / 365 * 1e4)


def test_early_window_and_gain():
    t_in = int(ny_utc(day_number(date(2023, 9, 25)), 15, 55))
    idx = _index(price_fn=lambda t: 4000.0 + np.where(t >= t_in, (t - t_in) / 86400.0, 0.0))   # +1 point per day
    r = run_model_t("T-FRÜH", idx, (2023, 10), (2023, 10), RATES)[0]
    assert r["t_entry"] == t_in                               # day -5 = 25.09.2023
    assert r["t_exit"] == ny_utc(day_number(date(2023, 10, 3)), 15, 55)
    assert r["gross_bp"] == pytest.approx((r["t_exit"] - t_in) / 86400 / 4000 * 1e4, rel=1e-3)
