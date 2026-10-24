"""Daily book, inverse-volatility weights and the FTMO simulation of the swing portfolio
(docs/01_Vorregistrierung.md, sections 3 and 4).

A component series is a dict {server day: (net, worst, active, cost)} with net, worst and cost (trading costs plus
swap charges) as fractions of capital at the component's native size. Server day = trading day that closes 17:00 New York (smc.timez.fx_day).
"""
from __future__ import annotations

import numpy as np

from smc import timez

COMPONENTS = ("P-SPX", "T-FRÜH", "V-VOL", "F-CARRY")
ANNUAL = 261
COMPONENT_VOL = 0.10
LEVELS = (0.005, 0.0075, 0.010, 0.0125)
PHASE2_FACTOR = 0.75
TARGETS = (0.10, 0.05)
DAILY_LIMIT, TOTAL_LIMIT = 0.05, 0.10
DERISK = ((0.97, 0.5), (0.94, 0.25))          # equity at or below 97 % -> half size, at or below 94 % -> quarter
MIN_DAYS = 4
MAX_MONTHS = 60
MAX_US500_NOTIONAL = 10.0
DAYS_PER_MONTH = 21.75


def book_trades(rows: np.ndarray) -> dict:
    """Event trades (fomc ROW_DTYPE): net and full-trade MAE on the server day of the exit."""
    out: dict[int, tuple] = {}
    for d, net, mae, cost in zip(timez.fx_day(rows["t_exit"]).tolist(), rows["net_bp"].tolist(), rows["mae_bp"].tolist(),
                                 rows["cost_bp"].tolist()):
        n0, w0, _, c0 = out.get(d, (0.0, 0.0, True, 0.0))
        out[d] = (n0 + net / 1e4, w0 + mae / 1e4, True, c0 + cost / 1e4)
    return out


def book_daily(rows: np.ndarray) -> dict:
    """Daily rows (DAY_DTYPE of model G/carry): net and worst per row; active while a weight is held."""
    out: dict[int, tuple] = {}
    for d, net, worst, w, pnl, cost in zip(rows["day"].tolist(), rows["net"].tolist(), rows["worst"].tolist(),
                                           rows["w"].tolist(), rows["pnl"].tolist(), rows["cost"].tolist()):
        n0, w0, a0, c0 = out.get(d, (0.0, 0.0, False, 0.0))
        out[d] = (n0 + net, w0 + worst, a0 or w != 0.0 or pnl != 0.0, c0 + cost)
    return out


def book_events(rows: np.ndarray, log: list) -> dict:
    """Model F: per event the net of the traded pairs on entry and exit day, booked on the exit day, and the
    sum of the pairs' worst values on the exit day."""
    out: dict[int, tuple] = {}
    for d0, d1, traded in log:
        if not traded:
            continue
        pair = np.isin(rows["symbol"], traded)
        both = pair & np.isin(rows["day"], [d0, d1])
        net, cost = float(rows["net"][both].sum()), float(rows["cost"][both].sum())
        worst = float(rows["worst"][pair & (rows["day"] == d1)].sum())
        n0, w0, _, c0 = out.get(d1, (0.0, 0.0, True, 0.0))
        out[d1] = (n0 + net, w0 + worst, True, c0 + cost)
    return out


def align(series: dict[str, dict], lo: int, hi: int) -> dict:
    """Calendar = union of all booked server days in [lo, hi) Mon-Fri; matrices (days x components)."""
    days = sorted({d for s in series.values() for d in s if lo <= d < hi and (d + 3) % 7 < 5})
    days = np.array(days, dtype=np.int64)
    n, k = len(days), len(series)
    net, worst, cost, act = np.zeros((n, k)), np.zeros((n, k)), np.zeros((n, k)), np.zeros((n, k), bool)
    pos = {d: i for i, d in enumerate(days.tolist())}
    for j, s in enumerate(series.values()):
        for d, (x, w, a, c) in s.items():
            if d in pos:
                i = pos[d]
                net[i, j], worst[i, j], act[i, j], cost[i, j] = x, w, a, c
    return {"days": days, "net": net, "worst": worst, "cost": cost, "active": act, "names": list(series)}


def inverse_vol_weights(net: np.ndarray) -> np.ndarray:
    """g_c = 10 % / (sigma_c * sqrt(261)) from the daily component series (columns)."""
    return COMPONENT_VOL / (net.std(axis=0, ddof=1) * np.sqrt(ANNUAL))


