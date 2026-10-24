"""Round-trip trading cost in price units on an FTMO Swing account (research chapter 8).

FX: typical raw spread + 0.3 pip volume-band surcharge (1-15 lots) + 5 USD commission per lot
round turn converted into the quote currency + 0.1 pip slippage. XAUUSD: spread + 0.0014 %
of the price (commission) + 0.05 USD band surcharge + 0.02 USD slippage. The 0.7 % currency
conversion fee on non-USD quotes is not included (about 0.01 R per trade).
"""
from __future__ import annotations

from smc.pipeline import TYPICAL_SPREAD

# quote currency units per USD, ECB reference rates of 23.10.2026 (research chapter 7)
QUOTE_PER_USD = {"USD": 1.0, "JPY": 156.8, "CAD": 1.3995, "CHF": 0.8244, "AUD": 1 / 0.7022, "NZD": 1 / 0.5687}
COMMISSION_RT_USD_PER_LOT = 5.0
CONTRACT = 100_000


def pip_size(symbol: str) -> float:
    return 0.01 if symbol.endswith("JPY") else 0.0001


def cost_in_price(symbol: str, price: float) -> float:
    if symbol == "XAUUSD":
        return TYPICAL_SPREAD[symbol] + 0.000014 * price + 0.05 + 0.02
    pip = pip_size(symbol)
    commission = COMMISSION_RT_USD_PER_LOT * QUOTE_PER_USD[symbol[3:]] / CONTRACT
    return TYPICAL_SPREAD[symbol] + 0.3 * pip + commission + 0.1 * pip
