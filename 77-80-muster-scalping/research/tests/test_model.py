import numpy as np
import pytest

from smc.data.bars import BAR_DTYPE
from smc.timez import server_to_utc
from hps.model import harmonic_signals, scalp_signals, spring_signals


def _bars(c, w=0.0005, step=14400, ts0=19002 * 86400):
    c = np.asarray(c, float)
    o = np.r_[c[0], c[:-1]]
    rows = [(int(server_to_utc(ts0 + step * j)), ts0 + step * j, o[j], max(o[j], c[j]) + w, min(o[j], c[j]) - w,
             c[j], 1) for j in range(len(c))]
    return np.array(rows, dtype=BAR_DTYPE)


def _path(points, seg=8):
    out = [points[0]]
    for p, q in zip(points[:-1], points[1:]):
        out += list(np.linspace(p, q, seg + 1)[1:])
    return np.array(out)


def test_bullish_gartley():
    # X 1.00, A 1.10, B 1.10 - 0.618*0.10 = 1.0382, C 1.08 (BC/AB ~0.67), D 1.10 - 0.786*0.10 = 1.0214
    c = np.r_[np.full(20, 1.03), _path([1.03, 1.00, 1.10, 1.0382, 1.08, 1.0214, 1.05])]
    b = _bars(c)
    sig, stop, a, tgt = harmonic_signals(b)
    i = np.flatnonzero(sig)
    assert len(i) == 1 and sig[i[0]] == 1
    d = b["l"][i[0] - 3]
    assert tgt[i[0]] == pytest.approx(d + 0.618 * (b["h"][np.argmax(b["h"][:i[0]])] - d), rel=1e-3)


def test_spring_and_upthrust():
    c = np.full(60, 1.10) + 0.001 * np.sin(np.arange(60))
    b = _bars(c)
    b["l"][50], b["c"][50] = 1.0950, 1.1000                           # dips below the range low, closes back in
    sig, stop, a, tgt = spring_signals(b)
    assert sig[50] == 1 and tgt[50] == pytest.approx(b["h"][10:50].max())
    b2 = _bars(c)
    b2["h"][50], b2["c"][50] = 1.1060, 1.1000
    sig, _, _, tgt = spring_signals(b2)
    assert sig[50] == -1


def test_scalp_cross_and_session_filter():
    c = np.r_[np.full(40, 1.10), np.linspace(1.10, 1.11, 30)]
    b = _bars(c, step=300, ts0=19002 * 86400 + 10 * 3600)           # server 10:00 = London 08:00 (winter)
    sig, xl, xs, allow = scalp_signals(b)
    assert (sig == 1).any() and allow.all()
    b2 = _bars(c, step=300, ts0=19002 * 86400 + 2 * 3600)           # server 02:00 = London 00:00
    assert not scalp_signals(b2)[3].any()
