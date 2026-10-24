"""Trading costs on an FTMO Swing account (research chapter 8), in price units.

FX: typical raw spread + 0.3 pip volume-band surcharge (1-15 lots) as the effective spread,
5 USD commission per lot round turn converted into the quote currency, 0.1 pip slippage
per market fill. XAUUSD: spread + 0.05 USD band surcharge, commission 0.0014 % of the price,
0.02 USD slippage. The 0.7 % currency conversion fee on non-USD quotes is not included
(about 0.01 R per trade).
"""
from __future__ import annotations

from smc.pipeline import TYPICAL_SPREAD

# quote currency units per USD, ECB reference rates of 23.10.2026 (research chapter 7)
QUOTE_PER_USD = {"USD": 1.0, "JPY": 156.8, "CAD": 1.3995, "CHF": 0.8244, "AUD": 1 / 0.7022, "NZD": 1 / 0.5687}
COMMISSION_RT_USD_PER_LOT = 5.0
CONTRACT = 100_000


def pip_size(symbol: str) -> float:
    return 0.01 if symbol.endswith("JPY") else 0.0001


def effective_spread(symbol: str) -> float:
    """Spread a 1-15 lot order actually pays (raw spread + volume-band surcharge)."""
    if symbol == "XAUUSD":
        return TYPICAL_SPREAD[symbol] + 0.05
    return TYPICAL_SPREAD[symbol] + 0.3 * pip_size(symbol)


def commission_price(symbol: str, price: float) -> float:
    """Round-turn commission expressed as a price distance."""
    if symbol == "XAUUSD":
        return 0.000014 * price
    return COMMISSION_RT_USD_PER_LOT * QUOTE_PER_USD[symbol[3:]] / CONTRACT


def slippage_price(symbol: str) -> float:
    """Assumed slippage of one market fill (market entry, stop, time exit)."""
    return 0.02 if symbol == "XAUUSD" else 0.1 * pip_size(symbol)


def cost_in_price(symbol: str, price: float) -> float:
    """All-in round trip for a market-in, market-out trade (used by the P2 event study)."""
    return effective_spread(symbol) + commission_price(symbol, price) + slippage_price(symbol)
