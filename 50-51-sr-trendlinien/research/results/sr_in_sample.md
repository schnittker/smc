# Modell SR (S/R-Zonen, Trendlinien), In-Sample 2015–2023 (Trial T174 SR-BOUNCE, T175 SR-BREAK, T176 SR-TLINE)

Lauf vom 24.10.2026. Regeln laut `docs/01_Vorregistrierung.md`, Code `research/chart/`. 17 Instrumente, H4-Serverkerzen; Swings 3/3, Zonen ±0,25 ATR, Einstieg zur nächsten Eröffnung, Stop hinter Zone bzw. Swing (≥ 1 ATR), Ziel 2R, Zeitstopp 30 Kerzen; 0,25 % Risiko je Trade. Netto = nach Spread, Slippage, Kommission und Swaps; Ergebnis eines Trades am Tag des Ausstiegs; Portfolio = Summe aller Instrumente je Tag.

## SR-BOUNCE

| Kennzahl | Wert |
|---|---|
| Handelstage / Trades | 2,342 / 12,608 |
| Netto je Tag (bp des Kapitals, Portfolio) | -8.48 bp (σ 85.1 bp) |
| vor Kosten je Tag | -2.08 bp |
| Handelskosten + Swap-Belastung je Tag (Swap netto) | 6.71 bp (-1.78 bp) |
| Rendite p. a. (netto, 0,25 % Risiko je Trade) | -22.06 % |
| Sharpe Ratio p. a. (netto) | -1.61 |
| t-Wert iid / Woche / Monat | -4.82 / -4.67 / -4.85 |
| Ø R je Trade vor / nach Kosten | -0.015 / -0.063 |
| Trefferquote / Anteil Long | 34% / 55% |
| Ausstiege Ziel / Stop / Zeit | 27% / 63% / 10% |
| Ø Haltedauer | 11.7 H4-Kerzen |
| bei doppelten Kosten | -15.19 bp/Tag |

| Kriterium | Ergebnis | erfüllt |
|---|---|---|
| Mittleres Netto-Tagesergebnis > 0 mit t ≥ 3,0 (kleinster aus iid / Woche / Monat) | -8.48 bp/Tag, t = -4.85 | **nein** |
| ≥ 6 von 9 Jahren positiv | 1 von 9 | **nein** |
| ≥ 60 % der Instrumente positiv | 2 von 17 | **nein** |
| bei doppelten Kosten > 0 | -15.19 bp/Tag | **nein** |

**SR-BOUNCE: nicht bestanden.**

| Jahr | Tage | Netto % |
|---|---|---|
| 2015 | 260 | -16.46 |
| 2016 | 260 | +6.69 |
| 2017 | 260 | -33.82 |
| 2018 | 261 | -39.68 |
| 2019 | 260 | -19.77 |
| 2020 | 261 | -30.89 |
| 2021 | 260 | -45.31 |
| 2022 | 260 | -17.23 |
| 2023 | 260 | -2.07 |

| Anlageklasse | Trades | Netto % p. a. |
|---|---|---|
| FX | 5450 | -6.58 |
| Metalle | 1532 | -4.85 |
| Indizes | 4855 | -9.53 |
| Öl | 771 | -1.10 |

| Instrument | Trades | Netto % p. a. | Ø R netto |
|---|---|---|---|
| EURUSD | 808 | -1.55 | -0.069 |
| GBPUSD | 786 | +0.11 | +0.005 |
| USDJPY | 764 | -1.51 | -0.071 |
| AUDUSD | 790 | -1.78 | -0.081 |
| NZDUSD | 763 | -0.26 | -0.012 |
| USDCAD | 768 | -0.24 | -0.011 |
| USDCHF | 771 | -1.36 | -0.064 |
| XAUUSD | 750 | -1.17 | -0.056 |
| US500 | 796 | -2.84 | -0.128 |
| US100 | 740 | +1.10 | +0.054 |
| FRA40 | 525 | -2.03 | -0.139 |
| UK100 | 672 | -1.26 | -0.067 |
| JP225 | 786 | -1.59 | -0.073 |
| HK50 | 608 | -1.51 | -0.089 |
| AUS200 | 728 | -1.40 | -0.069 |
| Brent | 771 | -1.10 | -0.051 |
| Silber | 782 | -3.68 | -0.170 |

## SR-BREAK

| Kennzahl | Wert |
|---|---|
| Handelstage / Trades | 2,342 / 12,088 |
| Netto je Tag (bp des Kapitals, Portfolio) | -6.97 bp (σ 90.1 bp) |
| vor Kosten je Tag | -0.71 bp |
| Handelskosten + Swap-Belastung je Tag (Swap netto) | 6.54 bp (-1.72 bp) |
| Rendite p. a. (netto, 0,25 % Risiko je Trade) | -18.13 % |
| Sharpe Ratio p. a. (netto) | -1.25 |
| t-Wert iid / Woche / Monat | -3.74 / -3.56 / -3.36 |
| Ø R je Trade vor / nach Kosten | -0.006 / -0.054 |
| Trefferquote / Anteil Long | 34% / 50% |
| Ausstiege Ziel / Stop / Zeit | 28% / 63% / 9% |
| Ø Haltedauer | 11.1 H4-Kerzen |
| bei doppelten Kosten | -13.51 bp/Tag |

| Kriterium | Ergebnis | erfüllt |
|---|---|---|
| Mittleres Netto-Tagesergebnis > 0 mit t ≥ 3,0 (kleinster aus iid / Woche / Monat) | -6.97 bp/Tag, t = -3.74 | **nein** |
| ≥ 6 von 9 Jahren positiv | 1 von 9 | **nein** |
| ≥ 60 % der Instrumente positiv | 3 von 17 | **nein** |
| bei doppelten Kosten > 0 | -13.51 bp/Tag | **nein** |

