from datetime import date, datetime
from zoneinfo import ZoneInfo

import numpy as np
import pytest

from smc import timez
from smc.data.bars import resample
from smc.data.histdata import M1_DTYPE
from smc.strategy_h import SLIPPAGE_SPREADS, SPECS, CfdSpec
from smc.swaps import RateTable
from fomc.model import (EPOCH, Index, bar_at, load_dates, ny_utc, prev_weekday, run_model_p, window_bp)

NY = ZoneInfo("America/New_York")
RATES = RateTable.constant({"USD": 0.05})
SPEC = CfdSpec(**{**SPECS["SPXUSD"].__dict__, "rel_spread": 1e-4})


def dn(y, m, d):
    return (date(y, m, d) - EPOCH).days


def test_dates_file_scheduled_meetings_only():
    days = load_dates()
    years = np.array([(EPOCH.toordinal() + int(d)) for d in days])
    ds = [date.fromordinal(int(x)) for x in years]
    by_year = {y: sum(1 for d in ds if d.year == y) for y in range(2015, 2024)}
    assert by_year == {2015: 8, 2016: 8, 2017: 8, 2018: 8, 2019: 8, 2020: 7, 2021: 8, 2022: 8, 2023: 8}
    assert date(2020, 3, 15) not in ds and date(2020, 3, 18) not in ds and date(2020, 3, 3) not in ds
    assert date(2017, 2, 1) in ds and date(2020, 11, 5) in ds and date(2024, 11, 7) in ds
    assert all(d.weekday() in (2, 3) for d in ds)            # Wednesday, rarely Thursday


def test_prev_weekday_and_ny_times():
    assert prev_weekday(dn(2023, 12, 13)) == dn(2023, 12, 12)
    assert prev_weekday(dn(2026, 10, 26)) == dn(2026, 10, 23)    # Monday -> Friday
    for d in [(2023, 3, 22), (2023, 11, 1), (2024, 3, 20), (2023, 1, 31)]:
        assert int(ny_utc(dn(*d), 13, 55)) == int(datetime(*d, 13, 55, tzinfo=NY).timestamp())


def _index(price_fn, start=(2023, 1, 2), days=60):
    """24h M1 index bars Mon-Fri from price_fn(utc seconds)."""
    t0 = int(datetime(*start, tzinfo=ZoneInfo("UTC")).timestamp())
    t = t0 + 60 * np.arange(days * 1440)
    t = t[(t // timez.DAY + 3) % 7 < 5]
    c = price_fn(t)
    m1 = np.empty(len(t), M1_DTYPE)
    m1["t"], m1["c"], m1["o"] = t, c, np.r_[c[0], c[:-1]]
    m1["h"], m1["l"] = np.maximum(m1["o"], c) + 0.2, np.minimum(m1["o"], c) - 0.2
    return Index(SPEC, resample(m1, "M5"), resample(m1, "D1"))


def test_trade_costs_and_swap_one_night():
    idx = _index(lambda t: 4000.0 + 0 * t)
    day = dn(2023, 2, 1)                                     # Wednesday announcement
    rows = run_model_p("P-SPX", idx, np.array([day]), RATES)
    assert len(rows) == 1 and not rows["stopped"][0]
    r = rows[0]
    assert r["t_entry"] == ny_utc(dn(2023, 1, 31), 14, 0) and r["t_exit"] == ny_utc(day, 13, 55)
    spread_bp = 1.0
    swap_bp = (0.018 - 0.05 - 0.025) / 365 * 1e4                # one rollover (Tuesday)
    assert r["swap_bp"] == pytest.approx(swap_bp)
    assert r["net_bp"] == pytest.approx(-spread_bp * (1 + 2 * SLIPPAGE_SPREADS) + swap_bp, rel=1e-6)
    assert r["gross_bp"] == pytest.approx(0.0, abs=1e-9)
    assert r["cost_bp"] == pytest.approx(spread_bp * 1.5 - swap_bp, rel=1e-6)


def test_thursday_announcement_pays_triple_swap():
    idx = _index(lambda t: 4000.0 + 0 * t, start=(2023, 10, 2))
    r = run_model_p("P-SPX", idx, np.array([dn(2023, 11, 2)]), RATES)[0]    # Thursday -> Wednesday rollover
    assert r["swap_bp"] == pytest.approx(3 * (0.018 - 0.05 - 0.025) / 365 * 1e4)


def test_gain_measured_from_entry_to_exit_open():
    t_in = int(ny_utc(dn(2023, 1, 31), 14, 0))
    idx = _index(lambda t: 4000.0 + np.where(t >= t_in, (t - t_in) / 3600.0, 0.0))  # +1 point per hour
    r = run_model_p("P-SPX", idx, np.array([dn(2023, 2, 1)]), RATES)[0]
    hours = (r["t_exit"] - r["t_entry"]) / 3600
    assert r["gross_bp"] == pytest.approx(hours / 4000 * 1e4, rel=1e-3)


def test_emergency_stop_on_crash():
    t_in = int(ny_utc(dn(2023, 1, 31), 14, 0))
    idx = _index(lambda t: 4000.0 * (1 + 0.002 * np.sin(t / 7000.0)) - np.where(t >= t_in + 3600, 400.0, 0.0))
    r = run_model_p("P-SPX", idx, np.array([dn(2023, 2, 1)]), RATES)[0]
    k = int(np.searchsorted(idx.d1_close, t_in, side="right")) - 1
    ref = idx.m5["o"][bar_at(idx.m5, t_in)]
    stop_bp = 3 * idx.atr_d1[k] / ref * 1e4               # no gap at a bar open here: filled at the stop
    assert r["stopped"] and r["t_exit"] < ny_utc(dn(2023, 2, 1), 13, 55)
    assert -stop_bp - 3 < r["net_bp"] < -stop_bp


def test_missing_bar_skips_event_and_window_bp():
    idx = _index(lambda t: 4000.0 + (t - t[0]) / 1e5)
    t_in = int(ny_utc(dn(2023, 1, 31), 14, 0))
    idx.m5 = idx.m5[idx.m5["t"] != t_in]
    assert len(run_model_p("P-SPX", idx, np.array([dn(2023, 2, 1)]), RATES)) == 0
    assert bar_at(idx.m5, t_in) == -1 and np.isnan(window_bp(idx.m5, t_in, t_in + 3600))
