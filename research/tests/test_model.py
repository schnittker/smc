from calendar import timegm
from datetime import date

import numpy as np
import pytest

from smc import timez
from smc.costs import pip_size
from smc.data.bars import resample
from smc.data.histdata import M1_DTYPE
from smc.strategy_f import run_model_f, window_times
from mer import events
from mer.model import Market, foreign_dir, index_returns, price_asof, run_model_m, run_reversal


def _bars(price_fn, start, days):
    """M1 bars for `days` consecutive UTC days from `start`, weekends removed, resampled to M5 and H1."""
    t0 = timegm(start)
    t = t0 + 60 * np.arange(days * 1440)
    wd = (t // timez.DAY + 3) % 7
    t = t[wd < 5]
    c = price_fn(t)
    o = np.r_[c[0], c[:-1]]
    m1 = np.empty(len(t), M1_DTYPE)
    m1["t"], m1["o"], m1["c"] = t, o, c
    m1["h"], m1["l"] = np.maximum(o, c) + 0.5e-4, np.minimum(o, c) - 0.5e-4
    return resample(m1, "M5"), resample(m1, "H1")


def _wave(scale, period_h=7.3, base=1.10):
    return lambda t: base * (1 + scale * np.sin(2 * np.pi * t / (period_h * 3600)) + 1e-9 * (t - t[0]) / 60)


def test_trade_reproduces_model_f():
    """Same mechanics as model F: identical fills, results and stops for its W3 window."""
    m5, h1 = _bars(_wave(0.004), (2026, 1, 5, 0, 0, 0), 12)
    rows = run_model_f("EURUSD", m5, h1, windows=(3,))
    assert len(rows) > 5 and rows["stopped"].any() and (~rows["stopped"]).any()
    mk = Market("EURUSD", m5, h1)
    start, end = window_times(rows["fx_day"])[3]
    for r, a, b in zip(rows, start, end):
        f = mk.trade(int(a), int(b), int(r["dir"]))
        assert f is not None
        assert (f.entry, f.exit, f.stopped, f.t_exit) == (r["entry"], r["exit"], r["stopped"], r["t_exit"])
        assert f.net_bp == pytest.approx(r["net_bp"], abs=1e-12)
        assert f.cost_bp == pytest.approx(r["cost_bp"], abs=1e-12)
        assert f.mae_bp == pytest.approx(r["mae_bp"], abs=1e-12)


def test_fix_exit_slippage_is_charged():
    m5, h1 = _bars(_wave(0.0), (2026, 1, 5, 0, 0, 0), 5)
    mk = Market("EURUSD", m5, h1)
    day = events.day_number(date(2026, 1, 8))
    a, b = int(events.london_utc(day, 14, 55)), int(events.london_utc(day, 16, 0))
    f1, f5 = mk.trade(a, b, 1), mk.trade(a, b, 1, exit_slip=0.5 * pip_size("EURUSD"))
    assert f5.net_bp == pytest.approx(f1.net_bp - 0.4e-4 / f1.entry * 1e4, rel=1e-3)
    assert f5.cost_bp > f1.cost_bp


def test_price_asof_uses_only_closed_bars_and_max_age():
    m5, _ = _bars(lambda t: 1.0 + (t - t[0]) / 1e9, (2026, 1, 5, 0, 0, 0), 3)
    t = int(m5["t"][100]) + 300                      # bar 100 closes exactly now
    assert price_asof(m5, t) == m5["c"][100]
    assert price_asof(m5, t + 299) == m5["c"][100]   # bar 101 still open
    assert np.isnan(price_asof(m5, int(m5["t"][0])))  # nothing closed yet
    assert np.isnan(price_asof(m5, int(m5["t"][-1]) + 300 + 7 * 3600))


def test_index_returns_between_signal_times():
    m5, _ = _bars(lambda t: np.exp((t - t[0]) / 1e7), (2026, 1, 5, 0, 0, 0), 4)
    ts = np.array([m5["t"][50] + 300, m5["t"][400] + 300])
    r = index_returns(m5, ts)
    assert np.isnan(r[0]) and r[1] == pytest.approx(np.log(m5["c"][400] / m5["c"][50]))


def test_foreign_dir():
    assert foreign_dir("EURUSD") == 1 and foreign_dir("AUDUSD") == 1 and foreign_dir("USDJPY") == -1


def _month_end_market():
    """FX, US index and foreign index around the month ends Jan-Apr 2026."""
    start, n = (2026, 1, 26, 0, 0, 0), 100
    fx = _bars(_wave(0.002), start, n)
    us = _bars(lambda t: 5000 * np.exp(1e-9 * (t - t[0])), start, n)[0]            # rises
    fo = _bars(lambda t: 8000 * np.exp(-1e-9 * (t - t[0])), start, n)[0]           # falls
    days = events.event_days((2026, 1), (2026, 4))
    return fx, us, fo, days


@pytest.mark.parametrize("symbol", ["EURUSD", "USDJPY"])
def test_direction_follows_hedging_logic(symbol):
    """US equities beat the foreign market -> long the foreign currency (short USDJPY)."""
    (m5, h1), us, fo, days = _month_end_market()
    rows = run_model_m(symbol, Market(symbol, m5, h1), us, fo, days, "M-1H")
    assert len(rows) == 3                                   # first month has no previous signal
    assert (rows["x"] > 0).all() and (rows["rel_eq_pct"] < 0).all()
    assert (rows["dir"] == foreign_dir(symbol)).all()
    rows_r = run_model_m(symbol, Market(symbol, m5, h1), fo, us, days, "M-1H")
    assert (rows_r["dir"] == -foreign_dir(symbol)).all()


def test_entry_and_exit_times():
    (m5, h1), us, fo, days = _month_end_market()
    for v, (hi, mi) in (("M-1H", (14, 55)), ("M-DAY", (8, 0))):
        rows = run_model_m("EURUSD", Market("EURUSD", m5, h1), us, fo, days, v)
        assert (rows["t_entry"] == events.london_utc(rows["event_day"], hi, mi)).all()
        ok = ~rows["stopped"]
        assert (rows["t_exit"][ok] == events.london_utc(rows["event_day"][ok], 16, 0)).all()


def test_signal_ignores_data_after_signal_time():
    """Changing index prices after the signal time of the last event leaves its signal unchanged."""
    (m5, h1), us, fo, days = _month_end_market()
    base = run_model_m("EURUSD", Market("EURUSD", m5, h1), us, fo, days, "M-1H")
    cut = int(events.london_utc(days[-1], 14, 55))
    us2 = us.copy()
    late = us2["t"] + 300 > cut
    us2["c"][late] *= 0.5
    alt = run_model_m("EURUSD", Market("EURUSD", m5, h1), us2, fo, days, "M-1H")
    assert np.array_equal(base["x"], alt["x"]) and np.array_equal(base["dir"], alt["dir"])


def test_reversal_is_opposite_and_ends_next_business_day():
    (m5, h1), us, fo, days = _month_end_market()
    mk = Market("EURUSD", m5, h1)
    main = run_model_m("EURUSD", mk, us, fo, days, "M-1H")
    rev = run_reversal("EURUSD", mk, us, fo, days, "M-1H")
    assert np.array_equal(rev["dir"], -main["dir"])
    nxt = [events.day_number(events.next_business_day(events.to_date(d))) for d in rev["event_day"]]
    ok = ~rev["stopped"]
    assert (rev["t_exit"][ok] == events.london_utc(np.array(nxt), 12, 0)[ok]).all()
