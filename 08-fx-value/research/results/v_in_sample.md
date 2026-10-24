# Modell V (FX Value G8), In-Sample 2015–2023 (Trial T299 V-5Y, T300 V-PPP)

Lauf vom 24.10.2026. Regeln laut `docs/01_Vorregistrierung.md`, Code `research/fval/` mit der Engine aus `../06-fx-carry/research/carry/`. Realer Wechselkurs aus FRED-CPI (2 Monate Verzug) und FRED-Monatsendkursen. Handelstage 01.01.2015–31.12.2023 (Warm-up 2014), 24 FX-Paare. Netto = nach Handelskosten, Swaps (Zinsdifferenz − 1 % Aufschlag) und 0,7-%-Gebühr. Renditen und Drawdown sind auf eine Portfolio-Volatilität von 10 % p. a. skaliert (Kalibrierung auf diesen Zeitraum, nur zur Einordnung).

## V-5Y

| Kennzahl | Wert |
|---|---|
| Handelstage | 2,340 |
| Sharpe Ratio p. a. (netto) | -0.06 |
| t-Wert iid / Woche / Monat | -0.18 / -0.17 / -0.17 |
| Rendite p. a. bei 10 % Volatilität | -0.59% |
| Max. Drawdown bei 10 % Volatilität | 41.8% |
| Zerlegung p. a. bei 10 % Vol.: Kurs / Swaps / Handel / Gebühr | +1.77% / -1.99% / -0.21% / -0.16% |
| Ø Brutto-Exposure (Summe \|w\|, unskaliert) | 3.92 |

| Kriterium | Ergebnis | erfüllt |
|---|---|---|
| Mittleres Netto-Tagesergebnis > 0 mit t ≥ 3,0 (kleinster aus iid / Woche / Monat) | t = -0.18 (Sharpe -0.06) | **nein** |
| ≥ 6 von 9 Jahren positiv | 3 von 9 | **nein** |
| ≥ 60 % der Instrumente (≥ 250 Positionstage) positiv | 8 von 13 | ja |
| bei doppelten Kosten > 0 | -3.36% p. a. bei 10 % Vol. | **nein** |

**V-5Y: nicht bestanden.**

| Jahr | Rendite bei 10 % Vol. | Sharpe |
|---|---|---|
| 2015 | -2.4% | -0.32 |
| 2016 | +9.9% | +1.16 |
| 2017 | -0.0% | -0.00 |
| 2018 | -5.6% | -0.50 |
| 2019 | +0.5% | +0.05 |
| 2020 | -5.7% | -0.40 |
| 2021 | +6.4% | +0.71 |
| 2022 | -1.0% | -0.09 |
| 2023 | -7.2% | -0.99 |

| Instrument | Positionstage | Beitrag netto bei 10 % Vol. (Summe) | davon Swaps |
|---|---|---|---|
| GBPAUD | 263 | +9.9% | -0.3% |
| USDCAD | 490 | +7.8% | -1.3% |
| NZDJPY | 305 | +6.4% | -0.7% |
| GBPJPY | 499 | +5.2% | -1.3% |
| AUDUSD | 716 | +3.3% | -1.6% |
| USDJPY | 953 | +2.5% | -5.2% |
| AUDCAD | 324 | +0.8% | -1.3% |
| CADCHF | 391 | +0.1% | +0.1% |
| GBPUSD | 370 | -3.3% | -1.7% |
| USDCHF | 693 | -3.5% | +1.5% |
| GBPCAD | 281 | -5.0% | -0.6% |
| EURCHF | 256 | -5.7% | -0.2% |
| NZDUSD | 821 | -14.6% | -2.3% |

### Beschreibend

| Auswertung | Sharpe | t (iid) | Rendite p. a. bei 10 % Vol. | Swaps p. a. |
|---|---|---|---|---|
| vorregistriert (Aufschlag 1 %) | -0.06 | -0.18 | -0.59% | -1.99% |
| ohne Swap-Aufschlag | +0.15 | +0.44 | +1.47% | +0.07% |

- 2015–2019: Sharpe +0.05, Kurs +2.62% p. a., Swaps -1.72% p. a. (bei 10 % Vol. des Teilzeitraums)
- 2020–2023: Sharpe -0.18, Kurs +0.86% p. a., Swaps -2.29% p. a. (bei 10 % Vol. des Teilzeitraums)

**Rangfolge nach Value-Signal (Long- und Short-Seite)**

