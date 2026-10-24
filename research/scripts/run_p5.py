#!/usr/bin/env python3
"""P5 Model F (fix reversal): in-sample runs T9 (F-ALL) and T10 (F-EU) with the pre-registered
acceptance check and - only for a variant that passed - the one-time hold-out run T11
(docs/08_P5_Vorregistrierung_ModellF.md).

Usage:
  research/.venv/bin/python -I research/scripts/run_p5.py                  # T9 + T10, in-sample 2015-2023
  research/.venv/bin/python -I research/scripts/run_p5.py --holdout F-EU   # T11, once
"""
import argparse
import sys
from calendar import timegm
from datetime import date
from pathlib import Path

import numpy as np
import pyarrow as pa
import pyarrow.parquet as pq

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from smc import timez  # noqa: E402
from smc.config import DATA_DIR, PROJECT_ROOT  # noqa: E402
from smc.data.bars import load_bars  # noqa: E402
from smc.report import cluster_bootstrap_ci, cluster_t  # noqa: E402
from smc.strategy_f import run_model_f  # noqa: E402

IS_FROM, IS_TO = timegm((2015, 1, 1, 0, 0, 0)) // timez.DAY, timegm((2024, 1, 1, 0, 0, 0)) // timez.DAY
HO_FROM, HO_TO = IS_TO, timegm((2100, 1, 1, 0, 0, 0)) // timez.DAY
IS_YEARS, HO_YEARS = range(2015, 2024), range(2024, 2027)
PAIRS = ("EURUSD", "GBPUSD", "USDJPY")
EXTRA = ("AUDUSD", "NZDUSD", "USDCAD", "USDCHF")        # descriptive only
VARIANTS = {"F-ALL": {"EURUSD": (1, 2, 3, 4), "GBPUSD": (1, 2, 3, 4), "USDJPY": (1, 2, 3)},
            "F-EU": {"EURUSD": (3, 4), "GBPUSD": (3, 4)}}
WINDOW_NAMES = {1: "W1 pre-Tokio", 2: "W2 post-Tokio", 3: "W3 pre-EZB", 4: "W4 post-London"}
OUT_DIR = DATA_DIR / "p5"
RESULTS = PROJECT_ROOT / "research" / "results"


def run(symbols, phase: str) -> dict:
    d0, d1 = (IS_FROM, IS_TO) if phase == "is" else (HO_FROM, HO_TO)
    parts = []
    for s in symbols:
        rows = run_model_f(s, load_bars(s, "M5"), load_bars(s, "H1"), day_from=d0, day_to=d1)
        print(f"{s}: {len(rows)} Fenster", flush=True)
        parts.append(rows)
    rows = np.concatenate(parts)
    (OUT_DIR / phase).mkdir(parents=True, exist_ok=True)
    pq.write_table(pa.table({n: rows[n] for n in rows.dtype.names}), OUT_DIR / phase / "rows.parquet",
                   compression="zstd")
    return {n: rows[n] for n in rows.dtype.names}


def load(phase: str) -> dict:
    t = pq.read_table(OUT_DIR / phase / "rows.parquet")
    return {n: t.column(n).to_numpy(zero_copy_only=False) for n in t.column_names}


def select(rows: dict, spec: dict) -> dict:
    m = np.zeros(len(rows["symbol"]), bool)
    for sym, wins in spec.items():
        m |= (rows["symbol"] == sym) & np.isin(rows["window"], wins)
    return {k: v[m] for k, v in rows.items()}


def daily(rows: dict) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """FX days with at least one position, their net and cost sums (bp)."""
    days, inv = np.unique(rows["fx_day"], return_inverse=True)
    return days, np.bincount(inv, rows["net_bp"]), np.bincount(inv, rows["cost_bp"])


def year_of_day(days: np.ndarray) -> np.ndarray:
    return np.asarray(days * timez.DAY, dtype="datetime64[s]").astype("datetime64[Y]").astype(int) + 1970


