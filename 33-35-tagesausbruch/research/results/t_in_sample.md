# Modell T (Tages-Ausbruch), In-Sample 2015–2023 (Trial T114 T-NR7, T115 T-INSIDE, T116 T-LW)

Lauf vom 24.10.2026. Regeln laut `docs/01_Vorregistrierung.md`, Code `research/dbo/`. 17 Instrumente, Servertage; Stop-Orders an den Levels, Stop am Gegenlevel, Schluss am Tagesende; 0,25 % Risiko je Trade. Netto = nach Spread, Slippage und Kommission; Ergebnisse in bp bzw. % des Kapitals, Portfolio = Summe aller Instrumente je Tag.

## T-NR7

| Kennzahl | Wert |
|---|---|
| Handelstage / Trades | 2,579 / 5,170 |
| Netto je Tag (bp des Kapitals, Portfolio) | -7.03 bp (σ 60.8 bp) |
| vor Kosten je Tag | -3.24 bp |
| Kosten je Tag | 3.78 bp |
| Rendite p. a. (netto, 0,25 % Risiko je Trade) | -20.14 % |
| Sharpe Ratio p. a. (netto) | -1.96 |
| t-Wert iid / Woche / Monat | -5.87 / -6.09 / -6.19 |
| Ø R je Trade vor / nach Kosten | -0.065 / -0.140 |
| Trefferquote / Anteil Stops | 37% / 43% |
| bei doppelten Kosten | -10.81 bp/Tag |

| Kriterium | Ergebnis | erfüllt |
|---|---|---|
| Mittleres Netto-Tagesergebnis > 0 mit t ≥ 3,0 (kleinster aus iid / Woche / Monat) | -7.03 bp/Tag, t = -6.19 | **nein** |
| ≥ 6 von 9 Jahren positiv | 0 von 9 | **nein** |
| ≥ 60 % der Instrumente positiv | 5 von 17 | **nein** |
| bei doppelten Kosten > 0 | -10.81 bp/Tag | **nein** |

**T-NR7: nicht bestanden.**

| Jahr | Tage | Netto % |
|---|---|---|
| 2015 | 288 | -4.54 |
| 2016 | 289 | -26.29 |
| 2017 | 289 | -23.62 |
| 2018 | 288 | -19.69 |
| 2019 | 284 | -12.96 |
| 2020 | 285 | -23.11 |
| 2021 | 285 | -17.30 |
| 2022 | 286 | -21.77 |
| 2023 | 285 | -31.96 |

| Instrument | Trades | Netto % p. a. | Ø R netto |
|---|---|---|---|
| EURUSD | 271 | -2.05 | -0.272 |
| GBPUSD | 270 | -2.05 | -0.273 |
| USDJPY | 274 | -2.11 | -0.277 |
| AUDUSD | 260 | -2.46 | -0.340 |
| NZDUSD | 273 | -2.41 | -0.318 |
| USDCAD | 265 | -1.86 | -0.253 |
| USDCHF | 266 | -3.34 | -0.451 |
| XAUUSD | 280 | +0.29 | +0.037 |
| US500 | 340 | +0.06 | +0.006 |
| US100 | 341 | +0.26 | +0.028 |
| FRA40 | 356 | -0.23 | -0.023 |
| UK100 | 345 | -0.73 | -0.076 |
| JP225 | 361 | +1.02 | +0.101 |
| HK50 | 326 | +0.52 | +0.057 |
| AUS200 | 353 | -1.48 | -0.151 |
| Brent | 301 | -1.53 | -0.184 |
| Silber | 288 | -2.06 | -0.257 |

## T-INSIDE

| Kennzahl | Wert |
|---|---|
| Handelstage / Trades | 2,579 / 6,367 |
| Netto je Tag (bp des Kapitals, Portfolio) | -10.20 bp (σ 67.9 bp) |
| vor Kosten je Tag | -5.36 bp |
| Kosten je Tag | 4.84 bp |
| Rendite p. a. (netto, 0,25 % Risiko je Trade) | -29.23 % |
| Sharpe Ratio p. a. (netto) | -2.54 |
| t-Wert iid / Woche / Monat | -7.63 / -7.82 / -7.58 |
| Ø R je Trade vor / nach Kosten | -0.087 / -0.165 |
| Trefferquote / Anteil Stops | 35% / 44% |
| bei doppelten Kosten | -15.04 bp/Tag |

| Kriterium | Ergebnis | erfüllt |
|---|---|---|
| Mittleres Netto-Tagesergebnis > 0 mit t ≥ 3,0 (kleinster aus iid / Woche / Monat) | -10.20 bp/Tag, t = -7.82 | **nein** |
| ≥ 6 von 9 Jahren positiv | 0 von 9 | **nein** |
| ≥ 60 % der Instrumente positiv | 3 von 17 | **nein** |
| bei doppelten Kosten > 0 | -15.04 bp/Tag | **nein** |

