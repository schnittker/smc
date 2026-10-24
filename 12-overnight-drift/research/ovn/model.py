"""Model N 'overnight drift US500', as pre-registered in docs/01_Vorregistrierung.md.

Long US500 from 16:00 New York on trading day p to 09:30 on the next trading day d (N-NACHT), or from 02:00 to
03:00 New York on d (N-EU), the latter optionally only when p's close-to-close return was negative (N-EU-DOWN,
Boyarchenko, Larsen & Whelan 2023). Position mechanics, costs, swaps and emergency stop are those of strategy
no. 9 (fomc.model.Index.trade_long).
"""
from __future__ import annotations

from datetime import date, timedelta

import numpy as np

from fomc.model import EPOCH, ROW_DTYPE, Index, bar_at, ny_utc
from smc.swaps import RateTable
from tom import nyse

VARIANTS = {"N-NACHT": ("p", (16, 0), "d", (9, 30), False),
            "N-EU": ("d", (2, 0), "d", (3, 0), False),
            "N-EU-DOWN": ("d", (2, 0), "d", (3, 0), True)}
CLOSE = (16, 0)


def dn(d: date) -> int:
    return (d - EPOCH).days


def price(idx: Index, d: date, hm: tuple[int, int]) -> float:
    i = bar_at(idx.m5, int(ny_utc(dn(d), *hm)))
    return float(idx.m5["o"][i]) if i >= 0 else np.nan


def day_triples(first: date, last: date) -> list[tuple[date, date, date]]:
    """(trading day before p, p, d) for trading days d in first..last."""
    days = nyse.trading_days(first - timedelta(days=15), last)
    return [(a, b, c) for a, b, c in zip(days[:-2], days[1:-1], days[2:]) if c >= first]


def run_model_n(variant: str, idx: Index, first: date, last: date, rates: RateTable,
                condition: str | None = None) -> np.ndarray:
    """One row per traded day d (ROW_DTYPE of strategy no. 9, `day` = d). `condition` ('down' / 'up') overrides the
    variant's own filter for descriptive runs."""
    d_in, hm_in, d_out, hm_out, down_only = VARIANTS[variant]
    cond = condition or ("down" if down_only else None)
    rows = []
    for pp, p, d in day_triples(first, last):
        if cond:
            c_p, c_pp = price(idx, p, CLOSE), price(idx, pp, CLOSE)
            if not (np.isfinite(c_p) and np.isfinite(c_pp)) or c_p == c_pp:
                continue
            if (cond == "down") != (c_p < c_pp):
                continue
        t_in = int(ny_utc(dn(p if d_in == "p" else d), *hm_in))
        t_out = int(ny_utc(dn(p if d_out == "p" else d), *hm_out))
        r = idx.trade_long(t_in, t_out, rates)
        if r is not None:
            rows.append((idx.spec.symbol, dn(d), *r))
    return np.array(rows, dtype=ROW_DTYPE)
