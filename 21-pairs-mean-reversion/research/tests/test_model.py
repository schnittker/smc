import numpy as np
import pytest

from smc.swaps import RateTable
from pmr.model import run_model_p, targets, trades, zscore

RATES = RateTable.constant({"AUD": 0.04, "NZD": 0.05, "EUR": 0.02, "CHF": 0.0})


def _px(p):
    n = len(p)
    days = np.array([d for d in range(16000, 16000 + 2 * n) if (d + 3) % 7 < 5][:n])
    p = np.asarray(p, float)
    return {"day": days, "p_sig": p, "p_mark": p, "exact": np.ones(n, bool), "lo": p * 0.999, "hi": p * 1.001}


def test_zscore_known():
    p = np.exp(np.r_[np.zeros(59), [1.0]])
    z = zscore(p)
    x = np.r_[np.zeros(59), [1.0]]
    assert z[59] == pytest.approx((1.0 - x.mean()) / x.std(ddof=1))
    assert np.isnan(z[58])


def test_short_on_spike_and_exit_at_mean():
    base = 1.08 * (1 + 0.001 * np.sin(np.arange(120) / 3.0))    # calm oscillation, |z| < 2
    base[80:84] *= 1.03                                      # spike -> z >> 2
    base[84:] = 1.08                                         # back to the mean
    t = targets(_px(base))
    days = sorted(t)
    assert t[days[0]] < 0 and t[days[1]] == 0.0


def test_trades_long_and_short_episodes():
    rows = np.zeros(8, dtype=[("day", "i8"), ("w", "f8"), ("net", "f8")])
    rows["day"] = np.arange(8)
    rows["w"] = [0, -1, -1, 0, 1, 1, 1, 0]
    rows["net"] = [0, 0.1, 0.2, 0.3, 0.0, -0.1, 0.05, 0.02]
    tr = trades(rows)
    assert [(d, h) for d, h, _ in tr] == [(1, 2), (4, 3)]
    assert tr[0][2] == pytest.approx(0.1 + 0.2 + 0.3) and tr[1][2] == pytest.approx(0.0 - 0.1 + 0.05 + 0.02)


def test_run_model_p_produces_rows():
    rng = np.random.default_rng(3)
    rows = run_model_p("P-AUDNZD", _px(1.08 * np.exp(np.cumsum(rng.normal(0, 0.004, 400)))), RATES)
    assert len(rows) == 400 and (rows["w"] != 0).any()
