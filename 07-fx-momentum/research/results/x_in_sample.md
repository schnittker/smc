# Modell X (FX Querschnitts-Momentum G8), In-Sample 2015–2023 (Trial T27 X-1, T28 X-12)

Lauf vom 24.10.2026. Regeln laut `docs/01_Vorregistrierung.md`, Code `research/xmom/` mit der Engine aus `../06-fx-carry/research/carry/`. Handelstage 01.01.2015–31.12.2023 (Warm-up 2014), 24 FX-Paare. Netto = nach Handelskosten, Swaps (Zinsdifferenz − 1 % Aufschlag) und 0,7-%-Gebühr. Renditen und Drawdown sind auf eine Portfolio-Volatilität von 10 % p. a. skaliert (Kalibrierung auf diesen Zeitraum, nur zur Einordnung).

## X-1

| Kennzahl | Wert |
|---|---|
| Handelstage | 2,340 |
| Sharpe Ratio p. a. (netto) | -0.28 |
| t-Wert iid / Woche / Monat | -0.83 / -0.81 / -0.87 |
| Rendite p. a. bei 10 % Volatilität | -2.77% |
| Max. Drawdown bei 10 % Volatilität | 43.8% |
| Zerlegung p. a. bei 10 % Vol.: Kurs / Swaps / Handel / Gebühr | -0.63% / -1.65% / -0.30% / -0.19% |
| Ø Brutto-Exposure (Summe \|w\|, unskaliert) | 3.73 |

| Kriterium | Ergebnis | erfüllt |
|---|---|---|
| Mittleres Netto-Tagesergebnis > 0 mit t ≥ 3,0 (kleinster aus iid / Woche / Monat) | t = -0.87 (Sharpe -0.28) | **nein** |
| ≥ 6 von 9 Jahren positiv | 2 von 9 | **nein** |
| ≥ 60 % der Instrumente (≥ 250 Positionstage) positiv | 6 von 14 | **nein** |
| bei doppelten Kosten > 0 | -5.35% p. a. bei 10 % Vol. | **nein** |

**X-1: nicht bestanden.**

| Jahr | Rendite bei 10 % Vol. | Sharpe |
|---|---|---|
| 2015 | +12.3% | +1.35 |
| 2016 | -5.0% | -0.51 |
| 2017 | +3.1% | +0.34 |
| 2018 | -4.2% | -0.45 |
| 2019 | -7.8% | -0.84 |
| 2020 | -2.5% | -0.18 |
| 2021 | -10.5% | -1.04 |
| 2022 | -3.5% | -0.32 |
| 2023 | -6.9% | -1.00 |

| Instrument | Positionstage | Beitrag netto bei 10 % Vol. (Summe) | davon Swaps |
|---|---|---|---|
| GBPJPY | 477 | +6.8% | -0.9% |
| EURNZD | 343 | +6.6% | -1.3% |
| AUDUSD | 835 | +3.4% | -1.6% |
| AUDJPY | 264 | +3.1% | -0.2% |
| USDCHF | 800 | +2.0% | -2.6% |
| USDCAD | 261 | +0.6% | -0.6% |
| GBPNZD | 308 | -0.2% | -0.4% |
| GBPUSD | 279 | -1.7% | -0.6% |
| EURUSD | 260 | -2.0% | -0.3% |
| NZDJPY | 322 | -2.8% | +0.5% |
| GBPCHF | 348 | -2.9% | -0.5% |
| CADJPY | 373 | -4.2% | -0.3% |
| CADCHF | 345 | -6.8% | -1.4% |
| NZDUSD | 821 | -17.9% | -1.7% |

### Beschreibend

| Auswertung | Sharpe | t (iid) | Rendite p. a. bei 10 % Vol. | Swaps p. a. |
|---|---|---|---|---|
| vorregistriert (Aufschlag 1 %) | -0.28 | -0.83 | -2.77% | -1.65% |
| ohne Swap-Aufschlag | -0.09 | -0.28 | -0.95% | +0.18% |

- 2015–2019: Sharpe -0.03, Kurs +2.05% p. a., Swaps -1.85% p. a. (bei 10 % Vol. des Teilzeitraums)
- 2020–2023: Sharpe -0.55, Kurs -3.57% p. a., Swaps -1.44% p. a. (bei 10 % Vol. des Teilzeitraums)

**Rangfolge nach Formationsrendite (Long- und Short-Seite)**

Monate: 104

