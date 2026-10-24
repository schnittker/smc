# Ergebnisse Strategie Nr. 20 – Modell Z „Zins-Momentum G8“

Stand: 24.10.2026

Grundlagen:
- Regeln: unverändert aus der Vorregistrierung `docs/01_Vorregistrierung.md` (Commit `ccffdfe`)
- Code: `research/zmom/` mit der Engine aus Nr. 6, Lauf `research/scripts/run_z.py` (Commit `2c4f60c`); 2 Tests grün
- In-Sample: Handelstage 2015–2023, 24 FX-Paare
- Vollständige Tabellen: `research/results/z_in_sample.md`

## 1. Ergebnis

**Beide Varianten verfehlen alle Kriterien. Strategie Nr. 20 ist damit gescheitert.** Der Hold-out 2024–2026 bleibt unberührt, T70 und T71 entfallen.

| Kriterium | Schwelle | Z-12 (12 Monate) | Z-3 (3 Monate) |
|---|---|---|---|
| Sharpe Ratio p. a. netto | (≈ 1,0) | **−0,22** | **−0,29** |
| t-Wert (kleinster aus iid, Woche, Monat) | ≥ 3,0 | **−0,68** | **−0,96** |
| Jahre positiv | ≥ 6 von 9 | **3 von 9** | **3 von 9** |
| Instrumente positiv | ≥ 60 % | **7 von 13** | **6 von 14** |
| bei doppelten Kosten | > 0 | **−4,6 % p. a.** | **−5,1 % p. a.** |
| ohne Swap-Aufschlag (beschreibend) | – | Sharpe −0,01 | Sharpe −0,11 |

## 2. Einordnung

1. **Kein Ertrag aus Zinsänderungen, selbst vor dem Swap-Aufschlag.** Die Kursentwicklung trägt mit −0,6 bzw. −1,1 % p. a. (bei 10 % Volatilität) nichts bei. Long-Positionen in Währungen mit steigenden Zinsen kosten zudem oft Swaps, weil deren Zinsniveau anfangs noch niedrig ist.
2. **USD dominiert die Long-Seite** (76 von 104 Monaten bei Z-12), AUD und NZD die Short-Seite. 2022 lief entsprechend (USD-Stärke). Insgesamt reicht das nicht, und 2020–2023 ist bei Z-3 deutlich negativ (Sharpe −0,54).
3. **Negativ korreliert mit Carry** (−0,25 bzw. −0,13). Eine Mischung zweier Strategien ohne Ertrag bringt aber keinen Ertrag.
4. **Gesamtbild FX:** Nach Trend (Nr. 3), Carry (Nr. 6), Kursmomentum (Nr. 7), COT (Nr. 18) und Zinsänderung (Nr. 20) hat kein systematischer Faktor auf den G8-Währungen 2015–2023 nach FTMO-Kosten einen Vorteil.

## 3. Trial-Log (Fortsetzung)

| # | Datum | Test | Ergebnis |
|---|---|---|---|
| T68 | 24.10.2026 | Z-12, In-Sample | nicht bestanden: Sharpe −0,22, t −0,68 |
| T69 | 24.10.2026 | Z-3, In-Sample | nicht bestanden: Sharpe −0,29, t −0,96 |
| T70 | – | Hold-out | entfällt, Hold-out unberührt |
| T71 | – | FTMO-Bootstrap | entfällt |
