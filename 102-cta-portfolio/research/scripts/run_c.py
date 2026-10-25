#!/usr/bin/env python3
"""Strategy no. 102, model C (multi-asset trend, CTA): in-sample runs T313 (C-FIX) and T314 (C-WF) with the
pre-registered acceptance check, and - only for a variant that passed - the one-time hold-out T315 with the FTMO
bootstrap T316 (docs/01_Vorregistrierung.md).

Usage:
  ../../smart-money-concept/research/.venv/bin/python -I scripts/run_c.py                 # T313 + T314
  ../../smart-money-concept/research/.venv/bin/python -I scripts/run_c.py --holdout C-WF  # T315 + T316, once
"""
import argparse
import sys
from datetime import date
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from cta import DATA_DIR, RESULTS_DIR  # noqa: E402
from cta.model import (CLASS_VOL, CLASSES, LOOKBACKS, LOOKBACKS_CRYPTO, SETS, book_market, dense,  # noqa: E402
                       portfolio, walk_forward)
from cta.universe import HO_END, load_markets  # noqa: E402
from smc.report import cluster_bootstrap_ci, cluster_t  # noqa: E402
from smc.swaps import RateTable  # noqa: E402
from swp.portfolio import LEVELS, bootstrap, historical  # noqa: E402

VARIANTS = ("C-FIX", "C-WF")
CAL_FROM, IS_FROM, IS_TO = 16071, 16436, 19723     # 2014-01-01, 2015-01-01, 2024-01-01
MARGIN_MAX = 0.5
MARKER = DATA_DIR / "ho" / "DONE"
DAYS_PER_MONTH = 365.25 / 12


def year_of(days):
    return np.asarray(days * 86400, dtype="datetime64[s]").astype("datetime64[Y]").astype(int) + 1970


def month_of(days):
    return np.asarray(days * 86400, dtype="datetime64[s]").astype("datetime64[M]").astype(np.int64)


def build(day_to: int | None):
    """Dense books of all three lookback sets."""
    rates = RateTable.load()
    markets = load_markets(day_to)
    n_cls = {c: sum(m["cls"] == c for m in markets.values()) for c in CLASSES}
    end = HO_END if day_to is None else day_to
    dn = {}
    for s in SETS:
        books = {}
        for name, m in markets.items():
            lb = (LOOKBACKS_CRYPTO if m["kind"] == "crypto" else LOOKBACKS)[s]
            books[name] = book_market(m, lb, CLASS_VOL / n_cls[m["cls"]], rates)
        dn[s] = dense(books, markets, CAL_FROM, end)
    return markets, dn


def run_variant(v: str, markets: dict, dn: dict, last_year: int):
    choice = walk_forward(dn, range(2015, last_year + 1)) if v == "C-WF" else None
    return portfolio(dn, markets, choice), choice


def window(pf: dict, lo: int, hi: int) -> dict:
    sel = (pf["days"] >= lo) & (pf["days"] < hi)
    out = {k: (v[sel] if isinstance(v, np.ndarray) else v) for k, v in pf.items() if k != "by_class"}
    out["by_class"] = {c: x[sel] for c, x in pf["by_class"].items()}
    return out


