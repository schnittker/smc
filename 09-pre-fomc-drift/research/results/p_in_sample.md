# Modell P (Pre-FOMC-Drift), In-Sample 2015–2023 (Trial T31 P-SPX, T32 P-NDX)

Lauf vom 24.10.2026. Regeln laut `docs/01_Vorregistrierung.md`, Code `research/fomc/`. 71 planmäßige FOMC-Entscheide; Long von 14:00 New York am Vortag bis 13:55 am Entscheidungstag. Netto = nach Spread (FTMO-Durchschnitt), Slippage (¼ Spread je Ausführung) und Swap; Ergebnisse in Basispunkten.

## P-SPX

| Kennzahl | Wert |
|---|---|
| Termine | 67 |
| Netto je Termin | +19.2 bp (σ 60.0 bp) |
| vor Kosten je Termin | +20.9 bp |
| Kosten je Termin (davon Swap) | 1.7 bp (0.6 bp) |
| Sharpe Ratio p. a. (netto) | 0.87 |
| t-Wert iid / Quartal | 2.62 / 2.38 |
| Anteil positiver Termine | 63% |
| Notfall-Stops | 0 |
| bei doppelten Kosten | +17.5 bp/Termin |

| Kriterium | Ergebnis | erfüllt |
|---|---|---|
| Mittleres Netto-Ergebnis je Termin > 0 mit t ≥ 3,0 (kleinster aus iid / Quartal) | +19.2 bp/Termin, t = 2.38 | **nein** |
| ≥ 6 von 9 Jahren positiv | 7 von 9 | ja |
| beide Teilzeiträume 2015–2019 und 2020–2023 positiv | +7.3 / +37.0 bp | ja |
| bei doppelten Kosten > 0 | +17.5 bp/Termin | ja |

**P-SPX: nicht bestanden.**

| Jahr | Termine | Netto Summe bp |
|---|---|---|
| 2015 | 8 | +57.5 |
| 2016 | 8 | +11.4 |
| 2017 | 8 | +81.4 |
| 2018 | 8 | +177.7 |
| 2019 | 8 | -37.8 |
| 2020 | 7 | +396.0 |
| 2021 | 8 | -125.5 |
| 2022 | 8 | +575.5 |
| 2023 | 4 | +151.7 |

### Vergleich mit allen anderen Handelstagen (vor Kosten, Bid zu Bid)

| Fenster 14:00 Vortag – 13:55 | Tage | Ø bp | t |
|---|---|---|---|
| FOMC-Termine | 67 | +20.9 | +2.85 |
| übrige Handelstage | 2045 | +3.9 | +1.60 |
| **Differenz (FOMC-Effekt)** | | **+17.1** | **+2.21** |

### Teilfenster an FOMC-Terminen (vor Kosten)

| Fenster | Termine | Ø bp | t |
|---|---|---|---|
| 14:00–16:00 Vortag | 67 | +0.6 | +0.19 |
| 16:00 Vortag – 09:30 Entscheidungstag | 68 | +19.2 | +3.77 |
| 09:30–13:55 Entscheidungstag | 67 | +0.7 | +0.16 |
| nach der Entscheidung 14:00–16:00 | 69 | +3.9 | +0.39 |

## P-NDX

| Kennzahl | Wert |
|---|---|
| Termine | 68 |
| Netto je Termin | +28.3 bp (σ 87.0 bp) |
| vor Kosten je Termin | +30.1 bp |
| Kosten je Termin (davon Swap) | 1.8 bp (0.9 bp) |
| Sharpe Ratio p. a. (netto) | 0.89 |
| t-Wert iid / Quartal | 2.68 / 2.26 |
| Anteil positiver Termine | 68% |
| Notfall-Stops | 0 |
| bei doppelten Kosten | +26.5 bp/Termin |

| Kriterium | Ergebnis | erfüllt |
|---|---|---|
| Mittleres Netto-Ergebnis je Termin > 0 mit t ≥ 3,0 (kleinster aus iid / Quartal) | +28.3 bp/Termin, t = 2.26 | **nein** |
| ≥ 6 von 9 Jahren positiv | 6 von 9 | ja |
| beide Teilzeiträume 2015–2019 und 2020–2023 positiv | +9.1 / +55.8 bp | ja |
| bei doppelten Kosten > 0 | +26.5 bp/Termin | ja |

**P-NDX: nicht bestanden.**

| Jahr | Termine | Netto Summe bp |
|---|---|---|
| 2015 | 8 | -64.4 |
| 2016 | 8 | -155.1 |
| 2017 | 8 | +140.3 |
| 2018 | 8 | +323.8 |
| 2019 | 8 | +117.9 |
| 2020 | 7 | +583.4 |
| 2021 | 8 | -146.0 |
| 2022 | 8 | +883.8 |
| 2023 | 5 | +239.8 |

### Vergleich mit allen anderen Handelstagen (vor Kosten, Bid zu Bid)

| Fenster 14:00 Vortag – 13:55 | Tage | Ø bp | t |
|---|---|---|---|
| FOMC-Termine | 68 | +30.1 | +2.85 |
| übrige Handelstage | 2051 | +5.9 | +2.05 |
| **Differenz (FOMC-Effekt)** | | **+24.2** | **+2.21** |

### Teilfenster an FOMC-Terminen (vor Kosten)

| Fenster | Termine | Ø bp | t |
|---|---|---|---|
| 14:00–16:00 Vortag | 68 | +0.4 | +0.09 |
| 16:00 Vortag – 09:30 Entscheidungstag | 69 | +29.3 | +4.06 |
| 09:30–13:55 Entscheidungstag | 69 | -1.5 | -0.26 |
| nach der Entscheidung 14:00–16:00 | 67 | +9.7 | +0.74 |

**Ergebnis: Keine Variante erfüllt alle In-Sample-Kriterien. Strategie Nr. 9 ist gescheitert; der Hold-out bleibt unberührt.**
