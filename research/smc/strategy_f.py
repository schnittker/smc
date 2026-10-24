"""Model F 'fix reversal' (P5), as pre-registered in docs/08_P5_Vorregistrierung_ModellF.md.

The USD tends to rise before the Tokyo and ECB fixes and to fall after the Tokyo and London fixes
(Krohn, Mueller & Whelan 2024). Four windows per FX day (17:00-17:00 New York):
  W1 17:30 New York -> Tokyo fix 9:55 Tokyo      long USD (not on the Sunday-evening session)
  W2 Tokyo fix -> 8:00 Frankfurt                  short USD
  W3 8:00 Frankfurt -> ECB fix 14:15 Frankfurt    long USD
  W4 London fix 16:00 London -> 16:50 New York    short USD (not for USDJPY)
Market entry and exit at the open of the M5 bars that start at those times, emergency stop at
3 x ATR14(H1). No trading on FX days dated 24.12.-01.01. Results are in basis points of the entry
price, net of spread (ask side), commission, slippage on both fills and, for non-USD profit
currencies, the 0.7 % conversion fee.
"""
from __future__ import annotations

import numpy as np

from smc import timez
from smc.costs import commission_price, effective_spread, slippage_price
from smc.data.bars import TF_SECONDS
from smc.engine.atr import atr

HOUR, MIN = 3600, 60
WINDOWS = (1, 2, 3, 4)
USD_DIR = {1: 1, 2: -1, 3: 1, 4: -1}          # +1 = long USD
STOP_ATR = 3.0
CONVERSION_FEE = 0.007

ROW_DTYPE = np.dtype([
    ("symbol", "U6"), ("window", "i1"), ("fx_day", "i8"), ("dir", "i1"), ("t_entry", "i8"), ("t_exit", "i8"),
    ("entry", "f8"), ("exit", "f8"), ("stopped", "?"), ("net_bp", "f8"), ("cost_bp", "f8"), ("mae_bp", "f8"),
])


def window_times(fx_day: np.ndarray) -> dict[int, tuple[np.ndarray, np.ndarray]]:
    """UTC entry and exit times of the four windows for server-day numbers fx_day."""
    d = np.asarray(fx_day, dtype=np.int64)
    day = d * timez.DAY                                   # the server date's calendar day in UTC terms
    eu = timez.eu_dst(day + 7 * HOUR).astype(np.int64)     # Frankfurt/London summer time (no switch on weekdays)
    tokyo_fix = day + 55 * MIN                             # 9:55 Tokyo = 0:55 UTC
    frankfurt_8 = day + 8 * HOUR - (1 + eu) * HOUR
    ecb_fix = day + 14 * HOUR + 15 * MIN - (1 + eu) * HOUR
    london_fix = day + 16 * HOUR - eu * HOUR
    w1_start = timez.server_to_utc(day + 30 * MIN)        # 17:30 New York = 00:30 server time
    w4_end = timez.server_to_utc(day + 23 * HOUR + 50 * MIN)
    return {1: (w1_start, tokyo_fix), 2: (tokyo_fix, frankfurt_8), 3: (frankfurt_8, ecb_fix), 4: (london_fix, w4_end)}


def trading_days(m5: np.ndarray) -> np.ndarray:
    """Server days with bars, without FX days dated 24.12.-01.01."""
    days = np.unique(m5["ts"] // timez.DAY)
    md = np.asarray(days * timez.DAY, dtype="datetime64[s]").astype("datetime64[D]").astype(str)
    mmdd = np.array([s[5:] for s in md])
    holiday = (mmdd >= "12-24") | (mmdd == "01-01")
    return days[~holiday]


def run_model_f(symbol: str, m5: np.ndarray, h1: np.ndarray, windows=WINDOWS, day_from: int | None = None,
                day_to: int | None = None) -> np.ndarray:
    """One row per traded window of `symbol` (ROW_DTYPE), for FX days day_from <= server day < day_to."""
    spread, slip = effective_spread(symbol), slippage_price(symbol)
    fee = CONVERSION_FEE if symbol[3:] != "USD" else 0.0
    usd_base = 1 if symbol.startswith("USD") else -1
    o, h, l, t5 = m5["o"], m5["h"], m5["l"], m5["t"]
    t1_close = h1["t"] + TF_SECONDS["H1"]
    atr_h1 = atr(h1["h"], h1["l"], h1["c"], 14)
    days = trading_days(m5)
    if day_from is not None:
        days = days[days >= day_from]
    if day_to is not None:
        days = days[days < day_to]
    times = window_times(days)
    rows = []
    for w in windows:
        if w == 4 and symbol == "USDJPY":
            continue
        start, end = times[w]
        sel = np.ones(len(days), bool)
        if w == 1:
            sel &= (days + 3) % 7 != 0                     # no W1 on the Sunday-evening session (server Monday)
        i = np.searchsorted(t5, start)
        j = np.searchsorted(t5, end)
        ok = sel & (i < len(t5)) & (j < len(t5))
        ok[ok] &= (t5[i[ok]] == start[ok]) & (t5[j[ok]] == end[ok]) & (j[ok] > i[ok])
        d = USD_DIR[w] * usd_base
        for day, ii, jj in zip(days[ok], i[ok], j[ok]):
            k1 = int(np.searchsorted(t1_close, t5[ii], side="right")) - 1
            a = atr_h1[k1] if k1 >= 0 else np.nan
            if not np.isfinite(a):
                continue
            ref = o[ii]
            if d == 1:
                entry = ref + spread + slip
                stop = ref + spread - STOP_ATR * a
                hit = l[ii:jj] <= stop
            else:
                entry = ref - slip
                stop = ref + STOP_ATR * a
                hit = h[ii:jj] + spread >= stop
            if hit.any():
                k = ii + int(np.argmax(hit))
                px = min(stop, o[k]) - slip if d == 1 else max(stop, o[k] + spread) + slip
                t_exit, last = t5[k] + TF_SECONDS["M5"], k
            else:
                px = o[jj] - slip if d == 1 else o[jj] + spread + slip
                t_exit, last = t5[jj], jj - 1
            move = d * (px - entry) / ref * 1e4
            comm = commission_price(symbol, ref) / ref * 1e4
            fee_bp = fee * abs(move)
            if d == 1:
                worst = (l[ii:last + 1].min() - entry) / ref * 1e4
            else:
                worst = (entry - (h[ii:last + 1].max() + spread)) / ref * 1e4
            cost = (spread + 2 * slip) / ref * 1e4 + comm + fee_bp
            rows.append((symbol, w, day, d, t5[ii], t_exit, entry, px, bool(hit.any()), move - comm - fee_bp, cost,
                         min(worst, 0.0)))
    out = np.array(rows, dtype=ROW_DTYPE)
    return out[np.lexsort((out["window"], out["fx_day"]))] if len(out) else out
