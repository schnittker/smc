# Modell OS (Oszillatoren, Divergenzen, Renko), In-Sample 2015–2023 (Trial T249–T254)

Lauf vom 24.10.2026. Regeln laut `docs/01_Vorregistrierung.md`, Code `research/osc/`. 17 Instrumente; Einstieg zur nächsten Eröffnung, Stop 2 ATR14 (Renko: Notfall-Stop 3 ATR14, Divergenz: hinter dem Swing, Ziel 2R); 0,25 % Risiko je Trade. Netto = nach Spread, Slippage, Kommission und Swaps; Ergebnis eines Trades am Tag des Ausstiegs; Portfolio = Summe aller Instrumente je Tag.

## OS-RSI (Nr. 65, H1)

| Kennzahl | Wert |
|---|---|
| Handelstage / Trades | 2,342 / 20,824 |
| Netto je Tag (bp des Kapitals, Portfolio) | -15.78 bp (σ 110.5 bp) |
| vor Kosten je Tag | -2.74 bp |
| Handelskosten + Swap-Belastung je Tag (Swap netto) | 13.20 bp (-1.30 bp) |
| Rendite p. a. (netto, 0,25 % Risiko je Trade) | -41.05 % |
| Sharpe Ratio p. a. (netto) | -2.30 |
| t-Wert iid / Woche / Monat | -6.91 / -7.26 / -7.78 |
| Ø R je Trade vor / nach Kosten | -0.012 / -0.071 |
| Trefferquote / Anteil Stops / Anteil Long | 52% / 46% / 49% |
| Ø Haltedauer | 9.6 Kerzen (H1) |
| bei doppelten Kosten | -28.97 bp/Tag |

| Kriterium | Ergebnis | erfüllt |
|---|---|---|
| Mittleres Netto-Tagesergebnis > 0 mit t ≥ 3,0 (kleinster aus iid / Woche / Monat) | -15.78 bp/Tag, t = -7.78 | **nein** |
| ≥ 6 von 9 Jahren positiv | 0 von 9 | **nein** |
| ≥ 60 % der Instrumente positiv | 0 von 17 | **nein** |
| bei doppelten Kosten > 0 | -28.97 bp/Tag | **nein** |

**OS-RSI: nicht bestanden.**

| Jahr | Tage | Netto % |
|---|---|---|
| 2015 | 260 | -42.09 |
| 2016 | 260 | -43.34 |
| 2017 | 260 | -34.33 |
| 2018 | 261 | -48.02 |
| 2019 | 260 | -52.61 |
| 2020 | 261 | -64.67 |
| 2021 | 260 | -52.45 |
| 2022 | 260 | -17.21 |
| 2023 | 260 | -14.77 |

| Anlageklasse | Trades | Netto % p. a. |
|---|---|---|
| FX | 9189 | -16.04 |
| Metalle | 2523 | -9.86 |
| Indizes | 7796 | -10.32 |
| Öl | 1316 | -4.83 |

| Instrument | Trades | Netto % p. a. | Ø R netto |
|---|---|---|---|
| EURUSD | 1321 | -2.47 | -0.067 |
| GBPUSD | 1348 | -0.32 | -0.008 |
| USDJPY | 1383 | -2.24 | -0.058 |
| AUDUSD | 1302 | -3.27 | -0.090 |
| NZDUSD | 1310 | -3.96 | -0.109 |
| USDCAD | 1267 | -0.71 | -0.020 |
| USDCHF | 1258 | -3.07 | -0.088 |
| XAUUSD | 1314 | -3.01 | -0.083 |
| US500 | 1322 | -1.55 | -0.042 |
| US100 | 1426 | -1.59 | -0.040 |
| FRA40 | 773 | -0.75 | -0.035 |
| UK100 | 937 | -1.34 | -0.052 |
| JP225 | 1322 | -1.97 | -0.054 |
| HK50 | 953 | -1.49 | -0.056 |
| AUS200 | 1063 | -1.62 | -0.055 |
| Brent | 1316 | -4.83 | -0.132 |
| Silber | 1209 | -6.85 | -0.204 |

## OS-STOCH (Nr. 66, H1)

