#!/usr/bin/env python3
"""Strategy no. 5, model M (month-end rebalancing at the London fix): in-sample runs T19 (M-1H) and
T20 (M-DAY) with the pre-registered acceptance check and descriptive tables, and - only for a variant
that passed - the one-time hold-out run T21 (docs/01_Vorregistrierung.md).

Usage:
  ../smart-money-concept/research/.venv/bin/python -I research/scripts/run_m.py                  # T19 + T20
  ../smart-money-concept/research/.venv/bin/python -I research/scripts/run_m.py --holdout M-1H   # T21, once
"""
import argparse
import sys
from datetime import date
from pathlib import Path

import numpy as np
import pyarrow as pa
import pyarrow.parquet as pq

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from mer import DATA_DIR, RESULTS_DIR, events  # noqa: E402
from mer.model import PAIRS, ROW_DTYPE, US_INDEX, VARIANTS, Market, run_model_m, run_reversal  # noqa: E402
from smc.data.bars import load_bars  # noqa: E402
from smc.report import cluster_bootstrap_ci, cluster_t  # noqa: E402

IS_YEARS, HO_YEARS = range(2015, 2024), range(2024, 2027)
OUT_DIR = DATA_DIR / "m"
PHASES = {"is": ((2014, 1), (2023, 12)), "ho": ((2023, 12), (2026, 12))}


def year_of(days: np.ndarray) -> np.ndarray:
    return np.array([events.to_date(d).year for d in days])


def month_of(days: np.ndarray) -> np.ndarray:
    return np.array([events.to_date(d).month for d in days])


def run(phase: str, variants) -> dict:
    days = events.event_days(*PHASES[phase])
    us = load_bars(US_INDEX, "M5")
    out = {}
    for v in variants:
        parts, rev = [], []
        for sym, idx in PAIRS.items():
            mk, fo = Market(sym, load_bars(sym, "M5"), load_bars(sym, "H1")), load_bars(idx, "M5")
            parts.append(run_model_m(sym, mk, us, fo, days, v))
            rev.append(run_reversal(sym, mk, us, fo, days, v))
            print(f"{v} {sym}: {len(parts[-1])} Ereignisse", flush=True)
        for name, rows in ((v, np.concatenate(parts)), (f"{v}-REV", np.concatenate(rev))):
            (OUT_DIR / phase).mkdir(parents=True, exist_ok=True)
            pq.write_table(pa.table({n: rows[n] for n in rows.dtype.names}), OUT_DIR / phase / f"{name}.parquet",
                           compression="zstd")
            out[name] = rows
    return out


def subset(rows: np.ndarray, years) -> np.ndarray:
    return rows[np.isin(year_of(rows["event_day"]), list(years))]


def per_event(rows: np.ndarray, col: str = "net_bp", w: np.ndarray | None = None) -> tuple[np.ndarray, np.ndarray]:
    days, inv = np.unique(rows["event_day"], return_inverse=True)
    x = rows[col] if w is None else rows[col] * w
    return days, np.bincount(inv, x)


def tval(x: np.ndarray) -> float:
    return float(x.mean() / (x.std(ddof=1) / np.sqrt(len(x)))) if len(x) > 2 else np.nan


def stats(rows: np.ndarray, years) -> dict:
    days, net = per_event(rows)
    _, cost = per_event(rows, "cost_bp")
    _, gross = per_event(rows, "gross_bp")
    yr = year_of(days)
    quarter = yr * 4 + (month_of(days) - 1) // 3
    m = {"events": len(days), "positions": len(rows), "E": float(net.mean()), "sd": float(net.std(ddof=1)),
         "gross": float(gross.mean()), "cost": float(cost.mean()), "E_2x": float((net - cost).mean()),
         "t_iid": tval(net), "t_q": cluster_t(net, quarter)}
    m["t"] = min(m["t_iid"], m["t_q"])
    m["sharpe"] = m["E"] / m["sd"] * np.sqrt(len(days) / max(1, len(set(yr.tolist()))))
    m["hit"] = float((net > 0).mean())
    m["by_year"] = {y: (int((yr == y).sum()), float(net[yr == y].sum())) for y in years}
    m["years_pos"] = sum(1 for k, tot in m["by_year"].values() if k and tot > 0)
    m["by_pair"] = {s: float(rows["net_bp"][rows["symbol"] == s].sum()) for s in PAIRS if (rows["symbol"] == s).any()}
    m["pairs_pos"] = sum(1 for v in m["by_pair"].values() if v > 0)
    m["days_arr"], m["net_arr"] = days, net
    return m