**T-INSIDE: nicht bestanden.**

| Jahr | Tage | Netto % |
|---|---|---|
| 2015 | 288 | -12.60 |
| 2016 | 289 | -27.61 |
| 2017 | 289 | -37.63 |
| 2018 | 288 | -34.94 |
| 2019 | 284 | -13.48 |
| 2020 | 285 | -25.27 |
| 2021 | 285 | -44.30 |
| 2022 | 286 | -35.72 |
| 2023 | 285 | -31.51 |

| Instrument | Trades | Netto % p. a. | Ø R netto |
|---|---|---|---|
| EURUSD | 428 | -3.19 | -0.268 |
| GBPUSD | 443 | -2.67 | -0.217 |
| USDJPY | 471 | -2.80 | -0.214 |
| AUDUSD | 458 | -3.11 | -0.245 |
| NZDUSD | 431 | -3.07 | -0.256 |
| USDCAD | 421 | -2.84 | -0.243 |
| USDCHF | 441 | -4.73 | -0.386 |
| XAUUSD | 478 | -0.45 | -0.034 |
| US500 | 260 | -0.37 | -0.051 |
| US100 | 244 | +0.08 | +0.011 |
| FRA40 | 289 | -0.16 | -0.020 |
| UK100 | 274 | -0.44 | -0.057 |
| JP225 | 289 | +1.06 | +0.132 |
| HK50 | 274 | +0.34 | +0.045 |
| AUS200 | 264 | -0.88 | -0.121 |
| Brent | 419 | -2.44 | -0.210 |
| Silber | 483 | -3.56 | -0.266 |

## T-LW

| Kennzahl | Wert |
|---|---|
| Handelstage / Trades | 2,579 / 30,305 |
| Netto je Tag (bp des Kapitals, Portfolio) | -8.96 bp (σ 123.3 bp) |
| vor Kosten je Tag | +3.60 bp |
| Kosten je Tag | 12.57 bp |
| Rendite p. a. (netto, 0,25 % Risiko je Trade) | -25.68 % |
| Sharpe Ratio p. a. (netto) | -1.23 |
| t-Wert iid / Woche / Monat | -3.69 / -3.85 / -3.63 |
| Ø R je Trade vor / nach Kosten | +0.012 / -0.031 |
| Trefferquote / Anteil Stops | 44% / 20% |
| bei doppelten Kosten | -21.53 bp/Tag |

| Kriterium | Ergebnis | erfüllt |
|---|---|---|
| Mittleres Netto-Tagesergebnis > 0 mit t ≥ 3,0 (kleinster aus iid / Woche / Monat) | -8.96 bp/Tag, t = -3.85 | **nein** |
| ≥ 6 von 9 Jahren positiv | 1 von 9 | **nein** |
| ≥ 60 % der Instrumente positiv | 4 von 17 | **nein** |
| bei doppelten Kosten > 0 | -21.53 bp/Tag | **nein** |

**T-LW: nicht bestanden.**

| Jahr | Tage | Netto % |
|---|---|---|
| 2015 | 288 | -2.66 |
| 2016 | 289 | -23.84 |
| 2017 | 289 | -46.80 |
| 2018 | 288 | -21.36 |
| 2019 | 284 | -50.63 |
| 2020 | 285 | +12.32 |
| 2021 | 285 | -20.91 |
| 2022 | 286 | -20.99 |
| 2023 | 285 | -56.27 |

| Instrument | Trades | Netto % p. a. | Ø R netto |
|---|---|---|---|
| EURUSD | 1839 | -2.60 | -0.051 |
| GBPUSD | 1825 | -2.58 | -0.051 |
| USDJPY | 1796 | +0.81 | +0.016 |
| AUDUSD | 1827 | -0.11 | -0.002 |
| NZDUSD | 1858 | -1.59 | -0.031 |
| USDCAD | 1834 | -3.12 | -0.061 |
| USDCHF | 1846 | -1.97 | -0.038 |
| XAUUSD | 1760 | -1.33 | -0.027 |
| US500 | 1678 | -0.06 | -0.001 |
| US100 | 1661 | +1.05 | +0.023 |
| FRA40 | 1748 | -1.86 | -0.038 |
| UK100 | 1762 | -2.33 | -0.048 |
| JP225 | 1769 | +1.08 | +0.022 |
| HK50 | 1695 | +1.98 | +0.042 |
| AUS200 | 1786 | -2.80 | -0.057 |
| Brent | 1820 | -3.17 | -0.063 |
| Silber | 1801 | -7.08 | -0.141 |

**Ergebnis: Keine Variante erfüllt alle In-Sample-Kriterien. Strategien Nr. 33, 34 und 35 sind gescheitert; der Hold-out bleibt unberührt.**
