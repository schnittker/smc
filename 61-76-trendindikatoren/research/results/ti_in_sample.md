# Modell TI (Trendindikatoren), In-Sample 2015–2023 (Trial T219–T228)

Lauf vom 24.10.2026. Regeln laut `docs/01_Vorregistrierung.md`, Code `research/tind/`. 17 Instrumente; Stop-and-Reverse bei Zustandswechsel des Indikators zur nächsten Eröffnung, Notfall-Stop 3 ATR14; 0,25 % Risiko je Trade (am Notfall-Stop). Netto = nach Spread, Slippage, Kommission und Swaps; Ergebnis eines Trades am Tag des Ausstiegs; Portfolio = Summe aller Instrumente je Tag.

## TI-MA200 (Nr. 61, D1)

| Kennzahl | Wert |
|---|---|
| Handelstage / Trades | 2,342 / 221 |
| Netto je Tag (bp des Kapitals, Portfolio) | -0.52 bp (σ 18.0 bp) |
| vor Kosten je Tag | -0.18 bp |
| Handelskosten + Swap-Belastung je Tag (Swap netto) | 0.38 bp (-0.32 bp) |
| Rendite p. a. (netto, 0,25 % Risiko je Trade) | -1.35 % |
| Sharpe Ratio p. a. (netto) | -0.46 |
| t-Wert iid / Woche / Monat | -1.39 / -1.37 / -1.31 |
| Ø R je Trade vor / nach Kosten | -0.077 / -0.220 |
| Trefferquote / Anteil Notfall-Stops / Anteil Long | 19% / 71% / 49% |
| Ø Haltedauer | 95.5 Kerzen (D1) |
| bei doppelten Kosten | -0.90 bp/Tag |

| Kriterium | Ergebnis | erfüllt |
|---|---|---|
| Mittleres Netto-Tagesergebnis > 0 mit t ≥ 3,0 (kleinster aus iid / Woche / Monat) | -0.52 bp/Tag, t = -1.39 | **nein** |
| ≥ 6 von 9 Jahren positiv | 4 von 9 | **nein** |
| ≥ 60 % der Instrumente positiv | 5 von 17 | **nein** |
| bei doppelten Kosten > 0 | -0.90 bp/Tag | **nein** |

**TI-MA200: nicht bestanden.**

| Jahr | Tage | Netto % |
|---|---|---|
| 2015 | 260 | -3.58 |
| 2016 | 260 | -4.68 |
| 2017 | 260 | -2.59 |
| 2018 | 261 | +2.36 |
| 2019 | 260 | -7.03 |
| 2020 | 261 | -3.49 |
| 2021 | 260 | +3.75 |
| 2022 | 260 | +1.95 |
| 2023 | 260 | +1.18 |

| Anlageklasse | Trades | Netto % p. a. |
|---|---|---|
| FX | 92 | -0.66 |
| Metalle | 31 | -0.05 |
| Indizes | 87 | -0.49 |
| Öl | 11 | -0.16 |

| Instrument | Trades | Netto % p. a. | Ø R netto |
|---|---|---|---|
| EURUSD | 11 | +0.19 | +0.622 |
| GBPUSD | 12 | +0.13 | +0.377 |
| USDJPY | 14 | -0.08 | -0.208 |
| AUDUSD | 14 | -0.14 | -0.366 |
| NZDUSD | 14 | -0.22 | -0.566 |
| USDCAD | 10 | -0.22 | -0.804 |
| USDCHF | 17 | -0.30 | -0.645 |
| XAUUSD | 15 | +0.15 | +0.364 |
| US500 | 10 | -0.12 | -0.421 |
| US100 | 12 | +0.43 | +1.284 |
| FRA40 | 12 | -0.23 | -0.684 |
| UK100 | 12 | -0.23 | -0.699 |
| JP225 | 14 | +0.08 | +0.216 |
| HK50 | 11 | -0.03 | -0.108 |
| AUS200 | 16 | -0.39 | -0.870 |
| Brent | 11 | -0.16 | -0.527 |
| Silber | 16 | -0.20 | -0.447 |

## TI-EMA921 (Nr. 62, H1)

