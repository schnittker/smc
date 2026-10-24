# Modell FC (Fibonacci-Pullback, Chandelier-Trend), In-Sample 2015–2023 (Trial T183 FC-FIB, T184 FC-CHAND)

Lauf vom 24.10.2026. Regeln laut `docs/01_Vorregistrierung.md`, Code `research/fch/`. 17 Instrumente. FC-FIB: H4, Einstieg im 50–61,8-%-Rücklauf eines Impulses ≥ 3 ATR, Stop unter dem Ursprung, Ziel Impulsextrem, Zeitstopp 30 Kerzen. FC-CHAND: D1, 55-Tage-Ausbruch, Chandelier-Stop HH − 3 ATR22. 0,25 % Risiko je Trade. Netto = nach Spread, Slippage, Kommission und Swaps; Ergebnis eines Trades am Tag des Ausstiegs; Portfolio = Summe aller Instrumente je Tag.

## FC-FIB

| Kennzahl | Wert |
|---|---|
| Handelstage / Trades | 2,342 / 3,490 |
| Netto je Tag (bp des Kapitals, Portfolio) | -1.76 bp (σ 33.2 bp) |
| vor Kosten je Tag | -0.40 bp |
| Handelskosten + Swap-Belastung je Tag (Swap netto) | 1.41 bp (-0.42 bp) |
| Rendite p. a. (netto, 0,25 % Risiko je Trade) | -4.58 % |
| Sharpe Ratio p. a. (netto) | -0.85 |
| t-Wert iid / Woche / Monat | -2.56 / -2.47 / -2.69 |
| Ø R je Trade vor / nach Kosten | -0.011 / -0.047 |
| Trefferquote / Anteil Long | 47% / 46% |
| Ausstiege Ziel / Stop / Zeit | 42% / 48% / 10% |
| Ø Haltedauer | 11.7 Kerzen (FC-FIB: H4, FC-CHAND: D1) |
| bei doppelten Kosten | -3.17 bp/Tag |

| Kriterium | Ergebnis | erfüllt |
|---|---|---|
| Mittleres Netto-Tagesergebnis > 0 mit t ≥ 3,0 (kleinster aus iid / Woche / Monat) | -1.76 bp/Tag, t = -2.69 | **nein** |
| ≥ 6 von 9 Jahren positiv | 2 von 9 | **nein** |
| ≥ 60 % der Instrumente positiv | 7 von 17 | **nein** |
| bei doppelten Kosten > 0 | -3.17 bp/Tag | **nein** |

**FC-FIB: nicht bestanden.**

| Jahr | Tage | Netto % |
|---|---|---|
| 2015 | 260 | -7.75 |
| 2016 | 260 | -1.79 |
| 2017 | 260 | +3.23 |
| 2018 | 261 | -13.91 |
| 2019 | 260 | -11.71 |
| 2020 | 261 | -6.54 |
| 2021 | 260 | -4.14 |
| 2022 | 260 | -1.41 |
| 2023 | 260 | +2.84 |

| Anlageklasse | Trades | Netto % p. a. |
|---|---|---|
| FX | 1448 | -2.63 |
| Metalle | 399 | -0.82 |
| Indizes | 1405 | -1.17 |
| Öl | 238 | +0.04 |

| Instrument | Trades | Netto % p. a. | Ø R netto |
|---|---|---|---|
| EURUSD | 211 | -0.11 | -0.019 |
| GBPUSD | 214 | -0.45 | -0.076 |
| USDJPY | 202 | -0.57 | -0.102 |
| AUDUSD | 212 | -0.65 | -0.111 |
| NZDUSD | 222 | +0.17 | +0.027 |
| USDCAD | 195 | -0.58 | -0.108 |
| USDCHF | 192 | -0.42 | -0.079 |
| XAUUSD | 212 | +0.46 | +0.078 |
| US500 | 238 | +0.10 | +0.016 |
| US100 | 219 | -0.17 | -0.028 |
| FRA40 | 138 | +0.02 | +0.005 |
| UK100 | 188 | +0.29 | +0.055 |
| JP225 | 232 | +0.11 | +0.017 |
| HK50 | 166 | -0.30 | -0.065 |
| AUS200 | 224 | -1.23 | -0.197 |
| Brent | 238 | +0.04 | +0.006 |
| Silber | 187 | -1.28 | -0.247 |

