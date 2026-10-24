# Modell V (volatilitätsgesteuertes US500-Long), In-Sample 2015–2023 (Trial T48 V-VOL, T49 V-MM)

Lauf vom 24.10.2026. Regeln laut `docs/01_Vorregistrierung.md`, Code `research/volm/`. Tagesbuchhaltung von Modell G (15:50 New York) mit Index-Kosten und -Swaps (Modell H). Netto = nach Handelskosten und Swaps. Renditen unskaliert (Gewicht w wie vorregistriert) und zusätzlich auf 10 % Volatilität skaliert (nur zur Einordnung).

## V-VOL

| Kennzahl | Wert |
|---|---|
| Handelstage | 2,324 |
| Rendite / Volatilität p. a. (unskaliert) | +9.47% / 16.8% |
| Sharpe Ratio p. a. (netto) | 0.56 |
| t-Wert iid / Woche / Monat | 1.68 / 1.69 / 1.72 |
| Zerlegung p. a. (unskaliert): Kurs / Swaps / Handel | +12.28% / -2.73% / -0.08% |
| Ø / max. Gewicht w | 1.29 / 3.00 |
| bei 10 % Vol.: Rendite p. a. / max. Drawdown / schlechtester Tag | +5.63% / 15.8% / -4.07% |

| Kriterium | Ergebnis | erfüllt |
|---|---|---|
| Mittleres Netto-Tagesergebnis > 0 mit t ≥ 3,0 (kleinster aus iid / Woche / Monat) | t = 1.68 (Sharpe 0.56) | **nein** |
| ≥ 6 von 9 Jahren positiv | 6 von 9 | ja |
| beide Teilzeiträume 2015–2019 und 2020–2023 positiv | +4.18 / +2.94 bp/Tag | ja |
| bei doppelten Kosten > 0 | +6.67% p. a. (unskaliert) | ja |

**V-VOL: nicht bestanden.**

| Jahr | Rendite (unskaliert) |
|---|---|
| 2015 | -5.5% |
| 2016 | +8.0% |
| 2017 | +38.7% |
| 2018 | -5.5% |
| 2019 | +18.2% |
| 2020 | +11.6% |
| 2021 | +22.2% |
| 2022 | -20.1% |
| 2023 | +16.7% |

## V-MM

| Kennzahl | Wert |
|---|---|
| Handelstage | 2,324 |
| Rendite / Volatilität p. a. (unskaliert) | +7.85% / 24.5% |
| Sharpe Ratio p. a. (netto) | 0.32 |
| t-Wert iid / Woche / Monat | 0.96 / 0.96 / 1.10 |
| Zerlegung p. a. (unskaliert): Kurs / Swaps / Handel | +11.28% / -3.38% / -0.05% |
| Ø / max. Gewicht w | 1.58 / 3.00 |
| bei 10 % Vol.: Rendite p. a. / max. Drawdown / schlechtester Tag | +3.21% / 17.9% / -4.19% |

| Kriterium | Ergebnis | erfüllt |
|---|---|---|
| Mittleres Netto-Tagesergebnis > 0 mit t ≥ 3,0 (kleinster aus iid / Woche / Monat) | t = 0.96 (Sharpe 0.32) | **nein** |
| ≥ 6 von 9 Jahren positiv | 5 von 9 | **nein** |
| beide Teilzeiträume 2015–2019 und 2020–2023 positiv | +3.73 / +2.10 bp/Tag | ja |
| bei doppelten Kosten > 0 | +4.41% p. a. (unskaliert) | ja |

**V-MM: nicht bestanden.**

| Jahr | Rendite (unskaliert) |
|---|---|
| 2015 | -18.7% |
| 2016 | +15.1% |
| 2017 | +50.2% |
| 2018 | -8.7% |
| 2019 | +10.2% |
| 2020 | -4.6% |
| 2021 | +25.5% |
| 2022 | -15.6% |
| 2023 | +16.5% |

# Beschreibend

## Referenz: konstant w = 1 (US500 halten)

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
| V-VOL | +0.77 | +2.29 | +12.76% | 6 von 9 |
| V-MM | +0.56 | +1.68 | +11.65% | 7 von 9 |
| KONSTANT | +0.69 | +2.06 | +14.63% | 7 von 9 |

**Ergebnis: Keine Variante erfüllt alle In-Sample-Kriterien. Strategie Nr. 14 ist gescheitert; der Hold-out bleibt unberührt.**
