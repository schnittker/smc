import numpy as np
import pytest

from smc.report import clustered_diff, holm
from smc.study import first_passage, forward


def test_first_passage_target_stop_and_same_bar_rule():
    o = np.array([1.0, 1.0, 1.0, 1.0])
    h = np.array([1.0, 1.5, 2.2, 1.0])
    l = np.array([1.0, 0.9, 0.95, 1.0])
    c = np.array([1.0, 1.2, 2.0, 1.0])
    unit = np.array([0.5])
    # long from bar 0 (entry 1.0): target 2.0 hit at bar 2, stop 0.5 never -> +2R
    assert first_passage(o, h, l, c, np.array([0]), np.array([1]), unit, 2.0, 1.0, horizon=4)[0] == 2.0
    # short from bar 0: stop at 1.5 hit at bar 1 (high 1.5) -> -1R
    assert first_passage(o, h, l, c, np.array([0]), np.array([-1]), unit, 2.0, 1.0, horizon=4)[0] == -1.0
    # both levels inside the same bar -> counted as a loss
    h2 = np.array([3.5, 1.0, 1.0, 1.0]); l2 = np.array([-0.5, 1.0, 1.0, 1.0])
    assert first_passage(o, h2, l2, c, np.array([0]), np.array([1]), unit, 2.0, 1.0, horizon=4)[0] == -1.0


def test_first_passage_timeout_marks_to_market_and_short_series_is_nan():
    o = np.ones(5); h = np.ones(5) * 1.1; l = np.ones(5) * 0.95; c = np.array([1, 1, 1, 1, 1.05])
    r = first_passage(o, h, l, c, np.array([0, 3]), np.array([1, 1]), np.array([1.0, 1.0]), 2.0, 1.0, horizon=5)
    assert r[0] == pytest.approx(0.05) and np.isnan(r[1])


def test_forward_return_sign():
    o = np.array([1.0, 1.0, 1.0]); c = np.array([1.0, 1.1, 1.3])
    f = forward(o, c, np.array([0, 0]), np.array([1, -1]), np.array([0.1, 0.1]), 3)
    assert f == pytest.approx([3.0, -3.0])


def test_clustered_diff_detects_shift_and_not_noise():
    rng = np.random.default_rng(0)
    days = np.repeat(np.arange(400), 10)
    pb = rng.normal(0, 1, len(days))
    ev_same = rng.normal(0, 1, len(days))
    ev_shift = rng.normal(0.3, 1, len(days))
    d0, lo0, hi0, p0 = clustered_diff(ev_same, days, pb, days)
    d1, lo1, hi1, p1 = clustered_diff(ev_shift, days, pb, days)
    assert lo0 < 0 < hi0 and p0 > 0.01
    assert lo1 > 0 and p1 < 1e-6 and d1 == pytest.approx(0.3, abs=0.08)


def test_holm():
    adj = holm([0.01, 0.04, 0.03, float("nan")])
    assert adj[0] == pytest.approx(0.03) and adj[2] == pytest.approx(0.06) and adj[1] == pytest.approx(0.06)
    assert np.isnan(adj[3])
