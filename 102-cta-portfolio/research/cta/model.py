"""Model C "multi-asset trend (CTA)", as pre-registered in docs/01_Vorregistrierung.md (sections 2 and 3).

A market is a dict with "px" (day, p_sig, p_mark, exact, lo, hi), "kind" ("fx", "cfd", "crypto"), "spec" (cost
model of FX/CFD markets) and "cls" (asset class). Books are dense arrays over one calendar of day numbers
(server days for FX/CFDs, UTC days for crypto)."""
from __future__ import annotations

import numpy as np

from carry.model import run_weights
from kry.model import SWAP as CRYPTO_SWAP, trade_cost_rate
from smc.strategy_g import _holiday

CLASSES = ("FX", "Indizes", "Rohstoffe", "Krypto")
LOOKBACKS = {"SCHNELL": (10, 21, 42), "MITTEL": (21, 63, 126, 252), "LANGSAM": (63, 126, 252)}
LOOKBACKS_CRYPTO = {"SCHNELL": (14, 30, 60), "MITTEL": (30, 91, 182, 365), "LANGSAM": (91, 182, 365)}
SETS = tuple(LOOKBACKS)
VOL_WINDOW, VOL_FLOOR, CLASS_VOL, BAND = 60, 0.04, 0.10, 0.25
LEVERAGE = {"FX": 30.0, "Indizes": 15.0, "Rohstoffe": 9.0, "Krypto": 1.0}
WF_START = 16436                                   # 2015-01-01


def annual(kind: str) -> int:
    return 365 if kind == "crypto" else 261


def may_trade(m: dict) -> np.ndarray:
    days = m["px"]["day"]
    if m["kind"] == "crypto":
        return np.ones(len(days), bool)
    return ((days + 3) % 7 <= 3) & ~_holiday(days) & m["px"]["exact"]


def target_path(p: np.ndarray, lookbacks: tuple, sigma_target: float, ann: int, allowed: np.ndarray) -> np.ndarray:
    """Weight held after each row's rebalance: signal x sigma_target / sigma with the 25 % band."""
    n = len(p)
    lr = np.r_[np.nan, np.diff(np.log(p))]
    start = max(max(lookbacks), VOL_WINDOW)
    out = np.zeros(n)
    w = 0.0
    for z in range(n):
        if allowed[z] and z >= start:
            s = np.mean([np.sign(np.log(p[z] / p[z - k])) for k in lookbacks])
            sig = max(float(np.std(lr[z - VOL_WINDOW + 1:z + 1], ddof=1) * np.sqrt(ann)), VOL_FLOOR)
            w_star = s * sigma_target / sig
            if np.sign(w_star) != np.sign(w) or abs(w_star - w) > BAND * abs(w):
                w = w_star
        out[z] = w
    return out


def crypto_rows(px: dict, coin: str, w_end: np.ndarray) -> dict:
    """Accounting of model K (Nr. 101) for a given path of held weights."""
    c, lo, hi = px["p_mark"], px["lo"], px["hi"]
    w_in = np.r_[0.0, w_end[:-1]]
    ret = np.r_[0.0, c[1:] / c[:-1] - 1]
    lo_r = np.r_[0.0, lo[1:] / c[:-1] - 1]
    hi_r = np.r_[0.0, hi[1:] / c[:-1] - 1]
    pnl = w_in * ret
    worst = np.minimum(0.0, np.where(w_in > 0, w_in * lo_r, w_in * hi_r))
    swap = np.abs(w_in) * CRYPTO_SWAP / 365
    trade = np.abs(w_end - w_in) * trade_cost_rate(coin)
    return {"net": pnl - trade - swap, "cost": trade + swap, "worst": worst, "w": w_end, "pnl": pnl}


def cost_rate(m: dict, z: int) -> float:
    """Cost per unit of notional traded at row z."""
    if m["kind"] == "crypto":
        return trade_cost_rate(m["coin"])
    p = float(m["px"]["p_mark"][z])
    return m["spec"].trade_cost(p) / p


def book_market(m: dict, lookbacks: tuple, sigma_target: float, rates) -> dict:
    """Rows of one market: day, net, cost, worst, w (held after the day's rebalance), pnl."""
    px = m["px"]
    w = target_path(px["p_sig"], lookbacks, sigma_target, annual(m["kind"]), may_trade(m))
    if m["kind"] == "crypto":
        r = crypto_rows(px, m["coin"], w)
    else:
        rows = run_weights(m["spec"], px, {int(d): float(x) for d, x in zip(px["day"], w)}, rates)
        r = {k: rows[k] for k in ("net", "cost", "worst", "w", "pnl")}
    r["day"] = px["day"]
    return r


def dense(books: dict, markets: dict, d0: int, d1: int) -> dict:
    """Stack market rows on the calendar d0..d1-1: arrays (days x markets) plus a has-row mask."""
    names = list(markets)
    n = d1 - d0
    out = {k: np.zeros((n, len(names))) for k in ("net", "cost", "worst", "w", "pnl")}
    out["row"] = np.zeros((n, len(names)), bool)
    for j, s in enumerate(names):
        r = books[s]
        sel = (r["day"] >= d0) & (r["day"] < d1)
        idx = (r["day"][sel] - d0).astype(int)
        for k in ("net", "cost", "worst", "w", "pnl"):
            out[k][idx, j] = r[k][sel]
        out["row"][idx, j] = True
        # held weight carries over days without a row (weekends of FX/CFDs)
        held = out["w"][:, j]
        has = out["row"][:, j]
        last = 0.0
        for i in range(n):
            if has[i]:
                last = held[i]
            else:
                held[i] = last
    out["days"] = np.arange(d0, d1)
    out["names"] = names
    out["cls"] = np.array([markets[s]["cls"] for s in names])
    out["lev"] = np.array([LEVERAGE[markets[s]["cls"]] for s in names])
    return out


