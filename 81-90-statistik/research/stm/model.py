"""Model ST 'statistical models' (strategies no. 81, 82, 85 and 90), as pre-registered in docs/01_Vorregistrierung.md.

r(d) = ln p_mark(d) - ln p_mark(d-1); models of year Y are estimated on the days 2014 .. Y-1 only.
  ST-HMM    2-state Gaussian HMM; 20-day momentum sign while P(calm) > 0.5, else flat; 10 % / sigma at changes
  ST-GARCH  GARCH(1,1); 20-day momentum sign sized 10 % / sqrt(252 h(d+1)), reset at changes and each week's first day
  ST-KNN    sign of the mean next-day (sigma-scaled) return of the 20 nearest 10-day patterns; 10 % / sigma at changes
  ST-GOLD   XAUUSD long from the last August to the last September mark and the last October to the last November
            mark; 10 % / sigma
"""
from __future__ import annotations

from datetime import date

import numpy as np
from scipy.optimize import minimize
from scipy.signal import lfilter

from carry.model import apply_days, ewma_sigma, run_weights
from smc.strategy_g import VOL_TARGET
from smc.swaps import RateTable

VARIANTS = ("ST-HMM", "ST-GARCH", "ST-KNN", "ST-GOLD")
EPOCH = date(1970, 1, 1)
FIRST_YEAR, MOM_N, HMM_ITERS, KNN_K, KNN_LAGS = 2014, 20, 100, 20, 10


def year_of(days: np.ndarray) -> np.ndarray:
    return np.asarray(days * 86400, dtype="datetime64[s]").astype("datetime64[Y]").astype(int) + 1970


def log_returns(px: dict) -> np.ndarray:
    return np.r_[np.nan, np.diff(np.log(px["p_mark"]))]


# ---------------------------------------------------------------- HMM
def _emis(x, mu, var):
    return np.exp(-0.5 * (x[:, None] - mu) ** 2 / var) / np.sqrt(2 * np.pi * var)


def hmm_fit(x: np.ndarray, iters: int = HMM_ITERS) -> tuple:
    v = x.var()
    pi, a = np.array([0.5, 0.5]), np.array([[0.95, 0.05], [0.05, 0.95]])
    mu, var = np.zeros(2), np.array([0.5 * v, 2.0 * v])
    n = len(x)
    for _ in range(iters):
        b = _emis(x, mu, var) + 1e-300
        al, c = np.empty((n, 2)), np.empty(n)
        al[0] = pi * b[0]
        c[0] = al[0].sum()
        al[0] /= c[0]
        for t in range(1, n):
            al[t] = (al[t - 1] @ a) * b[t]
            c[t] = al[t].sum()
            al[t] /= c[t]
        be = np.empty((n, 2))
        be[-1] = 1.0
        for t in range(n - 2, -1, -1):
            be[t] = (a @ (b[t + 1] * be[t + 1])) / c[t + 1]
        g = al * be
        g /= g.sum(axis=1, keepdims=True)
        xi = (al[:-1, :, None] * a[None] * (b[1:] * be[1:])[:, None, :]) / c[1:, None, None]
        pi = g[0]
        a = xi.sum(axis=0) / g[:-1].sum(axis=0)[:, None]
        a /= a.sum(axis=1, keepdims=True)
        w = g.sum(axis=0)
        mu = (g * x[:, None]).sum(axis=0) / w
        var = np.maximum((g * (x[:, None] - mu) ** 2).sum(axis=0) / w, 1e-12)
    order = np.argsort(var)
    return pi[order], a[np.ix_(order, order)], mu[order], var[order]


def hmm_filter(x: np.ndarray, params) -> np.ndarray:
    """Filtered P(state 0 = calm) per element of x (NaN entries carry the prediction forward)."""
    pi, a, mu, var = params
    p = pi.copy()
    out = np.full(len(x), np.nan)
    for t, xt in enumerate(x):
        p = p @ a if t else p
        if np.isfinite(xt):
            p = p * _emis(np.array([xt]), mu, var)[0]
            p = p / p.sum() if p.sum() > 0 else np.array([0.5, 0.5])
        out[t] = p[0]
    return out


# ---------------------------------------------------------------- GARCH
def garch_fit(x: np.ndarray) -> tuple[float, float, float]:
    v0 = x.var()

    x2 = x ** 2

    def nll(th):                                   # th[0] = w / v0 keeps the parameters on one scale
        w, al, be = th[0] * v0, th[1], th[2]
        if al + be >= 0.999:
            return 1e10
        # h(t) = w + al x(t-1)^2 + be h(t-1), h(0) = v0
        u = np.r_[v0, w + al * x2[:-1]]
        h = lfilter([1.0], [1.0, -be], u)
        return 0.5 * np.sum(np.log(h) + x2 / h)
    res = minimize(nll, x0=[0.05, 0.05, 0.90], method="L-BFGS-B", bounds=[(1e-6, 10.0), (0.0, 0.5), (0.0, 0.999)])
    return float(res.x[0] * v0), float(res.x[1]), float(res.x[2])


