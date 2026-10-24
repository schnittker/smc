# Modell K (FX Carry G8), In-Sample 2015–2023 (Trial T23 K-3, T24 K-1)

Lauf vom 24.10.2026. Regeln laut `docs/01_Vorregistrierung.md`, Code `research/carry/`. Handelstage 01.01.2015–31.12.2023 (Warm-up 2014), 24 FX-Paare. Netto = nach Handelskosten, Swaps (Zinsdifferenz − 1 % Aufschlag) und 0,7-%-Gebühr. Renditen und Drawdown sind auf eine Portfolio-Volatilität von 10 % p. a. skaliert (Kalibrierung auf diesen Zeitraum, nur zur Einordnung).

## K-3

| Kennzahl | Wert |
|---|---|
| Handelstage | 2,340 |
| Sharpe Ratio p. a. (netto) | -0.16 |
| t-Wert iid / Woche / Monat | -0.48 / -0.50 / -0.51 |
| Rendite p. a. bei 10 % Volatilität | -1.62% |
| Max. Drawdown bei 10 % Volatilität | 31.2% |
| Zerlegung p. a. bei 10 % Vol.: Kurs / Swaps / Handel / Gebühr | -2.57% / +1.05% / -0.04% / -0.05% |
| Ø Brutto-Exposure (Summe \|w\|, unskaliert) | 4.08 |

| Kriterium | Ergebnis | erfüllt |
|---|---|---|
| Mittleres Netto-Tagesergebnis > 0 mit t ≥ 3,0 (kleinster aus iid / Woche / Monat) | t = -0.51 (Sharpe -0.16) | **nein** |
| ≥ 6 von 9 Jahren positiv | 3 von 9 | **nein** |
| ≥ 60 % der Instrumente (≥ 250 Positionstage) positiv | 4 von 10 | **nein** |
| bei doppelten Kosten > 0 | -2.03% p. a. bei 10 % Vol. | **nein** |

**K-3: nicht bestanden.**

| Jahr | Rendite bei 10 % Vol. | Sharpe |
|---|---|---|
| 2015 | -13.6% | -1.09 |
| 2016 | +3.6% | +0.37 |
| 2017 | -4.1% | -0.47 |
| 2018 | -6.2% | -0.70 |
| 2019 | +5.0% | +0.60 |
| 2020 | -2.2% | -0.17 |
| 2021 | +5.2% | +0.47 |
| 2022 | -1.8% | -0.19 |
| 2023 | -0.5% | -0.08 |

| Instrument | Positionstage | Beitrag netto bei 10 % Vol. (Summe) | davon Swaps |
|---|---|---|---|
| EURCAD | 629 | +7.4% | +0.7% |
| EURUSD | 434 | +4.6% | +0.8% |
| AUDJPY | 436 | +2.8% | -0.3% |
| EURNZD | 304 | +2.5% | +1.0% |
| USDCHF | 2101 | -0.5% | +3.7% |
| NZDJPY | 541 | -1.5% | +1.8% |
| USDJPY | 411 | -2.3% | +0.2% |
| NZDUSD | 1495 | -3.7% | +0.0% |
| CADJPY | 887 | -3.7% | -0.3% |
| EURAUD | 973 | -4.2% | +1.3% |

### Beschreibend

| Auswertung | Sharpe | t (iid) | Rendite p. a. bei 10 % Vol. | Swaps p. a. |
|---|---|---|---|---|
| vorregistriert (Aufschlag 1 %) | -0.16 | -0.48 | -1.62% | +1.05% |
| ohne Swap-Aufschlag | +0.02 | +0.06 | +0.19% | +2.85% |

- 2015–2019: Sharpe -0.31, Kurs -4.42% p. a., Swaps +1.37% p. a. (bei 10 % Vol. des Teilzeitraums)
- 2020–2023: Sharpe +0.02, Kurs -0.36% p. a., Swaps +0.66% p. a. (bei 10 % Vol. des Teilzeitraums)

