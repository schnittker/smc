"""Model Y 'currency strength' (strategies no. 46 and 47), as pre-registered in docs/01_Vorregistrierung.md.

p_c = ln(price of currency c in USD) from the 7 USD pairs (p_USD = 0); strength over a window = change of p_c minus
the mean change of all 8 currencies.
  Y-ASIA / Y-LDN  strongest S vs weakest W over 00:00-07:00 / 07:00-12:00 London (H1 opens); the available pair of
                  S and W is bought S / sold W at the 07:00 / 12:00 open and closed at the 16:00 open
  Y-USDB          dev_c = 24-bar change of p_c minus the mean 24-bar change of the 6 other non-USD currencies;
                  z = dev_c / std(dev_c over the last 500 bars); |z| > 2 -> fade c against USD at the next open;
                  exit at the next open once z reaches 0 or changes sign, at the latest after 24 bars held
Fixed stop 2 ATR14_H1 (intrabar, gap fills at the open, wins over other exits); notional = min(0.25 % / (2 ATR14 /
price), 10) x capital; FX costs per market fill and swaps per rollover; no new entries on days 24.12.-01.01.
"""
from __future__ import annotations

from datetime import date, timedelta

import numpy as np

from dbo.model import EPOCH, Costs, holiday
from hkb.model import atr, swap_frac
from mer.events import london_utc
from smc.swaps import RateTable

VARIANTS = ("Y-ASIA", "Y-LDN", "Y-USDB")
CCYS = ("USD", "EUR", "GBP", "JPY", "AUD", "NZD", "CAD", "CHF")
USD_PAIRS = {"EUR": "EURUSD", "GBP": "GBPUSD", "JPY": "USDJPY", "AUD": "AUDUSD", "NZD": "NZDUSD", "CAD": "USDCAD",
             "CHF": "USDCHF"}
PAIRS = ("EURUSD", "GBPUSD", "USDJPY", "AUDUSD", "NZDUSD", "USDCAD", "USDCHF",
         "EURJPY", "GBPJPY", "AUDJPY", "NZDJPY", "CADJPY", "CHFJPY", "EURCAD", "EURCHF", "EURNZD", "EURAUD",
         "GBPCHF", "GBPNZD", "GBPCAD", "GBPAUD", "AUDNZD", "AUDCAD", "CADCHF")
WINDOWS = {"Y-ASIA": (0, 7), "Y-LDN": (7, 12)}
EXIT_HOUR = 16
RISK, LEVER_CAP, STOP_ATR = 0.0025, 10.0, 2.0
Z_LOOK, Z_N, Z_K, MAX_BARS = 24, 500, 2.0, 24
DAY, H1 = 86400, 3600
STOP, TIME, SIGNAL, END = 0, 4, 1, 2

ROW_DTYPE = np.dtype([
    ("entry_day", "i8"), ("exit_day", "i8"), ("pair", "i1"), ("buy", "i1"), ("sell", "i1"), ("dir", "i1"),
    ("exit_type", "i1"), ("bars", "i4"), ("r_bp", "f8"), ("notional", "f8"), ("r_net", "f8"), ("net_bp", "f8"),
    ("cost_bp", "f8"), ("swap_bp", "f8"), ("gross_bp", "f8"),
])


def pair_for(buy: str, sell: str) -> tuple[str | None, int]:
    """Available pair and direction (+1 buy the pair, -1 sell it) for buying `buy` against `sell`."""
    if buy + sell in PAIRS:
        return buy + sell, 1
    if sell + buy in PAIRS:
        return sell + buy, -1
    return None, 0


def log_ccy(symbol: str, price):
    """p_c = ln(price of c in USD) for the non-USD currency c of a USD pair."""
    return np.log(price) if symbol.endswith("USD") else -np.log(price)


def bar_at(t: np.ndarray, x: int) -> int:
    i = int(np.searchsorted(t, x))
    return i if i < len(t) and t[i] == x else -1


