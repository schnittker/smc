from datetime import datetime
from zoneinfo import ZoneInfo

import numpy as np
import pytest

from smc import timez
from smc.engine.atr import atr
from smc.engine.liquidity import (BROKEN, POOL_DTYPE, SESSION_ASIA, SWEPT, SWING_INT, evaluate_pools,
                                  group_outcomes, session_pools)
from smc.engine.mss import find_mss
from smc.engine.pivots import fractal_pivots, leg_pivots
from smc.engine.structure import run_structure
from smc.engine.zones import FVG, detect_fvg, detect_order_blocks, lifecycle
from smc.data.bars import BAR_DTYPE

from tests.test_engine_structure import random_walk

NY = ZoneInfo("America/New_York")


def bars_from(o, h, l, c, t0=0, step=300):
    return np.arange(len(c)) * step + t0, np.asarray(o, float), np.asarray(h, float), np.asarray(l, float), np.asarray(c, float)


def test_bullish_fvg_geometry_and_lifecycle():
    #            c1    c2 (impulse) c3    later: touch top, CE, far edge
    o = np.array([1.00, 1.00, 1.02, 1.03, 1.025, 1.015, 1.012])
    c = np.array([1.00, 1.02, 1.03, 1.025, 1.016, 1.013, 1.009])
    h = np.array([1.005, 1.021, 1.035, 1.031, 1.026, 1.017, 1.013])
    l = np.array([0.995, 0.999, 1.015, 1.019, 1.014, 1.011, 1.004])
    a = np.full(len(c), 0.01)
    z = detect_fvg(o, h, l, c, a, k_fvg=0.2)
    # bars 0,1,2: low[2]=1.015 > high[0]=1.005 -> zone [1.005, 1.015]
    first = z[0]
    assert first["kind"] == FVG and first["dir"] == 1 and first["k"] == 2
    assert first["bot"] == pytest.approx(1.005) and first["top"] == pytest.approx(1.015)
    life = lifecycle(z[:1], np.array([3]), o, h, l, c, max_bars=10)[0]
    assert life["touch"] == 4      # low 1.014 <= 1.015
    assert life["mid"] == 6        # low 1.004 <= CE 1.010
    assert life["far"] == 6 and life["invalid"] == -1  # wick through, body stays above 1.005


@pytest.mark.parametrize("cut", [2000, 4500])
def test_fvg_and_order_blocks_are_history_invariant(cut):
    o, h, l, c = random_walk(6000, 5)
    a = atr(h, l, c, 14)

    def run(n):
        oo, hh, ll, cc, aa = o[:n], h[:n], l[:n], c[:n], a[:n]
        s = run_structure(hh, ll, cc, leg_pivots(hh, ll, 5), leg_pivots(hh, ll, 50))
        f = detect_fvg(oo, hh, ll, cc, aa, k_fvg=0.1)
        return f, detect_order_blocks(oo, hh, ll, cc, aa, s.events, f, require_fvg=False)

    f_full, ob_full = run(6000)
    f_cut, ob_cut = run(cut)
    assert np.array_equal(f_full[f_full["k"] < cut], f_cut)
    assert len(ob_full) > 0
    assert np.array_equal(ob_full[ob_full["k"] < cut], ob_cut)


def test_pool_sweep_versus_break_and_ask_adjustment():
    t, o, h, l, c = bars_from(
        o=[1.010, 1.010, 1.002, 1.004, 0.997, 0.996],
        h=[1.012, 1.011, 1.005, 1.006, 0.999, 0.998],
        l=[1.008, 1.003, 0.998, 1.001, 0.995, 0.994],
        c=[1.010, 1.004, 1.002, 1.003, 0.996, 0.995])
    pools = np.array([
        (-1, SWING_INT, 1.000, 0, 10**9),   # wick to 0.998 at bar 2, close back above -> SWEPT at 2
        (-1, SWING_INT, 0.9965, 0, 10**9),  # closes below at bars 4 and 5 -> BROKEN at 5
        (1, SWING_INT, 1.0125, 0, 10**9),   # bid high 1.012 only reaches it with spread
    ], dtype=POOL_DTYPE)
    res = evaluate_pools(pools, t, h, l, c, spread=0.0)
    assert [(r["pool"], r["outcome"], r["k"]) for r in res] == [(0, SWEPT, 2), (1, BROKEN, 5)]
    res_sp = evaluate_pools(pools, t, h, l, c, spread=0.0006)
    bsl = res_sp[res_sp["pool"] == 2]
    assert len(bsl) == 1 and bsl["pierce"][0] == 0
    g = group_outcomes(res)
    assert len(g) == 2


