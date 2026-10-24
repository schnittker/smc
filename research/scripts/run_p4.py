#!/usr/bin/env python3
"""P4 Model D: in-sample run T6 with the pre-registered acceptance check and - only if it passed -
the one-time hold-out run T7 (docs/06_P4_Vorregistrierung_ModellD.md).

Usage:
  research/.venv/bin/python -I research/scripts/run_p4.py              # T6, in-sample 2015-2023
  research/.venv/bin/python -I research/scripts/run_p4.py --holdout    # T7, once
Needs data/derived (run_event_study.py) and data/raw/rates (download_rates.py).
"""
import argparse
import sys
import time
from calendar import timegm
from concurrent.futures import ProcessPoolExecutor
from datetime import date
from pathlib import Path

import numpy as np
import pyarrow as pa
import pyarrow.parquet as pq

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from smc.config import DATA_DIR, PROJECT_ROOT, SYMBOLS  # noqa: E402
from smc.evaluation import holdout_checks, in_sample_checks, trade_stats  # noqa: E402
from smc.strategy_c import STATUS_NAMES, TRADED, Inputs  # noqa: E402
from smc.strategy_d import EXIT_SL, EXIT_STRUCT, EXIT_TIME, run_model_d  # noqa: E402
from smc.swaps import RateTable  # noqa: E402

IS_FROM, IS_TO = timegm((2015, 1, 1, 0, 0, 0)), timegm((2024, 1, 1, 0, 0, 0))
HO_FROM, HO_TO = IS_TO, timegm((2100, 1, 1, 0, 0, 0))
IS_YEARS, HO_YEARS = range(2015, 2024), range(2024, 2027)
OUT_DIR = DATA_DIR / "p4"
RESULTS = PROJECT_ROOT / "research" / "results"
STATUS_DE = {"traded": "gehandelt", "blocked": "blockiert (Position offen)", "bad_risk": "Stop schon erreicht",
             "cost_gate": "Kosten-Gate (> 0,10 R)", "no_data": "Datenende"}


def run_symbol(job) -> str:
    symbol, phase = job
    t0 = time.time()
    t_from, t_to = (IS_FROM, IS_TO) if phase == "is" else (HO_FROM, HO_TO)
    rows = run_model_d(Inputs.load(symbol), t_from, t_to, RateTable.load())
    out = OUT_DIR / phase
    out.mkdir(parents=True, exist_ok=True)
    pq.write_table(pa.table({n: rows[n] for n in rows.dtype.names}), out / f"{symbol}.parquet", compression="zstd")
    return f"{symbol}: {len(rows)} signals, {int((rows['status'] == TRADED).sum())} trades, {time.time() - t0:.0f}s"


def run_all(phase: str, symbols, workers: int) -> dict:
    with ProcessPoolExecutor(workers) as ex:
        for msg in ex.map(run_symbol, [(s, phase) for s in symbols]):
            print(msg, flush=True)
    return load(phase, symbols)


def load(phase: str, symbols) -> dict:
    t = pa.concat_tables([pq.read_table(OUT_DIR / phase / f"{s}.parquet") for s in symbols])
    return {n: t.column(n).to_numpy(zero_copy_only=False) for n in t.column_names}


def take(data: dict, mask: np.ndarray) -> dict:
    return {k: v[mask] for k, v in data.items()}


def status_lines(rows: dict) -> list[str]:
    out = ["| Status | Anzahl |", "|---|---|"]
    for code, name in STATUS_NAMES.items():
        k = int((rows["status"] == code).sum())
        if k:
            out.append(f"| {STATUS_DE.get(name, name)} | {k:,} |")
    return out


def summary_lines(tr: dict, m: dict) -> list[str]:
    x, ex = tr["net_r"], tr["exit_reason"]
    hold = (tr["i_end"] - tr["i_fill"]) / 288
    wins, losses = x[x > 0], x[x <= 0]
    t_cl = " / ".join(f"{v:.2f}" for v in m["t_cl"].values())
    lines = ["| Kennzahl | Wert |", "|---|---|",
             f"| Trades | {m['n']:,} |",
             f"| Netto-Erwartungswert | {m['E']:+.3f} R (σ {m['sd']:.2f}) |",
             f"| t-Wert iid / Tag / Woche / Monat | {m['t_iid']:.2f} / {t_cl} |",
             f"| Profit-Factor netto | {m['pf']:.2f} |",
             f"| Trefferquote | {m['win']:.1%} |",
             f"| Ø Gewinner / Ø Verlierer | {wins.mean():+.2f} R / {losses.mean():+.2f} R |",
             f"| größter Gewinner, P90 der Gewinner | {wins.max():+.2f} R, {np.percentile(wins, 90):+.2f} R |",
             f"| Ø Kosten gesamt (Spread, Kommission, Slippage, Gebühr, belastende Swaps) | {m['cost']:.3f} R |",
             f"| davon Ø Swap (+ = Gutschrift) / Ø 0,7-%-Gebühr | {tr['swap_r'].mean():+.3f} R / {tr['fee_r'].mean():.3f} R |",
             f"| bei doppelten Kosten | {m['E_2x']:+.3f} R |",
             f"| Haltedauer Median / Mittel | {np.median(hold):.1f} / {hold.mean():.1f} Handelstage |", ""]
    for code, name in ((EXIT_STRUCT, "Struktur-Exit"), (EXIT_SL, "Stop"), (EXIT_TIME, "Zeit-Stopp")):
        sel = ex == code
        if sel.any():
            lines.append(f"- {name}: {sel.mean():.0%} der Trades, Ø {x[sel].mean():+.3f} R")
    lines.append(f"- Long {np.sum(tr['dir'] == 1)} Trades Ø {x[tr['dir'] == 1].mean():+.3f} R; "
                 f"Short {np.sum(tr['dir'] == -1)} Trades Ø {x[tr['dir'] == -1].mean():+.3f} R")
    return lines + [""]


