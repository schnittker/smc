"""Model C 'trend continuation' (P3), as pre-registered in docs/04_P3_Vorregistrierung_ModellC.md.

Signal: at the close of an H1 bar the strict H1 trend flips back into the direction of the strict
H4 trend (as of the last closed H4 bar) while the symbol has no position or pending order.
Stop: beyond the new H1 protected extreme (the end of the finished counter swing) by
max(2 x typical raw spread, 0.1 x ATR14(M15)).
C-MKT enters at the open of the next M5 bar. C-LMT places a limit order at the CE of the youngest
untouched M15 FVG of the confirmation leg (anchor H1 bar .. signal), else at the mean threshold of
the youngest untouched M15 order block, else no trade. The order lives 288 M5 bars and is cancelled
when the target or the stop level is reached first or the H4 trend turns.
Target, fixed at the fill: the nearest liquidity pool that is active at the fill and at least 2R
away, capped at 4R, else 2R. Exit at target, stop or at the close of the 864th M5 bar.

Bars are bid prices. The spread is constant (raw + volume-band surcharge): long entries and short
exits pay it, ask-side triggers are shifted by it. R is the planned distance entry -> stop.

Details the pre-registration leaves open, fixed here before the first run:
- target used to cancel a pending order: the one an order filled at the first bar after the signal gets;
- per bar a cancellation (H4 trend at the open, open beyond the stop, target reached) beats a fill;
- a stop crossed by a gap fills at the open; targets and limit entries fill at their price;
- a pool pierced in the fill bar of a limit order counts as pierced (order inside the bar unknown);
- pierce = first wick beyond the level, buy-side pools on the ask with the raw spread (as the pipeline);
- 'typical spread' in the stop buffer is the raw spread; the cost gate uses the P2 round trip
  (spread + commission + one slipped fill);
- a zone must still lie entirely behind the price at the signal (otherwise no valid limit order).
"""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from smc.config import DATA_DIR, DIGITS
from smc.costs import commission_price, cost_in_price, effective_spread, slippage_price
from smc.data.bars import TF_SECONDS, load_bars
from smc.engine.structure import CHOCH_STRICT
from smc.pipeline import TYPICAL_SPREAD, SymbolFeatures

RR_MIN, RR_CAP = 2.0, 4.0
TIME_STOP = 864          # M5 bars, about 3 trading days
LIMIT_VALID = 288        # M5 bars, 24 trading hours
COST_GATE = 0.10         # skip trades whose round-trip costs exceed this many R
BUFFER_SPREADS, BUFFER_ATR = 2.0, 0.1

MKT, LMT = "C-MKT", "C-LMT"

# signal status
TRADED, BLOCKED, NO_ZONE, BAD_RISK, COSTLY, CANCEL_TREND, CANCEL_STOP, CANCEL_TARGET, EXPIRED, NO_DATA = range(10)
STATUS_NAMES = {TRADED: "traded", BLOCKED: "blocked", NO_ZONE: "no_zone", BAD_RISK: "bad_risk", COSTLY: "cost_gate",
                CANCEL_TREND: "cancel_trend", CANCEL_STOP: "cancel_stop", CANCEL_TARGET: "cancel_target",
                EXPIRED: "expired", NO_DATA: "no_data"}
# entry kinds
ENTRY_MARKET, ENTRY_FVG, ENTRY_OB = 0, 1, 2
# exit reasons
EXIT_TP, EXIT_SL, EXIT_TIME = 1, 2, 3
# target kinds besides the pool kinds 1..9
TARGET_MIN, TARGET_CAP = 0, -1
_NEVER = np.iinfo(np.int64).max

SIGNAL_DTYPE = np.dtype([
    ("symbol", "U6"), ("variant", "U5"), ("status", "i1"), ("dir", "i1"), ("t_sig", "i8"), ("k_h1", "i8"),
    ("anchor", "f8"), ("sl", "f8"), ("entry_kind", "i1"), ("entry", "f8"), ("risk", "f8"),
    ("tp", "f8"), ("tp_kind", "i1"), ("tp_r", "f8"), ("i_fill", "i8"), ("t_fill", "i8"),
    ("i_end", "i8"), ("t_end", "i8"), ("exit_reason", "i1"), ("exit_px", "f8"),
    ("gross_r", "f8"), ("cost_r", "f8"), ("net_r", "f8"),
])


