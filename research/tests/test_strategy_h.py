from calendar import timegm
from datetime import datetime
from zoneinfo import ZoneInfo

import numpy as np
import pytest

from smc import timez
from smc.strategy_g import daily_prices, run_trend
from smc.strategy_h import (EUROPE, HONG_KONG, SPECS, SYDNEY, TOKYO, US, CfdSpec, relative_spread, server_time,
                            spec_for)
from smc.swaps import RateTable

from tests.test_strategy_g import _m5

NY = ZoneInfo("America/New_York")


def test_execution_times_in_server_time():
    assert US == 22 * 3600 + 50 * 60 and EUROPE == 17 * 3600 + 50 * 60
    assert TOKYO == 7 * 3600 + 50 * 60 and HONG_KONG == 9 * 3600 + 50 * 60 and SYDNEY == 6 * 3600 + 50 * 60
    # Sydney's 23:50 New York belongs to the next server day (the FX day starts at 17:00 New York)
    day = timegm((2026, 1, 14, 0, 0, 0)) // timez.DAY
    t = int(timez.server_to_utc(day * timez.DAY + SYDNEY))
    assert t == int(datetime(2026, 1, 13, 23, 50, tzinfo=NY).timestamp())
    assert server_time(10, 50) == EUROPE and SPECS["GRXEUR"].signal_time == EUROPE - 300


def test_swap_rates_cover_dividends_financing_and_markup():
    rates = RateTable.constant({"USD": 0.05, "EUR": 0.03})
    spx, dax, oil, gold = SPECS["SPXUSD"], SPECS["GRXEUR"], SPECS["WTIUSD"], SPECS["XAUUSD"]
    assert spx.swap_rate(1, 0, rates) == pytest.approx(0.018 - 0.05 - 0.025)
    assert spx.swap_rate(-1, 0, rates) == pytest.approx(0.05 - 0.018 - 0.025)
    assert dax.swap_rate(1, 0, rates) == pytest.approx(-0.03 - 0.025)        # performance index, no dividend
    assert oil.swap_rate(-1, 0, rates) == pytest.approx(0.05 - 0.025)
    assert gold.swap_rate(1, 0, rates) == pytest.approx(-0.05 - 0.01)
    assert SPECS["HKXHKD"].rate_ccy == "USD" and SPECS["HKXHKD"].fee_rate == 0.007 and spx.fee_rate == 0.0


def test_costs_are_relative_to_the_2026_price_level():
    m5 = _m5(lambda k, m: np.full(len(m), 4000.0 + 0 * k), weeks=2, start=(2026, 3, 2, 0, 0, 0))
    rel = relative_spread("SPXUSD", m5)
    assert rel == pytest.approx(0.55 / 4000.0)
    spec = spec_for("SPXUSD", m5)
    # in 2015 at 2000 points the same relative spread is 0.275 points
    assert spec.spread(2000.0) == pytest.approx(0.275)
    assert spec.trade_cost(2000.0) == pytest.approx((0.5 + 0.25) * 0.275)
    gold = CfdSpec(**{**SPECS["XAUUSD"].__dict__, "rel_spread": 1e-4})
    assert gold.trade_cost(1000.0) == pytest.approx((0.5e-4 + 0.25e-4 + 0.000007) * 1000.0)


def test_european_index_is_marked_at_1050_new_york():
    m5 = _m5(lambda k, m: 1.0 + k + m / 10_000, weeks=1, start=(2026, 3, 2, 0, 0, 0))
    px = daily_prices(m5, EUROPE - 300, EUROPE)
    # 10:50 New York = server 17:50 = minute 1070; the close of the bar ending then is minute 1069
    assert px["p_mark"][1] == pytest.approx(2.0 + 1069 / 10_000)
    assert px["p_sig"][1] == pytest.approx(2.0 + 1064 / 10_000)


def test_trend_engine_runs_on_a_cfd_spec():
    rng = np.random.default_rng(9)
    steps = rng.normal(0.0005, 0.01, 400)
    m5 = _m5(lambda k, m: np.full(len(m), 3000.0 * np.exp(steps[: k + 1].sum())), weeks=75,
             start=(2025, 6, 2, 0, 0, 0))
    spec = spec_for("SPXUSD", m5)
    rows = run_trend(spec, m5, RateTable.constant({"USD": 0.04}))
    live = rows[rows["w"] != 0]
    assert len(live) > 50 and (rows["fee"] == 0).all()
    held = live[(live["day"] + 3) % 7 != 2]          # not Wednesday: one night
    expect = np.abs(held["w"]) * np.where(held["w"] > 0, 0.018 - 0.04 - 0.025, 0.04 - 0.025 - 0.018) / 365
    assert np.allclose(held["swap"], expect)
