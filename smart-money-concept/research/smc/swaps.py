"""Overnight swaps from monthly short-term interest rates (FRED copies of OECD series).

Swap per rollover in price units = entry price x rate / 365 with
  long:  rate = r_base - r_quote - MARKUP
  short: rate = r_quote - r_base - MARKUP
(XAU has rate 0). Rollovers happen at 00:00 server time after each trading day (Mon-Fri server
days); the one after Wednesday counts three nights. A position pays the rollovers R with
entry < R <= exit. Months after the end of a series use its last value.
"""
from __future__ import annotations

from pathlib import Path

import numpy as np

from smc import timez
from smc.config import DATA_DIR

RATES_DIR = DATA_DIR / "raw" / "rates"
# call money rates; 3-month interbank for NZD and CHF, whose call money series end in 2024
RATE_SERIES = {"USD": "IRSTCI01USM156N", "EUR": "IRSTCI01EZM156N", "GBP": "IRSTCI01GBM156N",
               "JPY": "IRSTCI01JPM156N", "AUD": "IRSTCI01AUM156N", "CAD": "IRSTCI01CAM156N",
               "NZD": "IR3TIB01NZM156N", "CHF": "IR3TIB01CHM156N"}
MARKUP = 0.01            # assumed broker markup per side, per year
WEDNESDAY = 2            # server weekday (Monday = 0) whose rollover counts three nights


def month_index(t_utc) -> np.ndarray:
    """Months since 1970-01 of UTC epoch seconds."""
    return np.asarray(t_utc, dtype="datetime64[s]").astype("datetime64[M]").astype(np.int64)


def parse_fred_csv(text: str) -> tuple[np.ndarray, np.ndarray]:
    """(month index, rate as a decimal) from a FRED graph CSV; rows without a number are skipped."""
    months, rates = [], []
    for line in text.splitlines()[1:]:
        parts = line.strip().split(",")
        if len(parts) != 2:
            continue
        try:
            value = float(parts[1])
            month = np.datetime64(parts[0][:7], "M").astype(np.int64)
        except ValueError:
            continue
        months.append(month)
        rates.append(value / 100.0)
    order = np.argsort(months, kind="stable")
    return np.asarray(months, np.int64)[order], np.asarray(rates, float)[order]


class RateTable:
    def __init__(self, series: dict[str, tuple[np.ndarray, np.ndarray]]):
        self.series = series

    @classmethod
    def load(cls, rates_dir: Path = RATES_DIR) -> "RateTable":
        return cls({ccy: parse_fred_csv((rates_dir / f"{sid}.csv").read_text(encoding="utf-8"))
                    for ccy, sid in RATE_SERIES.items()})

    @classmethod
    def constant(cls, rates: dict[str, float]) -> "RateTable":
        return cls({ccy: (np.array([0], np.int64), np.array([r], float)) for ccy, r in rates.items()})

    def rate(self, ccy: str, month: int) -> float:
        if ccy == "XAU":
            return 0.0
        months, values = self.series[ccy]
        i = int(np.searchsorted(months, month, side="right")) - 1
        return float(values[max(i, 0)])


def rollovers(t_entry: int, t_exit: int) -> tuple[np.ndarray, np.ndarray]:
    """Rollover times (UTC) with t_entry < R <= t_exit and the nights each one charges."""
    d0 = int(timez.utc_to_server(t_entry)) // timez.DAY
    d1 = int(timez.utc_to_server(t_exit)) // timez.DAY
    days = np.arange(d0, d1 + 1)
    weekday = (days + 3) % 7
    days = days[weekday < 5]
    r = timez.server_to_utc((days + 1) * timez.DAY)
    keep = (r > t_entry) & (r <= t_exit)
    nights = np.where((days[keep] + 3) % 7 == WEDNESDAY, 3, 1)
    return r[keep], nights


def swap_r(symbol: str, d: int, t_entry: int, t_exit: int, price: float, risk: float, table: RateTable) -> float:
    """Sum of swaps of a position in R (positive = credit)."""
    r, nights = rollovers(t_entry, t_exit)
    if not len(r):
        return 0.0
    base, quote = symbol[:3], symbol[3:]
    total = 0.0
    for month, k in zip(month_index(r), nights):
        diff = table.rate(base, int(month)) - table.rate(quote, int(month))
        total += k * (d * diff - MARKUP)
    return total * price / 365.0 / risk
