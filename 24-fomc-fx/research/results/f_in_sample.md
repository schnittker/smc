# Modell F (USD an FOMC-Tagen), In-Sample 2015–2023 (Trial T84 F-USD, T85 F-CARRY)

Lauf vom 24.10.2026. Regeln laut `docs/01_Vorregistrierung.md`, Code `research/ffx/`. 71 FOMC-Termine; Short USD 16:50 New York am Vortag bis 16:50 am Entscheidungstag, je Paar 10 % / σ. Netto = nach Spread, Slippage, Kommission, Swap und Gebühr; Ergebnisse in bp des Kapitals.

## F-USD

| Kennzahl | Wert |
|---|---|
| Termine | 71 |
| Netto je Termin (bp des Kapitals) | +107.7 bp (σ 433.1 bp) |
| Kosten je Termin | 15.7 bp |
| Sharpe Ratio p. a. (8 Termine) | 0.70 |
| t-Wert iid / Quartal | 2.10 / 2.29 |
| Anteil positiver Termine | 59% |
| bei doppelten Kosten | +92.0 bp/Termin |

| Kriterium | Ergebnis | erfüllt |
|---|---|---|
| Mittleres Netto-Ergebnis je Termin > 0 mit t ≥ 3,0 (kleinster aus iid / Quartal) | +107.7 bp/Termin, t = 2.10 | **nein** |
| ≥ 6 von 9 Jahren positiv | 7 von 9 | ja |
| beide Teilzeiträume 2015–2019 und 2020–2023 positiv | +81.6 / +141.4 bp | ja |
| bei doppelten Kosten > 0 | +92.0 bp/Termin | ja |

**F-USD: nicht bestanden.**

| Jahr | Termine | Netto Summe bp |
|---|---|---|
| 2015 | 8 | +720.8 |
| 2016 | 8 | +536.8 |
| 2017 | 8 | +1316.3 |
| 2018 | 8 | -120.8 |
| 2019 | 8 | +811.7 |
| 2020 | 7 | +1667.1 |
| 2021 | 8 | -79.9 |
| 2022 | 8 | +1456.0 |
| 2023 | 8 | +1338.7 |

## F-CARRY

| Kennzahl | Wert |
|---|---|
| Termine | 58 |
| Netto je Termin (bp des Kapitals) | +54.6 bp (σ 196.9 bp) |
| Kosten je Termin | 4.6 bp |
| Sharpe Ratio p. a. (8 Termine) | 0.70 |
| t-Wert iid / Quartal | 2.11 / 2.58 |
| Anteil positiver Termine | 64% |
| bei doppelten Kosten | +50.0 bp/Termin |

| Kriterium | Ergebnis | erfüllt |
|---|---|---|
| Mittleres Netto-Ergebnis je Termin > 0 mit t ≥ 3,0 (kleinster aus iid / Quartal) | +54.6 bp/Termin, t = 2.11 | **nein** |
| ≥ 6 von 9 Jahren positiv | 9 von 9 | ja |
| beide Teilzeiträume 2015–2019 und 2020–2023 positiv | +42.3 / +67.8 bp | ja |
| bei doppelten Kosten > 0 | +50.0 bp/Termin | ja |

**F-CARRY: nicht bestanden.**

| Jahr | Termine | Netto Summe bp |
|---|---|---|
| 2015 | 8 | +29.5 |
| 2016 | 8 | +102.2 |
| 2017 | 8 | +845.5 |
| 2018 | 5 | +201.6 |
| 2019 | 1 | +91.3 |
| 2020 | 7 | +607.2 |
| 2021 | 8 | +224.5 |
| 2022 | 8 | +829.0 |
| 2023 | 5 | +237.0 |

### Vergleich (beschreibend, vor Kosten): Short-USD-Korb über den FX-Tag

| Tage | Anzahl | Ø bp | t |
|---|---|---|---|
| FOMC-Tage | 71 | +136.8 | +2.66 |
| übrige Tage | 2269 | -9.3 | -1.36 |
| **Differenz** | | **+146.1** | **+2.81** |

**Ergebnis: Keine Variante erfüllt alle In-Sample-Kriterien. Strategie Nr. 24 ist gescheitert; der Hold-out bleibt unberührt.**
