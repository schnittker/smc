import json

import numpy as np
import pytest

from kry.data import panel, read_coin
from kry.model import (ANNUAL, COMMISSION, MIN_HISTORY, SWAP, keep, run, sigma, signal, target, trade_cost_rate)


def write(tmp_path, coin, start_day, closes, page=0):
    rows = [[(start_day + i) * 86_400_000, str(c), str(c * 1.01), str(c * 0.99), str(c), "0", 0, "0", 0, "0", "0", "0"]
            for i, c in enumerate(closes)]
    (tmp_path / f"{coin}USDT_{page}.json").write_text(json.dumps(rows))


def test_read_coin_dedups_pages_and_cuts_incomplete_day(tmp_path):
    write(tmp_path, "BTC", 20380, [1, 2, 3, 4, 5, 6, 7])              # up to 20386 (> LAST_DAY 20385)
    write(tmp_path, "BTC", 20383, [4, 5], page=1)                      # overlap
    a = read_coin("BTC", tmp_path)
    assert a[:, 0].tolist() == list(range(20380, 20386)) and a[-1, 4] == 6


def test_panel_aligns_late_listing_with_nan(tmp_path):
    write(tmp_path, "BTC", 100, [1.0] * 5)
    write(tmp_path, "ETH", 102, [2.0] * 3)
    p = panel(tmp_path, coins=("BTC", "ETH"))
    assert p["day"].tolist() == [100, 101, 102, 103, 104]
    assert np.isnan(p["c"][:2, 1]).all() and p["c"][2:, 1].tolist() == [2.0] * 3


def test_signal_mean_of_signs():
    # 60 days down from 200 to 100, then 10 days up to 140: up over 7/14/28 days, down over 56 days
    c = np.r_[np.linspace(200, 100, 61), np.linspace(104, 140, 10)]
    t = len(c) - 1
    assert c[t - 28] < 140 < c[t - 56]
    assert signal(c, t) == pytest.approx(0.5)


def test_sigma_floor_and_annualisation():
    assert sigma(np.full(40, 100.0), 39) == 0.30
    rng = np.random.default_rng(0)
    c = 100 * np.exp(np.cumsum(rng.normal(0, 0.05, 40)))
    r = np.diff(np.log(c[-31:]))
    assert sigma(c, 39) == pytest.approx(r.std(ddof=1) * np.sqrt(365))


def test_target_variants_and_cap():
    assert target("K-TSM", -0.5, 0.5) == pytest.approx(-0.1)
    assert target("K-LONG", -0.5, 0.5) == 0.0
    assert target("K-TSM", 1.0, 0.1) == 0.5                           # 0.10 / 0.10 = 1 -> cap 0.5 (floor 0.3 aside)


def test_keep_band_and_sign():
    assert keep(0.2, 0.24) and not keep(0.2, 0.26)
    assert not keep(0.2, -0.2) and not keep(0.0, 0.1) and not keep(0.1, 0.0)
    assert keep(0.0, 0.0)


def test_cost_rate():
    assert trade_cost_rate("BTC") == pytest.approx(0.75 * 0.0005 + COMMISSION)


def make_px(closes: np.ndarray, coins=("BTC",)):
    c = np.asarray(closes, float).reshape(len(closes), -1)
    return {"day": np.arange(len(c)), "coins": list(coins), "o": c, "h": c * 1.02, "l": c * 0.97, "c": c}


def test_run_trend_long_accounting():
    c = 100 * 1.01 ** np.arange(MIN_HISTORY + 10)                     # steady uptrend, 1 % a day
    b = run("K-TSM", make_px(c))
    t0 = MIN_HISTORY                                                    # first day with a target
    assert b["w"][t0, 0] == 0 and b["w"][t0 + 1, 0] == pytest.approx(0.10 / 0.30)   # vol floor 30 %
    w = b["w"][t0 + 1, 0]
    assert b["cost"][t0, 0] == pytest.approx(w * trade_cost_rate("BTC"))
    assert b["pnl"][t0 + 1, 0] == pytest.approx(w * 0.01)
    assert b["swap"][t0 + 1, 0] == pytest.approx(w * SWAP / ANNUAL)
    assert b["worst"][t0 + 1, 0] == pytest.approx(w * (0.97 * 1.01 - 1))
    assert b["cost"][t0 + 2:, 0].sum() == 0                            # inside the band: no further trades
    assert b["net"][t0 + 1, 0] == pytest.approx(b["pnl"][t0 + 1, 0] - b["swap"][t0 + 1, 0])


def test_run_short_worst_uses_high_and_long_only_stays_flat():
    c = 100 * 0.99 ** np.arange(MIN_HISTORY + 5)
    b = run("K-TSM", make_px(c))
    t = MIN_HISTORY + 1
    assert b["w"][t, 0] < 0 and b["worst"][t, 0] == pytest.approx(b["w"][t, 0] * (1.02 * 0.99 - 1))
    assert np.all(run("K-LONG", make_px(c))["w"] == 0)


def test_run_gross_cap_one_to_one():
    n = MIN_HISTORY + 5
    c = np.column_stack([100 * 1.01 ** np.arange(n)] * 5)
    b = run("K-TSM", make_px(c, ("BTC", "ETH", "LTC", "XRP", "ADA")))
    gross = np.abs(b["w"]).sum(axis=1)
    assert gross.max() == pytest.approx(1.0)                           # 5 x 0.333 = 1.67 -> 1.0
    assert b["w"][MIN_HISTORY + 1].tolist() == pytest.approx([0.2] * 5)
