#!/usr/bin/env python3
"""Strategy no. 32, model A (Asian range fade): in-sample runs T110 (A-EURCHF) and T111 (A-AUDCAD) with the
pre-registered acceptance check and descriptive tables, and - only for a variant that passed - the one-time
hold-out run T112 (docs/01_Vorregistrierung.md).

Usage:
  ../smart-money-concept/research/.venv/bin/python -I research/scripts/run_a.py                     # T110 + T111
  ../smart-money-concept/research/.venv/bin/python -I research/scripts/run_a.py --holdout A-EURCHF  # T112, once
"""
import argparse
import sys
from datetime import date
from pathlib import Path

import numpy as np
import pyarrow as pa
import pyarrow.parquet as pq

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from arf import DATA_DIR, RESULTS_DIR  # noqa: E402
from arf.model import NIGHT_DTYPE as ROW_DTYPE, VARIANTS, run_model_a  # noqa: E402
from mer.events import EPOCH  # noqa: E402
from smc.data.bars import load_bars  # noqa: E402
from smc.report import cluster_bootstrap_ci, cluster_t  # noqa: E402

IS_YEARS, HO_YEARS = range(2015, 2024), range(2024, 2027)
OUT_DIR = DATA_DIR / "a"


def to_date(d: int) -> date:
    return date.fromordinal(EPOCH.toordinal() + int(d))


def tval(x: np.ndarray) -> float:
    return float(x.mean() / (x.std(ddof=1) / np.sqrt(len(x)))) if len(x) > 2 else np.nan





def stats(rows: np.ndarray, years) -> dict:
    net, cost = rows["net_bp"], rows["cost_bp"]
    ds = [to_date(d) for d in rows["day"]]
    yr = np.array([d.year for d in ds])
    month = np.array([d.year * 12 + d.month for d in ds])
    m = {"n": len(net), "E": float(net.mean()), "sd": float(net.std(ddof=1)), "gross": float(rows["gross_bp"].mean()),
         "cost": float(cost.mean()), "E_2x": float((net - cost).mean()), "t_iid": tval(net),
         "t_week": cluster_t(net, (rows["day"] + 3) // 7), "t_month": cluster_t(net, month),
         "hit": float((net > 0).mean()), "stops": int(rows["stopped"].sum())}
    m["t"] = min(m["t_iid"], m["t_week"], m["t_month"])
    m["sharpe"] = m["E"] / m["sd"] * np.sqrt(len(net) / max(1, len(set(yr.tolist()))))
    m["by_year"] = {y: (int((yr == y).sum()), float(net[yr == y].mean()) if (yr == y).any() else np.nan,
                        tval(net[yr == y])) for y in years}
    m["years_pos"] = sum(1 for k, e, _ in m["by_year"].values() if k and e > 0)
    first, second = net[yr <= 2019], net[yr >= 2020]
    m["halves"] = (float(first.mean()) if len(first) else np.nan, float(second.mean()) if len(second) else np.nan)
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
           f"| Nächte | {m['n']:,} |",
           f"| Netto je Tag (bp des Kapitals) | {m['E']:+.2f} bp (σ {m['sd']:.1f} bp) |",
           f"| vor Kosten je Tag | {m['gross']:+.2f} bp |",
           f"| Kosten je Tag | {m['cost']:.2f} bp |",
           f"| Sharpe Ratio p. a. (netto) | {m['sharpe']:.2f} |",
           f"| t-Wert iid / Woche / Monat | {m['t_iid']:.2f} / {m['t_week']:.2f} / {m['t_month']:.2f} |",
           f"| Trefferquote | {m['hit']:.0%} |",
           f"| Nächte mit mindestens einem Stop | {m['stops']} |",
           f"| bei doppelten Kosten | {m['E_2x']:+.2f} bp/Tag |", "",
           "| Kriterium | Ergebnis | erfüllt |", "|---|---|---|"]
    out += [f"| {c} | {v} | {'ja' if ok else '**nein**'} |" for c, v, ok in checks]
    out += ["", f"**{name}: {'alle Kriterien erfüllt' if passed else 'nicht bestanden'}.**\n",
            "| Jahr | Tage | Netto Ø bp | t |", "|---|---|---|---|"]
    out += [f"| {y} | {k} | {e:+.2f} | {t:+.2f} |" for y, (k, e, t) in m["by_year"].items()]
    return out + [""]