| Kennzahl | Wert |
|---|---|
| Handelstage / Trades | 2,342 / 40,271 |
| Netto je Tag (bp des Kapitals, Portfolio) | -29.84 bp (σ 148.3 bp) |
| vor Kosten je Tag | -3.86 bp |
| Handelskosten + Swap-Belastung je Tag (Swap netto) | 26.21 bp (-2.27 bp) |
| Rendite p. a. (netto, 0,25 % Risiko je Trade) | -77.65 % |
| Sharpe Ratio p. a. (netto) | -3.25 |
| t-Wert iid / Woche / Monat | -9.74 / -10.27 / -10.60 |
| Ø R je Trade vor / nach Kosten | -0.009 / -0.069 |
| Trefferquote / Anteil Stops / Anteil Long | 54% / 40% / 46% |
| Ø Haltedauer | 7.8 Kerzen (H1) |
| bei doppelten Kosten | -56.05 bp/Tag |

| Kriterium | Ergebnis | erfüllt |
|---|---|---|
| Mittleres Netto-Tagesergebnis > 0 mit t ≥ 3,0 (kleinster aus iid / Woche / Monat) | -29.84 bp/Tag, t = -10.60 | **nein** |
| ≥ 6 von 9 Jahren positiv | 0 von 9 | **nein** |
| ≥ 60 % der Instrumente positiv | 0 von 17 | **nein** |
| bei doppelten Kosten > 0 | -56.05 bp/Tag | **nein** |

**OS-STOCH: nicht bestanden.**

| Jahr | Tage | Netto % |
|---|---|---|
| 2015 | 260 | -45.27 |
| 2016 | 260 | -76.24 |
| 2017 | 260 | -73.56 |
| 2018 | 261 | -84.19 |
| 2019 | 260 | -92.76 |
| 2020 | 261 | -130.52 |
| 2021 | 260 | -83.69 |
| 2022 | 260 | -57.63 |
| 2023 | 260 | -54.98 |

| Anlageklasse | Trades | Netto % p. a. |
|---|---|---|
| FX | 17941 | -27.66 |
| Metalle | 4588 | -15.78 |
| Indizes | 15326 | -25.20 |
| Öl | 2416 | -9.01 |

| Instrument | Trades | Netto % p. a. | Ø R netto |
|---|---|---|---|
| EURUSD | 2426 | -1.96 | -0.029 |
| GBPUSD | 2433 | -1.61 | -0.024 |
| USDJPY | 2613 | -6.22 | -0.086 |
| AUDUSD | 2778 | -4.16 | -0.054 |
| NZDUSD | 2742 | -6.96 | -0.091 |
| USDCAD | 2560 | -4.61 | -0.065 |
| USDCHF | 2389 | -2.14 | -0.032 |
| XAUUSD | 2373 | -2.72 | -0.041 |
| US500 | 2484 | -3.35 | -0.049 |
| US100 | 2442 | -3.18 | -0.047 |
| FRA40 | 1662 | -3.61 | -0.078 |
| UK100 | 2033 | -3.72 | -0.066 |
| JP225 | 2589 | -3.25 | -0.045 |
| HK50 | 1559 | -2.53 | -0.059 |
| AUS200 | 2557 | -5.55 | -0.078 |
| Brent | 2416 | -9.01 | -0.134 |
| Silber | 2215 | -13.06 | -0.212 |

## OS-WPR (Nr. 67, H1)

| Kennzahl | Wert |
|---|---|
| Handelstage / Trades | 2,342 / 77,419 |
| Netto je Tag (bp des Kapitals, Portfolio) | -50.26 bp (σ 145.0 bp) |
| vor Kosten je Tag | -1.03 bp |
| Handelskosten + Swap-Belastung je Tag (Swap netto) | 49.52 bp (-2.36 bp) |
| Rendite p. a. (netto, 0,25 % Risiko je Trade) | -130.78 % |
| Sharpe Ratio p. a. (netto) | -5.59 |
| t-Wert iid / Woche / Monat | -16.77 / -16.51 / -16.16 |
| Ø R je Trade vor / nach Kosten | -0.001 / -0.061 |
| Trefferquote / Anteil Stops / Anteil Long | 58% / 29% / 49% |
| Ø Haltedauer | 4.6 Kerzen (H1) |
| bei doppelten Kosten | -99.78 bp/Tag |

| Kriterium | Ergebnis | erfüllt |
|---|---|---|
| Mittleres Netto-Tagesergebnis > 0 mit t ≥ 3,0 (kleinster aus iid / Woche / Monat) | -50.26 bp/Tag, t = -16.77 | **nein** |
| ≥ 6 von 9 Jahren positiv | 0 von 9 | **nein** |
| ≥ 60 % der Instrumente positiv | 0 von 17 | **nein** |
| bei doppelten Kosten > 0 | -99.78 bp/Tag | **nein** |

