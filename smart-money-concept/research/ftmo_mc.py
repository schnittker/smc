#!/usr/bin/env python3
"""Monte-Carlo-Simulation der FTMO 2-Step Challenge (100k, Swing).

Frage: Wie wahrscheinlich ist das Bestehen von Phase 1 (+10 %) und Phase 2 (+5 %)
bei Max Loss 10 % und Max Daily Loss 5 %, abhängig vom echten Netto-Edge der
Strategie (Erwartungswert in R pro Trade) und vom Risiko pro Trade? Und wie lange dauert es?

Modell (bewusst einfach, eher konservativ):
- Handelstage laufen nacheinander. Trades pro Tag ~ Poisson(lam), gedeckelt auf max_tr,
  innerhalb des Tages sequenziell.
- Ergebnis je Trade in R: Gewinn +rr, Verlust -loss_mult. Die Trefferquote p folgt aus dem
  Netto-Erwartungswert E: E = p*rr - (1-p)*loss_mult.
- Vor dem Abschluss läuft jeder Trade ins Minus (MAE): Verlierer bis -loss_mult R,
  Gewinner gleichverteilt bis -mae_win R. Max Loss und Daily Loss werden an diesem
  Tiefpunkt auf Equity-Basis geprüft.
- Tageskorrelation: Mit Wahrscheinlichkeit rho_day haben alle Trades eines Tages dasselbe
  Ergebnis (z. B. ein USD-Event trifft mehrere Paare).
- Internes Tageslimit: nach stop_losses Verlusten keine neuen Trades mehr an diesem Tag.
- Risiko je Trade in % des Anfangskapitals, optional mit Drawdown-Leiter.
- Bestanden: Balance >= Ziel nach einem Trade-Abschluss; Mindest-Handelstage werden ergänzt.
- Kein Zeitlimit; nach max_days Handelstagen gilt ein Lauf als "unfertig".
"""
import argparse
from pathlib import Path

import numpy as np

TRADING_DAYS_PER_MONTH = 21


def simulate(E, risk, target, *, rr=2.0, loss_mult=1.0, lam=1.0, max_tr=3, stop_losses=2,
             daily_lim=0.05, max_loss=0.10, n=20000, max_days=1500, rho_day=0.3,
             mae_win=0.8, ladder=(), min_days=4, seed=7):
    rng = np.random.default_rng(seed)
    p = (E + loss_mult) / (rr + loss_mult)
    eq = np.ones(n)
    st = np.zeros(n, np.int8)  # 0 läuft, 1 bestanden, 2 Max Loss, 3 Daily Loss
    end_day = np.full(n, -1, np.int32)
    tdays = np.zeros(n, np.int32)
    for d in range(max_days):
        if not (st == 0).any():
            break
        start = eq.copy()
        n_tr = np.minimum(rng.poisson(lam, n), max_tr)
        common = rng.random(n) < rho_day
        u_common = rng.random(n)
        losses = np.zeros(n, np.int8)
        traded = np.zeros(n, bool)
        for k in range(max_tr):
            act = (st == 0) & (n_tr > k) & (losses < stop_losses)
            if not act.any():
                break
            r = np.full(n, risk)
            dd = 1.0 - eq
            for thr, fac in ladder:  # Schwellen aufsteigend; die tiefere Stufe gewinnt
                r = np.where(dd >= thr, risk * fac, r)
            u = np.where(common, u_common, rng.random(n))
            win = u < p
            low = eq - np.where(win, rng.random(n) * mae_win, loss_mult) * r
            f_max = act & (low <= 1.0 - max_loss)
            f_day = act & ~f_max & (low <= start - daily_lim)
            st[f_max] = 2
            st[f_day] = 3
            end_day[f_max | f_day] = d
            ok = act & ~f_max & ~f_day
            eq = np.where(ok, eq + np.where(win, rr * r, -loss_mult * r), eq)
            losses += (ok & ~win).astype(np.int8)
            traded |= act
            hit = ok & (eq >= 1.0 + target)
            if hit.any():
                st[hit] = 1
                # heutiger Tag zählt als Handelstag; fehlende Mindesttage mit Mini-Trades auffüllen
                end_day[hit] = d + np.maximum(0, min_days - (tdays[hit] + 1))
        tdays += traded
    days = end_day + 1
    passed = st == 1
    return {
        "p": p,
        "pass": passed.mean(),
        "fail_max": (st == 2).mean(),
        "fail_day": (st == 3).mean(),
        "open": (st == 0).mean(),
        "days_pass": days[passed],
    }


