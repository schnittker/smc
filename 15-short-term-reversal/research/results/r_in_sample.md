# Modell R (Kurzfrist-Reversal US500, Connors), In-Sample 2015–2023 (Trial T52 R-RSI2, T53 R-7S)

Lauf vom 24.10.2026. Regeln laut `docs/01_Vorregistrierung.md`, Code `research/strev/`. Tagesbuchhaltung von Modell G (15:50 New York) mit Index-Kosten und -Swaps (Modell H). Netto = nach Handelskosten und Swaps. Position 1 × Kapital oder flat; Renditen unskaliert und zusätzlich auf 10 % Volatilität skaliert (nur zur Einordnung).

## R-RSI2

| Kennzahl | Wert |
|---|---|
| Handelstage | 2,324 |
| Rendite / Volatilität p. a. (unskaliert) | +1.99% / 6.4% |
| Sharpe Ratio p. a. (netto) | 0.31 |
| t-Wert iid / Woche / Monat | 0.93 / 0.78 / 0.94 |
| Zerlegung p. a. (unskaliert): Kurs / Swaps / Handel | +2.36% / -0.28% / -0.09% |
| Ø / max. Gewicht w | 0.11 / 1.00 |
| bei 10 % Vol.: Rendite p. a. / max. Drawdown / schlechtester Tag | +3.11% / 22.2% / -5.91% |

| Kriterium | Ergebnis | erfüllt |
|---|---|---|
| Mittleres Netto-Tagesergebnis > 0 mit t ≥ 3,0 (kleinster aus iid / Woche / Monat) | t = 0.78 (Sharpe 0.31) | **nein** |
| ≥ 6 von 9 Jahren positiv | 6 von 9 | ja |
| beide Teilzeiträume 2015–2019 und 2020–2023 positiv | +0.94 / +0.54 bp/Tag | ja |
| bei doppelten Kosten > 0 | +1.62% p. a. (unskaliert) | ja |

**R-RSI2: nicht bestanden.**

| Jahr | Rendite (unskaliert) |
|---|---|
| 2015 | +2.9% |
| 2016 | +3.4% |
| 2017 | +5.1% |
| 2018 | -0.9% |
| 2019 | +1.6% |
| 2020 | +2.5% |
| 2021 | +15.4% |
| 2022 | -3.8% |
| 2023 | -8.6% |

| Trades | Trefferquote | Ø Ergebnis je Trade | Ø Haltedauer (Handelstage) | Zeit im Markt |
|---|---|---|---|---|
| 69 | 70% | +25.7 bp | 3.8 | 11% |

## R-7S

| Kennzahl | Wert |
|---|---|
| Handelstage | 2,324 |
| Rendite / Volatilität p. a. (unskaliert) | +3.30% / 11.9% |
| Sharpe Ratio p. a. (netto) | 0.28 |
| t-Wert iid / Woche / Monat | 0.83 / 0.83 / 1.07 |
| Zerlegung p. a. (unskaliert): Kurs / Swaps / Handel | +4.10% / -0.69% / -0.11% |
| Ø / max. Gewicht w | 0.32 / 1.00 |
| bei 10 % Vol.: Rendite p. a. / max. Drawdown / schlechtester Tag | +2.78% / 32.9% / -7.06% |

| Kriterium | Ergebnis | erfüllt |
|---|---|---|
| Mittleres Netto-Tagesergebnis > 0 mit t ≥ 3,0 (kleinster aus iid / Woche / Monat) | t = 0.83 (Sharpe 0.28) | **nein** |
| ≥ 6 von 9 Jahren positiv | 5 von 9 | **nein** |
| beide Teilzeiträume 2015–2019 und 2020–2023 positiv | +2.22 / +0.08 bp/Tag | ja |
| bei doppelten Kosten > 0 | +2.50% p. a. (unskaliert) | ja |

**R-7S: nicht bestanden.**

| Jahr | Rendite (unskaliert) |
|---|---|
| 2015 | +2.0% |
| 2016 | +14.9% |
| 2017 | +9.0% |
| 2018 | -3.8% |
| 2019 | +6.5% |
| 2020 | -16.7% |
| 2021 | +23.0% |
| 2022 | -4.5% |
| 2023 | -0.9% |

| Trades | Trefferquote | Ø Ergebnis je Trade | Ø Haltedauer (Handelstage) | Zeit im Markt |
|---|---|---|---|---|
| 88 | 77% | +33.4 bp | 8.5 | 32% |

# Beschreibend

## Referenz: US500 halten (w = 1)

| Kennzahl | Wert |
|---|---|
| Handelstage | 2,324 |
| Rendite / Volatilität p. a. (unskaliert) | +8.88% / 17.5% |
| Sharpe Ratio p. a. (netto) | 0.51 |
| t-Wert iid / Woche / Monat | 1.51 / 1.51 / 1.72 |
| Zerlegung p. a. (unskaliert): Kurs / Swaps / Handel | +10.99% / -2.11% / -0.00% |
| Ø / max. Gewicht w | 1.00 / 1.00 |
| bei 10 % Vol.: Rendite p. a. / max. Drawdown / schlechtester Tag | +5.08% / 23.3% / -4.79% |

| Jahr | Rendite (unskaliert) |
|---|---|
| 2015 | -0.3% |
| 2016 | +8.6% |
| 2017 | +17.0% |
| 2018 | -8.3% |
| 2019 | +23.7% |
| 2020 | +18.8% |
| 2021 | +24.4% |
| 2022 | -21.7% |
| 2023 | +17.0% |

## US100

| Variante | Sharpe | t (iid) | Rendite p. a. | Jahre positiv |
|---|---|---|---|---|
| R-RSI2 | +0.40 | +1.20 | +3.26% | 7 von 9 |
| R-7S | +0.37 | +1.10 | +4.89% | 7 von 9 |
| HALTEN | +0.69 | +2.06 | +14.63% | 7 von 9 |

**Ergebnis: Keine Variante erfüllt alle In-Sample-Kriterien. Strategie Nr. 15 ist gescheitert; der Hold-out bleibt unberührt.**