| Kennzahl | Wert |
|---|---|
| Handelstage / Trades | 2,342 / 36,667 |
| Netto je Tag (bp des Kapitals, Portfolio) | -13.37 bp (σ 185.5 bp) |
| vor Kosten je Tag | +5.20 bp |
| Handelskosten + Swap-Belastung je Tag (Swap netto) | 19.15 bp (-3.64 bp) |
| Rendite p. a. (netto, 0,25 % Risiko je Trade) | -34.79 % |
| Sharpe Ratio p. a. (netto) | -1.16 |
| t-Wert iid / Woche / Monat | -3.49 / -3.22 / -3.32 |
| Ø R je Trade vor / nach Kosten | +0.013 / -0.034 |
| Trefferquote / Anteil Notfall-Stops / Anteil Long | 28% / 12% / 50% |
| Ø Haltedauer | 22.6 Kerzen (H1) |
| bei doppelten Kosten | -32.52 bp/Tag |

| Kriterium | Ergebnis | erfüllt |
|---|---|---|
| Mittleres Netto-Tagesergebnis > 0 mit t ≥ 3,0 (kleinster aus iid / Woche / Monat) | -13.37 bp/Tag, t = -3.49 | **nein** |
| ≥ 6 von 9 Jahren positiv | 1 von 9 | **nein** |
| ≥ 60 % der Instrumente positiv | 4 von 17 | **nein** |
| bei doppelten Kosten > 0 | -32.52 bp/Tag | **nein** |

**TI-EMA921: nicht bestanden.**

| Jahr | Tage | Netto % |
|---|---|---|
| 2015 | 260 | -13.94 |
| 2016 | 260 | -56.30 |
| 2017 | 260 | -75.58 |
| 2018 | 261 | -25.49 |
| 2019 | 260 | -85.70 |
| 2020 | 261 | +45.28 |
| 2021 | 260 | -52.44 |
| 2022 | 260 | -8.88 |
| 2023 | 260 | -40.08 |

| Anlageklasse | Trades | Netto % p. a. |
|---|---|---|
| FX | 16446 | -12.08 |
| Metalle | 4617 | -6.77 |
| Indizes | 13550 | -13.87 |
| Öl | 2054 | -2.07 |

| Instrument | Trades | Netto % p. a. | Ø R netto |
|---|---|---|---|
| EURUSD | 2307 | -0.67 | -0.010 |
| GBPUSD | 2324 | -1.02 | -0.016 |
| USDJPY | 2287 | +0.27 | +0.004 |
| AUDUSD | 2378 | -2.50 | -0.038 |
| NZDUSD | 2321 | -1.92 | -0.030 |
| USDCAD | 2425 | -2.96 | -0.044 |
| USDCHF | 2404 | -3.30 | -0.049 |
| XAUUSD | 2240 | +0.79 | +0.013 |
| US500 | 2244 | -2.07 | -0.033 |
| US100 | 2138 | +0.34 | +0.006 |
| FRA40 | 1440 | -2.85 | -0.071 |
| UK100 | 1934 | -3.74 | -0.070 |
| JP225 | 2305 | -1.96 | -0.031 |
| HK50 | 1256 | +0.94 | +0.027 |
| AUS200 | 2233 | -4.53 | -0.073 |
| Brent | 2054 | -2.07 | -0.036 |
| Silber | 2377 | -7.56 | -0.115 |

## TI-TRIPLE (Nr. 63, H4)

| Kennzahl | Wert |
|---|---|
| Handelstage / Trades | 2,342 / 7,170 |
| Netto je Tag (bp des Kapitals, Portfolio) | -2.26 bp (σ 70.5 bp) |
| vor Kosten je Tag | +0.56 bp |
| Handelskosten + Swap-Belastung je Tag (Swap netto) | 3.06 bp (-1.37 bp) |
| Rendite p. a. (netto, 0,25 % Risiko je Trade) | -5.88 % |
| Sharpe Ratio p. a. (netto) | -0.52 |
| t-Wert iid / Woche / Monat | -1.55 / -1.29 / -1.09 |
| Ø R je Trade vor / nach Kosten | +0.007 / -0.030 |
| Trefferquote / Anteil Notfall-Stops / Anteil Long | 30% / 14% / 53% |
| Ø Haltedauer | 24.7 Kerzen (H4) |
| bei doppelten Kosten | -5.32 bp/Tag |

| Kriterium | Ergebnis | erfüllt |
|---|---|---|
| Mittleres Netto-Tagesergebnis > 0 mit t ≥ 3,0 (kleinster aus iid / Woche / Monat) | -2.26 bp/Tag, t = -1.55 | **nein** |
| ≥ 6 von 9 Jahren positiv | 2 von 9 | **nein** |
| ≥ 60 % der Instrumente positiv | 4 von 17 | **nein** |
| bei doppelten Kosten > 0 | -5.32 bp/Tag | **nein** |

**TI-TRIPLE: nicht bestanden.**

