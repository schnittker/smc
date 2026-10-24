import numpy as np
import pytest

from dbo.model import Costs
from smc.costs import commission_price, effective_spread, slippage_price
from smc.data.bars import BAR_DTYPE
from smc.swaps import RateTable
from smc.timez import server_to_utc
import hmr.model as um
from hmr.model import DAY, SIGNAL, STOP, TIME, adx, half_life, run_symbol, signals

FXC = Costs("fx", "EURCHF")
SP, SL = effective_spread("EURCHF"), slippage_price("EURCHF")
FLAT = RateTable.constant({"EUR": 0.0, "CHF": 0.0})
DAY0 = 19002                                                     # a Monday


def _h1(ohlc) -> np.ndarray:
    rows = []
    for j, (o, h, l, c) in enumerate(ohlc):
        ts = DAY0 * DAY + 3600 * j
        rows.append((int(server_to_utc(ts)), ts, o, h, l, c, 60))
    return np.array(rows, dtype=BAR_DTYPE)


def test_adx_trend_vs_chop():
    x = np.arange(100.0)
    assert adx(x + 1, x - 1, x)[-1] > 95
    z = np.tile([0.0, 1.0], 50)
    assert adx(z + 1, z - 1, z)[-1] < 10
    assert np.isnan(adx(x + 1, x - 1, x)[26]) and np.isfinite(adx(x + 1, x - 1, x)[27])


def test_half_life_ar1_and_random_walk():
    rng = np.random.default_rng(0)
    e = rng.standard_normal(20000)
    ar = np.zeros_like(e)
    for t in range(1, len(e)):
        ar[t] = 0.9 * ar[t - 1] + e[t]
    hl = half_life(ar, 5000)
    assert np.isnan(hl[4999]) and hl[-1] == pytest.approx(-np.log(2) / np.log(0.9), rel=0.15)
    hl_rw = half_life(np.cumsum(e), 500)[500:]
    assert np.nanmedian(hl_rw) > 48 and np.mean(hl_rw <= 24) < 0.1             # small-sample bias, rarely <= 24


def test_bb_fade_needs_calm_market():
    calm = 1.10 + 0.0005 * np.tile([1.0, -1.0], 60)
    c = np.r_[calm, 1.0950]
    entry, mid, _ = signals("U-BB", _h1([(x, x + 0.0002, x - 0.0002, x) for x in c]))
    assert entry[-1] == 1
    trend = np.r_[np.linspace(1.0, 1.2, 120), 1.15]
    entry, _, _ = signals("U-BB", _h1([(x, x + 0.0002, x - 0.0002, x) for x in trend]))
    assert entry[-1] == 0                                         # ADX high: no fade


def _run(path, sig_bar, d, mid=1.1000, atr14=0.0010):
    bars = _h1(path)
    orig = um.signals

    def fake(variant, b):
        e = np.zeros(len(b), np.int8)
        e[sig_bar] = d
        return e, np.full(len(b), mid), np.full(len(b), atr14)
    um.signals = fake
    try:
        return run_symbol("U-BB", "EURCHF", bars, FXC, FLAT, 0, 10 ** 6)
    finally:
        um.signals = orig


def test_long_exits_at_middle_line():
    path = [(1.0980, 1.0982, 1.0978, 1.0980)] * 3 + [(1.0985, 1.0995, 1.0985, 1.0992), (1.0995, 1.1005, 1.0995, 1.1001),
                                                     (1.1003, 1.1004, 1.1002, 1.1003)]
    r = _run(path, 2, 1)
    assert r["exit_type"][0] == SIGNAL and r["bars"][0] == 2
    entry = 1.0985 + SP + SL
    assert r["r_net"][0] == pytest.approx((1.1003 - SL - entry - commission_price("EURCHF", entry)) / 0.0020)


def test_time_stop_after_48_bars():
    path = [(1.0980, 1.0982, 1.0978, 1.0980)] * 60
    r = _run(path, 2, 1)
    assert r["exit_type"][0] == TIME and r["bars"][0] == 48


def test_short_stop_has_priority():
    path = [(1.1020, 1.1022, 1.1018, 1.1020)] * 3 + [(1.1020, 1.1045, 1.0990, 1.0995), (1.0995,) * 4]
    r = _run(path, 2, -1)
    assert r["exit_type"][0] == STOP
    entry = 1.1020 - SL
    assert r["r_net"][0] == pytest.approx((entry - (entry + 0.0020 + SL) - commission_price("EURCHF", entry)) / 0.0020)
