#!/usr/bin/env python3
"""Strategies no. 28 and 30, model B (channel breakout): in-sample runs T96 (B-52W) and T97 (B-TURTLE) with the pre-registered
acceptance check and descriptive tables, and - only for a variant that passed - its one-time hold-out
run (docs/01_Vorregistrierung.md).

Usage:
  ../smart-money-concept/research/.venv/bin/python -I research/scripts/run_b.py                  # T96 + T97
  ../smart-money-concept/research/.venv/bin/python -I research/scripts/run_b.py --holdout B-52W  # once per variant
"""
import argparse
import sys
from calendar import timegm
from concurrent.futures import ProcessPoolExecutor
from datetime import date
from pathlib import Path

import numpy as np
import pyarrow as pa
import pyarrow.parquet as pq

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from brk import DATA_DIR, RESULTS_DIR  # noqa: E402
from brk.model import CFDS, VARIANTS, run_model_b  # noqa: E402
from carry.model import CarrySpec  # noqa: E402
from smc.config import SYMBOLS  # noqa: E402
from smc.strategy_h import spec_for  # noqa: E402
from smc import timez  # noqa: E402
from smc.data.bars import load_bars  # noqa: E402
from smc.report import cluster_bootstrap_ci, cluster_t  # noqa: E402
from smc.strategy_g import ANNUAL, daily_prices  # noqa: E402
from smc.swaps import RateTable  # noqa: E402

IS_FROM, IS_TO = timegm((2015, 1, 1, 0, 0, 0)) // timez.DAY, timegm((2024, 1, 1, 0, 0, 0)) // timez.DAY
IS_YEARS, HO_YEARS = range(2015, 2024), range(2024, 2027)
OUT_DIR = DATA_DIR / "b"
FX = tuple(SYMBOLS) + CFDS
CLASS = {**{s: "FX" for s in SYMBOLS if s != "XAUUSD"}, "XAUUSD": "Metalle", "XAGUSD": "Metalle", "BCOUSD": "Öl",
         **{s: "Indizes" for s in CFDS if s not in ("XAGUSD", "BCOUSD")}}
MIN_POSITION_DAYS = 250


def prices(symbol: str):
    m5 = load_bars(symbol, "M5")
    if symbol in CFDS:
        spec = spec_for(symbol, m5)
        return spec, daily_prices(m5, spec.signal_time, spec.mark_time)
    return CarrySpec(symbol), daily_prices(m5)


def load_prices(day_to: int | None) -> dict:
    with ProcessPoolExecutor(6) as ex:
        res = dict(zip(FX, ex.map(prices, FX)))
    specs, px = {s: r[0] for s, r in res.items()}, {s: r[1] for s, r in res.items()}
    if day_to is not None:
        px = {s: {k: v[p["day"] < day_to] for k, v in p.items()} for s, p in px.items()}
    return specs, px


def year_of_day(days):
    return np.asarray(days * timez.DAY, dtype="datetime64[s]").astype("datetime64[Y]").astype(int) + 1970


def month_of_day(days):
    return np.asarray(days * timez.DAY, dtype="datetime64[s]").astype("datetime64[M]").astype(np.int64)


def window(rows: np.ndarray, lo: int, hi: int) -> np.ndarray:
    return rows[(rows["day"] >= lo) & (rows["day"] < hi)]