| Jahr | Tage | Netto % |
|---|---|---|
| 2015 | 260 | -12.02 |
| 2016 | 260 | -12.88 |
| 2017 | 260 | -10.34 |
| 2018 | 261 | -1.94 |
| 2019 | 260 | -14.99 |
| 2020 | 261 | +23.49 |
| 2021 | 260 | -24.63 |
| 2022 | 260 | +6.85 |
| 2023 | 260 | -6.45 |

| Anlageklasse | Trades | Netto % p. a. |
|---|---|---|
| FX | 3097 | -1.68 |
| Metalle | 880 | -0.24 |
| Indizes | 2773 | -4.13 |
| Öl | 420 | +0.16 |

| Instrument | Trades | Netto % p. a. | Ø R netto |
|---|---|---|---|
| EURUSD | 442 | -0.21 | -0.017 |
| GBPUSD | 447 | -0.16 | -0.013 |
| USDJPY | 441 | -0.02 | -0.001 |
| AUDUSD | 462 | -0.64 | -0.050 |
| NZDUSD | 440 | -0.42 | -0.035 |
| USDCAD | 439 | -0.47 | -0.039 |
| USDCHF | 426 | +0.25 | +0.021 |
| XAUUSD | 422 | +0.51 | +0.044 |
| US500 | 424 | -0.46 | -0.039 |
| US100 | 407 | +0.19 | +0.017 |
| FRA40 | 302 | -0.48 | -0.057 |
| UK100 | 410 | -1.12 | -0.098 |
| JP225 | 435 | -0.17 | -0.014 |
| HK50 | 328 | -0.57 | -0.063 |
| AUS200 | 467 | -1.51 | -0.116 |
| Brent | 420 | +0.16 | +0.014 |
| Silber | 458 | -0.76 | -0.059 |

## TI-MACD (Nr. 64, H4)

| Kennzahl | Wert |
|---|---|
| Handelstage / Trades | 2,342 / 17,852 |
| Netto je Tag (bp des Kapitals, Portfolio) | -3.84 bp (σ 98.2 bp) |
| vor Kosten je Tag | +1.78 bp |
| Handelskosten + Swap-Belastung je Tag (Swap netto) | 5.89 bp (-1.99 bp) |
| Rendite p. a. (netto, 0,25 % Risiko je Trade) | -9.99 % |
| Sharpe Ratio p. a. (netto) | -0.63 |
| t-Wert iid / Woche / Monat | -1.89 / -1.62 / -1.54 |
| Ø R je Trade vor / nach Kosten | +0.009 / -0.020 |
| Trefferquote / Anteil Notfall-Stops / Anteil Long | 34% / 7% / 50% |
| Ø Haltedauer | 12.6 Kerzen (H4) |
| bei doppelten Kosten | -9.73 bp/Tag |

| Kriterium | Ergebnis | erfüllt |
|---|---|---|
| Mittleres Netto-Tagesergebnis > 0 mit t ≥ 3,0 (kleinster aus iid / Woche / Monat) | -3.84 bp/Tag, t = -1.89 | **nein** |
| ≥ 6 von 9 Jahren positiv | 3 von 9 | **nein** |
| ≥ 60 % der Instrumente positiv | 4 von 17 | **nein** |
| bei doppelten Kosten > 0 | -9.73 bp/Tag | **nein** |

**TI-MACD: nicht bestanden.**

| Jahr | Tage | Netto % |
|---|---|---|
| 2015 | 260 | +10.10 |
| 2016 | 260 | -21.35 |
| 2017 | 260 | -42.38 |
| 2018 | 261 | +3.73 |
| 2019 | 260 | -2.08 |
| 2020 | 261 | +28.69 |
| 2021 | 260 | -36.46 |
| 2022 | 260 | -16.65 |
| 2023 | 260 | -13.48 |

| Anlageklasse | Trades | Netto % p. a. |
|---|---|---|
| FX | 7719 | -3.40 |
| Metalle | 2192 | -2.57 |
| Indizes | 6847 | -2.94 |
| Öl | 1094 | -1.07 |

| Instrument | Trades | Netto % p. a. | Ø R netto |
|---|---|---|---|
| EURUSD | 1069 | +0.47 | +0.016 |
| GBPUSD | 1108 | -0.54 | -0.018 |
| USDJPY | 1038 | +0.72 | +0.025 |
| AUDUSD | 1143 | -1.33 | -0.042 |
| NZDUSD | 1136 | -1.14 | -0.036 |
| USDCAD | 1129 | -1.15 | -0.037 |
| USDCHF | 1096 | -0.43 | -0.014 |
| XAUUSD | 1083 | -0.16 | -0.005 |
| US500 | 1116 | -1.22 | -0.039 |
| US100 | 1061 | -0.63 | -0.021 |
| FRA40 | 718 | -0.24 | -0.012 |
| UK100 | 970 | -0.81 | -0.030 |
| JP225 | 1085 | +0.10 | +0.003 |
| HK50 | 814 | +0.57 | +0.025 |
| AUS200 | 1083 | -0.71 | -0.024 |
| Brent | 1094 | -1.07 | -0.035 |
| Silber | 1109 | -2.41 | -0.078 |

