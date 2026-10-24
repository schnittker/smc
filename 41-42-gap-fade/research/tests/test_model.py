from datetime import date

import numpy as np
import pytest

from dbo.model import Costs
from smc.costs import commission_price, effective_spread, slippage_price
from smc.data.bars import BAR_DTYPE
from smc.timez import server_to_utc
from gap.model import STOP, TARGET, TIME, fade, index_days, run_weekend, session

FXC = Costs("fx", "EURUSD")
SP, SL = effective_spread("EURUSD"), slippage_price("EURUSD")


def _m5(ohlc, ts0: int) -> np.ndarray:
    rows = []
    for j, (o, h, l, c) in enumerate(ohlc):
        ts = ts0 + 300 * j
        rows.append((int(server_to_utc(ts)), ts, o, h, l, c, 5))
    return np.array(rows, dtype=BAR_DTYPE)


def test_long_fade_hits_target():
    bars = [(1.0980, 1.0985, 1.0978, 1.0984), (1.0984, 1.1001, 1.0983, 1.0999), (1.1, 1.1, 1.1, 1.1)]
    m5 = _m5(bars, 19002 * 86400)
    d, ex, entry, risk, move, gross = fade(m5, 0, 3, 1.1, 1.1000, FXC)
    assert d == 1 and ex == TARGET
    assert entry == pytest.approx(1.0980 + SP + SL) and risk == pytest.approx(entry - 1.0960)
    assert move == pytest.approx(1.1000 - entry - commission_price("EURUSD", entry))
    assert gross == pytest.approx(0.0020)


def test_short_fade_stopped_and_same_bar_rule():
    bars = [(1.1020, 1.1022, 1.1015, 1.1018), (1.1018, 1.1045, 1.0990, 1.1040)]   # target and stop in bar 1
    m5 = _m5(bars, 19002 * 86400)
    d, ex, entry, risk, move, _ = fade(m5, 0, 2, 1.1040, 1.1000, FXC)
    assert d == -1 and ex == STOP
    assert move == pytest.approx(entry - (1.1040 + SL) - commission_price("EURUSD", entry))


def test_time_exit_and_entry_spread_multiplier():
    bars = [(1.0980, 1.0985, 1.0975, 1.0982)] * 4
    m5 = _m5(bars, 19002 * 86400)
    d, ex, entry, risk, move, gross = fade(m5, 0, 4, 1.0982, 1.1000, FXC, 3.0)
    assert ex == TIME and entry == pytest.approx(1.0980 + 3 * SP + SL)
    assert gross == pytest.approx(0.0002) and move == pytest.approx(1.0982 - SL - entry - commission_price("EURUSD", entry))


def test_us_index_days_use_nyse_calendar_and_early_close():
    days = index_days("SPXUSD", None, date(2019, 11, 28), date(2019, 12, 3))
    n = lambda d: (d - date(1970, 1, 1)).days
    assert days[0] == (n(date(2019, 11, 29)), n(date(2019, 11, 27)), True, False)    # Thanksgiving skipped
    assert days[1] == (n(date(2019, 12, 2)), n(date(2019, 11, 29)), False, True)
    o, c = session("SPXUSD", n(date(2019, 11, 29)), True)
    assert c - o == int(3.5 * 3600)


def test_weekend_gap_uses_friday_close_and_monday_0100():
    fri, mon = 19002 - 3, 19002                                    # server Friday 07.01.2022, Monday 10.01.2022
    m5f = _m5([(1.1000, 1.1001, 1.0999, 1.1000)] * 12, fri * 86400 + 22 * 3600)
    mon_bars = [(1.0980, 1.0981, 1.0979, 1.0980)] * 12 + [(1.0980, 1.1005, 1.0980, 1.1002)] + \
               [(1.1002, 1.1003, 1.1001, 1.1002)] * 30
    m5 = np.concatenate([m5f, _m5(mon_bars, mon * 86400)])
    to_date = lambda n: date.fromordinal(date(1970, 1, 1).toordinal() + n)
    rows = run_weekend("EURUSD", m5, FXC, to_date(fri), to_date(mon))
    assert len(rows) == 1 and rows["dir"][0] == 1 and rows["exit_type"][0] == TARGET
    assert rows["gap_bp"][0] == pytest.approx((1.0980 - 1.1000) / 1.1000 * 1e4)
