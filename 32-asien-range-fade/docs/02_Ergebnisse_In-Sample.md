# Ergebnisse Strategie Nr. 32 – Modell A „Asien-Range-Fade“

Stand: 24.10.2026

Grundlagen:
- Regeln: unverändert aus der Vorregistrierung `docs/01_Vorregistrierung.md` (Commit `b01941c`)
- Code: `research/arf/`, Lauf `research/scripts/run_a.py` (Commit `959be68`); 3 Tests grün
- In-Sample: Nächte 2015–2023
- Vollständige Tabellen: `research/results/a_in_sample.md`

## 1. Ergebnis

**Beide Varianten sind nach Kosten stark negativ. Strategie Nr. 32 ist damit gescheitert.** Der Hold-out bleibt unberührt, T112 und T113 entfallen.

| Kennzahl | A-EURCHF | A-AUDCAD |
|---|---|---|
| Netto je Nacht (bp des Kapitals, Risiko 0,25 % je Trade) | **−14,1** | **−11,8** |
| vor Kosten je Nacht | +9,1 | +4,0 |
| Kosten je Nacht | 23,2 | 15,8 |
| t-Wert (netto) | −23,4 | −18,2 |
| Jahre positiv | 0 von 9 | 0 von 9 |
| Trades (9 Jahre) | 6.902 | 7.523 |
| Ø R je Trade vor Kosten / netto | +0,123 / −0,208 | +0,049 / −0,144 |
| Trefferquote / Stops | 49 % / 18 % | 54 % / 22 % |

## 2. Einordnung

- **Die Mean Reversion in der Asien-Session existiert:** Vor Kosten verdienen die Fades +0,12 R (EURCHF) bzw. +0,05 R (AUDCAD) je Trade, und das bei Tausenden von Trades.
- **Die Kosten sind aber zwei- bis siebenmal so groß wie der Vorteil:** Die Bänder sind nachts nur wenige Pips breit. Spread (EURCHF ≈ 0,9 Pip, AUDCAD ≈ 1,0 Pip), Kommission und Slippage kosten 0,19–0,33 R je Trade.
- Genau daran scheitern laut Praxis auch die kommerziellen „Night Scalper“: Sie funktionieren nur mit sehr niedrigen Spreads, die es bei FTMO nicht gibt.
- **Folgerung:** Scalping-Ansätze auf M1/M5 (Nr. 80) haben bei FTMO-Kosten keinen Spielraum. Das gilt sicher für die ruhigen Sessions, vermutlich generell.

## 3. Trial-Log (Fortsetzung)

| # | Datum | Test | Ergebnis |
|---|---|---|---|
| T110 | 24.10.2026 | A-EURCHF, In-Sample | nicht bestanden: −14,1 bp/Nacht, vor Kosten +9,1 bp |
| T111 | 24.10.2026 | A-AUDCAD, In-Sample | nicht bestanden: −11,8 bp/Nacht, vor Kosten +4,0 bp |
| T112 | – | Hold-out | entfällt, Hold-out unberührt |
| T113 | – | FTMO-Bootstrap | entfällt |
