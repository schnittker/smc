"""Model K "crypto swing trend following", as pre-registered in docs/01_Vorregistrierung.md (section 3)."""
from __future__ import annotations

import numpy as np

VARIANTS = ("K-TSM", "K-LONG")
LOOKBACKS = (7, 14, 28, 56)
VOL_WINDOW, VOL_FLOOR, COIN_VOL = 30, 0.30, 0.10
W_MAX, GROSS_MAX = 0.5, 1.0
BAND = 0.25
MIN_HISTORY = 120
ANNUAL = 365
SPREAD = {"BTC": 0.0005, "ETH": 0.0008, "LTC": 0.0020, "XRP": 0.0020, "ADA": 0.0020}
COMMISSION = 0.000325
SWAP = 0.20


def trade_cost_rate(coin: str) -> float:
    """Cost per unit of nominal traded: half spread + slippage of a quarter spread + commission."""
    return 0.75 * SPREAD[coin] + COMMISSION


def signal(c: np.ndarray, t: int) -> float:
    return float(np.mean([np.sign(np.log(c[t] / c[t - k])) for k in LOOKBACKS]))


def sigma(c: np.ndarray, t: int) -> float:
    r = np.diff(np.log(c[t - VOL_WINDOW:t + 1]))
    return max(float(r.std(ddof=1) * np.sqrt(ANNUAL)), VOL_FLOOR)


def target(variant: str, s: float, sig: float) -> float:
    if variant == "K-LONG":
        s = max(s, 0.0)
    return float(np.clip(s * COIN_VOL / sig, -W_MAX, W_MAX))


def keep(w: float, w_star: float) -> bool:
    """No trade unless the sign changes (incl. to/from 0) or the size moves by more than 25 %."""
    if np.sign(w_star) != np.sign(w):
        return False
    return abs(w_star - w) <= BAND * abs(w)


def run(variant: str, px: dict) -> dict:
    """Daily book per coin (days x coins): w held into the day, pnl, trading cost, swap, worst, net."""
    c, h, l = px["c"], px["h"], px["l"]
    n, m = c.shape
    first = np.array([int(np.argmax(np.isfinite(c[:, j]))) for j in range(m)])
    out = {k: np.zeros((n, m)) for k in ("w", "pnl", "cost", "swap", "worst", "net")}
    rates = np.array([trade_cost_rate(x) for x in px["coins"]])
    w = np.zeros(m)
    for t in range(1, n):
        live = np.isfinite(c[t]) & np.isfinite(c[t - 1])
        ret = np.where(live, c[t] / np.where(live, c[t - 1], 1.0) - 1, 0.0)
        out["w"][t] = w
        out["pnl"][t] = w * ret
        lo = np.where(live, l[t] / np.where(live, c[t - 1], 1.0) - 1, 0.0)
        hi = np.where(live, h[t] / np.where(live, c[t - 1], 1.0) - 1, 0.0)
        out["worst"][t] = np.minimum(0.0, np.where(w > 0, w * lo, w * hi))
        out["swap"][t] = np.abs(w) * SWAP / ANNUAL
        w_star = np.zeros(m)
        for j in range(m):
            if live[j] and t - first[j] >= MIN_HISTORY:
                w_star[j] = target(variant, signal(c[:, j], t), sigma(c[:, j], t))
        gross = np.abs(w_star).sum()
        if gross > GROSS_MAX:
            w_star *= GROSS_MAX / gross
        new = np.array([w[j] if keep(w[j], w_star[j]) else w_star[j] for j in range(m)])
        gross = np.abs(new).sum()
        if gross > GROSS_MAX:                     # kept positions plus new ones may still exceed 1:1
            new *= GROSS_MAX / gross
        out["cost"][t] = np.abs(new - w) * rates
        w = new
    out["net"] = out["pnl"] - out["cost"] - out["swap"]
    out["w_end"] = np.vstack([out["w"][1:], w[None, :]])
    return out
