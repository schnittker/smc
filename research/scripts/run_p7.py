#!/usr/bin/env python3
"""P7 Model H (trend following on indices and commodities): in-sample run T16 with the pre-registered
acceptance check and - only if it passed - the one-time hold-out run T17
(docs/12_P7_Vorregistrierung_ModellH.md). Same evaluation as run_p6.py.

Usage:
  research/.venv/bin/python -I research/scripts/run_p7.py              # T16, in-sample 2015-2023
  research/.venv/bin/python -I research/scripts/run_p7.py --holdout    # T17, once
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

from smc import timez  # noqa: E402
from smc.config import DATA_DIR, PROJECT_ROOT  # noqa: E402
from smc.data.bars import load_bars  # noqa: E402
from smc.report import cluster_bootstrap_ci, cluster_t  # noqa: E402
from smc.strategy_g import ANNUAL  # noqa: E402
from smc.strategy_h import SYMBOLS_H, run_model_h  # noqa: E402
from smc.swaps import RateTable  # noqa: E402

IS_FROM, IS_TO = timegm((2015, 1, 1, 0, 0, 0)) // timez.DAY, timegm((2024, 1, 1, 0, 0, 0)) // timez.DAY
HO_FROM = IS_TO
IS_YEARS, HO_YEARS = range(2015, 2024), range(2024, 2027)
# ETXEUR (Euro Stoxx 50) is left out: HistData offers no file for 2020 (empty download token), found
# before the first run and recorded in docs/12, section 7.
SYMBOLS = tuple(s for s in SYMBOLS_H if s != "ETXEUR")
OUT_DIR = DATA_DIR / "p7"
RESULTS = PROJECT_ROOT / "research" / "results"


def run_symbol(job):
    symbol, day_to = job
    rows = run_model_h(symbol, load_bars(symbol, "M5"), RateTable.load(), day_to=day_to)
    return rows


def run(phase: str) -> dict:
    day_to = IS_TO if phase == "is" else None
    with ProcessPoolExecutor(6) as ex:
        parts = list(ex.map(run_symbol, [(s, day_to) for s in SYMBOLS]))
    rows = np.concatenate(parts)
    lo, hi = (IS_FROM, IS_TO) if phase == "is" else (HO_FROM, 10**9)
    rows = rows[(rows["day"] >= lo) & (rows["day"] < hi)]
    (OUT_DIR / phase).mkdir(parents=True, exist_ok=True)
    pq.write_table(pa.table({n: rows[n] for n in rows.dtype.names}), OUT_DIR / phase / "rows.parquet",
                   compression="zstd")
    return {n: rows[n] for n in rows.dtype.names}


def load(phase: str) -> dict:
    t = pq.read_table(OUT_DIR / phase / "rows.parquet")
    return {n: t.column(n).to_numpy(zero_copy_only=False) for n in t.column_names}


def year_of_day(days):
    return np.asarray(days * timez.DAY, dtype="datetime64[s]").astype("datetime64[Y]").astype(int) + 1970


def month_of_day(days):
    return np.asarray(days * timez.DAY, dtype="datetime64[s]").astype("datetime64[M]").astype(np.int64)


def stats(rows: dict, years) -> dict:
    days, inv = np.unique(rows["day"], return_inverse=True)
    net = np.bincount(inv, rows["net"])
    cost = np.bincount(inv, rows["cost"])
    n = len(net)
    sd = net.std(ddof=1)
    scale = 0.10 / (sd * np.sqrt(ANNUAL))                 # portfolio at 10 % volatility p. a.
    equity = np.cumsum(net * scale)
    m = {"days": n, "E": float(net.mean()), "sd": float(sd), "E_2x": float((net - cost).mean()),
         "t_iid": float(net.mean() / (sd / np.sqrt(n))), "t_week": cluster_t(net, (days + 3) // 7),
         "t_month": cluster_t(net, month_of_day(days)), "sharpe": float(net.mean() / sd * np.sqrt(ANNUAL)),
         "ret10": float(net.mean() * scale * ANNUAL), "maxdd10": float((np.maximum.accumulate(equity) - equity).max()),
         "cost_share": float(cost.sum() / max(1e-12, np.abs(rows["pnl"]).sum())),
         "swap10": float(rows["swap"].sum() * scale / (n / ANNUAL)),
         "trade10": float(rows["trade_cost"].sum() * scale / (n / ANNUAL)),
         "fee10": float(rows["fee"].sum() * scale / (n / ANNUAL)),
         "gross_exposure": float(np.bincount(inv, np.abs(rows["w"])).mean()), "scale": scale,
         "days_arr": days, "net_arr": net}
    m["t"] = min(m["t_iid"], m["t_week"], m["t_month"])
    yr = year_of_day(days)
    m["by_year"] = {y: (float(net[yr == y].sum() * scale), float(net[yr == y].mean() / net[yr == y].std(ddof=1) *
                        np.sqrt(ANNUAL)) if (yr == y).sum() > 2 else np.nan) for y in years}
    m["years_pos"] = sum(1 for tot, _ in m["by_year"].values() if tot > 0)
    m["by_symbol"] = {}
    for s in SYMBOLS:
        sel = rows["symbol"] == s
        if sel.any():
            x = rows["net"][sel]
            m["by_symbol"][s] = (float(x.sum() * scale), float(x.mean() / x.std(ddof=1) * np.sqrt(ANNUAL)))
    m["sym_pos"] = sum(1 for tot, _ in m["by_symbol"].values() if tot > 0)
    return m


def checks_is(m: dict, years) -> list:
    n_sym = len(m["by_symbol"])
    return [("Mittleres Netto-Tagesergebnis > 0 mit t ≥ 3,0 (kleinster aus iid / Woche / Monat)",
             f"t = {m['t']:.2f} (Sharpe {m['sharpe']:.2f})", m["E"] > 0 and m["t"] >= 3.0),
            (f"≥ 6 von {len(years)} Jahren positiv", f"{m['years_pos']} von {len(years)}", m["years_pos"] >= 6),
            ("≥ 60 % der Instrumente positiv", f"{m['sym_pos']} von {n_sym}", m["sym_pos"] >= 0.6 * n_sym),
            ("bei doppelten Kosten > 0", f"{m['E_2x'] * m['scale'] * ANNUAL:+.2%} p. a. bei 10 % Vol.", m["E_2x"] > 0)]


def report(title: str, intro: str, m: dict, checks: list, verdict: str) -> list[str]:
    out = [f"# {title}\n", intro + "\n", "| Kennzahl | Wert |", "|---|---|",
           f"| Handelstage | {m['days']:,} |",
           f"| Sharpe Ratio p. a. (netto) | {m['sharpe']:.2f} |",
           f"| t-Wert iid / Woche / Monat | {m['t_iid']:.2f} / {m['t_week']:.2f} / {m['t_month']:.2f} |",
           f"| Rendite p. a. bei 10 % Volatilität | {m['ret10']:+.2%} |",
           f"| Max. Drawdown bei 10 % Volatilität | {m['maxdd10']:.1%} |",
           f"| Kosten p. a. bei 10 % Vol.: Handel / Swaps (+ = Gutschrift) / 0,7-%-Gebühr | "
           f"{m['trade10']:.2%} / {m['swap10']:+.2%} / {m['fee10']:.2%} |",
           f"| Ø Brutto-Exposure (Summe \\|w\\|, unskaliert) | {m['gross_exposure']:.1f} |", "",
           "| Kriterium | Ergebnis | erfüllt |", "|---|---|---|"]
    out += [f"| {c} | {v} | {'ja' if ok else '**nein**'} |" for c, v, ok in checks]
    out += ["", verdict + "\n", "| Jahr | Rendite bei 10 % Vol. | Sharpe |", "|---|---|---|"]
    out += [f"| {y} | {tot:+.1%} | {sr:+.2f} |" for y, (tot, sr) in m["by_year"].items()]
    out += ["", "| Instrument | Beitrag bei 10 % Portfolio-Vol. (Summe) | Sharpe einzeln |", "|---|---|---|"]
    out += [f"| {s} | {tot:+.1%} | {sr:+.2f} |" for s, (tot, sr) in sorted(m["by_symbol"].items(), key=lambda kv: -kv[1][0])]
    return out + [""]


def in_sample():
    rows = run("is")
    m = stats(rows, IS_YEARS)
    checks = checks_is(m, IS_YEARS)
    passed = all(ok for _, _, ok in checks)
    verdict = ("**Modell H In-Sample: alle Kriterien erfüllt – der Hold-out (T17) ist freigegeben.**" if passed else
               "**Modell H In-Sample: nicht bestanden. P7 ist gescheitert; der Hold-out bleibt unberührt.**")
    intro = (f"Lauf vom {date.today():%d.%m.%Y}. Regeln laut `docs/12_P7_Vorregistrierung_ModellH.md`, Code "
             "`research/smc/strategy_h.py` und `strategy_g.run_trend`. Handelstage 01.01.2015–31.12.2023 "
             f"(Warm-up 2014), {len(SYMBOLS)} Instrumente (ohne ETXEUR, Datenlücke 2020). "
             "Netto = nach Handelskosten, Swaps und 0,7-%-Gebühr. Renditen und Drawdown sind auf eine "
             "Portfolio-Volatilität von 10 % p. a. skaliert (Kalibrierung auf diesen Zeitraum, nur zur Einordnung).")
    lines = report("P7 – Modell H (Trendfolge Indizes und Rohstoffe), In-Sample 2015–2023 (Trial T16)", intro, m,
                   checks, verdict)
    (RESULTS / "p7_modell_h_in_sample.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))


def holdout():
    marker = OUT_DIR / "ho" / "DONE"
    if marker.exists():
        sys.exit("Hold-out wurde bereits ausgewertet (data/p7/ho/DONE) – kein zweiter Lauf.")
    m_is = stats(load("is"), IS_YEARS)
    if not all(ok for _, _, ok in checks_is(m_is, IS_YEARS)):
        sys.exit("Modell H hat die In-Sample-Kriterien nicht erfüllt – kein Hold-out.")
    marker.parent.mkdir(parents=True, exist_ok=True)
    marker.write_text(f"T17 {date.today().isoformat()}\n")
    m = stats(run("ho"), HO_YEARS)
    lo, hi = cluster_bootstrap_ci(m_is["net_arr"], month_of_day(m_is["days_arr"]))
    checks = [("Mittleres Netto-Tagesergebnis > 0", f"Sharpe {m['sharpe']:.2f}", m["E"] > 0),
              ("≥ untere 95-%-Grenze von In-Sample (Cluster nach Monat)",
               f"{m['E'] * 1e4:+.3f} vs. IS {m_is['E'] * 1e4:+.3f} [{lo * 1e4:+.3f}; {hi * 1e4:+.3f}] bp/Tag unskaliert",
               m["E"] >= lo)]
    passed = all(ok for _, _, ok in checks)
    verdict = f"**Hold-out {'bestanden – weiter mit T18 (FTMO)' if passed else 'nicht bestanden. P7 ist gescheitert'}.**"
    lines = report("P7 – Modell H, Hold-out 2024–2026 (Trial T17)", f"Einmaliger Lauf vom {date.today():%d.%m.%Y}.",
                   m, checks, verdict)
    (RESULTS / "p7_modell_h_holdout.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--holdout", action="store_true")
    args = ap.parse_args()
    if args.holdout:
        holdout()
    else:
        in_sample()


if __name__ == "__main__":
    main()