Monate: 104

| Währung | Monate long | Monate short |
|---|---|---|
| AUD | 83 | 2 |
| JPY | 68 | 31 |
| CAD | 49 | 31 |
| NZD | 44 | 33 |
| GBP | 31 | 46 |
| EUR | 18 | 29 |
| CHF | 13 | 54 |
| USD | 6 | 86 |

## V-PPP

| Kennzahl | Wert |
|---|---|
| Handelstage | 2,340 |
| Sharpe Ratio p. a. (netto) | -0.07 |
| t-Wert iid / Woche / Monat | -0.22 / -0.22 / -0.29 |
| Rendite p. a. bei 10 % Volatilität | -0.74% |
| Max. Drawdown bei 10 % Volatilität | 25.6% |
| Zerlegung p. a. bei 10 % Vol.: Kurs / Swaps / Handel / Gebühr | +2.17% / -2.61% / -0.14% / -0.15% |
| Ø Brutto-Exposure (Summe \|w\|, unskaliert) | 3.64 |

| Kriterium | Ergebnis | erfüllt |
|---|---|---|
| Mittleres Netto-Tagesergebnis > 0 mit t ≥ 3,0 (kleinster aus iid / Woche / Monat) | t = -0.29 (Sharpe -0.07) | **nein** |
| ≥ 6 von 9 Jahren positiv | 5 von 9 | **nein** |
| ≥ 60 % der Instrumente (≥ 250 Positionstage) positiv | 4 von 11 | **nein** |
| bei doppelten Kosten > 0 | -3.78% p. a. bei 10 % Vol. | **nein** |

**V-PPP: nicht bestanden.**

| Jahr | Rendite bei 10 % Vol. | Sharpe |
|---|---|---|
| 2015 | -4.2% | -0.19 |
| 2016 | -3.9% | -0.63 |
| 2017 | +9.6% | +1.25 |
| 2018 | +1.9% | +0.29 |
| 2019 | +0.6% | +0.09 |
| 2020 | +4.1% | +0.51 |
| 2021 | +1.5% | +0.21 |
| 2022 | -11.4% | -1.17 |
| 2023 | -4.9% | -0.88 |

| Instrument | Positionstage | Beitrag netto bei 10 % Vol. (Summe) | davon Swaps |
|---|---|---|---|
| NZDJPY | 1167 | +11.3% | -5.2% |
| EURNZD | 285 | +8.6% | -1.7% |
| GBPAUD | 519 | +7.4% | -2.0% |
| USDCAD | 392 | +3.9% | -0.9% |
| AUDJPY | 260 | -1.2% | -0.9% |
| CHFJPY | 304 | -2.3% | -0.2% |
| GBPCHF | 411 | -3.2% | +0.6% |
| USDJPY | 609 | -4.6% | -4.0% |
| GBPNZD | 692 | -6.6% | -2.8% |
| GBPUSD | 476 | -7.2% | -1.6% |
| EURCHF | 888 | -21.8% | -1.4% |

### Beschreibend

| Auswertung | Sharpe | t (iid) | Rendite p. a. bei 10 % Vol. | Swaps p. a. |
|---|---|---|---|---|
| vorregistriert (Aufschlag 1 %) | -0.07 | -0.22 | -0.74% | -2.61% |
| ohne Swap-Aufschlag | +0.09 | +0.26 | +0.88% | -1.00% |

- 2015–2019: Sharpe +0.07, Kurs +3.41% p. a., Swaps -2.43% p. a. (bei 10 % Vol. des Teilzeitraums)
- 2020–2023: Sharpe -0.34, Kurs -0.00% p. a., Swaps -3.08% p. a. (bei 10 % Vol. des Teilzeitraums)

**Rangfolge nach Value-Signal (Long- und Short-Seite)**

Monate: 104

| Währung | Monate long | Monate short |
|---|---|---|
| JPY | 104 | 0 |
| GBP | 96 | 0 |
| EUR | 71 | 0 |
| CAD | 38 | 6 |
| AUD | 3 | 54 |
| USD | 0 | 69 |
| CHF | 0 | 81 |
| NZD | 0 | 102 |

**Korrelation der Netto-Tagesergebnisse mit Carry K-3 (Nr. 6):** V-5Y +0.15, V-PPP -0.19

**Ergebnis: Keine Variante erfüllt alle In-Sample-Kriterien. Strategie Nr. 8 ist gescheitert; der Hold-out bleibt unberührt.**
