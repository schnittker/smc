"""Model E 'daily patterns' (strategies no. 43 and 44), as pre-registered in docs/01_Vorregistrierung.md.

Server-day D1 bars (dbo.model.server_days). A position runs from the open of the first M5 bar of server day i to the
close of its last M5 bar; no stop. Notional = min(0.5 % / (ATR14(i-1) / price), 10) x capital (Wilder ATR of the
D1 bars up to i-1).
  E-REV   |C(i-1) - C(i-2)| > 2 ATR14(i-2) -> against that move on day i
  E-CONT  same signal -> with that move
  E-WD    per year Y the weekday with the largest |t| of open-to-close returns over 2014 .. Y-1, if |t| >= 2,
          traded in the direction of its mean on every such weekday of year Y
No trading on server days 24.12.-01.01.
"""
from __future__ import annotations

from datetime import date

import numpy as np

from dbo.model import EPOCH, Costs, holiday, server_days
from hkb.model import atr

VARIANTS = ("E-REV", "E-CONT", "E-WD")
RISK_ATR, LEVER_CAP, BIG, WD_T, FIRST_YEAR = 0.005, 10.0, 2.0, 2.0, 2014
NONE, EOD = 3, 2

ROW_DTYPE = np.dtype([
    ("day", "i8"), ("dir", "i1"), ("atr_bp", "f8"), ("notional", "f8"), ("r_atr", "f8"), ("net_bp", "f8"),
    ("cost_bp", "f8"), ("gross_bp", "f8"),
])


def year_of(day: int) -> int:
    return date.fromordinal(EPOCH.toordinal() + int(day)).year


def weekday_choice(d1: dict, year: int) -> tuple[int, int, float]:
    """(weekday 0-4 or -1, direction, t) chosen from the open-to-close returns of 2014 .. year-1."""
    days = d1["day"]
    yrs = np.array([year_of(x) for x in days])
    sel = (yrs >= FIRST_YEAR) & (yrs < year)
    r = (d1["c"] / d1["o"] - 1)[sel]
    wd = ((days + 3) % 7)[sel]
    best = (-1, 0, 0.0)
    for w in range(5):
        x = r[wd == w]
        if len(x) < 20:
            continue
        t = x.mean() / (x.std(ddof=1) / np.sqrt(len(x)))
        if abs(t) > abs(best[2]):
            best = (w, 1 if t > 0 else -1, float(t))
    return best if abs(best[2]) >= WD_T else (-1, 0, best[2])


def directions(variant: str, d1: dict) -> np.ndarray:
    n = len(d1["day"])
    c = d1["c"]
    a = atr(d1["h"], d1["l"], c, 14)
    out = np.zeros(n, np.int8)
    if variant in ("E-REV", "E-CONT"):
        for i in range(2, n):
            move = c[i - 1] - c[i - 2]
            if np.isfinite(a[i - 2]) and abs(move) > BIG * a[i - 2]:
                s = 1 if move > 0 else -1
                out[i] = -s if variant == "E-REV" else s
    elif variant == "E-WD":
        choice: dict[int, tuple] = {}
        for i in range(n):
            y = year_of(d1["day"][i])
            if y <= FIRST_YEAR:
                continue
            if y not in choice:
                choice[y] = weekday_choice(d1, y)
            w, d, _ = choice[y]
            if w >= 0 and (d1["day"][i] + 3) % 7 == w:
                out[i] = d
    else:
        raise ValueError(variant)
    return out


def run_symbol(variant: str, m5: np.ndarray, cost: Costs, day_from: int, day_to: int) -> np.ndarray:
    """One row per server day in [day_from, day_to); days without a position have dir 0."""
    d1 = server_days(m5)
    dirs = directions(variant, d1)
    a = atr(d1["h"], d1["l"], d1["c"], 14)
    rows = []
    for i in range(1, len(d1["day"])):
        day = int(d1["day"][i])
        if day < day_from or day >= day_to or holiday(day):
            continue
        d = int(dirs[i])
        if d == 0 or not np.isfinite(a[i - 1]):
            rows.append((day, 0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0))
            continue
        o, c = d1["o"][i], d1["c"][i]
        sp, slip = cost.spread(o), cost.slip(o)
        entry = o + sp + slip if d == 1 else o - slip
        px = c - slip if d == 1 else c + sp + slip
        comm = cost.commission(entry)
        move = d * (px - entry) - comm
        gross = d * (c - o)
        notional = min(RISK_ATR / (a[i - 1] / entry), LEVER_CAP)
        rows.append((day, d, a[i - 1] / entry * 1e4, notional, move / a[i - 1], notional * move / entry * 1e4,
                     notional * (gross - move) / entry * 1e4, notional * gross / entry * 1e4))
    return np.array(rows, dtype=ROW_DTYPE)
