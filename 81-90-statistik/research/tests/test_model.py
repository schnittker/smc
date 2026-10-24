import numpy as np
import pytest

from stm.model import garch_fit, garch_forecast, hmm_filter, hmm_fit, targets


def test_hmm_separates_calm_and_wild():
    rng = np.random.default_rng(0)
    x = np.r_[0.005 * rng.standard_normal(400), 0.02 * rng.standard_normal(400), 0.005 * rng.standard_normal(400)]
    prm = hmm_fit(x, 50)
    assert prm[3][0] < prm[3][1] and prm[3][1] / prm[3][0] > 8
    p = hmm_filter(x, prm)
    assert p[300] > 0.9 and p[600] < 0.1 and p[1100] > 0.9


def test_garch_recovers_persistence():
    rng = np.random.default_rng(1)
    w, a, b = 1e-6, 0.08, 0.90
    n = 3000
    h, x = np.empty(n), np.empty(n)
    h[0] = w / (1 - a - b)
    for t in range(n):
        if t:
            h[t] = w + a * x[t - 1] ** 2 + b * h[t - 1]
        x[t] = np.sqrt(h[t]) * rng.standard_normal()
    wf, af, bf = garch_fit(x)
    assert af + bf == pytest.approx(0.98, abs=0.03)
    f = garch_forecast(x, (wf, af, bf), x.var())
    assert np.corrcoef(f[:-1], h[1:])[0, 1] > 0.8


def _px(p, start_day):
    n = len(p)
    return {"day": start_day + np.arange(n) + 2 * (np.arange(n) // 5), "p_mark": np.asarray(p, float),
            "exact": np.ones(n, bool)}


def test_gold_months():
    days0 = (np.datetime64("2015-01-05") - np.datetime64("1970-01-01")).astype(int)
    px = _px(1000 + np.cumsum(np.ones(400)), days0)
    t = targets("ST-GOLD", px, 2015, 2015)
    on = sorted(d for d, w in t.items() if w > 0)
    off = sorted(d for d, w in t.items() if w == 0)
    mon = lambda d: str(np.datetime64(int(d), "D"))[:7]
    assert [mon(d) for d in on] == ["2015-08", "2015-10"] and [mon(d) for d in off] == ["2015-09", "2015-11"]
