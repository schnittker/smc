#!/usr/bin/env python3
"""Strategy no. 94, model N (NFP straddle): in-sample run T303 with the pre-registered acceptance check, and - only
if it passed - the one-time hold-out run T304 (docs/01_Vorregistrierung.md).

Usage:
  ../smart-money-concept/research/.venv/bin/python -I research/scripts/run_n.py
  ../smart-money-concept/research/.venv/bin/python -I research/scripts/run_n.py --holdout
"""
import argparse
import sys
from datetime import date
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from nws import DATA_DIR, RESULTS_DIR  # noqa: E402
from nws.model import STOP, SYMBOLS, TIME, run_symbol  # noqa: E402
from dbo.model import EPOCH  # noqa: E402
from smc.data.bars import load_m1  # noqa: E402
from smc.report import cluster_bootstrap_ci, cluster_t  # noqa: E402

IS, HO = (date(2015, 1, 1), date(2023, 12, 31)), (date(2024, 1, 1), date(2026, 12, 31))
IS_YEARS, HO_YEARS = range(2015, 2024), range(2024, 2027)
OUT_DIR = DATA_DIR / "n"


def tval(x):
    return float(x.mean() / (x.std(ddof=1) / np.sqrt(len(x)))) if len(x) > 2 else np.nan