## TI-ADX (Nr. 69, H4)

| Kennzahl | Wert |
|---|---|
| Handelstage / Trades | 2,342 / 7,952 |
| Netto je Tag (bp des Kapitals, Portfolio) | -1.75 bp (σ 54.6 bp) |
| vor Kosten je Tag | +0.73 bp |
| Handelskosten + Swap-Belastung je Tag (Swap netto) | 2.60 bp (-0.91 bp) |
| Rendite p. a. (netto, 0,25 % Risiko je Trade) | -4.55 % |
| Sharpe Ratio p. a. (netto) | -0.52 |
| t-Wert iid / Woche / Monat | -1.55 / -1.30 / -0.96 |
| Ø R je Trade vor / nach Kosten | +0.009 / -0.021 |
| Trefferquote / Anteil Notfall-Stops / Anteil Long | 33% / 7% / 50% |
| Ø Haltedauer | 13.1 Kerzen (H4) |
| bei doppelten Kosten | -4.35 bp/Tag |

| Kriterium | Ergebnis | erfüllt |
|---|---|---|
| Mittleres Netto-Tagesergebnis > 0 mit t ≥ 3,0 (kleinster aus iid / Woche / Monat) | -1.75 bp/Tag, t = -1.55 | **nein** |
| ≥ 6 von 9 Jahren positiv | 2 von 9 | **nein** |
| ≥ 60 % der Instrumente positiv | 4 von 17 | **nein** |
| bei doppelten Kosten > 0 | -4.35 bp/Tag | **nein** |

**TI-ADX: nicht bestanden.**

| Jahr | Tage | Netto % |
|---|---|---|
| 2015 | 260 | -12.56 |
| 2016 | 260 | -3.30 |
| 2017 | 260 | -11.44 |
| 2018 | 261 | +2.54 |
| 2019 | 260 | -14.16 |
| 2020 | 261 | +23.51 |
| 2021 | 260 | -10.65 |
| 2022 | 260 | -11.35 |
| 2023 | 260 | -3.56 |

| Anlageklasse | Trades | Netto % p. a. |
|---|---|---|
| FX | 3418 | -2.36 |
| Metalle | 1007 | -0.23 |
| Indizes | 3037 | -1.02 |
| Öl | 490 | -0.94 |

| Instrument | Trades | Netto % p. a. | Ø R netto |
|---|---|---|---|
| EURUSD | 520 | -0.08 | -0.006 |
| GBPUSD | 519 | -0.30 | -0.021 |
| USDJPY | 471 | -0.15 | -0.012 |
| AUDUSD | 443 | -0.13 | -0.010 |
| NZDUSD | 444 | -0.50 | -0.040 |
| USDCAD | 508 | -0.50 | -0.035 |
| USDCHF | 513 | -0.70 | -0.049 |
| XAUUSD | 503 | +0.35 | +0.025 |
| US500 | 510 | -0.46 | -0.032 |
| US100 | 528 | +0.16 | +0.011 |
| FRA40 | 304 | -0.22 | -0.026 |
| UK100 | 376 | +0.14 | +0.013 |
| JP225 | 512 | +0.12 | +0.008 |
| HK50 | 366 | -0.19 | -0.019 |
| AUS200 | 441 | -0.56 | -0.046 |
| Brent | 490 | -0.94 | -0.069 |
| Silber | 504 | -0.58 | -0.042 |

## TI-PSAR (Nr. 70, H4)

| Kennzahl | Wert |
|---|---|
| Handelstage / Trades | 2,342 / 19,944 |
| Netto je Tag (bp des Kapitals, Portfolio) | -5.18 bp (σ 90.5 bp) |
| vor Kosten je Tag | +0.65 bp |
| Handelskosten + Swap-Belastung je Tag (Swap netto) | 6.12 bp (-1.88 bp) |
| Rendite p. a. (netto, 0,25 % Risiko je Trade) | -13.48 % |
| Sharpe Ratio p. a. (netto) | -0.92 |
| t-Wert iid / Woche / Monat | -2.77 / -2.65 / -2.78 |
| Ø R je Trade vor / nach Kosten | +0.003 / -0.024 |
| Trefferquote / Anteil Notfall-Stops / Anteil Long | 37% / 7% / 50% |
| Ø Haltedauer | 11.4 Kerzen (H4) |
| bei doppelten Kosten | -11.30 bp/Tag |

