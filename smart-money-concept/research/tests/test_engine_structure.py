import numpy as np
import pytest

from smc.engine.atr import atr
from smc.engine.pivots import fractal_pivots, leg_pivots
from smc.engine.structure import BOS, CHOCH, CHOCH_STRICT, EXT, INT, run_structure


def random_walk(n=6000, seed=0):
    rng = np.random.default_rng(seed)
    c = 1.10 + np.cumsum(rng.normal(0, 1e-4, n))
    o = np.r_[c[0], c[:-1]]
    spread = np.abs(rng.normal(0, 6e-5, n))
    h = np.maximum(o, c) + spread
    l = np.minimum(o, c) - spread
    return o, h, l, c


def test_atr_matches_wilder_definition():
    o, h, l, c = random_walk(200, 1)
    a = atr(h, l, c, 14)
    tr = np.maximum(h - l, np.maximum(abs(h - np.r_[c[0], c[:-1]]), abs(l - np.r_[c[0], c[:-1]])))
    assert np.isnan(a[12]) and a[13] == pytest.approx(tr[:14].mean())
    assert a[14] == pytest.approx((a[13] * 13 + tr[14]) / 14)


def test_leg_pivots_alternate_start_with_low_and_confirm_after_size_bars():
    o, h, l, c = random_walk(3000, 2)
    p = leg_pivots(h, l, 5)
    assert p["side"][0] == -1
    assert np.all(p["side"][1:] != p["side"][:-1])
    assert np.all(p["k"] == p["i"] + 5)
    for row in p:  # a pivot high exceeds every high of the confirming window
        i, k = row["i"], row["k"]
        if row["side"] == 1:
            assert h[i] > h[i + 1:k + 1].max()
        else:
            assert l[i] < l[i + 1:k + 1].min()


def test_fractal_tie_rule_strict_right_inclusive_left():
    h = np.array([1.0, 2.0, 2.0, 1.0, 3.0, 1.0])
    l = np.array([0.5, 0.4, 0.6, 0.3, 0.9, 0.2])
    p = fractal_pivots(h, l, 1)
    highs = p[p["side"] == 1]["i"].tolist()
    assert highs == [2, 4]          # bar 1 fails (right neighbour equal), bar 2 passes (left equal allowed)
    assert (p["k"] == p["i"] + 1).all()


@pytest.mark.parametrize("cut", [1500, 2500, 4000, 5999])
def test_structure_is_history_invariant(cut):
    """Results for bars < cut must not change when later bars are appended (no lookahead)."""
    o, h, l, c = random_walk(6000, 3)
    full = run_structure(h, l, c, leg_pivots(h, l, 5), leg_pivots(h, l, 50))
    hc, lc, cc = h[:cut], l[:cut], c[:cut]
    part = run_structure(hc, lc, cc, leg_pivots(hc, lc, 5), leg_pivots(hc, lc, 50))
    ev_full = full.events[full.events["k"] < cut]
    assert np.array_equal(ev_full, part.events)
    for name in ("bias_int", "bias_ext", "trend", "transition", "trail_top", "prot_low", "prot_high", "int_high"):
        assert np.array_equal(getattr(full, name)[:cut], getattr(part, name), equal_nan=True), name


def test_strict_trend_flips_only_at_protected_level():
    # Up-move with higher highs, a pullback that holds, then a breakdown through the protected low.
    path = [10, 11, 12, 11, 10.5, 11.5, 13, 14, 13, 12.2, 12.6, 15, 16, 15, 14, 13.5, 13.8, 12.0, 11.0, 10.0]
    c = np.repeat(np.array(path, float), 1)
    h, l = c + 0.1, c - 0.1
    s = run_structure(h, l, c, leg_pivots(h, l, 1), leg_pivots(h, l, 1))
    strict = s.events[s.events["type"] == CHOCH_STRICT]
    bos_up = s.events[(s.events["layer"] == EXT) & (s.events["dir"] == 1)]
    assert len(bos_up) >= 1 and s.trend[int(bos_up["k"][0])] == 1
    assert len(strict) == 1 and strict["dir"][0] == -1
    k = int(strict["k"][0])
    assert c[k] < strict["level"][0] and (c[:k][s.trend[:k] == 1] >= strict["level"][0]).all()


def test_break_types_follow_bias():
    o, h, l, c = random_walk(6000, 4)
    s = run_structure(h, l, c, leg_pivots(h, l, 5), leg_pivots(h, l, 50))
    for layer in (INT, EXT):
        ev = s.events[(s.events["layer"] == layer) & (s.events["type"] != CHOCH_STRICT)]
        prev = 0
        for e in ev:
            assert e["type"] == (CHOCH if prev == -e["dir"] else BOS)
            prev = e["dir"]
