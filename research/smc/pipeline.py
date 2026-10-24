"""Per-symbol feature build: bars -> structure, zones, liquidity pools, sweeps, MSS.

Every derived object keeps the bar index (and so the time) at which it becomes known,
so downstream studies can join timeframes as-of without lookahead. Parameters are the
pre-registered defaults from the blueprint / research chapter 2 (not optimised).
"""
from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np

from smc.config import DATA_DIR
from smc.data.bars import TF_SECONDS, load_bars
from smc.engine.atr import atr
from smc.engine.liquidity import (EQ, PDHL, PMHL, POOL_DTYPE, PWHL, SESSION_ASIA, SESSION_LDN, SESSION_PRELDN,
                                  SWING_EXT, SWING_INT, calendar_period_bars, equal_level_pools, evaluate_pools,
                                  group_outcomes, period_pools, pools_from_pivots, session_pools)
from smc.engine.mss import find_mss
from smc.engine.pivots import fractal_pivots, leg_pivots
from smc.engine.structure import run_structure
from smc.engine.zones import detect_fvg, detect_order_blocks

TFS = ("D1", "H4", "H1", "M15", "M5")
PIVOT_LEN = {"D1": (3, 10), "H4": (5, 20), "H1": (5, 30), "M15": (5, 40), "M5": (5, 50)}
K_FVG = {"D1": 0.10, "H4": 0.12, "H1": 0.15, "M15": 0.20, "M5": 0.25}
K_DISP = {"D1": 1.0, "H4": 1.1, "H1": 1.2, "M15": 1.3, "M5": 1.4}
DAY = 86400

# Typical raw spread in price units (research chapter 7, IC Markets / Pepperstone averages).
# Used only where the engine needs a spread (ask-side pierce of buy stops, minimum gap size).
TYPICAL_SPREAD = {
    "EURUSD": 0.1e-4, "GBPUSD": 0.2e-4, "USDJPY": 0.2e-2, "AUDUSD": 0.1e-4, "NZDUSD": 0.38e-4,
    "USDCAD": 0.2e-4, "USDCHF": 0.2e-4, "EURJPY": 0.30e-2, "GBPJPY": 0.82e-2, "AUDJPY": 0.50e-2,
    "NZDJPY": 0.60e-2, "CADJPY": 0.48e-2, "CHFJPY": 0.86e-2, "EURCAD": 0.74e-4, "EURCHF": 0.61e-4,
    "EURNZD": 1.32e-4, "EURAUD": 0.80e-4, "GBPCHF": 1.10e-4, "GBPNZD": 1.98e-4, "GBPCAD": 1.12e-4,
    "GBPAUD": 1.06e-4, "AUDNZD": 0.77e-4, "AUDCAD": 0.68e-4, "CADCHF": 0.58e-4, "XAUUSD": 0.10,
}

SESSIONS = {SESSION_ASIA: (20 * 60, 24 * 60), SESSION_PRELDN: (0, 2 * 60), SESSION_LDN: (2 * 60, 7 * 60)}


@dataclass
class TFData:
    bars: np.ndarray
    t_close: np.ndarray
    atr14: np.ndarray
    atr200: np.ndarray
    piv_int: np.ndarray
    piv_ext: np.ndarray
    structure: object
    fvg: np.ndarray
    ob: np.ndarray


@dataclass
class SymbolFeatures:
    symbol: str
    tf: dict = field(default_factory=dict)
    sth: np.ndarray | None = None
    pools: np.ndarray | None = None
    outcomes: np.ndarray | None = None
    sweeps: np.ndarray | None = None
    mss: np.ndarray | None = None


