# Modell ST (Statistische Modelle), In-Sample 2015–2023 (Trial T276–T279)

Lauf vom 24.10.2026. Regeln laut `docs/01_Vorregistrierung.md`, Code `research/stm/`. Tagesbuchhaltung wie Nr. 28/30 (34 Instrumente; Gold-Saison nur XAUUSD), Modelle jährlich nur mit Vorjahresdaten geschätzt. Netto = nach Handelskosten, Swaps und Gebühr.

## ST-HMM (Nr. 81)

| Kennzahl | Wert |
|---|---|
| Handelstage | 2,340 |
| Sharpe Ratio p. a. (netto) | -0.55 |
| t-Wert iid / Woche / Monat | -1.63 / -1.56 / -1.69 |
| Rendite p. a. bei 10 % Volatilität | -5.45% |
| Zerlegung p. a. bei 10 % Vol.: Kurs / Swaps / Handel | +0.82% / -3.45% / -2.25% |
| Ø Brutto-Exposure (unskaliert) | 26.54 |

| Kriterium | Ergebnis | erfüllt |
|---|---|---|
| Mittleres Netto-Tagesergebnis > 0 mit t ≥ 3,0 (kleinster aus iid / Woche / Monat) | t = -1.69 (Sharpe -0.55) | **nein** |
| ≥ 6 von 9 Jahren positiv | 1 von 9 | **nein** |
| ≥ 60 % der Instrumente (≥ 250 Positionstage) positiv | 9 von 34 | **nein** |
| bei doppelten Kosten > 0 | -12.43% p. a. bei 10 % Vol. | **nein** |

**ST-HMM: nicht bestanden.**

| Jahr | Rendite bei 10 % Vol. |
|---|---|
| 2015 | -8.9% |
| 2016 | -2.8% |
| 2017 | -8.2% |
| 2018 | +9.3% |
| 2019 | -5.7% |
| 2020 | -1.5% |
| 2021 | -16.1% |
| 2022 | -4.4% |
| 2023 | -10.7% |

## ST-GARCH (Nr. 82)

| Kennzahl | Wert |
|---|---|
| Handelstage | 2,340 |
| Sharpe Ratio p. a. (netto) | -0.50 |
| t-Wert iid / Woche / Monat | -1.51 / -1.47 / -1.74 |
| Rendite p. a. bei 10 % Volatilität | -5.05% |
| Zerlegung p. a. bei 10 % Vol.: Kurs / Swaps / Handel | -0.67% / -2.76% / -1.25% |
| Ø Brutto-Exposure (unskaliert) | 33.59 |

| Kriterium | Ergebnis | erfüllt |
|---|---|---|
| Mittleres Netto-Tagesergebnis > 0 mit t ≥ 3,0 (kleinster aus iid / Woche / Monat) | t = -1.74 (Sharpe -0.50) | **nein** |
| ≥ 6 von 9 Jahren positiv | 3 von 9 | **nein** |
| ≥ 60 % der Instrumente (≥ 250 Positionstage) positiv | 12 von 34 | **nein** |
| bei doppelten Kosten > 0 | -9.93% p. a. bei 10 % Vol. | **nein** |

**ST-GARCH: nicht bestanden.**

| Jahr | Rendite bei 10 % Vol. |
|---|---|
| 2015 | -18.7% |
| 2016 | -4.3% |
| 2017 | -4.6% |
| 2018 | +3.5% |
| 2019 | -3.2% |
| 2020 | +2.0% |
| 2021 | -13.5% |
| 2022 | +2.7% |
| 2023 | -9.1% |

## ST-KNN (Nr. 85)

| Kennzahl | Wert |
|---|---|
| Handelstage | 2,340 |
| Sharpe Ratio p. a. (netto) | -2.02 |
| t-Wert iid / Woche / Monat | -6.06 / -6.27 / -6.16 |
| Rendite p. a. bei 10 % Volatilität | -20.22% |
| Zerlegung p. a. bei 10 % Vol.: Kurs / Swaps / Handel | -0.46% / -5.92% / -11.84% |
| Ø Brutto-Exposure (unskaliert) | 35.06 |

| Kriterium | Ergebnis | erfüllt |
|---|---|---|
| Mittleres Netto-Tagesergebnis > 0 mit t ≥ 3,0 (kleinster aus iid / Woche / Monat) | t = -6.27 (Sharpe -2.02) | **nein** |
| ≥ 6 von 9 Jahren positiv | 0 von 9 | **nein** |
| ≥ 60 % der Instrumente (≥ 250 Positionstage) positiv | 8 von 34 | **nein** |
| bei doppelten Kosten > 0 | -41.06% p. a. bei 10 % Vol. | **nein** |

**ST-KNN: nicht bestanden.**

| Jahr | Rendite bei 10 % Vol. |
|---|---|
| 2015 | -6.1% |
| 2016 | -11.9% |
| 2017 | -16.4% |
| 2018 | -29.9% |
| 2019 | -26.6% |
| 2020 | -27.1% |
| 2021 | -21.7% |
| 2022 | -21.4% |
| 2023 | -20.4% |

## ST-GOLD (Nr. 90)

| Kennzahl | Wert |
|---|---|
| Handelstage | 2,330 |
| Sharpe Ratio p. a. (netto) | -0.10 |
| t-Wert iid / Woche / Monat | -0.31 / -0.29 / -0.31 |
| Rendite p. a. bei 10 % Volatilität | -1.05% |
| Zerlegung p. a. bei 10 % Vol.: Kurs / Swaps / Handel | -0.22% / -0.79% / -0.03% |
| Ø Brutto-Exposure (unskaliert) | 0.25 |

| Kriterium | Ergebnis | erfüllt |
|---|---|---|
| Mittleres Netto-Tagesergebnis > 0 mit t ≥ 3,0 (kleinster aus iid / Woche / Monat) | t = -0.31 (Sharpe -0.10) | **nein** |
| ≥ 6 von 9 Jahren positiv | 2 von 9 | **nein** |
| beide Teilzeiträume 2015–2019 und 2020–2023 positiv | -1.47 / +1.25 bp/Tag | **nein** |
| bei doppelten Kosten > 0 | -1.87% p. a. bei 10 % Vol. | **nein** |

**ST-GOLD: nicht bestanden.**

| Jahr | Rendite bei 10 % Vol. |
|---|---|
| 2015 | -10.5% |
| 2016 | -9.3% |
| 2017 | -4.7% |
| 2018 | -1.0% |
| 2019 | -4.0% |
| 2020 | +27.9% |
| 2021 | -7.8% |
| 2022 | +4.7% |
| 2023 | -4.7% |

## Übersicht

| Variante | Nr. | Sharpe | t | Rendite p. a. bei 10 % Vol. | Jahre + | Instr. + |
|---|---|---|---|---|---|---|
| ST-HMM | 81 | -0.55 | -1.69 | -5.45% | 1 | 9 von 34 |
| ST-GARCH | 82 | -0.50 | -1.74 | -5.05% | 3 | 12 von 34 |
| ST-KNN | 85 | -2.02 | -6.27 | -20.22% | 0 | 8 von 34 |
| ST-GOLD | 90 | -0.10 | -0.31 | -1.05% | 2 | 0 von 1 |

**Ergebnis: Keine Variante erfüllt alle In-Sample-Kriterien. Strategien Nr. 81, 82, 85 und 90 sind gescheitert; der Hold-out bleibt unberührt.**
