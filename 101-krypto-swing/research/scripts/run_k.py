#!/usr/bin/env python3
"""Strategy no. 101, model K (crypto swing trend following): in-sample runs T309 (K-TSM) and T310 (K-LONG) with
the pre-registered acceptance check, and - only for a variant that passed - the one-time hold-out T311 with the
FTMO bootstrap T312 (docs/01_Vorregistrierung.md).

Usage:
  ../../smart-money-concept/research/.venv/bin/python -I scripts/run_k.py                   # T309 + T310
  ../../smart-money-concept/research/.venv/bin/python -I scripts/run_k.py --holdout K-TSM   # T311 + T312, once
"""
import argparse
import sys
from datetime import date
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from kry import DATA_DIR, RESULTS_DIR  # noqa: E402
from kry.data import panel  # noqa: E402
from kry.model import ANNUAL, SWAP, VARIANTS, run  # noqa: E402
from smc.report import cluster_bootstrap_ci, cluster_t  # noqa: E402
from swp.portfolio import LEVELS, bootstrap, historical  # noqa: E402

IS_FROM, IS_TO = 17532, 19723                  # 2018-01-01, 2024-01-01 (UTC day numbers)
MARKER = DATA_DIR / "ho" / "DONE"
DAYS_PER_MONTH = 365.25 / 12


def year_of(days):
    return np.asarray(days * 86400, dtype="datetime64[s]").astype("datetime64[Y]").astype(int) + 1970


def month_of(days):
    return np.asarray(days * 86400, dtype="datetime64[s]").astype("datetime64[M]").astype(np.int64)


def cut(px: dict, day_to: int) -> dict:
    keep = px["day"] < day_to
    return {k: (v[keep] if isinstance(v, np.ndarray) else v) for k, v in px.items()}


def window(book: dict, days: np.ndarray, lo: int, hi: int) -> dict:
    sel = (days >= lo) & (days < hi)
    out = {k: v[sel] for k, v in book.items()}
    out["days"] = days[sel]
    return out


