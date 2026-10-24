"""Market structure shift after a liquidity sweep (trigger timeframe, blueprint 6.2).

Bullish case: a sell-side pool was SWEPT. The reference is the latest short-term high
(3-candle pivot) formed before the pierce. Within `window` bars a close above it, with a
displacement in the leg from the sweep low and (optionally) a bullish FVG in that leg,
is an MSS. A close below the sweep extreme first cancels the setup.
"""
from __future__ import annotations

import numpy as np

from smc.engine.displacement import DisplacementIndex
from smc.engine.liquidity import SWEPT

MSS_DTYPE = np.dtype([
    ("k", "i8"), ("dir", "i1"), ("sweep_k", "i8"), ("pierce", "i8"), ("extreme", "f8"),
    ("ref_px", "f8"), ("ref_i", "i8"), ("leg", "i8"), ("disp", "i8"), ("fvg", "i8"),
    ("fvg_top", "f8"), ("fvg_bot", "f8"), ("leg_hi", "f8"), ("kinds", "i4"), ("top_kind", "i1"),
])


def find_mss(sweeps: np.ndarray, o, h, l, c, atr14, sth: np.ndarray, fvgs: np.ndarray,
             window: int = 20, kd: float = 1.2, require_fvg: bool = True,
             disp: DisplacementIndex | None = None) -> np.ndarray:
    n = len(c)
    disp = disp or DisplacementIndex(o, h, l, c, atr14, kd)
    rows = []
    piv = {1: sth[sth["side"] == 1], -1: sth[sth["side"] == -1]}   # sorted by pivot bar
    fv = {1: fvgs[fvgs["dir"] == 1], -1: fvgs[fvgs["dir"] == -1]}  # sorted by origin (= k - 1)
    for ev in sweeps[sweeps["outcome"] == SWEPT]:
        d = -int(ev["side"])                 # SSL swept -> bullish shift, BSL swept -> bearish
        j, ks, ext = int(ev["pierce"]), int(ev["k"]), float(ev["extreme"])
        refs = piv[d]
        r = int(np.searchsorted(refs["i"], j, side="left")) - 1   # latest pivot before the pierce
        if r < 0 or refs["k"][r] > ks:
            continue
        ref_px, ref_i = float(refs["px"][r]), int(refs["i"][r])
        for k in range(ks + 1, min(n, ks + window + 1)):
            if (d == 1 and c[k] < ext) or (d == -1 and c[k] > ext):
                break
            if not ((d == 1 and c[k] > ref_px) or (d == -1 and c[k] < ref_px)):
                continue
            if d == 1:
                leg = k - int(np.argmin(l[j:k + 1][::-1]))
                leg_px, leg_hi = l[leg], h[leg:k + 1].max()
            else:
                leg = k - int(np.argmax(h[j:k + 1][::-1]))
                leg_px, leg_hi = h[leg], l[leg:k + 1].min()
            found = disp.first(leg, k, d)
            if found is None:
                break
            f = fv[d]
            lo_i, hi_i = np.searchsorted(f["origin"], [leg, k - 1], side="right")
            cand = f[lo_i:hi_i]
            if not len(cand) and require_fvg:
                break
            fidx, ftop, fbot = -1, np.nan, np.nan
            if len(cand):
                half = (leg_px + leg_hi) / 2
                in_discount = cand[cand["mid"] <= half] if d == 1 else cand[cand["mid"] >= half]
                pick = in_discount[-1] if len(in_discount) else cand[-1]
                fidx = int(np.searchsorted(fvgs["k"], pick["k"]))
                ftop, fbot = pick["top"], pick["bot"]
            rows.append((k, d, ks, j, leg_px, ref_px, ref_i, leg, found[0], fidx, ftop, fbot, leg_hi,
                         ev["kinds"], ev["top_kind"]))
            break
    out = np.array(rows, dtype=MSS_DTYPE)
    return out[np.argsort(out["k"], kind="stable")] if len(out) else out
