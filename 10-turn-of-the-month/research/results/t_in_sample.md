# Modell T (Turn-of-the-Month US500), In-Sample 2015–2023 (Trial T35 T-KLASSIK, T36 T-FRÜH)

Lauf vom 24.10.2026. Regeln laut `docs/01_Vorregistrierung.md`, Code `research/tom/`. Monatswechsel mit Tag +1 in 2015–2023, NYSE-Handelstage, Kurse um 15:55 New York. Netto = nach Spread (FTMO-Durchschnitt), Slippage (¼ Spread je Ausführung) und Swaps; Ergebnisse in Basispunkten.

## T-KLASSIK

| Kennzahl | Wert |
|---|---|
| Ereignisse | 100 |
| Netto je Ereignis | +22.0 bp (σ 188.4 bp) |
| vor Kosten je Ereignis | +26.2 bp |
| Kosten je Ereignis (davon Swap) | 4.2 bp (3.0 bp) |
| Sharpe Ratio p. a. (netto) | 0.39 |
| t-Wert iid / Quartal | 1.17 / 1.33 |
| Anteil positiver Ereignisse | 54% |
| Notfall-Stops | 6 |
| bei doppelten Kosten | +17.9 bp/Ereignis |

| Kriterium | Ergebnis | erfüllt |
|---|---|---|
| Mittleres Netto-Ergebnis je Ereignis > 0 mit t ≥ 3,0 (kleinster aus iid / Quartal) | +22.0 bp/Ereignis, t = 1.17 | **nein** |
| ≥ 6 von 9 Jahren positiv | 5 von 9 | **nein** |
| beide Teilzeiträume 2015–2019 und 2020–2023 positiv | +6.1 / +44.1 bp | ja |
| bei doppelten Kosten > 0 | +17.9 bp/Ereignis | ja |

**T-KLASSIK: nicht bestanden.**

| Jahr | Ereignisse | Netto Summe bp |
|---|---|---|
| 2015 | 11 | -10.8 |
| 2016 | 12 | -264.3 |
| 2017 | 12 | +456.4 |
| 2018 | 12 | -77.2 |
| 2019 | 11 | +248.2 |
| 2020 | 11 | +1254.7 |
| 2021 | 12 | +210.0 |
| 2022 | 12 | -115.2 |
| 2023 | 7 | +502.6 |

## T-FRÜH

| Kennzahl | Wert |
|---|---|
| Ereignisse | 96 |
| Netto je Ereignis | +36.4 bp (σ 212.9 bp) |
| vor Kosten je Ereignis | +42.1 bp |
| Kosten je Ereignis (davon Swap) | 5.7 bp (4.5 bp) |
| Sharpe Ratio p. a. (netto) | 0.56 |
| t-Wert iid / Quartal | 1.68 / 2.05 |
| Anteil positiver Ereignisse | 51% |
| Notfall-Stops | 13 |
| bei doppelten Kosten | +30.7 bp/Ereignis |

| Kriterium | Ergebnis | erfüllt |
|---|---|---|
| Mittleres Netto-Ergebnis je Ereignis > 0 mit t ≥ 3,0 (kleinster aus iid / Quartal) | +36.4 bp/Ereignis, t = 1.68 | **nein** |
| ≥ 6 von 9 Jahren positiv | 6 von 9 | ja |
| beide Teilzeiträume 2015–2019 und 2020–2023 positiv | +13.0 / +66.6 bp | ja |
| bei doppelten Kosten > 0 | +30.7 bp/Ereignis | ja |

**T-FRÜH: nicht bestanden.**

| Jahr | Ereignisse | Netto Summe bp |
|---|---|---|
| 2015 | 11 | -92.1 |
| 2016 | 11 | +517.6 |
| 2017 | 10 | +268.4 |
| 2018 | 11 | -115.7 |
| 2019 | 11 | +121.3 |
| 2020 | 11 | +1270.2 |
| 2021 | 11 | -263.7 |
| 2022 | 12 | +938.5 |
| 2023 | 8 | +852.7 |

## Beschreibend

### Dieselben Fenster auf US100

| Variante | Ereignisse | Netto Ø bp | t | Jahre positiv |
|---|---|---|---|---|
| T-KLASSIK | 101 | +28.1 | +1.15 | 5 von 9 |
| T-FRÜH | 93 | +50.2 | +1.56 | 5 von 9 |

### Mittlere Tagesrendite je relativem Handelstag (15:55 bis 15:55, vor Kosten, bp)

| Tag | US500 Ø bp | t | US100 Ø bp | t |
|---|---|---|---|---|
| -8 | +1.2 | +0.13 | +6.9 | +0.60 |
| -7 | -0.7 | -0.08 | +8.0 | +0.64 |
| -6 | -4.8 | -0.36 | -10.8 | -0.72 |
| -5 | -9.7 | -0.95 | -14.0 | -1.07 |
| -4 | +12.0 | +1.08 | +5.9 | +0.44 |
| -3 | +8.2 | +0.74 | +11.3 | +0.77 |
| -2 | +19.2 | +1.81 | +18.3 | +1.37 |
| -1 | -7.5 | -0.76 | +0.7 | +0.06 |
| +1 | +14.6 | +1.21 | +25.1 | +1.80 |
| +2 | +6.0 | +0.57 | +1.6 | +0.12 |
| +3 | +8.4 | +0.72 | +2.3 | +0.15 |
| +4 | +13.9 | +1.24 | +18.6 | +1.38 |
| +5 | +7.9 | +0.75 | +4.6 | +0.35 |
| übrige | +2.3 | +0.56 | +6.9 | +1.43 |

**Ergebnis: Keine Variante erfüllt alle In-Sample-Kriterien. Strategie Nr. 10 ist gescheitert; der Hold-out bleibt unberührt.**
