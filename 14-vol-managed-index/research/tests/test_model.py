import numpy as np
import pytest

from smc.strategy_h import SPECS, CfdSpec
from smc.swaps import RateTable
from volm.model import CAP, TARGET, run_model_v, targets_mm, targets_vol

SPEC = CfdSpec(**{**SPECS["SPXUSD"].__dict__, "rel_spread": 1e-4})
RATES = RateTable.constant({"USD": 0.05})


def _px(daily_sd=0.01, n=400, start_day=19723, seed=0):
    """Weekday series from 2024-01-01 (day 19723) with i.i.d. log returns."""
    days = np.array([d for d in range(start_day, start_day + int(n * 1.5)) if (d + 3) % 7 < 5][:n])
    r = np.random.default_rng(seed).normal(0, daily_sd, n)
    p = 5000 * np.exp(np.cumsum(r))
    return {"day": days, "p_sig": p, "p_mark": p, "exact": np.ones(n, bool), "lo": p * 0.999, "hi": p * 1.001}


def test_vol_target_scales_inverse_to_volatility():
    lo, hi = targets_vol(_px(0.005)), targets_vol(_px(0.02))
    assert np.median(list(lo.values())) == pytest.approx(TARGET / (0.005 * np.sqrt(261)), rel=0.25)
    assert np.median(list(hi.values())) == pytest.approx(TARGET / (0.02 * np.sqrt(261)), rel=0.25)
    assert max(targets_vol(_px(0.001)).values()) == CAP


def test_vol_target_uses_only_past_returns():
    px = _px()
    t = targets_vol(px)
    k = 100
    px2 = {key: v.copy() for key, v in px.items()}
    px2["p_sig"][k + 1:] *= 1.5
    assert targets_vol(px2)[int(px["day"][k])] == t[int(px["day"][k])]


def test_mm_monthly_on_first_trading_day():
    px = _px(0.01)
    t = targets_mm(px)
    dates = [str(np.datetime64(d, "D")) for d in sorted(t)]
    assert dates[0] == "2024-02-01" and dates[1] == "2024-03-01" and all(x.endswith(("-01", "-02", "-03")) for x in dates)
    assert np.median(list(t.values())) == pytest.approx(TARGET ** 2 / (0.01 ** 2 * 252), rel=0.4)


def test_run_model_v_swaps_and_costs_sign():
    px = _px(0.01)
    rows = run_model_v("V-VOL", SPEC, px, RATES)
    held = rows["w"] > 0
    assert held.any() and (rows["swap"][held] < 0).all() and (rows["trade_cost"] >= 0).all()
    const = run_model_v("KONSTANT", SPEC, px, RATES)
    assert (const["w"][1:] == 1.0).all() and const["trade_cost"][1:].sum() == 0.0