**Rangfolge der Zinsen (Long- und Short-Seite)**

Monate: 104

| Währung | Monate long | Monate short |
|---|---|---|
| NZD | 104 | 0 |
| CAD | 77 | 0 |
| AUD | 66 | 0 |
| USD | 54 | 0 |
| GBP | 11 | 0 |
| JPY | 0 | 104 |
| EUR | 0 | 104 |
| CHF | 0 | 104 |

## K-1

| Kennzahl | Wert |
|---|---|
| Handelstage | 2,340 |
| Sharpe Ratio p. a. (netto) | -0.02 |
| t-Wert iid / Woche / Monat | -0.05 / -0.05 / -0.06 |
| Rendite p. a. bei 10 % Volatilität | -0.17% |
| Max. Drawdown bei 10 % Volatilität | 23.5% |
| Zerlegung p. a. bei 10 % Vol.: Kurs / Swaps / Handel / Gebühr | -1.43% / +1.30% / -0.02% / -0.02% |
| Ø Brutto-Exposure (Summe \|w\|, unskaliert) | 1.69 |

| Kriterium | Ergebnis | erfüllt |
|---|---|---|
| Mittleres Netto-Tagesergebnis > 0 mit t ≥ 3,0 (kleinster aus iid / Woche / Monat) | t = -0.06 (Sharpe -0.02) | **nein** |
| ≥ 6 von 9 Jahren positiv | 4 von 9 | **nein** |
| ≥ 60 % der Instrumente (≥ 250 Positionstage) positiv | 2 von 3 | ja |
| bei doppelten Kosten > 0 | -0.48% p. a. bei 10 % Vol. | **nein** |

**K-1: nicht bestanden.**

| Jahr | Rendite bei 10 % Vol. | Sharpe |
|---|---|---|
| 2015 | +1.8% | +0.21 |
| 2016 | +4.3% | +0.49 |
| 2017 | -1.2% | -0.12 |
| 2018 | -5.6% | -0.54 |
| 2019 | +4.5% | +0.47 |
| 2020 | -5.8% | -0.45 |
| 2021 | -2.5% | -0.25 |
| 2022 | -5.3% | -0.49 |
| 2023 | +8.2% | +1.05 |

| Instrument | Positionstage | Beitrag netto bei 10 % Vol. (Summe) | davon Swaps |
|---|---|---|---|
| USDCHF | 1819 | +13.1% | +6.1% |
| NZDJPY | 325 | +9.4% | +3.9% |
| NZDUSD | 1495 | -8.3% | +0.1% |

### Beschreibend

| Auswertung | Sharpe | t (iid) | Rendite p. a. bei 10 % Vol. | Swaps p. a. |
|---|---|---|---|---|
| vorregistriert (Aufschlag 1 %) | -0.02 | -0.05 | -0.17% | +1.30% |
| ohne Swap-Aufschlag | +0.15 | +0.45 | +1.51% | +2.98% |

- 2015–2019: Sharpe +0.08, Kurs -0.81% p. a., Swaps +1.66% p. a. (bei 10 % Vol. des Teilzeitraums)
- 2020–2023: Sharpe -0.13, Kurs -2.13% p. a., Swaps +0.90% p. a. (bei 10 % Vol. des Teilzeitraums)

**Rangfolge der Zinsen (Long- und Short-Seite)**

Monate: 104

| Währung | Monate long | Monate short |
|---|---|---|
| NZD | 84 | 0 |
| USD | 15 | 0 |
| CAD | 5 | 0 |
| EUR | 0 | 4 |
| JPY | 0 | 11 |
| CHF | 0 | 89 |

**Ergebnis: Keine Variante erfüllt alle In-Sample-Kriterien. Strategie Nr. 6 ist gescheitert; der Hold-out bleibt unberührt.**
