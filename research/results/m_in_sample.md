# Modell M (Monatsend-Rebalancing), In-Sample 2015–2023 (Trial T19 M-1H, T20 M-DAY)

Lauf vom 24.10.2026. Regeln laut `docs/01_Vorregistrierung.md`, Code `research/mer/`. Letzter Londoner Geschäftstag je Monat, HistData-M5 (Bid). Netto = nach Spread, Kommission, Slippage (0,1 Pip Einstieg, 0,5 Pip Ausstieg am Fix) und 0,7-%-Gebühr bei USDJPY; je Position gleicher Nominalwert, Ergebnisse in Basispunkten.

## M-1H

| Kennzahl | Wert |
|---|---|
| Ereignisse / Positionen | 106 / 391 |
| Netto je Ereignis | -4.41 bp (σ 45.1 bp) |
| vor Kosten je Ereignis | +1.35 bp |
| Kosten je Ereignis | 5.76 bp |
| Sharpe Ratio p. a. (netto) | -0.34 |
| t-Wert iid / Quartal | -1.01 / -0.90 |
| Anteil positiver Ereignisse | 42% |
| bei doppelten Kosten | -10.16 bp/Ereignis |

| Kriterium | Ergebnis | erfüllt |
|---|---|---|
| Mittleres Netto-Ereignisergebnis > 0 mit t ≥ 3,0 (kleinster aus iid / Quartal) | -4.41 bp/Ereignis, t = -1.01 | **nein** |
| ≥ 6 von 9 Jahren positiv | 3 von 9 | **nein** |
| ≥ 3 von 4 Paaren positiv | 1 von 4 | **nein** |
| bei doppelten Kosten > 0 | -10.16 bp/Ereignis | **nein** |

**M-1H: nicht bestanden.**

| Jahr | Ereignisse | Netto Summe bp |
|---|---|---|
| 2015 | 12 | -49.3 |
| 2016 | 12 | -46.3 |
| 2017 | 12 | +93.2 |
| 2018 | 12 | -25.3 |
| 2019 | 12 | +64.4 |
| 2020 | 10 | -19.0 |
| 2021 | 12 | -475.9 |
| 2022 | 12 | -55.1 |
| 2023 | 12 | +46.4 |

### Je Paar

| Paar | Positionen | netto Ø bp | vor Kosten Ø bp | Kosten Ø bp | t (netto) | Treffer | Stops |
|---|---|---|---|---|---|---|---|
| EURUSD | 101 | -1.56 | -0.23 | 1.33 | -0.87 | 45% | 2% |
| GBPUSD | 102 | +3.17 | +4.38 | 1.21 | +1.55 | 54% | 2% |
| USDJPY | 103 | -3.17 | -1.46 | 1.72 | -1.73 | 40% | 3% |
| AUDUSD | 85 | -3.60 | -1.53 | 2.07 | -1.45 | 42% | 2% |

### Regression wie im Paper

Fensterrendite der Fremdwährung gegen USD (bp) auf `R_fremd − R_US` (%), alle Paare gepoolt, t-Wert mit Clustern nach Ereignis. Paper (2004–2012, 15–16 Uhr): Steigung ≈ −1,4.

| Steigung bp je % | t-Wert | R² |
|---|---|---|
| -0.15 | -0.31 | 0.000 |

### Varianten der Auswertung

| Auswertung | Ereignisse | netto Ø bp | t-Wert |
|---|---|---|---|
| Vorzeichen (vorregistriert) | 106 | -4.41 | -1.01 |
| gewichtet mit \|x\| | 106 | -2.00 | -0.30 |
| nur Quartalsenden | 35 | -3.16 | -0.60 |
| übrige Monate | 71 | -5.02 | -0.83 |
| 2014 (vor der Fix-Reform; vor Kosten +4.60) | 11 | -0.86 | -0.09 |

### Umkehr nach dem Fix (Gegenposition 16:05 bis 12:00 am nächsten Geschäftstag, ohne Swaps)

Je Ereignis: netto +14.62 bp, vor Kosten +19.21 bp, t (netto) +1.26.

| Paar | Positionen | netto Ø bp | vor Kosten Ø bp | Kosten Ø bp | t (netto) | Treffer | Stops |
|---|---|---|---|---|---|---|---|
| EURUSD | 100 | +2.72 | +3.70 | 0.98 | +0.62 | 49% | 21% |
| GBPUSD | 103 | +8.12 | +9.03 | 0.91 | +1.60 | 57% | 20% |
| USDJPY | 102 | -1.39 | +0.13 | 1.52 | -0.33 | 48% | 27% |
| AUDUSD | 85 | +6.52 | +8.05 | 1.53 | +1.05 | 62% | 27% |

