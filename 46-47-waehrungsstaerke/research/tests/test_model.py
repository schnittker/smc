import numpy as np
import pytest

from dbo.model import Costs
from smc.costs import effective_spread, slippage_price
from smc.data.bars import BAR_DTYPE
from smc.timez import server_to_utc
from cst.model import CCYS, STOP, TIME, USD_PAIRS, basket_z, pair_for, strength, trade

FXC = Costs("fx", "EURUSD")
SP, SL = effective_spread("EURUSD"), slippage_price("EURUSD")
DAY0 = 19002


def _bars(ohlc, ts0=DAY0 * 86400, step=3600):
    rows = [(int(server_to_utc(ts0 + step * j)), ts0 + step * j, o, h, l, c, 60) for j, (o, h, l, c) in enumerate(ohlc)]
    return np.array(rows, dtype=BAR_DTYPE)


def test_pair_for():
    assert pair_for("EUR", "JPY") == ("EURJPY", 1) and pair_for("JPY", "EUR") == ("EURJPY", -1)
    assert pair_for("USD", "CAD") == ("USDCAD", 1) and pair_for("CAD", "USD") == ("USDCAD", -1)
    assert pair_for("EUR", "GBP") == (None, 0)


def test_strength_signs_and_demeaning():
    flat = {s: _bars([(1.0,) * 4] * 3) for s in USD_PAIRS.values()}
    flat["EURUSD"] = _bars([(1.0,) * 4, (1.0,) * 4, (1.01,) * 4])          # EUR up 1 %
    flat["USDJPY"] = _bars([(100.0,) * 4, (100.0,) * 4, (101.0,) * 4])     # JPY down 1 %
    t = flat["EURUSD"]["t"]
    st = strength(flat, int(t[0]), int(t[2]))
    assert CCYS[int(np.argmax(st))] == "EUR" and CCYS[int(np.argmin(st))] == "JPY"
    assert st.sum() == pytest.approx(0.0, abs=1e-12)


def test_trade_time_exit_and_stop():
    bars = _bars([(1.1000, 1.1005, 1.0995, 1.1000)] * 6)
    ex, j, entry, px, _, _ = trade(bars, 1, 1, 0.0020, FXC, exit_bar=4)
    assert ex == TIME and j == 3 and px == pytest.approx(1.1000 - SL) and entry == pytest.approx(1.1000 + SP + SL)
    bars = _bars([(1.1000,) * 4, (1.1000, 1.1030, 1.0999, 1.1020), (1.102,) * 4])
    ex, j, entry, px, _, _ = trade(bars, 1, -1, 0.0020, FXC, exit_bar=2)
    assert ex == STOP and px == pytest.approx(entry + 0.0020 + SL)


def test_basket_z_flags_idiosyncratic_move():
    rng = np.random.default_rng(1)
    n = 700
    common = 0.0005 * rng.standard_normal(n).cumsum()                     # USD factor moves all pairs alike
    usd = {}
    for c, sym in USD_PAIRS.items():
        own = 0.0002 * rng.standard_normal(n).cumsum()
        if c == "EUR":
            own[-30:] += np.linspace(0, 0.02, 30)                         # EUR-specific jump at the end
        p_c = common + own                                                 # ln price of c in USD
        px = np.exp(p_c) if sym.endswith("USD") else np.exp(-p_c)
        usd[sym] = _bars([(x,) * 4 for x in px])
    t, z = basket_z(usd)
    assert len(t) == n and np.isnan(z["EUR"][Z_IDX := 24 + 498]) and np.isfinite(z["EUR"][Z_IDX + 1])
    assert z["EUR"][-1] > 3 and abs(z["GBP"][-1]) < 3