def build_tf(symbol: str, tf: str, bars: np.ndarray | None = None) -> TFData:
    b = load_bars(symbol, tf) if bars is None else bars
    o, h, l, c = b["o"], b["h"], b["l"], b["c"]
    a14, a200 = atr(h, l, c, 14), atr(h, l, c, 200)
    li, le = PIVOT_LEN[tf]
    pi, pe = leg_pivots(h, l, li), leg_pivots(h, l, le)
    st = run_structure(h, l, c, pi, pe)
    spread = TYPICAL_SPREAD[symbol]
    fv = detect_fvg(o, h, l, c, a14, k_fvg=K_FVG[tf], min_abs=3 * spread, kd=K_DISP[tf])
    ob = detect_order_blocks(o, h, l, c, a14, st.events, fv, kd=K_DISP[tf])
    return TFData(b, b["t"] + TF_SECONDS[tf], a14, a200, pi, pe, st, fv, ob)


def build_pools(symbol: str, tfd: dict[str, TFData]) -> np.ndarray:
    m15, h1, h4, d1, m5 = tfd["M15"], tfd["H1"], tfd["H4"], tfd["D1"], tfd["M5"]
    parts = [
        pools_from_pivots(m15.piv_int, m15.t_close, SWING_INT, 5 * DAY),
        pools_from_pivots(h1.piv_ext, h1.t_close, SWING_EXT, 20 * DAY),
        pools_from_pivots(h4.piv_ext, h4.t_close, SWING_EXT, 40 * DAY),
        equal_level_pools(leg_pivots(m15.bars["h"], m15.bars["l"], 3), m15.t_close, m15.atr200, m15.atr14),
        session_pools(m5.bars, SESSIONS),
        period_pools(d1.bars, DAY, PDHL, ttl_periods=1),
    ]
    for period, kind, ttl in (("W", PWHL, 7 * DAY), ("M", PMHL, 31 * DAY)):
        hilo, t_close = calendar_period_bars(d1.bars, period)
        for side, col in ((1, 0), (-1, 1)):
            p = np.empty(len(hilo), POOL_DTYPE)
            p["side"], p["kind"], p["px"] = side, kind, hilo[:, col]
            p["t_avail"], p["t_expire"] = t_close, t_close + ttl
            parts.append(p)
    pools = np.concatenate([p for p in parts if len(p)])
    return pools[np.argsort(pools["t_avail"], kind="stable")]


def build_symbol(symbol: str, bars: dict[str, np.ndarray] | None = None) -> SymbolFeatures:
    """Full feature build from the bar files (or from given bars per timeframe, e.g. in tests)."""
    feats = SymbolFeatures(symbol)
    for tf in TFS:
        feats.tf[tf] = build_tf(symbol, tf, None if bars is None else bars[tf])
    m5 = feats.tf["M5"]
    b = m5.bars
    feats.sth = fractal_pivots(b["h"], b["l"], 1)
    feats.pools = build_pools(symbol, feats.tf)
    feats.outcomes = evaluate_pools(feats.pools, b["t"], b["h"], b["l"], b["c"], spread=TYPICAL_SPREAD[symbol])
    feats.sweeps = group_outcomes(feats.outcomes)
    feats.mss = find_mss(feats.sweeps, b["o"], b["h"], b["l"], b["c"], m5.atr14, feats.sth, m5.fvg,
                         window=20, kd=K_DISP["M5"])
    return feats


def save(feats: SymbolFeatures) -> None:
    out = DATA_DIR / "derived"
    out.mkdir(parents=True, exist_ok=True)
    arrays = {"sth": feats.sth, "pools": feats.pools, "outcomes": feats.outcomes, "sweeps": feats.sweeps,
              "mss": feats.mss}
    for tf, d in feats.tf.items():
        st = d.structure
        arrays.update({
            f"{tf}_events": st.events, f"{tf}_fvg": d.fvg, f"{tf}_ob": d.ob,
            f"{tf}_trend": st.trend, f"{tf}_bias_int": st.bias_int, f"{tf}_bias_ext": st.bias_ext,
            f"{tf}_trail_top": st.trail_top, f"{tf}_trail_bot": st.trail_bot,
            f"{tf}_atr14": d.atr14, f"{tf}_piv_int": d.piv_int, f"{tf}_piv_ext": d.piv_ext,
        })
    np.savez_compressed(out / f"{feats.symbol}.npz", **arrays)
