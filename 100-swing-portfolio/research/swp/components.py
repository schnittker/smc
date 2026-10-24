"""Daily series of the four building blocks, loaded and run exactly as in their run_*.py scripts.

Period "is": 2015-2023 (model V and F on prices cut at 2024-01-01, as in their in-sample runs).
Period "ho": events / days from 2024-01-01 on, prices up to the end of the data."""
from __future__ import annotations

from calendar import timegm
from datetime import date

import numpy as np

from smc import timez
from smc.data.bars import load_bars
from smc.strategy_g import daily_prices
from smc.strategy_h import spec_for
from smc.swaps import RateTable
from carry.model import USD_PAIRS
from fomc.model import EPOCH, Index, load_dates, run_model_p
from tom.model import run_model_t
from volm.model import run_model_v
from ffx.model import run_model_f

from swp.portfolio import book_daily, book_events, book_trades

IS_FROM = timegm((2015, 1, 1, 0, 0, 0)) // timez.DAY
IS_TO = timegm((2024, 1, 1, 0, 0, 0)) // timez.DAY
HO_TO = 10 ** 9


def years_of(days) -> np.ndarray:
    return np.array([date.fromordinal(EPOCH.toordinal() + int(d)).year for d in days])


def spx_index() -> Index:
    m5 = load_bars("SPXUSD", "M5")
    return Index(spec_for("SPXUSD", m5), m5, load_bars("SPXUSD", "D1"))


def trade_exposure(rows: np.ndarray) -> dict:
    """1x nominal on every server day from entry to exit (inclusive)."""
    out: dict[int, float] = {}
    for a, b in zip(timez.fx_day(rows["t_entry"]).tolist(), timez.fx_day(rows["t_exit"]).tolist()):
        for d in range(a, b + 1):
            out[d] = out.get(d, 0.0) + 1.0
    return out


def load(period: str) -> tuple[dict, dict]:
    """({component: {day: (net, worst, active)}}, {component: {day: US500 nominal}}) for the period."""
    rates = RateTable.load()
    ho = period == "ho"
    lo, hi = (IS_TO, HO_TO) if ho else (IS_FROM, IS_TO)
    spx = spx_index()

    fomc = load_dates()
    fomc = fomc[(years_of(fomc) >= 2024) if ho else np.isin(years_of(fomc), list(range(2015, 2024)))]
    p = run_model_p("P-SPX", spx, fomc, rates)
    t = run_model_t("T-FRÜH", spx, (2024, 1) if ho else (2015, 1), (2026, 12) if ho else (2023, 12), rates)

    m5 = load_bars("SPXUSD", "M5")
    spec = spec_for("SPXUSD", m5)
    px = daily_prices(m5, spec.signal_time, spec.mark_time)
    if not ho:
        px = {k: v[px["day"] < IS_TO] for k, v in px.items()}
    v = run_model_v("V-VOL", spec, px, rates)
    v = v[(v["day"] >= lo) & (v["day"] < hi)]

    pxs = {}
    for sym in USD_PAIRS.values():
        q = daily_prices(load_bars(sym, "M5"))
        pxs[sym] = q if ho else {k: x[q["day"] < IS_TO] for k, x in q.items()}
    f_rows, f_log = run_model_f("F-CARRY", pxs, fomc, rates)

    series = {"P-SPX": book_trades(p), "T-FRÜH": book_trades(t), "V-VOL": book_daily(v),
              "F-CARRY": book_events(f_rows, f_log)}
    expo = {"P-SPX": trade_exposure(p), "T-FRÜH": trade_exposure(t),
            "V-VOL": {int(d): float(w) for d, w in zip(v["day"], v["w"])}}
    return series, expo