def month_of_day(days: np.ndarray) -> np.ndarray:
    return np.asarray(days * timez.DAY, dtype="datetime64[s]").astype("datetime64[M]").astype(np.int64)


def stats(rows: dict, years) -> dict:
    days, net, cost = daily(rows)
    n = len(net)
    per_year = len(days) / max(1, len(set(year_of_day(days).tolist())))
    m = {"days": n, "positions": len(rows["net_bp"]), "E": float(net.mean()), "sd": float(net.std(ddof=1)),
         "cost": float(cost.mean()), "E_2x": float((net - cost).mean()),
         "t_iid": float(net.mean() / (net.std(ddof=1) / np.sqrt(n))),
         "t_week": cluster_t(net, (days + 3) // 7), "t_month": cluster_t(net, month_of_day(days))}
    m["t"] = min(m["t_iid"], m["t_week"], m["t_month"])
    m["sharpe"] = m["E"] / m["sd"] * np.sqrt(per_year)
    yr = year_of_day(days)
    m["by_year"] = {y: (int((yr == y).sum()), float(net[yr == y].sum())) for y in years}
    m["years_pos"] = sum(1 for k, tot in m["by_year"].values() if k and tot > 0)
    m["by_pair"] = {s: float(rows["net_bp"][rows["symbol"] == s].sum()) for s in sorted(set(rows["symbol"].tolist()))}
    m["pairs_pos"] = sum(1 for v in m["by_pair"].values() if v > 0)
    m["days_arr"], m["net_arr"] = days, net
    return m


def checks_is(m: dict, years) -> list:
    n_pairs = len(m["by_pair"])
    return [("Mittleres Netto-Tagesergebnis > 0 mit t ≥ 3,0 (kleinster aus iid / Woche / Monat)",
             f"{m['E']:+.2f} bp/Tag, t = {m['t']:.2f}", m["E"] > 0 and m["t"] >= 3.0),
            (f"≥ 6 von {len(years)} Jahren positiv", f"{m['years_pos']} von {len(years)}", m["years_pos"] >= 6),
            ("≥ 60 % der Paare positiv", f"{m['pairs_pos']} von {n_pairs}", m["pairs_pos"] >= 0.6 * n_pairs),
            ("bei doppelten Kosten > 0", f"{m['E_2x']:+.2f} bp/Tag", m["E_2x"] > 0)]


def window_table(rows: dict, symbols) -> list[str]:
    out = ["| Paar | Fenster | Positionen | netto Ø bp | vor Kosten Ø bp | t (netto) | Stops |", "|---|---|---|---|---|---|---|"]
    for s in symbols:
        for w in (1, 2, 3, 4):
            m = (rows["symbol"] == s) & (rows["window"] == w)
            if not m.any():
                continue
            x, c = rows["net_bp"][m], rows["cost_bp"][m]
            t = x.mean() / (x.std(ddof=1) / np.sqrt(len(x)))
            out.append(f"| {s} | {WINDOW_NAMES[w]} | {m.sum():,} | {x.mean():+.2f} | {(x + c).mean():+.2f} | "
                       f"{t:+.2f} | {rows['stopped'][m].mean():.1%} |")
    return out + [""]


def variant_lines(name: str, m: dict, checks: list) -> list[str]:
    passed = all(ok for _, _, ok in checks)
    out = [f"## {name}\n", "| Kennzahl | Wert |", "|---|---|",
           f"| Handelstage / Positionen | {m['days']:,} / {m['positions']:,} |",
           f"| Netto je Tag | {m['E']:+.2f} bp (σ {m['sd']:.1f} bp) |",
           f"| Kosten je Tag | {m['cost']:.2f} bp |",
           f"| Sharpe Ratio p. a. (netto) | {m['sharpe']:.2f} |",
           f"| t-Wert iid / Woche / Monat | {m['t_iid']:.2f} / {m['t_week']:.2f} / {m['t_month']:.2f} |",
           f"| bei doppelten Kosten | {m['E_2x']:+.2f} bp/Tag |", "",
           "| Kriterium | Ergebnis | erfüllt |", "|---|---|---|"]
    out += [f"| {c} | {v} | {'ja' if ok else '**nein**'} |" for c, v, ok in checks]
    out += ["", f"**{name}: {'alle Kriterien erfüllt' if passed else 'nicht bestanden'}.**\n",
            "| Jahr | Tage | Netto Summe bp |", "|---|---|---|"]
    out += [f"| {y} | {k} | {tot:+.1f} |" for y, (k, tot) in m["by_year"].items()]
    out += ["", "| Paar | Netto Summe bp |", "|---|---|"] + [f"| {s} | {v:+.1f} |" for s, v in m["by_pair"].items()]
    return out + [""]


def in_sample():
    rows = run(PAIRS + EXTRA, "is")
    lines = ["# P5 – Modell F (Fix-Reversal), In-Sample 2015–2023 (Trial T9 F-ALL, T10 F-EU)\n",
             f"Lauf vom {date.today():%d.%m.%Y}. Regeln laut `docs/08_P5_Vorregistrierung_ModellF.md`, Code "
             "`research/smc/strategy_f.py`. FX-Tage 01.01.2015–31.12.2023, HistData-M5 (Bid). Netto = nach Spread, "
             "Kommission, Slippage (Ein- und Ausstieg) und 0,7-%-Gebühr bei USDJPY; je Position gleicher Nominalwert, "
             "Ergebnisse in Basispunkten.\n",
             "## Alle Paare und Fenster (beschreibend)\n"]
    lines += window_table(rows, PAIRS + EXTRA)
    verdict = {}
    for name, spec in VARIANTS.items():
        m = stats(select(rows, spec), IS_YEARS)
        checks = checks_is(m, IS_YEARS)
        verdict[name] = (m, all(ok for _, _, ok in checks))
        lines += variant_lines(name, m, checks)
    passed = [v for v, (_, ok) in verdict.items() if ok]
    if passed:
        best = max(passed, key=lambda v: verdict[v][0]["t"])
        lines.append(f"**Ergebnis:** bestanden: {', '.join(passed)}; gewählt für den Hold-out: **{best}**.")
    else:
        lines.append("**Ergebnis: Keine Variante erfüllt alle In-Sample-Kriterien. P5 ist gescheitert; "
                     "der Hold-out bleibt unberührt.**")
    (RESULTS / "p5_modell_f_in_sample.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))


def holdout(variant: str):
    marker = OUT_DIR / "ho" / "DONE"
    if marker.exists():
        sys.exit("Hold-out wurde bereits ausgewertet (data/p5/ho/DONE) – kein zweiter Lauf.")
    m_is = stats(select(load("is"), VARIANTS[variant]), IS_YEARS)
    if not all(ok for _, _, ok in checks_is(m_is, IS_YEARS)):
        sys.exit(f"{variant} hat die In-Sample-Kriterien nicht erfüllt – kein Hold-out.")
    marker.parent.mkdir(parents=True, exist_ok=True)
    marker.write_text(f"T11 {variant} {date.today().isoformat()}\n")
    rows = select(run(tuple(VARIANTS[variant]), "ho"), VARIANTS[variant])
    m = stats(rows, HO_YEARS)
    lo, hi = cluster_bootstrap_ci(m_is["net_arr"], month_of_day(m_is["days_arr"]))
    checks = [("Mittleres Netto-Tagesergebnis > 0", f"{m['E']:+.2f} bp/Tag", m["E"] > 0),
              ("≥ untere 95-%-Grenze von In-Sample (Cluster nach Monat)",
               f"{m['E']:+.2f} vs. IS {m_is['E']:+.2f} [{lo:+.2f}; {hi:+.2f}] bp/Tag", m["E"] >= lo)]
    lines = [f"# P5 – Modell F, Hold-out 2024–2026 (Trial T11, {variant})\n",
             f"Einmaliger Lauf vom {date.today():%d.%m.%Y}.\n"] + variant_lines(variant, m, checks)
    lines += window_table(rows, tuple(VARIANTS[variant]))
    (RESULTS / "p5_modell_f_holdout.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
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
