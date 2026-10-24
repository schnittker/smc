"""Model ML 'machine learning' (strategies no. 83, 84 and 86), as pre-registered in docs/01_Vorregistrierung.md.

Walk-forward: the model for year Y is trained on 2014 .. Y-1 only (labels whose window reaches into Y dropped).
  ML-GBM   HistGradientBoosting on H1 features -> P(O(i+7) > O(i+1)); > 0.55 long, < 0.45 short, 6 bars, stop 2 ATR
  ML-MLP   MLP (32/16) on the last 24 H1 returns / s, same trading rule
  ML-META  Supertrend H4 base trades (no. 71) filtered by a GBM that predicts a positive net result (p > 0.55)
"""
from __future__ import annotations

import numpy as np
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.neural_network import MLPClassifier

from chart.engine import DAY
from hkb.model import atr, ema, swap_frac
from osc.model import rsi
from smc.timez import eu_dst
from tind.indicators import supertrend

VARIANTS = {"ML-GBM": "H1", "ML-META": "H4", "ML-MLP": "H1"}
LIST_NO = {"ML-GBM": 83, "ML-META": 84, "ML-MLP": 86}
CLASS = {"XAUUSD": 1, "XAGUSD": 1, "SPXUSD": 2, "NSXUSD": 2, "FRXEUR": 2, "UKXGBP": 2, "JPXJPY": 2, "HKXHKD": 2,
         "AUXAUD": 2, "BCOUSD": 3}
H, STEP, P_HI, P_LO, SEQ, S_N, FIRST_YEAR = 6, 6, 0.55, 0.45, 24, 500, 2014


def year_of_ts(ts: np.ndarray) -> np.ndarray:
    return np.asarray(ts, dtype="datetime64[s]").astype("datetime64[Y]").astype(int) + 1970


def _roll_std(x: np.ndarray, n: int) -> np.ndarray:
    out = np.full(len(x), np.nan)
    ok = np.isfinite(x)
    if len(x) > n:
        w = np.lib.stride_tricks.sliding_window_view(np.where(ok, x, 0.0), n)
        out[n - 1:] = w.std(axis=1)
    return out