| Kriterium | Ergebnis | erfüllt |
|---|---|---|
| Mittleres Netto-Tagesergebnis > 0 mit t ≥ 3,0 (kleinster aus iid / Woche / Monat) | -5.18 bp/Tag, t = -2.78 | **nein** |
| ≥ 6 von 9 Jahren positiv | 2 von 9 | **nein** |
| ≥ 60 % der Instrumente positiv | 2 von 17 | **nein** |
| bei doppelten Kosten > 0 | -11.30 bp/Tag | **nein** |

**TI-PSAR: nicht bestanden.**

| Jahr | Tage | Netto % |
|---|---|---|
| 2015 | 260 | +3.24 |
| 2016 | 260 | -39.14 |
| 2017 | 260 | -24.13 |
| 2018 | 261 | -8.11 |
| 2019 | 260 | -11.28 |
| 2020 | 261 | +2.51 |
| 2021 | 260 | -25.97 |
| 2022 | 260 | -9.61 |
| 2023 | 260 | -8.85 |

| Anlageklasse | Trades | Netto % p. a. |
|---|---|---|
| FX | 8673 | -5.74 |
| Metalle | 2252 | -0.93 |
| Indizes | 7841 | -5.52 |
| Öl | 1178 | -1.30 |

| Instrument | Trades | Netto % p. a. | Ø R netto |
|---|---|---|---|
| EURUSD | 1207 | -0.46 | -0.014 |
| GBPUSD | 1210 | -0.28 | -0.008 |
| USDJPY | 1188 | +0.02 | +0.000 |
| AUDUSD | 1281 | -1.17 | -0.033 |
| NZDUSD | 1272 | -1.20 | -0.034 |
| USDCAD | 1272 | -1.63 | -0.046 |
| USDCHF | 1243 | -1.01 | -0.029 |
| XAUUSD | 1142 | -0.42 | -0.013 |
| US500 | 1261 | -2.02 | -0.058 |
| US100 | 1240 | +0.13 | +0.004 |
| FRA40 | 881 | -1.36 | -0.056 |
| UK100 | 1090 | -1.00 | -0.033 |
| JP225 | 1242 | -0.16 | -0.005 |
| HK50 | 865 | -0.32 | -0.013 |
| AUS200 | 1262 | -0.78 | -0.022 |
| Brent | 1178 | -1.30 | -0.040 |
| Silber | 1110 | -0.51 | -0.017 |

## TI-SUPER (Nr. 71, H4)

| Kennzahl | Wert |
|---|---|
| Handelstage / Trades | 2,342 / 6,249 |
| Netto je Tag (bp des Kapitals, Portfolio) | -1.51 bp (σ 70.5 bp) |
| vor Kosten je Tag | +1.41 bp |
| Handelskosten + Swap-Belastung je Tag (Swap netto) | 3.18 bp (-1.72 bp) |
| Rendite p. a. (netto, 0,25 % Risiko je Trade) | -3.93 % |
| Sharpe Ratio p. a. (netto) | -0.35 |
| t-Wert iid / Woche / Monat | -1.04 / -0.89 / -0.76 |
| Ø R je Trade vor / nach Kosten | +0.021 / -0.023 |
| Trefferquote / Anteil Notfall-Stops / Anteil Long | 35% / 29% / 50% |
| Ø Haltedauer | 34.3 Kerzen (H4) |
| bei doppelten Kosten | -4.70 bp/Tag |

| Kriterium | Ergebnis | erfüllt |
|---|---|---|
| Mittleres Netto-Tagesergebnis > 0 mit t ≥ 3,0 (kleinster aus iid / Woche / Monat) | -1.51 bp/Tag, t = -1.04 | **nein** |
| ≥ 6 von 9 Jahren positiv | 4 von 9 | **nein** |
| ≥ 60 % der Instrumente positiv | 5 von 17 | **nein** |
| bei doppelten Kosten > 0 | -4.70 bp/Tag | **nein** |

**TI-SUPER: nicht bestanden.**

| Jahr | Tage | Netto % |
|---|---|---|
| 2015 | 260 | -19.90 |
| 2016 | 260 | -3.42 |
| 2017 | 260 | -18.36 |
| 2018 | 261 | +11.39 |
| 2019 | 260 | -11.14 |
| 2020 | 261 | +15.09 |
| 2021 | 260 | -20.81 |
| 2022 | 260 | +8.70 |
| 2023 | 260 | +3.03 |

