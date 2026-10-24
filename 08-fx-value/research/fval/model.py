"""Model V 'FX value G8', as pre-registered in docs/01_Vorregistrierung.md.

Real exchange rate q_c(m) = ln S_c(m) + ln P_c(m-2) - ln P_US(m-2) (S = USD per unit of c at the month end, CPI with a
two-month publication lag; quarterly CPI counts from the month after the quarter; Japan's CPI after 06/2021 is
carried forward with the previous year's annual inflation). On the first trading day of month m the currencies are
ranked by -(q(m-1) - q(m-61)) (V-5Y) or -(q(m-1) - mean q since 01/1999) (V-PPP), USD = 0, ties alphabetically;
positions (1/8), (2/7), (3/6), sizing, rebalancing and accounting as model K-3 (../06-fx-carry).
"""
from __future__ import annotations

import csv
from pathlib import Path

import numpy as np

from carry.model import (CURRENCIES, FX, VARIANTS as K_VARIANTS, VOL_TARGET, CarrySpec, apply_days, ewma_sigma,
                         legs, rebalance_days, run_weights, usd_log_prices)
from smc import timez
from smc.swaps import MARKUP, RateTable, month_index

VARIANTS = ("V-5Y", "V-PPP")
POSITIONS = K_VARIANTS["K-3"]
CPI = {"USD": ("CPIAUCSL", "M"), "EUR": ("CP0000EZ19M086NEST", "M"), "GBP": ("GBRCPIALLMINMEI", "M"),
       "JPY": ("JPNCPIALLMINMEI", "M"), "CAD": ("CANCPIALLMINMEI", "M"), "CHF": ("CHECPIALLMINMEI", "M"),
       "AUD": ("AUSCPIALLQINMEI", "Q"), "NZD": ("NZLCPIALLQINMEI", "Q")}
FXS = {"EUR": ("DEXUSEU", False), "GBP": ("DEXUSUK", False), "JPY": ("DEXJPUS", True), "AUD": ("DEXUSAL", False),
       "NZD": ("DEXUSNZ", False), "CAD": ("DEXCAUS", True), "CHF": ("DEXSZUS", True)}
LAG, YEARS_5, PPP_FROM = 2, 60, 1999 * 12


def read_fred(path: Path) -> list[tuple[int, int, float]]:
    """(year, month, value) rows with a value."""
    out = []
    with open(path, newline="") as f:
        r = csv.reader(f)
        next(r)
        for row in r:
            if len(row) < 2 or row[1].strip() in ("", "."):
                continue
            y, m = int(row[0][:4]), int(row[0][5:7])
            out.append((y, m, float(row[1])))
    return out


def cpi_table(raw: Path, last_m: int) -> dict[str, np.ndarray]:
    """Monthly CPI per currency on the month index axis 0 .. last_m (m = year * 12 + month - 1), forward-filled."""
    out = {}
    jp_infl = {y: v for y, _, v in read_fred(raw / "FPCPITOTLZGJPN.csv")}
    for c, (sid, freq) in CPI.items():
        a = np.full(last_m + 1, np.nan)
        for y, m, v in read_fred(raw / f"{sid}.csv"):
            k = y * 12 + m - 1 + (3 if freq == "Q" else 0)      # quarterly: from the month after the quarter
            if k <= last_m and v > 0:                           # NZD has zero placeholders in 1914
                a[k] = v
        if freq == "Q":
            for k in range(1, last_m + 1):
                if np.isnan(a[k]) and np.isfinite(a[k - 1]):
                    a[k] = a[k - 1]
        last = int(np.flatnonzero(np.isfinite(a))[-1])
        for k in range(last + 1, last_m + 1):
            if c == "JPY":
                y = k // 12
                rate = jp_infl.get(y - 1, 0.0)
                a[k] = a[k - 1] * (1 + rate / 100) ** (1 / 12)
            else:
                a[k] = a[k - 1]
        out[c] = a
    return out


def fx_month_end(raw: Path, last_m: int) -> dict[str, np.ndarray]:
    out = {}
    for c, (sid, invert) in FXS.items():
        a = np.full(last_m + 1, np.nan)
        rows = []
        with open(raw / f"{sid}.csv", newline="") as f:
            r = csv.reader(f)
            next(r)
            for row in r:
                if len(row) >= 2 and row[1].strip() not in ("", "."):
                    rows.append((int(row[0][:4]) * 12 + int(row[0][5:7]) - 1, float(row[1])))
        for k, v in rows:                                   # rows are sorted: the last one of a month wins
            if k <= last_m:
                a[k] = 1 / v if invert else v
        out[c] = a
    return out


def real_rates(raw: Path, last_m: int) -> dict[str, np.ndarray]:
    cpi, fx = cpi_table(raw, last_m), fx_month_end(raw, last_m)
    q = {"USD": np.zeros(last_m + 1)}
    for c in FXS:
        p_c, p_us = np.full(last_m + 1, np.nan), np.full(last_m + 1, np.nan)
        p_c[LAG:], p_us[LAG:] = cpi[c][:-LAG], cpi["USD"][:-LAG]
        q[c] = np.log(fx[c]) + np.log(p_c) - np.log(p_us)
    return q


def value_signal(variant: str, q: dict[str, np.ndarray], m_prev: int) -> dict[str, float]:
    out = {}
    for c in CURRENCIES:
        if c == "USD":
            out[c] = 0.0
            continue
        x = q[c]
        if variant == "V-5Y":
            out[c] = -(x[m_prev] - x[m_prev - YEARS_5])
        else:
            hist = x[PPP_FROM:m_prev + 1]
            out[c] = -(x[m_prev] - np.nanmean(hist))
    return out


def ranking(variant: str, q: dict[str, np.ndarray], m_prev: int) -> list[str]:
    s = value_signal(variant, q, m_prev)
    return sorted(CURRENCIES, key=lambda c: (-s[c], c))


def schedule(px: dict[str, dict], q: dict[str, np.ndarray], variant: str) -> tuple[dict[str, dict[int, float]], list]:
    common, logp = usd_log_prices(px)
    sigma = {}
    targets: dict[str, dict[int, float]] = {s: {} for s in FX}
    log = []
    for z in rebalance_days(common):
        day = int(common[z])
        m_prev = int(month_index(day * timez.DAY)) + 1970 * 12 - 1      # absolute month index (year * 12 + month - 1)
        rank = ranking(variant, q, m_prev)
        w: dict[str, float] = {}
        for hi, lo in POSITIONS:
            h, l_ = rank[hi], rank[lo]
            if (h, l_) not in sigma:
                sigma[(h, l_)] = ewma_sigma(np.r_[np.nan, np.diff(logp[h] - logp[l_])])
            n = VOL_TARGET / sigma[(h, l_)][z]
            for sym, sgn in legs(h, l_).items():
                w[sym] = w.get(sym, 0.0) + sgn * n
        for sym in FX:
            targets[sym][day] = w.get(sym, 0.0)
        log.append((day, [rank[i] for i, _ in POSITIONS], [rank[j] for _, j in POSITIONS]))
    return targets, log


def run_model_v(px: dict[str, dict], q: dict[str, np.ndarray], rates: RateTable, variant: str,
                markup: float = MARKUP) -> tuple[np.ndarray, list]:
    targets, log = schedule(px, q, variant)
    parts = [run_weights(CarrySpec(sym, markup=markup), px[sym], apply_days(px[sym], targets[sym]), rates)
             for sym in FX if any(v != 0.0 for v in targets[sym].values())]
    return np.concatenate(parts), log
