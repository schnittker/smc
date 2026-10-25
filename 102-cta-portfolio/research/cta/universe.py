"""The 24 markets of model C with prices and cost models (docs/01_Vorregistrierung.md, section 1)."""
from __future__ import annotations

import numpy as np

from carry.model import CarrySpec
from kry.data import panel
from smc.data.bars import load_bars
from smc.strategy_g import daily_prices
from smc.strategy_h import spec_for

FX = ("EURUSD", "GBPUSD", "AUDUSD", "NZDUSD", "USDJPY", "USDCAD", "USDCHF")
INDICES = ("SPXUSD", "NSXUSD", "GRXEUR", "FRXEUR", "UKXGBP", "JPXJPY", "HKXHKD", "AUXAUD")
COMMODITIES = ("XAUUSD", "XAGUSD", "WTIUSD", "BCOUSD")
COINS = ("BTC", "ETH", "LTC", "XRP", "ADA")
HO_END = int((np.datetime64("2026-10-17") - np.datetime64("1970-01-01")).astype(int))  # day after the last HistData
#                                                                 day 2026-10-16 (was hard-coded one year too early)


def cut(px: dict, day_to: int | None) -> dict:
    day_to = HO_END if day_to is None else min(day_to, HO_END)
    keep = px["day"] < day_to
    return {k: v[keep] for k, v in px.items()}


def load_markets(day_to: int | None) -> dict:
    """{name: market}; prices before day_to (None = up to the end of the HistData data)."""
    out = {}
    for sym in FX:
        spec = CarrySpec(sym)
        out[sym] = {"kind": "fx", "cls": "FX", "spec": spec,
                    "px": cut(daily_prices(load_bars(sym, "M5"), spec.signal_time, spec.mark_time), day_to)}
    for cls, syms in (("Indizes", INDICES), ("Rohstoffe", COMMODITIES)):
        for sym in syms:
            m5 = load_bars(sym, "M5")
            spec = spec_for(sym, m5)                # FTMO spread relative to the 2026 price level (as model H)
            out[sym] = {"kind": "cfd", "cls": cls, "spec": spec,
                        "px": cut(daily_prices(m5, spec.signal_time, spec.mark_time), day_to)}
    p = panel()
    for j, coin in enumerate(COINS):
        ok = np.isfinite(p["c"][:, j])
        px = {"day": p["day"][ok].astype(np.int64), "p_sig": p["c"][ok, j], "p_mark": p["c"][ok, j],
              "exact": np.ones(ok.sum(), bool), "lo": p["l"][ok, j], "hi": p["h"][ok, j]}
        out[coin] = {"kind": "crypto", "cls": "Krypto", "spec": None, "coin": coin, "px": cut(px, day_to)}
    return out
