"""Model LL 'lead-lag' (strategies no. 58 and 59), as pre-registered in docs/01_Vorregistrierung.md.

LL-AJ   z = ln-return of the US500 H1 bar i / std of the last 500 such returns; |z| > 1.5 -> AUDJPY in the same
        direction from the open of bar i+1, exit after 3 bars held, fixed stop 2 ATR14 (chart.engine)
LL-Y1   USDJPY long / short at the 16:50 New York mark of server day d by the sign of the last DGS10 change before
        calendar day d; weight 10 % / sigma reset every day
LL-Y20  sign of the change over the last 20 DGS10 observations before d; weight set when the sign changes
"""
from __future__ import annotations

import csv
from datetime import date
from pathlib import Path

import numpy as np

from carry.model import CarrySpec, apply_days, ewma_sigma, run_weights
from chart.engine import run_trades
from dbo.model import EPOCH, Costs
from hkb.model import atr
from smc.strategy_g import VOL_TARGET
from smc.swaps import RateTable

VARIANTS = ("LL-AJ", "LL-Y1", "LL-Y20")
Z_N, Z_K, AJ_BARS, STOP_ATR = 500, 1.5, 3, 2.0
H1 = 3600


def load_dgs10(path: Path) -> tuple[np.ndarray, np.ndarray]:
    """Calendar day numbers and yields (%) of the rows with a value."""
    days, vals = [], []
    with open(path, newline="") as f:
        for row in csv.DictReader(f):
            v = (row.get("DGS10") or "").strip()
            if v in ("", "."):
                continue
            days.append((date.fromisoformat(row["observation_date"]) - EPOCH).days)
            vals.append(float(v))
    return np.array(days, np.int64), np.array(vals)


def yield_sign(server_days: np.ndarray, y_days: np.ndarray, y: np.ndarray, lag: int) -> np.ndarray:
    """sign(y[last obs before d] - y[lag obs earlier]) per server day d (0 if not enough history)."""
    k = np.searchsorted(y_days, server_days, side="left") - 1
    out = np.zeros(len(server_days), np.int8)
    ok = k - lag >= 0
    diff = np.zeros(len(server_days))
    diff[ok] = y[k[ok]] - y[k[ok] - lag]
    out[ok] = np.sign(diff[ok]).astype(np.int8)
    return out


def yield_targets(variant: str, px: dict, y_days: np.ndarray, y: np.ndarray) -> dict[int, float]:
    days = px["day"]
    sig = yield_sign(days, y_days, y, 1 if variant == "LL-Y1" else 20)
    sigma = ewma_sigma(np.r_[np.nan, np.diff(np.log(px["p_mark"]))])
    out, cur = {}, 0
    for z in range(1, len(days)):
        s = int(sig[z])
        if not px["exact"][z] or not np.isfinite(sigma[z - 1]):
            continue
        if variant == "LL-Y1" or s != cur:
            out[int(days[z])] = s * VOL_TARGET / sigma[z - 1] if s else 0.0
            cur = s
    return out


def run_yield(variant: str, px: dict, y_days: np.ndarray, y: np.ndarray, rates: RateTable) -> np.ndarray:
    return run_weights(CarrySpec("USDJPY"), px, apply_days(px, yield_targets(variant, px, y_days, y)), rates)


def aj_signals(aud: np.ndarray, spx: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """(signal, stop level, minimum distance) per AUDJPY H1 bar from the US500 bar with the same UTC open."""
    r = np.r_[np.nan, np.diff(np.log(spx["c"]))]
    sd = np.full(len(r), np.nan)
    w = np.lib.stride_tricks.sliding_window_view(r[1:], Z_N)
    sd[Z_N:] = w.std(axis=1)
    z = r / sd
    a = atr(aud["h"], aud["l"], aud["c"], 14)
    pos = np.searchsorted(spx["t"], aud["t"])
    ok = (pos < len(spx)) & (spx["t"][np.clip(pos, 0, len(spx) - 1)] == aud["t"])
    zz = np.where(ok, z[np.clip(pos, 0, len(spx) - 1)], np.nan)
    sig = np.zeros(len(aud), np.int8)
    sig[zz > Z_K] = 1
    sig[zz < -Z_K] = -1
    dist = STOP_ATR * a
    stop = np.full(len(aud), np.nan)                             # finite levels beyond the entry: the engine
    stop[sig == 1] = 1e12                                        # then places the stop exactly at entry -+ dist
    stop[sig == -1] = 0.0
    return sig, stop, dist


def run_aj(aud: np.ndarray, spx: np.ndarray, cost: Costs, rates: RateTable, day_from: int, day_to: int) -> np.ndarray:
    aud = aud[aud["ts"] < day_to * 86400]
    spx = spx[spx["ts"] < day_to * 86400]
    sig, stop, dist = aj_signals(aud, spx)
    return run_trades("AUDJPY", aud, H1, cost, rates, None, sig, stop, dist, day_from, 1e9, AJ_BARS)
