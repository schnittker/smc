from calendar import timegm

import numpy as np
import pytest

from smc.costs import cost_in_price
from smc.data.bars import resample
from smc.data.histdata import M1_DTYPE
from smc.engine.liquidity import POOL_DTYPE, SWING_EXT, SWING_INT
from smc.engine.zones import FVG, ZONE_DTYPE
from smc.pipeline import TFS, build_symbol
from smc.strategy_c import (CANCEL_STOP, CANCEL_TARGET, CANCEL_TREND, ENTRY_MARKET, EXIT_SL, EXIT_TIME,
                            EXIT_TP, EXPIRED, LMT, MKT, NO_DATA, TARGET_CAP, TARGET_MIN, TRADED, Inputs, Market,
                            Targets, pending_order, pick_zone, run_model_c, run_position)

# binary-exact numbers so that trigger boundaries can be tested without rounding noise
MK = Market(spread=0.25, raw_spread=0.125, tick=0.0625, slip=0.03125)


def bars(*rows):
    o, h, l, c = (np.array(x, float) for x in zip(*rows))
    return o, h, l, c


# ---- position ------------------------------------------------------------------------------
def test_long_target_is_ignored_in_fill_bar_and_needs_one_tick():
    o, h, l, c = bars((10, 12.5, 9.5, 10), (10, 12.0, 9.6, 10), (10, 12.0625, 9.6, 10), (10, 10, 10, 10))
    assert run_position(o, h, l, c, 0, 1, 9.0, 12.0, MK, max_bars=4) == (2, 12.0, EXIT_TP)


def test_long_stop_same_bar_gap_and_fill_bar():
    o, h, l, c = bars((10, 10.5, 9.5, 10), (10, 12.5, 8.9, 10), (10, 10, 10, 10))
    assert run_position(o, h, l, c, 0, 1, 9.0, 12.0, MK, max_bars=3) == (1, 8.96875, EXIT_SL)
    o, h, l, c = bars((10, 10.5, 9.5, 10), (8.5, 8.7, 8.4, 8.6), (10, 10, 10, 10))
    assert run_position(o, h, l, c, 0, 1, 9.0, 12.0, MK, max_bars=3) == (1, 8.46875, EXIT_SL)
    o, h, l, c = bars((10, 12.5, 8.95, 10), (10, 10, 10, 10))
    assert run_position(o, h, l, c, 0, 1, 9.0, 12.0, MK, max_bars=2) == (0, 8.96875, EXIT_SL)


def test_time_stop_and_missing_data():
    o, h, l, c = bars((10, 10.5, 9.5, 10), (10, 10.5, 9.5, 10.25), (10, 10.5, 9.5, 10.375))
    assert run_position(o, h, l, c, 0, 1, 9.0, 12.0, MK, max_bars=3) == (2, 10.34375, EXIT_TIME)
    assert run_position(o, h, l, c, 0, -1, 11.0, 8.0, MK, max_bars=3) == (2, 10.65625, EXIT_TIME)
    assert run_position(o, h, l, c, 0, 1, 9.0, 12.0, MK, max_bars=4) is None
    # an exit inside the available data does not need the full window
    o2, h2, l2, c2 = bars((10, 10.5, 9.5, 10), (10, 10.5, 8.9, 10))
    assert run_position(o2, h2, l2, c2, 0, 1, 9.0, 12.0, MK, max_bars=864)[2] == EXIT_SL


def test_short_triggers_are_shifted_by_the_spread():
    # the short stop at 11 is an ask price: bid high 10.75 + spread 0.25 reaches it
    o, h, l, c = bars((10, 10.5, 9.5, 10), (10, 10.75, 9.9, 10), (10, 10, 10, 10))
    assert run_position(o, h, l, c, 0, -1, 11.0, 8.0, MK, max_bars=3) == (1, 11.03125, EXIT_SL)
    # the target at 8 is an ask price too: the bid must reach 8 - 0.25 - 0.0625
    o, h, l, c = bars((10, 10.5, 9.5, 10), (10, 10.5, 7.75, 10), (10, 10.5, 7.6875, 10))
    assert run_position(o, h, l, c, 0, -1, 11.0, 8.0, MK, max_bars=3) == (2, 8.0, EXIT_TP)
    # a gap through the short stop fills at the ask open
    o, h, l, c = bars((10, 10.5, 9.5, 10), (11.25, 11.5, 11.0, 11.25), (10, 10, 10, 10))
    assert run_position(o, h, l, c, 0, -1, 11.0, 8.0, MK, max_bars=3) == (1, 11.53125, EXIT_SL)


