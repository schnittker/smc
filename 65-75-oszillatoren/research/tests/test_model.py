import numpy as np
import pytest

from dbo.model import Costs
from smc.data.bars import BAR_DTYPE
from smc.swaps import RateTable
from smc.timez import server_to_utc
from chart.engine import STOP
from osc.model import SIGNAL, TIME, cci, divergence_signals, flag_signals, renko_state, rsi, run_flags, stoch, wpr

FXC = Costs("fx", "EURUSD")
FLAT = RateTable.constant({"EUR": 0.0, "USD": 0.0})


def _bars(c, w=0.0005, step=3600):
    ts0 = 19002 * 86400
    c = np.asarray(c, float)
    o = np.r_[c[0], c[:-1]]
    rows = [(int(server_to_utc(ts0 + step * j)), ts0 + step * j, o[j], max(o[j], c[j]) + w, min(o[j], c[j]) - w,
             c[j], 1) for j in range(len(c))]
    return np.array(rows, dtype=BAR_DTYPE)


def test_indicator_basics():
    x = np.arange(1.0, 40.0)
    assert rsi(x)[-1] == 100.0 and np.isnan(rsi(x)[13])
    b = _bars(np.linspace(1.0, 1.1, 60))
    k, d = stoch(b["h"], b["l"], b["c"])
    assert k[-1] > 80 and d[-1] > 80
    assert wpr(b["h"], b["l"], b["c"])[-1] > -20
    assert cci(b["h"], b["l"], b["c"])[-1] > 100


def test_rsi_signal_and_flag_engine():
    c = np.r_[np.full(30, 1.10), np.linspace(1.10, 1.08, 15), np.linspace(1.08, 1.0805, 2), np.linspace(1.081, 1.095, 20)]
    b = _bars(c)
    sig, xl, xs = flag_signals("OS-RSI", b)
    i = np.flatnonzero(sig == 1)
    assert len(i) >= 1
    r = run_flags("EURUSD", b, 3600, FXC, FLAT, None, sig, xl, xs, 48, 0)
    assert (r["dir"] == 1).any() and set(r["exit_type"]) <= {SIGNAL, TIME, STOP}


def test_renko_reversal_needs_two_bricks():
    a = np.full(10, 0.005)                                              # brick 0.01
    c = np.array([1.00, 1.012, 1.021, 1.015, 1.005, 0.999, 0.998, 0.99, 0.98, 0.97])
    st = renko_state(c, a)
    assert list(st) == [0, 1, 1, 1, 1, -1, -1, -1, -1, -1]


def test_bullish_divergence():
    n = 120
    c = np.full(n, 1.10)
    c[60:70] = np.linspace(1.10, 1.05, 10)                             # first low with RSI deeply oversold
    c[70:80] = np.linspace(1.05, 1.08, 10)
    c[80:90] = np.linspace(1.08, 1.049, 10)                            # lower low, slower fall -> higher RSI
    c[90:] = np.linspace(1.049, 1.06, 30)
    b = _bars(c, step=14400)
    sig, stop, a = divergence_signals(b)
    assert (sig == 1).any()
