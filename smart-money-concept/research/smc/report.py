"""Statistics for the event study: day-clustered Poisson bootstrap and Holm correction."""
from __future__ import annotations

import math

import numpy as np


def clustered_diff(ev: np.ndarray, ev_cl: np.ndarray, pb: np.ndarray, pb_cl: np.ndarray,
                   n_boot: int = 500, seed: int = 0) -> tuple[float, float, float, float]:
    """Mean(event) - mean(placebo) with a Poisson bootstrap over shared clusters (days).

    Returns (diff, ci_low, ci_high, p_two_sided). Clusters are resampled jointly so that
    events and placebos of the same day move together.
    """
    ev_ok, pb_ok = np.isfinite(ev), np.isfinite(pb)
    ev, ev_cl, pb, pb_cl = ev[ev_ok], ev_cl[ev_ok], pb[pb_ok], pb_cl[pb_ok]
    if len(ev) < 20 or len(pb) < 20:
        return np.nan, np.nan, np.nan, np.nan
    cl, inv = np.unique(np.r_[ev_cl, pb_cl], return_inverse=True)
    ec, pc = inv[:len(ev)], inv[len(ev):]
    C = len(cl)
    es, en = np.bincount(ec, ev, C), np.bincount(ec, minlength=C).astype(float)
    ps, pn = np.bincount(pc, pb, C), np.bincount(pc, minlength=C).astype(float)
    obs = es.sum() / en.sum() - ps.sum() / pn.sum()
    rng = np.random.default_rng(seed)
    diffs = []
    for _ in range(0, n_boot, 100):
        w = rng.poisson(1.0, (100, C)).astype(float)
        diffs.append((w @ es) / np.maximum(w @ en, 1) - (w @ ps) / np.maximum(w @ pn, 1))
    d = np.concatenate(diffs)[:n_boot]
    se = d.std(ddof=1)
    z = obs / se if se > 0 else 0.0
    p = math.erfc(abs(z) / math.sqrt(2))
    lo, hi = np.percentile(d, [2.5, 97.5])
    return float(obs), float(lo), float(hi), float(p)


def holm(pvals: list[float]) -> list[float]:
    """Holm-Bonferroni adjusted p-values (NaN stays NaN)."""
    p = np.array(pvals, dtype=float)
    ok = np.isfinite(p)
    idx = np.flatnonzero(ok)
    order = idx[np.argsort(p[ok])]
    m = len(order)
    adj = np.full(len(p), np.nan)
    running = 0.0
    for rank, i in enumerate(order):
        running = max(running, min(1.0, (m - rank) * p[i]))
        adj[i] = running
    return adj.tolist()


def cluster_t(x: np.ndarray, clusters: np.ndarray) -> float:
    """t-value of mean(x) with a cluster-robust (CR1) standard error."""
    n = len(x)
    _, inv = np.unique(clusters, return_inverse=True)
    g = np.bincount(inv, x - x.mean())
    G = len(g)
    if G < 2:
        return np.nan
    var = G / (G - 1) * float((g ** 2).sum()) / n ** 2
    return float(x.mean() / math.sqrt(var)) if var > 0 else np.nan


def cluster_bootstrap_ci(x: np.ndarray, clusters: np.ndarray, n_boot: int = 10_000, seed: int = 0,
                         level: float = 0.95) -> tuple[float, float]:
    """Percentile CI of mean(x), resampling whole clusters (Poisson weights)."""
    _, inv = np.unique(clusters, return_inverse=True)
    s, cnt = np.bincount(inv, x), np.bincount(inv).astype(float)
    rng = np.random.default_rng(seed)
    means = []
    for _ in range(0, n_boot, 500):
        w = rng.poisson(1.0, (500, len(s))).astype(float)
        means.append((w @ s) / np.maximum(w @ cnt, 1))
    m = np.concatenate(means)[:n_boot]
    a = (1 - level) / 2 * 100
    lo, hi = np.percentile(m, [a, 100 - a])
    return float(lo), float(hi)


def profit_factor(x: np.ndarray) -> float:
    loss = -x[x < 0].sum()
    return float(x[x > 0].sum() / loss) if loss > 0 else np.inf