def checks_is(m: dict, years) -> list:
    return [("Mittleres Netto-Ereignisergebnis > 0 mit t ≥ 3,0 (kleinster aus iid / Quartal)",
             f"{m['E']:+.2f} bp/Ereignis, t = {m['t']:.2f}", m["E"] > 0 and m["t"] >= 3.0),
            (f"≥ 6 von {len(years)} Jahren positiv", f"{m['years_pos']} von {len(years)}", m["years_pos"] >= 6),
            ("≥ 3 von 4 Paaren positiv", f"{m['pairs_pos']} von {len(PAIRS)}", m["pairs_pos"] >= 3),
            ("bei doppelten Kosten > 0", f"{m['E_2x']:+.2f} bp/Ereignis", m["E_2x"] > 0)]


def variant_lines(name: str, m: dict, checks: list) -> list[str]:
    passed = all(ok for _, _, ok in checks)
    out = [f"## {name}\n", "| Kennzahl | Wert |", "|---|---|",
           f"| Ereignisse / Positionen | {m['events']} / {m['positions']} |",
           f"| Netto je Ereignis | {m['E']:+.2f} bp (σ {m['sd']:.1f} bp) |",
           f"| vor Kosten je Ereignis | {m['gross']:+.2f} bp |",
           f"| Kosten je Ereignis | {m['cost']:.2f} bp |",
           f"| Sharpe Ratio p. a. (netto) | {m['sharpe']:.2f} |",
           f"| t-Wert iid / Quartal | {m['t_iid']:.2f} / {m['t_q']:.2f} |",
           f"| Anteil positiver Ereignisse | {m['hit']:.0%} |",
           f"| bei doppelten Kosten | {m['E_2x']:+.2f} bp/Ereignis |", "",
           "| Kriterium | Ergebnis | erfüllt |", "|---|---|---|"]
    out += [f"| {c} | {v} | {'ja' if ok else '**nein**'} |" for c, v, ok in checks]
    out += ["", f"**{name}: {'alle Kriterien erfüllt' if passed else 'nicht bestanden'}.**\n",
            "| Jahr | Ereignisse | Netto Summe bp |", "|---|---|---|"]
    out += [f"| {y} | {k} | {tot:+.1f} |" for y, (k, tot) in m["by_year"].items()]
    return out + [""]


def pair_table(rows: np.ndarray) -> list[str]:
    out = ["| Paar | Positionen | netto Ø bp | vor Kosten Ø bp | Kosten Ø bp | t (netto) | Treffer | Stops |",
           "|---|---|---|---|---|---|---|---|"]
    for s in PAIRS:
        r = rows[rows["symbol"] == s]
        if not len(r):
            continue
        out.append(f"| {s} | {len(r)} | {r['net_bp'].mean():+.2f} | {r['gross_bp'].mean():+.2f} | "
                   f"{r['cost_bp'].mean():.2f} | {tval(r['net_bp']):+.2f} | {(r['net_bp'] > 0).mean():.0%} | "
                   f"{r['stopped'].mean():.0%} |")
    return out + [""]


def regression(rows: np.ndarray) -> tuple[float, float, float]:
    """OLS slope of the foreign currency's window return (bp) on R_foreign - R_US (%), event-clustered t."""
    x, y = rows["rel_eq_pct"], rows["ccy_ret_bp"]
    xc = x - x.mean()
    b = float((xc * (y - y.mean())).sum() / (xc ** 2).sum())
    u = y - y.mean() - b * xc
    _, inv = np.unique(rows["event_day"], return_inverse=True)
    g = np.bincount(inv, xc * u)
    se = np.sqrt(len(g) / (len(g) - 1) * (g ** 2).sum()) / (xc ** 2).sum()
    r2 = 1 - (u ** 2).sum() / ((y - y.mean()) ** 2).sum()
    return b, b / se, float(r2)


def descriptive(rows: np.ndarray, rev: np.ndarray, pre: np.ndarray) -> list[str]:
    out = ["### Je Paar\n"] + pair_table(rows)
    b, t, r2 = regression(rows)
    out += ["### Regression wie im Paper\n",
            "Fensterrendite der Fremdwährung gegen USD (bp) auf `R_fremd − R_US` (%), alle Paare gepoolt, "
            "t-Wert mit Clustern nach Ereignis. Paper (2004–2012, 15–16 Uhr): Steigung ≈ −1,4.\n",
            "| Steigung bp je % | t-Wert | R² |", "|---|---|---|", f"| {b:+.2f} | {t:+.2f} | {r2:.3f} |", ""]
    w = np.empty(len(rows))
    for s in PAIRS:
        k = rows["symbol"] == s
        w[k] = np.abs(rows["x"][k]) / np.abs(rows["x"][k]).mean()
    _, lin = per_event(rows, w=w)
    days, net = per_event(rows)
    q = np.isin(month_of(days), (3, 6, 9, 12))
    out += ["### Varianten der Auswertung\n", "| Auswertung | Ereignisse | netto Ø bp | t-Wert |", "|---|---|---|---|",
            f"| Vorzeichen (vorregistriert) | {len(net)} | {net.mean():+.2f} | {tval(net):+.2f} |",
            f"| gewichtet mit \\|x\\| | {len(lin)} | {lin.mean():+.2f} | {tval(lin):+.2f} |",
            f"| nur Quartalsenden | {q.sum()} | {net[q].mean():+.2f} | {tval(net[q]):+.2f} |",
            f"| übrige Monate | {(~q).sum()} | {net[~q].mean():+.2f} | {tval(net[~q]):+.2f} |"]
    if len(pre):
        _, p = per_event(pre)
        _, pg = per_event(pre, "gross_bp")
        out.append(f"| 2014 (vor der Fix-Reform; vor Kosten {pg.mean():+.2f}) | {len(p)} | {p.mean():+.2f} | "
                   f"{tval(p):+.2f} |")
    _, rn = per_event(rev)
    _, rg = per_event(rev, "gross_bp")
    out += ["", "### Umkehr nach dem Fix (Gegenposition 16:05 bis 12:00 am nächsten Geschäftstag, ohne Swaps)\n",
            f"Je Ereignis: netto {rn.mean():+.2f} bp, vor Kosten {rg.mean():+.2f} bp, t (netto) {tval(rn):+.2f}.\n"]
    out += pair_table(rev)
    return out