## M-DAY

| Kennzahl | Wert |
|---|---|
| Ereignisse / Positionen | 107 / 306 |
| Netto je Ereignis | -7.10 bp (σ 78.1 bp) |
| vor Kosten je Ereignis | -2.42 bp |
| Kosten je Ereignis | 4.68 bp |
| Sharpe Ratio p. a. (netto) | -0.31 |
| t-Wert iid / Quartal | -0.94 / -1.04 |
| Anteil positiver Ereignisse | 43% |
| bei doppelten Kosten | -11.78 bp/Ereignis |

| Kriterium | Ergebnis | erfüllt |
|---|---|---|
| Mittleres Netto-Ereignisergebnis > 0 mit t ≥ 3,0 (kleinster aus iid / Quartal) | -7.10 bp/Ereignis, t = -1.04 | **nein** |
| ≥ 6 von 9 Jahren positiv | 3 von 9 | **nein** |
| ≥ 3 von 4 Paaren positiv | 1 von 4 | **nein** |
| bei doppelten Kosten > 0 | -11.78 bp/Ereignis | **nein** |

**M-DAY: nicht bestanden.**

| Jahr | Ereignisse | Netto Summe bp |
|---|---|---|
| 2015 | 12 | -66.9 |
| 2016 | 12 | -108.0 |
| 2017 | 12 | +313.6 |
| 2018 | 12 | +8.5 |
| 2019 | 12 | +20.2 |
| 2020 | 11 | -66.7 |
| 2021 | 12 | -260.4 |
| 2022 | 12 | -189.0 |
| 2023 | 12 | -410.6 |

### Je Paar

| Paar | Positionen | netto Ø bp | vor Kosten Ø bp | Kosten Ø bp | t (netto) | Treffer | Stops |
|---|---|---|---|---|---|---|---|
| EURUSD | 31 | -1.24 | -0.05 | 1.19 | -0.17 | 39% | 42% |
| GBPUSD | 67 | -4.02 | -2.90 | 1.12 | -0.87 | 46% | 39% |
| USDJPY | 105 | +1.86 | +3.63 | 1.77 | +0.56 | 51% | 13% |
| AUDUSD | 103 | -6.29 | -4.31 | 1.97 | -1.58 | 43% | 18% |

### Regression wie im Paper

Fensterrendite der Fremdwährung gegen USD (bp) auf `R_fremd − R_US` (%), alle Paare gepoolt, t-Wert mit Clustern nach Ereignis. Paper (2004–2012, 15–16 Uhr): Steigung ≈ −1,4.

| Steigung bp je % | t-Wert | R² |
|---|---|---|
| +0.51 | +0.61 | 0.002 |

### Varianten der Auswertung

| Auswertung | Ereignisse | netto Ø bp | t-Wert |
|---|---|---|---|
| Vorzeichen (vorregistriert) | 107 | -7.10 | -0.94 |
| gewichtet mit \|x\| | 107 | -13.74 | -1.28 |
| nur Quartalsenden | 36 | -10.70 | -1.07 |
| übrige Monate | 71 | -5.27 | -0.52 |
| 2014 (vor der Fix-Reform; vor Kosten -9.47) | 11 | -13.05 | -0.96 |

### Umkehr nach dem Fix (Gegenposition 16:05 bis 12:00 am nächsten Geschäftstag, ohne Swaps)

Je Ereignis: netto +16.59 bp, vor Kosten +20.45 bp, t (netto) +1.38.

| Paar | Positionen | netto Ø bp | vor Kosten Ø bp | Kosten Ø bp | t (netto) | Treffer | Stops |
|---|---|---|---|---|---|---|---|
| EURUSD | 30 | +16.92 | +17.90 | 0.98 | +1.97 | 70% | 13% |
| GBPUSD | 66 | +9.75 | +10.68 | 0.93 | +1.55 | 58% | 18% |
| USDJPY | 103 | +2.70 | +4.23 | 1.54 | +0.57 | 50% | 26% |
| AUDUSD | 103 | +3.04 | +4.56 | 1.52 | +0.56 | 56% | 27% |

**Ergebnis: Keine Variante erfüllt alle In-Sample-Kriterien. Strategie Nr. 5 ist gescheitert; der Hold-out bleibt unberührt.**
