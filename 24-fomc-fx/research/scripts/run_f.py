#!/usr/bin/env python3
"""Strategy no. 24, model F (USD on FOMC days): in-sample runs T84 (F-USD) and T85 (F-CARRY) with the
pre-registered acceptance check and descriptive tables, and - only for a variant that passed - the one-time
hold-out run T86 (docs/01_Vorregistrierung.md).

Usage:
  ../smart-money-concept/research/.venv/bin/python -I research/scripts/run_f.py                 # T84 + T85
  ../smart-money-concept/research/.venv/bin/python -I research/scripts/run_f.py --holdout F-USD  # T86, once
"""
import argparse
import sys
from datetime import date
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from ffx import DATA_DIR, RESULTS_DIR  # noqa: E402
from ffx.model import VARIANTS, per_event, run_model_f, short_usd_sign  # noqa: E402
from carry.model import USD_PAIRS, ewma_sigma  # noqa: E402
from fomc.model import EPOCH, load_dates  # noqa: E402
from smc.data.bars import load_bars  # noqa: E402
from smc.report import cluster_bootstrap_ci, cluster_t  # noqa: E402
from smc.strategy_g import VOL_TARGET, daily_prices  # noqa: E402
from smc.swaps import RateTable  # noqa: E402

IS_YEARS, HO_YEARS = range(2015, 2024), range(2024, 2027)
OUT_DIR = DATA_DIR / "f"


def to_date(d: int) -> date:
    return date.fromordinal(EPOCH.toordinal() + int(d))


def tval(x):
    return float(x.mean() / (x.std(ddof=1) / np.sqrt(len(x)))) if len(x) > 2 else np.nan


def prices(day_to: int | None) -> dict:
    out = {}
    for sym in USD_PAIRS.values():
        px = daily_prices(load_bars(sym, "M5"))
        if day_to is not None:
            px = {k: v[px["day"] < day_to] for k, v in px.items()}
        out[sym] = px
    return out


def stats(days, net, cost, years) -> dict:
    x, c = net * 1e4, cost * 1e4
    yr = np.array([to_date(d).year for d in days])
    q = yr * 4 + (np.array([to_date(d).month for d in days]) - 1) // 3
    m = {"n": len(x), "E": float(x.mean()), "sd": float(x.std(ddof=1)), "cost": float(c.mean()),
         "E_2x": float((x - c).mean()), "t_iid": tval(x), "t_q": cluster_t(x, q), "hit": float((x > 0).mean())}
    m["t"] = min(m["t_iid"], m["t_q"])
    m["sharpe"] = m["E"] / m["sd"] * np.sqrt(len(x) / max(1, len(set(yr.tolist()))))
    m["by_year"] = {y: (int((yr == y).sum()), float(x[yr == y].sum())) for y in years}
    m["years_pos"] = sum(1 for k, s in m["by_year"].values() if k and s > 0)
    m["halves"] = (float(x[yr <= 2019].mean()) if (yr <= 2019).any() else np.nan,
                   float(x[yr >= 2020].mean()) if (yr >= 2020).any() else np.nan)
    m["x"], m["days"] = x, days
    return m


def checks_is(m, years) -> list:
    a, b = m["halves"]
    return [("Mittleres Netto-Ergebnis je Termin > 0 mit t ≥ 3,0 (kleinster aus iid / Quartal)",
             f"{m['E']:+.1f} bp/Termin, t = {m['t']:.2f}", m["E"] > 0 and m["t"] >= 3.0),
            (f"≥ 6 von {len(years)} Jahren positiv", f"{m['years_pos']} von {len(years)}", m["years_pos"] >= 6),
            ("beide Teilzeiträume 2015–2019 und 2020–2023 positiv", f"{a:+.1f} / {b:+.1f} bp", a > 0 and b > 0),
            ("bei doppelten Kosten > 0", f"{m['E_2x']:+.1f} bp/Termin", m["E_2x"] > 0)]


def variant_lines(name, m, checks) -> list[str]:
    ok = all(c for _, _, c in checks)
    out = [f"## {name}\n", "| Kennzahl | Wert |", "|---|---|", f"| Termine | {m['n']} |",
           f"| Netto je Termin (bp des Kapitals) | {m['E']:+.1f} bp (σ {m['sd']:.1f} bp) |",
           f"| Kosten je Termin | {m['cost']:.1f} bp |", f"| Sharpe Ratio p. a. (8 Termine) | {m['sharpe']:.2f} |",
           f"| t-Wert iid / Quartal | {m['t_iid']:.2f} / {m['t_q']:.2f} |", f"| Anteil positiver Termine | {m['hit']:.0%} |",
           f"| bei doppelten Kosten | {m['E_2x']:+.1f} bp/Termin |", "", "| Kriterium | Ergebnis | erfüllt |", "|---|---|---|"]
    out += [f"| {c} | {v} | {'ja' if k else '**nein**'} |" for c, v, k in checks]
    out += ["", f"**{name}: {'alle Kriterien erfüllt' if ok else 'nicht bestanden'}.**\n",
            "| Jahr | Termine | Netto Summe bp |", "|---|---|---|"]
    out += [f"| {y} | {k} | {s:+.1f} |" for y, (k, s) in m["by_year"].items()]
    return out + [""]


