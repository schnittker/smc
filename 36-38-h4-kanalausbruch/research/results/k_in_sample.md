# Modell K (H4-Kanal-Ausbruch), In-Sample 2015–2023 (Trial T123 K-BBSQ, T124 K-KELT)

Lauf vom 24.10.2026. Regeln laut `docs/01_Vorregistrierung.md`, Code `research/hkb/`. 17 Instrumente, H4-Serverkerzen; Einstieg zur nächsten Eröffnung, Stop 2 ATR14, Ausstieg an der Mittellinie; 0,25 % Risiko je Trade. Netto = nach Spread, Slippage, Kommission und Swaps; Ergebnis eines Trades am Tag des Ausstiegs; Portfolio = Summe aller Instrumente je Tag.

## K-BBSQ

| Kennzahl | Wert |
|---|---|
| Handelstage / Trades | 2,342 / 1,535 |
| Netto je Tag (bp des Kapitals, Portfolio) | -0.25 bp (σ 30.4 bp) |
| vor Kosten je Tag | +0.51 bp |
| Handelskosten + Swap-Belastung je Tag (Swap netto) | 0.81 bp (-0.26 bp) |
| Rendite p. a. (netto, 0,25 % Risiko je Trade) | -0.64 % |
| Sharpe Ratio p. a. (netto) | -0.13 |
| t-Wert iid / Woche / Monat | -0.39 / -0.34 / -0.34 |
| Ø R je Trade vor / nach Kosten | +0.031 / -0.015 |
| Trefferquote / Anteil Stops / Anteil Long | 32% / 23% / 53% |
| Ø Haltedauer | 13.7 H4-Kerzen |
| bei doppelten Kosten | -1.05 bp/Tag |

| Kriterium | Ergebnis | erfüllt |
|---|---|---|
| Mittleres Netto-Tagesergebnis > 0 mit t ≥ 3,0 (kleinster aus iid / Woche / Monat) | -0.25 bp/Tag, t = -0.39 | **nein** |
| ≥ 6 von 9 Jahren positiv | 4 von 9 | **nein** |
| ≥ 60 % der Instrumente positiv | 7 von 17 | **nein** |
| bei doppelten Kosten > 0 | -1.05 bp/Tag | **nein** |

**K-BBSQ: nicht bestanden.**

| Jahr | Tage | Netto % |
|---|---|---|
| 2015 | 260 | -1.91 |
| 2016 | 260 | +7.47 |
| 2017 | 260 | -6.95 |
| 2018 | 261 | +5.36 |
| 2019 | 260 | -6.38 |
| 2020 | 261 | +2.92 |
| 2021 | 260 | -0.03 |
| 2022 | 260 | -8.23 |
| 2023 | 260 | +1.96 |

| Anlageklasse | Trades | Netto % p. a. |
|---|---|---|
| FX | 685 | +0.26 |
| Metalle | 163 | +0.68 |
| Indizes | 604 | -1.80 |
| Öl | 83 | +0.22 |

| Instrument | Trades | Netto % p. a. | Ø R netto |
|---|---|---|---|
| EURUSD | 99 | +0.09 | +0.034 |
| GBPUSD | 95 | -0.48 | -0.183 |
| USDJPY | 102 | +0.74 | +0.262 |
| AUDUSD | 85 | +0.04 | +0.018 |
| NZDUSD | 105 | -0.00 | -0.001 |
| USDCAD | 97 | -0.09 | -0.035 |
| USDCHF | 102 | -0.04 | -0.013 |
| XAUUSD | 85 | +0.59 | +0.249 |
| US500 | 99 | -0.26 | -0.093 |
| US100 | 93 | -0.50 | -0.195 |
| FRA40 | 75 | -0.01 | -0.003 |
| UK100 | 83 | -0.63 | -0.272 |
| JP225 | 93 | +0.34 | +0.131 |
| HK50 | 71 | -0.34 | -0.174 |
| AUS200 | 90 | -0.40 | -0.161 |
| Brent | 83 | +0.22 | +0.097 |
| Silber | 78 | +0.09 | +0.040 |

## K-KELT

| Kennzahl | Wert |
|---|---|
| Handelstage / Trades | 2,342 / 4,950 |
| Netto je Tag (bp des Kapitals, Portfolio) | -0.76 bp (σ 73.1 bp) |
| vor Kosten je Tag | +1.60 bp |
| Handelskosten + Swap-Belastung je Tag (Swap netto) | 2.53 bp (-0.93 bp) |
| Rendite p. a. (netto, 0,25 % Risiko je Trade) | -1.99 % |
| Sharpe Ratio p. a. (netto) | -0.17 |
| t-Wert iid / Woche / Monat | -0.51 / -0.43 / -0.39 |
| Ø R je Trade vor / nach Kosten | +0.030 / -0.014 |
| Trefferquote / Anteil Stops / Anteil Long | 34% / 33% / 52% |
| Ø Haltedauer | 16.8 H4-Kerzen |
| bei doppelten Kosten | -3.29 bp/Tag |

| Kriterium | Ergebnis | erfüllt |
|---|---|---|
| Mittleres Netto-Tagesergebnis > 0 mit t ≥ 3,0 (kleinster aus iid / Woche / Monat) | -0.76 bp/Tag, t = -0.51 | **nein** |
| ≥ 6 von 9 Jahren positiv | 3 von 9 | **nein** |
| ≥ 60 % der Instrumente positiv | 7 von 17 | **nein** |
| bei doppelten Kosten > 0 | -3.29 bp/Tag | **nein** |

**K-KELT: nicht bestanden.**

| Jahr | Tage | Netto % |
|---|---|---|
| 2015 | 260 | -1.59 |
| 2016 | 260 | +1.73 |
| 2017 | 260 | -9.56 |
| 2018 | 261 | +5.58 |
| 2019 | 260 | -6.05 |
| 2020 | 261 | +21.52 |
| 2021 | 260 | -15.39 |
| 2022 | 260 | -2.88 |
| 2023 | 260 | -11.28 |

| Anlageklasse | Trades | Netto % p. a. |
|---|---|---|
| FX | 2095 | -1.79 |
| Metalle | 552 | +1.49 |
| Indizes | 1979 | -0.75 |
| Öl | 324 | -0.93 |

| Instrument | Trades | Netto % p. a. | Ø R netto |
|---|---|---|---|
| EURUSD | 317 | -0.43 | -0.048 |
| GBPUSD | 306 | -0.22 | -0.025 |
| USDJPY | 300 | +0.39 | +0.047 |
| AUDUSD | 296 | -0.65 | -0.078 |
| NZDUSD | 300 | -0.95 | -0.114 |
| USDCAD | 291 | +0.06 | +0.007 |
| USDCHF | 285 | -0.00 | -0.000 |
| XAUUSD | 297 | +0.82 | +0.099 |
| US500 | 327 | -0.41 | -0.046 |
| US100 | 337 | +0.05 | +0.005 |
| FRA40 | 215 | -0.31 | -0.051 |
| UK100 | 248 | -0.17 | -0.025 |
| JP225 | 313 | +0.18 | +0.021 |
| HK50 | 242 | +0.92 | +0.137 |
| AUS200 | 297 | -1.01 | -0.122 |
| Brent | 324 | -0.93 | -0.104 |
| Silber | 255 | +0.67 | +0.095 |

**Ergebnis: Keine Variante erfüllt alle In-Sample-Kriterien. Strategien Nr. 36 und 38 sind gescheitert; der Hold-out bleibt unberührt.**