def features(bars, symbol: str, with_time: bool = True) -> np.ndarray:
    o, h, l, c, t = bars["o"], bars["h"], bars["l"], bars["c"], bars["t"]
    lc = np.log(c)
    r1 = np.r_[np.nan, np.diff(lc)]
    s = _roll_std(r1, S_N)
    cols = []
    for n in (1, 3, 6, 12, 24, 48):
        r = np.r_[np.full(n, np.nan), lc[n:] - lc[:-n]]
        cols.append(r / (s * np.sqrt(n)))
    cols.append(rsi(c))
    for n in (20, 100):
        cols.append((lc - np.log(ema(c, n))) / (s * np.sqrt(n)))
    cols.append(_roll_std(r1, 24) / s)
    hh = np.r_[np.full(23, np.nan), np.lib.stride_tricks.sliding_window_view(h, 24).max(axis=1)]
    ll = np.r_[np.full(23, np.nan), np.lib.stride_tricks.sliding_window_view(l, 24).min(axis=1)]
    with np.errstate(invalid="ignore", divide="ignore"):
        cols.append((c - ll) / (hh - ll))
    if with_time:
        mins = ((t + 3600 * eu_dst(t).astype(np.int64)) % 86400) / 60.0
        cols += [np.sin(2 * np.pi * mins / 1440), np.cos(2 * np.pi * mins / 1440)]
    cols.append(((bars["ts"] // DAY) + 3) % 7)
    cols.append(np.full(len(c), CLASS.get(symbol, 0), float))
    return np.column_stack(cols)


def sequences(bars) -> np.ndarray:
    lc = np.log(bars["c"])
    r1 = np.r_[np.nan, np.diff(lc)]
    s = _roll_std(r1, S_N)
    z = r1 / s
    out = np.full((len(z), SEQ), np.nan)
    for k in range(SEQ):                                  # out[i, k] = z(i - 23 + k)
        out[SEQ - 1:, k] = z[k:len(z) - SEQ + 1 + k]
    return out


def labels(bars) -> np.ndarray:
    o = bars["o"]
    y = np.full(len(o), np.nan)
    y[:-(H + 1)] = (o[H + 1:] > o[1:-H]).astype(float)
    return y


def make_model(variant: str):
    if variant == "ML-MLP":
        return MLPClassifier(hidden_layer_sizes=(32, 16), alpha=1e-3, early_stopping=True, max_iter=200,
                             random_state=0)
    return HistGradientBoostingClassifier(max_iter=200, learning_rate=0.05, max_leaf_nodes=15, l2_regularization=1.0,
                                          random_state=0)


def walk_forward(variant: str, data: dict, years) -> dict[str, np.ndarray]:
    """P(up) per H1 bar of each symbol for the bars in `years` (NaN elsewhere). data[s] = H1 bars."""
    xs = {s: (sequences(b) if variant == "ML-MLP" else features(b, s)) for s, b in data.items()}
    ys = {s: labels(b) for s, b in data.items()}
    yrs = {s: year_of_ts(b["ts"]) for s, b in data.items()}
    out = {s: np.full(len(b), np.nan) for s, b in data.items()}
    for y in years:
        start = (np.datetime64(f"{y}-01-01") - np.datetime64("1970-01-01")).astype("timedelta64[s]").astype(np.int64)
        X, Y = [], []
        for s, b in data.items():
            idx = np.arange(len(b))
            end_ts = np.r_[b["ts"][H + 1:], np.full(H + 1, np.iinfo(np.int64).max)]
            sel = (yrs[s] >= FIRST_YEAR) & (idx % STEP == 0) & (end_ts < start) & np.isfinite(ys[s]) \
                & np.isfinite(xs[s]).all(axis=1)
            X.append(xs[s][sel])
            Y.append(ys[s][sel])
        X, Y = np.concatenate(X), np.concatenate(Y)
        if len(Y) < 1000:
            continue
        model = make_model(variant).fit(X, Y)
        for s, b in data.items():
            sel = (yrs[s] == y) & np.isfinite(xs[s]).all(axis=1)
            if sel.any():
                out[s][sel] = model.predict_proba(xs[s][sel])[:, 1]
    return out


# ---------------------------------------------------------------- meta-labeling
def base_trades(symbol: str, bars, cost, rates, cfd, st: np.ndarray) -> list[tuple[int, int, int, float]]:
    """Supertrend base trades: (signal bar j, direction, last bar held, net result as a fraction of the entry)."""
    o, h, l, c, t = bars["o"], bars["h"], bars["l"], bars["c"], bars["t"]
    a14 = atr(h, l, c, 14)
    n = len(bars)
    ch = np.flatnonzero(np.r_[False, st[1:] != st[:-1]])
    out = []
    for q, j in enumerate(ch):
        d = int(st[j])
        if d == 0 or j + 1 >= n or not np.isfinite(a14[j]):
            continue
        k = j + 1
        j_next = ch[q + 1] if q + 1 < len(ch) else n - 1
        p = o[k]
        sp, slip = cost.spread(p), cost.slip(p)
        entry = p + sp + slip if d == 1 else p - slip
        stop = entry - 3 * a14[j] if d == 1 else entry + 3 * a14[j]
        px, last, t_exit = None, j_next, None
        for m in range(k, min(j_next + 1, n)):
            if d == 1 and l[m] <= stop:
                px, last, t_exit = min(stop, o[m]) - slip, m, int(t[m])
                break
            if d == -1 and h[m] + sp >= stop:
                px, last, t_exit = max(stop, o[m] + sp) + slip, m, int(t[m])
                break
        if px is None:
            e = min(j_next + 1, n - 1)
            px = o[e] - slip if d == 1 else o[e] + sp + slip
            last, t_exit = e - 1, int(t[e])
        net = d * (px - entry) - cost.commission(entry)
        net += swap_frac(symbol, d, int(t[k]), t_exit, rates, cfd) * entry
        out.append((int(j), d, int(last), float(net / entry)))
    return out


def meta_states(data: dict, years, costs: dict, rates, cfds: dict) -> dict[str, np.ndarray]:
    """Supertrend states with the base entries the meta model rejects set to flat until the next change."""
    st = {s: supertrend(b["h"], b["l"], b["c"]) for s, b in data.items()}
    feats = {s: features(b, s, with_time=False) for s, b in data.items()}
    trades = {s: base_trades(s, b, costs[s], rates, cfds[s], st[s]) for s, b in data.items()}
    yrs = {s: year_of_ts(b["ts"]) for s, b in data.items()}
    out = {s: v.copy() for s, v in st.items()}
    for y in years:
        start = (np.datetime64(f"{y}-01-01") - np.datetime64("1970-01-01")).astype("timedelta64[s]").astype(np.int64)
        X, Y = [], []
        for s, b in data.items():
            for j, d, last, net in trades[s]:
                if yrs[s][j] >= FIRST_YEAR and b["ts"][min(last + 1, len(b) - 1)] < start and np.isfinite(feats[s][j]).all():
                    X.append(np.r_[feats[s][j], d])
                    Y.append(float(net > 0))
        if len(Y) < 200 or len(set(Y)) < 2:
            continue
        model = make_model("ML-GBM").fit(np.array(X), np.array(Y))
        for s, b in data.items():
            ch = np.flatnonzero(np.r_[False, st[s][1:] != st[s][:-1]])
            for q, j in enumerate(ch):
                if yrs[s][j] != y or st[s][j] == 0:
                    continue
                f = feats[s][j]
                p = model.predict_proba(np.r_[f, st[s][j]][None, :])[0, 1] if np.isfinite(f).all() else 0.0
                if p <= P_HI:
                    j_next = ch[q + 1] if q + 1 < len(ch) else len(b)
                    out[s][j:j_next] = 0
    return out
