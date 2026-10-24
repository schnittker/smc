import numpy as np

from smc.swaps import RateTable
from dmom.model import ASSETS, LOOKBACK, schedule


def _pxs(drifts, n=400):
    days = np.array([d for d in range(16436, 16436 + 2 * n) if (d + 3) % 7 < 5][:n])   # from 2015-01-01
    out = {}
    for a, mu in zip(ASSETS, drifts):
        p = 100 * np.exp(mu * np.arange(n) + 0.001 * np.sin(np.arange(n)))
        out[a] = {"day": days, "p_sig": p, "p_mark": p, "exact": np.ones(n, bool)}
    return out


def test_top1_picks_strongest_above_hurdle():
    drifts = [0.0002, 0.0008, 0.0, -0.0001, 0.0004, 0.0, 0.0001, 0.0006]
    t, log = schedule(_pxs(drifts), RateTable.constant({"USD": 0.02}), 1)
    assert log and all(c == ["NSXUSD"] for _, c in log)
    d = log[0][0]
    assert t["NSXUSD"][d] > 0 and all(t[a][d] == 0.0 for a in ASSETS if a != "NSXUSD")


def test_cash_when_below_hurdle_and_top2():
    drifts = [0.0001] * 8
    _, log = schedule(_pxs(drifts), RateTable.constant({"USD": 0.10}), 2)
    assert all(c == [] for _, c in log)                       # ~2.5 % p. a. < 10 % hurdle
    drifts = [0.0002, 0.0008, 0.0, -0.0001, 0.0004, 0.0, 0.0001, 0.0006]
    _, log2 = schedule(_pxs(drifts), RateTable.constant({"USD": 0.0}), 2)
    assert log2[0][1] == ["NSXUSD", "XAUUSD"]
    assert LOOKBACK == 252