def trade_lines(tr: np.ndarray) -> list[str]:
    out = ["### Trades (beschreibend)\n", "| Teilmenge | Trades | Ø R netto | Ø R vor Kosten | Treffer | Stops |", "|---|---|---|---|---|---|"]
    for lbl, sel in (("alle", np.ones(len(tr), bool)), ("Long", tr["dir"] == 1), ("Short", tr["dir"] == -1)):
        x = tr[sel]
        if len(x):
            out.append(f"| {lbl} | {len(x)} | {x['r_net'].mean():+.3f} | {x['r_gross'].mean():+.3f} | "
                       f"{(x['r_net'] > 0).mean():.0%} | {x['stopped'].mean():.0%} |")
    return out + [""]


def save(rows: np.ndarray, phase: str, name: str):
    (OUT_DIR / phase).mkdir(parents=True, exist_ok=True)
    pq.write_table(pa.table({n: rows[n] for n in rows.dtype.names}), OUT_DIR / phase / f"{name}.parquet",
                   compression="zstd")


def load(phase: str, name: str) -> np.ndarray:
    t = pq.read_table(OUT_DIR / phase / f"{name}.parquet")
    rows = np.empty(t.num_rows, ROW_DTYPE)
    for n in ROW_DTYPE.names:
        rows[n] = t.column(n).to_numpy(zero_copy_only=False)
    return rows


def in_sample():
    first, last = date(2015, 1, 1), date(2023, 12, 31)
    lines = ["# Modell A (Asien-Range-Fade), In-Sample 2015–2023 (Trial T110 A-EURCHF, T111 A-AUDCAD)\n",
             f"Lauf vom {date.today():%d.%m.%Y}. Regeln laut `docs/01_Vorregistrierung.md`, Code `research/arf/`. "
             "Fade von M5-Bollinger-Ausschlägen 00:00–06:00 London, Ausstieg an der Mitte, Stop = Bandbreite; Risiko "
             "0,25 % je Trade, Hebel ≤ 10. Netto = nach Spread, Kommission und Slippage; Ergebnisse je Nacht in bp "
             "des Kapitals, Nächte ohne Trade mit 0.\n"]
    verdict = {}
    for v, sym in VARIANTS.items():
        rows, tr = run_model_a(load_bars(sym, "M5"), sym, first, last)
        save(rows, "is", v)
        m = stats(rows, IS_YEARS)
        checks = checks_is(m, IS_YEARS)
        verdict[v] = (m, all(ok for _, _, ok in checks))
        lines += variant_lines(v, m, checks) + trade_lines(tr)
    passed = [v for v, (_, ok) in verdict.items() if ok]
    if passed:
        best = max(passed, key=lambda v: verdict[v][0]["t"])
        lines.append(f"**Ergebnis:** bestanden: {', '.join(passed)}; gewählt für den Hold-out: **{best}**.")
    else:
        lines.append("**Ergebnis: Keine Variante erfüllt alle In-Sample-Kriterien. Strategie Nr. 32 ist gescheitert; "
                     "der Hold-out bleibt unberührt.**")
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    (RESULTS_DIR / "a_in_sample.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))


def holdout(variant: str):
    marker = OUT_DIR / "ho" / "DONE"
    if marker.exists():
        sys.exit("Hold-out wurde bereits ausgewertet (data/a/ho/DONE) – kein zweiter Lauf.")
    m_is = stats(load("is", variant), IS_YEARS)
    if not all(ok for _, _, ok in checks_is(m_is, IS_YEARS)):
        sys.exit(f"{variant} hat die In-Sample-Kriterien nicht erfüllt – kein Hold-out.")
    marker.parent.mkdir(parents=True, exist_ok=True)
    marker.write_text(f"T112 {variant} {date.today().isoformat()}\n")
    rows, _ = run_model_a(load_bars(VARIANTS[variant], "M5"), VARIANTS[variant], date(2024, 1, 1), date(2026, 12, 31))
    save(rows, "ho", variant)
    m = stats(rows, HO_YEARS)
    lo, hi = cluster_bootstrap_ci(m_is["net_arr"], m_is["month_arr"])
    checks = [("Mittleres Netto-Tagesergebnis > 0", f"{m['E']:+.2f} bp", m["E"] > 0),
              ("≥ untere 95-%-Grenze von In-Sample (Cluster-Bootstrap nach Monat)",
               f"{m['E']:+.2f} vs. IS {m_is['E']:+.2f} [{lo:+.2f}; {hi:+.2f}] bp", m["E"] >= lo)]
    lines = [f"# Modell A, Hold-out 2024–2026 (Trial T112, {variant})\n",
             f"Einmaliger Lauf vom {date.today():%d.%m.%Y}.\n"] + variant_lines(variant, m, checks)
    (RESULTS_DIR / "a_holdout.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
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