## FC-CHAND

| Kennzahl | Wert |
|---|---|
| Handelstage / Trades | 2,342 / 938 |
| Netto je Tag (bp des Kapitals, Portfolio) | -0.14 bp (σ 17.8 bp) |
| vor Kosten je Tag | +0.20 bp |
| Handelskosten + Swap-Belastung je Tag (Swap netto) | 0.40 bp (-0.27 bp) |
| Rendite p. a. (netto, 0,25 % Risiko je Trade) | -0.37 % |
| Sharpe Ratio p. a. (netto) | -0.13 |
| t-Wert iid / Woche / Monat | -0.38 / -0.36 / -0.28 |
| Ø R je Trade vor / nach Kosten | +0.020 / -0.014 |
| Trefferquote / Anteil Long | 36% / 51% |
| Ausstiege Ziel / Stop / Zeit | 0% / 99% / 0% |
| Ø Haltedauer | 19.5 Kerzen (FC-FIB: H4, FC-CHAND: D1) |
| bei doppelten Kosten | -0.54 bp/Tag |

| Kriterium | Ergebnis | erfüllt |
|---|---|---|
| Mittleres Netto-Tagesergebnis > 0 mit t ≥ 3,0 (kleinster aus iid / Woche / Monat) | -0.14 bp/Tag, t = -0.38 | **nein** |
| ≥ 6 von 9 Jahren positiv | 2 von 9 | **nein** |
| ≥ 60 % der Instrumente positiv | 6 von 17 | **nein** |
| bei doppelten Kosten > 0 | -0.54 bp/Tag | **nein** |

**FC-CHAND: nicht bestanden.**

| Jahr | Tage | Netto % |
|---|---|---|
| 2015 | 260 | -3.01 |
| 2016 | 260 | -4.54 |
| 2017 | 260 | +2.27 |
| 2018 | 261 | -0.09 |
| 2019 | 260 | -2.54 |
| 2020 | 261 | +8.73 |
| 2021 | 260 | -1.82 |
| 2022 | 260 | -1.91 |
| 2023 | 260 | -0.41 |

| Anlageklasse | Trades | Netto % p. a. |
|---|---|---|
| FX | 375 | -0.19 |
| Metalle | 111 | +0.13 |
| Indizes | 402 | -0.72 |
| Öl | 50 | +0.42 |

| Instrument | Trades | Netto % p. a. | Ø R netto |
|---|---|---|---|
| EURUSD | 55 | -0.12 | -0.080 |
| GBPUSD | 54 | -0.07 | -0.049 |
| USDJPY | 50 | +0.31 | +0.222 |
| AUDUSD | 52 | -0.01 | -0.004 |
| NZDUSD | 59 | -0.15 | -0.091 |
| USDCAD | 52 | +0.05 | +0.035 |
| USDCHF | 53 | -0.20 | -0.137 |
| XAUUSD | 53 | +0.24 | +0.161 |
| US500 | 60 | +0.01 | +0.005 |
| US100 | 61 | -0.04 | -0.026 |
| FRA40 | 58 | -0.16 | -0.097 |
| UK100 | 54 | -0.30 | -0.200 |
| JP225 | 62 | -0.21 | -0.123 |
| HK50 | 48 | +0.30 | +0.224 |
| AUS200 | 59 | -0.32 | -0.194 |
| Brent | 50 | +0.42 | +0.304 |
| Silber | 58 | -0.11 | -0.069 |

**Ergebnis: Keine Variante erfüllt alle In-Sample-Kriterien. Strategien Nr. 52 und 53 sind gescheitert; der Hold-out bleibt unberührt.**
