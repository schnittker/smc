# Modell ML (Machine Learning), In-Sample 2015–2023 (Trial T288–T290)

Lauf vom 24.10.2026. Regeln laut `docs/01_Vorregistrierung.md`, Code `research/mlx/`. 17 Instrumente; Modelle jährlich walk-forward trainiert; ML-GBM/ML-MLP: H1, 6 Kerzen bei p > 0,55 bzw. < 0,45, Stop 2 ATR; ML-META: Supertrend H4 mit Meta-Filter p > 0,55; 0,25 % Risiko je Trade. Netto = nach Spread, Slippage, Kommission und Swaps; Ergebnis eines Trades am Tag des Ausstiegs; Portfolio = Summe aller Instrumente je Tag.

## ML-GBM (Nr. 83, H1)

| Kennzahl | Wert |
|---|---|
| Handelstage / Trades | 2,342 / 29,512 |
| Netto je Tag (bp des Kapitals, Portfolio) | -9.10 bp (σ 97.6 bp) |
| vor Kosten je Tag | +9.31 bp |
| Handelskosten + Swap-Belastung je Tag (Swap netto) | 18.59 bp (-1.05 bp) |
| Rendite p. a. (netto, 0,25 % Risiko je Trade) | -23.67 % |
| Sharpe Ratio p. a. (netto) | -1.50 |
| t-Wert iid / Woche / Monat | -4.51 / -4.64 / -4.33 |
| Ø R je Trade vor / nach Kosten | +0.030 / -0.029 |
| Trefferquote / Anteil Notfall-Stops / Anteil Long | 48% / 21% / 58% |
| Ø Haltedauer | 5.5 Kerzen (H1) |
| bei doppelten Kosten | -27.69 bp/Tag |

| Kriterium | Ergebnis | erfüllt |
|---|---|---|
| Mittleres Netto-Tagesergebnis > 0 mit t ≥ 3,0 (kleinster aus iid / Woche / Monat) | -9.10 bp/Tag, t = -4.64 | **nein** |
| ≥ 6 von 9 Jahren positiv | 1 von 9 | **nein** |
| ≥ 60 % der Instrumente positiv | 4 von 17 | **nein** |
| bei doppelten Kosten > 0 | -27.69 bp/Tag | **nein** |

**ML-GBM: nicht bestanden.**

| Jahr | Tage | Netto % |
|---|---|---|
| 2015 | 260 | -45.18 |
| 2016 | 260 | -12.92 |
| 2017 | 260 | -48.62 |
| 2018 | 261 | -80.08 |
| 2019 | 260 | -9.57 |
| 2020 | 261 | -15.16 |
| 2021 | 260 | +13.33 |
| 2022 | 260 | -10.42 |
| 2023 | 260 | -4.40 |

| Anlageklasse | Trades | Netto % p. a. |
|---|---|---|
| FX | 13161 | +0.48 |
| Metalle | 3656 | -9.62 |
| Indizes | 10145 | -8.48 |
| Öl | 2550 | -6.04 |

| Instrument | Trades | Netto % p. a. | Ø R netto |
|---|---|---|---|
| EURUSD | 1828 | -0.10 | -0.002 |
| GBPUSD | 1832 | +0.69 | +0.013 |
| USDJPY | 1885 | +1.30 | +0.025 |
| AUDUSD | 1914 | -0.31 | -0.006 |
| NZDUSD | 1929 | -1.34 | -0.025 |
| USDCAD | 1928 | -1.25 | -0.023 |
| USDCHF | 1845 | +1.49 | +0.029 |
| XAUUSD | 1837 | -1.65 | -0.032 |
| US500 | 1718 | -0.40 | -0.008 |
| US100 | 1811 | -1.18 | -0.023 |
| FRA40 | 1036 | -1.54 | -0.053 |
| UK100 | 1215 | -1.75 | -0.052 |
| JP225 | 1767 | -2.01 | -0.041 |
| HK50 | 1011 | +0.40 | +0.014 |
| AUS200 | 1587 | -2.00 | -0.045 |
| Brent | 2550 | -6.04 | -0.085 |
| Silber | 1819 | -7.97 | -0.158 |

## ML-META (Nr. 84, H4)