def table_lines(m: dict) -> list[str]:
    out = ["| Jahr | Trades | Netto Ø R |", "|---|---|---|"]
    out += [f"| {y} | {k} | {e:+.3f} |" for y, (k, e) in m["by_year"].items()]
    out += ["", "| Instrument | Trades | Netto Ø R |", "|---|---|---|"]
    out += [f"| {s} | {k} | {e:+.3f} |" for s, (k, e) in sorted(m["by_symbol"].items(), key=lambda kv: -kv[1][1])]
    return out + [""]


def check_lines(checks) -> list[str]:
    out = ["| Kriterium | Ergebnis | erfüllt |", "|---|---|---|"]
    return out + [f"| {c} | {v} | {'ja' if ok else '**nein**'} |" for c, v, ok in checks] + [""]


def in_sample(symbols, workers):
    rows = run_all("is", symbols, workers)
    tr = take(rows, rows["status"] == TRADED)
    m = trade_stats(tr, IS_YEARS)
    checks = in_sample_checks(m, IS_YEARS)
    passed = all(ok for _, _, ok in checks)
    lines = ["# P4 – Modell D, In-Sample 2015–2023 (Trial T6)\n",
             f"Lauf vom {date.today():%d.%m.%Y}. Regeln laut `docs/06_P4_Vorregistrierung_ModellD.md`, Code "
             "`research/smc/strategy_d.py`. Signale 01.01.2015–31.12.2023, 25 Instrumente, HistData-M1 (Bid). "
             "Netto = nach Spread (Ask/Bid-Fills), Kommission, Slippage, Swaps (Zinsdifferenz − 1 % p. a.) "
             "und 0,7-%-Umrechnungsgebühr.\n",
             f"{len(rows['status']):,} Signale (strikter H1-Wechsel in Richtung des strikten H4-Trends).\n"]
    lines += status_lines(rows) + [""] + summary_lines(tr, m) + check_lines(checks)
    lines.append(f"**Modell D In-Sample: {'alle Kriterien erfüllt – der Hold-out (T7) ist freigegeben' if passed else 'nicht bestanden. P4 ist gescheitert; der Hold-out bleibt unberührt'}.**\n")
    lines += table_lines(m)
    (RESULTS / "p4_modell_d_in_sample.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))


def holdout(symbols, workers):
    marker = OUT_DIR / "ho" / "DONE"
    if marker.exists():
        sys.exit("Hold-out wurde bereits ausgewertet (data/p4/ho/DONE) – kein zweiter Lauf.")
    is_rows = load("is", symbols)
    is_tr = take(is_rows, is_rows["status"] == TRADED)
    m_is = trade_stats(is_tr, IS_YEARS)
    if not all(ok for _, _, ok in in_sample_checks(m_is, IS_YEARS)):
        sys.exit("Modell D hat die In-Sample-Kriterien nicht erfüllt – kein Hold-out.")
    marker.parent.mkdir(parents=True, exist_ok=True)
    marker.write_text(f"T7 {date.today().isoformat()}\n")
    rows = run_all("ho", symbols, workers)
    tr = take(rows, rows["status"] == TRADED)
    m = trade_stats(tr, HO_YEARS)
    checks, _ = holdout_checks(m, is_tr, m_is)
    passed = all(ok for _, _, ok in checks)
    lines = ["# P4 – Modell D, Hold-out 2024–2026 (Trial T7)\n",
             f"Einmaliger Lauf vom {date.today():%d.%m.%Y}. Signale ab 01.01.2024 bis Datenende 16.10.2026.\n"]
    lines += status_lines(rows) + [""] + summary_lines(tr, m) + check_lines(checks)
    lines.append(f"**Hold-out {'bestanden – weiter mit T8 (Portfolio und FTMO)' if passed else 'nicht bestanden. P4 ist gescheitert'}.**\n")
    lines += table_lines(m)
    (RESULTS / "p4_modell_d_holdout.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--symbols", default=",".join(SYMBOLS))
    ap.add_argument("--workers", type=int, default=6)
    ap.add_argument("--holdout", action="store_true")
    args = ap.parse_args()
    symbols = args.symbols.split(",")
    if args.holdout:
        holdout(symbols, args.workers)
    else:
        in_sample(symbols, args.workers)


if __name__ == "__main__":
    main()
