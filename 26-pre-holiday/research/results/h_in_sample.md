# Modell H (Pre-Holiday US-Indizes), In-Sample 2015–2023 (Trial T88 H-SPX, T89 H-NDX)

Lauf vom 24.10.2026. Regeln laut `docs/01_Vorregistrierung.md`, Code `research/preh/`. Reguläre NYSE-Feiertage 2015–2023; Long von 15:55 New York am Tag vor dem Vortag bis 15:55 am Vortag (12:55 an verkürzten Tagen). Netto = nach Spread, Slippage und Swaps; Ergebnisse in Basispunkten.

## H-SPX

| Kennzahl | Wert |
|---|---|
| Ereignisse | 78 |
| Netto je Ereignis | +13.9 bp (σ 73.2 bp) |
| vor Kosten je Ereignis | +15.7 bp |
| Kosten je Ereignis (davon Swap) | 1.8 bp (0.7 bp) |
| Sharpe Ratio p. a. (netto) | 0.56 |
| t-Wert iid / Quartal | 1.68 / 1.84 |
| Anteil positiver Ereignisse | 62% |
| Notfall-Stops | 0 |
| bei doppelten Kosten | +12.1 bp/Ereignis |

| Kriterium | Ergebnis | erfüllt |
|---|---|---|
| Mittleres Netto-Ergebnis je Ereignis > 0 mit t ≥ 3,0 (kleinster aus iid / Quartal) | +13.9 bp/Ereignis, t = 1.68 | **nein** |
| ≥ 6 von 9 Jahren positiv | 5 von 9 | **nein** |
| beide Teilzeiträume 2015–2019 und 2020–2023 positiv | +6.1 / +24.5 bp | ja |
| bei doppelten Kosten > 0 | +12.1 bp/Ereignis | ja |

**H-SPX: nicht bestanden.**

| Jahr | Ereignisse | Netto Summe bp |
|---|---|---|
| 2015 | 9 | -108.5 |
| 2016 | 9 | -60.2 |
| 2017 | 9 | -39.2 |
| 2018 | 9 | +29.1 |
| 2019 | 9 | +455.4 |
| 2020 | 9 | +185.8 |
| 2021 | 9 | +316.3 |
| 2022 | 9 | +324.9 |
| 2023 | 6 | -17.6 |

## H-NDX

| Kennzahl | Wert |
|---|---|
| Ereignisse | 79 |
| Netto je Ereignis | +10.6 bp (σ 107.6 bp) |
| vor Kosten je Ereignis | +12.5 bp |
| Kosten je Ereignis (davon Swap) | 1.9 bp (1.0 bp) |
| Sharpe Ratio p. a. (netto) | 0.29 |
| t-Wert iid / Quartal | 0.88 / 1.04 |
| Anteil positiver Ereignisse | 68% |
| Notfall-Stops | 1 |
| bei doppelten Kosten | +8.7 bp/Ereignis |

| Kriterium | Ergebnis | erfüllt |
|---|---|---|
| Mittleres Netto-Ergebnis je Ereignis > 0 mit t ≥ 3,0 (kleinster aus iid / Quartal) | +10.6 bp/Ereignis, t = 0.88 | **nein** |
| ≥ 6 von 9 Jahren positiv | 5 von 9 | **nein** |
| beide Teilzeiträume 2015–2019 und 2020–2023 positiv | +0.6 / +23.8 bp | ja |
| bei doppelten Kosten > 0 | +8.7 bp/Ereignis | ja |

**H-NDX: nicht bestanden.**

| Jahr | Ereignisse | Netto Summe bp |
|---|---|---|
| 2015 | 9 | -23.1 |
| 2016 | 9 | -251.8 |
| 2017 | 9 | -164.3 |
| 2018 | 9 | +157.9 |
| 2019 | 9 | +310.4 |
| 2020 | 9 | -209.3 |
| 2021 | 9 | +481.2 |
| 2022 | 9 | +325.0 |
| 2023 | 7 | +211.7 |

## Beschreibend: Vortage gegen übrige Handelstage (15:55 bis 15:55, vor Kosten)

| Index | Vortage | Ø Vortag bp | Ø übrige bp | Differenz | t |
|---|---|---|---|---|---|
| SPXUSD | 71 | +19.1 | +3.6 | +15.5 | +1.81 |
| NSXUSD | 72 | +21.0 | +5.9 | +15.1 | +1.30 |

**Ergebnis: Keine Variante erfüllt alle In-Sample-Kriterien. Strategie Nr. 26 ist gescheitert; der Hold-out bleibt unberührt.**
