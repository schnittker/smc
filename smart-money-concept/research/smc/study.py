"""Event study (gate P2): does a building block move price more than matched placebo bars?

For every event we enter at the open of the first M5 bar after the event is known, in the
direction of the hypothesis, and measure in units of A = ATR14(M15) as of the event:
  - first passage +2A target vs -1A stop within 24 h (R = +2 / -1, timeout = mark-to-market),
  - same with +1A / -1A,
  - signed forward returns after 1 h, 4 h and 12 h.
Second variant with the wider unit A_H1 = ATR14(H1): +2/-1 within 3 trading days.
Placebos: random M5 bars of the same symbol with the same New York hour and the same
ATR decile, traded in the same direction. Same-bar target/stop hits count as losses.
"""
from __future__ import annotations

import numpy as np

from smc import timez
from smc.engine.liquidity import BROKEN, SWEPT
from smc.engine.structure import CHOCH_STRICT, EXT
from smc.engine.zones import lifecycle
from smc.pipeline import SymbolFeatures

HORIZON = 288          # M5 bars = 24 trading hours
HORIZON_H1 = 864       # M5 bars = 3 trading days, for the wider ATR(H1) unit
FWD = (12, 48, 144)    # 1 h, 4 h, 12 h
OUT_DTYPE = np.dtype([
    ("etype", "U24"), ("symbol", "U6"), ("i", "i8"), ("dir", "i1"), ("t", "i8"), ("day", "i8"),
    ("hour", "i1"), ("session", "U8"), ("trend_h4", "i1"), ("trend_d1", "i1"), ("label", "U12"),
    ("unit", "f8"), ("r21", "f8"), ("r11", "f8"), ("f1h", "f8"), ("f4h", "f8"), ("f12h", "f8"),
    ("unit_h1", "f8"), ("r21_h1", "f8"), ("placebo", "?"),
])


def session_of(ny_minute: np.ndarray) -> np.ndarray:
    m = ny_minute
    return np.select(
        [(m >= 1200), (m < 120), (m < 300), (m < 420), (m < 600), (m < 1020)],
        ["asia", "pre_ldn", "ldn_kz", "ldn_late", "ny_kz", "ny_late"], default="eve")


def _asof(t_close: np.ndarray, t: np.ndarray) -> np.ndarray:
    """Index of the last bar closed at or before t (-1 if none)."""
    return np.searchsorted(t_close, t, side="right") - 1


def first_passage(o, h, l, c, i0: np.ndarray, d: np.ndarray, unit: np.ndarray, tp: float, sl: float,
                  horizon: int = HORIZON) -> np.ndarray:
    """R multiple (1R = sl*unit) of a market entry at open[i0]; NaN if not enough data."""
    n = len(c)
    out = np.full(len(i0), np.nan)
    for z, (i, dd, a) in enumerate(zip(i0, d, unit)):
        if i < 0 or i + horizon > n or not np.isfinite(a) or a <= 0:
            continue
        e = o[i]
        hs, ls = h[i:i + horizon], l[i:i + horizon]
        if dd == 1:
            hit_tp, hit_sl = hs >= e + tp * a, ls <= e - sl * a
        else:
            hit_tp, hit_sl = ls <= e - tp * a, hs >= e + sl * a
        t_tp = int(np.argmax(hit_tp)) if hit_tp.any() else horizon
        t_sl = int(np.argmax(hit_sl)) if hit_sl.any() else horizon
        if t_sl <= t_tp and t_sl < horizon:
            out[z] = -1.0
        elif t_tp < horizon:
            out[z] = tp / sl
        else:
            out[z] = np.clip(dd * (c[i + horizon - 1] - e) / (sl * a), -1.0, tp / sl)
    return out


def forward(o, c, i0, d, unit, h_bars):
    n = len(c)
    j = i0 + h_bars - 1
    ok = (i0 >= 0) & (j < n) & np.isfinite(unit) & (unit > 0)
    out = np.full(len(i0), np.nan)
    out[ok] = d[ok] * (c[j[ok]] - o[i0[ok]]) / unit[ok]
    return out


