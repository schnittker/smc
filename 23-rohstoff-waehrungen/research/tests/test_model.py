import numpy as np

from cfx.model import targets


def _px(p, days):
    p = np.asarray(p, float)
    return {"day": np.asarray(days), "p_sig": p, "p_mark": p, "exact": np.ones(len(p), bool)}


def test_oil_up_means_short_usdcad_same_day():
    n = 100
    days = np.arange(n)
    oil = 80 * np.exp(np.cumsum(np.r_[0, np.where(np.arange(1, n) % 2 == 0, 0.01, -0.01)]))
    fx = 1.35 * np.exp(np.random.default_rng(0).normal(0, 0.004, n).cumsum())
    t = targets(_px(oil, days), _px(fx, days), -1)
    d_up = [d for d in t if d % 2 == 0]
    d_dn = [d for d in t if d % 2 == 1]
    assert d_up and all(t[d] < 0 for d in d_up) and all(t[d] > 0 for d in d_dn)


def test_missing_commodity_day_keeps_position():
    days = np.arange(80)
    oil_days = days[days != 70]
    oil = 80 * np.exp(np.linspace(0, 0.1, len(oil_days)))
    fx = np.full(80, 1.35) * np.exp(np.random.default_rng(1).normal(0, 0.004, 80).cumsum())
    t = targets(_px(oil, oil_days), _px(fx, days), -1)
    assert 70 not in t and 71 in t
