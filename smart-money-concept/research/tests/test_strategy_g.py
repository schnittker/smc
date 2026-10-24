from calendar import timegm

import numpy as np
import pytest

from smc import timez
from smc.data.bars import resample
from smc.data.histdata import M1_DTYPE
from smc.strategy_g import ANNUAL, VOL_TARGET, daily_prices, run_model_g
from smc.swaps import MARKUP, RateTable

RATES = RateTable.constant({"EUR": 0.02, "USD": 0.05})


def _m5(price_fn, weeks=70, start=(2021, 1, 4, 0, 0, 0)):
    """M5 bars for Mon-Fri server days from price_fn(day index, minute of day) - day index counts trading days."""
    srv0 = timegm(start)                                   # server Monday 00:00
    parts, k = [], 0
    for wk in range(weeks):
        for wd in range(5):
            day0 = srv0 + (wk * 7 + wd) * timez.DAY
            minute = np.arange(1440)
            t = timez.server_to_utc(day0 + 60 * minute)
            c = price_fn(k, minute)
            m1 = np.empty(1440, M1_DTYPE)
            m1["t"], m1["c"] = t, c
            m1["o"] = np.r_[c[0], c[:-1]]
            m1["h"], m1["l"] = np.maximum(m1["o"], c) + 1e-5, np.minimum(m1["o"], c) - 1e-5
            parts.append(m1)
            k += 1
    return resample(np.concatenate(parts), "M5")


def test_daily_prices_take_the_1645_and_1650_new_york_prices():
    m5 = _m5(lambda k, m: 1.0 + k + m / 10_000, weeks=1)
    px = daily_prices(m5)
    assert len(px["day"]) == 5 and px["exact"].all()
    # 16:45 New York = server 23:45 = minute 1425 of the server day; the close of the M5 bar ending then
    assert px["p_sig"][2] == pytest.approx(3.0 + 1424 / 10_000)
    assert px["p_mark"][2] == pytest.approx(3.0 + 1429 / 10_000)


def test_uptrend_goes_long_with_volatility_scaled_size_and_never_trades_on_friday():
    rng = np.random.default_rng(3)
    noise = rng.normal(0, 0.004, 400)

    def price(k, m):   # steady uptrend with daily noise, flat inside the day
        return np.full(len(m), 1.0 * np.exp(0.001 * k + noise[: k + 1].sum()))
    rows = run_model_g("EURUSD", _m5(price), RATES)
    live = rows[260:]
    assert (live["w"] > 0).all()
    friday = (live["day"] + 3) % 7 == 4
    assert not live["rebalance"][friday].any()
    # size = 10 % / annualised EWMA volatility of the daily returns (about 0.4 % a day)
    sigma = 0.004 * np.sqrt(ANNUAL)
    assert np.median(live["w"]) == pytest.approx(VOL_TARGET / sigma, rel=0.25)


def test_costs_swaps_and_episode_fee():
    def price(k, m):   # up for 300 trading days, then down: the position flips from long to short
        x = np.where(k < 300, 0.002 * k, 0.6 - 0.002 * (k - 300))
        return np.full(len(m), np.exp(x))
    rows = run_model_g("EURUSD", _m5(price, weeks=90), RATES)
    held = rows[rows["w"] != 0]
    long_, short = held[held["w"] > 0], held[held["w"] < 0]
    assert len(long_) and len(short)
    # swap per night: long (2 % - 5 % - 1 %), short (5 % - 2 % - 1 %); Wednesday counts three nights
    wd = (long_["day"] + 3) % 7
    nights = np.where(wd == 2, 3, 1)
    assert np.allclose(long_["swap"], np.abs(long_["w"]) * (0.02 - 0.05 - MARKUP) * nights / 365)
    wd = (short["day"] + 3) % 7
    nights = np.where(wd == 2, 3, 1)
    assert np.allclose(short["swap"], np.abs(short["w"]) * (0.05 - 0.02 - MARKUP) * nights / 365)
    # trading costs only on rebalancing days, proportional to the traded notional
    trade = rows["rebalance"]
    assert (rows["trade_cost"][~trade] == 0).all() and (rows["trade_cost"][trade] > 0).all()
    # EURUSD pays no conversion fee; the long episode is realised when the position turns short
    assert (rows["fee"] == 0).all()
    flip = np.flatnonzero((np.sign(rows["w"][1:]) != np.sign(rows["w"][:-1])) & (rows["w"][:-1] > 0))[0] + 1
    assert rows["realized"][flip] == pytest.approx(rows["pnl"][: flip + 1].sum())
    eurjpy = run_model_g("EURJPY", _m5(lambda k, m: price(k, m) * 150, weeks=90), RateTable.constant(
        {"EUR": 0.02, "JPY": 0.0}))
    flip_j = np.flatnonzero(eurjpy["realized"] != 0)[0]
    assert eurjpy["fee"][flip_j] == pytest.approx(0.007 * abs(eurjpy["realized"][flip_j]))


def test_model_g_is_history_invariant():
    rng = np.random.default_rng(5)
    steps = rng.normal(0, 0.005, 500)

    def price(k, m):
        return np.full(len(m), 1.1 * np.exp(steps[: k + 1].sum())) * (1 + 1e-4 * np.sin(m / 50))
    m5 = _m5(price, weeks=80)
    full = run_model_g("EURUSD", m5, RATES)
    cut_day = full["day"][330]
    part = run_model_g("EURUSD", m5[m5["ts"] // timez.DAY < cut_day], RATES)
    assert np.array_equal(full[: len(part)], part)
