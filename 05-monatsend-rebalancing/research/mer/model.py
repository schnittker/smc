"""Model M 'month-end rebalancing at the London fix', as pre-registered in docs/01_Vorregistrierung.md.

On the last London business day of a month the currency of the equity market that did better over the
month tends to fall against the USD into the 16:00 London fix (Melvin & Prins 2015). Per pair,
x = R_US - R_foreign (log index returns between the signal times of the previous and the current
event day): x > 0 -> long the foreign currency, x < 0 -> short it. Market entry and exit at the open of
the M5 bars that start at the entry and exit times, emergency stop at 3 x ATR14(H1). Results are in
basis points of the entry reference price, net of spread (ask side), commission, slippage and, for
USDJPY, the 0.7 % conversion fee. The trade mechanics follow smc.strategy_f (model F).
"""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from smc.costs import commission_price, effective_spread, pip_size, slippage_price
from smc.data.bars import TF_SECONDS
from smc.engine.atr import atr
from mer import events

US_INDEX = "SPXUSD"
PAIRS = {"EURUSD": "FRXEUR", "GBPUSD": "UKXGBP", "USDJPY": "JPXJPY", "AUDUSD": "AUXAUD"}
VARIANTS = {"M-1H": {"signal": (14, 55), "entry": (14, 55), "exit": (16, 0)},
            "M-DAY": {"signal": (8, 0), "entry": (8, 0), "exit": (16, 0)}}
REVERSAL = {"entry": (16, 5), "exit": (12, 0)}      # descriptive: 16:05 event day -> 12:00 next business day
STOP_ATR = 3.0
CONVERSION_FEE = 0.007
MAX_PRICE_AGE = 6 * 3600
FIX_EXIT_SLIP_PIPS = 0.5

ROW_DTYPE = np.dtype([
    ("symbol", "U6"), ("event_day", "i8"), ("dir", "i1"), ("x", "f8"), ("rel_eq_pct", "f8"),
    ("t_entry", "i8"), ("t_exit", "i8"), ("entry", "f8"), ("exit", "f8"), ("stopped", "?"),
    ("net_bp", "f8"), ("cost_bp", "f8"), ("gross_bp", "f8"), ("ccy_ret_bp", "f8"), ("mae_bp", "f8"),
])


def price_asof(bars: np.ndarray, t: int, max_age: int = MAX_PRICE_AGE) -> float:
    """Close of the last M5 bar that has closed by t (NaN if none or older than max_age)."""
    t_close = bars["t"] + TF_SECONDS["M5"]
    k = int(np.searchsorted(t_close, t, side="right")) - 1
    if k < 0 or t - t_close[k] > max_age:
        return np.nan
    return float(bars["c"][k])


def index_returns(bars: np.ndarray, t_sig: np.ndarray) -> np.ndarray:
    """Log return of an index between consecutive signal times (NaN for the first or missing prices)."""
    p = np.array([price_asof(bars, int(t)) for t in t_sig])
    return np.r_[np.nan, np.log(p[1:] / p[:-1])]


def foreign_dir(symbol: str) -> int:
    """+1 if buying the symbol means buying the foreign currency (EURUSD), -1 for USD-base pairs."""
    return -1 if symbol.startswith("USD") else 1


@dataclass
class Fill:
    t_entry: int
    t_exit: int
    entry: float
    exit: float
    stopped: bool
    net_bp: float
    cost_bp: float
    gross_bp: float
    ccy_ret_bp: float
    mae_bp: float