def trade(bars: np.ndarray, k: int, d: int, dist: float, cost: Costs, exit_flags=None, exit_bar: int = -1,
          max_bars: int = 10 ** 9):
    """Market entry at the open of bar k in direction d with a fixed stop `dist` away. Time exit at the open of
    exit_bar, or at the next open after a bar whose exit flag (for this direction) is set / after max_bars held.
    Returns (exit_type, j, entry, px, sp, slip) with j the last bar held."""
    o, h, l, c = bars["o"], bars["h"], bars["l"], bars["c"]
    n = len(bars)
    p = o[k]
    sp, slip = cost.spread(p), cost.slip(p)
    entry = p + sp + slip if d == 1 else p - slip
    stop = entry - dist if d == 1 else entry + dist
    last = exit_bar - 1 if exit_bar >= 0 else n - 1
    for j in range(k, last + 1):
        if d == 1 and l[j] <= stop:
            return STOP, j, entry, min(stop, o[j]) - slip, sp, slip
        if d == -1 and h[j] + sp >= stop:
            return STOP, j, entry, max(stop, o[j] + sp) + slip, sp, slip
        if exit_flags is not None and j + 1 < n and (exit_flags[j] or j - k + 1 >= max_bars):
            ex = SIGNAL if exit_flags[j] else TIME
            return ex, j, entry, (o[j + 1] - slip if d == 1 else o[j + 1] + sp + slip), sp, slip
    if exit_bar >= 0:
        return TIME, exit_bar - 1, entry, (o[exit_bar] - slip if d == 1 else o[exit_bar] + sp + slip), sp, slip
    return END, n - 1, entry, (c[-1] - slip if d == 1 else c[-1] + sp + slip), sp, slip


