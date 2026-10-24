#!/usr/bin/env python3
"""Strategy no. 21, model P (z-score mean reversion AUDNZD / EURCHF): in-sample runs T72 (P-AUDNZD) and T73
(P-EURCHF) with the pre-registered acceptance check and descriptive tables, and - only for a variant that passed -
the one-time hold-out run T74 (docs/01_Vorregistrierung.md).

Usage:
  ../smart-money-concept/research/.venv/bin/python -I research/scripts/run_p.py                     # T72 + T73
  ../smart-money-concept/research/.venv/bin/python -I research/scripts/run_p.py --holdout P-AUDNZD  # T74, once
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

from pmr import DATA_DIR, RESULTS_DIR  # noqa: E402
from pmr.model import VARIANTS, run_model_p, trades  # noqa: E402
from smc import timez  # noqa: E402
from smc.data.bars import load_bars  # noqa: E402
from smc.report import cluster_bootstrap_ci, cluster_t  # noqa: E402
from smc.strategy_g import ANNUAL, DAY_DTYPE, daily_prices  # noqa: E402
from smc.swaps import RateTable  # noqa: E402

IS_FROM, IS_TO = timegm((2015, 1, 1, 0, 0, 0)) // timez.DAY, timegm((2024, 1, 1, 0, 0, 0)) // timez.DAY
IS_YEARS, HO_YEARS = range(2015, 2024), range(2024, 2027)
OUT_DIR = DATA_DIR / "p"


def year_of(days):
    return np.asarray(days * timez.DAY, dtype="datetime64[s]").astype("datetime64[Y]").astype(int) + 1970


def month_of(days):
    return np.asarray(days * timez.DAY, dtype="datetime64[s]").astype("datetime64[M]").astype(np.int64)


def market(symbol: str, day_to: int | None):
    px = daily_prices(load_bars(symbol, "M5"))
    if day_to is not None:
        px = {k: v[px["day"] < day_to] for k, v in px.items()}
    return px


def stats(rows: np.ndarray, years) -> dict:
    net, cost, days = rows["net"], rows["cost"], rows["day"]
    n, sd = len(net), net.std(ddof=1)
    scale = 0.10 / (sd * np.sqrt(ANNUAL))
    equity = np.cumsum(net * scale)
    per_year = n / ANNUAL
    m = {"days": n, "E": float(net.mean()), "sd": float(sd), "E_2x": float((net - cost).mean()),
         "t_iid": float(net.mean() / (sd / np.sqrt(n))), "t_week": cluster_t(net, (days + 3) // 7),
         "t_month": cluster_t(net, month_of(days)), "sharpe": float(net.mean() / sd * np.sqrt(ANNUAL)),
         "ret": float(net.mean() * ANNUAL), "vol": float(sd * np.sqrt(ANNUAL)),
         "ret10": float(net.mean() * scale * ANNUAL), "maxdd10": float((np.maximum.accumulate(equity) - equity).max()),
         "worst10": float((net * scale).min()),
         "pnl": float(rows["pnl"].sum() / per_year), "swap": float(rows["swap"].sum() / per_year),
         "trade": float(rows["trade_cost"].sum() / per_year), "w_mean": float(rows["w"].mean()),
         "w_max": float(rows["w"].max()), "scale": scale, "days_arr": days, "net_arr": net}
    m["t"] = min(m["t_iid"], m["t_week"], m["t_month"])
    yr = year_of(days)
    m["by_year"] = {y: float(net[yr == y].sum()) for y in years}
    m["years_pos"] = sum(1 for v in m["by_year"].values() if v > 0)
    m["halves"] = (float(net[yr <= 2019].mean()), float(net[yr >= 2020].mean()))
    return m


def checks_is(m: dict, years) -> list:
    a, b = m["halves"]
    return [("Mittleres Netto-Tagesergebnis > 0 mit t ≥ 3,0 (kleinster aus iid / Woche / Monat)",
             f"t = {m['t']:.2f} (Sharpe {m['sharpe']:.2f})", m["E"] > 0 and m["t"] >= 3.0),
            (f"≥ 6 von {len(years)} Jahren positiv", f"{m['years_pos']} von {len(years)}", m["years_pos"] >= 6),
            ("beide Teilzeiträume 2015–2019 und 2020–2023 positiv", f"{a * 1e4:+.2f} / {b * 1e4:+.2f} bp/Tag", a > 0 and b > 0),
            ("bei doppelten Kosten > 0", f"{m['E_2x'] * ANNUAL:+.2%} p. a. (unskaliert)", m["E_2x"] > 0)]


def report(name: str, m: dict, checks: list | None) -> list[str]:
    out = [f"## {name}\n", "| Kennzahl | Wert |", "|---|---|",
           f"| Handelstage | {m['days']:,} |",
           f"| Rendite / Volatilität p. a. (unskaliert) | {m['ret']:+.2%} / {m['vol']:.1%} |",
           f"| Sharpe Ratio p. a. (netto) | {m['sharpe']:.2f} |",
           f"| t-Wert iid / Woche / Monat | {m['t_iid']:.2f} / {m['t_week']:.2f} / {m['t_month']:.2f} |",
           f"| Zerlegung p. a. (unskaliert): Kurs / Swaps / Handel | {m['pnl']:+.2%} / {m['swap']:+.2%} / {-m['trade']:+.2%} |",
           f"| Ø / max. Gewicht w | {m['w_mean']:.2f} / {m['w_max']:.2f} |",
           f"| bei 10 % Vol.: Rendite p. a. / max. Drawdown / schlechtester Tag | {m['ret10']:+.2%} / {m['maxdd10']:.1%} / {m['worst10']:+.2%} |"]
    if checks:
        out += ["", "| Kriterium | Ergebnis | erfüllt |", "|---|---|---|"]
        out += [f"| {c} | {v} | {'ja' if ok else '**nein**'} |" for c, v, ok in checks]
        passed = all(ok for _, _, ok in checks)
        out += ["", f"**{name}: {'alle Kriterien erfüllt' if passed else 'nicht bestanden'}.**"]
    out += ["", "| Jahr | Rendite (unskaliert) |", "|---|---|"]
    out += [f"| {y} | {v:+.1%} |" for y, v in m["by_year"].items()]
    return out + [""]


def trade_lines(rows: np.ndarray) -> list[str]:
    tr = trades(rows)
    res = np.array([x for _, _, x in tr])
    hold = np.array([h for _, h, _ in tr])
    return ["| Trades | Trefferquote | Ø Ergebnis je Trade (Kapital) | Ø Haltedauer (Handelstage) | Zeit im Markt |",
            "|---|---|---|---|---|",
            f"| {len(tr)} | {(res > 0).mean():.0%} | {res.mean() * 1e4:+.1f} bp | {hold.mean():.1f} | "
            f"{(rows['w'] != 0).mean():.0%} |", ""]


def window(rows, lo, hi):
    return rows[(rows["day"] >= lo) & (rows["day"] < hi)]


def save(rows: np.ndarray, phase: str, name: str):
    (OUT_DIR / phase).mkdir(parents=True, exist_ok=True)
    pq.write_table(pa.table({n: rows[n] for n in rows.dtype.names}), OUT_DIR / phase / f"{name}.parquet",
                   compression="zstd")


def load(phase: str, name: str) -> np.ndarray:
    t = pq.read_table(OUT_DIR / phase / f"{name}.parquet")
    rows = np.empty(t.num_rows, DAY_DTYPE)
    for n in DAY_DTYPE.names:
        rows[n] = t.column(n).to_numpy(zero_copy_only=False)
    return rows


def in_sample():
    rates = RateTable.load()
    lines = ["# Modell P (z-Score Mean Reversion AUDNZD / EURCHF), In-Sample 2015–2023 (Trial T72 P-AUDNZD, T73 P-EURCHF)\n",
             f"Lauf vom {date.today():%d.%m.%Y}. Regeln laut `docs/01_Vorregistrierung.md`, Code `research/pmr/`. "
             "Tagesbuchhaltung von Modell G (16:50 New York), FX-Kosten, Swaps und 0,7-%-Gebühr. Positionen 10 % / σ; "
             "Renditen unskaliert und zusätzlich auf 10 % Volatilität skaliert (nur zur Einordnung).\n"]
    verdict = {}
    for v in VARIANTS:
        rows = run_model_p(v, market(VARIANTS[v], IS_TO), rates)
        save(rows, "is", v)
        rows_is = window(rows, IS_FROM, IS_TO)
        m = stats(rows_is, IS_YEARS)
        checks = checks_is(m, IS_YEARS)
        verdict[v] = (m, all(ok for _, _, ok in checks))
        lines += report(v, m, checks) + trade_lines(rows_is)
    lines += ["# Beschreibend\n"]
    rows = window(load("is", "P-EURCHF"), IS_FROM, IS_TO)
    jan15 = (rows["day"] >= timegm((2015, 1, 1, 0, 0, 0)) // timez.DAY) & (rows["day"] < timegm((2015, 2, 1, 0, 0, 0)) // timez.DAY)
    m = stats(rows[~jan15], IS_YEARS)
    lines += [f"P-EURCHF ohne Januar 2015 (SNB-Schock): Sharpe {m['sharpe']:+.2f}, t {m['t_iid']:+.2f}, "
              f"Januar 2015 allein {rows['net'][jan15].sum():+.2%} (unskaliert).\n"]
    passed = [v for v, (_, ok) in verdict.items() if ok]
    if passed:
        best = max(passed, key=lambda v: verdict[v][0]["t"])
        lines.append(f"**Ergebnis:** bestanden: {', '.join(passed)}; gewählt für den Hold-out: **{best}**.")
    else:
        lines.append("**Ergebnis: Keine Variante erfüllt alle In-Sample-Kriterien. Strategie Nr. 21 ist gescheitert; "
                     "der Hold-out bleibt unberührt.**")
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    (RESULTS_DIR / "p_in_sample.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))


def holdout(variant: str):
    marker = OUT_DIR / "ho" / "DONE"
    if marker.exists():
        sys.exit("Hold-out wurde bereits ausgewertet (data/p/ho/DONE) – kein zweiter Lauf.")
    m_is = stats(window(load("is", variant), IS_FROM, IS_TO), IS_YEARS)
    if not all(ok for _, _, ok in checks_is(m_is, IS_YEARS)):
        sys.exit(f"{variant} hat die In-Sample-Kriterien nicht erfüllt – kein Hold-out.")
    marker.parent.mkdir(parents=True, exist_ok=True)
    marker.write_text(f"T74 {variant} {date.today().isoformat()}\n")
    rows = run_model_p(variant, market(VARIANTS[variant], None), RateTable.load())
    save(rows, "ho", variant)
    m = stats(window(rows, IS_TO, 10 ** 9), HO_YEARS)
    lo, hi = cluster_bootstrap_ci(m_is["net_arr"], month_of(m_is["days_arr"]))
    checks = [("Mittleres Netto-Tagesergebnis > 0", f"Sharpe {m['sharpe']:.2f}", m["E"] > 0),
              ("≥ untere 95-%-Grenze von In-Sample (Cluster nach Monat)",
               f"{m['E'] * 1e4:+.3f} vs. IS {m_is['E'] * 1e4:+.3f} [{lo * 1e4:+.3f}; {hi * 1e4:+.3f}] bp/Tag", m["E"] >= lo)]
    lines = [f"# Modell P, Hold-out 2024–2026 (Trial T74, {variant})\n", f"Einmaliger Lauf vom {date.today():%d.%m.%Y}.\n"]
    lines += report(variant, m, checks)
    (RESULTS_DIR / "p_holdout.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
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
