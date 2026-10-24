#!/usr/bin/env python3
"""Descriptive robustness checks of Q-FXW on the in-sample data (2015-2023) - they do not change the rules or the
pre-registered decision; they look for data artefacts and cost sensitivity before the one-time hold-out.
"""
import sys
from datetime import date
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from gap import RESULTS_DIR  # noqa: E402
from gap.model import DAY, FXW, TARGET, run_weekend  # noqa: E402
from dbo.model import costs_for  # noqa: E402
from smc.data.bars import load_bars  # noqa: E402
from smc.report import cluster_t  # noqa: E402
from smc.timez import us_dst  # noqa: E402

IS = (date(2015, 1, 1), date(2023, 12, 31))


def portfolio(by_sym: dict) -> tuple[np.ndarray, np.ndarray]:
    rows = np.concatenate(list(by_sym.values()))
    days, inv = np.unique(rows["day"], return_inverse=True)
    return days, np.bincount(inv, rows["net_bp"])


def summary(by_sym: dict) -> str:
    days, net = portfolio(by_sym)
    tr = np.concatenate(list(by_sym.values()))
    tr = tr[tr["dir"] != 0]
    t = min(net.mean() / net.std(ddof=1) * np.sqrt(len(net)), cluster_t(net, (days // 30)))
    return (f"{len(tr):,} | {net.mean():+.2f} | {t:+.2f} | {np.mean(tr['gross_bp'] / (tr['notional'] * tr['r_bp'])):+.3f} | "
            f"{tr['r_net'].mean():+.3f} | {(tr['exit_type'] == TARGET).mean():.0%}")


def main():
    data = {}
    for s in FXW:
        m5 = load_bars(s, "M5")
        data[s] = (m5, costs_for(s, m5))
    run = lambda **kw: {s: run_weekend(s, m5, c, *IS, **kw) for s, (m5, c) in data.items()}
    head = "| Trades | Netto bp/Montag | t | Ø R vor Kosten | Ø R netto | Füllquote |"
    lines = ["# Q-FXW: Robustheitsprüfungen (beschreibend, In-Sample 2015–2023)\n",
             f"Lauf vom {date.today():%d.%m.%Y}. Ändert weder Regeln noch Entscheidung (`docs/01_Vorregistrierung.md`); "
             "Zweck: Datenartefakte und Kostenempfindlichkeit vor dem einmaligen Hold-out erkennen.\n",
             "## 1. Spread zur Montagseröffnung (Vielfaches des effektiven Spreads)\n",
             "| Vielfaches " + head, "|---" * 7 + "|"]
    for mult in (1, 3, 5, 8, 12, 20):
        lines.append(f"| {mult}× {'(vorregistriert)' if mult == 3 else ''} | " + summary(run(spread_mult=mult)) + " |")
    lines += ["", "## 2. Einstiegszeit (Server-Montag; 01:00 = vorregistriert)\n", "| Einstieg " + head, "|---" * 7 + "|"]
    for sec, lbl in ((300, "00:05"), (1800, "00:30"), (3600, "01:00"), (7200, "02:00"), (4 * 3600, "04:00"),
                     (9 * 3600, "09:00 (London 07:00/08:00)")):
        lines.append(f"| {lbl} | " + summary(run(entry_sec=sec)) + " |")
    base = run()
    tr = np.concatenate(list(base.values()))
    tr = tr[tr["dir"] != 0]
    days, net = portfolio(base)
    srt = np.sort(net)[::-1]
    lines += ["", "## 3. Verteilung\n", "| Kennzahl | Wert |", "|---|---|",
              f"| Anteil der Summe aus den besten 5 % der Montage | {srt[:max(1, len(srt) // 20)].sum() / net.sum():.0%} |",
              f"| Summe ohne die besten 5 % der Montage | {srt[len(srt) // 20:].sum() / 100:+.1f} % (gesamt {net.sum() / 100:+.1f} %) |",
              f"| Median je Montag / Anteil positiver Montage | {np.median(net):+.2f} bp / {(net > 0).mean():.0%} |",
              f"| Long (Gap nach unten) Ø R netto / Trades | {tr['r_net'][tr['dir'] == 1].mean():+.3f} / {(tr['dir'] == 1).sum()} |",
              f"| Short (Gap nach oben) Ø R netto / Trades | {tr['r_net'][tr['dir'] == -1].mean():+.3f} / {(tr['dir'] == -1).sum()} |",
              f"| Ø \\|Gap\\| / Ø Stop-Abstand | {np.abs(tr['gap_bp']).mean():.1f} bp / {tr['r_bp'].mean():.1f} bp |"]
    lines += ["", "## 4. Datenqualität der Einstiegskerze (Server-Montag 01:00)\n",
              "| Paar | Montage | Ø M1-Kerzen in der M5-Kerze | Anteil < 5 | Ø Spannweite der Kerze (bp) |", "|---|---|---|---|---|"]
    for s, (m5, _) in data.items():
        ts = m5["ts"]
        mon = ts[(ts % DAY == 3600) & ((ts // DAY + 3) % 7 == 0)]
        sel = np.isin(ts, mon) & (ts >= (IS[0] - date(1970, 1, 1)).days * DAY) & (ts < (date(2024, 1, 1) - date(1970, 1, 1)).days * DAY)
        b = m5[sel]
        lines.append(f"| {s} | {len(b)} | {b['n'].mean():.2f} | {(b['n'] < 5).mean():.0%} | "
                     f"{((b['h'] - b['l']) / b['o']).mean() * 1e4:.1f} |")
    lines += ["", "## 5. Zerlegung nach Jahreszeit (erste Kerze der Woche im HistData-Feed)\n",
              "Im Sommer (US-Sommerzeit) beginnt der HistData-Feed die Woche erst um 01:00 Server (17:00 EST fest = 18:00 EDT); "
              "im Winter um 00:00. Auf dem FTMO-Server beginnt der Handel ganzjährig um 00:00 Server.\n",
              "| Teilmenge " + head, "|---" * 7 + "|"]
    is_summer = lambda r: us_dst(r["day"] * DAY)
    two = run(entry_sec=7200)
    for lbl, src, pick in (("Sommer, 01:00 = erste Kerze der Woche", base, True),
                           ("Winter, 01:00 = 1 h nach Eröffnung", base, False),
                           ("Sommer, Einstieg 02:00 = 1 h nach erster Kerze", two, True)):
        sub = {s: r[is_summer(r) == pick] for s, r in src.items()}
        lines.append(f"| {lbl} | " + summary(sub) + " |")
    out = "\n".join(lines) + "\n"
    (RESULTS_DIR / "q_fxw_robustheit.md").write_text(out, encoding="utf-8")
    print(out)


if __name__ == "__main__":
    main()
