from datetime import date

import numpy as np
import pytest

from smc.costs import commission_price, effective_spread, slippage_price
from smc.data.bars import BAR_DTYPE
from dbo.model import (DAY, EOD, NONE, STOP, Costs, holiday, levels, run_symbol, server_days, trade)

FXC = Costs("fx", "EURUSD")
SP, SL = effective_spread("EURUSD"), slippage_price("EURUSD")


def _bars(days: list[list[tuple]], day0: int = 19002) -> np.ndarray:
    """days[k] = list of (o, h, l, c) M5 bars starting at server midnight of day0 + k."""
    rows = []
    for k, bars in enumerate(days):
        for j, (o, h, l, c) in enumerate(bars):
            ts = (day0 + k) * DAY + 300 * j
            rows.append((ts - 7 * 3600, ts, o, h, l, c, 5))
    return np.array(rows, dtype=BAR_DTYPE)


def _flat_day(lo: float, hi: float, n: int = 288):
    return [(lo, hi, lo, lo)] + [(lo, lo, lo, lo)] * (n - 1)


def test_server_days_ohlc_and_min_bars():
    m5 = _bars([_flat_day(1.10, 1.12), [(1.0, 1.0, 1.0, 1.0)] * 5, _flat_day(1.11, 1.13)])
    d1 = server_days(m5)
    assert list(d1["day"]) == [19002, 19004]                 # 5-bar stub dropped
    assert d1["h"][1] == 1.13 and d1["l"][1] == 1.11 and d1["o"][1] == 1.11


def test_levels_nr7_inside_lw():
    rng = [10, 9, 8, 7, 6, 5, 4, 8, 3]
    d1 = {"day": np.arange(9), "o": np.full(9, 100.0), "h": 100 + np.array(rng, float), "l": np.full(9, 100.0)}
    up, dn = levels("T-NR7", d1)
    assert np.isnan(up[6]) and up[7] == 104 and np.isnan(up[8])    # bar 6 is the NR7 -> trade on 7
    d1i = {"day": np.arange(3), "o": np.zeros(3), "h": np.array([10.0, 9.0, 12.0]), "l": np.array([0.0, 1.0, 0.0])}
    up, dn = levels("T-INSIDE", d1i)
    assert up[2] == 9.0 and dn[2] == 1.0 and np.isnan(up[1])
    up, dn = levels("T-LW", {"day": np.arange(2), "o": np.array([0.0, 50.0]), "h": np.array([10.0, 60.0]),
                             "l": np.array([0.0, 45.0])})
    assert up[1] == 55.0 and dn[1] == 45.0


def test_long_breakout_to_close():
    bars = [(1.1000, 1.1005, 1.0995, 1.1000)] * 10 + [(1.1000, 1.1030, 1.1000, 1.1030)] + \
           [(1.1030, 1.1040, 1.1025, 1.1035)] * 277
    m5 = _bars([bars])
    direction, ex, entry, risk, px, _ = trade(m5, 0, len(m5), 1.1020, 1.0980, FXC)
    assert direction == 1 and ex == EOD
    assert entry == pytest.approx(1.1020 + SL) and risk == pytest.approx(1.1020 + SL - 1.0980)
    assert px == pytest.approx(1.1035 - SL)


def test_gap_fills_at_open_and_short_stopped():
    bars = [(1.0970, 1.0975, 1.0960, 1.0965)] * 5 + [(1.0990, 1.1030, 1.0990, 1.1025)] + \
           [(1.1025, 1.1025, 1.1025, 1.1025)] * 282
    m5 = _bars([bars])
    direction, ex, entry, risk, px, _ = trade(m5, 0, len(m5), 1.1020, 1.0980, FXC)
    assert direction == -1 and entry == pytest.approx(1.0970 - SL)          # gap below the level: open
    assert ex == STOP and px == pytest.approx(1.1020 + SL)                  # ask reaches the upper level


def test_entry_and_stop_same_bar_is_stop():
    bars = [(1.1000, 1.1030, 1.0970, 1.1000)] + [(1.1, 1.1, 1.1, 1.1)] * 287
    direction, ex, entry, risk, px, _ = trade(_bars([bars]), 0, 288, 1.1020, 1.0980, FXC)
    assert ex == STOP and direction * (px - entry) == pytest.approx(-risk - SL)     # stop fill pays slippage


def test_no_orders_in_last_hour():
    bars = [(1.1, 1.1, 1.1, 1.1)] * 276 + [(1.1, 1.1050, 1.1, 1.1)] * 12        # breakout only after 23:00
    assert trade(_bars([bars]), 0, 288, 1.1020, 1.0980, FXC) is None


def test_run_symbol_r_and_flat_rows():
    day0 = (date(2019, 3, 4) - date(1970, 1, 1)).days
    wide = [(1.10, 1.1010, 1.0990, 1.10)] * 288
    calm = [(1.10, 1.1002, 1.0998, 1.10)] * 288
    brk = [(1.10, 1.10, 1.10, 1.10)] * 10 + [(1.10, 1.1030, 1.10, 1.1030)] * 278
    m5 = _bars([wide, calm, brk], day0)
    rows = run_symbol("T-LW", m5, FXC, 0, 10 ** 9)
    assert list(rows["exit_type"]) == [NONE, EOD]
    r = rows[1]
    entry = 1.10 + 0.5 * 0.0004 + SL
    move = 1.1030 - SL - entry - commission_price("EURUSD", entry)
    assert r["r_net"] == pytest.approx(move / (entry - (1.10 - 0.0002)))
    notional = min(0.0025 / ((entry - 1.0998) / entry), 10.0)
    assert r["notional"] == pytest.approx(notional) and r["net_bp"] == pytest.approx(notional * move / entry * 1e4)


def test_holiday_window():
    assert holiday((date(2019, 12, 24) - date(1970, 1, 1)).days)
    assert holiday((date(2020, 1, 1) - date(1970, 1, 1)).days)
    assert not holiday((date(2020, 1, 2) - date(1970, 1, 1)).days)


def test_saturday_stub_is_not_a_d1_bar():
    day0 = (date(2019, 3, 8) - date(1970, 1, 1)).days                          # a Friday
    m5 = _bars([_flat_day(1.10, 1.12), [(1.1, 1.1, 1.1, 1.1)] * 12, _flat_day(1.10, 1.11), _flat_day(1.10, 1.11)],
               day0)
    assert list(server_days(m5)["day"]) == [day0, day0 + 3]                      # Saturday stub and Sunday dropped
