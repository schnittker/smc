import numpy as np
import pytest

from cta.model import (BAND, CLASSES, SETS, VOL_FLOOR, crypto_rows, dense, portfolio, target_path, walk_forward,
                       year_start)
from kry.model import SWAP, trade_cost_rate


def test_target_path_signal_vol_and_floor():
    p = 100 * 1.001 ** np.arange(300)               # smooth uptrend: sigma ~ 0 -> floor 4 %
    w = target_path(p, (21, 63), 0.025, 261, np.ones(300, bool))
    assert (w[:63] == 0).all()
    assert w[63] == pytest.approx(0.025 / VOL_FLOOR) and (w[63:] == w[63]).all()


def test_target_path_band_and_allowed_days():
    rng = np.random.default_rng(3)
    p = 100 * np.exp(np.cumsum(rng.normal(0.002, 0.01, 400)))
    allowed = np.arange(400) % 2 == 0
    w = target_path(p, (10, 21), 0.05, 261, allowed)
    changed = np.flatnonzero(np.diff(w) != 0) + 1
    assert allowed[changed].all()                   # trades only on allowed days
    for i in changed:
        if np.sign(w[i]) == np.sign(w[i - 1]):
            assert abs(w[i] - w[i - 1]) > BAND * abs(w[i - 1])


def test_crypto_rows_accounting():
    px = {"p_mark": np.array([100.0, 110.0, 99.0]), "lo": np.array([0, 105.0, 90.0]),
          "hi": np.array([0, 112.0, 111.0])}
    r = crypto_rows(px, "BTC", np.array([0.2, -0.1, -0.1]))
    rate = trade_cost_rate("BTC")
    assert r["pnl"].tolist() == pytest.approx([0.0, 0.2 * 0.10, -0.1 * (99 / 110 - 1)])
    assert r["worst"].tolist() == pytest.approx([0.0, 0.2 * (105 / 100 - 1) * 0, -0.1 * (111 / 110 - 1)])
    assert r["cost"][1] == pytest.approx(0.3 * rate + 0.2 * SWAP / 365)
    assert r["net"][0] == pytest.approx(-0.2 * rate)


def fake_dense(nets: dict, ws: dict, days):
    """dn[set] with one market per class; nets/ws per set: (days x 4)."""
    out = {}
    for s in SETS:
        out[s] = {"days": days, "net": nets[s], "cost": np.zeros_like(nets[s]), "worst": np.zeros_like(nets[s]),
                  "w": ws[s], "pnl": nets[s], "row": np.ones_like(nets[s], bool), "names": list("abcd"),
                  "cls": np.array(CLASSES), "lev": np.array([30.0, 15.0, 9.0, 1.0])}
    return out


def test_walk_forward_picks_best_set_and_normalises():
    y15, y17 = year_start(2015), year_start(2017)
    days = np.arange(y15, y17 + 10)
    rng = np.random.default_rng(0)
    base = rng.normal(0, 0.01, (len(days), 4))
    nets = {"SCHNELL": base + [0.002, -0.001, 0.0, 0.0], "MITTEL": base + [0.0, 0.001, -0.002, 0.0],
            "LANGSAM": base + [-0.001, 0.0, -0.001, 0.0]}
    ws = {s: np.ones((len(days), 4)) * 0.1 for s in SETS}
    ws["MITTEL"][:, 3] = np.where(days >= y15 + 500, 0.1, 0.0)        # crypto starts late -> < 1 year by 2016
    ch = walk_forward(fake_dense(nets, ws, days), range(2015, 2018))
    assert ch[2015]["set"] == dict.fromkeys(CLASSES, "MITTEL") and ch[2015]["a"] == dict.fromkeys(CLASSES, 1.0)
    assert ch[2016]["set"]["FX"] == "SCHNELL" and ch[2016]["set"]["Indizes"] == "MITTEL"
    assert ch[2016]["a"]["Krypto"] == 1.0                             # not eligible: fixed weight 1
    elig = [c for c in CLASSES if c != "Krypto"]
    assert sum(ch[2016]["a"][c] for c in elig) == pytest.approx(3.0)


def test_portfolio_transition_cost_and_margin():
    days = np.arange(year_start(2015), year_start(2016) + 3)
    n = len(days)
    nets = {s: np.zeros((n, 4)) for s in SETS}
    ws = {s: np.full((n, 4), 0.3 if s == "MITTEL" else 0.1) for s in SETS}
    dn = fake_dense(nets, ws, days)
    markets = {nm: {"kind": "crypto", "coin": "BTC", "px": {"day": days}} for nm in "abcd"}
    ch = {2015: {"set": dict.fromkeys(CLASSES, "MITTEL"), "a": dict.fromkeys(CLASSES, 1.0)},
          2016: {"set": dict.fromkeys(CLASSES, "SCHNELL"), "a": dict.fromkeys(CLASSES, 2.0)}}
    pf = portfolio(dn, markets, ch)
    i = int(np.flatnonzero(days == year_start(2016))[0])
    assert pf["trans"][i] == pytest.approx(4 * abs(0.2 - 0.3) * trade_cost_rate("BTC"))
    assert pf["trans"].sum() == pytest.approx(pf["trans"][i])
    assert pf["margin"][0] == pytest.approx(0.3 * (1 / 30 + 1 / 15 + 1 / 9 + 1))
    fix = portfolio(dn, markets, None)
    assert fix["trans"].sum() == 0 and fix["margin"][-1] == pytest.approx(pf["margin"][0])


def test_dense_carries_held_weight_over_missing_days():
    books = {"x": {"day": np.array([10, 11, 14]), "net": np.array([1.0, 2.0, 3.0]), "cost": np.zeros(3),
                   "worst": np.zeros(3), "w": np.array([0.1, 0.2, 0.3]), "pnl": np.zeros(3)}}
    d = dense(books, {"x": {"cls": "FX"}}, 10, 15)
    assert d["w"][:, 0].tolist() == [0.1, 0.2, 0.2, 0.2, 0.3]
    assert d["net"][:, 0].tolist() == [1.0, 2.0, 0.0, 0.0, 3.0] and d["row"][:, 0].tolist() == [1, 1, 0, 0, 1]
