from datetime import date, datetime
from zoneinfo import ZoneInfo

import numpy as np
import pytest

from smc import timez
from smc.data.bars import resample
from smc.data.histdata import M1_DTYPE
from smc.strategy_h import SPECS, CfdSpec
from smc.swaps import RateTable
from fomc.model import Index, ny_utc
from ovn.model import day_triples, dn, run_model_n

RATES = RateTable.constant({"USD": 0.05})
SPEC = CfdSpec(**{**SPECS["SPXUSD"].__dict__, "rel_spread": 1e-4})
SWAP_NIGHT = (0.018 - 0.05 - 0.025) / 365 * 1e4


def _index(price_fn, start=(2023, 6, 1), days=60):
    t0 = int(datetime(*start, tzinfo=ZoneInfo("UTC")).timestamp())
    t = t0 + 60 * np.arange(days * 1440)
    t = t[(t // timez.DAY + 3) % 7 < 5]
    c = price_fn(t)
    m1 = np.empty(len(t), M1_DTYPE)
    m1["t"], m1["c"], m1["o"] = t, c, c
    m1["h"], m1["l"] = c + 0.1, c - 0.1
    return Index(SPEC, resample(m1, "M5"), resample(m1, "D1"))


def test_day_triples_skip_weekend_and_holiday():
    tr = day_triples(date(2023, 7, 5), date(2023, 7, 10))
    assert tr[0] == (date(2023, 6, 30), date(2023, 7, 3), date(2023, 7, 5))      # 4 July closed
    assert (date(2023, 7, 6), date(2023, 7, 7), date(2023, 7, 10)) in tr


def test_night_over_weekend_pays_weekend_swap():
    idx = _index(lambda t: 4000.0 + 0 * t)
    r = run_model_n("N-NACHT", idx, date(2023, 7, 10), date(2023, 7, 10), RATES)[0]
    assert r["t_entry"] == ny_utc(dn(date(2023, 7, 7)), 16, 0) and r["t_exit"] == ny_utc(dn(date(2023, 7, 10)), 9, 30)
    assert r["swap_bp"] == pytest.approx(SWAP_NIGHT)          # Friday rollover counts one night (weekend on Wed)
    r = run_model_n("N-NACHT", idx, date(2023, 7, 13), date(2023, 7, 13), RATES)[0]
    assert r["swap_bp"] == pytest.approx(3 * SWAP_NIGHT)      # Wednesday rollover counts three


def test_eu_window_no_swap_and_gain():
    d = date(2023, 7, 12)
    t_in = int(ny_utc(dn(d), 2, 0))
    idx = _index(lambda t: 4000.0 + np.where(t >= t_in + 1800, 4.0, 0.0))
    r = run_model_n("N-EU", idx, d, d, RATES)[0]
    assert r["t_entry"] == t_in and r["t_exit"] == ny_utc(dn(d), 3, 0)
    assert r["swap_bp"] == 0.0 and r["gross_bp"] == pytest.approx(10.0, abs=0.01)


def test_eu_down_only_after_down_close():
    d = date(2023, 7, 12)                                     # p = 11.07., pp = 10.07.
    c_pp = int(ny_utc(dn(date(2023, 7, 10)), 16, 0))
    c_p = int(ny_utc(dn(date(2023, 7, 11)), 16, 0))
    up = _index(lambda t: 4000.0 + np.where(t >= c_pp + 3600, 10.0, 0.0))     # close p above close pp
    down = _index(lambda t: 4000.0 - np.where(t >= c_pp + 3600, 10.0, 0.0))
    assert len(run_model_n("N-EU-DOWN", up, d, d, RATES)) == 0
    assert len(run_model_n("N-EU-DOWN", down, d, d, RATES)) == 1
    assert len(run_model_n("N-EU", up, d, d, RATES, condition="up")) == 1
    assert c_p > c_pp
