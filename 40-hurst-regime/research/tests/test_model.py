import numpy as np
import pytest

from dbo.model import Costs
from smc.costs import commission_price, effective_spread, slippage_price
from smc.data.bars import BAR_DTYPE
from smc.swaps import RateTable
from smc.timez import server_to_utc
import hrs.model as wm
from hrs.model import DAY, MR, SIGNAL, STOP, TIME, TREND, hurst, run_symbol

FXC = Costs("fx", "EURUSD")
SP, SL = effective_spread("EURUSD"), slippage_price("EURUSD")
FLAT = RateTable.constant({"EUR": 0.0, "USD": 0.0})
DAY0 = 19002


def _h4(ohlc) -> np.ndarray:
    rows = []
    for j, (o, h, l, c) in enumerate(ohlc):
        ts = DAY0 * DAY + 14400 * j
        rows.append((int(server_to_utc(ts)), ts, o, h, l, c, 240))
    return np.array(rows, dtype=BAR_DTYPE)


def test_hurst_random_walk_trend_and_reversal():
    rng = np.random.default_rng(3)
    e = 0.001 * rng.standard_normal(6000)
    rw = np.exp(np.cumsum(e))
    assert np.nanmedian(hurst(rw)) == pytest.approx(0.5, abs=0.04)
    ar = np.zeros_like(e)                                         # strongly mean-reverting log price
    for t in range(1, len(e)):
        ar[t] = 0.5 * ar[t - 1] + e[t]
    assert np.nanmedian(hurst(np.exp(ar))) < 0.3
    mom = np.zeros_like(e)                                        # positively autocorrelated returns
    for t in range(1, len(e)):
        mom[t] = 0.5 * mom[t - 1] + e[t]
    assert np.nanmedian(hurst(np.exp(np.cumsum(mom)))) > 0.6
    h = hurst(rw)
    assert np.isnan(h[498]) and np.isfinite(h[499])


def _run(path, sig_bar, d, mode, mid=1.1000, atr14=0.0010):
    bars = _h4(path)
    orig = wm.signals

    def fake(variant, b):
        e = np.zeros(len(b), np.int8)
        e[sig_bar] = d
        m = np.full(len(b), mode, np.int8)
        line = np.full(len(b), mid)
        return {"entry": e, "mode": m, "ema20": line, "sma20": line, "atr14": np.full(len(b), atr14)}
    wm.signals = fake
    try:
        return run_symbol("W-HURST", "EURUSD", bars, None, FXC, FLAT, 0, 10 ** 6)
    finally:
        wm.signals = orig


def test_trend_trade_exits_on_cross_back():
    path = [(1.1010, 1.1012, 1.1008, 1.1010)] * 3 + [(1.1010, 1.1020, 1.1010, 1.1015), (1.1005, 1.1006, 1.0998, 1.0999),
                                                     (1.0999,) * 4]
    r = _run(path, 2, 1, TREND)
    assert r["exit_type"][0] == SIGNAL and r["mode"][0] == TREND and r["bars"][0] == 2


def test_mr_trade_time_stop_12_bars():
    path = [(1.0990, 1.0992, 1.0988, 1.0990)] * 20
    r = _run(path, 2, 1, MR)
    assert r["exit_type"][0] == TIME and r["bars"][0] == 12


def test_stop_priority_and_r():
    path = [(1.1000,) * 4] * 3 + [(1.1000, 1.1001, 1.0970, 1.1005), (1.1005,) * 4]
    r = _run(path, 2, 1, MR)
    entry = 1.1000 + SP + SL
    assert r["exit_type"][0] == STOP
    assert r["r_net"][0] == pytest.approx((-0.0020 - SL - commission_price("EURUSD", entry)) / 0.0020)
