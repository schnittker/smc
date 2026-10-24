# Modell N (Overnight-Drift US500), In-Sample 2015–2023 (Trial T43 N-NACHT, T44 N-EU, T45 N-EU-DOWN)

Lauf vom 24.10.2026. Regeln laut `docs/01_Vorregistrierung.md`, Code `research/ovn/`. NYSE-Handelstage; Long US500. Netto = nach Spread (FTMO-Durchschnitt), Slippage (¼ Spread je Ausführung) und Swaps; Ergebnisse in Basispunkten.

## N-NACHT

| Kennzahl | Wert |
|---|---|
| Handelstage | 2,152 |
| Netto je Tag | +0.22 bp (σ 71.7 bp) |
| vor Kosten je Tag | +2.14 bp |
| Kosten je Tag (davon Swap) | 1.92 bp (0.79 bp) |
| Sharpe Ratio p. a. (netto) | 0.05 |
| t-Wert iid / Woche / Monat | 0.14 / 0.17 / 0.17 |
| Trefferquote | 52% |
| Notfall-Stops | 6 |
| bei doppelten Kosten | -1.70 bp/Tag |

| Kriterium | Ergebnis | erfüllt |
|---|---|---|
| Mittleres Netto-Ergebnis je Trade > 0 mit t ≥ 3,0 (kleinster aus iid / Woche / Monat) | +0.22 bp/Tag, t = 0.14 | **nein** |
| ≥ 6 von 9 Jahren positiv | 5 von 9 | **nein** |
| beide Teilzeiträume 2015–2019 und 2020–2023 positiv | +0.11 / +0.36 bp | ja |
| bei doppelten Kosten > 0 | -1.70 bp/Tag | **nein** |

**N-NACHT: nicht bestanden.**

| Jahr | Tage | Netto Ø bp | t |
|---|---|---|---|
| 2015 | 249 | +0.39 | +0.10 |
| 2016 | 251 | -1.22 | -0.33 |
| 2017 | 242 | +1.17 | +0.70 |
| 2018 | 248 | -1.96 | -0.50 |
| 2019 | 249 | +2.22 | +0.68 |
| 2020 | 248 | +6.62 | +0.77 |
| 2021 | 251 | +0.57 | +0.18 |
| 2022 | 250 | -2.56 | -0.46 |
| 2023 | 164 | -4.97 | -1.35 |

## N-EU

| Kennzahl | Wert |
|---|---|
| Handelstage | 2,195 |
| Netto je Tag | -0.51 bp (σ 15.4 bp) |
| vor Kosten je Tag | +0.63 bp |
| Kosten je Tag (davon Swap) | 1.13 bp (0.00 bp) |
| Sharpe Ratio p. a. (netto) | -0.51 |
| t-Wert iid / Woche / Monat | -1.54 / -1.49 / -1.18 |
| Trefferquote | 46% |
| Notfall-Stops | 0 |
| bei doppelten Kosten | -1.64 bp/Tag |

| Kriterium | Ergebnis | erfüllt |
|---|---|---|
| Mittleres Netto-Ergebnis je Trade > 0 mit t ≥ 3,0 (kleinster aus iid / Woche / Monat) | -0.51 bp/Tag, t = -1.54 | **nein** |
| ≥ 6 von 9 Jahren positiv | 2 von 9 | **nein** |
| beide Teilzeiträume 2015–2019 und 2020–2023 positiv | -0.47 / -0.56 bp | **nein** |
| bei doppelten Kosten > 0 | -1.64 bp/Tag | **nein** |

**N-EU: nicht bestanden.**

| Jahr | Tage | Netto Ø bp | t |
|---|---|---|---|
| 2015 | 233 | -0.62 | -0.71 |
| 2016 | 245 | +1.40 | +1.51 |
| 2017 | 216 | -0.91 | -3.31 |
| 2018 | 249 | -1.27 | -1.57 |
| 2019 | 251 | -0.97 | -1.77 |
| 2020 | 248 | +1.54 | +0.78 |
| 2021 | 252 | -0.81 | -1.16 |
| 2022 | 251 | -1.86 | -1.77 |
| 2023 | 250 | -1.07 | -1.65 |

## N-EU-DOWN

| Kennzahl | Wert |
|---|---|
| Handelstage | 955 |
| Netto je Tag | -0.10 bp (σ 17.2 bp) |
| vor Kosten je Tag | +1.04 bp |
| Kosten je Tag (davon Swap) | 1.13 bp (0.00 bp) |
| Sharpe Ratio p. a. (netto) | -0.06 |
| t-Wert iid / Woche / Monat | -0.17 / -0.18 / -0.13 |
| Trefferquote | 48% |
| Notfall-Stops | 0 |
| bei doppelten Kosten | -1.23 bp/Tag |

| Kriterium | Ergebnis | erfüllt |
|---|---|---|
| Mittleres Netto-Ergebnis je Trade > 0 mit t ≥ 3,0 (kleinster aus iid / Woche / Monat) | -0.10 bp/Tag, t = -0.18 | **nein** |
| ≥ 6 von 9 Jahren positiv | 3 von 9 | **nein** |
| beide Teilzeiträume 2015–2019 und 2020–2023 positiv | -0.19 / +0.02 bp | **nein** |
| bei doppelten Kosten > 0 | -1.23 bp/Tag | **nein** |

**N-EU-DOWN: nicht bestanden.**

| Jahr | Tage | Netto Ø bp | t |
|---|---|---|---|
| 2015 | 118 | -0.20 | -0.13 |
| 2016 | 108 | +1.40 | +1.16 |
| 2017 | 95 | -1.02 | -2.21 |
| 2018 | 115 | -0.35 | -0.25 |
| 2019 | 101 | -0.90 | -0.93 |
| 2020 | 107 | +3.93 | +1.20 |
| 2021 | 100 | -0.37 | -0.28 |
| 2022 | 139 | -2.94 | -2.00 |
| 2023 | 72 | +0.48 | +0.40 |

## Beschreibend

| Auswertung | Trades | Netto Ø bp | vor Kosten Ø bp | t |
|---|---|---|---|---|
| N-NACHT, nur 2021–2023 | 665 | -1.97 | +0.22 | -0.77 |
| N-EU, nur 2021–2023 | 753 | -1.25 | -0.11 | -2.64 |
| N-EU-DOWN, nur 2021–2023 | 311 | -1.32 | -0.19 | -1.59 |
| N-EU nach Gewinntagen | 1116 | -0.77 | +0.36 | -1.84 |
| Intraday-Long 09:30–16:00 (Vergleich) | 2146 | +1.48 | +2.62 | +0.84 |
| US100 N-NACHT | 2157 | +1.45 | +3.52 | +0.81 |
| US100 N-EU | 2252 | -0.22 | +0.68 | -0.60 |
| US100 N-EU-DOWN | 950 | +0.68 | +1.57 | +1.12 |

**Ergebnis: Keine Variante erfüllt alle In-Sample-Kriterien. Strategie Nr. 12 ist gescheitert; der Hold-out bleibt unberührt.**