def control(pxs: dict, fomc: set, years) -> list[str]:
    """Short-USD basket (all 7, 10 % / sigma) from 16:50 to 16:50, before costs: FOMC days vs all other days."""
    by_day: dict[int, float] = {}
    for sym, px in pxs.items():
        sig = ewma_sigma(np.r_[np.nan, np.diff(np.log(px["p_mark"]))])
        r = np.r_[np.nan, px["p_mark"][1:] / px["p_mark"][:-1] - 1]
        w = short_usd_sign(sym) * VOL_TARGET / np.r_[np.nan, sig[:-1]]
        for d, x in zip(px["day"].tolist(), (w * r).tolist()):
            if np.isfinite(x) and to_date(d).year in years:
                by_day[d] = by_day.get(d, 0.0) + x
    f = np.array([v for d, v in by_day.items() if d in fomc]) * 1e4
    o = np.array([v for d, v in by_day.items() if d not in fomc]) * 1e4
    t_diff = (f.mean() - o.mean()) / np.sqrt(f.var(ddof=1) / len(f) + o.var(ddof=1) / len(o))
    return ["### Vergleich (beschreibend, vor Kosten): Short-USD-Korb über den FX-Tag\n",
            "| Tage | Anzahl | Ø bp | t |", "|---|---|---|---|",
            f"| FOMC-Tage | {len(f)} | {f.mean():+.1f} | {tval(f):+.2f} |",
            f"| übrige Tage | {len(o)} | {o.mean():+.1f} | {tval(o):+.2f} |",
            f"| **Differenz** | | **{f.mean() - o.mean():+.1f}** | **{t_diff:+.2f}** |", ""]


def in_sample():
    rates = RateTable.load()
    is_to = (date(2024, 1, 1) - EPOCH).days
    pxs = prices(is_to)
    ev = load_dates()
    ev = ev[[to_date(d).year in IS_YEARS for d in ev]]
    lines = ["# Modell F (USD an FOMC-Tagen), In-Sample 2015–2023 (Trial T84 F-USD, T85 F-CARRY)\n",
             f"Lauf vom {date.today():%d.%m.%Y}. Regeln laut `docs/01_Vorregistrierung.md`, Code `research/ffx/`. "
             f"{len(ev)} FOMC-Termine; Short USD 16:50 New York am Vortag bis 16:50 am Entscheidungstag, je Paar "
             "10 % / σ. Netto = nach Spread, Slippage, Kommission, Swap und Gebühr; Ergebnisse in bp des Kapitals.\n"]
    verdict = {}
    for v in VARIANTS:
        rows, log = run_model_f(v, pxs, ev, rates)
        m = stats(*per_event(rows, log), IS_YEARS)
        checks = checks_is(m, IS_YEARS)
        verdict[v] = (m, all(c for _, _, c in checks))
        lines += variant_lines(v, m, checks)
    lines += control(pxs, set(ev.tolist()), IS_YEARS)
    passed = [v for v, (_, ok) in verdict.items() if ok]
    if passed:
        best = max(passed, key=lambda v: verdict[v][0]["t"])
        lines.append(f"**Ergebnis:** bestanden: {', '.join(passed)}; gewählt für den Hold-out: **{best}**.")
    else:
        lines.append("**Ergebnis: Keine Variante erfüllt alle In-Sample-Kriterien. Strategie Nr. 24 ist gescheitert; "
                     "der Hold-out bleibt unberührt.**")
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    (RESULTS_DIR / "f_in_sample.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))


def holdout(variant: str):
    marker = OUT_DIR / "ho" / "DONE"
    if marker.exists():
        sys.exit("Hold-out wurde bereits ausgewertet (data/f/ho/DONE) – kein zweiter Lauf.")
    rates = RateTable.load()
    is_to = (date(2024, 1, 1) - EPOCH).days
    ev = load_dates()
    ev_is = ev[[to_date(d).year in IS_YEARS for d in ev]]
    m_is = stats(*per_event(*run_model_f(variant, prices(is_to), ev_is, rates)), IS_YEARS)
    if not all(c for _, _, c in checks_is(m_is, IS_YEARS)):
        sys.exit(f"{variant} hat die In-Sample-Kriterien nicht erfüllt – kein Hold-out.")
    marker.parent.mkdir(parents=True, exist_ok=True)
    marker.write_text(f"T86 {variant} {date.today().isoformat()}\n")
    ev_ho = ev[[to_date(d).year >= 2024 for d in ev]]
    m = stats(*per_event(*run_model_f(variant, prices(None), ev_ho, rates)), HO_YEARS)
    lo, hi = cluster_bootstrap_ci(m_is["x"], m_is["days"])
    checks = [("Mittleres Netto-Ergebnis je Termin > 0", f"{m['E']:+.1f} bp", m["E"] > 0),
              ("≥ untere 95-%-Grenze von In-Sample", f"{m['E']:+.1f} vs. IS {m_is['E']:+.1f} [{lo:+.1f}; {hi:+.1f}] bp",
               m["E"] >= lo)]
    lines = [f"# Modell F, Hold-out 2024–2026 (Trial T86, {variant})\n", f"Einmaliger Lauf vom {date.today():%d.%m.%Y}.\n"]
    lines += variant_lines(variant, m, checks)
    (RESULTS_DIR / "f_holdout.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
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