@dataclass(frozen=True)
class Market:
    spread: float        # simulated spread: typical raw spread + volume-band surcharge
    raw_spread: float    # typical raw spread (stop buffer, pool pierce)
    tick: float
    slip: float          # slippage of one market fill

    @classmethod
    def of(cls, symbol: str) -> "Market":
        return cls(effective_spread(symbol), TYPICAL_SPREAD[symbol], 10.0 ** -DIGITS[symbol], slippage_price(symbol))


@dataclass
class Inputs:
    symbol: str
    m5: np.ndarray
    m15: np.ndarray
    h1: np.ndarray
    h4: np.ndarray
    h1_events: np.ndarray
    h4_trend: np.ndarray
    m15_atr14: np.ndarray
    m15_fvg: np.ndarray
    m15_ob: np.ndarray
    pools: np.ndarray

    @classmethod
    def from_features(cls, f: SymbolFeatures) -> "Inputs":
        t = f.tf
        return cls(f.symbol, t["M5"].bars, t["M15"].bars, t["H1"].bars, t["H4"].bars, t["H1"].structure.events,
                   t["H4"].structure.trend, t["M15"].atr14, t["M15"].fvg, t["M15"].ob, f.pools)

    @classmethod
    def load(cls, symbol: str) -> "Inputs":
        """From the saved feature build (data/derived) and the bar files."""
        z = np.load(DATA_DIR / "derived" / f"{symbol}.npz")
        b = {tf: load_bars(symbol, tf) for tf in ("M5", "M15", "H1", "H4")}
        return cls(symbol, b["M5"], b["M15"], b["H1"], b["H4"], z["H1_events"], z["H4_trend"], z["M15_atr14"],
                   z["M15_fvg"], z["M15_ob"], z["pools"])


def run_position(o, h, l, c, f: int, d: int, sl: float, tp: float, mk: Market, max_bars: int = TIME_STOP):
    """Exit of a position filled in bar f as (bar, price, reason); None if the data ends first.

    The fill bar is only checked for the stop, the target from the next bar on. Stop and target in
    the same bar count as a stop. A stop crossed by a gap fills at the open, the target at its price.
    """
    last = f + max_bars - 1
    seg = slice(f, min(len(c), last + 1))
    n = seg.stop - f
    if d == 1:
        hit_sl = l[seg] <= sl
        hit_tp = h[seg] >= tp + mk.tick
    else:
        hit_sl = h[seg] >= sl - mk.spread
        hit_tp = l[seg] <= tp - mk.spread - mk.tick
    hit_tp[0] = False
    j_sl = int(np.argmax(hit_sl)) if hit_sl.any() else n
    j_tp = int(np.argmax(hit_tp)) if hit_tp.any() else n
    if j_sl < n and j_sl <= j_tp:
        i = f + j_sl
        px = min(sl, o[i]) - mk.slip if d == 1 else max(sl, o[i] + mk.spread) + mk.slip
        return i, px, EXIT_SL
    if j_tp < n:
        return f + j_tp, tp, EXIT_TP
    if last >= len(c):
        return None
    px = c[last] - mk.slip if d == 1 else c[last] + mk.spread + mk.slip
    return last, px, EXIT_TIME


def pending_order(o, h, l, trend, s: int, d: int, price: float, sl: float, tp: float, mk: Market,
                  valid: int = LIMIT_VALID) -> tuple[int, int]:
    """Fate of a limit order placed before bar s: (TRADED, fill bar) or (cancel status, bar).

    trend[i] is the strict H4 trend at the open of bar i. Per bar the cancellations come first
    (trend no longer d at the open, open beyond the stop level, target reached), then the fill.
    (NO_DATA, -1) if the data ends before the order is resolved.
    """
    e = min(len(o), s + valid)
    seg = slice(s, e)
    if d == 1:
        gap = o[seg] <= sl
        target = h[seg] >= tp + mk.tick
        fill = l[seg] <= price - mk.spread - mk.tick
    else:
        gap = o[seg] + mk.spread >= sl
        target = l[seg] <= tp - mk.spread - mk.tick
        fill = h[seg] >= price + mk.tick
    first, status = e - s, EXPIRED
    for st, hit in ((CANCEL_TREND, trend[seg] != d), (CANCEL_STOP, gap), (CANCEL_TARGET, target)):
        if hit.any() and int(np.argmax(hit)) < first:
            first, status = int(np.argmax(hit)), st
    j = int(np.argmax(fill)) if fill.any() else e - s
    if j < first:
        return TRADED, s + j
    if first < e - s:
        return status, s + first
    if e - s < valid:
        return NO_DATA, -1
    return EXPIRED, e - 1


