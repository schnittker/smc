from calendar import timegm

import numpy as np
import pytest

from smc import timez
from smc.data.bars import resample
from smc.data.histdata import M1_DTYPE
from smc.strategy_g import FxSpec, daily_prices, run_model_g
from smc.swaps import RateTable, month_index
from carry.model import (FX, VOL_START, CarrySpec, apply_days, ewma_sigma, legs, ranking,
                         rebalance_days, run_model_k, run_weights, schedule)

def _m5(price_fn, weeks=70, start=(2021, 1, 4, 0, 0, 0)):
    """M5 bars for Mon-Fri server days; price_fn(trading-day index, minute of day) (as in the model G tests)."""
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


def _noise(seed, scale=0.006, base=1.1):
    rng = np.random.default_rng(seed)
    steps = rng.normal(0, scale, 400)
    return lambda k, m: base * np.exp(steps[:k].sum() + steps[k] * m / 1440) * np.ones_like(m, dtype=float)


def test_run_weights_reproduces_model_g():
    """Fed with model G's own weights, the generic engine reproduces G's accounting exactly."""
    rates = RateTable.constant({"JPY": 0.001, "USD": 0.05})
    m5 = _m5(lambda k, m: 150 * np.exp(0.08 * np.sin(k / 25.0) + 0.003 * np.sin(k / 3.0)) * np.ones_like(m, dtype=float))
    g = run_model_g("USDJPY", m5, rates)
    assert (g["w"] > 0).any() and (g["w"] < 0).any() and g["fee"].any() and g["swap"].any()
    k = run_weights(FxSpec("USDJPY"), daily_prices(m5), {int(d): float(w) for d, w in zip(g["day"], g["w"])}, rates)
    for col in ("w", "pnl", "trade_cost", "swap", "fee", "realized", "worst", "net", "cost"):
        assert np.allclose(k[col], g[col], rtol=0, atol=1e-15), col


@pytest.mark.parametrize("high, low, expected", [
    ("EUR", "GBP", {"EURUSD": 1, "GBPUSD": -1}),
    ("NZD", "CHF", {"NZDUSD": 1, "USDCHF": 1}),
    ("NZD", "CAD", {"NZDUSD": 1, "USDCAD": 1}),
    ("CHF", "AUD", {"USDCHF": -1, "AUDUSD": -1}),
    ("AUD", "JPY", {"AUDJPY": 1}),
    ("JPY", "AUD", {"AUDJPY": -1}),
    ("USD", "JPY", {"USDJPY": 1}),
    ("CHF", "USD", {"USDCHF": -1}),
    ("GBP", "EUR", {"EURUSD": -1, "GBPUSD": 1}),
])
def test_legs(high, low, expected):
    assert legs(high, low) == expected


def test_legs_cover_every_currency_pair():
    cur = ("USD", "EUR", "GBP", "JPY", "AUD", "CAD", "NZD", "CHF")
    for h in cur:
        for l_ in cur:
            if h != l_:
                assert set(legs(h, l_)) <= set(FX)


def test_ranking_highest_first_ties_alphabetical():
    rates = RateTable.constant({"USD": 0.05, "EUR": 0.02, "GBP": 0.05, "JPY": 0.0, "AUD": 0.04, "CAD": 0.03,
                                "NZD": 0.045, "CHF": 0.0})
    assert ranking(rates, 600) == ["GBP", "USD", "NZD", "AUD", "CAD", "EUR", "CHF", "JPY"]


def test_ewma_sigma_matches_constant_volatility():
    rng = np.random.default_rng(3)
    r = np.r_[np.nan, rng.normal(0, 0.006, 3000)]
    s = ewma_sigma(r)
    assert np.isnan(s[:VOL_START]).all()
    assert s[-1] == pytest.approx(0.006 * np.sqrt(261), rel=0.2)
    assert ewma_sigma(np.r_[np.nan, np.zeros(100)])[VOL_START] == 0.04       # floor


def test_rebalance_days_first_trading_day_of_month_without_holidays():
    days = np.array([timegm(t) // timez.DAY for t in
                     [(2020, 9, d, 0, 0, 0) for d in range(1, 31)] + [(2020, 12, 1, 0, 0, 0), (2020, 12, 2, 0, 0, 0)]
                     + [(2021, 1, 1, 0, 0, 0), (2021, 1, 4, 0, 0, 0), (2021, 2, 1, 0, 0, 0)]])
    days = np.r_[np.arange(days[0] - 100, days[0]), days]
    z = rebalance_days(days)
    got = [str(np.datetime64(int(days[i]), "D")) for i in z]
    assert got[-3:] == ["2020-12-01", "2021-01-04", "2021-02-01"]
    assert "2020-09-01" in got and all(i >= VOL_START for i in z)


