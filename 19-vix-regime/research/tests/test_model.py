from datetime import date

import numpy as np

from smc.strategy_g import VOL_TARGET
from vixr.model import EPOCH, LOOKBACK, load_vix, regime_changes, risk_off, targets


def test_risk_off_uses_only_past_quantile():
    close = np.r_[np.full(LOOKBACK, 15.0), [15.0, 30.0, 14.0]]
    close[:26] = 20.0                      # top decile of the lookback window = 20
    flag = risk_off(close)
    assert not flag[:LOOKBACK].any()
    assert not flag[LOOKBACK] and flag[LOOKBACK + 1] and not flag[LOOKBACK + 2]


def test_regime_changes():
    days = np.arange(LOOKBACK + 5)
    flag = np.zeros(LOOKBACK + 5, bool)
    flag[LOOKBACK + 1:LOOKBACK + 3] = True
    assert regime_changes(days, flag) == [(LOOKBACK + 1, True), (LOOKBACK + 3, False)]


def _px(n=300, start=16000):
    days = np.array([d for d in range(start, start + 2 * n) if (d + 3) % 7 < 5][:n])
    p = 100 * np.exp(np.cumsum(np.random.default_rng(2).normal(0, 0.01, n)))
    return {"day": days, "p_sig": p, "p_mark": p, "exact": np.ones(n, bool), "lo": p, "hi": p}


def test_targets_same_day_and_next_day():
    px = _px()
    d_on, d_off = int(px["day"][100]), int(px["day"][110])
    same = targets(px, [(d_on, True), (d_off, False)], -1, next_day=False)
    nxt = targets(px, [(d_on, True), (d_off, False)], 1, next_day=True)
    assert set(same) == {d_on, d_off} and same[d_on] < 0 and same[d_off] == 0.0
    assert set(nxt) == {int(px["day"][101]), int(px["day"][111])} and nxt[int(px["day"][101])] > 0
    assert abs(same[d_on]) < 1.0 / 0.04 * VOL_TARGET + 1e-9


def test_load_vix(tmp_path):
    p = tmp_path / "v.csv"
    p.write_text("DATE,OPEN,HIGH,LOW,CLOSE\n01/02/2015,17,18,16,17.5\n01/05/2015,18,20,17,19.9\n")
    days, close = load_vix(p)
    assert days[0] == (date(2015, 1, 2) - EPOCH).days and close.tolist() == [17.5, 19.9]