| Währung | Monate long | Monate short |
|---|---|---|
| CHF | 51 | 35 |
| USD | 44 | 32 |
| NZD | 43 | 40 |
| GBP | 41 | 44 |
| AUD | 38 | 42 |
| JPY | 37 | 47 |
| CAD | 31 | 40 |
| EUR | 27 | 32 |

## X-12

| Kennzahl | Wert |
|---|---|
| Handelstage | 2,340 |
| Sharpe Ratio p. a. (netto) | -0.81 |
| t-Wert iid / Woche / Monat | -2.43 / -2.39 / -2.49 |
| Rendite p. a. bei 10 % Volatilität | -8.10% |
| Max. Drawdown bei 10 % Volatilität | 75.5% |
| Zerlegung p. a. bei 10 % Vol.: Kurs / Swaps / Handel / Gebühr | -6.41% / -1.31% / -0.23% / -0.16% |
| Ø Brutto-Exposure (Summe \|w\|, unskaliert) | 3.78 |

| Kriterium | Ergebnis | erfüllt |
|---|---|---|
| Mittleres Netto-Tagesergebnis > 0 mit t ≥ 3,0 (kleinster aus iid / Woche / Monat) | t = -2.49 (Sharpe -0.81) | **nein** |
| ≥ 6 von 9 Jahren positiv | 1 von 9 | **nein** |
| ≥ 60 % der Instrumente (≥ 250 Positionstage) positiv | 5 von 14 | **nein** |
| bei doppelten Kosten > 0 | -10.35% p. a. bei 10 % Vol. | **nein** |

**X-12: nicht bestanden.**

| Jahr | Rendite bei 10 % Vol. | Sharpe |
|---|---|---|
| 2015 | -14.2% | -1.15 |
| 2016 | -8.0% | -0.79 |
| 2017 | -13.2% | -1.43 |
| 2018 | -16.8% | -1.90 |
| 2019 | -9.2% | -0.95 |
| 2020 | +0.3% | +0.03 |
| 2021 | -7.3% | -0.65 |
| 2022 | -1.3% | -0.13 |
| 2023 | -2.9% | -0.47 |

| Instrument | Positionstage | Beitrag netto bei 10 % Vol. (Summe) | davon Swaps |
|---|---|---|---|
| USDJPY | 433 | +6.8% | +1.1% |
| AUDUSD | 825 | +6.7% | -1.2% |
| NZDJPY | 304 | +3.2% | -0.8% |
| CHFJPY | 258 | +0.7% | -0.3% |
| GBPUSD | 456 | +0.7% | -1.0% |
| EURCAD | 433 | -2.3% | +0.1% |
| EURUSD | 611 | -3.3% | -0.5% |
| EURNZD | 406 | -3.9% | -0.1% |
| USDCHF | 700 | -6.3% | -1.2% |
| GBPJPY | 324 | -8.4% | -0.6% |
| CADCHF | 278 | -9.1% | -0.6% |
| GBPCHF | 390 | -11.1% | -1.4% |
| NZDUSD | 610 | -11.4% | -1.2% |
| USDCAD | 258 | -11.8% | -0.6% |

### Beschreibend

| Auswertung | Sharpe | t (iid) | Rendite p. a. bei 10 % Vol. | Swaps p. a. |
|---|---|---|---|---|
| vorregistriert (Aufschlag 1 %) | -0.81 | -2.43 | -8.10% | -1.31% |
| ohne Swap-Aufschlag | -0.62 | -1.86 | -6.21% | +0.58% |

- 2015–2019: Sharpe -1.21, Kurs -10.39% p. a., Swaps -1.35% p. a. (bei 10 % Vol. des Teilzeitraums)
- 2020–2023: Sharpe -0.29, Kurs -1.24% p. a., Swaps -1.26% p. a. (bei 10 % Vol. des Teilzeitraums)

**Rangfolge nach Formationsrendite (Long- und Short-Seite)**

Monate: 104

| Währung | Monate long | Monate short |
|---|---|---|
| USD | 62 | 25 |
| CHF | 44 | 35 |
| CAD | 41 | 30 |
| GBP | 39 | 43 |
| NZD | 35 | 34 |
| JPY | 34 | 49 |
| EUR | 29 | 52 |
| AUD | 28 | 44 |

**Korrelation der Netto-Tagesergebnisse mit Carry K-3 (Nr. 6):** X-1 -0.08, X-12 +0.15

**Ergebnis: Keine Variante erfüllt alle In-Sample-Kriterien. Strategie Nr. 7 ist gescheitert; der Hold-out bleibt unberührt.**
