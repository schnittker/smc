# Modell I (Intraday-Momentum US500), In-Sample 2015–2023 (Trial T39 I-ONFH, T40 I-ROD)

Lauf vom 24.10.2026. Regeln laut `docs/01_Vorregistrierung.md`, Code `research/imom/`. Volle NYSE-Handelstage; Position 15:30–16:00 New York in Richtung des Signals. Netto = nach Spread (FTMO-Durchschnitt) und Slippage (¼ Spread je Ausführung); Ergebnisse in Basispunkten.

## I-ONFH

| Kennzahl | Wert |
|---|---|
| Handelstage | 2,102 |
| Netto je Tag | +0.44 bp (σ 31.0 bp) |
| vor Kosten je Tag | +1.58 bp |
| Kosten je Tag | 1.13 bp |
| Sharpe Ratio p. a. (netto) | 0.22 |
| t-Wert iid / Woche / Monat | 0.65 / 0.63 / 0.52 |
| Trefferquote | 49% |
| Notfall-Stops | 10 |
| bei doppelten Kosten | -0.69 bp/Tag |

| Kriterium | Ergebnis | erfüllt |
|---|---|---|
| Mittleres Netto-Tagesergebnis > 0 mit t ≥ 3,0 (kleinster aus iid / Woche / Monat) | +0.44 bp/Tag, t = 0.52 | **nein** |
| ≥ 6 von 9 Jahren positiv | 5 von 9 | **nein** |
| beide Teilzeiträume 2015–2019 und 2020–2023 positiv | -0.18 / +1.29 bp | **nein** |
| bei doppelten Kosten > 0 | -0.69 bp/Tag | **nein** |

**I-ONFH: nicht bestanden.**

| Jahr | Tage | Netto Ø bp | t |
|---|---|---|---|
| 2015 | 247 | +1.54 | +1.06 |
| 2016 | 247 | -1.26 | -1.21 |
| 2017 | 232 | -1.59 | -2.56 |
| 2018 | 244 | +1.93 | +1.02 |
| 2019 | 246 | -1.57 | -1.77 |
| 2020 | 248 | +4.78 | +1.13 |
| 2021 | 250 | -1.42 | -1.24 |
| 2022 | 249 | +0.06 | +0.03 |
| 2023 | 139 | +2.15 | +1.47 |

### Beschreibend

| Regression von r_LAST auf | Steigung | t (Cluster Monat) | R² |
|---|---|---|---|
| r_onfh | +0.0504 | +1.52 | 0.0162 |
| r_rod | +0.0383 | +3.45 | 0.0179 |

| Teilmenge | Tage | Netto Ø bp | vor Kosten Ø bp | t |
|---|---|---|---|---|
| Long | 1108 | +0.72 | +1.85 | +0.90 |
| Short | 994 | +0.13 | +1.27 | +0.12 |
| großes Signal (oberstes Drittel) | 701 | +1.99 | +3.12 | +1.16 |
| übrige | 1401 | -0.33 | +0.80 | -0.61 |

## I-ROD

| Kennzahl | Wert |
|---|---|
| Handelstage | 2,104 |
| Netto je Tag | +1.00 bp (σ 31.0 bp) |
| vor Kosten je Tag | +2.14 bp |
| Kosten je Tag | 1.13 bp |
| Sharpe Ratio p. a. (netto) | 0.49 |
| t-Wert iid / Woche / Monat | 1.48 / 1.54 / 1.31 |
| Trefferquote | 50% |
| Notfall-Stops | 14 |
| bei doppelten Kosten | -0.13 bp/Tag |

| Kriterium | Ergebnis | erfüllt |
|---|---|---|
| Mittleres Netto-Tagesergebnis > 0 mit t ≥ 3,0 (kleinster aus iid / Woche / Monat) | +1.00 bp/Tag, t = 1.31 | **nein** |
| ≥ 6 von 9 Jahren positiv | 4 von 9 | **nein** |
| beide Teilzeiträume 2015–2019 und 2020–2023 positiv | +0.61 / +1.54 bp | ja |
| bei doppelten Kosten > 0 | -0.13 bp/Tag | **nein** |

**I-ROD: nicht bestanden.**

| Jahr | Tage | Netto Ø bp | t |
|---|---|---|---|
| 2015 | 247 | +2.91 | +1.98 |
| 2016 | 245 | -0.65 | -0.62 |
| 2017 | 236 | -1.87 | -3.03 |
| 2018 | 244 | +3.05 | +1.62 |
| 2019 | 246 | -0.49 | -0.52 |
| 2020 | 248 | +2.62 | +0.62 |
| 2021 | 250 | -0.31 | -0.27 |
| 2022 | 249 | +3.61 | +1.66 |
| 2023 | 139 | -0.76 | -0.51 |

### Beschreibend

| Regression von r_LAST auf | Steigung | t (Cluster Monat) | R² |
|---|---|---|---|
| r_onfh | +0.0504 | +1.52 | 0.0162 |
| r_rod | +0.0383 | +3.45 | 0.0179 |

| Teilmenge | Tage | Netto Ø bp | vor Kosten Ø bp | t |
|---|---|---|---|---|
| Long | 1134 | +1.03 | +2.16 | +1.23 |
| Short | 970 | +0.97 | +2.11 | +0.89 |
| großes Signal (oberstes Drittel) | 702 | +3.43 | +4.57 | +2.03 |
| übrige | 1402 | -0.22 | +0.92 | -0.39 |

## US100 (beschreibend)

| Variante | Tage | Netto Ø bp | vor Kosten Ø bp | t | Jahre positiv |
|---|---|---|---|---|---|
| I-ONFH | 2115 | +1.01 | +1.90 | +1.05 | 5 von 9 |
| I-ROD | 2114 | +1.85 | +2.75 | +2.18 | 6 von 9 |

**Ergebnis: Keine Variante erfüllt alle In-Sample-Kriterien. Strategie Nr. 11 ist gescheitert; der Hold-out bleibt unberührt.**
