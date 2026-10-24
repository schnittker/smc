import numpy as np

from gsr.model import common_series, targets


def _px(p, days):
    p = np.asarray(p, float)
    return {"day": np.asarray(days), "p_sig": p, "p_mark": p, "exact": np.ones(len(p), bool)}


def test_common_series_aligns_days():
    g = _px([2000, 2010, 2020], [1, 2, 4])
    s = _px([25, 25, 26, 27], [1, 2, 3, 4])
    c = common_series(g, s)
    assert c["day"].tolist() == [1, 2, 4]
    assert np.allclose(c["q_sig"], np.log([2000 / 25, 2010 / 25, 2020 / 27]))


def test_short_ratio_on_spike_equal_notional_and_exit():
    n = 200
    days = np.arange(n)
    gold = 2000 * (1 + 0.002 * np.sin(np.arange(n) / 3.0))
    silver = np.full(n, 25.0)
    gold[120:124] *= 1.05                                     # ratio spike
    gold[124:] = 2000.0                                       # back to the mean
    t_g, t_s = targets(common_series(_px(gold, days), _px(silver, days)), 60)
    d = sorted(t_g)
    assert t_g[d[0]] < 0 and t_s[d[0]] == -t_g[d[0]]          # short gold, long silver, equal notional
    assert t_g[d[1]] == 0.0 and t_s[d[1]] == 0.0