| Anlageklasse | Trades | Netto % p. a. |
|---|---|---|
| FX | 2658 | -2.05 |
| Metalle | 676 | +0.67 |
| Indizes | 2506 | -1.87 |
| Öl | 409 | -0.68 |

| Instrument | Trades | Netto % p. a. | Ø R netto |
|---|---|---|---|
| EURUSD | 399 | -0.64 | -0.058 |
| GBPUSD | 391 | -0.22 | -0.021 |
| USDJPY | 387 | -0.18 | -0.017 |
| AUDUSD | 383 | -0.79 | -0.074 |
| NZDUSD | 373 | -0.26 | -0.025 |
| USDCAD | 377 | -0.60 | -0.058 |
| USDCHF | 348 | +0.65 | +0.067 |
| XAUUSD | 358 | +0.32 | +0.032 |
| US500 | 401 | -0.83 | -0.074 |
| US100 | 427 | -0.28 | -0.023 |
| FRA40 | 273 | +0.24 | +0.031 |
| UK100 | 315 | -0.15 | -0.017 |
| JP225 | 398 | -0.42 | -0.038 |
| HK50 | 316 | +0.08 | +0.009 |
| AUS200 | 376 | -0.52 | -0.050 |
| Brent | 409 | -0.68 | -0.060 |
| Silber | 318 | +0.35 | +0.039 |

## TI-ICHI (Nr. 72, H4)

| Kennzahl | Wert |
|---|---|
| Handelstage / Trades | 2,342 / 10,386 |
| Netto je Tag (bp des Kapitals, Portfolio) | -2.68 bp (σ 64.7 bp) |
| vor Kosten je Tag | +0.57 bp |
| Handelskosten + Swap-Belastung je Tag (Swap netto) | 3.47 bp (-1.17 bp) |
| Rendite p. a. (netto, 0,25 % Risiko je Trade) | -6.98 % |
| Sharpe Ratio p. a. (netto) | -0.67 |
| t-Wert iid / Woche / Monat | -2.01 / -1.62 / -1.36 |
| Ø R je Trade vor / nach Kosten | +0.005 / -0.024 |
| Trefferquote / Anteil Notfall-Stops / Anteil Long | 28% / 7% / 52% |
| Ø Haltedauer | 14.9 Kerzen (H4) |
| bei doppelten Kosten | -6.15 bp/Tag |

| Kriterium | Ergebnis | erfüllt |
|---|---|---|
| Mittleres Netto-Tagesergebnis > 0 mit t ≥ 3,0 (kleinster aus iid / Woche / Monat) | -2.68 bp/Tag, t = -2.01 | **nein** |
| ≥ 6 von 9 Jahren positiv | 3 von 9 | **nein** |
| ≥ 60 % der Instrumente positiv | 2 von 17 | **nein** |
| bei doppelten Kosten > 0 | -6.15 bp/Tag | **nein** |

**TI-ICHI: nicht bestanden.**

| Jahr | Tage | Netto % |
|---|---|---|
| 2015 | 260 | -21.07 |
| 2016 | 260 | -9.45 |
| 2017 | 260 | -11.65 |
| 2018 | 261 | +2.12 |
| 2019 | 260 | -16.14 |
| 2020 | 261 | +19.83 |
| 2021 | 260 | -26.59 |
| 2022 | 260 | +6.37 |
| 2023 | 260 | -6.20 |

| Anlageklasse | Trades | Netto % p. a. |
|---|---|---|
| FX | 4548 | -4.25 |
| Metalle | 1279 | +0.18 |
| Indizes | 3947 | -2.83 |
| Öl | 612 | -0.08 |

| Instrument | Trades | Netto % p. a. | Ø R netto |
|---|---|---|---|
| EURUSD | 661 | -0.77 | -0.042 |
| GBPUSD | 634 | -0.44 | -0.025 |
| USDJPY | 626 | -0.20 | -0.012 |
| AUDUSD | 665 | -0.52 | -0.028 |
| NZDUSD | 661 | -0.89 | -0.048 |
| USDCAD | 660 | -0.86 | -0.047 |
| USDCHF | 641 | -0.57 | -0.032 |
| XAUUSD | 634 | +0.47 | +0.026 |
| US500 | 617 | -0.57 | -0.033 |
| US100 | 561 | +0.53 | +0.034 |
| FRA40 | 416 | -0.02 | -0.002 |
| UK100 | 575 | -0.96 | -0.060 |
| JP225 | 650 | -0.05 | -0.003 |
| HK50 | 467 | -0.34 | -0.026 |
| AUS200 | 661 | -1.42 | -0.078 |
| Brent | 612 | -0.08 | -0.005 |
| Silber | 645 | -0.28 | -0.016 |

