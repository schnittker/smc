"""Model P 'pre-FOMC drift', as pre-registered in docs/01_Vorregistrierung.md.

Long US500 (P-SPX) or US100 (P-NDX) from 14:00 New York on the weekday before a scheduled FOMC
announcement day to 13:55 New York on that day (Lucca & Moench 2015). Market fills at the open of the M5
bars starting at those times, emergency stop at 3 x ATR14(D1). Costs as model H of the SMC project: FTMO's
2026 average spread relative to the 2026 price level, a quarter spread slippage per fill, no commission,
and the index swap (dividend yield - USD rate - 2.5 %) per rollover. Results in bp of the entry bid.
"""
from __future__ import annotations

import csv
from dataclasses import dataclass
from datetime import date, timedelta
from pathlib import Path

import numpy as np

from smc import timez
from smc.data.bars import TF_SECONDS
from smc.engine.atr import atr
from smc.strategy_h import SLIPPAGE_SPREADS, CfdSpec
from smc.swaps import RateTable, month_index, rollovers

DATES_CSV = Path(__file__).resolve().parents[1] / "fomc_dates.csv"
VARIANTS = {"P-SPX": "SPXUSD", "P-NDX": "NSXUSD"}
ENTRY, EXIT = (14, 0), (13, 55)
STOP_ATR = 3.0
EPOCH = date(1970, 1, 1)

ROW_DTYPE = np.dtype([
    ("symbol", "U6"), ("day", "i8"), ("t_entry", "i8"), ("t_exit", "i8"), ("entry", "f8"), ("exit", "f8"),
    ("stopped", "?"), ("net_bp", "f8"), ("cost_bp", "f8"), ("gross_bp", "f8"), ("swap_bp", "f8"), ("mae_bp", "f8"),
])


def load_dates(path: Path = DATES_CSV) -> np.ndarray:
    """Scheduled FOMC announcement days as day numbers since 1970-01-01."""
    with path.open(encoding="utf-8") as f:
        return np.array(sorted((date.fromisoformat(r["announcement_day"]) - EPOCH).days for r in csv.DictReader(f)),
                        dtype=np.int64)


def prev_weekday(day: int) -> int:
    d = EPOCH + timedelta(days=int(day) - 1)
    while d.weekday() >= 5:
        d -= timedelta(days=1)
    return (d - EPOCH).days


def ny_utc(day, hh: int, mm: int = 0):
    """UTC epoch seconds of hh:mm New York time on calendar day number(s) `day`."""
    t0 = np.asarray(day, dtype=np.int64) * timez.DAY
    return t0 + (hh + 5) * 3600 + mm * 60 - timez.us_dst(t0 + 12 * 3600).astype(np.int64) * 3600


def bar_at(m5: np.ndarray, t: int) -> int:
    """Index of the M5 bar that starts exactly at t, or -1."""
    i = int(np.searchsorted(m5["t"], t))
    return i if i < len(m5) and m5["t"][i] == t else -1


def window_bp(m5: np.ndarray, t_a: int, t_b: int) -> float:
    """Bid change from the M5 open at t_a to the M5 open at t_b in bp (NaN if a bar is missing)."""
    i, j = bar_at(m5, t_a), bar_at(m5, t_b)
    if i < 0 or j < 0 or j <= i:
        return np.nan
    return float((m5["o"][j] / m5["o"][i] - 1) * 1e4)


@dataclass
class Index:
    """M5 and D1 bars of one index CFD with its cost and swap specification."""
    spec: CfdSpec
    m5: np.ndarray
    d1: np.ndarray

    def __post_init__(self):
        self.d1_close = self.d1["t"] + TF_SECONDS["D1"]
        self.atr_d1 = atr(self.d1["h"], self.d1["l"], self.d1["c"], 14)

    def swap_fraction(self, t_in: int, t_out: int, rates: RateTable) -> float:
        """Swaps of a long position held from t_in to t_out, as a fraction of its notional (+ = credit)."""
        r, nights = rollovers(t_in, t_out)
        return float(sum(k * self.spec.swap_rate(1, int(m), rates) for m, k in zip(month_index(r), nights)) / 365)

    def trade_long(self, t_in: int, t_out: int, rates: RateTable):
        o, h, l, t5 = self.m5["o"], self.m5["h"], self.m5["l"], self.m5["t"]
        i, j = bar_at(self.m5, t_in), bar_at(self.m5, t_out)
        if i < 0 or j < 0 or j <= i:
            return None
        k1 = int(np.searchsorted(self.d1_close, t_in, side="right")) - 1
        a = self.atr_d1[k1] if k1 >= 0 else np.nan
        if not np.isfinite(a):
            return None
        ref = o[i]
        spread = self.spec.rel_spread * ref
        slip = SLIPPAGE_SPREADS * spread
        entry = ref + spread + slip
        stop = ref - STOP_ATR * a
        hit = l[i:j] <= stop
        stopped = bool(hit.any())
        if stopped:
            k = i + int(np.argmax(hit))
            px, t_x, last = min(stop, o[k]) - slip, int(t5[k] + TF_SECONDS["M5"]), k
        else:
            px, t_x, last = o[j] - slip, int(t5[j]), j - 1
        swap = self.swap_fraction(int(t5[i]), t_x, rates)
        swap_bp = swap * 1e4
        move = (px - entry) / ref * 1e4
        net = move + swap_bp
        cost = (spread + 2 * slip) / ref * 1e4 + max(-swap_bp, 0.0)
        mae = min(0.0, (l[i:last + 1].min() - entry) / ref * 1e4)
        return (int(t5[i]), t_x, float(entry), float(px), stopped, float(net), float(cost), float(net + cost),
                float(swap_bp), float(mae))


def run_model_p(variant: str, idx: Index, days: np.ndarray, rates: RateTable) -> np.ndarray:
    """One row per announcement day in `days` that could be traded (ROW_DTYPE)."""
    rows = []
    for day in days:
        t_in = int(ny_utc(prev_weekday(day), *ENTRY))
        t_out = int(ny_utc(day, *EXIT))
        r = idx.trade_long(t_in, t_out, rates)
        if r is not None:
            rows.append((VARIANTS[variant], int(day), *r))
    return np.array(rows, dtype=ROW_DTYPE)
