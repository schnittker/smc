# Modell KA (Verfall, Santa Rally), In-Sample 2015–2023 (Trial T201 K-OPEX, T202 K-POST, T203 K-SANTA)

Lauf vom 24.10.2026. Regeln laut `docs/01_Vorregistrierung.md`, Code `research/cal/`. US500, NYSE-Handelstage, Kurse um 15:55 New York, Position 1 × Kapital mit Notfall-Stop 3 ATR14 (D1). Netto = nach Spread (FTMO-Durchschnitt), Slippage (¼ Spread je Ausführung) und Swaps; Ergebnisse in Basispunkten.

## K-OPEX

| Kennzahl | Wert |
|---|---|
| Ereignisse | 105 |
| Netto je Ereignis | -6.7 bp (σ 246.7 bp) |
| vor Kosten je Ereignis | -1.7 bp |
| Kosten je Ereignis (davon Swap) | 5.0 bp (3.9 bp) |
| Sharpe Ratio p. a. (netto) | -0.09 |
| t-Wert iid / Quartal | -0.28 / -0.27 |
| Anteil positiver Ereignisse | 52% |
| Notfall-Stops | 9 |
| bei doppelten Kosten | -11.7 bp/Ereignis |

| Kriterium | Ergebnis | erfüllt |
|---|---|---|
| Mittleres Netto-Ergebnis je Ereignis > 0 mit t ≥ 3,0 (kleinster aus iid / Quartal) | -6.7 bp/Ereignis, t = -0.28 | **nein** |
| ≥ 6 von 9 Jahren positiv | 5 von 9 | **nein** |
| beide Teilzeiträume 2015–2019 und 2020–2023 positiv | +41.6 / -71.1 bp | **nein** |
| bei doppelten Kosten > 0 | -11.7 bp/Ereignis | **nein** |

**K-OPEX: nicht bestanden.**

| Jahr | Ereignisse | Netto Summe bp |
|---|---|---|
| 2015 | 12 | +461.1 |
| 2016 | 12 | +607.0 |
| 2017 | 12 | +341.6 |
| 2018 | 12 | -22.0 |
| 2019 | 12 | +1106.2 |
| 2020 | 12 | -766.6 |
| 2021 | 12 | -647.3 |
| 2022 | 12 | -1894.6 |
| 2023 | 9 | +109.1 |

## K-POST

| Kennzahl | Wert |
|---|---|
| Ereignisse | 102 |
| Netto je Ereignis | -30.3 bp (σ 257.3 bp) |
| vor Kosten je Ereignis | -23.0 bp |
| Kosten je Ereignis (davon Swap) | 7.3 bp (6.1 bp) |
| Sharpe Ratio p. a. (netto) | -0.40 |
| t-Wert iid / Quartal | -1.19 / -1.61 |
| Anteil positiver Ereignisse | 39% |
| Notfall-Stops | 4 |
| bei doppelten Kosten | -37.6 bp/Ereignis |

| Kriterium | Ergebnis | erfüllt |
|---|---|---|
| Mittleres Netto-Ergebnis je Ereignis > 0 mit t ≥ 3,0 (kleinster aus iid / Quartal) | -30.3 bp/Ereignis, t = -1.61 | **nein** |
| ≥ 6 von 9 Jahren positiv | 4 von 9 | **nein** |
| beide Teilzeiträume 2015–2019 und 2020–2023 positiv | -18.8 / -46.8 bp | **nein** |
| bei doppelten Kosten > 0 | -37.6 bp/Ereignis | **nein** |

**K-POST: nicht bestanden.**

| Jahr | Ereignisse | Netto Summe bp |
|---|---|---|
| 2015 | 12 | -298.7 |
| 2016 | 12 | -907.4 |
| 2017 | 12 | -636.3 |
| 2018 | 12 | +476.2 |
| 2019 | 12 | +239.7 |
| 2020 | 11 | +284.4 |
| 2021 | 12 | -1422.7 |
| 2022 | 12 | -1133.6 |
| 2023 | 7 | +307.2 |

## K-SANTA

| Kennzahl | Wert |
|---|---|
| Ereignisse | 9 |
| Netto je Ereignis | +0.1 bp (σ 156.1 bp) |
| vor Kosten je Ereignis | +7.3 bp |
| Kosten je Ereignis (davon Swap) | 7.2 bp (6.1 bp) |
| Sharpe Ratio p. a. (netto) | 0.00 |
| t-Wert iid / Quartal | 0.00 / 0.00 |
| Anteil positiver Ereignisse | 78% |
| Notfall-Stops | 0 |
| bei doppelten Kosten | -7.1 bp/Ereignis |

| Kriterium | Ergebnis | erfüllt |
|---|---|---|
| Mittleres Netto-Ergebnis je Ereignis > 0 mit t ≥ 3,0 (kleinster aus iid / Quartal) | +0.1 bp/Ereignis, t = 0.00 | **nein** |
| ≥ 6 von 9 Jahren positiv | 7 von 9 | ja |
| beide Teilzeiträume 2015–2019 und 2020–2023 positiv | -55.5 / +69.6 bp | **nein** |
| bei doppelten Kosten > 0 | -7.1 bp/Ereignis | **nein** |

**K-SANTA: nicht bestanden.**

| Jahr | Ereignisse | Netto Summe bp |
|---|---|---|
| 2015 | 1 | -295.1 |
| 2016 | 1 | -238.0 |
| 2017 | 1 | +36.1 |
| 2018 | 1 | +90.5 |
| 2019 | 1 | +128.8 |
| 2020 | 1 | +33.3 |
| 2021 | 1 | +81.7 |
| 2022 | 1 | +126.1 |
| 2023 | 1 | +37.4 |

## Beschreibend

| Auswertung | Ereignisse | Netto Ø bp | vor Kosten Ø bp | t | Jahre positiv |
|---|---|---|---|---|---|
| US100 K-OPEX | 103 | +19.6 | +26.3 | +0.68 | 6 von 9 |
| US100 K-POST | 102 | -44.0 | -38.9 | -1.53 | 3 von 9 |
| US100 K-SANTA | 9 | -23.7 | -13.4 | -0.40 | 4 von 9 |
| US500 K-OPEX, Quartalsverfall | 34 | -48.4 | -43.6 | -0.81 | – |
| US500 K-OPEX, übrige Monate | 71 | +13.2 | +18.3 | +0.62 | – |
| US500 K-POST, Quartalsverfall | 34 | -30.6 | -23.3 | -0.63 | – |
| US500 K-POST, übrige Monate | 68 | -30.2 | -22.9 | -1.01 | – |

**Ergebnis: Keine Variante erfüllt alle In-Sample-Kriterien. Strategien Nr. 56 und 57 sind gescheitert; der Hold-out bleibt unberührt.**
