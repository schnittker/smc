from datetime import date

import numpy as np
import pytest

from chart.engine import STOP, TARGET
from dbo.model import Costs
from smc.costs import effective_spread, slippage_price
from smc.data.bars import BAR_DTYPE
from smc.swaps import RateTable
from smc.timez import server_to_utc
from fch.model import fib_signals, run_chandelier, run_fib

FXC = Costs("fx", "EURUSD")
SP, SL = effective_spread("EURUSD"), slippage_price("EURUSD")
FLAT = RateTable.constant({"EUR": 0.0, "USD": 0.0})
DAY0 = 19002


def _bars(ohlc, step=14400, ts0=DAY0 * 86400):
    rows = [(int(server_to_utc(ts0 + step * j)), ts0 + step * j, o, h, l, c, 1) for j, (o, h, l, c) in enumerate(ohlc)]
    return np.array(rows, dtype=BAR_DTYPE)


def _impulse():
    # swing low 1.08 (bar 35), swing high 1.12 (bar 45), straight decline into the 50-61.8 % zone
    return np.r_[np.full(30, 1.10), np.linspace(1.10, 1.08, 6), np.linspace(1.08, 1.12, 10),
                 np.linspace(1.12, 1.098, 9)[1:]]


def test_fib_long_signal_in_zone_once():
    c = _impulse()
    bars = _bars([(x, x + 0.0002, x - 0.0002, x) for x in c])
    sig, stop, a, tgt = fib_signals(bars)
    i = np.flatnonzero(sig)
    assert len(i) == 1 and sig[i[0]] == 1
    assert tgt[i[0]] == pytest.approx(1.1202) and stop[i[0]] == pytest.approx(1.0798 - 0.25 * a[i[0]])
    assert 1.1202 - 0.618 * (1.1202 - 1.0798) <= c[i[0]] <= 1.1202 - 0.5 * (1.1202 - 1.0798)


def test_fib_trade_reaches_target():
    c = np.r_[_impulse(), np.linspace(1.0985, 1.1210, 8)]
    bars = _bars([(x, x + 0.0002, x - 0.0002, x) for x in c])
    r = run_fib("EURUSD", bars, FXC, FLAT, None, 0, 10 ** 6)
    assert len(r) == 1 and r["exit_type"][0] == TARGET and r["r_net"][0] > 0


def _days(closes, rng=0.004):
    rows = []
    d0 = (date(2019, 1, 7) - date(1970, 1, 1)).days
    k = 0
    for x in closes:
        while (d0 + k + 3) % 7 >= 5:
            k += 1
        for j in range(12):
            ts = (d0 + k) * 86400 + 7200 * j
            rows.append((ts - 7200, ts, x, x + rng / 2, x - rng / 2, x, 5))
        k += 1
    return np.array(rows, dtype=BAR_DTYPE)


def test_chandelier_trails_and_stops():
    closes = np.r_[np.full(60, 1.10), np.linspace(1.10, 1.20, 30), np.linspace(1.20, 1.15, 10)]
    r = run_chandelier("EURUSD", _days(closes), FXC, FLAT, None, 0, 10 ** 6)
    assert len(r) >= 1 and r["dir"][0] == 1 and r["exit_type"][0] == STOP
    assert r["r_net"][0] > 1.0                                          # trend captured well beyond 1 R
