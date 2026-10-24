# Modell Z (Zins-Momentum G8), In-Sample 2015–2023 (Trial T68 Z-12, T69 Z-3)

Lauf vom 24.10.2026. Regeln laut `docs/01_Vorregistrierung.md`, Code `research/zmom/` mit der Engine aus `../06-fx-carry/research/carry/`. Handelstage 01.01.2015–31.12.2023 (Warm-up 2014), 24 FX-Paare. Netto = nach Handelskosten, Swaps (Zinsdifferenz − 1 % Aufschlag) und 0,7-%-Gebühr. Renditen und Drawdown sind auf eine Portfolio-Volatilität von 10 % p. a. skaliert (Kalibrierung auf diesen Zeitraum, nur zur Einordnung).

## Z-12

| Kennzahl | Wert |
|---|---|
| Handelstage | 2,340 |
| Sharpe Ratio p. a. (netto) | -0.22 |
| t-Wert iid / Woche / Monat | -0.65 / -0.65 / -0.68 |
| Rendite p. a. bei 10 % Volatilität | -2.15% |
| Max. Drawdown bei 10 % Volatilität | 35.7% |
| Zerlegung p. a. bei 10 % Vol.: Kurs / Swaps / Handel / Gebühr | -0.64% / -1.21% / -0.17% / -0.13% |
| Ø Brutto-Exposure (Summe \|w\|, unskaliert) | 4.05 |

| Kriterium | Ergebnis | erfüllt |
|---|---|---|
| Mittleres Netto-Tagesergebnis > 0 mit t ≥ 3,0 (kleinster aus iid / Woche / Monat) | t = -0.68 (Sharpe -0.22) | **nein** |
| ≥ 6 von 9 Jahren positiv | 3 von 9 | **nein** |
| ≥ 60 % der Instrumente (≥ 250 Positionstage) positiv | 7 von 13 | **nein** |
| bei doppelten Kosten > 0 | -4.60% p. a. bei 10 % Vol. | **nein** |

**Z-12: nicht bestanden.**

| Jahr | Rendite bei 10 % Vol. | Sharpe |
|---|---|---|
| 2015 | +11.6% | +0.87 |
| 2016 | -11.1% | -1.16 |
| 2017 | -12.8% | -1.53 |
| 2018 | -2.3% | -0.27 |
| 2019 | +4.4% | +0.49 |
| 2020 | +6.8% | +0.57 |
| 2021 | -10.2% | -0.99 |
| 2022 | -2.2% | -0.23 |
| 2023 | -3.5% | -0.46 |

| Instrument | Positionstage | Beitrag netto bei 10 % Vol. (Summe) | davon Swaps |
|---|---|---|---|
| EURUSD | 479 | +9.6% | +0.6% |
| AUDUSD | 414 | +6.4% | -1.1% |
| GBPAUD | 366 | +3.9% | -1.5% |
| USDJPY | 381 | +2.9% | +1.1% |
| GBPCHF | 303 | +1.4% | +0.6% |
| USDCHF | 931 | +0.6% | -2.4% |
| USDCAD | 388 | +0.4% | -1.3% |
| CADJPY | 550 | -1.4% | -0.6% |
| NZDUSD | 1217 | -7.1% | -3.2% |
| EURCAD | 256 | -7.3% | +0.7% |
| EURNZD | 538 | -7.3% | +0.4% |
| CADCHF | 364 | -9.0% | +0.9% |
| GBPUSD | 434 | -10.5% | -2.3% |

### Beschreibend

| Auswertung | Sharpe | t (iid) | Rendite p. a. bei 10 % Vol. | Swaps p. a. |
|---|---|---|---|---|
| vorregistriert (Aufschlag 1 %) | -0.22 | -0.65 | -2.15% | -1.21% |
| ohne Swap-Aufschlag | -0.01 | -0.03 | -0.09% | +0.86% |

- 2015–2019: Sharpe -0.20, Kurs +0.16% p. a., Swaps -1.89% p. a. (bei 10 % Vol. des Teilzeitraums)
- 2020–2023: Sharpe -0.23, Kurs -1.63% p. a., Swaps -0.36% p. a. (bei 10 % Vol. des Teilzeitraums)

**Rangfolge nach Zinsänderung (Long- und Short-Seite)**

Monate: 104