def stats(p: dict) -> dict:
    x, days = p["net"], p["days"]
    n, sd = len(x), x.std(ddof=1)
    yr = year_of(days)
    years = n / 365.25
    m = {"n": n, "E": float(x.mean()), "sd": float(sd), "ann": float(x.sum() / years),
         "sharpe": float(x.mean() / sd * np.sqrt(365.25)), "t_iid": float(x.mean() / (sd / np.sqrt(n))),
         "t_week": cluster_t(x, (days + 3) // 7), "t_month": cluster_t(x, month_of(days)),
         "cost": float(p["cost"].sum() / years), "E_2x": float((x - p["cost"]).mean()),
         "by_year": {int(y): float(x[yr == y].sum()) for y in np.unique(yr)},
         "by_class": {c: float(v.sum() / years) for c, v in p["by_class"].items()},
         "long": float(p["long"].sum() / years), "short": float(p["short"].sum() / years),
         "margin_avg": float(p["margin"].mean()), "margin_max": float(p["margin"].max()),
         "trans": float(p["trans"].sum() / years)}
    m["t"] = min(m["t_iid"], m["t_week"], m["t_month"])
    m["years_pos"] = sum(v > 0 for v in m["by_year"].values())
    m["cls_pos"] = sum(v > 0 for v in m["by_class"].values())
    return m


def checks_is(m: dict) -> list:
    ny = len(m["by_year"])
    return [("Mittleres Netto-Tagesergebnis > 0 mit t ≥ 3,0 (kleinster aus iid / Woche / Monat)",
             f"{m['E'] * 1e4:+.2f} bp/Tag, t = {m['t']:.2f}", m["E"] > 0 and m["t"] >= 3.0),
            (f"≥ 6 von {ny} Jahren positiv", f"{m['years_pos']} von {ny}", m["years_pos"] >= 6),
            ("≥ 3 von 4 Klassen positiv", f"{m['cls_pos']} von 4", m["cls_pos"] >= 3),
            ("bei doppelten Kosten > 0", f"{m['E_2x'] * 1e4:+.2f} bp/Tag", m["E_2x"] > 0)]


def report(name: str, m: dict, checks: list, choice: dict | None) -> list[str]:
    ok = all(k for _, _, k in checks)
    out = [f"## {name}\n", "| Kennzahl | Wert |", "|---|---|", f"| Kalendertage | {m['n']:,} |",
           f"| Netto je Tag (Anteil des Kapitals, unskaliert) | {m['E'] * 1e4:+.2f} bp (σ {m['sd'] * 1e4:.1f} bp) |",
           f"| Rendite p. a. (unskaliert) | {m['ann']:+.1%} bei {m['sd'] * np.sqrt(365.25):.1%} Vola |",
           f"| Sharpe Ratio p. a. | {m['sharpe']:.2f} |",
           f"| t-Wert iid / Woche / Monat | {m['t_iid']:.2f} / {m['t_week']:.2f} / {m['t_month']:.2f} |",
           f"| Kosten + Swap-Belastung p. a. (davon Umstellung) | {m['cost']:.2%} ({m['trans']:.2%}) |",
           f"| Long / Short vor Kosten p. a. | {m['long']:+.2%} / {m['short']:+.2%} |",
           f"| Margin-Auslastung Ø / max. (unskaliert) | {m['margin_avg']:.3f} / {m['margin_max']:.3f} |",
           f"| bei doppelten Kosten | {m['E_2x'] * 1e4:+.2f} bp/Tag |", "", "| Kriterium | Ergebnis | erfüllt |",
           "|---|---|---|"]
    out += [f"| {c} | {v} | {'ja' if k else '**nein**'} |" for c, v, k in checks]
    out += ["", f"**{name}: {'alle Kriterien erfüllt' if ok else 'nicht bestanden'}.**\n",
            "| Klasse | Netto p. a. |", "|---|---|"] + [f"| {c} | {v:+.2%} |" for c, v in m["by_class"].items()]
    out += ["", "| Jahr | Netto |", "|---|---|"] + [f"| {y} | {v:+.2%} |" for y, v in m["by_year"].items()]
    if choice:
        out += ["", "| Jahr | " + " | ".join(CLASSES) + " |", "|---|" + "---|" * len(CLASSES)]
        out += [f"| {y} | " + " | ".join(f"{ch['set'][c]} ×{ch['a'][c]:.2f}" for c in CLASSES) + " |"
                for y, ch in choice.items()]
    return out + [""]


def in_sample():
    markets, dn = build(IS_TO)
    lines = ["# Modell C (Multi-Asset-Trend, CTA), In-Sample 2015–2023 (Trial T313 C-FIX, T314 C-WF)\n",
             f"Lauf vom {date.today():%d.%m.%Y}. Regeln laut `docs/01_Vorregistrierung.md`, Code `research/cta/`. "
             "24 Märkte in 4 Klassen (FX 7, Indizes 8, Rohstoffe 4, Krypto 5 ab 2018); je Klasse 10 % Risikobudget. "
             "Netto = nach Spread, Slippage, Kommission, Swaps (Krypto 20 % p. a.) und Gebühren; Tagesrendite als Anteil "
             "des Kapitals vor der FTMO-Skalierung, Kalendertage (Wochenende nur Krypto).\n"]
    verdict = {}
    for v in VARIANTS:
        pf, choice = run_variant(v, markets, dn, 2023)
        m = stats(window(pf, IS_FROM, IS_TO))
        checks = checks_is(m)
        verdict[v] = (m, all(k for _, _, k in checks))
        lines += report(v, m, checks, choice)
    passed = [v for v, (_, ok) in verdict.items() if ok]
    if passed:
        best = max(passed, key=lambda v: verdict[v][0]["t"])
        lines.append(f"**Ergebnis:** bestanden: {', '.join(passed)}; gewählt für den Hold-out: **{best}** "
                     "(vorher Artefakt-Prüfung).")
    else:
        lines.append("**Ergebnis: Keine Variante erfüllt alle In-Sample-Kriterien. Strategie Nr. 102 ist gescheitert; "
                     "der Hold-out bleibt unberührt.**")
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    (RESULTS_DIR / "c_in_sample.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))


def ftmo(p: dict, sd_is: float) -> tuple[list[str], bool]:
    out = ["## FTMO-Block-Bootstrap auf IS + Hold-out (T316)\n",
           "| Tagesschwankung | k | P(Phase 1) | P(Phase 2) | P(beide) | Median-Dauer (Monate) | historische Starts | erfüllt |",
           "|---|---|---|---|---|---|---|---|"]
    ok_any = False
    for s in LEVELS:
        k = s / sd_is
        cap = np.minimum(1.0, MARGIN_MAX / np.maximum(k * p["margin"], 1e-12))
        r, w = p["net"] * cap, p["worst"] * cap
        bs = bootstrap(r, w, p["active"], p["days"], k, days_per_month=DAYS_PER_MONTH)
        h = historical(r, w, p["active"], p["days"], k, days_per_month=DAYS_PER_MONTH)
        ok = bs["both"] >= 0.70 and bs["median_months"] <= 12
        ok_any |= ok
        out.append(f"| {s:.2%} | {k:.2f} | {bs['p1']:.0%} | {bs['p2']:.0%} | **{bs['both']:.0%}** | "
                   f"{bs['median_months']:.1f} | {h['passed']} von {h['resolved']} | {'ja' if ok else 'nein'} |")
    return out + [""], ok_any


def holdout(variant: str):
    if MARKER.exists():
        sys.exit("Hold-out wurde bereits ausgewertet (data/ho/DONE) – kein zweiter Lauf.")
    markets, dn = build(IS_TO)
    pf_is, _ = run_variant(variant, markets, dn, 2023)
    m_is = stats(window(pf_is, IS_FROM, IS_TO))
    if not all(k for _, _, k in checks_is(m_is)):
        sys.exit(f"{variant} hat die In-Sample-Kriterien nicht erfüllt – kein Hold-out.")
    MARKER.parent.mkdir(parents=True, exist_ok=True)
    MARKER.write_text(f"T315 {variant} {date.today().isoformat()}\n")
    markets, dn = build(None)
    pf, choice = run_variant(variant, markets, dn, 2026)
    p_ho = window(pf, IS_TO, HO_END)
    m = stats(p_ho)
    is_p = window(pf_is, IS_FROM, IS_TO)
    lo, hi = cluster_bootstrap_ci(is_p["net"], month_of(is_p["days"]))
    checks = [("Mittleres Netto-Tagesergebnis > 0", f"{m['E'] * 1e4:+.2f} bp/Tag", m["E"] > 0),
              ("≥ untere 95-%-Grenze von IS (Cluster nach Monat)",
               f"{m['E'] * 1e4:+.2f} vs. IS {m_is['E'] * 1e4:+.2f} [{lo * 1e4:+.2f}; {hi * 1e4:+.2f}] bp/Tag", m["E"] >= lo)]
    ok = all(k for _, _, k in checks)
    lines = [f"# Modell C, Hold-out 01.01.2024–16.10.2026 (Trial T315, {variant})\n",
             f"Einmaliger Lauf vom {date.today():%d.%m.%Y}.\n"]
    lines += report(variant, m, checks, {y: c for y, c in (choice or {}).items() if y >= 2024})
    if ok:
        both = {k: np.r_[is_p[k], p_ho[k]] for k in ("net", "worst", "margin", "active", "days")}
        ft, passed = ftmo(both, m_is["sd"])
        lines += ft + [f"**T316: {'bestanden – Strategie Nr. 102 erfüllt alle Kriterien' if passed else 'nicht bestanden'}.**"]
    else:
        lines.append("**Ergebnis: Hold-out nicht bestanden; kein FTMO-Bootstrap (T316 entfällt).**")
    (RESULTS_DIR / "c_holdout.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--holdout", choices=list(VARIANTS))
    a = ap.parse_args()
    holdout(a.holdout) if a.holdout else in_sample()


if __name__ == "__main__":
    main()