def month_of(days: np.ndarray) -> np.ndarray:
    return np.asarray(days * timez.DAY, dtype="datetime64[s]").astype("datetime64[M]").astype(np.int64)


def month_blocks(days: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Start index and length of each calendar month in a sorted day array."""
    m = month_of(days)
    starts = np.r_[0, np.flatnonzero(np.diff(m)) + 1]
    return starts, np.diff(np.r_[starts, len(days)])


def derisk(e: np.ndarray) -> np.ndarray:
    f = np.ones_like(e)
    for level, factor in DERISK:
        f = np.where(e <= level, factor, f)
    return f


def run_phase(r, w, act, starts, lens, months, scale, target, m0=None, p0=None):
    """Simulate one FTMO phase for many paths at once.

    r, w, act: portfolio net, worst and activity per day (already weighted, unscaled).
    months: (paths x max months) indices into the month blocks, -1 = no more data.
    Returns status (1 passed, 2 failed, 0 unresolved), trading days used and the end position (month, pos)."""
    n_paths, max_m = months.shape
    m_i = np.zeros(n_paths, np.int64) if m0 is None else m0.copy()
    p_i = np.zeros(n_paths, np.int64) if p0 is None else p0.copy()
    e = np.ones(n_paths)
    status = np.zeros(n_paths, np.int8)
    used = np.zeros(n_paths, np.int64)
    active = np.zeros(n_paths, np.int64)
    rows = np.arange(n_paths)
    while True:
        run = status == 0
        run &= m_i < max_m
        blk = np.where(run, months[rows, np.minimum(m_i, max_m - 1)], -1)
        run &= blk >= 0
        if not run.any():
            break
        idx = starts[np.maximum(blk, 0)] + p_i
        k = scale * derisk(e)
        loss = k * np.minimum(w[idx], np.minimum(r[idx], 0.0))
        fail = run & ((loss <= -DAILY_LIMIT) | (e + loss <= 1.0 - TOTAL_LIMIT))
        e = np.where(run & ~fail, e + k * r[idx], e)
        active += run & act[idx]
        used += run
        status[fail] = 2
        done = run & ~fail & (e >= 1.0 + target) & (active >= MIN_DAYS)
        status[done] = 1
        p_i = np.where(run, p_i + 1, p_i)
        nxt = run & (p_i >= lens[np.maximum(blk, 0)])
        m_i = np.where(nxt, m_i + 1, m_i)
        p_i = np.where(nxt, 0, p_i)
    return status, used, m_i, p_i


def bootstrap(r, w, act, days, scale, n_paths=10_000, seed=0) -> dict:
    """Both phases with independently drawn calendar months (with replacement), at most 60 months each."""
    starts, lens = month_blocks(days)
    rng = np.random.default_rng(seed)
    m1 = rng.integers(0, len(starts), (n_paths, MAX_MONTHS))
    m2 = rng.integers(0, len(starts), (n_paths, MAX_MONTHS))
    s1, u1, _, _ = run_phase(r, w, act, starts, lens, m1, scale, TARGETS[0])
    s2, u2, _, _ = run_phase(r, w, act, starts, lens, m2, scale * PHASE2_FACTOR, TARGETS[1])
    both = (s1 == 1) & (s2 == 1)
    dur = (u1 + u2)[both] / DAYS_PER_MONTH
    return {"p1": float((s1 == 1).mean()), "p2": float((s2 == 1).mean()), "both": float(both.mean()),
            "median_months": float(np.median(dur)) if both.any() else np.nan}


def historical(r, w, act, days, scale) -> dict:
    """Start on the first day of every calendar month on the real path; phase 2 starts the day after phase 1."""
    starts, lens = month_blocks(days)
    nm = len(starts)
    months = np.arange(nm)[:, None] + np.arange(nm)[None, :]
    months = np.where(months < nm, months, -1)
    s1, u1, m_e, p_e = run_phase(r, w, act, starts, lens, months, scale, TARGETS[0])
    s2, u2, _, _ = run_phase(r, w, act, starts, lens, months, scale * PHASE2_FACTOR, TARGETS[1], m_e, p_e)
    s2 = np.where(s1 == 1, s2, s1)
    both = s2 == 1
    resolved = (s2 == 1) | (s2 == 2)
    return {"starts": nm, "resolved": int(resolved.sum()), "passed": int(both.sum()),
            "median_months": float(np.median((u1 + u2)[both] / DAYS_PER_MONTH)) if both.any() else np.nan}
