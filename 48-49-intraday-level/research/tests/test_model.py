from datetime import date

import numpy as np
import pytest

from dbo.model import Costs
from smc.costs import commission_price, effective_spread, slippage_price
from smc.data.bars import BAR_DTYPE
from lvl.model import EOD, STOP, TARGET, pivots, run_pivots, simulate, value_area

FXC = Costs("fx", "EURUSD")
SP, SL = effective_spread("EURUSD"), slippage_price("EURUSD")
N = lambda d: (d - date(1970, 1, 1)).days


def test_value_area_70_percent():
    # 10 blocks: 6 in 100-101, 2 in 101-102, 2 in 99-100 (step 0.5)
    h = np.array([100.99] * 6 + [101.99] * 2 + [99.99] * 2)
    l = np.array([100.0] * 6 + [101.0] * 2 + [99.0] * 2)
    val, vah = value_area(h, l, 0.5)
    assert val <= 100.0 and vah >= 101.0 and vah - val <= 2.0


def test_pivot_formulas():
    lv = pivots(1.11, 1.09, 1.10)
    assert lv["P"] == pytest.approx(1.10) and lv["R1"] == pytest.approx(1.11) and lv["S1"] == pytest.approx(1.09)
    assert lv["R2"] == pytest.approx(1.12) and lv["S2"] == pytest.approx(1.08)
    assert lv["R3"] == pytest.approx(1.13) and lv["S3"] == pytest.approx(1.07)


def _m5(days):
    rows = []
    for day, bars in days:
        for j, (o, h, l, c) in enumerate(bars):
            ts = day * 86400 + 300 * j
            rows.append((ts - 7200, ts, o, h, l, c, 5))
    return np.array(rows, dtype=BAR_DTYPE)


def test_pivot_fade_long_hits_target():
    d0 = N(date(2019, 3, 4))
    day1 = [(1.10, 1.11, 1.09, 1.10)] + [(1.10, 1.10, 1.10, 1.10)] * 287
    day2 = [(1.095, 1.095, 1.0895, 1.090)] + [(1.090, 1.0950, 1.0900, 1.0950), (1.095, 1.1005, 1.0950, 1.1000)] + \
           [(1.10,) * 4] * 285
    r = run_pivots("LV-PFADE", _m5([(d0, day1), (d0 + 1, day2)]), FXC, 0, 10 ** 9)
    t = r[r["dir"] != 0]
    assert len(t) == 1 and t["dir"][0] == 1 and t["exit_type"][0] == TARGET
    entry = 1.09
    assert t["r_net"][0] == pytest.approx((1.10 - entry - commission_price("EURUSD", entry)) / (entry - 1.08))


def test_pivot_breakout_short_to_close():
    d0 = N(date(2019, 3, 4))
    day1 = [(1.10, 1.11, 1.09, 1.10)] + [(1.10,) * 4] * 287
    day2 = [(1.10,) * 4] * 10 + [(1.075, 1.075, 1.065, 1.066)] + [(1.066,) * 4] * 277
    r = run_pivots("LV-PBRK", _m5([(d0, day1), (d0 + 1, day2)]), FXC, 0, 10 ** 9)
    t = r[r["dir"] != 0]
    assert t["dir"][0] == -1 and t["exit_type"][0] == EOD
    entry = 1.07 - SL                                                   # sell stop at S3 (bar opens above it)
    assert t["r_bp"][0] == pytest.approx((1.08 - entry) / entry * 1e4)


def test_simulate_stop_in_entry_bar():
    m5 = _m5([(N(date(2019, 3, 4)), [(1.10, 1.101, 1.08, 1.09), (1.09,) * 4])])
    ex, px, bid = simulate(m5, 0, 2, 1, 1.09, 1.09 - SP, 1.085, 1.10, SP, SL, 1.09)
    assert ex == STOP and px == pytest.approx(1.085 - SL)