**OS-WPR: nicht bestanden.**

| Jahr | Tage | Netto % |
|---|---|---|
| 2015 | 260 | -92.21 |
| 2016 | 260 | -117.54 |
| 2017 | 260 | -158.25 |
| 2018 | 261 | -143.69 |
| 2019 | 260 | -148.17 |
| 2020 | 261 | -160.71 |
| 2021 | 260 | -163.89 |
| 2022 | 260 | -75.60 |
| 2023 | 260 | -116.94 |

| Anlageklasse | Trades | Netto % p. a. |
|---|---|---|
| FX | 35177 | -48.56 |
| Metalle | 9457 | -35.40 |
| Indizes | 28197 | -30.34 |
| Öl | 4588 | -16.48 |

| Instrument | Trades | Netto % p. a. | Ø R netto |
|---|---|---|---|
| EURUSD | 5071 | -7.14 | -0.051 |
| GBPUSD | 5079 | -5.33 | -0.038 |
| USDJPY | 4793 | -8.88 | -0.067 |
| AUDUSD | 5006 | -6.14 | -0.044 |
| NZDUSD | 5039 | -9.81 | -0.070 |
| USDCAD | 5096 | -6.74 | -0.048 |
| USDCHF | 5093 | -4.52 | -0.032 |
| XAUUSD | 4666 | -8.61 | -0.066 |
| US500 | 4809 | -3.12 | -0.023 |
| US100 | 4764 | -1.88 | -0.014 |
| FRA40 | 2955 | -4.64 | -0.057 |
| UK100 | 3807 | -4.64 | -0.044 |
| JP225 | 4634 | -7.96 | -0.062 |
| HK50 | 2625 | -2.80 | -0.038 |
| AUS200 | 4603 | -5.29 | -0.041 |
| Brent | 4588 | -16.48 | -0.129 |
| Silber | 4791 | -26.79 | -0.201 |

## OS-CCI (Nr. 68, H4)

| Kennzahl | Wert |
|---|---|
| Handelstage / Trades | 2,342 / 11,909 |
| Netto je Tag (bp des Kapitals, Portfolio) | -2.92 bp (σ 105.7 bp) |
| vor Kosten je Tag | +2.52 bp |
| Handelskosten + Swap-Belastung je Tag (Swap netto) | 5.76 bp (-1.86 bp) |
| Rendite p. a. (netto, 0,25 % Risiko je Trade) | -7.60 % |
| Sharpe Ratio p. a. (netto) | -0.45 |
| t-Wert iid / Woche / Monat | -1.34 / -1.13 / -1.10 |
| Ø R je Trade vor / nach Kosten | +0.020 / -0.023 |
| Trefferquote / Anteil Stops / Anteil Long | 32% / 26% / 51% |
| Ø Haltedauer | 13.2 Kerzen (H4) |
| bei doppelten Kosten | -8.68 bp/Tag |

| Kriterium | Ergebnis | erfüllt |
|---|---|---|
| Mittleres Netto-Tagesergebnis > 0 mit t ≥ 3,0 (kleinster aus iid / Woche / Monat) | -2.92 bp/Tag, t = -1.34 | **nein** |
| ≥ 6 von 9 Jahren positiv | 2 von 9 | **nein** |
| ≥ 60 % der Instrumente positiv | 5 von 17 | **nein** |
| bei doppelten Kosten > 0 | -8.68 bp/Tag | **nein** |

**OS-CCI: nicht bestanden.**

| Jahr | Tage | Netto % |
|---|---|---|
| 2015 | 260 | -11.73 |
| 2016 | 260 | -4.16 |
| 2017 | 260 | -30.18 |
| 2018 | 261 | +13.93 |
| 2019 | 260 | -3.62 |
| 2020 | 261 | +36.20 |
| 2021 | 260 | -42.21 |
| 2022 | 260 | -14.20 |
| 2023 | 260 | -12.43 |

| Anlageklasse | Trades | Netto % p. a. |
|---|---|---|
| FX | 5162 | -5.44 |
| Metalle | 1401 | +0.78 |
| Indizes | 4622 | -1.90 |
| Öl | 724 | -1.04 |

