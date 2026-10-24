# Swing-Portfolio (Nr. 100), In-Sample 2015–2023 (Trial T306, beschreibend)

Lauf vom 24.10.2026. Regeln laut `docs/01_Vorregistrierung.md`, Code `research/swp/`. Bausteine unverändert aus Nr. 9, 10, 14 und 24; je Baustein auf 10 % Jahresvola normiert (inverse Volatilität, nur aus IS). Netto = nach Spread, Slippage, Kommission, Swaps und Gebühren; Tagesrendite als Anteil des Kapitals vor der FTMO-Skalierung.

**Wegen der Auswahl der Bausteine (die besten aus ~130 Versuchen) ist dieses Ergebnis nach oben verzerrt und nur beschreibend.**

### Bausteine

| Baustein | Gewicht g | Buchungstage | Summe netto p. a. (nativ) | Sharpe p. a. | Beitrag p. a. (gewichtet) |
|---|---|---|---|---|---|
| P-SPX | 5.83 | 67 | +1.45% | 0.84 | +8.44% |
| T-FRÜH | 1.42 | 96 | +3.93% | 0.56 | +5.57% |
| V-VOL | 0.59 | 2324 | +9.47% | 0.56 | +5.63% |
| F-CARRY | 1.93 | 58 | +3.56% | 0.69 | +6.88% |

### Korrelation der Tagesreihen

| | P-SPX | T-FRÜH | V-VOL | F-CARRY |
|---|---|---|---|---|
| P-SPX | +1.00 | +0.08 | +0.08 | +0.32 |
| T-FRÜH | +0.08 | +1.00 | +0.15 | +0.03 |
| V-VOL | +0.08 | +0.15 | +1.00 | +0.09 |
| F-CARRY | +0.32 | +0.03 | +0.09 | +1.00 |

## Portfolio

| Kennzahl | Wert |
|---|---|
| Handelstage | 2,324 |
| Netto je Tag | +10.16 bp (σ 145.2 bp) |
| Rendite p. a. (Summe, unskaliert) | +26.5% |
| Sharpe Ratio p. a. | 1.13 |
| t-Wert iid / Woche / Monat | 3.37 / 3.36 / 3.48 |
| Jahre positiv | 8 von 9 |
| bei doppelten Kosten | +8.68 bp/Tag |

| Jahr | Netto (Summe, unskaliert) |
|---|---|
| 2015 | -0.68% |
| 2016 | +14.77% |
| 2017 | +47.90% |
| 2018 | +9.36% |
| 2019 | +12.13% |
| 2020 | +59.76% |
| 2021 | +6.48% |
| 2022 | +50.98% |
| 2023 | +35.44% |

### FTMO-Bootstrap nur auf IS (zur Einordnung, nicht entscheidend)

| Tagesschwankung | Skalierung k | max. US500-Nominal | P(Phase 1) | P(Phase 2) | P(beide) | Median-Dauer (Monate) | historische Starts bestanden | Stufe erfüllt |
|---|---|---|---|---|---|---|---|---|
| 0.50% | 0.34 | 3.1× | 88% | 92% | **81%** | 18.2 | 77 von 89 (Median 19.3 M.) | nein |
| 0.75% | 0.52 | 4.7× | 67% | 90% | **60%** | 10.4 | 61 von 98 (Median 14.3 M.) | nein |
| 1.00% | 0.69 | 6.2× | 48% | 80% | **38%** | 6.3 | 39 von 101 (Median 8.9 M.) | nein |
| 1.25% | 0.86 | 7.8× | 34% | 69% | **24%** | 4.1 | 21 von 102 (Median 6.4 M.) | nein |

**Artefakt-Prüfung (Spielregel 6):** Keiner der Bausteine handelt zur ersten Feed-Kerze einer Sitzung (Zeitpunkte 13:55/14:00/15:55/16:50 New York).

**Ergebnis:** IS-Mittel > 0 – der Hold-out (T307) läuft wie vorregistriert.