class EventStudy:
    def __init__(self, feats: SymbolFeatures, t_from: int, t_to: int, seed: int = 0, n_placebo: int = 3):
        self.f = feats
        m5 = feats.tf["M5"].bars
        self.m5 = m5
        self.o, self.h, self.l, self.c = m5["o"], m5["h"], m5["l"], m5["c"]
        self.t_open = m5["t"]
        self.t_from, self.t_to = t_from, t_to
        self.rng = np.random.default_rng(seed)
        self.n_placebo = n_placebo
        m15 = feats.tf["M15"]
        # unit and trend as of every M5 bar open (= what is known when entering at that open)
        self.unit_at = m15.atr14[np.clip(_asof(m15.t_close, self.t_open), 0, None)]
        self.unit_at[_asof(m15.t_close, self.t_open) < 0] = np.nan
        h1 = feats.tf["H1"]
        i_h1 = _asof(h1.t_close, self.t_open)
        self.unit_h1_at = np.where(i_h1 >= 0, h1.atr14[np.clip(i_h1, 0, None)], np.nan)
        self.trend_h4 = self._trend_at("H4")
        self.trend_d1 = self._trend_at("D1")
        ny_min = timez.ny_minute_of_day(self.t_open)
        self.hour = (ny_min // 60).astype(np.int8)
        self.session = session_of(ny_min)
        valid = np.isfinite(self.unit_at)
        dec_edges = np.nanpercentile(self.unit_at[valid], np.arange(10, 100, 10))
        self.decile = np.searchsorted(dec_edges, np.nan_to_num(self.unit_at, nan=-1.0))
        in_window = (self.t_open >= t_from) & (self.t_open < t_to) & valid
        self.strata = {}
        keys = self.hour.astype(np.int64) * 16 + self.decile
        for key in np.unique(keys[in_window]):
            self.strata[int(key)] = np.flatnonzero(in_window & (keys == key))
        self.keys = keys

    def _trend_at(self, tf: str) -> np.ndarray:
        d = self.f.tf[tf]
        idx = _asof(d.t_close, self.t_open)
        out = np.where(idx >= 0, d.structure.trend[np.clip(idx, 0, None)], 0)
        return out.astype(np.int8)

    def entry_index(self, t_known: np.ndarray) -> np.ndarray:
        return np.searchsorted(self.t_open, t_known, side="left")

    def _rows(self, etype, i0, d, label, placebo):
        keep = (i0 >= 0) & (i0 < len(self.t_open))
        i0, d, label = i0[keep], d[keep], np.asarray(label)[keep]
        t = self.t_open[i0]
        win = (t >= self.t_from) & (t < self.t_to)
        i0, d, label, t = i0[win], d[win], label[win], t[win]
        unit = self.unit_at[i0]
        rows = np.zeros(len(i0), OUT_DTYPE)
        rows["etype"], rows["symbol"], rows["i"], rows["dir"], rows["t"] = etype, self.f.symbol, i0, d, t
        rows["day"] = timez.fx_day(t)
        rows["hour"], rows["session"] = self.hour[i0], self.session[i0]
        rows["trend_h4"], rows["trend_d1"] = self.trend_h4[i0], self.trend_d1[i0]
        rows["label"], rows["unit"], rows["placebo"] = label, unit, placebo
        o, h, l, c = self.o, self.h, self.l, self.c
        rows["r21"] = first_passage(o, h, l, c, i0, d, unit, 2.0, 1.0)
        rows["r11"] = first_passage(o, h, l, c, i0, d, unit, 1.0, 1.0)
        for col, hb in zip(("f1h", "f4h", "f12h"), FWD):
            rows[col] = forward(o, c, i0, d, unit, hb)
        unit_h1 = self.unit_h1_at[i0]
        rows["unit_h1"] = unit_h1
        rows["r21_h1"] = first_passage(o, h, l, c, i0, d, unit_h1, 2.0, 1.0, horizon=HORIZON_H1)
        return rows

    def add(self, etype: str, t_known: np.ndarray, d: np.ndarray, label) -> np.ndarray:
        """Event rows plus matched placebo rows (same hour and ATR decile, same direction)."""
        i0 = self.entry_index(np.asarray(t_known, dtype=np.int64))
        d = np.asarray(d, dtype=np.int8)
        label = np.broadcast_to(np.asarray(label), (len(i0),))
        ev = self._rows(etype, i0, d, label, False)
        pi, pd, pl = [], [], []
        for row in ev:
            pool = self.strata.get(int(self.keys[row["i"]]))
            if pool is None or not len(pool):
                continue
            pick = pool[self.rng.integers(0, len(pool), self.n_placebo)]
            pi.append(pick)
            pd.append(np.full(len(pick), row["dir"]))
            pl.append(np.full(len(pick), row["label"]))
        if pi:
            pb = self._rows(etype, np.concatenate(pi), np.concatenate(pd), np.concatenate(pl), True)
            return np.concatenate([ev, pb])
        return ev

    # ---- building blocks -------------------------------------------------------------------
    def run_all(self) -> np.ndarray:
        f = self.f
        m5t = self.t_open
        out = []
        tclose_m5 = f.tf["M5"].t_close
        sw = f.sweeps
        for outcome, name, sign in ((SWEPT, "sweep_rev", -1), (BROKEN, "break_cont", 1)):
            s = sw[sw["outcome"] == outcome]
            out.append(self.add(name, tclose_m5[s["k"]], sign * s["side"], s["top_kind"].astype(str)))
        m = f.mss
        out.append(self.add("mss", tclose_m5[m["k"]], m["dir"], m["top_kind"].astype(str)))
        for tf, kind, max_bars in (("M5", "fvg", 288), ("M15", "fvg", 1440), ("H1", "fvg", 2880),
                                   ("M15", "ob", 1440), ("H1", "ob", 2880)):
            d = f.tf[tf]
            z = d.fvg if kind == "fvg" else d.ob
            start = np.searchsorted(m5t, d.t_close[z["k"]], side="left")
            life = lifecycle(z, start, self.o, self.h, self.l, self.c, max_bars)
            touched = life["touch"] >= 0
            out.append(self.add(f"{kind}_touch_{tf}", tclose_m5[life["touch"][touched]], z["dir"][touched],
                                np.where((z["flags"][touched] & 1) > 0, "strong", "normal")))
        for tf in ("H1", "H4"):
            d = f.tf[tf]
            ev = d.structure.events
            ext = ev[(ev["layer"] == EXT) & (ev["type"] != CHOCH_STRICT)]
            out.append(self.add(f"ext_break_{tf}", d.t_close[ext["k"]], ext["dir"],
                                np.where(ext["type"] == 1, "bos", "choch")))
            strict = ev[ev["type"] == CHOCH_STRICT]
            out.append(self.add(f"strict_flip_{tf}", d.t_close[strict["k"]], strict["dir"], "strict"))
        return np.concatenate(out)
