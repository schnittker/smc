# Modell S (Halloween US-Indizes), In-Sample 2015–2023 (Trial T92 S-SPX, T93 S-NDX)

Lauf vom 24.10.2026. Regeln laut `docs/01_Vorregistrierung.md`, Code `research/hallo/`. Tagesbuchhaltung von Modell G (15:50 New York) mit Index-Kosten und -Swaps (Modell H). Netto = nach Handelskosten und Swaps. Long 1 × Kapital von November bis April; Renditen unskaliert und zusätzlich auf 10 % Volatilität skaliert (nur zur Einordnung).

## S-SPX

| Kennzahl | Wert |
|---|---|
| Handelstage | 2,324 |
| Rendite / Volatilität p. a. (unskaliert) | +5.06% / 13.5% |
| Sharpe Ratio p. a. (netto) | 0.37 |
| t-Wert iid / Woche / Monat | 1.12 / 1.08 / 1.30 |
| Zerlegung p. a. (unskaliert): Kurs / Swaps / Handel | +6.09% / -1.02% / -0.01% |
| Ø / max. Gewicht w | 0.49 / 1.00 |
| bei 10 % Vol.: Rendite p. a. / max. Drawdown / schlechtester Tag | +3.75% / 30.2% / -6.22% |

| Kriterium | Ergebnis | erfüllt |
|---|---|---|
| Mittleres Netto-Tagesergebnis > 0 mit t ≥ 3,0 (kleinster aus iid / Woche / Monat) | t = 1.08 (Sharpe 0.37) | **nein** |
| ≥ 6 von 9 Jahren positiv | 6 von 9 | ja |
| beide Teilzeiträume 2015–2019 und 2020–2023 positiv | +2.11 / +1.72 bp/Tag | ja |
| bei doppelten Kosten > 0 | +4.02% p. a. (unskaliert) | ja |

**S-SPX: nicht bestanden.**

| Jahr | Rendite (unskaliert) |
|---|---|
| 2015 | -0.4% |
| 2016 | +7.6% |
| 2017 | +10.1% |
| 2018 | -10.6% |
| 2019 | +20.5% |
| 2020 | +2.6% |
| 2021 | +15.2% |
| 2022 | -16.6% |
| 2023 | +16.7% |

## S-NDX

| Kennzahl | Wert |
|---|---|
| Handelstage | 2,324 |
| Rendite / Volatilität p. a. (unskaliert) | +7.37% / 15.8% |
| Sharpe Ratio p. a. (netto) | 0.47 |
| t-Wert iid / Woche / Monat | 1.39 / 1.40 / 1.61 |
| Zerlegung p. a. (unskaliert): Kurs / Swaps / Handel | +8.89% / -1.51% / -0.01% |
| Ø / max. Gewicht w | 0.49 / 1.00 |
| bei 10 % Vol.: Rendite p. a. / max. Drawdown / schlechtester Tag | +4.66% / 20.6% / -4.99% |

| Kriterium | Ergebnis | erfüllt |
|---|---|---|
| Mittleres Netto-Tagesergebnis > 0 mit t ≥ 3,0 (kleinster aus iid / Woche / Monat) | t = 1.39 (Sharpe 0.47) | **nein** |
| ≥ 6 von 9 Jahren positiv | 6 von 9 | ja |
| beide Teilzeiträume 2015–2019 und 2020–2023 positiv | +2.75 / +2.92 bp/Tag | ja |
| bei doppelten Kosten > 0 | +5.85% p. a. (unskaliert) | ja |

**S-NDX: nicht bestanden.**

| Jahr | Rendite (unskaliert) |
|---|---|
| 2015 | +2.9% |
| 2016 | -3.0% |
| 2017 | +16.6% |
| 2018 | -8.1% |
| 2019 | +27.0% |
| 2020 | +17.5% |
| 2021 | +10.5% |
| 2022 | -27.7% |
| 2023 | +29.9% |

# Beschreibend

| Index | Halten Sharpe | Winter (Nov–Apr) Ø Tagesrendite bp | Sommer (Mai–Okt) Ø bp | Differenz t |
|---|---|---|---|---|
| SPXUSD | 0.51 | +5.36 | +3.10 | +0.50 |
| NSXUSD | 0.69 | +7.26 | +6.36 | +0.17 |

**Ergebnis: Keine Variante erfüllt alle In-Sample-Kriterien. Strategie Nr. 27 ist gescheitert; der Hold-out bleibt unberührt.**