class Market:
    """M5 and H1 bars of one FX symbol with the cost parameters of the SMC cost model."""

    def __init__(self, symbol: str, m5: np.ndarray, h1: np.ndarray):
        self.symbol, self.m5 = symbol, m5
        self.t1_close = h1["t"] + TF_SECONDS["H1"]
        self.atr_h1 = atr(h1["h"], h1["l"], h1["c"], 14)
        self.spread, self.slip = effective_spread(symbol), slippage_price(symbol)
        self.fee = CONVERSION_FEE if symbol[3:] != "USD" else 0.0

    def trade(self, t_entry: int, t_exit: int, d: int, exit_slip: float | None = None) -> Fill | None:
        """Market position d (+1 long, -1 short) from the M5 open at t_entry to the M5 open at t_exit."""
        o, h, l, t5 = self.m5["o"], self.m5["h"], self.m5["l"], self.m5["t"]
        i, j = int(np.searchsorted(t5, t_entry)), int(np.searchsorted(t5, t_exit))
        if j >= len(t5) or t5[i] != t_entry or t5[j] != t_exit or j <= i:
            return None
        k1 = int(np.searchsorted(self.t1_close, t5[i], side="right")) - 1
        a = self.atr_h1[k1] if k1 >= 0 else np.nan
        if not np.isfinite(a):
            return None
        spread, slip = self.spread, self.slip
        xslip = slip if exit_slip is None else exit_slip
        ref = o[i]
        if d == 1:
            entry = ref + spread + slip
            stop = ref + spread - STOP_ATR * a
            hit = l[i:j] <= stop
        else:
            entry = ref - slip
            stop = ref + STOP_ATR * a
            hit = h[i:j] + spread >= stop
        stopped = bool(hit.any())
        if stopped:
            k = i + int(np.argmax(hit))
            px = min(stop, o[k]) - slip if d == 1 else max(stop, o[k] + spread) + slip
            t_out, last, out_slip = t5[k] + TF_SECONDS["M5"], k, slip
        else:
            px = o[j] - xslip if d == 1 else o[j] + spread + xslip
            t_out, last, out_slip = t5[j], j - 1, xslip
        move = d * (px - entry) / ref * 1e4
        comm = commission_price(self.symbol, ref) / ref * 1e4
        fee_bp = self.fee * abs(move)
        if d == 1:
            worst = (l[i:last + 1].min() - entry) / ref * 1e4
        else:
            worst = (entry - (h[i:last + 1].max() + spread)) / ref * 1e4
        cost = (spread + slip + out_slip) / ref * 1e4 + comm + fee_bp
        net = move - comm - fee_bp
        ccy = foreign_dir(self.symbol) * (o[j] - ref) / ref * 1e4
        return Fill(int(t5[i]), int(t_out), float(entry), float(px), stopped, float(net), float(cost),
                    float(net + cost), float(ccy), float(min(worst, 0.0)))


def signals(days: np.ndarray, us: np.ndarray, foreign: np.ndarray, hhmm: tuple[int, int]) -> tuple[np.ndarray, np.ndarray]:
    """x = R_US - R_foreign per event day and R_foreign - R_US in percent."""
    t_sig = events.london_utc(days, *hhmm)
    r_us, r_f = index_returns(us, t_sig), index_returns(foreign, t_sig)
    x = r_us - r_f
    return x, -x * 100.0


def run_model_m(symbol: str, market: Market, us: np.ndarray, foreign: np.ndarray, days: np.ndarray,
                variant: str, keep: np.ndarray | None = None) -> np.ndarray:
    """One row per traded event of `symbol` (ROW_DTYPE). `days` must be consecutive event days so that the
    month returns run from one event to the next; `keep` selects the days that are traded."""
    spec = VARIANTS[variant]
    x, rel = signals(days, us, foreign, spec["signal"])
    t_in, t_out = events.london_utc(days, *spec["entry"]), events.london_utc(days, *spec["exit"])
    fix_slip = FIX_EXIT_SLIP_PIPS * pip_size(symbol)
    rows = []
    for n, day in enumerate(days):
        if (keep is not None and not keep[n]) or not np.isfinite(x[n]) or x[n] == 0:
            continue
        d = int(np.sign(x[n])) * foreign_dir(symbol)
        f = market.trade(int(t_in[n]), int(t_out[n]), d, exit_slip=fix_slip)
        if f is None:
            continue
        rows.append((symbol, day, d, x[n], rel[n], f.t_entry, f.t_exit, f.entry, f.exit, f.stopped,
                     f.net_bp, f.cost_bp, f.gross_bp, f.ccy_ret_bp, f.mae_bp))
    return np.array(rows, dtype=ROW_DTYPE)


def run_reversal(symbol: str, market: Market, us: np.ndarray, foreign: np.ndarray, days: np.ndarray,
                 variant: str, keep: np.ndarray | None = None) -> np.ndarray:
    """Descriptive: the opposite position from 16:05 London to 12:00 London on the next business day."""
    x, rel = signals(days, us, foreign, VARIANTS[variant]["signal"])
    rows = []
    for n, day in enumerate(days):
        if (keep is not None and not keep[n]) or not np.isfinite(x[n]) or x[n] == 0:
            continue
        nxt = events.day_number(events.next_business_day(events.to_date(day)))
        t_in = int(events.london_utc(day, *REVERSAL["entry"]))
        t_out = int(events.london_utc(nxt, *REVERSAL["exit"]))
        d = -int(np.sign(x[n])) * foreign_dir(symbol)
        f = market.trade(t_in, t_out, d)
        if f is None:
            continue
        rows.append((symbol, day, d, x[n], rel[n], f.t_entry, f.t_exit, f.entry, f.exit, f.stopped,
                     f.net_bp, f.cost_bp, f.gross_bp, f.ccy_ret_bp, f.mae_bp))
    return np.array(rows, dtype=ROW_DTYPE)