def _universe(weeks=70):
    """All 24 FX pairs from 7 independent USD rates; crosses are consistent with the USD pairs."""
    usd = {c: _noise(i, base=b) for i, (c, b) in enumerate(
        [("EUR", 1.1), ("GBP", 1.3), ("AUD", 0.7), ("NZD", 0.6), ("JPY", 0.009), ("CAD", 0.75), ("CHF", 1.05)])}
    usd["USD"] = lambda k, m: np.ones_like(m, dtype=float)
    return {s: daily_prices(_m5(lambda k, m, a=s[:3], b=s[3:]: usd[a](k, m) / usd[b](k, m), weeks=weeks)) for s in FX}


@pytest.fixture(scope="module")
def universe():
    return _universe()


RATES_K = RateTable.constant({"USD": 0.05, "EUR": 0.01, "GBP": 0.04, "JPY": -0.001, "AUD": 0.045, "CAD": 0.03,
                              "NZD": 0.055, "CHF": 0.0})


def test_schedule_k3_weights_and_sizes(universe):
    targets, log = schedule(universe, RATES_K, "K-3")
    day, longs, shorts = log[0]
    assert longs == ["NZD", "USD", "AUD"] and shorts == ["JPY", "CHF", "EUR"]
    w = {s: targets[s][day] for s in FX if targets[s][day] != 0}
    # NZD/JPY and AUD/EUR are direct crosses; USD/CHF is a USD pair
    assert set(w) == {"NZDJPY", "USDCHF", "EURAUD"}
    assert w["NZDJPY"] > 0 and w["USDCHF"] > 0 and w["EURAUD"] < 0
    # 10 % / sigma with sigma ≈ sqrt(2) x 0.6 % daily for an independent-legs cross
    assert w["NZDJPY"] == pytest.approx(0.10 / (np.sqrt(2) * 0.006 * np.sqrt(261)), rel=0.35)


def test_schedule_uses_last_months_rates(universe):
    class Switch(RateTable):
        def rate(self, ccy, month):
            base = RATES_K.rate(ccy, month)
            return base + (0.2 if ccy == "CHF" and month >= self.m0 else 0.0)
    common = universe["EURUSD"]["day"]
    sw = Switch({})
    first, _ = schedule(universe, RATES_K, "K-1")
    rdays = sorted(first["NZDJPY"])
    sw.m0 = int(month_index(rdays[3] * timez.DAY))         # CHF jumps to the top in the month of rebalance 3
    _, log = schedule(universe, sw, "K-1")
    assert log[3][1] == ["NZD"] and log[4][1] == ["CHF"]
    assert len(common) > 300


def test_targets_ignore_prices_after_the_rebalance_day(universe):
    targets, log = schedule(universe, RATES_K, "K-3")
    day = log[2][0]
    cut = {}
    for s, px in universe.items():
        keep = px["day"] <= day
        cut[s] = {k: v[keep] for k, v in px.items()}
    t2, _ = schedule(cut, RATES_K, "K-3")
    for s in FX:
        assert t2[s][day] == targets[s][day]


def test_apply_days_moves_to_next_marked_day():
    px = {"day": np.array([10, 11, 12, 13, 40, 41]), "exact": np.array([True, False, True, True, False, True])}
    assert apply_days(px, {11: 1.0, 41: 2.0}) == {12: 1.0, 41: 2.0}
    assert apply_days(px, {11: 1.0, 12: 0.5}) == {12: 0.5}         # not applicable before the next rebalance -> dropped


def test_run_model_k_swap_markup_and_dollar_neutrality(universe):
    rows, log = run_model_k(universe, RATES_K, "K-1")
    no_markup, _ = run_model_k(universe, RATES_K, "K-1", markup=0.0)
    held = rows["w"] != 0
    # NZD/JPY: carry credit = 5.6 % p. a. minus the 1 % markup per position
    nzdjpy = rows[(rows["symbol"] == "NZDJPY") & held]
    assert len(nzdjpy) > 100 and set(np.unique(rows["symbol"][held])) == {"NZDJPY"}
    ratio = nzdjpy["swap"] / (np.abs(nzdjpy["w"]) * np.where((nzdjpy["day"] + 3) % 7 == 2, 3, 1) / 365)
    assert np.allclose(ratio, 0.056 - 0.01)
    assert (no_markup["swap"] >= rows["swap"]).all() and no_markup["swap"].sum() > rows["swap"].sum()
    assert isinstance(CarrySpec("EURUSD"), FxSpec)
