#!/usr/bin/env python3
"""Strategy no. 8, model V (FX value G8): in-sample runs T299 (V-5Y) and T300 (V-PPP) with the pre-registered
acceptance check and descriptive tables, and - only for a variant that passed - the one-time hold-out
run T301 (docs/01_Vorregistrierung.md).

Usage:
  ../smart-money-concept/research/.venv/bin/python -I research/scripts/run_v8.py                # T299 + T300
  ../smart-money-concept/research/.venv/bin/python -I research/scripts/run_v8.py --holdout V-5Y  # T301, once
"""
import argparse
import sys
from calendar import timegm
from collections import Counter
from concurrent.futures import ProcessPoolExecutor
from datetime import date
from pathlib import Path

import numpy as np
import pyarrow as pa
import pyarrow.parquet as pq

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from fval import DATA_DIR, RAW_DIR, RESULTS_DIR  # noqa: E402
from carry.model import FX, run_model_k  # noqa: E402
from fval.model import VARIANTS, real_rates, run_model_v  # noqa: E402
from smc import timez  # noqa: E402
from smc.data.bars import load_bars  # noqa: E402
from smc.report import cluster_bootstrap_ci, cluster_t  # noqa: E402
from smc.strategy_g import ANNUAL, daily_prices  # noqa: E402
from smc.swaps import RateTable  # noqa: E402

IS_FROM, IS_TO = timegm((2015, 1, 1, 0, 0, 0)) // timez.DAY, timegm((2024, 1, 1, 0, 0, 0)) // timez.DAY
IS_YEARS, HO_YEARS = range(2015, 2024), range(2024, 2027)
OUT_DIR = DATA_DIR / "v"
Q = real_rates(RAW_DIR, 2026 * 12 + 11)
MIN_POSITION_DAYS = 250


def prices(symbol: str) -> dict:
    return daily_prices(load_bars(symbol, "M5"))


def load_prices(day_to: int | None) -> dict:
    with ProcessPoolExecutor(6) as ex:
        px = dict(zip(FX, ex.map(prices, FX)))
    if day_to is not None:
        px = {s: {k: v[p["day"] < day_to] for k, v in p.items()} for s, p in px.items()}
    return px


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


def ranking_table(log: list, lo: int, hi: int) -> list[str]:
    log = [x for x in log if lo <= x[0] < hi]
    longs, shorts = Counter(c for _, ls, _ in log for c in ls), Counter(c for _, _, ss in log for c in ss)
    cur = sorted(set(longs) | set(shorts), key=lambda c: (-longs[c], shorts[c]))
    out = [f"Monate: {len(log)}\n", "| Währung | Monate long | Monate short |", "|---|---|---|"]
    return out + [f"| {c} | {longs[c]} | {shorts[c]} |" for c in cur] + [""]


def save(rows: np.ndarray, phase: str, name: str):
    (OUT_DIR / phase).mkdir(parents=True, exist_ok=True)
    pq.write_table(pa.table({n: rows[n] for n in rows.dtype.names}), OUT_DIR / phase / f"{name}.parquet",
                   compression="zstd")


