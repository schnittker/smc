"""Binance spot daily klines (00:00 UTC) of the five coins, aligned on one calendar of UTC day numbers."""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np

from kry import RAW_DIR

COINS = ("BTC", "ETH", "LTC", "XRP", "ADA")
LAST_DAY = 20385                     # 2026-10-24, last complete day of the download on 25.10.2026


def read_coin(coin: str, raw_dir: Path = RAW_DIR) -> np.ndarray:
    """Rows (day, o, h, l, c) sorted by day, only complete days up to LAST_DAY."""
    rows = []
    for f in sorted(raw_dir.glob(f"{coin}USDT_*.json")):
        rows += json.loads(f.read_text())
    arr = np.array([(r[0] // 86_400_000, float(r[1]), float(r[2]), float(r[3]), float(r[4])) for r in rows])
    arr = arr[np.argsort(arr[:, 0], kind="stable")]
    arr = arr[np.r_[True, np.diff(arr[:, 0]) > 0]]
    return arr[arr[:, 0] <= LAST_DAY]


def panel(raw_dir: Path = RAW_DIR, coins=COINS) -> dict:
    """{"day": calendar, "o"/"h"/"l"/"c": (days x coins), NaN before listing; missing days forward-filled
    with o = h = l = c = previous close (none occur in the download)."""
    data = {c: read_coin(c, raw_dir) for c in coins}
    d0 = int(min(a[0, 0] for a in data.values()))
    d1 = int(max(a[-1, 0] for a in data.values()))
    days = np.arange(d0, d1 + 1)
    out = {"day": days, "coins": list(coins)}
    for k in "ohlc":
        out[k] = np.full((len(days), len(coins)), np.nan)
    for j, c in enumerate(coins):
        a = data[c]
        idx = (a[:, 0] - d0).astype(int)
        for i, k in enumerate("ohlc", start=1):
            out[k][idx, j] = a[:, i]
        first = idx[0]
        for t in range(first + 1, len(days)):
            if np.isnan(out["c"][t, j]):
                out["o"][t, j] = out["h"][t, j] = out["l"][t, j] = out["c"][t, j] = out["c"][t - 1, j]
    return out