def sharpe(x: np.ndarray, per_year: float) -> float:
    sd = x.std(ddof=1) if len(x) > 2 else 0.0
    return float(x.mean() / sd * np.sqrt(per_year)) if sd > 0 else -np.inf


def year_start(y: int) -> int:
    return int((np.datetime64(f"{y}-01-01") - np.datetime64("1970-01-01")).astype(int))


def walk_forward(dn: dict[str, dict], years: range) -> dict:
    """Per year and class: chosen lookback set and weight a_c (section 3, C-WF)."""
    base = dn["MITTEL"]
    choice: dict[int, dict] = {}
    for y in years:
        y0 = year_start(y)
        sel, wts, eligible = {}, {}, []
        for c in CLASSES:
            cols = base["cls"] == c
            if y == years[0]:
                sel[c], wts[c] = "MITTEL", 1.0
                continue
            first_pos = np.flatnonzero((np.abs(base["w"][:, cols]).sum(axis=1) > 0) & (base["days"] < y0))
            if len(first_pos) == 0 or y0 - base["days"][first_pos[0]] < 365:
                sel[c], wts[c] = "MITTEL", 1.0
                continue
            best, best_sr = "MITTEL", -np.inf
            for s in SETS:
                b = dn[s]
                live = np.flatnonzero(np.abs(b["w"][:, cols]).sum(axis=1) > 0)
                lo = max(WF_START, int(b["days"][live[0]])) if len(live) else y0
                win = (b["days"] >= lo) & (b["days"] < y0) & b["row"][:, cols].any(axis=1)
                x = b["net"][win][:, cols].sum(axis=1)
                per_year = win.sum() / max((y0 - lo) / 365.25, 1e-9)
                sr = sharpe(x, per_year)
                if sr > best_sr:
                    best, best_sr = s, sr
            sel[c], wts[c] = best, max(best_sr, 0.0)
            eligible.append(c)
        total = sum(wts[c] for c in eligible)
        for c in eligible:
            wts[c] = wts[c] / total * len(eligible) if total > 0 else 0.0
        choice[y] = {"set": sel, "a": wts}
    return choice


def portfolio(dn: dict[str, dict], markets: dict, choice: dict | None) -> dict:
    """Daily portfolio of C-FIX (choice None) or C-WF: net, cost, worst, margin (sum |w| / leverage)."""
    base = dn["MITTEL"]
    n, k = base["net"].shape
    a = np.ones((n, k))
    src = np.full((n, k), SETS.index("MITTEL"))     # index into SETS; C-FIX and years without a choice: MITTEL
    if choice is not None:
        yr = np.asarray(base["days"] * 86400, dtype="datetime64[s]").astype("datetime64[Y]").astype(int) + 1970
        for y, ch in choice.items():
            rows = yr == y
            for j, c in enumerate(base["cls"]):
                a[rows, j] = ch["a"][c]
                src[rows, j] = SETS.index(ch["set"][c])
    pick = lambda key: sum(np.where(src == i, dn[s][key], 0.0) for i, s in enumerate(SETS))
    net, cost, worst, w = pick("net") * a, pick("cost") * a, pick("worst") * a, pick("w") * a
    # transition cost when set or weight changes between consecutive days (only at year starts)
    rates = np.array([[cost_rate(markets[nm], len(markets[nm]["px"]["day"]) - 1) for nm in base["names"]]])
    trans = np.zeros(n)
    jump = np.flatnonzero(((src[1:] != src[:-1]) | (a[1:] != a[:-1])).any(axis=1)) + 1
    for i in jump:
        old = np.zeros(k)
        for idx, s in enumerate(SETS):
            old = old + np.where(src[i - 1] == idx, dn[s]["w"][i - 1], 0.0) * a[i - 1]
        new = np.zeros(k)
        for idx, s in enumerate(SETS):
            new = new + np.where(src[i] == idx, dn[s]["w"][i - 1], 0.0) * a[i]
        trans[i] = float((np.abs(new - old) * rates[0]).sum())
    w_in = np.vstack([np.zeros((1, k)), w[:-1]])
    pnl = pick("pnl") * a
    out = {"days": base["days"], "net": net.sum(axis=1) - trans, "cost": cost.sum(axis=1) + trans,
           "worst": worst.sum(axis=1), "margin": (np.abs(w) / base["lev"]).sum(axis=1),
           "active": (np.abs(w) > 0).any(axis=1), "by_class": {c: net[:, base["cls"] == c].sum(axis=1) for c in CLASSES},
           "long": np.where(w_in > 0, pnl, 0).sum(axis=1), "short": np.where(w_in < 0, pnl, 0).sum(axis=1),
           "trans": trans}
    return out