def in_sample():
    rates = RateTable.load()
    px = load_prices(IS_TO)
    lines = ["# Modell V (FX Value G8), In-Sample 2015–2023 (Trial T299 V-5Y, T300 V-PPP)\n",
             f"Lauf vom {date.today():%d.%m.%Y}. Regeln laut `docs/01_Vorregistrierung.md`, Code `research/fval/` mit der Engine aus `../06-fx-carry/research/carry/`. "
             "Realer Wechselkurs aus FRED-CPI (2 Monate Verzug) und FRED-Monatsendkursen. "
             "Handelstage 01.01.2015–31.12.2023 (Warm-up 2014), 24 FX-Paare. Netto = nach Handelskosten, Swaps "
             "(Zinsdifferenz − 1 % Aufschlag) und 0,7-%-Gebühr. Renditen und Drawdown sind auf eine Portfolio-"
             "Volatilität von 10 % p. a. skaliert (Kalibrierung auf diesen Zeitraum, nur zur Einordnung).\n"]
    verdict = {}
    for v in VARIANTS:
        rows, log = run_model_v(px, Q, rates, v)
        save(rows, "is", v)
        rows = window(rows, IS_FROM, IS_TO)
        m = stats(rows, IS_YEARS)
        checks = checks_is(m, IS_YEARS)
        ok = all(c for _, _, c in checks)
        verdict[v] = (m, ok)
        lines += report(v, m, checks, f"**{v}: {'alle Kriterien erfüllt' if ok else 'nicht bestanden'}.**")
        nm = stats(window(run_model_v(px, Q, rates, v, markup=0.0)[0], IS_FROM, IS_TO), IS_YEARS)
        lines += ["### Beschreibend\n", "| Auswertung | Sharpe | t (iid) | Rendite p. a. bei 10 % Vol. | Swaps p. a. |",
                  "|---|---|---|---|---|",
                  f"| vorregistriert (Aufschlag 1 %) | {m['sharpe']:+.2f} | {m['t_iid']:+.2f} | {m['ret10']:+.2%} | {m['swap10']:+.2%} |",
                  f"| ohne Swap-Aufschlag | {nm['sharpe']:+.2f} | {nm['t_iid']:+.2f} | {nm['ret10']:+.2%} | {nm['swap10']:+.2%} |",
                  ""]
        for lbl, (a, b) in (("2015–2019", (2015, 2020)), ("2020–2023", (2020, 2024))):
            sub = window(rows, timegm((a, 1, 1, 0, 0, 0)) // timez.DAY, timegm((b, 1, 1, 0, 0, 0)) // timez.DAY)
            s = stats(sub, range(a, b))
            lines.append(f"- {lbl}: Sharpe {s['sharpe']:+.2f}, Kurs {s['pnl10']:+.2%} p. a., Swaps {s['swap10']:+.2%} p. a. "
                         "(bei 10 % Vol. des Teilzeitraums)")
        lines += ["", "**Rangfolge nach Value-Signal (Long- und Short-Seite)**\n"] + ranking_table(log, IS_FROM, IS_TO)
    k3 = window(run_model_k(px, rates, "K-3")[0], IS_FROM, IS_TO)
    kd, ki = np.unique(k3["day"], return_inverse=True)
    k_net = np.bincount(ki, k3["net"])
    corr = {}
    for v, (m, _) in verdict.items():
        both = np.intersect1d(m["days_arr"], kd)
        corr[v] = np.corrcoef(m["net_arr"][np.isin(m["days_arr"], both)], k_net[np.isin(kd, both)])[0, 1]
    lines.append("**Korrelation der Netto-Tagesergebnisse mit Carry K-3 (Nr. 6):** "
                 + ", ".join(f"{v} {c:+.2f}" for v, c in corr.items()) + "\n")
    passed = [v for v, (_, ok) in verdict.items() if ok]
    if passed:
        best = max(passed, key=lambda v: verdict[v][0]["t"])
        lines.append(f"**Ergebnis:** bestanden: {', '.join(passed)}; gewählt für den Hold-out: **{best}**.")
    else:
        lines.append("**Ergebnis: Keine Variante erfüllt alle In-Sample-Kriterien. Strategie Nr. 8 ist gescheitert; "
                     "der Hold-out bleibt unberührt.**")
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    (RESULTS_DIR / "v_in_sample.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))


def load(phase: str, name: str) -> np.ndarray:
    from smc.strategy_g import DAY_DTYPE
    t = pq.read_table(OUT_DIR / phase / f"{name}.parquet")
    rows = np.empty(t.num_rows, DAY_DTYPE)
    for n in DAY_DTYPE.names:
        rows[n] = t.column(n).to_numpy(zero_copy_only=False)
    return rows


def holdout(variant: str):
    marker = OUT_DIR / "ho" / "DONE"
    if marker.exists():
        sys.exit("Hold-out wurde bereits ausgewertet (data/v/ho/DONE) – kein zweiter Lauf.")
    m_is = stats(window(load("is", variant), IS_FROM, IS_TO), IS_YEARS)
    if not all(ok for _, _, ok in checks_is(m_is, IS_YEARS)):
        sys.exit(f"{variant} hat die In-Sample-Kriterien nicht erfüllt – kein Hold-out.")
    marker.parent.mkdir(parents=True, exist_ok=True)
    marker.write_text(f"T301 {variant} {date.today().isoformat()}\n")
    rows, _ = run_model_v(load_prices(None), Q, RateTable.load(), variant)
    save(rows, "ho", variant)
    m = stats(window(rows, IS_TO, 10**9), HO_YEARS)
    lo, hi = cluster_bootstrap_ci(m_is["net_arr"], month_of_day(m_is["days_arr"]))
    checks = [("Mittleres Netto-Tagesergebnis > 0", f"Sharpe {m['sharpe']:.2f}", m["E"] > 0),
              ("≥ untere 95-%-Grenze von In-Sample (Cluster nach Monat)",
               f"{m['E'] * 1e4:+.3f} vs. IS {m_is['E'] * 1e4:+.3f} [{lo * 1e4:+.3f}; {hi * 1e4:+.3f}] bp/Tag unskaliert",
               m["E"] >= lo)]
    ok = all(c for _, _, c in checks)
    lines = [f"# Modell V, Hold-out 2024–2026 (Trial T301, {variant})\n", f"Einmaliger Lauf vom {date.today():%d.%m.%Y}.\n"]
    lines += report(variant, m, checks, f"**Hold-out {'bestanden – weiter mit T71 (FTMO)' if ok else 'nicht bestanden'}.**")
    (RESULTS_DIR / "v_holdout.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
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
