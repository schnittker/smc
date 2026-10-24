import numpy as np
import pytest

from smc import timez
from swp.portfolio import (DAILY_LIMIT, align, book_daily, book_events, book_trades, bootstrap, derisk, historical,
                           inverse_vol_weights, month_blocks, run_phase)
from fomc.model import ROW_DTYPE
from smc.strategy_g import DAY_DTYPE

D0 = 19723                                   # 2024-01-01, Monday


def trade(t_entry, t_exit, net_bp, mae_bp):
    r = np.zeros(1, ROW_DTYPE)
    r["t_entry"], r["t_exit"], r["net_bp"], r["mae_bp"], r["cost_bp"] = t_entry, t_exit, net_bp, mae_bp, 3.0
    return r


def test_book_trades_on_server_day_of_exit():
    # exit 13:55 New York on 2024-01-03 (winter, UTC 18:55) -> server day of 2024-01-03
    t_exit = (D0 + 2) * timez.DAY + 18 * 3600 + 55 * 60
    b = book_trades(trade(t_exit - 86400, t_exit, 25.0, -40.0))
    assert b == {D0 + 2: (pytest.approx(0.0025), pytest.approx(-0.004), True, pytest.approx(0.0003))}


def test_book_trades_after_17_ny_goes_to_next_server_day():
    t_exit = (D0 + 2) * timez.DAY + 22 * 3600 + 30 * 60      # 17:30 New York
    assert list(book_trades(trade(t_exit - 86400, t_exit, 1.0, 0.0))) == [D0 + 3]


def test_book_daily_sums_rows_and_marks_activity():
    r = np.zeros(3, DAY_DTYPE)
    r["day"] = [D0, D0, D0 + 1]
    r["net"], r["worst"], r["w"] = [0.01, -0.002, 0.0], [-0.02, -0.01, 0.0], [1.0, 0.0, 0.0]
    r["cost"] = [0.001, 0.0, 0.0]
    b = book_daily(r)
    assert b[D0] == (pytest.approx(0.008), pytest.approx(-0.03), True, pytest.approx(0.001))
    assert b[D0 + 1] == (0.0, 0.0, False, 0.0)


def test_book_events_entry_and_exit_rows_of_traded_pairs_only():
    r = np.zeros(4, DAY_DTYPE)
    r["symbol"] = ["EURUSD", "EURUSD", "AUDUSD", "AUDUSD"]
    r["day"] = [D0, D0 + 1, D0, D0 + 1]
    r["net"] = [-0.001, 0.005, -0.001, 0.009]
    r["worst"] = [0.0, -0.004, 0.0, -0.007]
    r["cost"] = [0.0002, 0.0001, 0.0002, 0.0001]
    b = book_events(r, [(D0, D0 + 1, ["EURUSD"]), (D0 + 3, D0 + 4, [])])
    assert b == {D0 + 1: (pytest.approx(0.004), pytest.approx(-0.004), True, pytest.approx(0.0003))}


def test_align_union_calendar_weekdays_and_window():
    s = {"a": {D0: (0.01, -0.01, True, 0.001), D0 + 5: (1.0, 0.0, True, 0.0)},
         "b": {D0 + 1: (0.02, 0.0, True, 0.0), D0 + 9: (1, 0, True, 0)}}
    a = align(s, D0, D0 + 8)
    assert a["days"].tolist() == [D0, D0 + 1]                 # D0+5 is a Saturday, D0+9 outside
    assert a["net"].tolist() == [[0.01, 0.0], [0.0, 0.02]]
    assert a["active"].tolist() == [[True, False], [False, True]]
    assert a["cost"].tolist() == [[0.001, 0.0], [0.0, 0.0]]


def test_inverse_vol_weights_normalise_to_10_percent():
    rng = np.random.default_rng(1)
    x = rng.normal(0, [0.01, 0.002], (5000, 2))
    g = inverse_vol_weights(x)
    assert (x * g).std(axis=0, ddof=1) * np.sqrt(261) == pytest.approx([0.10, 0.10])


def test_month_blocks():
    days = np.array([D0, D0 + 1, D0 + 31, D0 + 32, D0 + 33, D0 + 60])
    s, n = month_blocks(days)
    assert s.tolist() == [0, 2, 5] and n.tolist() == [2, 3, 1]


def test_derisk_levels():
    assert derisk(np.array([1.0, 0.97, 0.95, 0.94, 0.90])).tolist() == [1, 0.5, 0.5, 0.25, 0.25]


def one_month(r, w=None, act=None):
    r = np.asarray(r, float)
    return (r, np.zeros_like(r) if w is None else np.asarray(w, float), np.ones(len(r), bool) if act is None else act,
            np.array([0]), np.array([len(r)]), np.array([[0]]))


def test_phase_passes_only_after_four_active_days():
    s, used, _, _ = run_phase(*one_month([0.11, 0.0, 0.0, 0.0, 0.0]), scale=1.0, target=0.10)
    assert s.tolist() == [1] and used.tolist() == [4]


def test_phase_daily_loss_uses_intraday_worst():
    s, used, _, _ = run_phase(*one_month([0.0, 0.01], [0.0, -DAILY_LIMIT]), scale=1.0, target=0.10)
    assert s.tolist() == [2] and used.tolist() == [2]          # the failing day counts as used


def test_phase_total_loss_with_derisk():
    # day 1 full: 97.1 %; day 2 full: 95.1 %; days 3-4 half: 94.1 %, 93.1 %; day 5 quarter: 92.6 %;
    # day 6 quarter of -20 % = -5 % -> daily limit
    r = [-0.029] + [-0.02] * 4 + [-0.20]
    s, used, _, _ = run_phase(*one_month(r), scale=1.0, target=0.10)
    assert s.tolist() == [2] and used.tolist() == [6]


def test_phase_unresolved_at_end_of_data():
    s, _, _, _ = run_phase(*one_month([0.001] * 5), scale=1.0, target=0.10)
    assert s.tolist() == [0]


def test_bootstrap_and_historical_trivial_paths():
    days = np.array([D0 + i for i in range(120) if (D0 + i + 3) % 7 < 5])
    r = np.full(len(days), 0.004)
    w = np.full(len(days), -0.001)
    act = np.ones(len(days), bool)
    b = bootstrap(r, w, act, days, scale=1.0, n_paths=200)
    assert b["both"] == 1.0 and 1.0 < b["median_months"] < 2.0
    h = historical(r, w, act, days, scale=1.0)
    assert h["starts"] == 4 and h["passed"] >= 2