| Kennzahl | Wert |
|---|---|
| Handelstage / Trades | 2,342 / 344 |
| Netto je Tag (bp des Kapitals, Portfolio) | -0.24 bp (σ 11.7 bp) |
| vor Kosten je Tag | -0.10 bp |
| Handelskosten + Swap-Belastung je Tag (Swap netto) | 0.14 bp (-0.08 bp) |
| Rendite p. a. (netto, 0,25 % Risiko je Trade) | -0.62 % |
| Sharpe Ratio p. a. (netto) | -0.33 |
| t-Wert iid / Woche / Monat | -0.99 / -0.92 / -0.96 |
| Ø R je Trade vor / nach Kosten | -0.028 / -0.065 |
| Trefferquote / Anteil Notfall-Stops / Anteil Long | 33% / 28% / 56% |
| Ø Haltedauer | 34.6 Kerzen (H4) |
| bei doppelten Kosten | -0.38 bp/Tag |

| Kriterium | Ergebnis | erfüllt |
|---|---|---|
| Mittleres Netto-Tagesergebnis > 0 mit t ≥ 3,0 (kleinster aus iid / Woche / Monat) | -0.24 bp/Tag, t = -0.99 | **nein** |
| ≥ 6 von 9 Jahren positiv | 3 von 9 | **nein** |
| ≥ 60 % der Instrumente positiv | 5 von 17 | **nein** |
| bei doppelten Kosten > 0 | -0.38 bp/Tag | **nein** |

**ML-META: nicht bestanden.**

| Jahr | Tage | Netto % |
|---|---|---|
| 2015 | 260 | -1.91 |
| 2016 | 260 | -1.99 |
| 2017 | 260 | -3.03 |
| 2018 | 261 | -1.28 |
| 2019 | 260 | +0.73 |
| 2020 | 261 | +1.99 |
| 2021 | 260 | -0.36 |
| 2022 | 260 | -0.93 |
| 2023 | 260 | +1.20 |

| Anlageklasse | Trades | Netto % p. a. |
|---|---|---|
| FX | 120 | +0.04 |
| Metalle | 38 | -0.01 |
| Indizes | 169 | -0.75 |
| Öl | 17 | +0.10 |

| Instrument | Trades | Netto % p. a. | Ø R netto |
|---|---|---|---|
| EURUSD | 13 | +0.04 | +0.117 |
| GBPUSD | 25 | +0.13 | +0.183 |
| USDJPY | 25 | -0.00 | -0.003 |
| AUDUSD | 13 | +0.10 | +0.277 |
| NZDUSD | 16 | -0.24 | -0.550 |
| USDCAD | 19 | +0.07 | +0.133 |
| USDCHF | 9 | -0.05 | -0.206 |
| XAUUSD | 22 | -0.00 | -0.004 |
| US500 | 38 | -0.07 | -0.070 |
| US100 | 29 | -0.09 | -0.111 |
| FRA40 | 12 | -0.07 | -0.221 |
| UK100 | 17 | -0.09 | -0.187 |
| JP225 | 23 | -0.13 | -0.202 |
| HK50 | 19 | -0.09 | -0.168 |
| AUS200 | 31 | -0.20 | -0.235 |
| Brent | 17 | +0.10 | +0.203 |
| Silber | 16 | -0.01 | -0.021 |

## ML-MLP (Nr. 86, H1)

| Kennzahl | Wert |
|---|---|
| Handelstage / Trades | 2,342 / 67,350 |
| Netto je Tag (bp des Kapitals, Portfolio) | -39.74 bp (σ 143.8 bp) |
| vor Kosten je Tag | +0.96 bp |
| Handelskosten + Swap-Belastung je Tag (Swap netto) | 41.00 bp (-2.04 bp) |
| Rendite p. a. (netto, 0,25 % Risiko je Trade) | -103.41 % |
| Sharpe Ratio p. a. (netto) | -4.46 |
| t-Wert iid / Woche / Monat | -13.37 / -12.90 / -11.56 |
| Ø R je Trade vor / nach Kosten | +0.001 / -0.055 |
| Trefferquote / Anteil Notfall-Stops / Anteil Long | 45% / 23% / 63% |
| Ø Haltedauer | 5.4 Kerzen (H1) |
| bei doppelten Kosten | -80.74 bp/Tag |

| Kriterium | Ergebnis | erfüllt |
|---|---|---|
| Mittleres Netto-Tagesergebnis > 0 mit t ≥ 3,0 (kleinster aus iid / Woche / Monat) | -39.74 bp/Tag, t = -13.37 | **nein** |
| ≥ 6 von 9 Jahren positiv | 0 von 9 | **nein** |
| ≥ 60 % der Instrumente positiv | 0 von 17 | **nein** |
| bei doppelten Kosten > 0 | -80.74 bp/Tag | **nein** |

