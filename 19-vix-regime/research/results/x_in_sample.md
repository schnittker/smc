# Modell X (VIX-Regime), In-Sample 2015–2023 (Trial T64 X-HAVEN, T65 X-FEAR)

Lauf vom 24.10.2026. Regeln laut `docs/01_Vorregistrierung.md`, Code `research/vixr/`. Risk-off = VIX ≥ 90-%-Quantil der 252 Vortage (Cboe). Tagesbuchhaltung von Modell G; Netto = nach Handelskosten, Swaps und Gebühr. Renditen unskaliert und zusätzlich auf 10 % Volatilität skaliert (nur zur Einordnung).

## X-HAVEN

| Kennzahl | Wert |
|---|---|
| Handelstage | 2,340 |
| Rendite / Volatilität p. a. (unskaliert) | -1.96% / 14.4% |
| Sharpe Ratio p. a. (netto) | -0.14 |
| t-Wert iid / Woche / Monat | -0.41 / -0.37 / -0.65 |
| Zerlegung p. a. (unskaliert): Kurs / Swaps / Handel | -0.74% / -0.89% / -0.24% |
| Ø / max. Gewicht w | -0.22 / 0.00 |
| bei 10 % Vol.: Rendite p. a. / max. Drawdown / schlechtester Tag | -1.36% / 27.4% / -7.00% |

| Kriterium | Ergebnis | erfüllt |
|---|---|---|
| Mittleres Netto-Tagesergebnis > 0 mit t ≥ 3,0 (kleinster aus iid / Woche / Monat) | t = -0.65 (Sharpe -0.14) | **nein** |
| ≥ 6 von 9 Jahren positiv | 3 von 9 | **nein** |
| beide Teilzeiträume 2015–2019 und 2020–2023 positiv | -0.19 / -1.44 bp/Tag | **nein** |
| bei doppelten Kosten > 0 | -3.17% p. a. (unskaliert) | **nein** |

**X-HAVEN: nicht bestanden.**

| Jahr | Rendite (unskaliert) |
|---|---|
| 2015 | +7.0% |
| 2016 | -6.6% |
| 2017 | -2.8% |
| 2018 | +3.1% |
| 2019 | -3.2% |
| 2020 | +9.6% |
| 2021 | -1.4% |
| 2022 | -23.2% |
| 2023 | +0.0% |

## X-FEAR

| Kennzahl | Wert |
|---|---|
| Handelstage | 2,324 |
| Rendite / Volatilität p. a. (unskaliert) | +0.33% / 7.8% |
| Sharpe Ratio p. a. (netto) | 0.04 |
| t-Wert iid / Woche / Monat | 0.13 / 0.13 / 0.22 |
| Zerlegung p. a. (unskaliert): Kurs / Swaps / Handel | +0.51% / -0.13% / -0.04% |
| Ø / max. Gewicht w | 0.08 / 1.45 |
| bei 10 % Vol.: Rendite p. a. / max. Drawdown / schlechtester Tag | +0.42% / 30.2% / -7.38% |

| Kriterium | Ergebnis | erfüllt |
|---|---|---|
| Mittleres Netto-Tagesergebnis > 0 mit t ≥ 3,0 (kleinster aus iid / Woche / Monat) | t = 0.13 (Sharpe 0.04) | **nein** |
| ≥ 6 von 9 Jahren positiv | 6 von 9 | ja |
| beide Teilzeiträume 2015–2019 und 2020–2023 positiv | +0.40 / -0.22 bp/Tag | **nein** |
| bei doppelten Kosten > 0 | +0.16% p. a. (unskaliert) | ja |

**X-FEAR: nicht bestanden.**

| Jahr | Rendite (unskaliert) |
|---|---|
| 2015 | +4.8% |
| 2016 | +1.5% |
| 2017 | +1.0% |
| 2018 | -2.5% |
| 2019 | +0.4% |
| 2020 | -3.7% |
| 2021 | +1.0% |
| 2022 | +0.4% |
| 2023 | +0.0% |

# Beschreibend

Risk-off an 11% der VIX-Handelstage 2015–2023, 48 Episoden.

| Instrument | Positionstage | Netto Summe (unskaliert) |
|---|---|---|
| X-HAVEN USDCHF | 259 | -9.96% |
| X-HAVEN USDJPY | 259 | -10.57% |
| X-HAVEN XAUUSD | 255 | +2.99% |
| X-FEAR SPXUSD | 260 | +2.96% |

**Ergebnis: Keine Variante erfüllt alle In-Sample-Kriterien. Strategie Nr. 19 ist gescheitert; der Hold-out bleibt unberührt.**
