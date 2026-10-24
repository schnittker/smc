import numpy as np
import pytest

from smc.strategy_h import SPECS, CfdSpec
from smc.swaps import RateTable
from strev.model import rolling_extreme, rsi_wilder, run_model_r, sma, targets, trades

SPEC = CfdSpec(**{**SPECS["SPXUSD"].__dict__, "rel_spread": 1e-4})
RATES = RateTable.constant({"USD": 0.05})


def test_sma_and_extremes():
    x = np.arange(10, dtype=float)
    assert np.isnan(sma(x, 3)[1]) and sma(x, 3)[2] == 1.0 and sma(x, 3)[9] == 8.0
    assert rolling_extreme(x, 3, np.min)[5] == 3.0 and rolling_extreme(x, 3, np.max)[5] == 5.0


def test_rsi_wilder_known_values():
    x = np.array([10.0, 11.0, 12.0, 11.0, 10.0, 11.0])
    r = rsi_wilder(x, 2)
    assert np.isnan(r[1]) and r[2] == 100.0                     # two gains, no loss
    # i=3: ag=(1*1+0)/2=0.5, al=(0+1)/2=0.5 -> 50; i=4: ag=0.25, al=0.75 -> 25
    assert r[3] == pytest.approx(50.0) and r[4] == pytest.approx(25.0)


def _px(prices):
    n = len(prices)
    days = np.array([d for d in range(19723, 19723 + 2 * n) if (d + 3) % 7 < 5][:n])
    p = np.asarray(prices, float)
    return {"day": days, "p_sig": p, "p_mark": p, "exact": np.ones(n, bool), "lo": p * 0.999, "hi": p * 1.001}


def test_rsi2_enters_on_dip_in_uptrend_and_exits_above_sma5():
    up = list(1000 + np.arange(220) * 2.0)
    dip = [up[-1] - 10, up[-1] - 20, up[-1] - 30]              # sharp 3-day dip, still above SMA200
    rec = [up[-1] - 5, up[-1] + 5, up[-1] + 15]
    px = _px(up + dip + rec)
    t = targets(px, "R-RSI2")
    keys = sorted(t)
    assert t[keys[0]] == 1.0 and keys[0] == int(px["day"][221])   # RSI2: 16.7 on day 1 of the dip, 6.25 on day 2
    assert t[keys[1]] == 0.0 and keys[1] > keys[0]


def test_no_entry_below_sma200():
    down = list(2000 - np.arange(230) * 2.0)
    assert targets(_px(down), "R-RSI2") == {} and targets(_px(down), "R-7S") == {}


def test_double7_and_trade_log():
    seq = list(1000 + np.arange(220) * 2.0) + [1400, 1390, 1380] + [1450]
    px = _px(seq)
    t = targets(px, "R-7S")
    keys = sorted(t)
    assert t[keys[0]] == 1.0 and t[keys[-1]] == 0.0
    rows = run_model_r("R-7S", SPEC, px, RATES)
    tr = trades(rows)
    assert len(tr) == 1 and tr[0][1] == len(seq) - 1 - list(px["day"]).index(keys[0])