def stats(rows: np.ndarray, years) -> dict:
    days, inv = np.unique(rows["day"], return_inverse=True)
    net, cost = np.bincount(inv, rows["net"]), np.bincount(inv, rows["cost"])
    n, sd = len(net), net.std(ddof=1)
    scale = 0.10 / (sd * np.sqrt(ANNUAL))                 # portfolio at 10 % volatility p. a.
    equity = np.cumsum(net * scale)
    per_year = n / ANNUAL
    m = {"days": n, "E": float(net.mean()), "sd": float(sd), "E_2x": float((net - cost).mean()),
         "t_iid": float(net.mean() / (sd / np.sqrt(n))), "t_week": cluster_t(net, (days + 3) // 7),
         "t_month": cluster_t(net, month_of_day(days)), "sharpe": float(net.mean() / sd * np.sqrt(ANNUAL)),
         "ret10": float(net.mean() * scale * ANNUAL), "maxdd10": float((np.maximum.accumulate(equity) - equity).max()),
         "pnl10": float(rows["pnl"].sum() * scale / per_year), "swap10": float(rows["swap"].sum() * scale / per_year),
         "trade10": float(rows["trade_cost"].sum() * scale / per_year), "fee10": float(rows["fee"].sum() * scale / per_year),
         "gross_exposure": float(np.bincount(inv, np.abs(rows["w"])).mean()), "scale": scale,
         "days_arr": days, "net_arr": net}
    m["t"] = min(m["t_iid"], m["t_week"], m["t_month"])
    yr = year_of_day(days)
    m["by_year"] = {y: (float(net[yr == y].sum() * scale), float(net[yr == y].mean() / net[yr == y].std(ddof=1) *
                        np.sqrt(ANNUAL)) if (yr == y).sum() > 2 else np.nan) for y in years}
    m["years_pos"] = sum(1 for tot, _ in m["by_year"].values() if tot > 0)
    m["by_symbol"] = {}
    for s in FX:
        sel = (rows["symbol"] == s) & (rows["w"] != 0)
        if sel.sum() >= MIN_POSITION_DAYS:
            x = rows["net"][rows["symbol"] == s]
            m["by_symbol"][s] = (float(x.sum() * scale), int(sel.sum()), float(rows["swap"][rows["symbol"] == s].sum() * scale))
    m["sym_pos"] = sum(1 for tot, _, _ in m["by_symbol"].values() if tot > 0)
    return m


def checks_is(m: dict, years) -> list:
    n_sym = len(m["by_symbol"])
    return [("Mittleres Netto-Tagesergebnis > 0 mit t ≥ 3,0 (kleinster aus iid / Woche / Monat)",
             f"t = {m['t']:.2f} (Sharpe {m['sharpe']:.2f})", m["E"] > 0 and m["t"] >= 3.0),
            (f"≥ 6 von {len(years)} Jahren positiv", f"{m['years_pos']} von {len(years)}", m["years_pos"] >= 6),
            (f"≥ 60 % der Instrumente (≥ {MIN_POSITION_DAYS} Positionstage) positiv", f"{m['sym_pos']} von {n_sym}",
             n_sym > 0 and m["sym_pos"] >= 0.6 * n_sym),
            ("bei doppelten Kosten > 0", f"{m['E_2x'] * m['scale'] * ANNUAL:+.2%} p. a. bei 10 % Vol.", m["E_2x"] > 0)]


def report(name: str, m: dict, checks: list, verdict: str) -> list[str]:
    out = [f"## {name}\n", "| Kennzahl | Wert |", "|---|---|",
           f"| Handelstage | {m['days']:,} |",
           f"| Sharpe Ratio p. a. (netto) | {m['sharpe']:.2f} |",
           f"| t-Wert iid / Woche / Monat | {m['t_iid']:.2f} / {m['t_week']:.2f} / {m['t_month']:.2f} |",
           f"| Rendite p. a. bei 10 % Volatilität | {m['ret10']:+.2%} |",
           f"| Max. Drawdown bei 10 % Volatilität | {m['maxdd10']:.1%} |",
           f"| Zerlegung p. a. bei 10 % Vol.: Kurs / Swaps / Handel / Gebühr | {m['pnl10']:+.2%} / {m['swap10']:+.2%} / "
           f"{-m['trade10']:+.2%} / {-m['fee10']:+.2%} |",
           f"| Ø Brutto-Exposure (Summe \\|w\\|, unskaliert) | {m['gross_exposure']:.2f} |", "",
           "| Kriterium | Ergebnis | erfüllt |", "|---|---|---|"]
    out += [f"| {c} | {v} | {'ja' if ok else '**nein**'} |" for c, v, ok in checks]
    out += ["", verdict + "\n", "| Jahr | Rendite bei 10 % Vol. | Sharpe |", "|---|---|---|"]
    out += [f"| {y} | {tot:+.1%} | {sr:+.2f} |" for y, (tot, sr) in m["by_year"].items()]
    out += ["", "| Instrument | Positionstage | Beitrag netto bei 10 % Vol. (Summe) | davon Swaps |", "|---|---|---|---|"]
    out += [f"| {s} | {k} | {tot:+.1%} | {sw:+.1%} |"
            for s, (tot, k, sw) in sorted(m["by_symbol"].items(), key=lambda kv: -kv[1][0])]
    return out + [""]


def run_all(variant: str, specs: dict, px: dict, rates: RateTable) -> np.ndarray:
    return np.concatenate([run_model_b(variant, specs[s], px[s], rates) for s in FX])


def save(rows: np.ndarray, phase: str, name: str):
    (OUT_DIR / phase).mkdir(parents=True, exist_ok=True)
    pq.write_table(pa.table({n: rows[n] for n in rows.dtype.names}), OUT_DIR / phase / f"{name}.parquet",
                   compression="zstd")


def in_sample():
    rates = RateTable.load()
    specs, px = load_prices(IS_TO)
    lines = ["# Modell B (Kanal-Ausbruch), In-Sample 2015–2023 (Trial T96 B-52W = Nr. 28, T97 B-TURTLE = Nr. 30)\n",
             f"Lauf vom {date.today():%d.%m.%Y}. Regeln laut `docs/01_Vorregistrierung.md`, Code `research/brk/`. "
             "Handelstage 01.01.2015–31.12.2023 (Warm-up 2014), 34 Instrumente. Netto = nach Handelskosten, Swaps "
             "und 0,7-%-Gebühr (Kostenmodelle G und H). Renditen und Drawdown sind auf eine Portfolio-Volatilität von "
             "10 % p. a. skaliert (Kalibrierung auf diesen Zeitraum, nur zur Einordnung).\n"]
    verdict = {}
    for v in VARIANTS:
        rows = run_all(v, specs, px, rates)
        save(rows, "is", v)
        rows = window(rows, IS_FROM, IS_TO)
        m = stats(rows, IS_YEARS)
        checks = checks_is(m, IS_YEARS)
        ok = all(c for _, _, c in checks)
        verdict[v] = (m, ok)
        lines += report(v, m, checks, f"**{v}: {'alle Kriterien erfüllt' if ok else 'nicht bestanden'}.**")
        lines += ["| Anlageklasse | Beitrag netto bei 10 % Vol. (Summe 2015–2023) |", "|---|---|"]
        for cls in ("FX", "Metalle", "Indizes", "Öl"):
            sel = np.isin(rows["symbol"], [s for s, c in CLASS.items() if c == cls])
            lines.append(f"| {cls} | {rows['net'][sel].sum() * m['scale']:+.1%} |")
        lines.append("")
    passed = [v for v, (_, ok) in verdict.items() if ok]
    if passed:
        best = max(passed, key=lambda v: verdict[v][0]["t"])
        lines.append(f"**Ergebnis:** bestanden: {', '.join(passed)}; gewählt für den Hold-out: **{best}**.")
    else:
        lines.append("**Ergebnis: Keine Variante erfüllt alle In-Sample-Kriterien. Die Strategien Nr. 28 und Nr. 30 sind gescheitert; "
                     "der Hold-out bleibt unberührt.**")
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    (RESULTS_DIR / "b_in_sample.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))


def load(phase: str, name: str) -> np.ndarray:
    from smc.strategy_g import DAY_DTYPE
    t = pq.read_table(OUT_DIR / phase / f"{name}.parquet")
    rows = np.empty(t.num_rows, DAY_DTYPE)
    for n in DAY_DTYPE.names:
        rows[n] = t.column(n).to_numpy(zero_copy_only=False)
    return rows


def holdout(variant: str):
    marker = OUT_DIR / "ho" / f"DONE_{variant}"
    if marker.exists():
        sys.exit("Hold-out wurde bereits ausgewertet (data/b/ho/DONE) – kein zweiter Lauf.")
    m_is = stats(window(load("is", variant), IS_FROM, IS_TO), IS_YEARS)
    if not all(ok for _, _, ok in checks_is(m_is, IS_YEARS)):
        sys.exit(f"{variant} hat die In-Sample-Kriterien nicht erfüllt – kein Hold-out.")
    marker.parent.mkdir(parents=True, exist_ok=True)
    marker.write_text(f"Hold-out {variant} {date.today().isoformat()}\n")
    specs, px = load_prices(None)
    rows = run_all(variant, specs, px, RateTable.load())
    save(rows, "ho", variant)
    m = stats(window(rows, IS_TO, 10**9), HO_YEARS)
    lo, hi = cluster_bootstrap_ci(m_is["net_arr"], month_of_day(m_is["days_arr"]))
    checks = [("Mittleres Netto-Tagesergebnis > 0", f"Sharpe {m['sharpe']:.2f}", m["E"] > 0),
              ("≥ untere 95-%-Grenze von In-Sample (Cluster nach Monat)",
               f"{m['E'] * 1e4:+.3f} vs. IS {m_is['E'] * 1e4:+.3f} [{lo * 1e4:+.3f}; {hi * 1e4:+.3f}] bp/Tag unskaliert",
               m["E"] >= lo)]
    ok = all(c for _, _, c in checks)
    lines = [f"# Modell B, Hold-out 2024–2026 ({variant})\n", f"Einmaliger Lauf vom {date.today():%d.%m.%Y}.\n"]
    lines += report(variant, m, checks, f"**Hold-out {'bestanden – weiter mit FTMO' if ok else 'nicht bestanden'}.**")
    (RESULTS_DIR / f"b_holdout_{variant}.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
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
