# Modell T (Tages-Ausbruch), In-Sample 2015–2023 (Trial T114 T-NR7, T115 T-INSIDE, T116 T-LW)

Lauf vom 24.10.2026. Regeln laut `docs/01_Vorregistrierung.md`, Code `research/dbo/`. 17 Instrumente, Servertage; Stop-Orders an den Levels, Stop am Gegenlevel, Schluss am Tagesende; 0,25 % Risiko je Trade. Netto = nach Spread, Slippage und Kommission; Ergebnisse in bp bzw. % des Kapitals, Portfolio = Summe aller Instrumente je Tag.

## T-NR7

| Kennzahl | Wert |
|---|---|
| Handelstage / Trades | 2,291 / 5,717 |
| Netto je Tag (bp des Kapitals, Portfolio) | -0.54 bp (σ 52.5 bp) |
| vor Kosten je Tag | +1.83 bp |
| Kosten je Tag | 2.38 bp |
| Rendite p. a. (netto, 0,25 % Risiko je Trade) | -1.39 % |
| Sharpe Ratio p. a. (netto) | -0.17 |
| t-Wert iid / Woche / Monat | -0.50 / -0.50 / -0.50 |
| Ø R je Trade vor / nach Kosten | +0.029 / -0.009 |
| Trefferquote / Anteil Stops | 46% / 27% |
| bei doppelten Kosten | -2.92 bp/Tag |

| Kriterium | Ergebnis | erfüllt |
|---|---|---|
| Mittleres Netto-Tagesergebnis > 0 mit t ≥ 3,0 (kleinster aus iid / Woche / Monat) | -0.54 bp/Tag, t = -0.50 | **nein** |
| ≥ 6 von 9 Jahren positiv | 4 von 9 | **nein** |
| ≥ 60 % der Instrumente positiv | 8 von 17 | **nein** |
| bei doppelten Kosten > 0 | -2.92 bp/Tag | **nein** |

**T-NR7: nicht bestanden.**

| Jahr | Tage | Netto % |
|---|---|---|
| 2015 | 254 | +14.69 |
| 2016 | 255 | -7.84 |
| 2017 | 255 | -11.97 |
| 2018 | 254 | +5.76 |
| 2019 | 254 | -6.61 |
| 2020 | 255 | +0.17 |
| 2021 | 254 | +9.11 |
| 2022 | 255 | -2.45 |
| 2023 | 255 | -13.34 |

| Instrument | Trades | Netto % p. a. | Ø R netto |
|---|---|---|---|
| EURUSD | 336 | +0.59 | +0.063 |
| GBPUSD | 315 | -0.02 | -0.003 |
| USDJPY | 351 | +0.66 | +0.068 |
| AUDUSD | 298 | -0.80 | -0.097 |
| NZDUSD | 327 | -0.75 | -0.082 |
| USDCAD | 320 | -0.08 | -0.009 |
| USDCHF | 329 | -0.78 | -0.085 |
| XAUUSD | 331 | +0.35 | +0.038 |
| US500 | 340 | +0.06 | +0.006 |
| US100 | 341 | +0.26 | +0.028 |
| FRA40 | 355 | -0.20 | -0.020 |
| UK100 | 345 | -0.91 | -0.095 |
| JP225 | 364 | +0.36 | +0.035 |
| HK50 | 326 | +0.52 | +0.057 |
| AUS200 | 366 | -0.79 | -0.078 |
| Brent | 344 | +0.64 | +0.067 |
| Silber | 329 | -0.50 | -0.054 |

## T-INSIDE

| Kennzahl | Wert |
|---|---|
| Handelstage / Trades | 2,291 / 4,778 |
| Netto je Tag (bp des Kapitals, Portfolio) | +0.13 bp (σ 40.4 bp) |
| vor Kosten je Tag | +1.90 bp |
| Kosten je Tag | 1.77 bp |
| Rendite p. a. (netto, 0,25 % Risiko je Trade) | +0.33 % |
| Sharpe Ratio p. a. (netto) | 0.05 |
| t-Wert iid / Woche / Monat | 0.15 / 0.15 / 0.17 |
| Ø R je Trade vor / nach Kosten | +0.036 / +0.003 |
| Trefferquote / Anteil Stops | 47% / 22% |
| bei doppelten Kosten | -1.64 bp/Tag |

| Kriterium | Ergebnis | erfüllt |
|---|---|---|
| Mittleres Netto-Tagesergebnis > 0 mit t ≥ 3,0 (kleinster aus iid / Woche / Monat) | +0.13 bp/Tag, t = 0.15 | **nein** |
| ≥ 6 von 9 Jahren positiv | 3 von 9 | **nein** |
| ≥ 60 % der Instrumente positiv | 8 von 17 | **nein** |
| bei doppelten Kosten > 0 | -1.64 bp/Tag | **nein** |

**T-INSIDE: nicht bestanden.**

| Jahr | Tage | Netto % |
|---|---|---|
| 2015 | 254 | +15.03 |
| 2016 | 255 | -0.82 |
| 2017 | 255 | -14.19 |
| 2018 | 254 | -1.28 |
| 2019 | 254 | -1.80 |
| 2020 | 255 | +10.72 |
| 2021 | 254 | +4.22 |
| 2022 | 255 | -5.14 |
| 2023 | 255 | -3.74 |