# ---- pending order -------------------------------------------------------------------------
def _pend(rows, d=1, trend=None, price=10.0, sl=9.0, tp=12.0, valid=3):
    o, h, l, c = bars(*rows)
    trend = np.full(len(o), d) if trend is None else np.asarray(trend)
    return pending_order(o, h, l, trend, 0, d, price, sl, tp, MK, valid=valid)


def test_limit_fill_needs_spread_and_a_tick():
    # buy limit at 10 (ask) fills when the bid low reaches 10 - 0.25 - 0.0625
    assert _pend([(10.5, 10.6, 9.75, 10.3), (10.3, 10.4, 9.6875, 10.2), (10, 10, 10, 10)]) == (TRADED, 1)
    # sell limit at 9.5 (bid) fills one tick above
    assert _pend([(9.25, 9.5, 9.0, 9.25)], d=-1, price=9.5, sl=10.5, tp=7.0, valid=1) == (EXPIRED, 0)
    assert _pend([(9.25, 9.5625, 9.0, 9.25)], d=-1, price=9.5, sl=10.5, tp=7.0, valid=1) == (TRADED, 0)


def test_cancellations_beat_a_fill_in_the_same_bar():
    rows = [(10.5, 10.6, 10.2, 10.3), (10.3, 10.4, 9.6, 10.2), (10, 10, 10, 10)]
    assert _pend(rows) == (TRADED, 1)
    assert _pend(rows, trend=[1, -1, 1]) == (CANCEL_TREND, 1)
    assert _pend([(10.5, 10.6, 10.2, 10.3), (8.9, 9.0, 8.8, 8.9), (10, 10, 10, 10)]) == (CANCEL_STOP, 1)
    assert _pend([(10.5, 10.6, 10.2, 10.3), (10.3, 12.0625, 9.6, 10.2), (10, 10, 10, 10)]) == (CANCEL_TARGET, 1)


def test_expiry_and_end_of_data():
    rows = [(10.5, 10.6, 10.2, 10.3)] * 3
    assert _pend(rows) == (EXPIRED, 2)
    assert _pend(rows[:2]) == (NO_DATA, -1)


# ---- targets -------------------------------------------------------------------------------
def _pool_table(rows):
    p = np.array(rows, dtype=POOL_DTYPE)
    return p[np.argsort(p["t_avail"], kind="stable")]


def test_target_is_nearest_active_pool_beyond_2r():
    t_open = np.arange(10) * 300
    h = np.full(10, 10.25)
    l = np.full(10, 9.75)
    h[2] = 11.25          # + raw spread pierces 10.75 and 11.25 before the fill
    h[5] = 11.4375        # + raw spread pierces 11.5 in the fill bar (bar 5) only
    pools = _pool_table([
        (1, SWING_INT, 10.75, 0, 10_000),
        (1, SWING_INT, 11.25, 0, 10_000),
        (1, SWING_EXT, 11.5, 0, 10_000),
        (1, SWING_EXT, 11.625, 300, 10_000),
        (1, SWING_INT, 11.3125, 1_800, 10_000),  # known only after bar 5 opens
        (1, SWING_INT, 11.4375, 0, 1_500),       # expired when bar 5 opens
        (-1, SWING_INT, 11.125, 0, 10_000),      # wrong side
        (1, SWING_EXT, 13.0, 0, 10_000),
    ])
    tg = Targets(pools, t_open, h, l, 0.125)
    # entry 10, risk 0.5: target at least 11, at most 12
    assert tg.pick(5, 1, 10.0, 0.5, include_bar=False) == (11.5, SWING_EXT)
    assert tg.pick(5, 1, 10.0, 0.5, include_bar=True) == (11.625, SWING_EXT)
    assert tg.pick(1, 1, 10.0, 0.25, include_bar=True) == (10.75, SWING_INT)
    assert tg.pick(5, 1, 10.0, 0.375, include_bar=True) == (11.5, TARGET_CAP)   # 11.625 is beyond 4R
    assert tg.pick(5, 1, 10.0, 2.0, include_bar=True) == (14.0, TARGET_MIN)     # nothing beyond 2R
    short = _pool_table([(-1, SWING_INT, 8.875, 0, 10_000), (-1, SWING_INT, 8.625, 0, 10_000)])
    l2 = l.copy()
    l2[3] = 8.75
    assert Targets(short, t_open, h, l2, 0.125).pick(5, -1, 10.0, 0.5, include_bar=False) == (8.625, SWING_INT)


