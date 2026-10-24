"""Model PL 'placebo controls' (no. 98 and 99), as pre-registered in docs/01_Vorregistrierung.md.

PL-RANDOM  entry with probability 1/30 per H4 bar, random direction (rng seed 98 + instrument index, one draw pair
           per bar); stop 2 ATR14, target 2 R, time exit 30 bars (chart.engine)
PL-MOON    long from new moon to full moon, short from full moon to new moon (age < 14.765 days), 10 % / sigma
"""
from __future__ import annotations

import numpy as np

from carry.model import apply_days, ewma_sigma, run_weights
from smc.strategy_g import VOL_TARGET
from smc import timez

P_ENTRY, STOP_ATR = 1 / 30, 2.0
SYNODIC = 29.530588853
NEW_MOON_REF = (np.datetime64("2000-01-06T18:14:00") - np.datetime64("1970-01-01T00:00:00")).astype("timedelta64[s]").astype(np.int64)


def random_signals(n: int, seed: int) -> np.ndarray:
    rng = np.random.default_rng(seed)
    u, d = rng.random(n), rng.random(n)
    sig = np.zeros(n, np.int8)
    sig[u < P_ENTRY] = np.where(d[u < P_ENTRY] < 0.5, 1, -1)
    return sig


def moon_age(t_utc: np.ndarray) -> np.ndarray:
    return ((np.asarray(t_utc, np.int64) - NEW_MOON_REF) / 86400.0) % SYNODIC


def moon_targets(spec, px: dict) -> dict[int, float]:
    days = px["day"]
    t_mark = timez.server_to_utc(days * timez.DAY + spec.mark_time)
    sig = np.where(moon_age(t_mark) < SYNODIC / 2, 1.0, -1.0)
    sigma = ewma_sigma(np.r_[np.nan, np.diff(np.log(px["p_mark"]))])
    out, cur = {}, 0.0
    for i in range(len(days)):
        if not px["exact"][i] or not np.isfinite(sigma[i]):
            continue
        if sig[i] != cur:
            out[int(days[i])] = float(sig[i] * VOL_TARGET / sigma[i])
            cur = sig[i]
    return out


def run_moon(spec, px: dict, rates) -> np.ndarray:
    return run_weights(spec, px, apply_days(px, moon_targets(spec, px)), rates)
