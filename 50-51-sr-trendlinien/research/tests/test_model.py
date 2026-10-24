import numpy as np
import pytest

from dbo.model import Costs
from smc.costs import commission_price, effective_spread, slippage_price
from smc.data.bars import BAR_DTYPE
from smc.swaps import RateTable
from smc.timez import server_to_utc
from chart.engine import STOP, TARGET, TIME, run_trades
from chart.swings import swings
import chart.sr as srm

FXC = Costs("fx", "EURUSD")
SP, SL = effective_spread("EURUSD"), slippage_price("EURUSD")
FLAT = RateTable.constant({"EUR": 0.0, "USD": 0.0})
DAY0 = 19002


def _bars(ohlc, step=14400):
    ts0 = DAY0 * 86400
    rows = [(int(server_to_utc(ts0 + step * j)), ts0 + step * j, o, h, l, c, 1) for j, (o, h, l, c) in enumerate(ohlc)]
    return np.array(rows, dtype=BAR_DTYPE)


def test_swings_need_three_bars_each_side():
    h = np.array([1, 2, 3, 5, 3, 2, 1, 2, 3, 4], float)
    sh, sl = swings(h, h - 1)
    assert list(np.flatnonzero(sh)) == [3] and list(np.flatnonzero(sl)) == [6]


def test_engine_long_target_and_short_stop():
    bars = _bars([(1.1000, 1.1002, 1.0998, 1.1000)] * 2 + [(1.1000, 1.1005, 1.0995, 1.1000),
                                                          (1.1000, 1.1100, 1.1000, 1.1090), (1.109,) * 4])
    sig = np.array([1, 0, 0, 0, 0], np.int8)
    r = run_trades("EURUSD", bars, 14400, FXC, FLAT, None, sig, np.full(5, 1.0980), np.full(5, 0.0010), 0, 2.0, 30)
    entry = 1.1000 + SP + SL
    assert r["exit_type"][0] == TARGET
    assert r["r_net"][0] == pytest.approx((2 * (entry - 1.0980) - commission_price("EURUSD", entry)) / (entry - 1.0980))
    sig = np.array([-1, 0, 0, 0, 0], np.int8)
    r = run_trades("EURUSD", bars, 14400, FXC, FLAT, None, sig, np.full(5, 1.1010), np.full(5, 0.0010), 0, 2.0, 30)
    assert r["exit_type"][0] == STOP


def test_engine_min_distance_and_time_stop():
    bars = _bars([(1.1000, 1.1001, 1.0999, 1.1000)] * 40)
    sig = np.zeros(40, np.int8)
    sig[0] = 1
    r = run_trades("EURUSD", bars, 14400, FXC, FLAT, None, sig, np.full(40, 1.0999), np.full(40, 0.0010), 0, 2.0, 30)
    entry = 1.1000 + SP + SL
    assert r["exit_type"][0] == TIME and r["bars"][0] == 30
    assert r["r_bp"][0] == pytest.approx(0.0010 / entry * 1e4)          # stop pushed to 1 ATR


def test_bounce_and_break_signals():
    n = 200
    base = np.full(n, 1.10)
    h, l = base + 0.0005, base - 0.0005
    for j in (100, 140):                                                 # two swing lows at 1.0950 -> support zone
        l[j] = 1.0950
    h[150] = 1.1060                                                      # single swing high (no zone)
    c = base.copy()
    o = c.copy()
    l[190], c[190] = 1.0952, 1.1000                                      # touch (within 0.25 ATR) and rejection
    bars = _bars(list(zip(o, h, l, c)))
    sig, stop, a = srm.signals("SR-BOUNCE", bars)
    assert sig[190] == 1 and stop[190] == pytest.approx(1.0950 - a[190])
    c2 = c.copy()
    c2[189], c2[190] = 1.0960, 1.0930                                    # close through the zone from above
    l2 = l.copy()
    l2[190] = 1.0925
    sig, stop, a = srm.signals("SR-BREAK", _bars(list(zip(o, h, l2, c2))))
    assert sig[190] == -1


def test_trendline_breakout():
    n = 140
    c = np.full(n, 1.10)
    h, l = c + 0.0005, c - 0.0005
    h[100], h[115] = 1.1100, 1.1060                                      # falling swing highs
    l[108] = 1.0950                                                      # swing low for the stop
    c[129], c[130] = 1.1000, 1.1060                                      # line at 130 ~ 1.1020 -> break
    h[130] = 1.1065
    sig, stop, a = srm.signals("SR-TLINE", _bars(list(zip(c, h, l, c))))
    assert sig[130] == 1 and stop[130] == pytest.approx(1.0950 - 0.5 * a[130])