## TI-HA (Nr. 73, H4)

| Kennzahl | Wert |
|---|---|
| Handelstage / Trades | 2,342 / 34,431 |
| Netto je Tag (bp des Kapitals, Portfolio) | -6.72 bp (σ 100.7 bp) |
| vor Kosten je Tag | +2.19 bp |
| Handelskosten + Swap-Belastung je Tag (Swap netto) | 9.20 bp (-1.90 bp) |
| Rendite p. a. (netto, 0,25 % Risiko je Trade) | -17.49 % |
| Sharpe Ratio p. a. (netto) | -1.08 |
| t-Wert iid / Woche / Monat | -3.23 / -3.19 / -3.16 |
| Ø R je Trade vor / nach Kosten | +0.006 / -0.018 |
| Trefferquote / Anteil Notfall-Stops / Anteil Long | 35% / 4% / 50% |
| Ø Haltedauer | 6.6 Kerzen (H4) |
| bei doppelten Kosten | -15.93 bp/Tag |

| Kriterium | Ergebnis | erfüllt |
|---|---|---|
| Mittleres Netto-Tagesergebnis > 0 mit t ≥ 3,0 (kleinster aus iid / Woche / Monat) | -6.72 bp/Tag, t = -3.23 | **nein** |
| ≥ 6 von 9 Jahren positiv | 2 von 9 | **nein** |
| ≥ 60 % der Instrumente positiv | 1 von 17 | **nein** |
| bei doppelten Kosten > 0 | -15.93 bp/Tag | **nein** |

**TI-HA: nicht bestanden.**

| Jahr | Tage | Netto % |
|---|---|---|
| 2015 | 260 | -6.88 |
| 2016 | 260 | -29.71 |
| 2017 | 260 | -41.55 |
| 2018 | 261 | -15.89 |
| 2019 | 260 | -32.02 |
| 2020 | 261 | +26.74 |
| 2021 | 260 | -34.19 |
| 2022 | 260 | -24.30 |
| 2023 | 260 | +0.36 |

| Anlageklasse | Trades | Netto % p. a. |
|---|---|---|
| FX | 14946 | -8.14 |
| Metalle | 4316 | -3.66 |
| Indizes | 13170 | -4.55 |
| Öl | 1999 | -1.15 |

| Instrument | Trades | Netto % p. a. | Ø R netto |
|---|---|---|---|
| EURUSD | 2111 | -0.96 | -0.016 |
| GBPUSD | 2104 | -0.97 | -0.017 |
| USDJPY | 2131 | -0.09 | -0.002 |
| AUDUSD | 2144 | -1.18 | -0.020 |
| NZDUSD | 2151 | -1.03 | -0.017 |
| USDCAD | 2162 | -1.92 | -0.032 |
| USDCHF | 2143 | -1.99 | -0.034 |
| XAUUSD | 2135 | -0.23 | -0.004 |
| US500 | 2032 | -0.37 | -0.007 |
| US100 | 1995 | +0.61 | +0.011 |
| FRA40 | 1476 | -1.42 | -0.035 |
| UK100 | 1805 | -1.09 | -0.022 |
| JP225 | 2203 | -0.73 | -0.012 |
| HK50 | 1581 | -0.53 | -0.012 |
| AUS200 | 2078 | -1.02 | -0.018 |
| Brent | 1999 | -1.15 | -0.021 |
| Silber | 2181 | -3.43 | -0.057 |

## TI-KALMAN (Nr. 76, H4)

| Kennzahl | Wert |
|---|---|
| Handelstage / Trades | 2,342 / 12,526 |
| Netto je Tag (bp des Kapitals, Portfolio) | -3.12 bp (σ 87.6 bp) |
| vor Kosten je Tag | +1.31 bp |
| Handelskosten + Swap-Belastung je Tag (Swap netto) | 4.72 bp (-1.87 bp) |
| Rendite p. a. (netto, 0,25 % Risiko je Trade) | -8.11 % |
| Sharpe Ratio p. a. (netto) | -0.57 |
| t-Wert iid / Woche / Monat | -1.72 / -1.48 / -1.34 |
| Ø R je Trade vor / nach Kosten | +0.010 / -0.023 |
| Trefferquote / Anteil Notfall-Stops / Anteil Long | 32% / 9% / 50% |
| Ø Haltedauer | 17.9 Kerzen (H4) |
| bei doppelten Kosten | -7.83 bp/Tag |

