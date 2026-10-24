#!/usr/bin/env python3
"""Strategies no. 58 and 59, model LL (lead-lag): in-sample runs T210 (LL-AJ), T211 (LL-Y1) and T212 (LL-Y20) with
the pre-registered acceptance check and descriptive tables, and - only for a variant that passed - the one-time
hold-out run (docs/01_Vorregistrierung.md).

Usage:
  ../smart-money-concept/research/.venv/bin/python -I research/scripts/run_ll.py                 # T210-T212
  ../smart-money-concept/research/.venv/bin/python -I research/scripts/run_ll.py --holdout LL-AJ  # once
"""
import argparse
import sys
from datetime import date
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from ll import DATA_DIR, RESULTS_DIR  # noqa: E402
from ll.model import VARIANTS, Z_K, aj_signals, load_dgs10, run_aj, run_yield  # noqa: E402
from dbo.model import EPOCH, Costs  # noqa: E402
from smc.data.bars import load_bars  # noqa: E402
from smc.report import cluster_bootstrap_ci, cluster_t  # noqa: E402
from smc.strategy_g import daily_prices  # noqa: E402
from smc.swaps import RateTable  # noqa: E402

IS_YEARS, HO_YEARS = range(2015, 2024), range(2024, 2027)
IS_FROM, IS_TO = (date(2015, 1, 1) - EPOCH).days, (date(2024, 1, 1) - EPOCH).days
HO_TO = (date(2027, 1, 1) - EPOCH).days
OUT_DIR = DATA_DIR / "ll"
DGS10 = DATA_DIR / "raw" / "DGS10.csv"


def to_date(d: int) -> date:
    return date.fromordinal(EPOCH.toordinal() + int(d))


def tval(x: np.ndarray) -> float:
    return float(x.mean() / (x.std(ddof=1) / np.sqrt(len(x)))) if len(x) > 2 else np.nan


def load_all() -> dict:
    jpy = load_bars("USDJPY", "M5")
    return {"aud": load_bars("AUDJPY", "H1"), "spx": load_bars("SPXUSD", "H1"), "usdjpy_px": daily_prices(jpy),
            "dgs10": load_dgs10(DGS10), "rates": RateTable.load()}


def daily_series(variant: str, data: dict, lo: int, hi: int) -> tuple[np.ndarray, np.ndarray, np.ndarray, dict]:
    """(weekdays, net bp, cost bp, extras) over [lo, hi)."""
    days = np.arange(lo, hi)
    days = days[(days + 3) % 7 < 5]
    if variant == "LL-AJ":
        tr = run_aj(data["aud"], data["spx"], Costs("fx", "AUDJPY"), data["rates"], lo, hi)
        idx = np.searchsorted(days, np.clip(tr["exit_day"], days[0], days[-1]))
        net, cost = (np.bincount(idx, tr[k], len(days)) for k in ("net_bp", "cost_bp"))
        ex = {"trades": len(tr), "R_net": float(tr["r_net"].mean()),
              "R_gross": float(np.mean(tr["gross_bp"] / (tr["notional"] * tr["r_bp"])))}
        return days, net, cost, ex
    px = data["usdjpy_px"]
    cut = px["day"] < hi
    px = {k: v[cut] for k, v in px.items()}
    rows = run_yield(variant, px, *data["dgs10"], data["rates"])
    rows = rows[(rows["day"] >= lo) & (rows["day"] < hi)]
    idx = np.searchsorted(days, rows["day"])
    keep = (idx < len(days)) & (days[np.clip(idx, 0, len(days) - 1)] == rows["day"])
    net = np.bincount(idx[keep], rows["net"][keep] * 1e4, len(days))
    cost = np.bincount(idx[keep], rows["cost"][keep] * 1e4, len(days))
    w = rows["w"]
    ex = {"trades": int((np.abs(np.diff(np.r_[0.0, w])) > 0).sum()), "exposure": float(np.abs(w).mean()),
          "pnl": float(rows["pnl"].sum() * 1e4 / len(days)), "swap": float(rows["swap"].sum() * 1e4 / len(days))}
    return days, net, cost, ex


