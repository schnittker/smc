import numpy as np
import pytest

from chart.engine import STOP
from dbo.model import Costs
from smc.costs import effective_spread, slippage_price
from smc.data.bars import BAR_DTYPE
from smc.swaps import RateTable
from smc.timez import server_to_utc
from tind.engine import SIGNAL, run_state
from tind.indicators import dmi, heikin_ashi, kalman_slope, psar, sma, state, supertrend

FXC = Costs("fx", "EURUSD")
SP, SL = effective_spread("EURUSD"), slippage_price("EURUSD")
FLAT = RateTable.constant({"EUR": 0.0, "USD": 0.0})


def _bars(c, w=0.001, step=14400):
    ts0 = 19002 * 86400
    c = np.asarray(c, float)
    o = np.r_[c[0], c[:-1]]
    rows = [(int(server_to_utc(ts0 + step * j)), ts0 + step * j, o[j], max(o[j], c[j]) + w, min(o[j], c[j]) - w,
             c[j], 1) for j in range(len(c))]
    return np.array(rows, dtype=BAR_DTYPE)


def test_trend_states_follow_a_v_shape():
    c = np.r_[np.linspace(1.0, 1.3, 300), np.linspace(1.3, 1.0, 300)]
    b = _bars(c)
    for v in ("TI-MA200", "TI-EMA921", "TI-TRIPLE", "TI-MACD", "TI-PSAR", "TI-SUPER", "TI-ICHI", "TI-HA", "TI-ADX"):
        s = state(v, b)
        assert s[280] == 1 and s[590] == -1, v


def test_kalman_needs_500_bars_then_tracks_the_slope():
    rng = np.random.default_rng(0)
    c = np.exp(np.r_[np.linspace(0, 0.3, 800), np.linspace(0.3, 0.0, 800)] + 0.002 * rng.standard_normal(1600))
    s = state("TI-KALMAN", _bars(c))
    assert s[400] == 0 and s[780] == 1 and s[1580] == -1


def test_sma_and_dmi_basics():
    assert sma(np.arange(1.0, 6.0), 2)[1:].tolist() == [1.5, 2.5, 3.5, 4.5]
    x = np.arange(100.0)
    adx, pdi, mdi = dmi(x + 1, x - 1, x)
    assert adx[-1] > 90 and pdi[-1] > mdi[-1]


def test_engine_reverses_on_state_change():
    b = _bars(np.full(40, 1.10), w=0.0005)
    st = np.zeros(40, np.int8)
    st[25:30], st[30:36], st[36:] = 1, -1, 1
    r = run_state("EURUSD", b, 14400, FXC, FLAT, None, st, 0)
    assert list(r["dir"]) == [1, -1, 1]
    assert r["exit_type"][0] == SIGNAL and r["bars"][0] == 5            # held from bar 26 to bar 30 (exit at 31)


def test_engine_emergency_stop():
    c = np.r_[np.full(16, 1.10), 1.06, np.full(5, 1.06)]
    b = _bars(c, w=0.0005)
    st = np.zeros(len(c), np.int8)
    st[14:] = 1
    r = run_state("EURUSD", b, 14400, FXC, FLAT, None, st, 0)
    assert r["exit_type"][0] == STOP and len(r) == 1