**ML-MLP: nicht bestanden.**

| Jahr | Tage | Netto % |
|---|---|---|
| 2015 | 260 | -160.40 |
| 2016 | 260 | -111.11 |
| 2017 | 260 | -176.01 |
| 2018 | 261 | -115.04 |
| 2019 | 260 | -62.87 |
| 2020 | 261 | -102.44 |
| 2021 | 260 | -56.71 |
| 2022 | 260 | -103.68 |
| 2023 | 260 | -42.44 |

| Anlageklasse | Trades | Netto % p. a. |
|---|---|---|
| FX | 30691 | -34.43 |
| Metalle | 8385 | -27.50 |
| Indizes | 24278 | -28.89 |
| Öl | 3996 | -12.59 |

| Instrument | Trades | Netto % p. a. | Ø R netto |
|---|---|---|---|
| EURUSD | 4361 | -4.05 | -0.033 |
| GBPUSD | 4449 | -4.48 | -0.036 |
| USDJPY | 4239 | -5.50 | -0.047 |
| AUDUSD | 4424 | -5.30 | -0.043 |
| NZDUSD | 4471 | -7.29 | -0.059 |
| USDCAD | 4348 | -4.63 | -0.038 |
| USDCHF | 4399 | -3.19 | -0.026 |
| XAUUSD | 4135 | -5.75 | -0.050 |
| US500 | 4028 | -3.36 | -0.030 |
| US100 | 4042 | -2.31 | -0.021 |
| FRA40 | 2474 | -4.30 | -0.063 |
| UK100 | 3096 | -2.78 | -0.032 |
| JP225 | 4088 | -5.25 | -0.046 |
| HK50 | 2597 | -5.01 | -0.069 |
| AUS200 | 3953 | -5.87 | -0.053 |
| Brent | 3996 | -12.59 | -0.113 |
| Silber | 4250 | -21.75 | -0.184 |

## Übersicht

| Variante | Nr. | TF | Trades | Netto bp/Tag | vor Kosten bp/Tag | Ø R vor / nach Kosten | t | Jahre + | Instr. + |
|---|---|---|---|---|---|---|---|---|---|
| ML-GBM | 83 | H1 | 29,512 | -9.10 | +9.31 | +0.030 / -0.029 | -4.64 | 1 | 4 |
| ML-META | 84 | H4 | 344 | -0.24 | -0.10 | -0.028 / -0.065 | -0.99 | 3 | 5 |
| ML-MLP | 86 | H1 | 67,350 | -39.74 | +0.96 | +0.001 / -0.055 | -13.37 | 0 | 0 |

## Beschreibend: Prognosegüte out-of-sample (gepoolt)

| Modell | Jahr | AUC | Trefferquote (p > 0,5) |
|---|---|---|---|
| ML-GBM | 2015 | 0.516 | 51.0% |
| ML-GBM | 2016 | 0.519 | 51.6% |
| ML-GBM | 2017 | 0.515 | 51.4% |
| ML-GBM | 2018 | 0.517 | 51.4% |
| ML-GBM | 2019 | 0.525 | 52.3% |
| ML-GBM | 2020 | 0.514 | 51.9% |
| ML-GBM | 2021 | 0.524 | 51.8% |
| ML-GBM | 2022 | 0.515 | 51.0% |
| ML-GBM | 2023 | 0.516 | 51.3% |
| ML-MLP | 2015 | 0.502 | 50.0% |
| ML-MLP | 2016 | 0.505 | 50.3% |
| ML-MLP | 2017 | 0.508 | 50.3% |
| ML-MLP | 2018 | 0.506 | 50.4% |
| ML-MLP | 2019 | 0.504 | 50.8% |
| ML-MLP | 2020 | 0.501 | 50.1% |
| ML-MLP | 2021 | 0.508 | 51.3% |
| ML-MLP | 2022 | 0.504 | 50.4% |
| ML-MLP | 2023 | 0.501 | 50.2% |

**Ergebnis: Keine Variante erfüllt alle In-Sample-Kriterien. Strategien Nr. 83, 84 und 86 sind gescheitert; der Hold-out bleibt unberührt.**
