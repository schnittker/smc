from datetime import date

import numpy as np
import pytest

from dbo.model import Costs
from smc.costs import effective_spread, slippage_price
from smc.data.bars import BAR_DTYPE
from smc.swaps import RateTable
from smc.timez import server_to_utc
from chart.engine import TIME
from ll.model import load_dgs10, run_aj, yield_sign

N = lambda d: (d - date(1970, 1, 1)).days


def test_load_dgs10_skips_missing(tmp_path):
    p = tmp_path / "d.csv"
    p.write_text("observation_date,DGS10\n2020-01-02,1.88\n2020-01-03,\n2020-01-06,1.81\n")
    d, y = load_dgs10(p)
    assert list(d) == [N(date(2020, 1, 2)), N(date(2020, 1, 6))] and list(y) == [1.88, 1.81]


def test_yield_sign_uses_only_observations_before_the_day():
    y_days = np.array([N(date(2020, 1, 2)), N(date(2020, 1, 3)), N(date(2020, 1, 6))])
    y = np.array([1.80, 1.90, 1.70])
    days = np.array([N(date(2020, 1, 3)), N(date(2020, 1, 6)), N(date(2020, 1, 7))])
    assert list(yield_sign(days, y_days, y, 1)) == [0, 1, -1]


def _h1(closes, t0):
    rows = []
    for j, c in enumerate(closes):
        ts = t0 + 3600 * j
        rows.append((int(server_to_utc(ts)), ts, c, c * 1.0005, c * 0.9995, c, 60))
    return np.array(rows, dtype=BAR_DTYPE)


def test_aj_trades_after_big_us500_move():
    t0 = N(date(2019, 3, 4)) * 86400
    rng = np.random.default_rng(0)
    spx = 3000 * np.exp(np.cumsum(0.001 * rng.standard_normal(600)))
    spx[550:] *= 1.01                                                   # +1 % jump in bar 550 (~10 sigma)
    aud = np.full(600, 80.0)
    r = run_aj(_h1(aud, t0), _h1(spx, t0), Costs("fx", "AUDJPY"), RateTable.constant({"AUD": 0.0, "JPY": 0.0}), 0,
               10 ** 6)
    t = r[r["entry_day"] >= 0]
    assert len(t) >= 1 and (t["dir"] == 1).any() and t["exit_type"][-1] == TIME and t["bars"][-1] == 3
