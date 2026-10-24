#!/usr/bin/env python3
"""Strategy no. 15, model R (short-term reversal US500, Connors): in-sample runs T52 (R-RSI2) and T53 (R-7S) with
the pre-registered acceptance check and descriptive tables, and - only for a variant that passed - the one-time
hold-out run T54 (docs/01_Vorregistrierung.md).

Usage:
  ../smart-money-concept/research/.venv/bin/python -I research/scripts/run_r.py                   # T52 + T53
  ../smart-money-concept/research/.venv/bin/python -I research/scripts/run_r.py --holdout R-RSI2  # T54, once
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

from strev import DATA_DIR, RESULTS_DIR  # noqa: E402
from strev.model import VARIANTS, run_model_r, trades  # noqa: E402
from smc import timez  # noqa: E402
from smc.data.bars import load_bars  # noqa: E402
from smc.report import cluster_bootstrap_ci, cluster_t  # noqa: E402
from smc.strategy_g import ANNUAL, DAY_DTYPE, daily_prices  # noqa: E402
from smc.strategy_h import spec_for  # noqa: E402
from smc.swaps import RateTable  # noqa: E402

IS_FROM, IS_TO = timegm((2015, 1, 1, 0, 0, 0)) // timez.DAY, timegm((2024, 1, 1, 0, 0, 0)) // timez.DAY
IS_YEARS, HO_YEARS = range(2015, 2024), range(2024, 2027)
OUT_DIR = DATA_DIR / "r"


def year_of(days):
    return np.asarray(days * timez.DAY, dtype="datetime64[s]").astype("datetime64[Y]").astype(int) + 1970


def month_of(days):
    return np.asarray(days * timez.DAY, dtype="datetime64[s]").astype("datetime64[M]").astype(np.int64)


def market(symbol: str, day_to: int | None):
    m5 = load_bars(symbol, "M5")
    spec = spec_for(symbol, m5)
    px = daily_prices(m5, spec.signal_time, spec.mark_time)
    if day_to is not None:
        px = {k: v[px["day"] < day_to] for k, v in px.items()}
    return spec, px


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
    return ["| Trades | Trefferquote | Ø Ergebnis je Trade | Ø Haltedauer (Handelstage) | Zeit im Markt |",
            "|---|---|---|---|---|",
            f"| {len(tr)} | {(res > 0).mean():.0%} | {res.mean() * 1e4:+.1f} bp | {hold.mean():.1f} | "
            f"{(rows['w'] > 0).mean():.0%} |", ""]


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
    spec, px = market("SPXUSD", IS_TO)
    lines = ["# Modell R (Kurzfrist-Reversal US500, Connors), In-Sample 2015–2023 (Trial T52 R-RSI2, T53 R-7S)\n",
             f"Lauf vom {date.today():%d.%m.%Y}. Regeln laut `docs/01_Vorregistrierung.md`, Code `research/strev/`. "
             "Tagesbuchhaltung von Modell G (15:50 New York) mit Index-Kosten und -Swaps (Modell H). Netto = nach "
             "Handelskosten und Swaps. Position 1 × Kapital oder flat; Renditen unskaliert und zusätzlich auf 10 % "
             "Volatilität skaliert (nur zur Einordnung).\n"]
    verdict = {}
    for v in VARIANTS:
        rows = run_model_r(v, spec, px, rates)
        save(rows, "is", v)
        rows_is = window(rows, IS_FROM, IS_TO)
        m = stats(rows_is, IS_YEARS)
        checks = checks_is(m, IS_YEARS)
        verdict[v] = (m, all(ok for _, _, ok in checks))
        lines += report(v, m, checks) + trade_lines(rows_is)
    lines += ["# Beschreibend\n"]
    lines += report("Referenz: US500 halten (w = 1)", stats(window(run_model_r("HALTEN", spec, px, rates),
                                                                      IS_FROM, IS_TO), IS_YEARS), None)
    spec_n, px_n = market("NSXUSD", IS_TO)
    lines += ["## US100\n", "| Variante | Sharpe | t (iid) | Rendite p. a. | Jahre positiv |", "|---|---|---|---|---|"]
    for v in (*VARIANTS, "HALTEN"):
        m = stats(window(run_model_r(v, spec_n, px_n, rates), IS_FROM, IS_TO), IS_YEARS)
        lines.append(f"| {v} | {m['sharpe']:+.2f} | {m['t_iid']:+.2f} | {m['ret']:+.2%} | {m['years_pos']} von 9 |")
    lines.append("")
    passed = [v for v, (_, ok) in verdict.items() if ok]
    if passed:
        best = max(passed, key=lambda v: verdict[v][0]["t"])
        lines.append(f"**Ergebnis:** bestanden: {', '.join(passed)}; gewählt für den Hold-out: **{best}**.")
    else:
        lines.append("**Ergebnis: Keine Variante erfüllt alle In-Sample-Kriterien. Strategie Nr. 15 ist gescheitert; "
                     "der Hold-out bleibt unberührt.**")
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    (RESULTS_DIR / "r_in_sample.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))


def holdout(variant: str):
    marker = OUT_DIR / "ho" / "DONE"
    if marker.exists():
        sys.exit("Hold-out wurde bereits ausgewertet (data/r/ho/DONE) – kein zweiter Lauf.")
    m_is = stats(window(load("is", variant), IS_FROM, IS_TO), IS_YEARS)
    if not all(ok for _, _, ok in checks_is(m_is, IS_YEARS)):
        sys.exit(f"{variant} hat die In-Sample-Kriterien nicht erfüllt – kein Hold-out.")
    marker.parent.mkdir(parents=True, exist_ok=True)
    marker.write_text(f"T54 {variant} {date.today().isoformat()}\n")
    spec, px = market("SPXUSD", None)
    rows = run_model_r(variant, spec, px, RateTable.load())
    save(rows, "ho", variant)
    m = stats(window(rows, IS_TO, 10 ** 9), HO_YEARS)
    lo, hi = cluster_bootstrap_ci(m_is["net_arr"], month_of(m_is["days_arr"]))
    checks = [("Mittleres Netto-Tagesergebnis > 0", f"Sharpe {m['sharpe']:.2f}", m["E"] > 0),
              ("≥ untere 95-%-Grenze von In-Sample (Cluster nach Monat)",
               f"{m['E'] * 1e4:+.3f} vs. IS {m_is['E'] * 1e4:+.3f} [{lo * 1e4:+.3f}; {hi * 1e4:+.3f}] bp/Tag", m["E"] >= lo)]
    lines = [f"# Modell R, Hold-out 2024–2026 (Trial T54, {variant})\n", f"Einmaliger Lauf vom {date.today():%d.%m.%Y}.\n"]
    lines += report(variant, m, checks)
    (RESULTS_DIR / "r_holdout.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
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
