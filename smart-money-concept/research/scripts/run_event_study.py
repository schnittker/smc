#!/usr/bin/env python3
"""Gate P2 event study over all symbols (in-sample window only; 2024+ stays untouched).

Usage: research/.venv/bin/python -I research/scripts/run_event_study.py [--symbols ...] [--workers 6]
"""
import argparse
import sys
import time
from calendar import timegm
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

import numpy as np
import pyarrow as pa
import pyarrow.parquet as pq

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from smc.config import DATA_DIR, PROJECT_ROOT, SYMBOLS  # noqa: E402
from smc.costs import cost_in_price  # noqa: E402
from smc.pipeline import build_symbol, save  # noqa: E402
from smc.report import clustered_diff, holm  # noqa: E402
from smc.study import EventStudy  # noqa: E402

T_FROM = timegm((2015, 1, 1, 0, 0, 0))
T_TO = timegm((2024, 1, 1, 0, 0, 0))   # hold-out 2024-2026 is not touched here
STUDY_DIR = DATA_DIR / "study"


def run_symbol(symbol: str) -> str:
    t0 = time.time()
    feats = build_symbol(symbol)
    save(feats)
    rows = EventStudy(feats, T_FROM, T_TO, seed=hash(symbol) % 2**32).run_all()
    price = feats.tf["M5"].bars["o"][rows["i"]]
    cost = np.array([cost_in_price(symbol, p) for p in price])
    STUDY_DIR.mkdir(parents=True, exist_ok=True)
    cols = {name: rows[name] for name in rows.dtype.names}
    cols["cost_r"] = cost / rows["unit"]
    cols["cost_r_h1"] = cost / rows["unit_h1"]
    pq.write_table(pa.table(cols), STUDY_DIR / f"{symbol}.parquet", compression="zstd")
    return f"{symbol}: {int((~rows['placebo']).sum()):,} events, {int(rows['placebo'].sum()):,} placebos, {time.time() - t0:.0f}s"


def load_all(symbols):
    tables = [pq.read_table(STUDY_DIR / f"{s}.parquet") for s in symbols if (STUDY_DIR / f"{s}.parquet").exists()]
    t = pa.concat_tables(tables)
    return {name: t.column(name).to_numpy(zero_copy_only=False) for name in t.column_names}


def summarize(data, out_path: Path):
    et, pb, d = data["etype"], data["placebo"], data["dir"]
    day = data["day"]
    groups = [("alle", lambda m: m),
              ("H4-Trend gleichgerichtet", lambda m: m & (data["trend_h4"] == d)),
              ("H4-Trend gegenläufig", lambda m: m & (data["trend_h4"] == -d)),
              ("London-KZ 02-05 NY", lambda m: m & (data["session"] == "ldn_kz")),
              ("NY-KZ 07-10 NY", lambda m: m & (data["session"] == "ny_kz"))]
    results = []
    for etype in sorted(set(et.tolist())):
        base = et == etype
        for gname, gf in groups:
            m = gf(base)
            ev, pl = m & ~pb, m & pb
            if ev.sum() < 50:
                continue
            row = dict(etype=etype, group=gname, n=int(ev.sum()))
            for tag, col, cost_col in (("m15", "r21", "cost_r"), ("h1", "r21_h1", "cost_r_h1")):
                diff, lo, hi, p = clustered_diff(data[col][ev], day[ev], data[col][pl], day[pl])
                mean_ev = float(np.nanmean(data[col][ev]))
                cost = float(np.nanmedian(data[cost_col][ev]))
                row.update({f"{tag}_ev": mean_ev, f"{tag}_diff": diff, f"{tag}_lo": lo, f"{tag}_hi": hi,
                            f"{tag}_p": p, f"{tag}_cost": cost, f"{tag}_net": mean_ev - cost})
            results.append(row)
    for tag in ("m15", "h1"):
        for r, a in zip(results, holm([r[f"{tag}_p"] for r in results])):
            r[f"{tag}_ph"] = a

    def star(p):
        return " **" if np.isfinite(p) and p < 0.05 else ""

    lines = ["# Ereignisstudie (Gate P2) – In-Sample 2015–2023, 25 Instrumente\n",
             "Markteinstieg zur Eröffnung der ersten M5-Kerze nach dem Ereignis, in Richtung der Hypothese. "
             "**R(2:1)** = Ziel +2 Einheiten, Stop −1 Einheit; gleiche Kerze → Verlust; Timeout → Marktwert. "
             "Einheit **M15** = ATR14(M15), Horizont 24 h; Einheit **H1** = ATR14(H1), Horizont 3 Handelstage. "
             "Placebo = zufällige M5-Kerzen gleicher NY-Stunde und gleichen ATR(M15)-Dezils, gleiche Richtung (3 je Ereignis). "
             "Δ = Ereignis − Placebo mit 95-%-Bootstrap-KI (Cluster = Handelstag über alle Symbole); "
             "p(Holm) je Einheit über alle Zeilen; ** = p(Holm) < 0,05. "
             "Kosten = FTMO-All-in-Kosten / Einheit (Median, ohne 0,7-%-Abschlag); netto = Ereignis-R − Kosten.\n",
             "| Baustein | Gruppe | n | Δ R M15 [95-%-KI] | p Holm | netto M15 | Δ R H1 [95-%-KI] | p Holm | R H1 Ereignis | Kosten H1 | netto H1 |",
             "|---|---|---|---|---|---|---|---|---|---|---|"]
    for r in results:
        lines.append(
            f"| {r['etype']} | {r['group']} | {r['n']:,} | "
            f"{r['m15_diff']:+.3f} [{r['m15_lo']:+.3f}; {r['m15_hi']:+.3f}] | {r['m15_ph']:.2g}{star(r['m15_ph'])} | "
            f"{r['m15_net']:+.3f} | "
            f"{r['h1_diff']:+.3f} [{r['h1_lo']:+.3f}; {r['h1_hi']:+.3f}] | {r['h1_ph']:.2g}{star(r['h1_ph'])} | "
            f"{r['h1_ev']:+.3f} | {r['h1_cost']:.3f} | {r['h1_net']:+.3f} |")
    out_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return lines


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--symbols", default=",".join(SYMBOLS))
    ap.add_argument("--workers", type=int, default=6)
    ap.add_argument("--summary-only", action="store_true")
    args = ap.parse_args()
    symbols = args.symbols.split(",")
    if not args.summary_only:
        with ProcessPoolExecutor(args.workers) as ex:
            for msg in ex.map(run_symbol, symbols):
                print(msg, flush=True)
    lines = summarize(load_all(symbols), PROJECT_ROOT / "research" / "results" / "event_study_p2.md")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