| Instrument | Trades | Netto % p. a. | Ø R netto |
|---|---|---|---|
| EURUSD | 724 | -0.75 | -0.037 |
| GBPUSD | 722 | +0.24 | +0.012 |
| USDJPY | 708 | +1.07 | +0.055 |
| AUDUSD | 764 | -1.66 | -0.078 |
| NZDUSD | 750 | -1.60 | -0.077 |
| USDCAD | 757 | -2.43 | -0.115 |
| USDCHF | 737 | -0.31 | -0.015 |
| XAUUSD | 704 | +0.81 | +0.041 |
| US500 | 738 | -1.37 | -0.067 |
| US100 | 712 | -0.16 | -0.008 |
| FRA40 | 529 | -0.74 | -0.051 |
| UK100 | 663 | -0.91 | -0.049 |
| JP225 | 718 | +0.85 | +0.042 |
| HK50 | 526 | +1.05 | +0.072 |
| AUS200 | 736 | -0.62 | -0.030 |
| Brent | 724 | -1.04 | -0.052 |
| Silber | 697 | -0.03 | -0.002 |

## OS-RENKO (Nr. 74, H1)

| Kennzahl | Wert |
|---|---|
| Handelstage / Trades | 2,342 / 9,839 |
| Netto je Tag (bp des Kapitals, Portfolio) | -4.71 bp (σ 117.2 bp) |
| vor Kosten je Tag | +1.39 bp |
| Handelskosten + Swap-Belastung je Tag (Swap netto) | 6.51 bp (-2.53 bp) |
| Rendite p. a. (netto, 0,25 % Risiko je Trade) | -12.26 % |
| Sharpe Ratio p. a. (netto) | -0.65 |
| t-Wert iid / Woche / Monat | -1.94 / -1.72 / -1.62 |
| Ø R je Trade vor / nach Kosten | +0.013 / -0.045 |
| Trefferquote / Anteil Stops / Anteil Long | 29% / 53% / 50% |
| Ø Haltedauer | 64.3 Kerzen (H1) |
| bei doppelten Kosten | -11.22 bp/Tag |

| Kriterium | Ergebnis | erfüllt |
|---|---|---|
| Mittleres Netto-Tagesergebnis > 0 mit t ≥ 3,0 (kleinster aus iid / Woche / Monat) | -4.71 bp/Tag, t = -1.94 | **nein** |
| ≥ 6 von 9 Jahren positiv | 3 von 9 | **nein** |
| ≥ 60 % der Instrumente positiv | 4 von 17 | **nein** |
| bei doppelten Kosten > 0 | -11.22 bp/Tag | **nein** |

**OS-RENKO: nicht bestanden.**

| Jahr | Tage | Netto % |
|---|---|---|
| 2015 | 260 | -27.19 |
| 2016 | 260 | -6.69 |
| 2017 | 260 | -50.99 |
| 2018 | 261 | +18.14 |
| 2019 | 260 | -34.67 |
| 2020 | 261 | +19.11 |
| 2021 | 260 | -32.22 |
| 2022 | 260 | +9.72 |
| 2023 | 260 | -5.53 |

| Anlageklasse | Trades | Netto % p. a. |
|---|---|---|
| FX | 4264 | -2.93 |
| Metalle | 1053 | -1.07 |
| Indizes | 3916 | -5.37 |
| Öl | 606 | -2.88 |

| Instrument | Trades | Netto % p. a. | Ø R netto |
|---|---|---|---|
| EURUSD | 598 | -1.01 | -0.061 |
| GBPUSD | 579 | +1.50 | +0.093 |
| USDJPY | 598 | +0.33 | +0.020 |
| AUDUSD | 645 | -0.89 | -0.050 |
| NZDUSD | 600 | -1.03 | -0.062 |
| USDCAD | 654 | -1.76 | -0.097 |
| USDCHF | 590 | -0.08 | -0.005 |
| XAUUSD | 546 | +0.59 | +0.039 |
| US500 | 641 | -0.52 | -0.029 |
| US100 | 680 | -0.17 | -0.009 |
| FRA40 | 392 | -1.02 | -0.093 |
| UK100 | 527 | -0.66 | -0.045 |
| JP225 | 653 | -1.37 | -0.076 |
| HK50 | 434 | +0.21 | +0.017 |
| AUS200 | 589 | -1.84 | -0.113 |
| Brent | 606 | -2.88 | -0.171 |
| Silber | 507 | -1.66 | -0.118 |

## OS-DIV (Nr. 75, H4)