class Targets:
    """Liquidity pools (sorted by t_avail) as take-profit candidates on the M5 series."""

    def __init__(self, pools: np.ndarray, t_open: np.ndarray, h: np.ndarray, l: np.ndarray, raw_spread: float):
        self.p = pools
        self.t_avail = np.ascontiguousarray(pools["t_avail"])
        self.start = np.searchsorted(t_open, pools["t_avail"], side="left")
        self.max_ttl = int((pools["t_expire"] - pools["t_avail"]).max()) if len(pools) else 0
        self.t_open, self.h, self.l, self.spread = t_open, h, l, raw_spread

    def pick(self, f: int, d: int, entry: float, risk: float, include_bar: bool) -> tuple[float, int]:
        """Target of a position filled in bar f: the nearest pool on side d at least 2R beyond the entry
        that is known at the open of f, not expired and not pierced before the fill (pierced in bar f
        too if include_bar); 4R if that pool is farther, 2R if there is none."""
        t_ref = self.t_open[f]
        lo = int(np.searchsorted(self.t_avail, t_ref - self.max_ttl, side="left"))
        hi = int(np.searchsorted(self.t_avail, t_ref, side="right"))
        p = self.p[lo:hi]
        need, cap = entry + d * RR_MIN * risk, entry + d * RR_CAP * risk
        cand = lo + np.flatnonzero((p["side"] == d) & (p["t_expire"] > t_ref) & (d * (p["px"] - need) >= 0))
        cand = cand[np.argsort(d * self.p["px"][cand], kind="stable")]
        end = f + 1 if include_bar else f
        for z in cand:
            px, s = float(self.p["px"][z]), int(self.start[z])
            if s < end:
                if d == 1 and self.h[s:end].max() + self.spread > px:
                    continue
                if d == -1 and self.l[s:end].min() < px:
                    continue
            if d * (px - cap) > 0:
                return cap, TARGET_CAP
            return px, int(self.p["kind"][z])
        return need, TARGET_MIN


def pick_zone(zones: np.ndarray, m15: np.ndarray, i_lo: int, i15: int, d: int):
    """Youngest zone of direction d with its origin bar in [i_lo, i15], known by i15 and untouched since:
    no wick reached the proximal edge after it became known and the last close is still beyond it."""
    if not len(zones) or i15 < 0:
        return None
    lo = int(np.searchsorted(zones["k"], i_lo, side="left"))
    hi = int(np.searchsorted(zones["k"], i15, side="right"))
    z = zones[lo:hi]
    z = z[(z["dir"] == d) & (z["origin"] >= i_lo)]
    for zz in z[np.lexsort((-z["origin"], -z["k"]))]:
        k = int(zz["k"])
        if d == 1:
            edge = zz["top"]
            if m15["c"][i15] > edge and not (m15["l"][k + 1:i15 + 1] <= edge).any():
                return zz
        else:
            edge = zz["bot"]
            if m15["c"][i15] < edge and not (m15["h"][k + 1:i15 + 1] >= edge).any():
                return zz
    return None


def _empty_rows(n: int) -> np.ndarray:
    rows = np.zeros(n, SIGNAL_DTYPE)
    for name in ("anchor", "sl", "entry", "risk", "tp", "tp_r", "exit_px", "gross_r", "cost_r", "net_r"):
        rows[name] = np.nan
    for name in ("i_fill", "t_fill", "i_end", "t_end"):
        rows[name] = -1
    rows["entry_kind"] = rows["tp_kind"] = -2
    return rows