**SR-BREAK: nicht bestanden.**

| Jahr | Tage | Netto % |
|---|---|---|
| 2015 | 260 | -5.05 |
| 2016 | 260 | +2.93 |
| 2017 | 260 | -25.36 |
| 2018 | 261 | -23.84 |
| 2019 | 260 | -30.91 |
| 2020 | 261 | -6.01 |
| 2021 | 260 | -56.17 |
| 2022 | 260 | -1.50 |
| 2023 | 260 | -17.27 |

| Anlageklasse | Trades | Netto % p. a. |
|---|---|---|
| FX | 5192 | -3.60 |
| Metalle | 1445 | -3.86 |
| Indizes | 4733 | -9.84 |
| Öl | 718 | -0.83 |

| Instrument | Trades | Netto % p. a. | Ø R netto |
|---|---|---|---|
| EURUSD | 781 | -1.22 | -0.056 |
| GBPUSD | 769 | +0.67 | +0.031 |
| USDJPY | 696 | -0.49 | -0.026 |
| AUDUSD | 727 | +0.06 | +0.003 |
| NZDUSD | 727 | -2.07 | -0.103 |
| USDCAD | 760 | +0.40 | +0.019 |
| USDCHF | 732 | -0.94 | -0.046 |
| XAUUSD | 720 | -0.82 | -0.041 |
| US500 | 775 | -2.69 | -0.125 |
| US100 | 729 | -1.52 | -0.075 |
| FRA40 | 499 | -1.33 | -0.096 |
| UK100 | 669 | -1.53 | -0.082 |
| JP225 | 742 | -0.44 | -0.021 |
| HK50 | 576 | -0.82 | -0.051 |
| AUS200 | 743 | -1.51 | -0.073 |
| Brent | 718 | -0.83 | -0.042 |
| Silber | 725 | -3.04 | -0.151 |

## SR-TLINE

| Kennzahl | Wert |
|---|---|
| Handelstage / Trades | 2,342 / 7,638 |
| Netto je Tag (bp des Kapitals, Portfolio) | -3.48 bp (σ 59.9 bp) |
| vor Kosten je Tag | +0.09 bp |
| Handelskosten + Swap-Belastung je Tag (Swap netto) | 3.74 bp (-1.24 bp) |
| Rendite p. a. (netto, 0,25 % Risiko je Trade) | -9.05 % |
| Sharpe Ratio p. a. (netto) | -0.94 |
| t-Wert iid / Woche / Monat | -2.81 / -2.78 / -2.48 |
| Ø R je Trade vor / nach Kosten | +0.001 / -0.043 |
| Trefferquote / Anteil Long | 39% / 48% |
| Ausstiege Ziel / Stop / Zeit | 19% / 51% / 30% |
| Ø Haltedauer | 16.4 H4-Kerzen |
| bei doppelten Kosten | -7.22 bp/Tag |

| Kriterium | Ergebnis | erfüllt |
|---|---|---|
| Mittleres Netto-Tagesergebnis > 0 mit t ≥ 3,0 (kleinster aus iid / Woche / Monat) | -3.48 bp/Tag, t = -2.81 | **nein** |
| ≥ 6 von 9 Jahren positiv | 2 von 9 | **nein** |
| ≥ 60 % der Instrumente positiv | 2 von 17 | **nein** |
| bei doppelten Kosten > 0 | -7.22 bp/Tag | **nein** |

**SR-TLINE: nicht bestanden.**

| Jahr | Tage | Netto % |
|---|---|---|
| 2015 | 260 | +5.78 |
| 2016 | 260 | -1.99 |
| 2017 | 260 | -10.66 |
| 2018 | 261 | -14.46 |
| 2019 | 260 | -2.55 |
| 2020 | 261 | +2.85 |
| 2021 | 260 | -26.48 |
| 2022 | 260 | -21.35 |
| 2023 | 260 | -12.53 |

| Anlageklasse | Trades | Netto % p. a. |
|---|---|---|
| FX | 3292 | -2.28 |
| Metalle | 951 | -1.59 |
| Indizes | 2927 | -4.48 |
| Öl | 468 | -0.69 |

| Instrument | Trades | Netto % p. a. | Ø R netto |
|---|---|---|---|
| EURUSD | 475 | -0.54 | -0.041 |
| GBPUSD | 478 | -0.13 | -0.009 |
| USDJPY | 454 | +1.73 | +0.137 |
| AUDUSD | 470 | -0.39 | -0.030 |
| NZDUSD | 469 | -1.16 | -0.089 |
| USDCAD | 473 | -0.70 | -0.053 |
| USDCHF | 473 | -1.09 | -0.083 |
| XAUUSD | 479 | -0.43 | -0.033 |
| US500 | 472 | -0.59 | -0.045 |
| US100 | 486 | -1.96 | -0.145 |
| FRA40 | 322 | -0.92 | -0.103 |
| UK100 | 397 | -0.32 | -0.029 |
| JP225 | 446 | +0.60 | +0.048 |
| HK50 | 360 | -1.12 | -0.112 |
| AUS200 | 444 | -0.17 | -0.014 |
| Brent | 468 | -0.69 | -0.053 |
| Silber | 472 | -1.16 | -0.088 |

**Ergebnis: Keine Variante erfüllt alle In-Sample-Kriterien. Strategien Nr. 50 und 51 sind gescheitert; der Hold-out bleibt unberührt.**