| Kennzahl | Wert |
|---|---|
| Handelstage / Trades | 2,342 / 1,629 |
| Netto je Tag (bp des Kapitals, Portfolio) | -1.59 bp (σ 29.7 bp) |
| vor Kosten je Tag | -0.75 bp |
| Handelskosten + Swap-Belastung je Tag (Swap netto) | 0.88 bp (-0.24 bp) |
| Rendite p. a. (netto, 0,25 % Risiko je Trade) | -4.14 % |
| Sharpe Ratio p. a. (netto) | -0.86 |
| t-Wert iid / Woche / Monat | -2.59 / -2.25 / -2.30 |
| Ø R je Trade vor / nach Kosten | -0.043 / -0.091 |
| Trefferquote / Anteil Stops / Anteil Long | 35% / 60% / 46% |
| Ø Haltedauer | 12.3 Kerzen (H4) |
| bei doppelten Kosten | -2.47 bp/Tag |

| Kriterium | Ergebnis | erfüllt |
|---|---|---|
| Mittleres Netto-Tagesergebnis > 0 mit t ≥ 3,0 (kleinster aus iid / Woche / Monat) | -1.59 bp/Tag, t = -2.59 | **nein** |
| ≥ 6 von 9 Jahren positiv | 2 von 9 | **nein** |
| ≥ 60 % der Instrumente positiv | 4 von 17 | **nein** |
| bei doppelten Kosten > 0 | -2.47 bp/Tag | **nein** |

**OS-DIV: nicht bestanden.**

| Jahr | Tage | Netto % |
|---|---|---|
| 2015 | 260 | -5.85 |
| 2016 | 260 | +3.43 |
| 2017 | 260 | -13.09 |
| 2018 | 261 | -7.86 |
| 2019 | 260 | -0.18 |
| 2020 | 261 | +4.46 |
| 2021 | 260 | -0.09 |
| 2022 | 260 | -9.23 |
| 2023 | 260 | -8.86 |

| Anlageklasse | Trades | Netto % p. a. |
|---|---|---|
| FX | 659 | -0.38 |
| Metalle | 220 | -1.17 |
| Indizes | 660 | -2.32 |
| Öl | 90 | -0.27 |

| Instrument | Trades | Netto % p. a. | Ø R netto |
|---|---|---|---|
| EURUSD | 100 | -0.25 | -0.091 |
| GBPUSD | 100 | -0.29 | -0.104 |
| USDJPY | 88 | -0.22 | -0.090 |
| AUDUSD | 88 | +0.16 | +0.067 |
| NZDUSD | 87 | -0.13 | -0.052 |
| USDCAD | 107 | +0.44 | +0.148 |
| USDCHF | 89 | -0.09 | -0.037 |
| XAUUSD | 111 | -0.20 | -0.064 |
| US500 | 111 | -0.10 | -0.032 |
| US100 | 141 | -0.76 | -0.194 |
| FRA40 | 73 | +0.05 | +0.025 |
| UK100 | 78 | -0.49 | -0.224 |
| JP225 | 96 | -0.36 | -0.137 |
| HK50 | 86 | -0.88 | -0.369 |
| AUS200 | 75 | +0.22 | +0.105 |
| Brent | 90 | -0.27 | -0.109 |
| Silber | 109 | -0.98 | -0.322 |

## Übersicht

| Variante | Nr. | TF | Trades | Netto bp/Tag | vor Kosten bp/Tag | Ø R vor / nach Kosten | t | Jahre + | Instr. + |
|---|---|---|---|---|---|---|---|---|---|
| OS-RSI | 65 | H1 | 20,824 | -15.78 | -2.74 | -0.012 / -0.071 | -7.78 | 0 | 0 |
| OS-STOCH | 66 | H1 | 40,271 | -29.84 | -3.86 | -0.009 / -0.069 | -10.60 | 0 | 0 |
| OS-WPR | 67 | H1 | 77,419 | -50.26 | -1.03 | -0.001 / -0.061 | -16.77 | 0 | 0 |
| OS-CCI | 68 | H4 | 11,909 | -2.92 | +2.52 | +0.020 / -0.023 | -1.34 | 2 | 5 |
| OS-RENKO | 74 | H1 | 9,839 | -4.71 | +1.39 | +0.013 / -0.045 | -1.94 | 3 | 4 |
| OS-DIV | 75 | H4 | 1,629 | -1.59 | -0.75 | -0.043 / -0.091 | -2.59 | 2 | 4 |

**Ergebnis: Keine Variante erfüllt alle In-Sample-Kriterien. Strategien Nr. 65–68, 74 und 75 sind gescheitert; der Hold-out bleibt unberührt.**
