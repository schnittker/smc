"""Model D 'trend following with a structure exit' (P4), as pre-registered in docs/06_P4_Vorregistrierung_ModellD.md.

Signal, market entry, stop and cost gate are those of C-MKT (strategy_c). There is no target. The
position closes at the fixed stop, at the market when the strict H1 trend flips against it (the next
CHOCH_STRICT on H1; exit at the open of the first M5 bar after that H1 close) or at the close of the
5,760th M5 bar (20 trading days), whichever comes first. A structure exit frees the symbol at the exit
time: an opposite signal from the same H1 close enters at the same open (stop and reverse), also when
a weekend lies in between. Stop and time exits free it after their bar.

Costs in R: spread via ask/bid fills, commission, slippage on entry and exit, overnight swaps from
short-term interest rates (smc.swaps) and the 0.7 % conversion fee on the price result of symbols
whose profit currency is not USD. cost_r adds up every cost except swap credits, so net_r - cost_r is
the result with doubled costs.
"""
from __future__ import annotations

import numpy as np

from smc.costs import commission_price, cost_in_price
from smc.data.bars import TF_SECONDS
from smc.engine.structure import CHOCH_STRICT
from smc.strategy_c import (BAD_RISK, BLOCKED, BUFFER_ATR, BUFFER_SPREADS, COST_GATE, COSTLY, ENTRY_MARKET,
                            EXIT_SL, EXIT_TIME, NO_DATA, SIGNAL_DTYPE, TRADED, Inputs, Market, _empty_rows)
from smc.swaps import RateTable, swap_r

TIME_STOP_D = 5760       # M5 bars = 20 trading days
EXIT_STRUCT = 4
CONVERSION_FEE = 0.007
_NEVER = np.iinfo(np.int64).max

D_DTYPE = np.dtype(SIGNAL_DTYPE.descr + [("swap_r", "f8"), ("fee_r", "f8")])


def run_exit(o, h, l, c, f: int, d: int, sl: float, x_struct: int, mk: Market, max_bars: int = TIME_STOP_D):
    """Exit of a position entered at the open of bar f as (bar, price, reason); None if the data ends first.

    x_struct is the bar at whose open the structure exit fires (any number >= len(c) if none). The bars
    before it are watched for the stop; a stop crossed by a gap fills at the open.
    """
    n = len(c)
    last = f + max_bars - 1
    end = min(last + 1, x_struct, n)
    seg = slice(f, end)
    hit = l[seg] <= sl if d == 1 else h[seg] >= sl - mk.spread
    if hit.any():
        i = f + int(np.argmax(hit))
        px = min(sl, o[i]) - mk.slip if d == 1 else max(sl, o[i] + mk.spread) + mk.slip
        return i, px, EXIT_SL
    if x_struct <= last and x_struct < n:
        px = o[x_struct] - mk.slip if d == 1 else o[x_struct] + mk.spread + mk.slip
        return x_struct, px, EXIT_STRUCT
    if last >= n:
        return None
    px = c[last] - mk.slip if d == 1 else c[last] + mk.spread + mk.slip
    return last, px, EXIT_TIME


def run_model_d(inp: Inputs, t_from: int, t_to: int, rates: RateTable, max_bars: int = TIME_STOP_D) -> np.ndarray:
    """One row (D_DTYPE) per Model D signal with t_from <= signal time < t_to."""
    sym, mk = inp.symbol, Market.of(inp.symbol)
    o, h, l, c, t5 = (inp.m5[x] for x in ("o", "h", "l", "c", "t"))
    t5_close = t5 + TF_SECONDS["M5"]
    t15_close = inp.m15["t"] + TF_SECONDS["M15"]
    t1_close = inp.h1["t"] + TF_SECONDS["H1"]
    t4_close = inp.h4["t"] + TF_SECONDS["H4"]
    fee = CONVERSION_FEE if sym[3:] != "USD" else 0.0

    strict = inp.h1_events[inp.h1_events["type"] == CHOCH_STRICT]
    t_strict = t1_close[strict["k"]]
    j4 = np.searchsorted(t4_close, t_strict, side="right") - 1
    trend4 = np.where(j4 >= 0, inp.h4_trend[np.clip(j4, 0, None)], 0)
    sig = np.flatnonzero((t_strict >= t_from) & (t_strict < t_to) & (trend4 == strict["dir"]))

    base = _empty_rows(len(sig))
    rows = np.zeros(len(sig), D_DTYPE)
    for name in SIGNAL_DTYPE.names:
        rows[name] = base[name]
    rows["swap_r"] = rows["fee_r"] = np.nan
    rows["variant"], rows["symbol"] = "D", sym
    rows["dir"], rows["t_sig"], rows["k_h1"] = strict["dir"][sig], t_strict[sig], strict["k"][sig]
    free_bar = 0             # first M5 bar at whose open a new position may be entered
    for z, e in enumerate(sig):
        r = rows[z]
        d, ts = int(r["dir"]), int(r["t_sig"])
        s = int(np.searchsorted(t5, ts, side="left"))
        if s < free_bar:
            r["status"] = BLOCKED
            continue
        i15 = int(np.searchsorted(t15_close, ts, side="right")) - 1
        if s >= len(t5) or i15 < 0 or not np.isfinite(inp.m15_atr14[i15]):
            r["status"] = NO_DATA
            continue
        j = int(strict["ref_i"][e])
        anchor = float(inp.h1["l"][j] if d == 1 else inp.h1["h"][j])
        sl = anchor - d * max(BUFFER_SPREADS * mk.raw_spread, BUFFER_ATR * float(inp.m15_atr14[i15]))
        entry = o[s] + mk.spread if d == 1 else o[s]
        risk = d * (entry - sl)
        r["anchor"], r["sl"], r["entry_kind"], r["entry"], r["risk"] = anchor, sl, ENTRY_MARKET, entry, risk
        if (o[s] <= sl if d == 1 else o[s] + mk.spread >= sl) or risk <= 0:
            r["status"] = BAD_RISK
            continue
        if cost_in_price(sym, entry) > COST_GATE * risk:
            r["status"] = COSTLY
            continue
        x_struct = int(np.searchsorted(t5, t_strict[e + 1], side="left")) if e + 1 < len(strict) else _NEVER
        res = run_exit(o, h, l, c, s, d, sl, x_struct, mk, max_bars)
        if res is None:
            r["status"], free_bar = NO_DATA, _NEVER
            continue
        i_x, px, why = res
        t_exit = int(t5[i_x]) if why == EXIT_STRUCT else int(t5_close[i_x])
        gross = d * (px - (entry + d * mk.slip)) / risk
        comm = commission_price(sym, entry) / risk
        swap = swap_r(sym, d, int(t5[s]), t_exit, entry, risk, rates)
        fee_r = fee * abs(gross)
        r["status"], r["i_fill"], r["t_fill"] = TRADED, s, t5[s]
        r["i_end"], r["t_end"], r["exit_reason"], r["exit_px"] = i_x, t_exit, why, px
        r["gross_r"], r["swap_r"], r["fee_r"] = gross, swap, fee_r
        r["net_r"] = gross - comm + swap - fee_r
        r["cost_r"] = (mk.spread + 2 * mk.slip) / risk + comm + fee_r + max(-swap, 0.0)
        free_bar = i_x if why == EXIT_STRUCT else i_x + 1
    return rows
