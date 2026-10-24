from calendar import timegm

import numpy as np
import pytest

from smc.strategy_c import NO_DATA, TRADED
from smc.strategy_d import EXIT_SL, EXIT_STRUCT, EXIT_TIME, run_exit, run_model_d
from smc.swaps import MARKUP, RateTable, parse_fred_csv, rollovers, swap_r

from tests.test_strategy_c import MK, bars

NEVER = 10**9
RATES = RateTable.constant({"EUR": 0.02, "USD": 0.05})


# ---- exits ---------------------------------------------------------------------------------
def test_structure_exit_at_open_beats_a_stop_in_the_same_bar():
    o, h, l, c = bars((10, 10.5, 9.5, 10), (10, 10.5, 9.5, 10.2), (10.25, 10.6, 8.5, 10))
    assert run_exit(o, h, l, c, 0, 1, 9.0, 2, MK, max_bars=10) == (2, 10.21875, EXIT_STRUCT)
    # gap below the stop at the structure exit: filled at the open
    o2 = o.copy()
    o2[2] = 8.5
    assert run_exit(o2, h, l, c, 0, 1, 9.0, 2, MK, max_bars=10) == (2, 8.46875, EXIT_STRUCT)


def test_stop_before_structure_exit_and_time_stop():
    o, h, l, c = bars((10, 10.5, 9.5, 10), (10, 10.5, 8.9, 10.2), (10.25, 10.6, 9.5, 10))
    assert run_exit(o, h, l, c, 0, 1, 9.0, 2, MK, max_bars=10) == (1, 8.96875, EXIT_SL)
    o, h, l, c = bars((10, 10.5, 9.5, 10), (10, 10.5, 9.5, 10.25), (10, 10.5, 9.5, 10.375))
    assert run_exit(o, h, l, c, 0, 1, 9.0, NEVER, MK, max_bars=3) == (2, 10.34375, EXIT_TIME)
    assert run_exit(o, h, l, c, 0, 1, 9.0, 5, MK, max_bars=3) == (2, 10.34375, EXIT_TIME)   # struct too late
    assert run_exit(o, h, l, c, 0, 1, 9.0, NEVER, MK, max_bars=5) is None


def test_short_exits_pay_the_spread():
    o, h, l, c = bars((10, 10.5, 9.5, 10), (10, 10.5, 9.5, 10), (9.75, 10, 9.5, 9.75))
    assert run_exit(o, h, l, c, 0, -1, 11.0, 2, MK, max_bars=10) == (2, 10.03125, EXIT_STRUCT)
    o, h, l, c = bars((10, 10.5, 9.5, 10), (10, 10.75, 9.5, 10), (9.75, 10, 9.5, 9.75))
    assert run_exit(o, h, l, c, 0, -1, 11.0, 2, MK, max_bars=10) == (1, 11.03125, EXIT_SL)


# ---- swaps ---------------------------------------------------------------------------------
def test_rollovers_count_wednesday_triple_and_skip_the_weekend():
    # Tuesday 20.10.2026 12:00 UTC to Tuesday 27.10.2026 12:00 UTC; server = UTC+3, rollover 21:00 UTC
    t0, t1 = timegm((2026, 10, 20, 12, 0, 0)), timegm((2026, 10, 27, 12, 0, 0))
    r, nights = rollovers(t0, t1)
    assert nights.tolist() == [1, 3, 1, 1, 1]
    assert r[0] == timegm((2026, 10, 20, 21, 0, 0)) and r[-1] == timegm((2026, 10, 26, 21, 0, 0))
    # entry exactly at a rollover pays nothing for it, an exit exactly at one pays it
    r2, n2 = rollovers(timegm((2026, 10, 20, 21, 0, 0)), timegm((2026, 10, 21, 21, 0, 0)))
    assert n2.tolist() == [3]
    assert len(rollovers(t0, t0 + 3600)[0]) == 0


def test_swap_in_r_follows_rate_differential_and_markup():
    t0, t1 = timegm((2026, 10, 20, 12, 0, 0)), timegm((2026, 10, 27, 12, 0, 0))
    long_ = swap_r("EURUSD", 1, t0, t1, 1.1, 0.011, RATES)
    short = swap_r("EURUSD", -1, t0, t1, 1.1, 0.011, RATES)
    assert long_ == pytest.approx(7 * (0.02 - 0.05 - MARKUP) * 1.1 / 365 / 0.011)
    assert short == pytest.approx(7 * (0.05 - 0.02 - MARKUP) * 1.1 / 365 / 0.011)
    gold = swap_r("XAUUSD", 1, t0, t1, 2000.0, 20.0, RATES)
    assert gold == pytest.approx(7 * (0.0 - 0.05 - MARKUP) * 2000.0 / 365 / 20.0)


def test_parse_fred_csv_skips_missing_values():
    m, r = parse_fred_csv("observation_date,X\n2024-01-01,5.33\n2024-02-01,.\n2024-03-01,5.25\n")
    assert r.tolist() == [0.0533, 0.0525]
    assert m.tolist() == [np.datetime64("2024-01", "M").astype(np.int64), np.datetime64("2024-03", "M").astype(np.int64)]
    table = RateTable({"USD": (m, r)})
    assert table.rate("USD", int(m[1]) + 30) == 0.0525 and table.rate("USD", int(m[0]) - 5) == 0.0533


# ---- whole model on synthetic data -----------------------------------------------------------
@pytest.fixture(scope="module")
def synthetic_d(synthetic_inputs):
    full, part, cut = synthetic_inputs
    return run_model_d(full, 0, 2**62, RATES), run_model_d(part, 0, 2**62, RATES), cut


def test_model_d_trades_are_consistent(synthetic_d):
    rows, _, _ = synthetic_d
    tr = rows[rows["status"] == TRADED]
    assert len(tr) >= 5
    # one position at a time; after a structure exit the next entry may use the same open
    gap = tr["i_fill"][1:] - tr["i_end"][:-1]
    assert (gap >= np.where(tr["exit_reason"][:-1] == EXIT_STRUCT, 0, 1)).all()
    assert (tr["exit_reason"] == EXIT_STRUCT).any()
    assert (tr["gross_r"][tr["exit_reason"] == EXIT_SL] <= -1 + 1e-9).all()
    assert np.isnan(tr["tp"]).all() and (tr["t_end"] > tr["t_fill"]).all()
    assert np.allclose(tr["fee_r"], 0.0)                           # EURUSD pays no conversion fee
    # EUR 2 %, USD 5 %, markup 1 %: longs pay 4 % p. a., shorts earn 2 % p. a.
    assert (tr["swap_r"][tr["dir"] == 1] <= 0).all() and (tr["swap_r"][tr["dir"] == -1] >= 0).all()
    assert (tr["cost_r"] > 0).all() and (tr["net_r"] < tr["gross_r"] + np.maximum(tr["swap_r"], 0) + 1e-12).all()


def test_model_d_is_history_invariant(synthetic_d):
    full, part, cut = synthetic_d
    done = (part["status"] != NO_DATA) & (part["t_end"] <= cut)
    assert done.sum() >= 5
    pos = np.searchsorted(full["t_sig"], part["t_sig"][done])
    for name in full.dtype.names:
        a, b = full[name][pos], part[name][done]
        assert np.array_equal(a, b, equal_nan=a.dtype.kind == "f"), name