def run_model_c(inp: Inputs, variant: str, t_from: int, t_to: int) -> np.ndarray:
    """One row (SIGNAL_DTYPE) per Model C signal with t_from <= signal time < t_to."""
    sym, mk = inp.symbol, Market.of(inp.symbol)
    o, h, l, c, t5 = (inp.m5[x] for x in ("o", "h", "l", "c", "t"))
    t5_close = t5 + TF_SECONDS["M5"]
    t15_close = inp.m15["t"] + TF_SECONDS["M15"]
    t1_close = inp.h1["t"] + TF_SECONDS["H1"]
    t4_close = inp.h4["t"] + TF_SECONDS["H4"]
    i4 = np.searchsorted(t4_close, t5, side="right") - 1          # last H4 bar closed at each M5 open
    trend4_at = np.where(i4 >= 0, inp.h4_trend[np.clip(i4, 0, None)], 0)
    targets = Targets(inp.pools, t5, h, l, mk.raw_spread)

    ev = inp.h1_events[inp.h1_events["type"] == CHOCH_STRICT]
    t_sig = t1_close[ev["k"]]
    j4 = np.searchsorted(t4_close, t_sig, side="right") - 1
    trend4 = np.where(j4 >= 0, inp.h4_trend[np.clip(j4, 0, None)], 0)
    keep = (t_sig >= t_from) & (t_sig < t_to) & (trend4 == ev["dir"])
    ev, t_sig = ev[keep], t_sig[keep]

    rows = _empty_rows(len(ev))
    rows["symbol"], rows["variant"], rows["dir"], rows["t_sig"], rows["k_h1"] = sym, variant, ev["dir"], t_sig, ev["k"]
    busy_until = np.iinfo(np.int64).min
    for z in range(len(rows)):
        r = rows[z]
        d, ts = int(r["dir"]), int(r["t_sig"])
        if ts < busy_until:
            r["status"] = BLOCKED
            continue
        s = int(np.searchsorted(t5, ts, side="left"))
        i15 = int(np.searchsorted(t15_close, ts, side="right")) - 1
        if s >= len(t5) or i15 < 0 or not np.isfinite(inp.m15_atr14[i15]):
            r["status"] = NO_DATA
            continue
        j = int(ev["ref_i"][z])
        anchor = float(inp.h1["l"][j] if d == 1 else inp.h1["h"][j])
        sl = anchor - d * max(BUFFER_SPREADS * mk.raw_spread, BUFFER_ATR * float(inp.m15_atr14[i15]))
        r["anchor"], r["sl"] = anchor, sl
        if variant == MKT:
            entry, kind = (o[s] + mk.spread if d == 1 else o[s]), ENTRY_MARKET
            valid = o[s] > sl if d == 1 else o[s] + mk.spread < sl   # stop not already triggered
        else:
            i_lo = int(np.searchsorted(inp.m15["t"], inp.h1["t"][j], side="left"))
            zone, kind = pick_zone(inp.m15_fvg, inp.m15, i_lo, i15, d), ENTRY_FVG
            if zone is None:
                zone, kind = pick_zone(inp.m15_ob, inp.m15, i_lo, i15, d), ENTRY_OB
            if zone is None:
                r["status"] = NO_ZONE
                continue
            entry, valid = float(zone["mid"]), True
        risk = d * (entry - sl)
        r["entry_kind"], r["entry"], r["risk"] = kind, entry, risk
        if not valid or risk <= 0:
            r["status"] = BAD_RISK
            continue
        if cost_in_price(sym, entry) > COST_GATE * risk:
            r["status"] = COSTLY
            continue
        f = s
        if variant == LMT:
            tp0, _ = targets.pick(s, d, entry, risk, include_bar=False)
            status, f = pending_order(o, h, l, trend4_at, s, d, entry, sl, tp0, mk)
            if status != TRADED:
                r["status"], r["i_end"] = status, f
                if f >= 0:
                    r["t_end"] = busy_until = t5_close[f]
                else:
                    busy_until = _NEVER
                continue
        tp, tp_kind = targets.pick(f, d, entry, risk, include_bar=variant == LMT)
        res = run_position(o, h, l, c, f, d, sl, tp, mk)
        if res is None:
            r["status"], busy_until = NO_DATA, _NEVER
            continue
        i_x, px, why = res
        fill_px = entry + d * mk.slip if variant == MKT else entry
        comm = commission_price(sym, entry)
        n_slip = int(variant == MKT) + int(why != EXIT_TP)
        r["status"], r["tp"], r["tp_kind"], r["tp_r"] = TRADED, tp, tp_kind, d * (tp - entry) / risk
        r["i_fill"], r["t_fill"] = f, t5[f]
        r["i_end"], r["t_end"], r["exit_reason"], r["exit_px"] = i_x, t5_close[i_x], why, px
        r["gross_r"] = d * (px - fill_px) / risk
        r["cost_r"] = (mk.spread + comm + n_slip * mk.slip) / risk
        r["net_r"] = r["gross_r"] - comm / risk
        busy_until = t5_close[i_x]
    return rows