def stats(b: dict, coins: list) -> dict:
    x = b["net"].sum(axis=1)
    days, n, sd = b["days"], len(x), x.std(ddof=1)
    yr = year_of(days)
    cost, swap, pnl = b["cost"].sum(axis=1), b["swap"].sum(axis=1), b["pnl"].sum(axis=1)
    m = {"n": n, "E": float(x.mean()), "sd": float(sd), "ann": float(x.mean() * ANNUAL),
         "sharpe": float(x.mean() / sd * np.sqrt(ANNUAL)), "t_iid": float(x.mean() / (sd / np.sqrt(n))),
         "t_week": cluster_t(x, (days + 3) // 7), "t_month": cluster_t(x, month_of(days)),
         "gross": float(pnl.mean()), "cost": float(cost.mean()), "swap": float(swap.mean()),
         "E_2x": float((x - cost - swap).mean()),
         "swap10": float((x + swap / 2).mean()), "swap30": float((x - swap / 2).mean()),
         "by_year": {int(y): float(x[yr == y].sum()) for y in np.unique(yr)},
         "by_coin": {c: (float(b["net"][:, j].sum() / n * ANNUAL), float(b["pnl"][:, j].sum() / n * ANNUAL))
                     for j, c in enumerate(coins)},
         "long": float(np.where(b["w"] > 0, b["pnl"], 0).sum() / n * ANNUAL),
         "short": float(np.where(b["w"] < 0, b["pnl"], 0).sum() / n * ANNUAL),
         "gross_w": float(np.abs(b["w"]).sum(axis=1).mean()),
         "capped": float((np.abs(b["w"]).sum(axis=1) > 0.999).mean()),
         "x": x, "days": days, "worst": b["worst"].sum(axis=1), "w_gross": np.abs(b["w"]).sum(axis=1)}
    m["t"] = min(m["t_iid"], m["t_week"], m["t_month"])
    m["years_pos"] = sum(v > 0 for v in m["by_year"].values())
    m["coins_pos"] = sum(v[0] > 0 for v in m["by_coin"].values())
    return m


def checks_is(m: dict) -> list:
    ny, nc = len(m["by_year"]), len(m["by_coin"])
    return [("Mittleres Netto-Tagesergebnis > 0 mit t ≥ 3,0 (kleinster aus iid / Woche / Monat)",
             f"{m['E'] * 1e4:+.2f} bp/Tag, t = {m['t']:.2f}", m["E"] > 0 and m["t"] >= 3.0),
            (f"≥ 4 von {ny} Jahren positiv", f"{m['years_pos']} von {ny}", m["years_pos"] >= 4),
            (f"≥ 3 von {nc} Coins positiv", f"{m['coins_pos']} von {nc}", m["coins_pos"] >= 3),
            ("bei doppelten Kosten > 0", f"{m['E_2x'] * 1e4:+.2f} bp/Tag", m["E_2x"] > 0)]


def report(name: str, m: dict, checks: list) -> list[str]:
    ok = all(k for _, _, k in checks)
    out = [f"## {name}\n", "| Kennzahl | Wert |", "|---|---|", f"| Kalendertage | {m['n']:,} |",
           f"| Netto je Tag (Anteil des Kapitals) | {m['E'] * 1e4:+.2f} bp (σ {m['sd'] * 1e4:.1f} bp) |",
           f"| vor Kosten je Tag | {m['gross'] * 1e4:+.2f} bp |",
           f"| Handelskosten / Swap je Tag | {m['cost'] * 1e4:.2f} / {m['swap'] * 1e4:.2f} bp |",
           f"| Rendite p. a. (netto, unskaliert) | {m['ann']:+.1%} |", f"| Sharpe Ratio p. a. | {m['sharpe']:.2f} |",
           f"| t-Wert iid / Woche / Monat | {m['t_iid']:.2f} / {m['t_week']:.2f} / {m['t_month']:.2f} |",
           f"| Swap 10 % / 30 % p. a. statt 20 % | {m['swap10'] * 1e4:+.2f} / {m['swap30'] * 1e4:+.2f} bp/Tag |",
           f"| Long / Short vor Kosten p. a. | {m['long']:+.1%} / {m['short']:+.1%} |",
           f"| Ø Gesamtnominal / Anteil Tage an der 1:1-Grenze | {m['gross_w']:.2f} / {m['capped']:.0%} |",
           f"| bei doppelten Kosten | {m['E_2x'] * 1e4:+.2f} bp/Tag |", "", "| Kriterium | Ergebnis | erfüllt |",
           "|---|---|---|"]
    out += [f"| {c} | {v} | {'ja' if k else '**nein**'} |" for c, v, k in checks]
    out += ["", f"**{name}: {'alle Kriterien erfüllt' if ok else 'nicht bestanden'}.**\n",
            "| Jahr | Netto % |", "|---|---|"] + [f"| {y} | {v:+.1%} |" for y, v in m["by_year"].items()]
    out += ["", "| Coin | Netto p. a. | vor Kosten p. a. |", "|---|---|---|"]
    out += [f"| {c} | {a:+.1%} | {g:+.1%} |" for c, (a, g) in m["by_coin"].items()]
    return out + [""]


def buy_hold(px: dict, lo: int, hi: int) -> str:
    c = px["c"][:, 0]
    sel = (px["day"] >= lo) & (px["day"] < hi)
    r = (c[1:] / c[:-1] - 1)[sel[1:]] - SWAP / ANNUAL
    return f"Referenz BTC halten (1× Nominal, mit 20 % Swap): Sharpe {r.mean() / r.std(ddof=1) * np.sqrt(ANNUAL):.2f}, " \
           f"{r.mean() * ANNUAL:+.1%} p. a."


def books(variant: str, day_to: int | None):
    px = panel()
    if day_to is not None:
        px = cut(px, day_to)
    return px, run(variant, px)


def in_sample():
    lines = ["# Modell K (Krypto-Swing-Trendfolge), In-Sample 2018–2023 (Trial T309 K-TSM, T310 K-LONG)\n",
             f"Lauf vom {date.today():%d.%m.%Y}. Regeln laut `docs/01_Vorregistrierung.md`, Code `research/kry/`. "
             "Binance-Spot-Tageskerzen 00:00 UTC, BTC/ETH/LTC/XRP/ADA; je Coin 10 % Zielvola, Hebel ≤ 1:1. Netto = nach "
             "Spread, Slippage, Kommission und 20 % p. a. Swap auf das Nominal.\n"]
    verdict = {}
    for v in VARIANTS:
        px, b = books(v, IS_TO)
        m = stats(window(b, px["day"], IS_FROM, IS_TO), px["coins"])
        checks = checks_is(m)
        verdict[v] = (m, all(k for _, _, k in checks))
        lines += report(v, m, checks)
    lines += [buy_hold(px, IS_FROM, IS_TO), ""]
    passed = [v for v, (_, ok) in verdict.items() if ok]
    if passed:
        best = max(passed, key=lambda v: verdict[v][0]["t"])
        lines.append(f"**Ergebnis:** bestanden: {', '.join(passed)}; gewählt für den Hold-out: **{best}** "
                     "(vorher Artefakt-Prüfung).")
    else:
        lines.append("**Ergebnis: Keine Variante erfüllt alle In-Sample-Kriterien. Strategie Nr. 101 ist gescheitert; "
                     "der Hold-out bleibt unberührt.**")
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    (RESULTS_DIR / "k_in_sample.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))


def ftmo(m_is: dict, m_ho: dict) -> tuple[list[str], bool]:
    days = np.r_[m_is["days"], m_ho["days"]]
    r, w, g = np.r_[m_is["x"], m_ho["x"]], np.r_[m_is["worst"], m_ho["worst"]], np.r_[m_is["w_gross"], m_ho["w_gross"]]
    act = g > 0
    out = ["## FTMO-Block-Bootstrap auf IS + Hold-out (T312)\n",
           "| Tagesschwankung | k | P(Phase 1) | P(Phase 2) | P(beide) | Median-Dauer (Monate) | historische Starts | erfüllt |",
           "|---|---|---|---|---|---|---|---|"]
    ok_any = False
    for s in LEVELS:
        k = s / m_is["sd"]
        cap = np.minimum(1.0, 1.0 / np.maximum(k * g, 1e-12))
        bs = bootstrap(r * cap, w * cap, act, days, k, days_per_month=DAYS_PER_MONTH)
        h = historical(r * cap, w * cap, act, days, k, days_per_month=DAYS_PER_MONTH)
        ok = bs["both"] >= 0.70 and bs["median_months"] <= 12
        ok_any |= ok
        out.append(f"| {s:.2%} | {k:.2f} | {bs['p1']:.0%} | {bs['p2']:.0%} | **{bs['both']:.0%}** | "
                   f"{bs['median_months']:.1f} | {h['passed']} von {h['resolved']} | {'ja' if ok else 'nein'} |")
    return out + [""], ok_any


def holdout(variant: str):
    if MARKER.exists():
        sys.exit("Hold-out wurde bereits ausgewertet (data/ho/DONE) – kein zweiter Lauf.")
    px, b = books(variant, IS_TO)
    m_is = stats(window(b, px["day"], IS_FROM, IS_TO), px["coins"])
    if not all(k for _, _, k in checks_is(m_is)):
        sys.exit(f"{variant} hat die In-Sample-Kriterien nicht erfüllt – kein Hold-out.")
    MARKER.parent.mkdir(parents=True, exist_ok=True)
    MARKER.write_text(f"T311 {variant} {date.today().isoformat()}\n")
    px, b = books(variant, None)
    m = stats(window(b, px["day"], IS_TO, 10 ** 9), px["coins"])
    lo, hi = cluster_bootstrap_ci(m_is["x"], month_of(m_is["days"]))
    checks = [("Mittleres Netto-Tagesergebnis > 0", f"{m['E'] * 1e4:+.2f} bp/Tag", m["E"] > 0),
              ("≥ untere 95-%-Grenze von IS (Cluster nach Monat)",
               f"{m['E'] * 1e4:+.2f} vs. IS {m_is['E'] * 1e4:+.2f} [{lo * 1e4:+.2f}; {hi * 1e4:+.2f}] bp/Tag", m["E"] >= lo)]
    ok = all(k for _, _, k in checks)
    lines = [f"# Modell K, Hold-out 01.01.2024–24.10.2026 (Trial T311, {variant})\n",
             f"Einmaliger Lauf vom {date.today():%d.%m.%Y}.\n"]
    lines += report(variant, m, checks) + [buy_hold(px, IS_TO, 10 ** 9), ""]
    if ok:
        ft, passed = ftmo(m_is, m)
        lines += ft + [f"**T312: {'bestanden – Strategie Nr. 101 erfüllt alle Kriterien' if passed else 'nicht bestanden'}.**"]
    else:
        lines.append("**Ergebnis: Hold-out nicht bestanden; kein FTMO-Bootstrap (T312 entfällt).**")
    (RESULTS_DIR / "k_holdout.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--holdout", choices=list(VARIANTS))
    a = ap.parse_args()
    holdout(a.holdout) if a.holdout else in_sample()


if __name__ == "__main__":
    main()
