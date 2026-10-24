"""Model K 'FX carry G8', as pre-registered in docs/01_Vorregistrierung.md.

On the first trading day of every month the eight major currencies are ranked by last month's short-term
interest rate; K-3 holds the carry positions (1/8), (2/7), (3/6), K-1 only (1/8). A carry position H/L is
traded through the H/L cross if one of the 24 FX pairs is that cross, otherwise through two USD pairs. Each
position targets 10 % volatility (EWMA of the daily H/L returns from the USD pairs' 16:50 New York prices).
Weights stay constant until the next month. Accounting (16:50 New York marks, trading costs, swaps with
markup, 0.7 % fee on episode results) is that of model G (smc.strategy_g.run_trend), generalised to a
given schedule of target weights.
"""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from smc import timez
from smc.config import SYMBOLS
from smc.strategy_g import ANNUAL, DAY_DTYPE, VOL_ALPHA, VOL_FLOOR, VOL_TARGET, WEDNESDAY, FxSpec, _holiday
from smc.swaps import MARKUP, RateTable, month_index

CURRENCIES = ("USD", "EUR", "GBP", "JPY", "AUD", "CAD", "NZD", "CHF")
FX = tuple(s for s in SYMBOLS if s != "XAUUSD")
USD_PAIRS = {"EUR": "EURUSD", "GBP": "GBPUSD", "AUD": "AUDUSD", "NZD": "NZDUSD",
             "JPY": "USDJPY", "CAD": "USDCAD", "CHF": "USDCHF"}
VARIANTS = {"K-3": ((0, 7), (1, 6), (2, 5)), "K-1": ((0, 7),)}
VOL_START = 60


@dataclass(frozen=True)
class CarrySpec(FxSpec):
    """FxSpec with an adjustable swap markup (default: the SMC swap model's 1 % p. a.)."""
    markup: float = MARKUP

    def swap_rate(self, d: int, month: int, rates: RateTable) -> float:
        diff = rates.rate(self.symbol[:3], month) - rates.rate(self.symbol[3:], month)
        return d * diff - self.markup


def ranking(rates: RateTable, month: int) -> list[str]:
    """Currencies by the rate of `month` (months since 1970-01), highest first, ties alphabetical."""
    return sorted(CURRENCIES, key=lambda c: (-rates.rate(c, month), c))


def legs(high: str, low: str) -> dict[str, int]:
    """Instrument signs (+1 = long the symbol) of one unit long `high` / short `low`."""
    if high + low in FX:
        return {high + low: 1}
    if low + high in FX:
        return {low + high: -1}
    out: dict[str, int] = {}
    for ccy, sgn in ((high, 1), (low, -1)):
        sym = USD_PAIRS[ccy]
        out[sym] = out.get(sym, 0) + (sgn if sym.startswith(ccy) else -sgn)
    return out


def usd_log_prices(px: dict[str, dict]) -> tuple[np.ndarray, dict[str, np.ndarray]]:
    """Common trading days (all 7 USD pairs marked exactly at 16:50 New York) and log USD value of each
    currency per such day."""
    common = None
    for sym in USD_PAIRS.values():
        d = px[sym]["day"][px[sym]["exact"]]
        common = d if common is None else np.intersect1d(common, d)
    logp = {"USD": np.zeros(len(common))}
    for ccy, sym in USD_PAIRS.items():
        p = px[sym]["p_mark"][np.searchsorted(px[sym]["day"], common)]
        logp[ccy] = np.log(p) if sym.startswith(ccy) else -np.log(p)
    return common, logp


def ewma_sigma(r: np.ndarray) -> np.ndarray:
    """Annualised EWMA volatility at each day (model G's estimator: start value = variance of the first 60
    returns, centre of mass 60 days, floor 4 % p. a.); NaN before day VOL_START."""
    out = np.full(len(r), np.nan)
    var = np.nan
    for z in range(len(r)):
        if z == VOL_START:
            var = float(np.var(r[1:VOL_START + 1]))
        elif z > VOL_START:
            var = (1 - VOL_ALPHA) * var + VOL_ALPHA * r[z] ** 2
        if z >= VOL_START:
            out[z] = max(np.sqrt(ANNUAL * var), VOL_FLOOR)
    return out


def rebalance_days(common: np.ndarray) -> np.ndarray:
    """Indices into `common` of the first trading day of each month (not 24.12.-01.01.), once volatility exists."""
    ok = ~_holiday(common)
    months = month_index(common * timez.DAY)
    idx = []
    seen = set()
    for z in np.flatnonzero(ok):
        if z >= VOL_START and months[z] not in seen:
            idx.append(int(z))
        seen.add(months[z])
    return np.array(idx, dtype=np.int64)