| Kriterium | Ergebnis | erfüllt |
|---|---|---|
| Mittleres Netto-Tagesergebnis > 0 mit t ≥ 3,0 (kleinster aus iid / Woche / Monat) | -3.12 bp/Tag, t = -1.72 | **nein** |
| ≥ 6 von 9 Jahren positiv | 2 von 9 | **nein** |
| ≥ 60 % der Instrumente positiv | 4 von 17 | **nein** |
| bei doppelten Kosten > 0 | -7.83 bp/Tag | **nein** |

**TI-KALMAN: nicht bestanden.**

| Jahr | Tage | Netto % |
|---|---|---|
| 2015 | 260 | -12.88 |
| 2016 | 260 | -13.45 |
| 2017 | 260 | -28.48 |
| 2018 | 261 | +18.28 |
| 2019 | 260 | -9.79 |
| 2020 | 261 | +29.54 |
| 2021 | 260 | -36.03 |
| 2022 | 260 | -7.84 |
| 2023 | 260 | -12.33 |

| Anlageklasse | Trades | Netto % p. a. |
|---|---|---|
| FX | 5343 | -1.61 |
| Metalle | 1541 | -0.56 |
| Indizes | 4888 | -4.91 |
| Öl | 754 | -1.02 |

| Instrument | Trades | Netto % p. a. | Ø R netto |
|---|---|---|---|
| EURUSD | 755 | -0.09 | -0.004 |
| GBPUSD | 731 | +0.71 | +0.035 |
| USDJPY | 739 | +0.88 | +0.043 |
| AUDUSD | 755 | -0.66 | -0.031 |
| NZDUSD | 788 | -0.69 | -0.031 |
| USDCAD | 801 | -1.50 | -0.068 |
| USDCHF | 774 | -0.27 | -0.012 |
| XAUUSD | 774 | +0.52 | +0.024 |
| US500 | 800 | -1.67 | -0.075 |
| US100 | 729 | -0.63 | -0.031 |
| FRA40 | 534 | -0.59 | -0.040 |
| UK100 | 704 | -1.43 | -0.073 |
| JP225 | 756 | +0.23 | +0.011 |
| HK50 | 552 | -0.20 | -0.013 |
| AUS200 | 813 | -0.63 | -0.028 |
| Brent | 754 | -1.02 | -0.049 |
| Silber | 767 | -1.08 | -0.050 |

## Übersicht

| Variante | Nr. | TF | Trades | Netto bp/Tag | vor Kosten bp/Tag | Ø R vor / nach Kosten | t | Jahre + | Instr. + |
|---|---|---|---|---|---|---|---|---|---|
| TI-MA200 | 61 | D1 | 221 | -0.52 | -0.18 | -0.077 / -0.220 | -1.39 | 4 | 5 |
| TI-EMA921 | 62 | H1 | 36,667 | -13.37 | +5.20 | +0.013 / -0.034 | -3.49 | 1 | 4 |
| TI-TRIPLE | 63 | H4 | 7,170 | -2.26 | +0.56 | +0.007 / -0.030 | -1.55 | 2 | 4 |
| TI-MACD | 64 | H4 | 17,852 | -3.84 | +1.78 | +0.009 / -0.020 | -1.89 | 3 | 4 |
| TI-ADX | 69 | H4 | 7,952 | -1.75 | +0.73 | +0.009 / -0.021 | -1.55 | 2 | 4 |
| TI-PSAR | 70 | H4 | 19,944 | -5.18 | +0.65 | +0.003 / -0.024 | -2.78 | 2 | 2 |
| TI-SUPER | 71 | H4 | 6,249 | -1.51 | +1.41 | +0.021 / -0.023 | -1.04 | 4 | 5 |
| TI-ICHI | 72 | H4 | 10,386 | -2.68 | +0.57 | +0.005 / -0.024 | -2.01 | 3 | 2 |
| TI-HA | 73 | H4 | 34,431 | -6.72 | +2.19 | +0.006 / -0.018 | -3.23 | 2 | 1 |
| TI-KALMAN | 76 | H4 | 12,526 | -3.12 | +1.31 | +0.010 / -0.023 | -1.72 | 2 | 4 |

**Ergebnis: Keine Variante erfüllt alle In-Sample-Kriterien. Strategien Nr. 61–64, 69–73 und 76 sind gescheitert; der Hold-out bleibt unberührt.**