def stats(days, net, cost, ex, years) -> dict:
    yr = np.array([to_date(d).year for d in days])
    month = np.array([to_date(d).year * 12 + to_date(d).month for d in days])
    m = {"n": len(net), "E": float(net.mean()), "sd": float(net.std(ddof=1)), "cost": float(cost.mean()),
         "E_2x": float((net - cost).mean()), "t_iid": tval(net), "t_week": cluster_t(net, (days + 3) // 7),
         "t_month": cluster_t(net, month), **ex}
    m["t"] = min(m["t_iid"], m["t_week"], m["t_month"])
    nyears = max(1, len(set(yr.tolist())))
    m["ann"] = m["E"] * len(net) / nyears / 100
    m["sharpe"] = m["E"] / m["sd"] * np.sqrt(len(net) / nyears) if m["sd"] > 0 else np.nan
    m["by_year"] = {y: float(net[yr == y].sum()) / 100 for y in years}
    m["years_pos"] = sum(1 for s in m["by_year"].values() if s > 0)
    m["halves"] = (float(net[yr <= 2019].mean()) if (yr <= 2019).any() else np.nan,
                   float(net[yr >= 2020].mean()) if (yr >= 2020).any() else np.nan)
    m["net_arr"], m["month_arr"] = net, month
    return m


def checks_is(m: dict, years) -> list:
    a, b = m["halves"]
    return [("Mittleres Netto-Tagesergebnis > 0 mit t ≥ 3,0 (kleinster aus iid / Woche / Monat)",
             f"{m['E']:+.2f} bp/Tag, t = {m['t']:.2f}", m["E"] > 0 and m["t"] >= 3.0),
            (f"≥ 6 von {len(years)} Jahren positiv", f"{m['years_pos']} von {len(years)}", m["years_pos"] >= 6),
            ("beide Teilzeiträume 2015–2019 und 2020–2023 positiv", f"{a:+.2f} / {b:+.2f} bp", a > 0 and b > 0),
            ("bei doppelten Kosten > 0", f"{m['E_2x']:+.2f} bp/Tag", m["E_2x"] > 0)]


def variant_lines(name: str, m: dict, checks: list) -> list[str]:
    passed = all(ok for _, _, ok in checks)
    out = [f"## {name}\n", "| Kennzahl | Wert |", "|---|---|",
           f"| Werktage / Trades bzw. Positionswechsel | {m['n']:,} / {m['trades']:,} |",
           f"| Netto je Tag (bp des Kapitals) | {m['E']:+.2f} bp (σ {m['sd']:.1f} bp) |",
           f"| Kosten je Tag | {m['cost']:.2f} bp |",
           f"| Rendite p. a. (netto) | {m['ann']:+.2f} % |",
           f"| Sharpe Ratio p. a. (netto) | {m['sharpe']:.2f} |",
           f"| t-Wert iid / Woche / Monat | {m['t_iid']:.2f} / {m['t_week']:.2f} / {m['t_month']:.2f} |"]
    if "R_net" in m:
        out.append(f"| Ø R je Trade vor / nach Kosten | {m['R_gross']:+.3f} / {m['R_net']:+.3f} |")
    else:
        out.append(f"| Kurs-Ergebnis / Swap je Tag | {m['pnl']:+.2f} / {m['swap']:+.2f} bp (Ø Gewicht {m['exposure']:.2f}) |")
    out += [f"| bei doppelten Kosten | {m['E_2x']:+.2f} bp/Tag |", "",
            "| Kriterium | Ergebnis | erfüllt |", "|---|---|---|"]
    out += [f"| {c} | {v} | {'ja' if ok else '**nein**'} |" for c, v, ok in checks]
    out += ["", f"**{name}: {'alle Kriterien erfüllt' if passed else 'nicht bestanden'}.**\n",
            "| Jahr | Netto % |", "|---|---|"]
    out += [f"| {y} | {s:+.2f} |" for y, s in m["by_year"].items()]
    return out + [""]


def descriptive(data: dict) -> list[str]:
    aud = data["aud"][(data["aud"]["ts"] >= IS_FROM * 86400) & (data["aud"]["ts"] < IS_TO * 86400)]
    spx = data["spx"][data["spx"]["ts"] < IS_TO * 86400]
    sig, _, _ = aj_signals(aud, spx)
    fwd = np.full(len(aud), np.nan)
    fwd[:-4] = np.log(aud["o"][4:] / aud["o"][1:-3]) * 1e4             # open i+1 -> open i+4
    out = ["## Beschreibend\n", "| AUDJPY Open i+1 → Open i+4 (bp, vor Kosten) | Anzahl | Ø | t |", "|---|---|---|---|"]
    for lbl, sel in ((f"nach US500 z > {Z_K}", sig == 1), (f"nach US500 z < −{Z_K}", sig == -1), ("alle Stunden", sig != 9)):
        x = fwd[sel & np.isfinite(fwd)]
        out.append(f"| {lbl} | {len(x):,} | {x.mean():+.2f} | {tval(x):+.2f} |")
    px = data["usdjpy_px"]
    sel = (px["day"] >= IS_FROM) & (px["day"] < IS_TO)
    d, p = px["day"][sel], px["p_mark"][sel]
    r = np.diff(np.log(p)) * 1e4
    y_days, y = data["dgs10"]
    k = np.searchsorted(y_days, d, side="right") - 1                   # yield of the same calendar day or before
    dy = np.diff(y[k]) * 100
    out += ["", "| USDJPY-Tagesrendite (Marke) gegen ΔDGS10 (bp) | Korrelation |", "|---|---|",
            f"| gleicher Tag | {np.corrcoef(r, dy)[0, 1]:+.3f} |",
            f"| ΔDGS10 des Vortags → USDJPY heute | {np.corrcoef(r[1:], dy[:-1])[0, 1]:+.3f} |", ""]
    return out


def in_sample():
    data = load_all()
    lines = ["# Modell LL (Lead-Lag), In-Sample 2015–2023 (Trial T210 LL-AJ, T211 LL-Y1, T212 LL-Y20)\n",
             f"Lauf vom {date.today():%d.%m.%Y}. Regeln laut `docs/01_Vorregistrierung.md`, Code `research/ll/`. "
             "LL-AJ: AUDJPY 3 h in Richtung einer US500-H1-Bewegung > 1,5σ (Stop 2 ATR, 0,25 % Risiko); LL-Y1/LL-Y20: "
             "USDJPY in Richtung der Vortagesänderung bzw. 20-Tage-Änderung der 10-jährigen US-Rendite (10 %/σ, "
             "Tagesbuchhaltung Modell G). Netto = nach allen Kosten und Swaps.\n"]
    verdict = {}
    for v in VARIANTS:
        m = stats(*daily_series(v, data, IS_FROM, IS_TO), IS_YEARS)
        checks = checks_is(m, IS_YEARS)
        verdict[v] = all(ok for _, _, ok in checks)
        lines += variant_lines(v, m, checks)
    lines += descriptive(data)
    passed = [v for v, ok in verdict.items() if ok]
    lines.append(f"**Ergebnis:** bestanden: {', '.join(passed)}; Artefakt-Prüfung und Hold-out folgen." if passed else
                 "**Ergebnis: Keine Variante erfüllt alle In-Sample-Kriterien. Strategien Nr. 58 und 59 sind "
                 "gescheitert; der Hold-out bleibt unberührt.**")
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    (RESULTS_DIR / "ll_in_sample.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))


def holdout(variant: str):
    marker = OUT_DIR / "ho" / f"DONE_{variant}"
    if marker.exists():
        sys.exit(f"Hold-out für {variant} wurde bereits ausgewertet ({marker}) – kein zweiter Lauf.")
    data = load_all()
    m_is = stats(*daily_series(variant, data, IS_FROM, IS_TO), IS_YEARS)
    if not all(ok for _, _, ok in checks_is(m_is, IS_YEARS)):
        sys.exit(f"{variant} hat die In-Sample-Kriterien nicht erfüllt – kein Hold-out.")
    marker.parent.mkdir(parents=True, exist_ok=True)
    marker.write_text(f"{variant} {date.today().isoformat()}\n")
    m = stats(*daily_series(variant, data, IS_TO, HO_TO), HO_YEARS)
    lo, hi = cluster_bootstrap_ci(m_is["net_arr"], m_is["month_arr"])
    checks = [("Mittleres Netto-Tagesergebnis > 0", f"{m['E']:+.2f} bp", m["E"] > 0),
              ("≥ untere 95-%-Grenze von In-Sample (Cluster-Bootstrap nach Monat)",
               f"{m['E']:+.2f} vs. IS {m_is['E']:+.2f} [{lo:+.2f}; {hi:+.2f}] bp", m["E"] >= lo)]
    lines = [f"# Modell LL, Hold-out 2024–2026 ({variant})\n",
             f"Einmaliger Lauf vom {date.today():%d.%m.%Y}.\n"] + variant_lines(variant, m, checks)
    (RESULTS_DIR / f"ll_holdout_{variant}.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--holdout", choices=list(VARIANTS))
    args = ap.parse_args()
    if args.holdout:
        holdout(args.holdout)
    else:
        in_sample()


if __name__ == "__main__":
    main()
