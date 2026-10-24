# Modell R (Rohstoff-Lead-Lag), In-Sample 2015–2023 (Trial T80 R-OEL, T81 R-GOLD)

Lauf vom 24.10.2026. Regeln laut `docs/01_Vorregistrierung.md`, Code `research/cfx/`. Signal: Rohstoffrendite bis 15:45 New York; Position im FX-Paar ab 16:50 (Tagesbuchhaltung von Modell G, FX-Kosten, Swaps, Gebühr). Renditen unskaliert und zusätzlich auf 10 % Volatilität skaliert.

## R-OEL

| Kennzahl | Wert |
|---|---|
| Handelstage | 2,340 |
| Rendite / Volatilität p. a. (unskaliert) | -4.17% / 10.1% |
| Sharpe Ratio p. a. (netto) | -0.41 |
| t-Wert iid / Woche / Monat | -1.23 / -1.22 / -1.19 |
| Zerlegung p. a. (unskaliert): Kurs / Swaps / Handel | -0.26% / -1.40% / -1.92% |
| Ø / max. Gewicht w | -0.08 / 2.50 |
| bei 10 % Vol.: Rendite p. a. / max. Drawdown / schlechtester Tag | -4.11% / 55.4% / -2.30% |

| Kriterium | Ergebnis | erfüllt |
|---|---|---|
| Mittleres Netto-Tagesergebnis > 0 mit t ≥ 3,0 (kleinster aus iid / Woche / Monat) | t = -1.23 (Sharpe -0.41) | **nein** |
| ≥ 6 von 9 Jahren positiv | 2 von 9 | **nein** |
| beide Teilzeiträume 2015–2019 und 2020–2023 positiv | -2.26 / -0.77 bp/Tag | **nein** |
| bei doppelten Kosten > 0 | -8.08% p. a. (unskaliert) | **nein** |

**R-OEL: nicht bestanden.**

| Jahr | Rendite (unskaliert) |
|---|---|
| 2015 | -10.9% |
| 2016 | -17.4% |
| 2017 | +7.9% |
| 2018 | -5.6% |
| 2019 | -3.3% |
| 2020 | +18.0% |
| 2021 | -4.5% |
| 2022 | -20.5% |
| 2023 | -1.1% |

## R-GOLD

| Kennzahl | Wert |
|---|---|
| Handelstage | 2,340 |
| Rendite / Volatilität p. a. (unskaliert) | +2.14% / 10.2% |
| Sharpe Ratio p. a. (netto) | 0.21 |
| t-Wert iid / Woche / Monat | 0.63 / 0.65 / 0.64 |
| Zerlegung p. a. (unskaliert): Kurs / Swaps / Handel | +5.28% / -1.08% / -2.06% |
| Ø / max. Gewicht w | 0.06 / 1.67 |
| bei 10 % Vol.: Rendite p. a. / max. Drawdown / schlechtester Tag | +2.10% / 22.9% / -3.19% |

| Kriterium | Ergebnis | erfüllt |
|---|---|---|
| Mittleres Netto-Tagesergebnis > 0 mit t ≥ 3,0 (kleinster aus iid / Woche / Monat) | t = 0.63 (Sharpe 0.21) | **nein** |
| ≥ 6 von 9 Jahren positiv | 6 von 9 | ja |
| beide Teilzeiträume 2015–2019 und 2020–2023 positiv | +0.06 / +1.77 bp/Tag | ja |
| bei doppelten Kosten > 0 | -1.07% p. a. (unskaliert) | **nein** |

**R-GOLD: nicht bestanden.**

| Jahr | Rendite (unskaliert) |
|---|---|
| 2015 | -13.0% |
| 2016 | +11.1% |
| 2017 | +1.6% |
| 2018 | -12.9% |
| 2019 | +14.0% |
| 2020 | +5.2% |
| 2021 | -4.6% |
| 2022 | +4.5% |
| 2023 | +13.3% |

# Beschreibend

| Variante | Korrelation gleichzeitig (Rohstoff vs. FX, gleicher Tag) | Korrelation Signal vs. Folgetag |
|---|---|---|
| R-OEL | +0.416 | +0.013 |
| R-GOLD | +0.380 | +0.034 |

**Ergebnis: Keine Variante erfüllt alle In-Sample-Kriterien. Strategie Nr. 23 ist gescheitert; der Hold-out bleibt unberührt.**