def test_session_pool_available_at_window_end():
    start = int(datetime(2026, 10, 20, 17, 0, tzinfo=NY).timestamp())  # FX day opens (server Wed 00:00)
    n = 12 * 24
    m5 = np.zeros(n, dtype=BAR_DTYPE)
    m5["t"] = start + 300 * np.arange(n)
    m5["ts"] = timez.utc_to_server(m5["t"])
    m5["h"] = 1.10 + 1e-4 * np.arange(n)
    m5["l"] = m5["h"] - 5e-4
    p = session_pools(m5, {SESSION_ASIA: (20 * 60, 24 * 60)})
    assert len(p) == 2
    hi = p[p["side"] == 1][0]
    assert timez.ny_minute_of_day(hi["t_avail"]) == 0          # known at 00:00 NY
    asia = (timez.ny_minute_of_day(m5["t"]) >= 1200)
    assert hi["px"] == pytest.approx(m5["h"][asia].max())


def test_mss_after_ssl_sweep():
    # short-term high at bar 2 (1.0040); SSL at 1.0000 swept at bar 5; strong rally closes above 1.0040
    o = [1.0030, 1.0035, 1.0038, 1.0030, 1.0015, 1.0004, 1.0010, 1.0028, 1.0050]
    c = [1.0035, 1.0038, 1.0031, 1.0016, 1.0005, 1.0010, 1.0027, 1.0049, 1.0058]
    h = [1.0037, 1.0039, 1.0040, 1.0032, 1.0017, 1.0012, 1.0028, 1.0050, 1.0060]
    l = [1.0028, 1.0033, 1.0030, 1.0014, 1.0003, 0.9996, 1.0009, 1.0026, 1.0048]
    o, h, l, c = map(lambda x: np.array(x, float), (o, h, l, c))
    t = np.arange(len(c)) * 300
    a = np.full(len(c), 0.0012)
    pools = np.array([(-1, SWING_INT, 1.0000, 0, 10**9)], dtype=POOL_DTYPE)
    sweeps = group_outcomes(evaluate_pools(pools, t, h, l, c))
    assert sweeps["outcome"][0] == SWEPT and sweeps["k"][0] == 5
    sth = fractal_pivots(h, l, 1)
    fvgs = detect_fvg(o, h, l, c, a, k_fvg=0.1)
    m = find_mss(sweeps, o, h, l, c, a, sth, fvgs, window=10, kd=1.0)
    assert len(m) == 1
    assert m["dir"][0] == 1 and m["k"][0] == 7 and m["ref_px"][0] == pytest.approx(1.0040)
    assert m["extreme"][0] == pytest.approx(0.9996)


def test_displacement_index_matches_reference():
    from smc.engine.displacement import DisplacementIndex, first_displacement
    o, h, l, c = random_walk(3000, 7)
    a = atr(h, l, c, 14)
    idx = DisplacementIndex(o, h, l, c, a, kd=0.8)
    rng = np.random.default_rng(0)
    hits = 0
    for _ in range(600):
        lo = int(rng.integers(0, 2900))
        hi = lo + int(rng.integers(0, 40))
        for d in (1, -1):
            ref = first_displacement(o, h, l, c, a, lo, hi, d, kd=0.8)
            assert idx.first(lo, hi, d) == ref
            hits += ref is not None
    assert hits > 50