def garch_forecast(x: np.ndarray, params, v0: float) -> np.ndarray:
    """h(t+1) given returns up to t (NaN returns leave h unchanged)."""
    w, al, be = params
    h, out = v0, np.full(len(x), np.nan)
    for t, xt in enumerate(x):
        if np.isfinite(xt):
            h = w + al * xt ** 2 + be * h
        out[t] = h
    return out


# ---------------------------------------------------------------- signals
def momentum_sign(px: dict) -> np.ndarray:
    lp = np.log(px["p_mark"])
    s = np.zeros(len(lp))
    s[MOM_N:] = np.sign(lp[MOM_N:] - lp[:-MOM_N])
    return s


def _by_year_params(days, x, years, fit):
    out = {}
    yr = year_of(days)
    for y in years:
        train = x[(yr >= FIRST_YEAR) & (yr < y) & np.isfinite(x)]
        if len(train) >= 200:
            out[y] = fit(train)
    return out


def targets(variant: str, px: dict, first_year: int, last_year: int) -> dict[int, float]:
    days = px["day"]
    x = log_returns(px)
    sigma = ewma_sigma(x)
    yr = year_of(days)
    years = range(first_year, last_year + 1)
    sig = np.zeros(len(days))
    size = np.full(len(days), np.nan)
    weekly = np.zeros(len(days), bool)
    if variant == "ST-HMM":
        mom = momentum_sign(px)
        for y, prm in _by_year_params(days, x, years, hmm_fit).items():
            p_calm = hmm_filter(np.where(yr >= FIRST_YEAR, x, np.nan), prm)
            sel = yr == y
            sig[sel] = np.where(p_calm[sel] > 0.5, mom[sel], 0.0)
        size = VOL_TARGET / sigma
    elif variant == "ST-GARCH":
        mom = momentum_sign(px)
        for y, prm in _by_year_params(days, x, years, garch_fit).items():
            train = x[(yr >= FIRST_YEAR) & (yr < y) & np.isfinite(x)]
            h = garch_forecast(np.where(yr >= FIRST_YEAR, x, np.nan), prm, float(train.var()))
            sel = yr == y
            sig[sel] = mom[sel]
            size[sel] = VOL_TARGET / np.sqrt(252 * h[sel])
        wk = (days + 3) // 7
        weekly[1:] = wk[1:] != wk[:-1]
    elif variant == "ST-KNN":
        sd = sigma / np.sqrt(252)
        feats = np.full((len(days), KNN_LAGS), np.nan)
        for k in range(KNN_LAGS):                                  # feats[d, k] = r(d - 9 + k)
            feats[KNN_LAGS - 1:, k] = x[k:len(x) - KNN_LAGS + 1 + k]
        feats = feats / sd[:, None]
        label = np.r_[x[1:], np.nan] / sd
        valid = np.isfinite(feats).all(axis=1) & np.isfinite(label) & (yr >= FIRST_YEAR)
        for d in np.flatnonzero((yr >= first_year) & (yr <= last_year)):
            if not np.isfinite(feats[d]).all():
                continue
            tr = np.flatnonzero(valid[:max(0, d - 1)])          # t + 1 <= d - 1
            if len(tr) < KNN_K:
                continue
            dist = ((feats[tr] - feats[d]) ** 2).sum(axis=1)
            nn = tr[np.argpartition(dist, KNN_K - 1)[:KNN_K]]
            sig[d] = np.sign(label[nn].mean())
        size = VOL_TARGET / sigma
    elif variant == "ST-GOLD":
        months = np.asarray(days * 86400, dtype="datetime64[s]").astype("datetime64[M]").astype(int) % 12 + 1
        exact = px["exact"]
        on = False
        for i in range(len(days) - 1):
            if not exact[i] or not (first_year <= yr[i] <= last_year):
                sig[i] = 1.0 if on else 0.0
                continue
            nxt = i + 1
            last_of_month = months[nxt] != months[i]
            if last_of_month and months[i] in (8, 10):
                on = True
            elif last_of_month and months[i] in (9, 11):
                on = False
            sig[i] = 1.0 if on else 0.0
        size = VOL_TARGET / sigma
    else:
        raise ValueError(variant)
    out, cur = {}, 0.0
    for i in range(1, len(days)):
        if not (first_year <= yr[i] <= last_year) or not px["exact"][i]:
            continue
        s = sig[i]
        if s != cur or (weekly[i] and s != 0):
            if s != 0 and not np.isfinite(size[i]):
                continue
            out[int(days[i])] = float(s * size[i]) if s != 0 else 0.0
            cur = s
    return out


def run_symbol(variant: str, spec, px: dict, rates: RateTable, first_year: int, last_year: int) -> np.ndarray:
    return run_weights(spec, px, apply_days(px, targets(variant, px, first_year, last_year)), rates)
