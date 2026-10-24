import numpy as np
import pytest

from dbo.model import Costs
from smc.costs import commission_price, effective_spread, slippage_price
from smc.data.bars import BAR_DTYPE
from smc.swaps import RateTable
from smc.timez import server_to_utc
import mtf.model as jm
from mtf.model import DAY, STOP, TARGET, TIME, run_symbol, trend

FXC = Costs("fx", "EURUSD")
SP, SL = effective_spread("EURUSD"), slippage_price("EURUSD")
FLAT = RateTable.constant({"EUR": 0.0, "USD": 0.0})
DAY0 = 19002


def _bars(ohlc, ts0, step):
    rows = [(int(server_to_utc(ts0 + step * j)), ts0 + step * j, o, h, l, c, 60) for j, (o, h, l, c) in enumerate(ohlc)]
    return np.array(rows, dtype=BAR_DTYPE)


def test_trend_uses_only_completed_bars():
    nd = 60
    days = np.arange(DAY0 - nd, DAY0 + 1)
    c = np.r_[np.full(nd, 1.0), 0.5]                                  # last day (DAY0) falls below its EMA50
    d1 = {"day": days, "c": c}
    h4 = _bars([(1.0 + 0.001 * j,) * 4 for j in range(80)], (DAY0 - 13) * DAY, 14400)   # rising H4
    d1["c"][:nd] = np.linspace(0.9, 1.0, nd)                         # rising before DAY0: close > EMA50
    h1 = _bars([(1.0,) * 4] * 3, DAY0 * DAY + 22 * 3600, 3600)       # bars 22:00 (in DAY0), 23:00, 00:00 next day
    tr = trend(h1, h4, d1)
    assert tr[0] == 1                                                # closes 23:00: last full day is DAY0 - 1
    assert tr[1] == 0 and tr[2] == 0                                 # closes 24:00: DAY0 (close 0.5) is complete


def _run(path, sig_bar, d, a=0.0010):
    bars = _bars(path, DAY0 * DAY, 3600)
    orig = jm.signals

    def fake(h1, h4, d1):
        s = np.zeros(len(h1), np.int8)
        s[sig_bar] = d
        return s, np.full(len(h1), a)
    jm.signals = fake
    try:
        return run_symbol("EURUSD", bars, bars, _bars([(1.1,) * 4] * 300, DAY0 * DAY, 300), FXC, FLAT, 0, 10 ** 6)
    finally:
        jm.signals = orig


def test_long_target_two_r():
    path = [(1.1000, 1.1002, 1.0990, 1.1000)] * 12 + [(1.1000, 1.1100, 1.1000, 1.1090)] + [(1.109,) * 4] * 3
    r = _run(path, 11, 1)
    entry = 1.1000 + SP + SL
    stop = min(1.0990 - 0.0005, entry - 0.0010)
    assert r["exit_type"][0] == TARGET
    tgt = entry + 2 * (entry - stop)
    assert r["r_net"][0] == pytest.approx((tgt - entry - commission_price("EURUSD", entry)) / (entry - stop))


def test_short_stopped_and_time_exit():
    path = [(1.1000, 1.1010, 1.0998, 1.1000)] * 12 + [(1.1000, 1.1030, 1.0995, 1.1020)] + [(1.1020,) * 4] * 3
    r = _run(path, 11, -1)
    assert r["exit_type"][0] == STOP
    flat = [(1.1000, 1.1001, 1.0999, 1.1000)] * 80
    r = _run(flat, 11, 1)
    assert r["exit_type"][0] == TIME and r["bars"][0] == 48