# ---- zones ---------------------------------------------------------------------------------
def test_pick_zone_youngest_untouched_inside_the_leg():
    n = 10
    m15 = np.zeros(n, dtype=[("t", "i8"), ("o", "f8"), ("h", "f8"), ("l", "f8"), ("c", "f8")])
    m15["l"], m15["h"], m15["c"] = 10.9, 11.2, 11.0
    m15["l"][7] = 10.75   # touches zone B
    m15["l"][9] = 10.85   # touches zone C
    zones = np.zeros(3, ZONE_DTYPE)
    for z, (k, top, bot) in enumerate(((4, 10.5, 10.3), (6, 10.8, 10.6), (8, 10.875, 10.7))):
        zones[z] = (FVG, 1, k, k - 1, top, bot, (top + bot) / 2, bot, 1.0, 0)
    assert pick_zone(zones, m15, 3, 9, 1)["k"] == 4
    assert pick_zone(zones, m15, 4, 9, 1) is None            # zone A was formed before the leg
    assert pick_zone(zones, m15, 3, 9, -1) is None
    m15["c"][9] = 10.45                                      # price is back below A's top
    assert pick_zone(zones, m15, 3, 9, 1) is None


# ---- whole model on synthetic data -----------------------------------------------------------
def synthetic_m1(weeks=104, seed=1):
    """Random walk plus a slow (4-week) and a fast (~2-day) swing, so that H1 counter swings
    inside H4 trends occur often enough. Five 24-hour days per week."""
    rng = np.random.default_rng(seed)
    t0 = timegm((2021, 1, 3, 22, 0, 0))          # Sunday 17:00 New York
    t = np.concatenate([t0 + w * 7 * 86400 + 60 * np.arange(5 * 1440) for w in range(weeks)])
    x = np.arange(len(t))
    c = (1.10 + np.cumsum(rng.normal(0, 5e-5, len(t))) + 0.02 * np.sin(2 * np.pi * x / 28_800)
         + 0.006 * np.sin(2 * np.pi * x / 3_000))
    o = np.r_[c[0], c[:-1]]
    wick = np.abs(rng.normal(0, 2.5e-5, (2, len(t))))
    m1 = np.empty(len(t), M1_DTYPE)
    m1["t"], m1["o"], m1["c"] = t, o, c
    m1["h"], m1["l"] = np.maximum(o, c) + wick[0], np.minimum(o, c) - wick[1]
    return m1


def model_rows(m1):
    feats = build_symbol("EURUSD", bars={tf: resample(m1, tf) for tf in TFS})
    inp = Inputs.from_features(feats)
    return {v: run_model_c(inp, v, 0, 2**62) for v in (MKT, LMT)}


@pytest.fixture(scope="module")
def synthetic():
    m1 = synthetic_m1()
    cut = timegm((2022, 2, 26, 12, 0, 0))         # Saturday: no bar is cut in half
    return model_rows(m1), model_rows(m1[m1["t"] < cut]), cut


def test_model_c_trades_are_consistent(synthetic):
    full, _, _ = synthetic
    for v, rows in full.items():
        tr = rows[rows["status"] == TRADED]
        assert len(tr) >= 5, v
        d = tr["dir"]
        assert (tr["risk"] > 0).all() and (d * (tr["anchor"] - tr["sl"]) > 0).all()
        assert ((tr["tp_r"] >= 2 - 1e-9) & (tr["tp_r"] <= 4 + 1e-9)).all()
        assert all(cost_in_price("EURUSD", e) <= 0.1 * r for e, r in zip(tr["entry"], tr["risk"]))
        assert (tr["gross_r"][tr["exit_reason"] == EXIT_SL] <= -1 + 1e-9).all()
        assert (tr["gross_r"][tr["exit_reason"] == EXIT_TP] > 1.9).all()
        assert (tr["net_r"] < tr["gross_r"]).all() and (tr["cost_r"] > 0).all()
        assert (tr["t_sig"][1:] >= tr["t_end"][:-1]).all()      # one position at a time
        assert ((tr["entry_kind"] == ENTRY_MARKET) == (v == MKT)).all()


def test_model_c_is_history_invariant(synthetic):
    """Rows resolved before the cut must not change when later data is appended (no lookahead)."""
    full, part, cut = synthetic
    for v in (MKT, LMT):
        p = part[v]
        done = (p["status"] != NO_DATA) & (p["t_end"] <= cut)
        assert done.sum() >= 5, v
        f = full[v]
        pos = np.searchsorted(f["t_sig"], p["t_sig"][done])
        for name in f.dtype.names:
            a, b = f[name][pos], p[name][done]
            assert np.array_equal(a, b, equal_nan=a.dtype.kind == "f"), (v, name)
