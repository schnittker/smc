#!/usr/bin/env python3
"""P3 Model C: in-sample runs T2 (C-MKT) and T3 (C-LMT) with the pre-registered acceptance check,
and - only for a variant that passed in-sample - the one-time hold-out run T4.

Usage:
  research/.venv/bin/python -I research/scripts/run_p3.py                    # T2 + T3, in-sample 2015-2023
  research/.venv/bin/python -I research/scripts/run_p3.py --holdout C-MKT    # T4, once, chosen variant only
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

from smc import timez  # noqa: E402
from smc.config import DATA_DIR, PROJECT_ROOT, SYMBOLS  # noqa: E402
from smc.engine.liquidity import KIND_NAMES  # noqa: E402
from smc.report import cluster_bootstrap_ci, cluster_t, profit_factor  # noqa: E402
from smc.strategy_c import (ENTRY_FVG, ENTRY_OB, EXIT_SL, EXIT_TIME, EXIT_TP, LMT, MKT, STATUS_NAMES,  # noqa: E402
                            TARGET_CAP, TARGET_MIN, TRADED, Inputs, run_model_c)

IS_FROM, IS_TO = timegm((2015, 1, 1, 0, 0, 0)), timegm((2024, 1, 1, 0, 0, 0))
HO_FROM, HO_TO = IS_TO, timegm((2100, 1, 1, 0, 0, 0))
IS_YEARS = range(2015, 2024)
OUT_DIR = DATA_DIR / "p3"
RESULTS = PROJECT_ROOT / "research" / "results"

STATUS_DE = {"traded": "gehandelt", "blocked": "blockiert (Position/Order offen)", "no_zone": "keine Zone",
             "bad_risk": "Stop schon erreicht / Risiko ≤ 0", "cost_gate": "Kosten-Gate (> 0,10 R)",
             "cancel_trend": "Storno: H4-Trend gedreht", "cancel_stop": "Storno: Stop-Level erreicht",
             "cancel_target": "Storno: Ziel erreicht", "expired": "abgelaufen (288 Bars)", "no_data": "Datenende"}


def run_symbol(job) -> str:
    symbol, phase, variants = job
    t0 = time.time()
    inp = Inputs.load(symbol)
    t_from, t_to = (IS_FROM, IS_TO) if phase == "is" else (HO_FROM, HO_TO)
    rows = np.concatenate([run_model_c(inp, v, t_from, t_to) for v in variants])
    out = OUT_DIR / phase
    out.mkdir(parents=True, exist_ok=True)
    pq.write_table(pa.table({n: rows[n] for n in rows.dtype.names}), out / f"{symbol}.parquet", compression="zstd")
    n_tr = int((rows["status"] == TRADED).sum())
    return f"{symbol}: {len(rows)} signals, {n_tr} trades, {time.time() - t0:.0f}s"


def load(phase: str, symbols) -> dict:
    t = pa.concat_tables([pq.read_table(OUT_DIR / phase / f"{s}.parquet") for s in symbols])
    return {n: t.column(n).to_numpy(zero_copy_only=False) for n in t.column_names}


def take(data: dict, mask: np.ndarray) -> dict:
    return {k: v[mask] for k, v in data.items()}


def years_of(t: np.ndarray) -> np.ndarray:
    return np.asarray(t, dtype="datetime64[s]").astype("datetime64[Y]").astype(int) + 1970


def metrics(tr: dict, years=IS_YEARS) -> dict:
    x, cost = tr["net_r"], tr["cost_r"]
    n = len(x)
    day = timez.ftmo_day(tr["t_fill"])
    week = (day + 3) // 7
    m = {"n": n, "E": float(x.mean()), "sd": float(x.std(ddof=1)), "cost": float(cost.mean()),
         "E_gross": float((x + cost).mean()), "E_2x": float((x - cost).mean()), "pf": profit_factor(x),
         "win": float((x > 0).mean()), "t_iid": float(x.mean() / (x.std(ddof=1) / np.sqrt(n))),
         "t_day": cluster_t(x, day), "t_week": cluster_t(x, week)}
    m["t"] = min(m["t_iid"], m["t_day"], m["t_week"])
    yr = years_of(tr["t_sig"])
    m["by_year"] = {y: (int((yr == y).sum()), float(x[yr == y].mean()) if (yr == y).any() else np.nan) for y in years}
    m["years_pos"] = sum(1 for y in years if m["by_year"][y][0] and m["by_year"][y][1] > 0)
    m["by_symbol"] = {s: (int((tr["symbol"] == s).sum()), float(x[tr["symbol"] == s].mean()))
                      for s in SYMBOLS if (tr["symbol"] == s).any()}
    elig = [v for v in m["by_symbol"].values() if v[0] >= 10]
    m["sym_eligible"] = len(elig)
    m["sym_pos"] = sum(1 for v in elig if v[1] > 0)
    m["sym_share"] = m["sym_pos"] / len(elig) if elig else np.nan
    m["checks"] = [
        ("Netto-Erwartungswert ≥ +0,10 R", f"{m['E']:+.3f} R", m["E"] >= 0.10),
        ("t-Wert ≥ 2,5 (kleinster aus iid / Tag / Woche)", f"{m['t']:.2f}", m["t"] >= 2.5),
        ("Netto-Profit-Factor ≥ 1,2", f"{m['pf']:.2f}", m["pf"] >= 1.2),
        ("≥ 6 von 9 Jahren positiv", f"{m['years_pos']} von {len(years)}", m["years_pos"] >= 6),
        ("≥ 60 % der Instrumente (≥ 10 Trades) positiv",
         f"{m['sym_pos']} von {m['sym_eligible']} ({m['sym_share']:.0%})", m["sym_share"] >= 0.6),
        ("bei doppelten Kosten > 0", f"{m['E_2x']:+.3f} R", m["E_2x"] > 0),
    ]
    m["passed"] = all(ok for _, _, ok in m["checks"])
    return m


def describe(tr: dict) -> list[str]:
    """Exit reasons, target types, entries, holding time, long/short split."""
    x = tr["net_r"]
    ex = tr["exit_reason"]
    hold_h = (tr["t_end"] - tr["t_fill"]) / 3600
    tk = tr["tp_kind"]
    tp_names = {TARGET_MIN: "2 R (kein Pool)", TARGET_CAP: "4 R (Deckel)", **KIND_NAMES}
    lines = [f"- Ausstieg: Ziel {np.mean(ex == EXIT_TP):.0%}, Stop {np.mean(ex == EXIT_SL):.0%}, "
             f"Zeit-Stopp {np.mean(ex == EXIT_TIME):.0%} (Ø {x[ex == EXIT_TIME].mean() if (ex == EXIT_TIME).any() else np.nan:+.2f} R)",
             f"- Ziel-Abstand Ø {tr['tp_r'].mean():.2f} R; Ziel-Typ: "
             + ", ".join(f"{tp_names[int(k)]} {np.mean(tk == k):.0%}" for k in sorted(set(tk.tolist()))),
             f"- Haltedauer Median {np.median(hold_h):.1f} h; Kosten Median {np.median(tr['cost_r']):.3f} R",
             f"- Long {np.sum(tr['dir'] == 1)} Trades Ø {x[tr['dir'] == 1].mean():+.3f} R; "
             f"Short {np.sum(tr['dir'] == -1)} Trades Ø {x[tr['dir'] == -1].mean():+.3f} R"]
    ek = tr["entry_kind"]
    if (ek != 0).any():
        lines.append(f"- Einstieg: FVG-CE {np.sum(ek == ENTRY_FVG)} Trades Ø {x[ek == ENTRY_FVG].mean():+.3f} R; "
                     f"OB-MT {np.sum(ek == ENTRY_OB)} Trades Ø {x[ek == ENTRY_OB].mean():+.3f} R")
    return lines


def status_table(rows: dict) -> list[str]:
    st = rows["status"]
    out = ["| Status | Anzahl |", "|---|---|"]
    for code, name in STATUS_NAMES.items():
        k = int((st == code).sum())
        if k:
            out.append(f"| {STATUS_DE[name]} | {k:,} |")
    return out


def variant_section(name: str, rows: dict, m: dict) -> list[str]:
    tr = take(rows, rows["status"] == TRADED)
    out = [f"## {name}\n", f"{len(rows['status']):,} Signale (strikter H1-Wechsel in Richtung des strikten H4-Trends).\n"]
    out += status_table(rows) + [""]
    out += ["| Kennzahl | Wert |", "|---|---|",
            f"| Trades | {m['n']:,} |",
            f"| Netto-Erwartungswert | {m['E']:+.3f} R (σ {m['sd']:.2f}) |",
            f"| vor Kosten (netto + Kosten) | {m['E_gross']:+.3f} R |",
            f"| Ø Kosten (Spread, Kommission, Slippage) | {m['cost']:.3f} R |",
            f"| t-Wert iid / Tages-Cluster / Wochen-Cluster | {m['t_iid']:.2f} / {m['t_day']:.2f} / {m['t_week']:.2f} |",
            f"| Profit-Factor netto | {m['pf']:.2f} |",
            f"| Trefferquote | {m['win']:.1%} |",
            f"| bei doppelten Kosten | {m['E_2x']:+.3f} R |", ""]
    out += describe(tr) + [""]
    out += ["| Kriterium | Ergebnis | erfüllt |", "|---|---|---|"]
    out += [f"| {c} | {v} | {'ja' if ok else '**nein**'} |" for c, v, ok in m["checks"]]
    out += ["", f"**{name}: {'alle Kriterien erfüllt' if m['passed'] else 'nicht bestanden'}.**\n",
            "| Jahr | Trades | Netto Ø R |", "|---|---|---|"]
    out += [f"| {y} | {k} | {e:+.3f} |" for y, (k, e) in m["by_year"].items()]
    out += ["", "| Instrument | Trades | Netto Ø R |", "|---|---|---|"]
    out += [f"| {s} | {k} | {e:+.3f} |" for s, (k, e) in sorted(m["by_symbol"].items(), key=lambda kv: -kv[1][1])]
    return out + [""]


def in_sample(symbols, workers):
    with ProcessPoolExecutor(workers) as ex:
        for msg in ex.map(run_symbol, [(s, "is", (MKT, LMT)) for s in symbols]):
            print(msg, flush=True)
    data = load("is", symbols)
    lines = ["# P3 – Modell C, In-Sample 2015–2023 (Trial T2 C-MKT, T3 C-LMT)\n",
             f"Lauf vom {date.today():%d.%m.%Y}, Regeln laut `docs/04_P3_Vorregistrierung_ModellC.md`, Code "
             "`research/smc/strategy_c.py`. Signale 01.01.2015–31.12.2023, alle 25 Instrumente, HistData-M1 (Bid). "
             "Netto = nach Spread (über Ask/Bid-Fills), FTMO-Kommission und Slippage; ohne 0,7-%-Umrechnungsgebühr. "
             "Der t-Wert für das Kriterium ist der kleinste aus iid, Cluster nach FTMO-Tag und Cluster nach Woche "
             "(Einstiegstag).\n"]
    verdict = {}
    for v in (MKT, LMT):
        rows = take(data, data["variant"] == v)
        m = metrics(take(rows, rows["status"] == TRADED))
        verdict[v] = m
        lines += variant_section(v, rows, m)
    passed = [v for v in (MKT, LMT) if verdict[v]["passed"]]
    if passed:
        best = max(passed, key=lambda v: verdict[v]["t"])
        lines.append(f"**Ergebnis:** {', '.join(passed)} bestanden; gewählt für den Hold-out: **{best}** (höherer t-Wert).")
    else:
        lines.append("**Ergebnis: Keine Variante erfüllt alle In-Sample-Kriterien. P3 ist gescheitert; "
                     "der Hold-out bleibt unberührt.**")
    path = RESULTS / "p3_modell_c_in_sample.md"
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))


def holdout(variant, symbols, workers):
    """T4: run once. Compares with the stored in-sample trades of the same variant."""
    marker = OUT_DIR / "ho" / "DONE"
    if marker.exists():
        sys.exit("Hold-out wurde bereits ausgewertet (data/p3/ho/DONE) – kein zweiter Lauf.")
    is_data = load("is", symbols)
    is_tr = take(is_data, (is_data["variant"] == variant) & (is_data["status"] == TRADED))
    m_is = metrics(is_tr)
    if not m_is["passed"]:
        sys.exit(f"{variant} hat die In-Sample-Kriterien nicht erfüllt – kein Hold-out.")
    with ProcessPoolExecutor(workers) as ex:
        for msg in ex.map(run_symbol, [(s, "ho", (variant,)) for s in symbols]):
            print(msg, flush=True)
    marker.write_text(f"{variant} {date.today().isoformat()}\n")
    ho = load("ho", symbols)
    ho_tr = take(ho, ho["status"] == TRADED)
    years = range(2024, 2027)
    m = metrics(ho_tr, years)
    lo, hi = cluster_bootstrap_ci(is_tr["net_r"], (timez.ftmo_day(is_tr["t_fill"]) + 3) // 7)
    checks = [("Netto-Erwartungswert > 0", f"{m['E']:+.3f} R", m["E"] > 0),
              ("Netto-Profit-Factor > 1,1", f"{m['pf']:.2f}", m["pf"] > 1.1),
              ("nicht signifikant schlechter als In-Sample (≥ untere 95-%-Grenze IS)",
               f"{m['E']:+.3f} R vs. IS {m_is['E']:+.3f} R [{lo:+.3f}; {hi:+.3f}]", m["E"] >= lo)]
    lines = [f"# P3 – Modell C, Hold-out 2024–2026 (Trial T4, {variant})\n",
             f"Einmaliger Lauf vom {date.today():%d.%m.%Y}. Signale ab 01.01.2024 bis Datenende 16.10.2026.\n"]
    lines += status_table(ho) + [""]
    lines += ["| Kennzahl | Wert |", "|---|---|", f"| Trades | {m['n']:,} |",
              f"| Netto-Erwartungswert | {m['E']:+.3f} R |", f"| Profit-Factor netto | {m['pf']:.2f} |",
              f"| t-Wert iid / Tag / Woche | {m['t_iid']:.2f} / {m['t_day']:.2f} / {m['t_week']:.2f} |",
              f"| bei doppelten Kosten | {m['E_2x']:+.3f} R |", ""]
    lines += describe(ho_tr) + ["", "| Kriterium | Ergebnis | erfüllt |", "|---|---|---|"]
    lines += [f"| {c} | {v} | {'ja' if ok else '**nein**'} |" for c, v, ok in checks]
    ok = all(c[2] for c in checks)
    lines += ["", f"**Hold-out {'bestanden' if ok else 'nicht bestanden'}.**\n", "| Jahr | Trades | Netto Ø R |",
              "|---|---|---|"]
    lines += [f"| {y} | {k} | {e:+.3f} |" for y, (k, e) in m["by_year"].items()]
    path = RESULTS / "p3_modell_c_holdout.md"
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--symbols", default=",".join(SYMBOLS))
    ap.add_argument("--workers", type=int, default=6)
    ap.add_argument("--holdout", choices=[MKT, LMT])
    args = ap.parse_args()
    symbols = args.symbols.split(",")
    if args.holdout:
        holdout(args.holdout, symbols, args.workers)
    else:
        in_sample(symbols, args.workers)


if __name__ == "__main__":
    main()
