# Modell PA (Price Action), In-Sample 2015–2023 (Trial T189 PA-PIN, T190 PA-ENG, T191 PA-DT, T192 PA-SD)

Lauf vom 24.10.2026. Regeln laut `docs/01_Vorregistrierung.md`, Code `research/pa/`. 17 Instrumente, H4-Serverkerzen; Einstieg zur nächsten Eröffnung, Stop hinter dem Muster (≥ 1 ATR), Ziel 2R bzw. Measured Move (PA-DT), Zeitstopp 30 Kerzen; 0,25 % Risiko je Trade. Netto = nach Spread, Slippage, Kommission und Swaps; Ergebnis eines Trades am Tag des Ausstiegs; Portfolio = Summe aller Instrumente je Tag.

## PA-PIN

| Kennzahl | Wert |
|---|---|
| Handelstage / Trades | 2,342 / 1,825 |
| Netto je Tag (bp des Kapitals, Portfolio) | -0.45 bp (σ 32.4 bp) |
| vor Kosten je Tag | +0.56 bp |
| Handelskosten + Swap-Belastung je Tag (Swap netto) | 1.06 bp (-0.23 bp) |
| Rendite p. a. (netto, 0,25 % Risiko je Trade) | -1.18 % |
| Sharpe Ratio p. a. (netto) | -0.23 |
| t-Wert iid / Woche / Monat | -0.68 / -0.64 / -0.68 |
| Ø R je Trade vor / nach Kosten | +0.029 / -0.023 |
| Trefferquote / Anteil Long | 35% / 57% |
| Ausstiege Ziel / Stop / Zeit | 30% / 63% / 7% |
| Ø Haltedauer | 9.6 H4-Kerzen |
| bei doppelten Kosten | -1.52 bp/Tag |

| Kriterium | Ergebnis | erfüllt |
|---|---|---|
| Mittleres Netto-Tagesergebnis > 0 mit t ≥ 3,0 (kleinster aus iid / Woche / Monat) | -0.45 bp/Tag, t = -0.68 | **nein** |
| ≥ 6 von 9 Jahren positiv | 5 von 9 | **nein** |
| ≥ 60 % der Instrumente positiv | 6 von 17 | **nein** |
| bei doppelten Kosten > 0 | -1.52 bp/Tag | **nein** |

**PA-PIN: nicht bestanden.**

| Jahr | Tage | Netto % |
|---|---|---|
| 2015 | 260 | +1.66 |
| 2016 | 260 | +2.85 |
| 2017 | 260 | -7.20 |
| 2018 | 261 | -3.05 |
| 2019 | 260 | +0.44 |
| 2020 | 261 | +8.35 |
| 2021 | 260 | -6.48 |
| 2022 | 260 | +1.67 |
| 2023 | 260 | -8.84 |

| Anlageklasse | Trades | Netto % p. a. |
|---|---|---|
| FX | 797 | -0.30 |
| Metalle | 216 | -0.10 |
| Indizes | 689 | -0.39 |
| Öl | 123 | -0.39 |

| Instrument | Trades | Netto % p. a. | Ø R netto |
|---|---|---|---|
| EURUSD | 127 | +0.20 | +0.056 |
| GBPUSD | 130 | +0.77 | +0.214 |
| USDJPY | 95 | -0.48 | -0.183 |
| AUDUSD | 112 | +0.46 | +0.149 |
| NZDUSD | 90 | -0.20 | -0.080 |
| USDCAD | 110 | -0.50 | -0.164 |
| USDCHF | 133 | -0.55 | -0.149 |
| XAUUSD | 96 | +0.20 | +0.074 |
| US500 | 110 | +0.50 | +0.163 |
| US100 | 99 | -0.07 | -0.025 |
| FRA40 | 74 | -0.00 | -0.002 |
| UK100 | 109 | -0.40 | -0.132 |
| JP225 | 102 | -0.48 | -0.168 |
| HK50 | 73 | -0.40 | -0.199 |
| AUS200 | 122 | +0.47 | +0.137 |
| Brent | 123 | -0.39 | -0.114 |
| Silber | 120 | -0.30 | -0.089 |

## PA-ENG

| Kennzahl | Wert |
|---|---|
| Handelstage / Trades | 2,342 / 6,276 |
| Netto je Tag (bp des Kapitals, Portfolio) | -5.80 bp (σ 60.4 bp) |
| vor Kosten je Tag | -2.36 bp |
| Handelskosten + Swap-Belastung je Tag (Swap netto) | 3.58 bp (-0.79 bp) |
| Rendite p. a. (netto, 0,25 % Risiko je Trade) | -15.09 % |
| Sharpe Ratio p. a. (netto) | -1.55 |
| t-Wert iid / Woche / Monat | -4.64 / -4.46 / -4.37 |
| Ø R je Trade vor / nach Kosten | -0.035 / -0.087 |
| Trefferquote / Anteil Long | 33% / 50% |
| Ausstiege Ziel / Stop / Zeit | 26% / 64% / 10% |
| Ø Haltedauer | 10.4 H4-Kerzen |
| bei doppelten Kosten | -9.38 bp/Tag |

