import numpy as np

from smc.data.bars import BAR_DTYPE
from smc.timez import server_to_utc
from mlx.model import features, labels, sequences, walk_forward


def _bars(n, step=3600, seed=0, start="2014-01-06"):
    rng = np.random.default_rng(seed)
    ts0 = (np.datetime64(start) - np.datetime64("1970-01-01")).astype("timedelta64[s]").astype(np.int64)
    c = 1.1 * np.exp(np.cumsum(0.001 * rng.standard_normal(n)))
    o = np.r_[c[0], c[:-1]]
    rows = [(int(server_to_utc(ts0 + step * j)), ts0 + step * j, o[j], max(o[j], c[j]) + 1e-4, min(o[j], c[j]) - 1e-4,
             c[j], 60) for j in range(n)]
    return np.array(rows, dtype=BAR_DTYPE)


def test_shapes_and_labels():
    b = _bars(800)
    f = features(b, "EURUSD")
    assert f.shape == (800, 15) and np.isfinite(f[600]).all()
    s = sequences(b)
    assert s.shape == (800, 24) and np.isnan(s[499]).any() and np.isfinite(s[600]).all()
    y = labels(b)
    assert y[10] == float(b["o"][17] > b["o"][11]) and np.isnan(y[-1])


def test_walk_forward_predicts_only_target_year_and_is_random_on_noise():
    b = _bars(3 * 52 * 5 * 24)                      # about three years of hourly bars
    p = walk_forward("ML-GBM", {"EURUSD": b}, [2016])["EURUSD"]
    yr = np.asarray(b["ts"], dtype="datetime64[s]").astype("datetime64[Y]").astype(int) + 1970
    assert np.isnan(p[yr < 2016]).all() and np.isfinite(p[yr == 2016]).mean() > 0.9
    y = labels(b)
    sel = (yr == 2016) & np.isfinite(p) & np.isfinite(y)
    hit = ((p[sel] > 0.5) == (y[sel] == 1)).mean()
    assert 0.45 < hit < 0.55                       # pure noise: no predictive power