def both_phases(E, risk, seed, **kw):
    a = simulate(E, risk, 0.10, seed=seed, **kw)
    b = simulate(E, risk, 0.05, seed=seed + 1, **kw)
    rng = np.random.default_rng(seed + 2)
    tot = None
    if len(a["days_pass"]) and len(b["days_pass"]):
        m = min(len(a["days_pass"]), len(b["days_pass"]), 20000)
        tot = rng.choice(a["days_pass"], m) + rng.choice(b["days_pass"], m)
    return a, b, tot


def fmt_months(days):
    return f"{days / TRADING_DAYS_PER_MONTH:.1f}"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=20000)
    ap.add_argument("--lam", type=float, default=1.0, help="Trades pro Handelstag (Portfolio)")
    ap.add_argument("--rr", type=float, default=2.0)
    ap.add_argument("--rho", type=float, default=0.3)
    ap.add_argument("--out", type=Path, default=Path(__file__).parent / "results" / "ftmo_mc_results.md")
    args = ap.parse_args()

    edges = [-0.10, -0.05, 0.0, 0.05, 0.10, 0.20]
    risks = [0.0025, 0.005, 0.0075, 0.01, 0.015, 0.02]
    kw = dict(n=args.n, lam=args.lam, rr=args.rr, rho_day=args.rho)
    out = []
    out.append("# FTMO 2-Step (100k, Swing) – Monte-Carlo-Ergebnisse\n")
    out.append(f"Annahmen: {args.lam} Trades/Handelstag (Poisson, max. 3), Gewinn = {args.rr} R, Verlust = 1 R, "
               f"Tageskorrelation {args.rho}, internes Tageslimit 2 Verluste, Max Loss 10 % und Daily Loss 5 % "
               f"auf Equity (Gewinner-MAE bis 0,8 R), kein Zeitlimit, {args.n} Läufe je Zelle. "
               "E = Netto-Erwartungswert pro Trade in R (nach Kosten). "
               f"Monate = Handelstage / {TRADING_DAYS_PER_MONTH}.\n")

    res = {}
    for i, E in enumerate(edges):
        for j, r in enumerate(risks):
            res[(E, r)] = both_phases(E, r, seed=1000 + 10 * i + j, **kw)

    def table(title, cell):
        out.append(f"\n## {title}\n")
        out.append("| E (R/Trade) | Trefferquote | " + " | ".join(f"{r * 100:.3g} % Risiko" for r in risks) + " |")
        out.append("|---|---|" + "---|" * len(risks))
        for E in edges:
            p = res[(E, risks[0])][0]["p"]
            out.append(f"| {E:+.2f} | {p * 100:.1f} % | " + " | ".join(cell(res[(E, r)]) for r in risks) + " |")

    table("P(Phase 1 bestanden) – Ziel +10 %", lambda x: f"{x[0]['pass'] * 100:.0f} %")
    table("P(Phase 2 bestanden) – Ziel +5 %", lambda x: f"{x[1]['pass'] * 100:.0f} %")
    table("P(beide Phasen bestanden)", lambda x: f"**{x[0]['pass'] * x[1]['pass'] * 100:.0f} %**")
    table("Dauer bis zum Bestehen beider Phasen – Median in Monaten (P10–P90)",
          lambda x: "–" if x[2] is None else
          f"{fmt_months(np.median(x[2]))} ({fmt_months(np.percentile(x[2], 10))}–{fmt_months(np.percentile(x[2], 90))})")
    table("Phase 1: Anteil Fehlschlag durch Daily Loss / Max Loss / unfertig nach "
          f"{1500 // TRADING_DAYS_PER_MONTH} Monaten",
          lambda x: f"{x[0]['fail_day'] * 100:.0f} / {x[0]['fail_max'] * 100:.0f} / {x[0]['open'] * 100:.0f} %")

    # Risikoleiter: Basisrisiko, halbiert ab 3 % DD, geviertelt ab 6 % DD (DD vom Anfangskapital)
    ladder = ((0.03, 0.5), (0.06, 0.25))
    out.append("\n## Risikoleiter (Basisrisiko; ab 3 % Drawdown halbiert, ab 6 % geviertelt)\n")
    out.append("| E (R/Trade) | Basis 1 %: P(beide) | Median Monate | Basis 1,5 %: P(beide) | Median Monate | Basis 2 %: P(beide) | Median Monate |")
    out.append("|---|---|---|---|---|---|---|")
    for i, E in enumerate(edges):
        cells = []
        for j, base in enumerate((0.01, 0.015, 0.02)):
            a, b, tot = both_phases(E, base, seed=5000 + 10 * i + j, ladder=ladder, **kw)
            cells.append(f"{a['pass'] * b['pass'] * 100:.0f} %")
            cells.append("–" if tot is None else fmt_months(np.median(tot)))
        out.append(f"| {E:+.2f} | " + " | ".join(cells) + " |")

    # Phasenabhängige Leiter: eigenes Basisrisiko je Phase
    out.append("\n## Risikoleiter je Phase (Basisrisiko Phase 1 / Phase 2)\n")
    combos = ((0.01, 0.01), (0.01, 0.0075), (0.01, 0.005), (0.0075, 0.005), (0.0125, 0.0075))
    out.append("| E (R/Trade) | " + " | ".join(f"{a * 100:.3g} % / {b * 100:.3g} %" for a, b in combos) + " |")
    out.append("|---|" + "---|" * len(combos))
    for i, E in enumerate(edges):
        cells = []
        for j, (r1, r2) in enumerate(combos):
            a = simulate(E, r1, 0.10, seed=9000 + 10 * i + j, ladder=ladder, **kw)
            b = simulate(E, r2, 0.05, seed=9500 + 10 * i + j, ladder=ladder, **kw)
            rng = np.random.default_rng(9900 + 10 * i + j)
            m = min(len(a["days_pass"]), len(b["days_pass"]), 20000)
            med = fmt_months(np.median(rng.choice(a["days_pass"], m) + rng.choice(b["days_pass"], m))) if m else "–"
            cells.append(f"{a['pass'] * b['pass'] * 100:.0f} % ({med} M)")
        out.append(f"| {E:+.2f} | " + " | ".join(cells) + " |")

    # Sensitivität Handelsfrequenz bei E = +0,10 R
    out.append("\n## Sensitivität: Handelsfrequenz (E = +0,10 R, Risiko 1 %)\n")
    out.append("| Trades/Tag | P(beide) | Median Monate (P10–P90) |")
    out.append("|---|---|---|")
    for j, lam in enumerate((0.5, 1.0, 2.0, 3.0)):
        kw2 = dict(kw, lam=lam)
        a, b, tot = both_phases(0.10, 0.01, seed=7000 + j, **kw2)
        out.append(f"| {lam} | {a['pass'] * b['pass'] * 100:.0f} % | {fmt_months(np.median(tot))} "
                   f"({fmt_months(np.percentile(tot, 10))}–{fmt_months(np.percentile(tot, 90))}) |")

    text = "\n".join(out) + "\n"
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(text, encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()