def book(symbol: str, bars: np.ndarray, k: int, d: int, dist: float, res, cost: Costs, rates: RateTable,
         pair_idx: int, buy: int, sell: int):
    exit_type, j, entry, px, sp, slip = res
    t, ts = bars["t"], bars["ts"]
    at_open = exit_type in (SIGNAL, TIME)
    jj = min(j + 1, len(bars) - 1)
    t_exit = int(t[jj]) if at_open else (int(t[j]) if exit_type == STOP else int(t[j]) + H1)
    comm = cost.commission(entry)
    move = d * (px - entry) - comm
    trade_cost = sp + 2 * slip + comm
    notional = min(RISK / (dist / entry), LEVER_CAP)
    swap = swap_frac(symbol, d, int(t[k]), t_exit, rates, None)
    exit_day = int(ts[jj] // DAY) if at_open else int(ts[j] // DAY)
    return (int(ts[k] // DAY), exit_day, pair_idx, buy, sell, d, exit_type, j - k + 1, dist / entry * 1e4, notional,
            (move + swap * entry) / dist, notional * (move / entry + swap) * 1e4,
            notional * (trade_cost / entry + max(-swap, 0.0)) * 1e4, notional * swap * 1e4,
            notional * (move + trade_cost) / entry * 1e4)


def strength(usd: dict, t_a: int, t_b: int) -> np.ndarray | None:
    """Window strength of the 8 currencies (order CCYS) from the H1 opens at t_a and t_b; None if a bar is missing."""
    ch = np.zeros(len(CCYS))
    for ci, c in enumerate(CCYS[1:], start=1):
        b = usd[USD_PAIRS[c]]
        a_i, b_i = bar_at(b["t"], t_a), bar_at(b["t"], t_b)
        if a_i < 0 or b_i < 0:
            return None
        sym = USD_PAIRS[c]
        ch[ci] = log_ccy(sym, b["o"][b_i]) - log_ccy(sym, b["o"][a_i])
    return ch - ch.mean()


def run_session(variant: str, data: dict, rates: RateTable, first: date, last: date) -> np.ndarray:
    """Y-ASIA / Y-LDN over the London weekdays first .. last; data[symbol] = (H1 bars, Costs)."""
    h_a, h_b = WINDOWS[variant]
    usd = {s: data[s][0] for s in USD_PAIRS.values()}
    atrs = {s: atr(b["h"], b["l"], b["c"], 14) for s, (b, _) in data.items()}
    rows, d = [], first
    while d <= last:
        day = (d - EPOCH).days
        d += timedelta(days=1)
        if (day + 3) % 7 >= 5 or holiday(day):
            continue
        t_a, t_b, t_x = (int(london_utc(day, hh, 0)) for hh in (h_a, h_b, EXIT_HOUR))
        st = strength(usd, t_a, t_b)
        if st is None:
            continue
        s_i, w_i = int(np.argmax(st)), int(np.argmin(st))
        sym, direction = pair_for(CCYS[s_i], CCYS[w_i])
        if sym is None:
            continue
        bars, cost = data[sym]
        k, e = bar_at(bars["t"], t_b), bar_at(bars["t"], t_x)
        if k < 1 or e < 0 or not np.isfinite(atrs[sym][k - 1]):
            continue
        dist = STOP_ATR * atrs[sym][k - 1]
        res = trade(bars, k, direction, dist, cost, exit_bar=e)
        rows.append(book(sym, bars, k, direction, dist, res, cost, rates, PAIRS.index(sym), s_i, w_i))
    return np.array(rows, dtype=ROW_DTYPE)


def basket_z(usd: dict) -> tuple[np.ndarray, dict]:
    """Common UTC time axis of the 7 USD pairs (bars present in all) and z per non-USD currency on it."""
    common = None
    for b in usd.values():
        common = b["t"] if common is None else np.intersect1d(common, b["t"])
    p = {}
    for c, sym in USD_PAIRS.items():
        b = usd[sym]
        p[c] = log_ccy(sym, b["c"][np.searchsorted(b["t"], common)])
    ch = {c: np.r_[np.full(Z_LOOK, np.nan), v[Z_LOOK:] - v[:-Z_LOOK]] for c, v in p.items()}
    z = {}
    for c in USD_PAIRS:
        others = np.mean([ch[k] for k in USD_PAIRS if k != c], axis=0)
        dev = ch[c] - others
        sd = np.full(len(dev), np.nan)
        ok = np.isfinite(dev)
        idx = np.flatnonzero(ok)
        if len(idx) >= Z_N:
            w = np.lib.stride_tricks.sliding_window_view(dev[idx], Z_N)
            sd[idx[Z_N - 1:]] = w.std(axis=1)
        with np.errstate(invalid="ignore", divide="ignore"):
            z[c] = dev / sd
    return common, z


def run_basket(data: dict, rates: RateTable, day_from: int, day_to: int) -> np.ndarray:
    """Y-USDB: trades with an entry bar on server days [day_from, day_to); prices only before day_to."""
    usd = {s: data[s][0][data[s][0]["ts"] < day_to * DAY] for s in USD_PAIRS.values()}
    common, zs = basket_z(usd)
    rows = []
    for c, sym in USD_PAIRS.items():
        bars, cost = usd[sym], data[sym][1]
        pos = np.searchsorted(common, bars["t"])
        on_axis = (pos < len(common)) & (common[np.clip(pos, 0, len(common) - 1)] == bars["t"])
        z = np.where(on_axis, zs[c][np.clip(pos, 0, len(common) - 1)], np.nan)
        a14 = atr(bars["h"], bars["l"], bars["c"], 14)
        sign_pair = 1 if sym.endswith("USD") else -1           # +1: buying the pair buys c
        ci = CCYS.index(c)
        n, i = len(bars), 0
        while i < n - 1:
            zi = z[i]
            k = i + 1
            day_k = int(bars["ts"][k] // DAY)
            if not np.isfinite(zi) or abs(zi) <= Z_K or not np.isfinite(a14[i]) or day_k < day_from or holiday(day_k):
                i += 1
                continue
            c_dir = -1 if zi > 0 else 1                            # fade: sell c when it is too strong
            d = c_dir * sign_pair
            flags = z * np.sign(zi) <= 0                           # z back at 0 or beyond (NaN: no exit)
            dist = STOP_ATR * a14[i]
            res = trade(bars, k, d, dist, cost, exit_flags=flags, max_bars=MAX_BARS)
            buy, sell = (ci, 0) if c_dir == 1 else (0, ci)
            rows.append(book(sym, bars, k, d, dist, res, cost, rates, PAIRS.index(sym), buy, sell))
            i = n if res[0] == END else res[1] + 1
    return np.array(rows, dtype=ROW_DTYPE)
