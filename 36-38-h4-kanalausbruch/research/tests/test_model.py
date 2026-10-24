import numpy as np
import pytest

from dbo.model import Costs
from smc.costs import commission_price, effective_spread, slippage_price
from smc.data.bars import BAR_DTYPE
from smc.swaps import MARKUP, RateTable
from smc.timez import server_to_utc
from hkb.model import DAY, END, SIGNAL, STOP, atr, ema, run_symbol, signals, sma_std, swap_frac

FXC = Costs("fx", "EURUSD")
SP, SL = effective_spread("EURUSD"), slippage_price("EURUSD")
ZERO = RateTable.constant({"EUR": 0.0, "USD": 0.0})
DAY0 = 19002                                                     # a Monday


def _h4(ohlc: list[tuple]) -> np.ndarray:
    rows = []
    for j, (o, h, l, c) in enumerate(ohlc):
        ts = DAY0 * DAY + 14400 * j
        rows.append((int(server_to_utc(ts)), ts, o, h, l, c, 240))
    return np.array(rows, dtype=BAR_DTYPE)


def test_indicators():
    c = np.arange(1.0, 31.0)
    m, s = sma_std(c, 20)
    assert np.isnan(m[18]) and m[19] == pytest.approx(10.5) and s[19] == pytest.approx(np.std(np.arange(1, 21)))
    e = ema(np.r_[np.zeros(5), np.ones(5)], 3)
    assert np.isnan(e[1]) and e[5] == pytest.approx(0.5) and e[6] == pytest.approx(0.75)
    a = atr(np.full(5, 2.0), np.full(5, 1.0), np.full(5, 1.5), 3)
    assert np.isnan(a[1]) and a[2] == pytest.approx(1.0) and a[4] == pytest.approx(1.0)


def test_squeeze_breakout_signal():
    rng = np.random.default_rng(1)
    c = np.r_[1.10 + 0.01 * rng.standard_normal(200), 1.10 + 0.0002 * rng.standard_normal(30), 1.12]
    bars = _h4([(x, x + 0.0001, x - 0.0001, x) for x in c])
    entry, mid, _ = signals("K-BBSQ", bars)
    assert entry[-1] == 1 and not entry[150:200].any()


def test_keltner_needs_trend():
    c = np.r_[np.linspace(1.2, 1.0, 260), 1.0, 1.05]                  # spike up below the falling EMA200
    bars = _h4([(x, x + 0.001, x - 0.001, x) for x in c])
    entry, _, _ = signals("K-KELT", bars)
    assert entry[-1] == 0


def _run(prices, sig_bar, d=1):
    """Flat bars at 1.1000 with ATR 0.0010 (h - l), custom path afterwards; entry signal injected at sig_bar."""
    bars = _h4(prices)
    import hkb.model as km
    orig = km.signals

    def fake(variant, b):
        e, mid, a = orig("K-KELT", b)
        e[:] = 0
        e[sig_bar] = d
        return e, np.full(len(b), 1.1000), np.full(len(b), 0.0010)
    km.signals = fake
    try:
        return run_symbol("K-KELT", "EURUSD", bars, bars, FXC, ZERO, 0, 10 ** 6)
    finally:
        km.signals = orig


def test_long_exit_on_signal():
    path = [(1.1000, 1.1005, 1.0995, 1.1000)] * 5 + [(1.1000, 1.1012, 1.1000, 1.1010)] * 3 + \
           [(1.1010, 1.1010, 1.0990, 1.0995), (1.0990, 1.0990, 1.0990, 1.0990)]
    r = _run(path, 4)
    assert len(r) == 1 and r["exit_type"][0] == SIGNAL and r["dir"][0] == 1
    entry = 1.1000 + SP + SL
    px = 1.0990 - SL                                                   # open of the bar after the cross
    move = px - entry - commission_price("EURUSD", entry)
    swap = -MARKUP / 365 * entry                                       # one rollover (Monday night), zero rates
    assert r["r_net"][0] == pytest.approx((move + swap) / 0.0020)
    assert r["notional"][0] == pytest.approx(min(0.0025 / (0.0020 / entry), 10.0))


def test_short_stop_gap():
    path = [(1.1000, 1.1005, 1.0995, 1.1000)] * 5 + [(1.0995, 1.0995, 1.0990, 1.0992), (1.1030, 1.1035, 1.1030, 1.1030)]
    r = _run(path, 4, d=-1)
    entry = 1.0995 - SL                                                # open of the bar after the signal
    assert r["exit_type"][0] == STOP
    swap = -MARKUP / 365 * entry                                       # stopped in the bar after the Monday rollover
    assert r["r_net"][0] == pytest.approx((entry - (1.1030 + SP + SL) - commission_price("EURUSD", entry) + swap) / 0.0020)


def test_open_position_closed_at_end():
    path = [(1.1000, 1.1005, 1.0995, 1.1000)] * 5 + [(1.1000, 1.1012, 1.1000, 1.1010)] * 3
    r = _run(path, 4)
    assert r["exit_type"][0] == END


def test_swap_wednesday_triple():
    rates = RateTable.constant({"EUR": 0.03, "USD": 0.05})
    t0 = int(server_to_utc(DAY0 * DAY + 3600))                         # Monday 01:00 server
    f = swap_frac("EURUSD", 1, t0, t0 + 7 * DAY, rates, None)          # 5 rollovers Mon-Fri, Wednesday x3 = 7 nights
    assert f == pytest.approx(7 * (0.03 - 0.05 - MARKUP) / 365)
