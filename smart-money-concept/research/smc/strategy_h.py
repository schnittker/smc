"""Model H 'trend following on indices and commodities' (P7), as pre-registered in
docs/12_P7_Vorregistrierung_ModellH.md.

The trend rule of Model G (strategy_g.run_trend) on 13 CFDs, each marked and traded at a fixed New York
time inside its liquid cash session. Costs: FTMO's average raw spread (FXVerify, 2026) expressed relative
to the mean 2026 price and applied in basis points to all years, slippage of a quarter spread per fill,
commission only on metals (0.0007 % per side). Swaps per rollover, annual rate as a fraction of notional:
  indices  d x (dividend yield - rate of the index currency) - 2.5 %
  oil      d x (0 - USD rate) - 2.5 %        (the futures roll yield is not modelled)
  metals   d x (0 - USD rate) - 1 %
plus the 0.7 % conversion fee on episode results of non-USD profit currencies.
"""
from __future__ import annotations

from calendar import timegm
from dataclasses import dataclass

import numpy as np

from smc.strategy_g import CONVERSION_FEE, run_trend
from smc.swaps import RateTable

HOUR, MIN = 3600, 60
SLIPPAGE_SPREADS = 0.25
SPREAD_FROM, SPREAD_TO = timegm((2026, 1, 1, 0, 0, 0)), timegm((2026, 10, 17, 0, 0, 0))


def server_time(ny_hour: int, ny_minute: int) -> int:
    """New York wall-clock time -> seconds after server midnight (server = New York + 7 h)."""
    return ((ny_hour + 7) % 24) * HOUR + ny_minute * MIN


US, EUROPE, TOKYO, HONG_KONG, SYDNEY = (server_time(15, 50), server_time(10, 50), server_time(0, 50),
                                        server_time(2, 50), server_time(23, 50))


@dataclass(frozen=True)
class CfdSpec:
    symbol: str             # HistData symbol
    ftmo: str               # FTMO symbol
    currency: str           # profit currency
    rate_ccy: str           # currency whose short-term rate finances the position
    mark_time: int          # server seconds after midnight: daily mark and rebalancing
    spread_abs: float       # FTMO average spread in price units (2026)
    dividend: float         # dividend yield p. a. of a price index (0 otherwise)
    markup: float           # swap markup p. a.
    commission_side: float  # commission per side as a fraction of notional
    rel_spread: float = float("nan")

    @property
    def signal_time(self) -> int:
        return self.mark_time - 5 * MIN

    @property
    def fee_rate(self) -> float:
        return CONVERSION_FEE if self.currency != "USD" else 0.0

    def trade_cost(self, price: float) -> float:
        """Cost of trading one unit, in price units: half spread + slippage + commission per side."""
        return (self.rel_spread / 2 + SLIPPAGE_SPREADS * self.rel_spread + self.commission_side) * price

    def spread(self, price: float) -> float:
        return self.rel_spread * price

    def swap_rate(self, d: int, month: int, rates: RateTable) -> float:
        return d * (self.dividend - rates.rate(self.rate_ccy, month)) - self.markup


SPECS = {s.symbol: s for s in (
    CfdSpec("SPXUSD", "US500.cash", "USD", "USD", US, 0.55, 0.018, 0.025, 0.0),
    CfdSpec("NSXUSD", "US100.cash", "USD", "USD", US, 1.66, 0.008, 0.025, 0.0),
    CfdSpec("GRXEUR", "GER40.cash", "EUR", "EUR", EUROPE, 1.58, 0.0, 0.025, 0.0),
    CfdSpec("FRXEUR", "FRA40.cash", "EUR", "EUR", EUROPE, 2.25, 0.028, 0.025, 0.0),
    CfdSpec("UKXGBP", "UK100.cash", "GBP", "GBP", EUROPE, 1.34, 0.038, 0.025, 0.0),
    CfdSpec("ETXEUR", "EU50.cash", "EUR", "EUR", EUROPE, 2.0, 0.032, 0.025, 0.0),
    CfdSpec("JPXJPY", "JP225.cash", "JPY", "JPY", TOKYO, 10.0, 0.019, 0.025, 0.0),
    CfdSpec("HKXHKD", "HK50.cash", "HKD", "USD", HONG_KONG, 6.99, 0.035, 0.025, 0.0),
    CfdSpec("AUXAUD", "AUS200.cash", "AUD", "AUD", SYDNEY, 1.61, 0.042, 0.025, 0.0),
    CfdSpec("WTIUSD", "USOIL.cash", "USD", "USD", US, 0.08, 0.0, 0.025, 0.0),
    CfdSpec("BCOUSD", "UKOIL.cash", "USD", "USD", US, 0.08, 0.0, 0.025, 0.0),
    CfdSpec("XAGUSD", "XAGUSD", "USD", "USD", US, 0.071, 0.0, 0.01, 0.000007),
    CfdSpec("XAUUSD", "XAUUSD", "USD", "USD", US, 0.52, 0.0, 0.01, 0.000007),
)}
SYMBOLS_H = tuple(SPECS)


def relative_spread(symbol: str, m5: np.ndarray) -> float:
    """FTMO's average spread divided by the mean 2026 close in the data."""
    sel = (m5["t"] >= SPREAD_FROM) & (m5["t"] < SPREAD_TO)
    return SPECS[symbol].spread_abs / float(m5["c"][sel].mean())


def spec_for(symbol: str, m5: np.ndarray) -> CfdSpec:
    s = SPECS[symbol]
    return CfdSpec(**{**s.__dict__, "rel_spread": relative_spread(symbol, m5)})


def run_model_h(symbol: str, m5: np.ndarray, rates: RateTable, day_to: int | None = None) -> np.ndarray:
    """One row (strategy_g.DAY_DTYPE) per trading day of `symbol`, up to server day day_to (excl.)."""
    return run_trend(spec_for(symbol, m5), m5, rates, day_to)
