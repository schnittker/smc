"""Model G 'trend following D1' (P6), as pre-registered in docs/10_P6_Vorregistrierung_ModellG.md.

Time-series momentum per instrument: s = mean(sign(R21), sign(R63), sign(R252)) of the 16:45 New York
prices, position w = s x 10 % / sigma with sigma = EWMA volatility (centre of mass 60 days, floor 4 % p. a.).
Positions are set at 16:50 New York on Monday to Thursday (never on Fridays, never on FX days dated
24.12.-01.01., not when the M5 data up to 16:50 is missing) and marked at 16:50 New York every trading
day. Results are fractions of capital: price result, trading costs (half spread + slippage + half the
round-trip commission per traded notional), swaps and the 0.7 % conversion fee on episode results of
non-USD profit currencies (an episode is a run of positions with the same sign).
"""
from __future__ import annotations

import numpy as np

from smc import timez
from smc.costs import commission_price, effective_spread, slippage_price
from smc.data.bars import TF_SECONDS
from smc.swaps import MARKUP, WEDNESDAY, RateTable, month_index

LOOKBACKS = (21, 63, 252)
VOL_ALPHA = 1 / 61          # EWMA with centre of mass 60 days
VOL_FLOOR = 0.04
VOL_TARGET = 0.10
ANNUAL = 261
CONVERSION_FEE = 0.007
SIGNAL_TIME = 23 * 3600 + 45 * 60      # 16:45 New York in server time
MARK_TIME = 23 * 3600 + 50 * 60        # 16:50 New York

DAY_DTYPE = np.dtype([
    ("symbol", "U6"), ("day", "i8"), ("p_sig", "f8"), ("p_mark", "f8"), ("rebalance", "?"), ("w", "f8"),
    ("pnl", "f8"), ("trade_cost", "f8"), ("swap", "f8"), ("fee", "f8"), ("realized", "f8"), ("worst", "f8"),
    ("net", "f8"), ("cost", "f8"),
])


def daily_prices(m5: np.ndarray) -> dict[str, np.ndarray]:
    """Per server day Mon-Fri with data: 16:45 and 16:50 New York prices (closes of the last M5 bar
    ending by then, within the same FX day), whether a bar ends exactly at 16:50, and the low/high of
    all bars since the previous day's 16:50 bar."""
    t5 = m5["t"]
    t_close = t5 + TF_SECONDS["M5"]
    days = np.unique(m5["ts"] // timez.DAY)
    days = days[(days + 3) % 7 < 5]
    day_start = timez.server_to_utc(days * timez.DAY)
    t_sig = timez.server_to_utc(days * timez.DAY + SIGNAL_TIME)
    t_mark = timez.server_to_utc(days * timez.DAY + MARK_TIME)
    i_sig = np.searchsorted(t_close, t_sig, side="right") - 1
    i_mark = np.searchsorted(t_close, t_mark, side="right") - 1
    ok = (i_sig >= 0) & (i_mark >= 0)
    ok[ok] &= (t5[i_sig[ok]] >= day_start[ok]) & (t5[i_mark[ok]] >= day_start[ok])
    days, i_sig, i_mark, t_mark = days[ok], i_sig[ok], i_mark[ok], t_mark[ok]
    starts = np.r_[0, i_mark[:-1] + 1]
    starts = np.minimum(starts, i_mark)
    lo = np.array([m5["l"][a:b + 1].min() for a, b in zip(starts, i_mark)])
    hi = np.array([m5["h"][a:b + 1].max() for a, b in zip(starts, i_mark)])
    return {"day": days, "p_sig": m5["c"][i_sig], "p_mark": m5["c"][i_mark],
            "exact": t_close[i_mark] == t_mark, "lo": lo, "hi": hi}


def _holiday(days: np.ndarray) -> np.ndarray:
    md = np.asarray(days * timez.DAY, dtype="datetime64[s]").astype("datetime64[D]").astype(str)
    mmdd = np.array([s[5:] for s in md])
    return (mmdd >= "12-24") | (mmdd == "01-01")


def run_model_g(symbol: str, m5: np.ndarray, rates: RateTable, day_to: int | None = None) -> np.ndarray:
    """One row (DAY_DTYPE) per trading day of `symbol` with a signal price, up to server day day_to (excl.)."""
    px = daily_prices(m5)
    if day_to is not None:
        keep = px["day"] < day_to
        px = {k: v[keep] for k, v in px.items()}
    days, p_sig, p_mark = px["day"], px["p_sig"], px["p_mark"]
    n = len(days)
    spread, slip = effective_spread(symbol), slippage_price(symbol)
    base, quote = symbol[:3], symbol[3:]
    fee_rate = CONVERSION_FEE if quote != "USD" else 0.0
    weekday = (days + 3) % 7
    may_trade = (weekday <= 3) & ~_holiday(days) & px["exact"]
    months = month_index(timez.server_to_utc(days * timez.DAY + MARK_TIME))

    rows = np.zeros(n, DAY_DTYPE)
    rows["symbol"], rows["day"], rows["p_sig"], rows["p_mark"] = symbol, days, p_sig, p_mark
    r = np.r_[np.nan, np.diff(np.log(p_sig))]
    var = np.nan
    w = 0.0
    episode = 0.0
    for z in range(n):
        if z == 60:                                   # start value: variance of the first 60 returns
            var = float(np.var(r[1:61]))
        elif z > 60:
            var = (1 - VOL_ALPHA) * var + VOL_ALPHA * r[z] ** 2
        pnl = worst = 0.0
        if z >= 1 and w != 0.0:
            prev = p_mark[z - 1]
            pnl = w * (p_mark[z] / prev - 1)
            extreme = px["lo"][z] if w > 0 else px["hi"][z] + spread
            worst = min(0.0, w * (extreme / prev - 1))
        episode += pnl
        target = w
        if may_trade[z] and z >= max(LOOKBACKS) and np.isfinite(var):
            s = np.mean([np.sign(np.log(p_sig[z] / p_sig[z - k])) for k in LOOKBACKS])
            sigma = max(np.sqrt(ANNUAL * var), VOL_FLOOR)
            target = s * VOL_TARGET / sigma
        trade_cost = abs(target - w) * (spread / 2 + slip + commission_price(symbol, p_mark[z]) / 2) / p_mark[z]
        realized = fee = 0.0
        if w != 0.0 and np.sign(target) != np.sign(w):
            realized, episode = episode, 0.0
            fee = fee_rate * abs(realized)
        swap = 0.0
        if target != 0.0:
            d = 1 if target > 0 else -1
            diff = rates.rate(base, int(months[z])) - rates.rate(quote, int(months[z]))
            nights = 3 if weekday[z] == WEDNESDAY else 1
            swap = abs(target) * (d * diff - MARKUP) * nights / 365
        r_ = rows[z]
        r_["rebalance"], r_["w"] = target != w, target
        r_["pnl"], r_["trade_cost"], r_["swap"], r_["fee"], r_["realized"], r_["worst"] = (
            pnl, trade_cost, swap, fee, realized, worst)
        r_["net"] = pnl - trade_cost + swap - fee
        r_["cost"] = trade_cost + fee + max(-swap, 0.0)
        w = target
    return rows
