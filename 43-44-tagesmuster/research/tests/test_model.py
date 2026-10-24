from datetime import date

import numpy as np
import pytest

from dbo.model import Costs
from smc.costs import commission_price, effective_spread, slippage_price
from dpat.model import directions, run_symbol, weekday_choice
from smc.data.bars import BAR_DTYPE

FXC = Costs("fx", "EURUSD")
SP, SL = effective_spread("EURUSD"), slippage_price("EURUSD")
N = lambda d: (d - date(1970, 1, 1)).days


def _d1(days, o, h, l, c):
    return {"day": np.asarray(days), "o": np.asarray(o, float), "h": np.asarray(h, float), "l": np.asarray(l, float),
            "c": np.asarray(c, float)}


def test_big_move_signal_and_direction():
    c = np.r_[np.full(20, 1.0), 1.10, 1.10, 1.10]                    # ATR ~ 0.02 from h - l, jump of 0.10 on day 20
    d1 = _d1(np.arange(23), c, c + 0.01, c - 0.01, c)
    rev, cont = directions("E-REV", d1), directions("E-CONT", d1)
    assert rev[21] == -1 and cont[21] == 1
    assert not rev[:21].any() and not rev[22:].any()


def test_weekday_choice_expanding_window():
    days = np.arange(N(date(2014, 1, 6)), N(date(2016, 12, 31)))
    days = days[(days + 3) % 7 < 5]
    rng = np.random.default_rng(0)
    o = np.ones(len(days))
    r = 0.001 * rng.standard_normal(len(days)) + np.where((days + 3) % 7 == 1, 0.002, 0.0)   # Tuesdays up
    d1 = _d1(days, o, o * 1.01, o * 0.99, o * (1 + r))
    w, d, t = weekday_choice(d1, 2015)
    assert (w, d) == (1, 1) and t > 2
    dirs = directions("E-WD", d1)
    yrs = np.array([date.fromordinal(date(1970, 1, 1).toordinal() + int(x)).year for x in days])
    assert not dirs[yrs == 2014].any()
    assert set(np.flatnonzero(dirs)) == set(np.flatnonzero((yrs >= 2015) & ((days + 3) % 7 == 1)))


def test_run_symbol_open_to_close():
    day0 = N(date(2019, 3, 4))                                         # Monday
    rows = []
    for k in range(25):
        day = day0 + k + 2 * (k // 5)                                  # weekdays only
        base = 1.10 if k < 22 else 1.20
        for j in range(288):
            ts = day * 86400 + 300 * j
            px = base + (0.002 if (k == 23 and j == 287) else 0.0)
            rows.append((ts - 7200, ts, px, px + 0.0005, px - 0.0005, px, 5))
    m5 = np.array(rows, dtype=BAR_DTYPE)
    r = run_symbol("E-CONT", m5, FXC, 0, 10 ** 9)
    tr = r[r["dir"] != 0]
    assert len(tr) == 1 and tr["dir"][0] == 1                          # day 23 after the jump on day 22
    entry = 1.20 + SP + SL
    move = 1.202 - SL - entry - commission_price("EURUSD", entry)
    assert tr["net_bp"][0] == pytest.approx(tr["notional"][0] * move / entry * 1e4)