| Währung | Monate long | Monate short |
|---|---|---|
| USD | 76 | 20 |
| GBP | 63 | 12 |
| CAD | 50 | 34 |
| JPY | 40 | 32 |
| CHF | 34 | 44 |
| NZD | 27 | 65 |
| EUR | 20 | 45 |
| AUD | 2 | 60 |

## Z-3

| Kennzahl | Wert |
|---|---|
| Handelstage | 2,340 |
| Sharpe Ratio p. a. (netto) | -0.29 |
| t-Wert iid / Woche / Monat | -0.85 / -0.83 / -0.96 |
| Rendite p. a. bei 10 % Volatilität | -2.85% |
| Max. Drawdown bei 10 % Volatilität | 47.2% |
| Zerlegung p. a. bei 10 % Vol.: Kurs / Swaps / Handel / Gebühr | -1.11% / -1.34% / -0.23% / -0.18% |
| Ø Brutto-Exposure (Summe \|w\|, unskaliert) | 4.02 |

| Kriterium | Ergebnis | erfüllt |
|---|---|---|
| Mittleres Netto-Tagesergebnis > 0 mit t ≥ 3,0 (kleinster aus iid / Woche / Monat) | t = -0.96 (Sharpe -0.29) | **nein** |
| ≥ 6 von 9 Jahren positiv | 3 von 9 | **nein** |
| ≥ 60 % der Instrumente (≥ 250 Positionstage) positiv | 6 von 14 | **nein** |
| bei doppelten Kosten > 0 | -5.09% p. a. bei 10 % Vol. | **nein** |

**Z-3: nicht bestanden.**

| Jahr | Rendite bei 10 % Vol. | Sharpe |
|---|---|---|
| 2015 | +13.9% | +0.68 |
| 2016 | -10.9% | -1.47 |
| 2017 | -4.7% | -0.66 |
| 2018 | -5.4% | -0.68 |
| 2019 | -0.8% | -0.12 |
| 2020 | +1.5% | +0.16 |
| 2021 | -10.2% | -1.28 |
| 2022 | -11.2% | -1.29 |
| 2023 | +2.3% | +0.39 |

| Instrument | Positionstage | Beitrag netto bei 10 % Vol. (Summe) | davon Swaps |
|---|---|---|---|
| EURCHF | 340 | +12.6% | -0.5% |
| AUDUSD | 432 | +10.6% | -1.0% |
| GBPAUD | 324 | +5.5% | -0.6% |
| EURUSD | 344 | +3.2% | -0.4% |
| USDJPY | 588 | +2.6% | +0.9% |
| EURCAD | 285 | +0.5% | +0.4% |
| USDCAD | 391 | -2.7% | -1.1% |
| CADCHF | 284 | -3.4% | -0.1% |
| NZDJPY | 343 | -4.5% | -0.9% |
| USDCHF | 976 | -5.1% | -1.6% |
| GBPNZD | 260 | -7.5% | -0.6% |
| CADJPY | 297 | -7.6% | -0.2% |
| NZDUSD | 998 | -10.7% | -2.6% |
| GBPUSD | 390 | -11.3% | -0.8% |

### Beschreibend

| Auswertung | Sharpe | t (iid) | Rendite p. a. bei 10 % Vol. | Swaps p. a. |
|---|---|---|---|---|
| vorregistriert (Aufschlag 1 %) | -0.29 | -0.85 | -2.85% | -1.34% |
| ohne Swap-Aufschlag | -0.11 | -0.33 | -1.10% | +0.41% |

- 2015–2019: Sharpe -0.14, Kurs +0.55% p. a., Swaps -1.61% p. a. (bei 10 % Vol. des Teilzeitraums)
- 2020–2023: Sharpe -0.54, Kurs -4.02% p. a., Swaps -0.92% p. a. (bei 10 % Vol. des Teilzeitraums)

**Rangfolge nach Zinsänderung (Long- und Short-Seite)**

Monate: 104

| Währung | Monate long | Monate short |
|---|---|---|
| USD | 68 | 23 |
| CAD | 49 | 26 |
| GBP | 44 | 20 |
| JPY | 43 | 43 |
| CHF | 36 | 46 |
| NZD | 30 | 61 |
| EUR | 25 | 47 |
| AUD | 17 | 46 |

**Korrelation der Netto-Tagesergebnisse mit Carry K-3 (Nr. 6):** Z-12 -0.25, Z-3 -0.13

**Ergebnis: Keine Variante erfüllt alle In-Sample-Kriterien. Strategie Nr. 20 ist gescheitert; der Hold-out bleibt unberührt.**