def stats(by_sym: dict, years) -> dict:
    rows = np.concatenate(list(by_sym.values()))
    days, inv = np.unique(rows["day"], return_inverse=True)
    net, cost, gross = (np.bincount(inv, rows[k]) for k in ("net_bp", "cost_bp", "gross_bp"))
    ds = [date.fromordinal(EPOCH.toordinal() + int(d)) for d in days]
    yr = np.array([d.year for d in ds])
    q = np.array([d.year * 4 + (d.month - 1) // 3 for d in ds])
    tr = rows[rows["dir"] != 0]
    m = {"n": len(net), "trades": len(tr), "E": float(net.mean()), "gross": float(gross.mean()),
         "cost": float(cost.mean()), "E_2x": float((net - cost).mean()), "t_iid": tval(net), "t_q": cluster_t(net, q),
         "fill": float(len(tr) / len(rows)), "stops": float((tr["exit_type"] == STOP).mean()),
         "R_net": float(tr["r_net"].mean()), "R_gross": float(np.mean(tr["gross_bp"] / (tr["notional"] * tr["r_bp"]))),
         "by_year": {y: float(net[yr == y].sum()) for y in years},
         "by_sym": {s: float(r["net_bp"].sum()) for s, r in by_sym.items()}, "net_arr": net, "q_arr": q}
    m["t"] = min(m["t_iid"], m["t_q"])
    m["years_pos"] = sum(1 for v in m["by_year"].values() if v > 0)
    m["sym_pos"] = sum(1 for v in m["by_sym"].values() if v > 0)
    return m


def checks(m, years):
    return [("Netto je Termin > 0 mit t ≥ 3,0 (iid / Quartal)", f"{m['E']:+.2f} bp, t = {m['t']:.2f}", m["E"] > 0 and m["t"] >= 3),
            (f"≥ 6 von {len(years)} Jahren positiv", f"{m['years_pos']} von {len(years)}", m["years_pos"] >= 6),
            ("≥ 3 von 4 Instrumenten positiv", f"{m['sym_pos']} von 4", m["sym_pos"] >= 3),
            ("bei doppelten Kosten > 0", f"{m['E_2x']:+.2f} bp", m["E_2x"] > 0)]


def lines_for(name, m, chk):
    ok = all(c for _, _, c in chk)
    out = [f"## {name}\n", "| Kennzahl | Wert |", "|---|---|", f"| Termine / Trades | {m['n']} / {m['trades']} |",
           f"| Netto je Termin (bp des Kapitals, 4 Instrumente) | {m['E']:+.2f} bp |",
           f"| vor Kosten / Kosten je Termin | {m['gross']:+.2f} / {m['cost']:.2f} bp |",
           f"| t-Wert iid / Quartal | {m['t_iid']:.2f} / {m['t_q']:.2f} |",
           f"| Auslösequote / Anteil Stops | {m['fill']:.0%} / {m['stops']:.0%} |",
           f"| Ø R je Trade vor / nach Kosten | {m['R_gross']:+.3f} / {m['R_net']:+.3f} |", "",
           "| Kriterium | Ergebnis | erfüllt |", "|---|---|---|"]
    out += [f"| {c} | {v} | {'ja' if k else '**nein**'} |" for c, v, k in chk]
    out += ["", f"**{name}: {'alle Kriterien erfüllt' if ok else 'nicht bestanden'}.**\n", "| Jahr | Netto Summe bp |", "|---|---|"]
    out += [f"| {y} | {v:+.1f} |" for y, v in m["by_year"].items()]
    out += ["", "| Instrument | Netto Summe bp |", "|---|---|"] + [f"| {s} | {v:+.1f} |" for s, v in m["by_sym"].items()]
    return out + [""]


def in_sample():
    m1 = {s: load_m1(s) for s in SYMBOLS}
    m = stats({s: run_symbol(s, x, *IS) for s, x in m1.items()}, IS_YEARS)
    chk = checks(m, IS_YEARS)
    norm = stats({s: run_symbol(s, x, *IS, spread_mult=1.0, news_slip=0.00001) for s, x in m1.items()}, IS_YEARS)
    lines = ["# Modell N (NFP-Straddle), In-Sample 2015–2023 (Trial T303 N-NFP)\n",
             f"Lauf vom {date.today():%d.%m.%Y}. Regeln laut `docs/01_Vorregistrierung.md`, Code `research/nws/`. "
             "OCO ±0,10 % um 08:29 New York, Stop 0,20 %, Ausstieg 09:30; News-Kosten 5-facher Spread und 0,03 % "
             "Slippage (08:30–08:34). Ergebnisse in bp des Kapitals, 0,25 % Risiko je Trade.\n"]
    lines += lines_for("N-NFP", m, chk)
    lines += ["## Beschreibend: normale Kosten (1-facher Spread, ≈ 0,1 Pip Slippage)\n",
              f"Netto {norm['E']:+.2f} bp je Termin (t {norm['t']:.2f}), vor Kosten {norm['gross']:+.2f} bp, "
              f"Ø R netto {norm['R_net']:+.3f}.\n"]
    ok = all(c for _, _, c in chk)
    lines.append("**Ergebnis: N-NFP erfüllt alle In-Sample-Kriterien; Artefakt-Prüfung und Hold-out folgen.**" if ok else
                 "**Ergebnis: N-NFP erfüllt die In-Sample-Kriterien nicht. Strategie Nr. 94 ist gescheitert; der "
                 "Hold-out bleibt unberührt.**")
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    (RESULTS_DIR / "n_in_sample.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))


def holdout():
    marker = OUT_DIR / "ho" / "DONE"
    if marker.exists():
        sys.exit("Hold-out wurde bereits ausgewertet (data/n/ho/DONE) – kein zweiter Lauf.")
    m1 = {s: load_m1(s) for s in SYMBOLS}
    m_is = stats({s: run_symbol(s, x, *IS) for s, x in m1.items()}, IS_YEARS)
    if not all(c for _, _, c in checks(m_is, IS_YEARS)):
        sys.exit("N-NFP hat die In-Sample-Kriterien nicht erfüllt – kein Hold-out.")
    marker.parent.mkdir(parents=True, exist_ok=True)
    marker.write_text(f"T304 N-NFP {date.today().isoformat()}\n")
    m = stats({s: run_symbol(s, x, *HO) for s, x in m1.items()}, HO_YEARS)
    lo, hi = cluster_bootstrap_ci(m_is["net_arr"], m_is["q_arr"])
    chk = [("Netto je Termin > 0", f"{m['E']:+.2f} bp", m["E"] > 0),
           ("≥ untere 95-%-Grenze von In-Sample", f"{m['E']:+.2f} vs. [{lo:+.2f}; {hi:+.2f}]", m["E"] >= lo)]
    lines = ["# Modell N, Hold-out 2024–2026 (Trial T304)\n", f"Einmaliger Lauf vom {date.today():%d.%m.%Y}.\n"]
    lines += lines_for("N-NFP", m, chk)
    (RESULTS_DIR / "n_holdout.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--holdout", action="store_true")
    args = ap.parse_args()
    holdout() if args.holdout else in_sample()


if __name__ == "__main__":
    main()