| Kriterium | Ergebnis | erfüllt |
|---|---|---|
| Mittleres Netto-Tagesergebnis > 0 mit t ≥ 3,0 (kleinster aus iid / Woche / Monat) | -5.80 bp/Tag, t = -4.64 | **nein** |
| ≥ 6 von 9 Jahren positiv | 0 von 9 | **nein** |
| ≥ 60 % der Instrumente positiv | 3 von 17 | **nein** |
| bei doppelten Kosten > 0 | -9.38 bp/Tag | **nein** |

**PA-ENG: nicht bestanden.**

| Jahr | Tage | Netto % |
|---|---|---|
| 2015 | 260 | -15.00 |
| 2016 | 260 | -23.72 |
| 2017 | 260 | -14.33 |
| 2018 | 261 | -12.53 |
| 2019 | 260 | -9.08 |
| 2020 | 261 | -17.45 |
| 2021 | 260 | -21.27 |
| 2022 | 260 | -11.34 |
| 2023 | 260 | -11.05 |

| Anlageklasse | Trades | Netto % p. a. |
|---|---|---|
| FX | 2889 | -6.52 |
| Metalle | 776 | -2.73 |
| Indizes | 2269 | -5.38 |
| Öl | 342 | -0.46 |

| Instrument | Trades | Netto % p. a. | Ø R netto |
|---|---|---|---|
| EURUSD | 416 | -0.82 | -0.071 |
| GBPUSD | 428 | +0.03 | +0.003 |
| USDJPY | 389 | -1.02 | -0.094 |
| AUDUSD | 427 | -1.43 | -0.121 |
| NZDUSD | 415 | -1.41 | -0.123 |
| USDCAD | 394 | +0.46 | +0.042 |
| USDCHF | 420 | -2.33 | -0.200 |
| XAUUSD | 380 | -0.24 | -0.023 |
| US500 | 376 | -2.76 | -0.265 |
| US100 | 357 | +0.66 | +0.067 |
| FRA40 | 234 | -0.11 | -0.016 |
| UK100 | 333 | -0.70 | -0.075 |
| JP225 | 362 | -0.13 | -0.013 |
| HK50 | 249 | -0.42 | -0.061 |
| AUS200 | 358 | -1.93 | -0.194 |
| Brent | 342 | -0.46 | -0.048 |
| Silber | 396 | -2.49 | -0.226 |

## PA-DT

| Kennzahl | Wert |
|---|---|
| Handelstage / Trades | 2,342 / 1,571 |
| Netto je Tag (bp des Kapitals, Portfolio) | -0.55 bp (σ 16.3 bp) |
| vor Kosten je Tag | -0.14 bp |
| Handelskosten + Swap-Belastung je Tag (Swap netto) | 0.44 bp (-0.16 bp) |
| Rendite p. a. (netto, 0,25 % Risiko je Trade) | -1.44 % |
| Sharpe Ratio p. a. (netto) | -0.55 |
| t-Wert iid / Woche / Monat | -1.64 / -1.65 / -1.73 |
| Ø R je Trade vor / nach Kosten | -0.009 / -0.033 |
| Trefferquote / Anteil Long | 56% / 49% |
| Ausstiege Ziel / Stop / Zeit | 50% / 31% / 19% |
| Ø Haltedauer | 15.5 H4-Kerzen |
| bei doppelten Kosten | -0.99 bp/Tag |

| Kriterium | Ergebnis | erfüllt |
|---|---|---|
| Mittleres Netto-Tagesergebnis > 0 mit t ≥ 3,0 (kleinster aus iid / Woche / Monat) | -0.55 bp/Tag, t = -1.73 | **nein** |
| ≥ 6 von 9 Jahren positiv | 3 von 9 | **nein** |
| ≥ 60 % der Instrumente positiv | 5 von 17 | **nein** |
| bei doppelten Kosten > 0 | -0.99 bp/Tag | **nein** |

**PA-DT: nicht bestanden.**

| Jahr | Tage | Netto % |
|---|---|---|
| 2015 | 260 | -4.33 |
| 2016 | 260 | -1.43 |
| 2017 | 260 | -3.13 |
| 2018 | 261 | -1.97 |
| 2019 | 260 | -1.27 |
| 2020 | 261 | +1.11 |
| 2021 | 260 | -4.57 |
| 2022 | 260 | +2.04 |
| 2023 | 260 | +0.58 |

