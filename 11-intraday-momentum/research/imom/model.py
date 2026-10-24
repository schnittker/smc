"""Model I 'intraday momentum US500', as pre-registered in docs/01_Vorregistrierung.md.

On full NYSE trading days whose previous trading day was also a full day: signal = sign of the index return
from 16:00 New York on the previous day to 10:00 (I-ONFH, Gao et al. 2018) or to 15:30 (I-ROD, Baltussen et al.
2021); position in the signal's direction from 15:30 to 16:00. Prices are the opens of the M5 bars starting at
those times. Market fills with FTMO's average spread and a quarter spread slippage per fill (cost model H of the
SMC project), emergency stop 3 x ATR14(H1); no swaps.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import date, timedelta

import numpy as np

from fomc.model import EPOCH, bar_at, ny_utc
from smc.data.bars import TF_SECONDS
from smc.engine.atr import atr
from smc.strategy_h import SLIPPAGE_SPREADS, CfdSpec
from tom import nyse

VARIANTS = {"I-ONFH": (10, 0), "I-ROD": (15, 30)}        # end of the signal window (New York)
PREV_CLOSE, ENTRY, EXIT = (16, 0), (15, 30), (16, 0)
STOP_ATR = 3.0

ROW_DTYPE = np.dtype([
    ("day", "i8"), ("dir", "i1"), ("signal_bp", "f8"), ("r_onfh_bp", "f8"), ("r_rod_bp", "f8"), ("r_last_bp", "f8"),
    ("stopped", "?"), ("net_bp", "f8"), ("cost_bp", "f8"), ("gross_bp", "f8"), ("mae_bp", "f8"),
])


def is_early_close(d: date) -> bool:
    """NYSE 13:00 close: day after Thanksgiving, 24 December and 3 July when they are trading days."""
    thanksgiving = nyse._nth_weekday(d.year, 11, 3, 4)
    return nyse.is_trading_day(d) and (d == thanksgiving + timedelta(days=1) or (d.month, d.day) in ((12, 24), (7, 3)))


def full_days(first: date, last: date) -> list[tuple[date, date]]:
    """(previous trading day, day) for full trading days first..last whose previous trading day was full too."""
    days = nyse.trading_days(first - timedelta(days=10), last)
    return [(p, d) for p, d in zip(days[:-1], days[1:])
            if d >= first and not is_early_close(d) and not is_early_close(p)]


def dn(d: date) -> int:
    return (d - EPOCH).days


@dataclass
class IndexBars:
    spec: CfdSpec
    m5: np.ndarray
    h1: np.ndarray

    def __post_init__(self):
        self.h1_close = self.h1["t"] + TF_SECONDS["H1"]
        self.atr_h1 = atr(self.h1["h"], self.h1["l"], self.h1["c"], 14)

    def price(self, d: date, hm: tuple[int, int]) -> float:
        i = bar_at(self.m5, int(ny_utc(dn(d), *hm)))
        return float(self.m5["o"][i]) if i >= 0 else np.nan

    def trade(self, d: date, direction: int):
        """Market position from 15:30 to 16:00 on day d: (stopped, net, cost, gross, mae) in bp, or None."""
        o, h, l, t5 = self.m5["o"], self.m5["h"], self.m5["l"], self.m5["t"]
        t_in = int(ny_utc(dn(d), *ENTRY))
        i, j = bar_at(self.m5, t_in), bar_at(self.m5, int(ny_utc(dn(d), *EXIT)))
        if i < 0 or j < 0 or j <= i:
            return None
        k1 = int(np.searchsorted(self.h1_close, t_in, side="right")) - 1
        a = self.atr_h1[k1] if k1 >= 0 else np.nan
        if not np.isfinite(a):
            return None
        ref = o[i]
        spread = self.spec.rel_spread * ref
        slip = SLIPPAGE_SPREADS * spread
        if direction == 1:
            entry, stop = ref + spread + slip, ref + spread - STOP_ATR * a
            hit = l[i:j] <= stop
        else:
            entry, stop = ref - slip, ref + STOP_ATR * a
            hit = h[i:j] + spread >= stop
        stopped = bool(hit.any())
        if stopped:
            k = i + int(np.argmax(hit))
            px = min(stop, o[k]) - slip if direction == 1 else max(stop, o[k] + spread) + slip
            last = k
        else:
            px = o[j] - slip if direction == 1 else o[j] + spread + slip
            last = j - 1
        net = direction * (px - entry) / ref * 1e4
        cost = (spread + 2 * slip) / ref * 1e4
        if direction == 1:
            mae = (l[i:last + 1].min() - entry) / ref * 1e4
        else:
            mae = (entry - (h[i:last + 1].max() + spread)) / ref * 1e4
        return stopped, float(net), float(cost), float(net + cost), float(min(mae, 0.0))


def run_model_i(variant: str, idx: IndexBars, first: date, last: date) -> np.ndarray:
    """One row per traded day (ROW_DTYPE)."""
    sig_end = VARIANTS[variant]
    rows = []
    for p, d in full_days(first, last):
        close_prev = idx.price(p, PREV_CLOSE)
        p10, p1530, p16 = idx.price(d, (10, 0)), idx.price(d, ENTRY), idx.price(d, EXIT)
        if not np.all(np.isfinite([close_prev, p10, p1530, p16])):
            continue
        onfh, rod, last_ = (p10 / close_prev - 1) * 1e4, (p1530 / close_prev - 1) * 1e4, (p16 / p1530 - 1) * 1e4
        signal = onfh if sig_end == (10, 0) else rod
        if signal == 0:
            continue
        direction = 1 if signal > 0 else -1
        r = idx.trade(d, direction)
        if r is None:
            continue
        rows.append((dn(d), direction, signal, onfh, rod, last_, *r))
    return np.array(rows, dtype=ROW_DTYPE)
