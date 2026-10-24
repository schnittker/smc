from calendar import timegm
from datetime import datetime
from zoneinfo import ZoneInfo

import numpy as np
import pytest

from smc import timez
from smc.data.bars import resample
from smc.data.histdata import M1_DTYPE
from smc.strategy_f import run_model_f, trading_days, window_times

UTC, NY, TOKYO, FRANKFURT, LONDON = (ZoneInfo(z) for z in ("UTC", "America/New_York", "Asia/Tokyo",
                                                           "Europe/Berlin", "Europe/London"))


def _ts(y, m, d, hh, mm, tz):
    return int(datetime(y, m, d, hh, mm, tzinfo=tz).timestamp())


@pytest.mark.parametrize("date", [(2026, 1, 14), (2026, 7, 15), (2026, 3, 18), (2026, 10, 28)])
def test_window_times_follow_local_clocks(date):
    """Winter, summer, and both weeks in which US and EU summer time differ."""
    y, m, d = date
    day = timegm((y, m, d, 0, 0, 0)) // timez.DAY
    w = {k: (int(a[0]), int(b[0])) for k, (a, b) in window_times(np.array([day])).items()}
    prev = datetime(y, m, d, tzinfo=UTC).date().toordinal() - 1
    py, pm, pd_ = datetime.fromordinal(prev).timetuple()[:3]
    tokyo = _ts(y, m, d, 9, 55, TOKYO)
    ffm8 = _ts(y, m, d, 8, 0, FRANKFURT)
    assert w[1] == (_ts(py, pm, pd_, 17, 30, NY), tokyo)
    assert w[2] == (tokyo, ffm8)
    assert w[3] == (ffm8, _ts(y, m, d, 14, 15, FRANKFURT))
    assert w[4] == (_ts(y, m, d, 16, 0, LONDON), _ts(y, m, d, 16, 50, NY))


def test_trading_days_skip_christmas_to_new_year():
    t = np.array([timegm((2023, 12, x, 12, 0, 0)) for x in (21, 22, 27)] + [timegm((2024, 1, x, 12, 0, 0)) for x in (1, 2)])
    m5 = np.zeros(len(t), dtype=[("ts", "i8")])
    m5["ts"] = timez.utc_to_server(t)
    days = trading_days(m5)
    dates = np.asarray(days * timez.DAY, dtype="datetime64[s]").astype("datetime64[D]").astype(str).tolist()
    assert dates == ["2023-12-21", "2023-12-22", "2024-01-02"]


def _market(price_fn, start=(2026, 1, 12, 0, 0, 0), days=4, jumps_at_open=False):
    """M1 bars on server days Mon.. with prices from price_fn(utc seconds) and 0.5-pip wicks.
    jumps_at_open: every minute opens at its own price, so a jump shows up as a gap at the bar open."""
    srv0 = timegm(start)                      # server Monday 00:00
    t = np.concatenate([timez.server_to_utc(srv0 + k * timez.DAY + 60 * np.arange(1440)) for k in range(days)])
    c = price_fn(t)
    o = c.copy() if jumps_at_open else np.r_[c[0], c[:-1]]
    m1 = np.empty(len(t), M1_DTYPE)
    m1["t"], m1["o"], m1["c"] = t, o, c
    m1["h"], m1["l"] = np.maximum(o, c) + 0.5e-4, np.minimum(o, c) - 0.5e-4
    return resample(m1, "M5"), resample(m1, "H1")


TUE = timegm((2026, 1, 13, 0, 0, 0)) // timez.DAY


def test_flat_market_loses_exactly_the_costs():
    m5, h1 = _market(lambda t: np.full(len(t), 1.1))
    rows = run_model_f("EURUSD", m5, h1)
    rows = rows[rows["fx_day"] >= TUE]        # Monday lacks the 14 H1 bars for the stop's ATR
    assert len(rows) == 12 and (rows["window"] == 1).sum() == 3
    # spread 0.4 pip + 2 x 0.1 pip slippage + 0.5 pip commission = 1.1 pip = 1.0 bp at 1.1
    assert np.allclose(rows["cost_bp"], 1.1e-4 / 1.1 * 1e4)
    assert np.allclose(rows["net_bp"], -rows["cost_bp"])
    assert not rows["stopped"].any()
    # long USD = short EURUSD in W1/W3, long EURUSD in W2/W4
    assert (rows["dir"] == np.where(np.isin(rows["window"], (1, 3)), -1, 1)).all()


def test_no_w1_on_the_sunday_evening_session_and_no_w4_for_usdjpy():
    m5, h1 = _market(lambda t: np.full(len(t), 150.0), start=(2026, 1, 5, 0, 0, 0), days=8)
    rows = run_model_f("USDJPY", m5, h1)
    w1_days = rows["fx_day"][rows["window"] == 1]
    assert len(w1_days) and ((w1_days + 3) % 7 != 0).all()
    assert 4 not in rows["window"].tolist()
    assert np.allclose(rows["cost_bp"], -rows["net_bp"])


def test_usd_rally_before_the_tokyo_fix_is_earned():
    s1, e1 = (int(x[0]) for x in window_times(np.array([TUE]))[1])

    def path(t):   # EURUSD falls 20 pips during Tuesday's W1, flat otherwise
        return 1.1 - 20e-4 * np.clip((t - s1) / (e1 - s1), 0, 1)
    rows = run_model_f("EURUSD", *_market(path))
    w1 = rows[(rows["window"] == 1) & (rows["fx_day"] == TUE)][0]
    assert w1["net_bp"] == pytest.approx((20e-4 - 1.1e-4) / 1.1 * 1e4, abs=0.6)   # minus the bar-open lag


def test_emergency_stop_at_three_atr_and_gap_fill():
    wed = TUE + 1
    s3 = int(window_times(np.array([wed]))[3][0][0])

    def path(t):   # quiet market, then EURUSD jumps 300 pips one hour into Wednesday's W3 (short EURUSD)
        return 1.1 + np.where(t >= s3 + 3600, 300e-4, 0.0)
    for gap in (False, True):
        rows = run_model_f("EURUSD", *_market(path, jumps_at_open=gap))
        r = rows[(rows["window"] == 3) & (rows["fx_day"] == wed)][0]
        assert r["stopped"] and r["t_exit"] == s3 + 3600 + 300
        if gap:   # filled at the ask open after the jump
            assert r["net_bp"] == pytest.approx(-(300e-4 + 0.4e-4 + 0.2e-4 + 0.5e-4) / 1.1 * 1e4, abs=0.01)
        else:     # filled at the stop: 3 x ATR(H1) = 3 x 1 pip above the entry
            assert r["net_bp"] == pytest.approx(-(3e-4 + 0.2e-4 + 0.5e-4) / 1.1 * 1e4, abs=0.01)
        assert r["mae_bp"] < -250