def load(phase: str, name: str) -> np.ndarray:
    t = pq.read_table(OUT_DIR / phase / f"{name}.parquet")
    rows = np.empty(t.num_rows, ROW_DTYPE)
    for n in ROW_DTYPE.names:
        rows[n] = t.column(n).to_numpy(zero_copy_only=False)
    return rows


def in_sample():
    res = run("is", list(VARIANTS))
    lines = ["# Modell M (Monatsend-Rebalancing), In-Sample 2015–2023 (Trial T19 M-1H, T20 M-DAY)\n",
             f"Lauf vom {date.today():%d.%m.%Y}. Regeln laut `docs/01_Vorregistrierung.md`, Code `research/mer/`. "
             "Letzter Londoner Geschäftstag je Monat, HistData-M5 (Bid). Netto = nach Spread, Kommission, Slippage "
             "(0,1 Pip Einstieg, 0,5 Pip Ausstieg am Fix) und 0,7-%-Gebühr bei USDJPY; je Position gleicher "
             "Nominalwert, Ergebnisse in Basispunkten.\n"]
    verdict = {}
    for v in VARIANTS:
        rows = subset(res[v], IS_YEARS)
        m = stats(rows, IS_YEARS)
        checks = checks_is(m, IS_YEARS)
        verdict[v] = (m, all(ok for _, _, ok in checks))
        lines += variant_lines(v, m, checks)
        lines += descriptive(rows, subset(res[f"{v}-REV"], IS_YEARS), subset(res[v], [2014]))
    passed = [v for v, (_, ok) in verdict.items() if ok]
    if passed:
        best = max(passed, key=lambda v: verdict[v][0]["t"])
        lines.append(f"**Ergebnis:** bestanden: {', '.join(passed)}; gewählt für den Hold-out: **{best}**.")
    else:
        lines.append("**Ergebnis: Keine Variante erfüllt alle In-Sample-Kriterien. Strategie Nr. 5 ist "
                     "gescheitert; der Hold-out bleibt unberührt.**")
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    (RESULTS_DIR / "m_in_sample.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))


def holdout(variant: str):
    marker = OUT_DIR / "ho" / "DONE"
    if marker.exists():
        sys.exit("Hold-out wurde bereits ausgewertet (data/m/ho/DONE) – kein zweiter Lauf.")
    m_is = stats(subset(load("is", variant), IS_YEARS), IS_YEARS)
    if not all(ok for _, _, ok in checks_is(m_is, IS_YEARS)):
        sys.exit(f"{variant} hat die In-Sample-Kriterien nicht erfüllt – kein Hold-out.")
    marker.parent.mkdir(parents=True, exist_ok=True)
    marker.write_text(f"T21 {variant} {date.today().isoformat()}\n")
    rows = subset(run("ho", [variant])[variant], HO_YEARS)
    m = stats(rows, HO_YEARS)
    lo, hi = cluster_bootstrap_ci(m_is["net_arr"], m_is["days_arr"])
    checks = [("Mittleres Netto-Ereignisergebnis > 0", f"{m['E']:+.2f} bp/Ereignis", m["E"] > 0),
              ("≥ untere 95-%-Grenze von In-Sample (Bootstrap über Ereignisse)",
               f"{m['E']:+.2f} vs. IS {m_is['E']:+.2f} [{lo:+.2f}; {hi:+.2f}] bp/Ereignis", m["E"] >= lo)]
    lines = [f"# Modell M, Hold-out 2024–2026 (Trial T21, {variant})\n",
             f"Einmaliger Lauf vom {date.today():%d.%m.%Y}.\n"] + variant_lines(variant, m, checks) + pair_table(rows)
    (RESULTS_DIR / "m_holdout.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
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
