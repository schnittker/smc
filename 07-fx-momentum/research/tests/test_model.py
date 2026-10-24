from calendar import timegm

import numpy as np
import pytest

from smc import timez
from smc.data.bars import resample
from smc.data.histdata import M1_DTYPE
from smc.strategy_g import daily_prices
from smc.swaps import RateTable
from carry.model import FX, usd_log_prices
from xmom.model import excess_values, ranking, run_model_x, schedule

RATES = RateTable.constant({"USD": 0.05, "EUR": 0.01, "GBP": 0.04, "JPY": 0.0, "AUD": 0.045, "CAD": 0.03,
                            "NZD": 0.055, "CHF": 0.0})
DRIFT = {"EUR": 0.008, "CHF": 0.006, "GBP": 0.004, "JPY": 0.001, "CAD": -0.004, "AUD": -0.006, "NZD": -0.008}
BASE = {"EUR": 1.1, "GBP": 1.3, "AUD": 0.7, "NZD": 0.6, "JPY": 0.009, "CAD": 0.75, "CHF": 1.05}


def _m5(price_fn, weeks, start=(2021, 1, 4, 0, 0, 0)):
    srv0 = timegm(start)
    parts, k = [], 0
    for wk in range(weeks):
        for wd in range(5):
            day0 = srv0 + (wk * 7 + wd) * timez.DAY
            minute = np.arange(1440)
            m1 = np.empty(1440, M1_DTYPE)
            m1["t"], m1["c"] = timez.server_to_utc(day0 + 60 * minute), price_fn(k, minute)
            m1["o"] = np.r_[m1["c"][0], m1["c"][:-1]]
            m1["h"], m1["l"] = np.maximum(m1["o"], m1["c"]) + 1e-5, np.minimum(m1["o"], m1["c"]) - 1e-5
            parts.append(m1)
            k += 1
    return resample(np.concatenate(parts), "M5")


def _usd_value(c):
    noise = np.random.default_rng(list(BASE).index(c)).normal(0, 0.001, 800)
    return lambda k, m: BASE[c] * np.exp(DRIFT[c] * k + noise[:k + 1].sum()) * np.ones_like(m, dtype=float)


def _universe(weeks=70, flip_after=None):
    usd = {c: _usd_value(c) for c in BASE}
    if flip_after is not None:                                  # drifts reverse after `flip_after` trading days
        usd = {c: (lambda k, m, c=c: BASE[c] * np.exp(DRIFT[c] * (k if k < flip_after else 2 * flip_after - k))
                   * np.ones_like(m, dtype=float)) for c in BASE}
    usd["USD"] = lambda k, m: np.ones_like(m, dtype=float)
    return {s: daily_prices(_m5(lambda k, m, a=s[:3], b=s[3:]: usd[a](k, m) / usd[b](k, m), weeks)) for s in FX}


@pytest.fixture(scope="module")
def universe():
    return _universe()


def test_excess_values_add_rate_differential():
    days = np.arange(18000, 18010)
    logp = {c: np.zeros(10) for c in ("USD", "EUR", "GBP", "JPY", "AUD", "CAD", "NZD", "CHF")}
    xv = excess_values(days, logp, RATES)
    assert xv["USD"].tolist() == [0.0] * 10
    assert xv["NZD"][9] == pytest.approx(9 * (0.055 - 0.05) / 261)
    assert xv["JPY"][9] == pytest.approx(9 * (0.0 - 0.05) / 261)


def test_ranking_ties_alphabetical():
    s = {"USD": 0, "EUR": 0.02, "GBP": 0.02, "JPY": -0.01, "AUD": 0.01, "CAD": 0, "NZD": -0.02, "CHF": 0.03}
    assert ranking(s) == ["CHF", "EUR", "GBP", "AUD", "CAD", "USD", "JPY", "NZD"]


@pytest.mark.parametrize("variant", ["X-1", "X-12"])
def test_winners_long_losers_short(universe, variant):
    """Steady drifts dominate: EUR, CHF, GBP are the winners, NZD, AUD, CAD the losers."""
    _, log = schedule(universe, RATES, variant)
    assert log
    for _, longs, shorts in log:
        assert longs == ["EUR", "CHF", "GBP"] and shorts == ["NZD", "AUD", "CAD"]


def test_x12_waits_for_a_year_and_skips_last_month():
    """Drifts reverse after 300 days: X-1 turns within a month, X-12 (12-1) much later."""
    px = _universe(weeks=110, flip_after=300)
    common, _ = usd_log_prices(px)
    _, log1 = schedule(px, RATES, "X-1")
    _, log12 = schedule(px, RATES, "X-12")
    first12 = int(np.searchsorted(common, log12[0][0]))
    assert first12 >= 252 and int(np.searchsorted(common, log1[0][0])) >= 60
    flip_day = common[300]
    after1 = [x for x in log1 if x[0] > flip_day + 30]
    after12 = [x for x in log12 if flip_day + 30 < x[0] < flip_day + 120]
    assert after1 and after1[0][1][0] == "NZD"                   # former loser leads after one month
    assert after12 and all(x[1][0] == "EUR" for x in after12)    # 12-1 still on the old winners


def test_targets_ignore_prices_after_the_rebalance_day(universe):
    targets, log = schedule(universe, RATES, "X-1")
    day = log[2][0]
    cut = {s: {k: v[px["day"] <= day] for k, v in px.items()} for s, px in universe.items()}
    t2, _ = schedule(cut, RATES, "X-1")
    assert all(t2[s][day] == targets[s][day] for s in FX)


def test_run_model_x_holds_k3_style_positions(universe):
    rows, log = run_model_x(universe, RATES, "X-1")
    held = set(np.unique(rows["symbol"][rows["w"] != 0]))
    # EUR/NZD and CHF/AUD (two USD legs: AUDUSD, USDCHF) and GBP/CAD
    assert held == {"EURNZD", "AUDUSD", "USDCHF", "GBPCAD"}