def schedule(px: dict[str, dict], rates: RateTable, variant: str) -> tuple[dict[str, dict[int, float]], list]:
    """Target weight per instrument and rebalance day, and a log (day, long currencies, short currencies)."""
    common, logp = usd_log_prices(px)
    sigma = {}
    targets: dict[str, dict[int, float]] = {s: {} for s in FX}
    log = []
    for z in rebalance_days(common):
        day = int(common[z])
        rank = ranking(rates, int(month_index(day * timez.DAY)) - 1)
        w: dict[str, float] = {}
        for hi, lo in VARIANTS[variant]:
            h, l_ = rank[hi], rank[lo]
            if (h, l_) not in sigma:
                cross = logp[h] - logp[l_]
                sigma[(h, l_)] = ewma_sigma(np.r_[np.nan, np.diff(cross)])
            n = VOL_TARGET / sigma[(h, l_)][z]
            for sym, sgn in legs(h, l_).items():
                w[sym] = w.get(sym, 0.0) + sgn * n
        for sym in FX:
            targets[sym][day] = w.get(sym, 0.0)
        log.append((day, [rank[i] for i, _ in VARIANTS[variant]], [rank[j] for _, j in VARIANTS[variant]]))
    return targets, log


def apply_days(px: dict, targets: dict[int, float]) -> dict[int, float]:
    """Move each rebalance target to the instrument's first exactly marked day on or after it (and before
    the next rebalance day)."""
    days, exact = px["day"], px["exact"]
    rdays = sorted(targets)
    out = {}
    for k, r in enumerate(rdays):
        end = rdays[k + 1] if k + 1 < len(rdays) else np.iinfo(np.int64).max
        i = int(np.searchsorted(days, r))
        while i < len(days) and days[i] < end and not exact[i]:
            i += 1
        if i < len(days) and days[i] < end:
            out[int(days[i])] = targets[r]
    return out


def run_weights(spec, px: dict, targets: dict[int, float], rates: RateTable) -> np.ndarray:
    """Daily rows (smc.strategy_g.DAY_DTYPE) of one instrument that moves to targets[day] at the 16:50
    New York mark of that day and holds its weight otherwise; accounting as smc.strategy_g.run_trend."""
    days, p_mark = px["day"], px["p_mark"]
    n = len(days)
    weekday = (days + 3) % 7
    months = month_index(timez.server_to_utc(days * timez.DAY + spec.mark_time))
    rows = np.zeros(n, DAY_DTYPE)
    rows["symbol"], rows["day"], rows["p_sig"], rows["p_mark"] = spec.symbol, days, px["p_sig"], p_mark
    w = episode = 0.0
    for z in range(n):
        pnl = worst = 0.0
        if z >= 1 and w != 0.0:
            prev = p_mark[z - 1]
            pnl = w * (p_mark[z] / prev - 1)
            extreme = px["lo"][z] if w > 0 else px["hi"][z] + spec.spread(prev)
            worst = min(0.0, w * (extreme / prev - 1))
        episode += pnl
        target = targets.get(int(days[z]), w)
        trade_cost = abs(target - w) * spec.trade_cost(p_mark[z]) / p_mark[z]
        realized = fee = 0.0
        if w != 0.0 and np.sign(target) != np.sign(w):
            realized, episode = episode, 0.0
            fee = spec.fee_rate * abs(realized)
        swap = 0.0
        if target != 0.0:
            d = 1 if target > 0 else -1
            nights = 3 if weekday[z] == WEDNESDAY else 1
            swap = abs(target) * spec.swap_rate(d, int(months[z]), rates) * nights / 365
        r_ = rows[z]
        r_["rebalance"], r_["w"] = target != w, target
        r_["pnl"], r_["trade_cost"], r_["swap"], r_["fee"], r_["realized"], r_["worst"] = (
            pnl, trade_cost, swap, fee, realized, worst)
        r_["net"] = pnl - trade_cost + swap - fee
        r_["cost"] = trade_cost + fee + max(-swap, 0.0)
        w = target
    return rows


def run_model_k(px: dict[str, dict], rates: RateTable, variant: str, markup: float = MARKUP) -> tuple[np.ndarray, list]:
    """Rows of all instruments that are ever held, and the rebalance log."""
    targets, log = schedule(px, rates, variant)
    parts = []
    for sym in FX:
        if any(v != 0.0 for v in targets[sym].values()):
            parts.append(run_weights(CarrySpec(sym, markup=markup), px[sym], apply_days(px[sym], targets[sym]), rates))
    return np.concatenate(parts), log
