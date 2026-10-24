"""Model KA 'options expiry and Santa rally' (strategies no. 56 and 57), as pre-registered in docs/01_Vorregistrierung.md.

OPEX day = third Friday of the month, or the NYSE trading day before it. Prices at 15:55 New York; position
mechanics of strategy no. 9 (fomc.model.Index: 1 x capital, emergency stop 3 ATR14 D1, cost model H, swaps):
  K-OPEX   long  from trading day -5 to the OPEX day
  K-POST   short from the OPEX day to trading day +5
  K-SANTA  long  from the 6th-last December trading day to the 2nd January trading day
"""
from __future__ import annotations

from datetime import date, timedelta

import numpy as np

from fomc.model import EPOCH, ROW_DTYPE, STOP_ATR, Index, bar_at, ny_utc
from smc.data.bars import TF_SECONDS
from smc.strategy_h import SLIPPAGE_SPREADS
from smc.swaps import RateTable, month_index, rollovers
from tom import nyse

VARIANTS = ("K-OPEX", "K-POST", "K-SANTA")
CLOSE = (15, 55)


def dn(d: date) -> int:
    return (d - EPOCH).days


def opex_day(year: int, month: int) -> date:
    d = nyse._nth_weekday(year, month, 4, 3)                 # third Friday
    while not nyse.is_trading_day(d):
        d -= timedelta(days=1)
    return d


def windows(variant: str, first_year: int, last_year: int) -> list[tuple[date, date]]:
    """(entry date, exit date) of the events whose exit lies in first_year .. last_year."""
    days = nyse.trading_days(date(first_year - 1, 11, 1), date(last_year + 1, 1, 31))
    pos = {d: i for i, d in enumerate(days)}
    out = []
    if variant in ("K-OPEX", "K-POST"):
        for y in range(first_year - 1, last_year + 1):
            for m in range(1, 13):
                k = pos[opex_day(y, m)] if date(y, m, 1) > days[0] else None
                if k is None or k < 5 or k + 5 >= len(days):
                    continue
                a, b = (days[k - 5], days[k]) if variant == "K-OPEX" else (days[k], days[k + 5])
                if first_year <= b.year <= last_year:
                    out.append((a, b))
    elif variant == "K-SANTA":
        for y in range(first_year - 1, last_year + 1):
            dec = [d for d in days if d.year == y and d.month == 12]
            jan = [d for d in days if d.year == y + 1 and d.month == 1]
            if len(dec) >= 6 and len(jan) >= 2 and first_year <= jan[1].year <= last_year:
                out.append((dec[-6], jan[1]))
    else:
        raise ValueError(variant)
    return out


def trade_short(idx: Index, t_in: int, t_out: int, rates: RateTable):
    """Mirror of fomc.model.Index.trade_long for a short position (same ROW_DTYPE fields after symbol / day)."""
    o, h, t5 = idx.m5["o"], idx.m5["h"], idx.m5["t"]
    i, j = bar_at(idx.m5, t_in), bar_at(idx.m5, t_out)
    if i < 0 or j < 0 or j <= i:
        return None
    k1 = int(np.searchsorted(idx.d1_close, t_in, side="right")) - 1
    a = idx.atr_d1[k1] if k1 >= 0 else np.nan
    if not np.isfinite(a):
        return None
    ref = o[i]
    spread = idx.spec.rel_spread * ref
    slip = SLIPPAGE_SPREADS * spread
    entry = ref - slip
    stop = ref + STOP_ATR * a
    hit = h[i:j] + spread >= stop
    stopped = bool(hit.any())
    if stopped:
        k = i + int(np.argmax(hit))
        px, t_x, last = max(stop, o[k] + spread) + slip, int(t5[k] + TF_SECONDS["M5"]), k
    else:
        px, t_x, last = o[j] + spread + slip, int(t5[j]), j - 1
    r, nights = rollovers(int(t5[i]), t_x)
    swap = float(sum(k * idx.spec.swap_rate(-1, int(m), rates) for m, k in zip(month_index(r), nights)) / 365)
    swap_bp = swap * 1e4
    move = (entry - px) / ref * 1e4
    net = move + swap_bp
    cost = (spread + 2 * slip) / ref * 1e4 + max(-swap_bp, 0.0)
    mae = min(0.0, (entry - (h[i:last + 1].max() + spread)) / ref * 1e4)
    return (int(t5[i]), t_x, float(entry), float(px), stopped, float(net), float(cost), float(net + cost),
            float(swap_bp), float(mae))


def run_model_ka(variant: str, idx: Index, first_year: int, last_year: int, rates: RateTable) -> np.ndarray:
    """One row per event (ROW_DTYPE of strategy no. 9; `day` = exit day)."""
    rows = []
    for a, b in windows(variant, first_year, last_year):
        t_in, t_out = int(ny_utc(dn(a), *CLOSE)), int(ny_utc(dn(b), *CLOSE))
        r = trade_short(idx, t_in, t_out, rates) if variant == "K-POST" else idx.trade_long(t_in, t_out, rates)
        if r is not None:
            rows.append((idx.spec.symbol, dn(b), *r))
    return np.array(rows, dtype=ROW_DTYPE)