| Instrument | Trades | Netto % p. a. | Ø R netto |
|---|---|---|---|
| EURUSD | 279 | +0.34 | +0.044 |
| GBPUSD | 297 | +0.17 | +0.021 |
| USDJPY | 318 | +1.09 | +0.123 |
| AUDUSD | 303 | -0.30 | -0.035 |
| NZDUSD | 291 | -0.76 | -0.094 |
| USDCAD | 272 | -0.13 | -0.017 |
| USDCHF | 279 | -0.61 | -0.079 |
| XAUUSD | 325 | +0.51 | +0.056 |
| US500 | 260 | -0.37 | -0.051 |
| US100 | 244 | +0.08 | +0.011 |
| FRA40 | 283 | -0.14 | -0.018 |
| UK100 | 265 | -0.62 | -0.084 |
| JP225 | 269 | +0.79 | +0.105 |
| HK50 | 274 | +0.34 | +0.045 |
| AUS200 | 221 | -0.28 | -0.046 |
| Brent | 252 | +0.67 | +0.096 |
| Silber | 346 | -0.44 | -0.046 |

## T-LW

| Kennzahl | Wert |
|---|---|
| Handelstage / Trades | 2,291 / 29,338 |
| Netto je Tag (bp des Kapitals, Portfolio) | -4.23 bp (σ 102.4 bp) |
| vor Kosten je Tag | +4.52 bp |
| Kosten je Tag | 8.75 bp |
| Rendite p. a. (netto, 0,25 % Risiko je Trade) | -10.76 % |
| Sharpe Ratio p. a. (netto) | -0.66 |
| t-Wert iid / Woche / Monat | -1.97 / -2.07 / -1.99 |
| Ø R je Trade vor / nach Kosten | +0.014 / -0.013 |
| Trefferquote / Anteil Stops | 47% / 13% |
| bei doppelten Kosten | -12.97 bp/Tag |

| Kriterium | Ergebnis | erfüllt |
|---|---|---|
| Mittleres Netto-Tagesergebnis > 0 mit t ≥ 3,0 (kleinster aus iid / Woche / Monat) | -4.23 bp/Tag, t = -2.07 | **nein** |
| ≥ 6 von 9 Jahren positiv | 2 von 9 | **nein** |
| ≥ 60 % der Instrumente positiv | 4 von 17 | **nein** |
| bei doppelten Kosten > 0 | -12.97 bp/Tag | **nein** |

**T-LW: nicht bestanden.**

| Jahr | Tage | Netto % |
|---|---|---|
| 2015 | 254 | +13.45 |
| 2016 | 255 | -7.21 |
| 2017 | 255 | -22.50 |
| 2018 | 254 | -12.78 |
| 2019 | 254 | -40.86 |
| 2020 | 255 | +13.20 |
| 2021 | 254 | -4.62 |
| 2022 | 255 | -10.39 |
| 2023 | 255 | -25.10 |

| Instrument | Trades | Netto % p. a. | Ø R netto |
|---|---|---|---|
| EURUSD | 1727 | -0.60 | -0.013 |
| GBPUSD | 1722 | -0.42 | -0.009 |
| USDJPY | 1706 | +0.84 | +0.018 |
| AUDUSD | 1730 | -0.48 | -0.010 |
| NZDUSD | 1756 | -1.04 | -0.021 |
| USDCAD | 1738 | -1.08 | -0.022 |
| USDCHF | 1750 | -1.07 | -0.022 |
| XAUUSD | 1658 | -0.08 | -0.002 |
| US500 | 1678 | -0.06 | -0.001 |
| US100 | 1661 | +1.05 | +0.023 |
| FRA40 | 1745 | -1.67 | -0.034 |
| UK100 | 1757 | -2.05 | -0.042 |
| JP225 | 1759 | +0.75 | +0.015 |
| HK50 | 1695 | +1.98 | +0.042 |
| AUS200 | 1768 | -2.30 | -0.047 |
| Brent | 1767 | -0.46 | -0.009 |
| Silber | 1721 | -4.06 | -0.085 |

**Ergebnis: Keine Variante erfüllt alle In-Sample-Kriterien. Strategien Nr. 33, 34 und 35 sind gescheitert; der Hold-out bleibt unberührt.**

## Hinweis zum ersten Lauf

Der erste Lauf (Commit `40bb5b1`) zählte eine einstündige HistData-Restkerze (Freitag 17:00–18:00 New York im Sommer, Server-Samstag) als D1-Kerze. Das erzeugte zusätzliche Samstags-Handelstage und fast jeden Montag ein NR7-Signal. Korrigiert in Commit `6cb19d5`: Nur Servertage Mo–Fr zählen. Die Regeln selbst sind unverändert. Der fehlerhafte Lauf war ebenfalls deutlich negativ (T-NR7 −7,0, T-INSIDE −10,2, T-LW −9,0 bp/Tag), die Korrektur ändert das Ergebnis also nicht.
