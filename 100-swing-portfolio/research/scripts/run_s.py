#!/usr/bin/env python3
"""Strategy no. 100 (swing portfolio): descriptive in-sample run T306 and - once - the hold-out T307 with the
FTMO bootstrap T308 (docs/01_Vorregistrierung.md).

Usage:
  ../../smart-money-concept/research/.venv/bin/python -I scripts/run_s.py              # T306
  ../../smart-money-concept/research/.venv/bin/python -I scripts/run_s.py --holdout    # T307 + T308, once
"""
import argparse
import sys
from datetime import date
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from swp import DATA_DIR, PROJECT_ROOT, RESULTS_DIR  # noqa: E402
from swp.components import HO_TO, IS_FROM, IS_TO, load  # noqa: E402
from swp.portfolio import (ANNUAL, LEVELS, MAX_US500_NOTIONAL, align, bootstrap, historical,  # noqa: E402
                           inverse_vol_weights, month_of)
from smc.report import cluster_bootstrap_ci, cluster_t  # noqa: E402

MARKER = DATA_DIR / "ho" / "DONE"
COMPONENT_MARKERS = {"09-pre-fomc-drift": "p", "10-turn-of-the-month": "t", "14-vol-managed-index": "v",
                     "24-fomc-fx": "f"}


def year_of(days):
    return np.asarray(days * 86400, dtype="datetime64[s]").astype("datetime64[Y]").astype(int) + 1970


def book(a: dict, g: np.ndarray) -> dict:
    return {"days": a["days"], "r": a["net"] @ g, "w": a["worst"] @ g, "c": a["cost"] @ g,
            "act": a["active"].any(axis=1)}


def us500(expo: dict, g: dict, days: np.ndarray) -> np.ndarray:
    return np.array([sum(g[c] * abs(expo[c].get(int(d), 0.0)) for c in expo) for d in days])