| Anlageklasse | Trades | Netto % p. a. |
|---|---|---|
| FX | 659 | -0.53 |
| Metalle | 172 | -0.57 |
| Indizes | 634 | -0.26 |
| Öl | 106 | -0.08 |

| Instrument | Trades | Netto % p. a. | Ø R netto |
|---|---|---|---|
| EURUSD | 94 | -0.13 | -0.050 |
| GBPUSD | 86 | +0.03 | +0.014 |
| USDJPY | 82 | -0.03 | -0.013 |
| AUDUSD | 101 | -0.34 | -0.122 |
| NZDUSD | 86 | -0.11 | -0.047 |
| USDCAD | 121 | -0.17 | -0.051 |
| USDCHF | 89 | +0.22 | +0.091 |
| XAUUSD | 88 | -0.24 | -0.097 |
| US500 | 108 | +0.01 | +0.003 |
| US100 | 101 | -0.21 | -0.073 |
| FRA40 | 72 | -0.18 | -0.090 |
| UK100 | 92 | +0.04 | +0.016 |
| JP225 | 92 | -0.21 | -0.083 |
| HK50 | 73 | -0.02 | -0.011 |
| AUS200 | 96 | +0.31 | +0.117 |
| Brent | 106 | -0.08 | -0.027 |
| Silber | 84 | -0.34 | -0.144 |

## PA-SD

| Kennzahl | Wert |
|---|---|
| Handelstage / Trades | 2,342 / 473 |
| Netto je Tag (bp des Kapitals, Portfolio) | +0.15 bp (σ 16.9 bp) |
| vor Kosten je Tag | +0.46 bp |
| Handelskosten + Swap-Belastung je Tag (Swap netto) | 0.32 bp (-0.07 bp) |
| Rendite p. a. (netto, 0,25 % Risiko je Trade) | +0.40 % |
| Sharpe Ratio p. a. (netto) | 0.15 |
| t-Wert iid / Woche / Monat | 0.44 / 0.44 / 0.40 |
| Ø R je Trade vor / nach Kosten | +0.092 / +0.031 |
| Trefferquote / Anteil Long | 35% / 44% |
| Ausstiege Ziel / Stop / Zeit | 32% / 64% / 3% |
| Ø Haltedauer | 7.2 H4-Kerzen |
| bei doppelten Kosten | -0.16 bp/Tag |

| Kriterium | Ergebnis | erfüllt |
|---|---|---|
| Mittleres Netto-Tagesergebnis > 0 mit t ≥ 3,0 (kleinster aus iid / Woche / Monat) | +0.15 bp/Tag, t = 0.40 | **nein** |
| ≥ 6 von 9 Jahren positiv | 5 von 9 | **nein** |
| ≥ 60 % der Instrumente positiv | 8 von 17 | **nein** |
| bei doppelten Kosten > 0 | -0.16 bp/Tag | **nein** |

**PA-SD: nicht bestanden.**

| Jahr | Tage | Netto % |
|---|---|---|
| 2015 | 260 | +2.17 |
| 2016 | 260 | -0.28 |
| 2017 | 260 | -2.33 |
| 2018 | 261 | -1.80 |
| 2019 | 260 | -4.48 |
| 2020 | 261 | +2.22 |
| 2021 | 260 | +3.49 |
| 2022 | 260 | +2.25 |
| 2023 | 260 | +2.35 |

| Anlageklasse | Trades | Netto % p. a. |
|---|---|---|
| FX | 163 | -0.23 |
| Metalle | 62 | +0.11 |
| Indizes | 225 | +0.68 |
| Öl | 23 | -0.15 |

| Instrument | Trades | Netto % p. a. | Ø R netto |
|---|---|---|---|
| EURUSD | 29 | +0.11 | +0.132 |
| GBPUSD | 20 | -0.23 | -0.413 |
| USDJPY | 40 | -0.01 | -0.013 |
| AUDUSD | 18 | -0.01 | -0.026 |
| NZDUSD | 23 | +0.18 | +0.278 |
| USDCAD | 18 | -0.00 | -0.006 |
| USDCHF | 15 | -0.26 | -0.616 |
| XAUUSD | 34 | +0.22 | +0.233 |
| US500 | 34 | +0.30 | +0.313 |
| US100 | 54 | +0.15 | +0.102 |
| FRA40 | 7 | +0.07 | +0.378 |
| UK100 | 19 | -0.03 | -0.050 |
| JP225 | 38 | -0.22 | -0.205 |
| HK50 | 41 | +0.06 | +0.056 |
| AUS200 | 32 | +0.34 | +0.379 |
| Brent | 23 | -0.15 | -0.238 |
| Silber | 28 | -0.11 | -0.147 |

**Ergebnis: Keine Variante erfüllt alle In-Sample-Kriterien. Strategien Nr. 54, 55 und 60 sind gescheitert; der Hold-out bleibt unberührt.**