def stats(x: np.ndarray, cost: np.ndarray, days: np.ndarray) -> dict:
    n, sd = len(x), x.std(ddof=1)
    yr = year_of(days)
    by_year = {int(y): float(x[yr == y].sum()) for y in np.unique(yr)}
    m = {"n": n, "E": float(x.mean()), "sd": float(sd), "sharpe": float(x.mean() / sd * np.sqrt(ANNUAL)),
         "t_iid": float(x.mean() / (sd / np.sqrt(n))), "t_week": cluster_t(x, (days + 3) // 7),
         "t_month": cluster_t(x, month_of(days)), "E_2x": float((x - cost).mean()), "by_year": by_year,
         "years_pos": sum(v > 0 for v in by_year.values()), "ann": float(x.mean() * ANNUAL)}
    m["t"] = min(m["t_iid"], m["t_week"], m["t_month"])
    return m


def stat_lines(m: dict) -> list[str]:
    return ["| Kennzahl | Wert |", "|---|---|", f"| Handelstage | {m['n']:,} |",
            f"| Netto je Tag | {m['E'] * 1e4:+.2f} bp (σ {m['sd'] * 1e4:.1f} bp) |",
            f"| Rendite p. a. (Summe, unskaliert) | {m['ann']:+.1%} |", f"| Sharpe Ratio p. a. | {m['sharpe']:.2f} |",
            f"| t-Wert iid / Woche / Monat | {m['t_iid']:.2f} / {m['t_week']:.2f} / {m['t_month']:.2f} |",
            f"| Jahre positiv | {m['years_pos']} von {len(m['by_year'])} |",
            f"| bei doppelten Kosten | {m['E_2x'] * 1e4:+.2f} bp/Tag |", ""]


def component_lines(a: dict, g: np.ndarray, title: str) -> list[str]:
    out = [f"### {title}\n", "| Baustein | Gewicht g | Buchungstage | Summe netto p. a. (nativ) | Sharpe p. a. | "
           "Beitrag p. a. (gewichtet) |", "|---|---|---|---|---|---|"]
    years = len(a["days"]) / ANNUAL
    for j, c in enumerate(a["names"]):
        x = a["net"][:, j]
        sh = x.mean() / x.std(ddof=1) * np.sqrt(ANNUAL) if x.std() > 0 else np.nan
        out.append(f"| {c} | {g[j]:.2f} | {int((x != 0).sum())} | {x.sum() / years:+.2%} | {sh:.2f} | "
                   f"{g[j] * x.sum() / years:+.2%} |")
    return out + [""]


def corr_lines(a: dict) -> list[str]:
    c = np.corrcoef(a["net"].T)
    out = ["### Korrelation der Tagesreihen\n", "| | " + " | ".join(a["names"]) + " |",
           "|---|" + "---|" * len(a["names"])]
    out += [f"| {n} | " + " | ".join(f"{v:+.2f}" for v in c[i]) + " |" for i, n in enumerate(a["names"])]
    return out + [""]


def ftmo_lines(b: dict, sd_is: float, lev: np.ndarray, title: str, hist: bool = True) -> tuple[list[str], bool]:
    out = [f"### {title}\n", "| Tagesschwankung | Skalierung k | max. US500-Nominal | P(Phase 1) | P(Phase 2) | "
           "P(beide) | Median-Dauer (Monate) | historische Starts bestanden | Stufe erfüllt |",
           "|---|---|---|---|---|---|---|---|---|"]
    ok_any = False
    for s in LEVELS:
        k = s / sd_is
        lev_ok = lev.max() * k <= MAX_US500_NOTIONAL
        bs = bootstrap(b["r"], b["w"], b["act"], b["days"], k)
        h = historical(b["r"], b["w"], b["act"], b["days"], k) if hist else None
        ok = lev_ok and bs["both"] >= 0.70 and bs["median_months"] <= 12
        ok_any |= ok
        hs = f"{h['passed']} von {h['resolved']} (Median {h['median_months']:.1f} M.)" if h else "–"
        out.append(f"| {s:.2%} | {k:.2f} | {lev.max() * k:.1f}× | {bs['p1']:.0%} | {bs['p2']:.0%} | "
                   f"**{bs['both']:.0%}** | {bs['median_months']:.1f} | {hs} | {'ja' if ok else 'nein'} |")
    return out + [""], ok_any


def year_lines(m: dict) -> list[str]:
    return ["| Jahr | Netto (Summe, unskaliert) |", "|---|---|"] + \
        [f"| {y} | {v:+.2%} |" for y, v in m["by_year"].items()] + [""]


def in_sample_parts():
    series, expo = load("is")
    a = align(series, IS_FROM, IS_TO)
    g = inverse_vol_weights(a["net"])
    b = book(a, g)
    gd = dict(zip(a["names"], g))
    return a, g, b, us500(expo, gd, a["days"]), gd


def in_sample():
    a, g, b, lev, _ = in_sample_parts()
    m = stats(b["r"], b["c"], b["days"])
    lines = ["# Swing-Portfolio (Nr. 100), In-Sample 2015–2023 (Trial T306, beschreibend)\n",
             f"Lauf vom {date.today():%d.%m.%Y}. Regeln laut `docs/01_Vorregistrierung.md`, Code `research/swp/`. "
             "Bausteine unverändert aus Nr. 9, 10, 14 und 24; je Baustein auf 10 % Jahresvola normiert (inverse "
             "Volatilität, nur aus IS). Netto = nach Spread, Slippage, Kommission, Swaps und Gebühren; Tagesrendite "
             "als Anteil des Kapitals vor der FTMO-Skalierung.\n",
             "**Wegen der Auswahl der Bausteine (die besten aus ~130 Versuchen) ist dieses Ergebnis nach oben verzerrt "
             "und nur beschreibend.**\n"]
    lines += component_lines(a, g, "Bausteine") + corr_lines(a) + ["## Portfolio\n"] + stat_lines(m) + year_lines(m)
    ft, _ = ftmo_lines(b, m["sd"], lev, "FTMO-Bootstrap nur auf IS (zur Einordnung, nicht entscheidend)")
    lines += ft
    lines += ["**Artefakt-Prüfung (Spielregel 6):** Keiner der Bausteine handelt zur ersten Feed-Kerze einer Sitzung "
              "(Zeitpunkte 13:55/14:00/15:55/16:50 New York).\n",
              f"**Ergebnis:** IS-Mittel {'> 0 – der Hold-out (T307) läuft wie vorregistriert.' if m['E'] > 0 else '≤ 0 – kein Hold-out.'}"]
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    (RESULTS_DIR / "s_in_sample.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))


def holdout():
    if MARKER.exists():
        sys.exit("Hold-out wurde bereits ausgewertet (data/ho/DONE) – kein zweiter Lauf.")
    a_is, g, b_is, lev_is, gd = in_sample_parts()
    m_is = stats(b_is["r"], b_is["c"], b_is["days"])
    if m_is["E"] <= 0:
        sys.exit("IS-Mittel ≤ 0 – kein Hold-out.")
    stamp = f"T307 Nr. 100 Swing-Portfolio {date.today().isoformat()}\n"
    MARKER.parent.mkdir(parents=True, exist_ok=True)
    MARKER.write_text(stamp)
    for proj, sub in COMPONENT_MARKERS.items():
        mk = PROJECT_ROOT.parent / proj / "data" / sub / "ho" / "DONE"
        mk.parent.mkdir(parents=True, exist_ok=True)
        mk.write_text(f"verbraucht durch {stamp}")

    series, expo = load("ho")
    a = align(series, IS_TO, HO_TO)
    b = book(a, g)
    m = stats(b["r"], b["c"], b["days"])
    lo, hi = cluster_bootstrap_ci(b_is["r"], month_of(b_is["days"]))
    checks = [("Mittleres Netto-Tagesergebnis > 0", f"{m['E'] * 1e4:+.2f} bp/Tag", m["E"] > 0),
              ("≥ untere 95-%-Grenze von IS (Cluster nach Monat)",
               f"{m['E'] * 1e4:+.2f} vs. IS {m_is['E'] * 1e4:+.2f} [{lo * 1e4:+.2f}; {hi * 1e4:+.2f}] bp/Tag",
               m["E"] >= lo)]
    ok = all(k for _, _, k in checks)
    lines = ["# Swing-Portfolio (Nr. 100), Hold-out 01.01.2024–16.10.2026 (Trial T307, T308)\n",
             f"Einmaliger Lauf vom {date.today():%d.%m.%Y}. Gewichte und Skalierung aus IS eingefroren. "
             "Der Hold-out von Nr. 9, 10, 14 und 24 ist damit verbraucht (Marker in deren `data/*/ho/DONE`).\n"]
    lines += component_lines(a, g, "Bausteine im Hold-out") + ["## Portfolio\n"] + stat_lines(m) + year_lines(m)
    lines += ["| Kriterium | Ergebnis | erfüllt |", "|---|---|---|"]
    lines += [f"| {c} | {v} | {'ja' if k else '**nein**'} |" for c, v, k in checks]
    lines += ["", f"**T307: {'bestanden' if ok else 'nicht bestanden'}.**\n"]
    if ok:
        both = {k: np.r_[b_is[k], b[k]] for k in ("r", "w", "c", "act", "days")}
        lev = np.r_[lev_is, us500(expo, gd, a["days"])]
        ft, passed = ftmo_lines(both, m_is["sd"], lev, "FTMO-Block-Bootstrap auf IS + Hold-out (T308)")
        lines += ft + [f"**T308: {'bestanden – Strategie Nr. 100 erfüllt alle Kriterien' if passed else 'nicht bestanden'}.**"]
    else:
        lines.append("**Ergebnis: Strategie Nr. 100 ist im Hold-out gescheitert; kein FTMO-Bootstrap (T308 entfällt).**")
    (RESULTS_DIR / "s_holdout.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--holdout", action="store_true")
    holdout() if ap.parse_args().holdout else in_sample()


if __name__ == "__main__":
    main()
