# Modell LV (Intraday-Level), In-Sample 2015–2023 (Trial T165 LV-VA80, T166 LV-PFADE, T167 LV-PBRK)

Lauf vom 24.10.2026. Regeln laut `docs/01_Vorregistrierung.md`, Code `research/lvl/`. LV-VA80: 80-%-Regel der Value Area auf US500, US100, FRA40, UK100; LV-PFADE/LV-PBRK: klassische Pivots auf 7 Majors und 7 Indizes. 0,25 % Risiko je Trade. Netto = nach Spread, Slippage und Kommission; Portfolio = Summe je Tag.

## LV-VA80

| Kennzahl | Wert |
|---|---|
| Handelstage / Trades | 2,254 / 1,800 |
| Netto je Tag (bp des Kapitals, Portfolio) | -0.83 bp (σ 18.8 bp) |
| vor Kosten je Tag | +0.07 bp |
| Kosten je Tag | 0.90 bp |
| Rendite p. a. (netto, 0,25 % Risiko je Trade) | -2.08 % |
| Sharpe Ratio p. a. (netto) | -0.70 |
| t-Wert iid / Woche / Monat | -2.10 / -2.02 / -1.96 |
| Ø R je Trade vor / nach Kosten | +0.004 / -0.042 |
| Trefferquote | 56% |
| Ausstiege Ziel / Stop / Zeit | 45% / 26% / 29% |
| bei doppelten Kosten | -1.74 bp/Tag |

| Kriterium | Ergebnis | erfüllt |
|---|---|---|
| Mittleres Netto-Tagesergebnis > 0 mit t ≥ 3,0 (kleinster aus iid / Woche / Monat) | -0.83 bp/Tag, t = -2.10 | **nein** |
| ≥ 6 von 9 Jahren positiv | 3 von 9 | **nein** |
| ≥ 60 % der Instrumente positiv | 1 von 4 | **nein** |
| bei doppelten Kosten > 0 | -1.74 bp/Tag | **nein** |

**LV-VA80: nicht bestanden.**

| Jahr | Tage | Netto % |
|---|---|---|
| 2015 | 253 | -3.09 |
| 2016 | 254 | +0.25 |
| 2017 | 249 | -5.20 |
| 2018 | 253 | -1.87 |
| 2019 | 253 | -3.52 |
| 2020 | 254 | +0.95 |
| 2021 | 253 | -4.10 |
| 2022 | 254 | +1.84 |
| 2023 | 231 | -3.99 |

| Instrument | Trades | Netto % p. a. | Ø R netto |
|---|---|---|---|
| US500 | 400 | +0.07 | +0.006 |
| US100 | 436 | -0.18 | -0.015 |
| FRA40 | 491 | -1.35 | -0.099 |
| UK100 | 473 | -0.62 | -0.047 |

## LV-PFADE

| Kennzahl | Wert |
|---|---|
| Handelstage / Trades | 2,291 / 24,300 |
| Netto je Tag (bp des Kapitals, Portfolio) | -12.63 bp (σ 107.0 bp) |
| vor Kosten je Tag | -1.76 bp |
| Kosten je Tag | 10.86 bp |
| Rendite p. a. (netto, 0,25 % Risiko je Trade) | -32.14 % |
| Sharpe Ratio p. a. (netto) | -1.88 |
| t-Wert iid / Woche / Monat | -5.65 / -5.89 / -7.30 |
| Ø R je Trade vor / nach Kosten | -0.005 / -0.048 |
| Trefferquote | 46% |
| Ausstiege Ziel / Stop / Zeit | 29% / 38% / 32% |
| bei doppelten Kosten | -23.49 bp/Tag |

| Kriterium | Ergebnis | erfüllt |
|---|---|---|
| Mittleres Netto-Tagesergebnis > 0 mit t ≥ 3,0 (kleinster aus iid / Woche / Monat) | -12.63 bp/Tag, t = -7.30 | **nein** |
| ≥ 6 von 9 Jahren positiv | 0 von 9 | **nein** |
| ≥ 60 % der Instrumente positiv | 0 von 14 | **nein** |
| bei doppelten Kosten > 0 | -23.49 bp/Tag | **nein** |

**LV-PFADE: nicht bestanden.**

| Jahr | Tage | Netto % |
|---|---|---|
| 2015 | 254 | -32.87 |
| 2016 | 255 | -34.84 |
| 2017 | 255 | -34.49 |
| 2018 | 254 | -25.59 |
| 2019 | 254 | -38.46 |
| 2020 | 255 | -33.04 |
| 2021 | 254 | -34.61 |
| 2022 | 255 | -33.58 |
| 2023 | 255 | -21.78 |

| Instrument | Trades | Netto % p. a. | Ø R netto |
|---|---|---|---|
| EURUSD | 1740 | -1.62 | -0.034 |
| GBPUSD | 1741 | -2.24 | -0.046 |
| USDJPY | 1702 | -3.53 | -0.075 |
| AUDUSD | 1747 | -1.40 | -0.029 |
| NZDUSD | 1749 | -1.18 | -0.025 |
| USDCAD | 1721 | -2.50 | -0.052 |
| USDCHF | 1772 | -1.29 | -0.026 |
| US500 | 1705 | -1.11 | -0.024 |
| US100 | 1704 | -2.59 | -0.055 |
| FRA40 | 1770 | -4.99 | -0.107 |
| UK100 | 1745 | -0.17 | -0.004 |
| JP225 | 1723 | -4.95 | -0.104 |
| HK50 | 1695 | -4.32 | -0.094 |
| AUS200 | 1786 | -0.26 | -0.005 |

## LV-PBRK

| Kennzahl | Wert |
|---|---|
| Handelstage / Trades | 2,291 / 3,866 |
| Netto je Tag (bp des Kapitals, Portfolio) | -4.25 bp (σ 69.0 bp) |
| vor Kosten je Tag | -1.91 bp |
| Kosten je Tag | 2.35 bp |
| Rendite p. a. (netto, 0,25 % Risiko je Trade) | -10.83 % |
| Sharpe Ratio p. a. (netto) | -0.98 |
| t-Wert iid / Woche / Monat | -2.95 / -3.08 / -3.26 |
| Ø R je Trade vor / nach Kosten | -0.045 / -0.101 |
| Trefferquote | 38% |
| Ausstiege Ziel / Stop / Zeit | 0% / 42% / 58% |
| bei doppelten Kosten | -6.60 bp/Tag |

| Kriterium | Ergebnis | erfüllt |
|---|---|---|
| Mittleres Netto-Tagesergebnis > 0 mit t ≥ 3,0 (kleinster aus iid / Woche / Monat) | -4.25 bp/Tag, t = -3.26 | **nein** |
| ≥ 6 von 9 Jahren positiv | 1 von 9 | **nein** |
| ≥ 60 % der Instrumente positiv | 2 von 14 | **nein** |
| bei doppelten Kosten > 0 | -6.60 bp/Tag | **nein** |

**LV-PBRK: nicht bestanden.**

| Jahr | Tage | Netto % |
|---|---|---|
| 2015 | 254 | -11.50 |
| 2016 | 255 | -19.97 |
| 2017 | 255 | -20.88 |
| 2018 | 254 | -6.66 |
| 2019 | 254 | -18.39 |
| 2020 | 255 | -1.83 |
| 2021 | 254 | +7.31 |
| 2022 | 255 | -11.68 |
| 2023 | 255 | -13.84 |

| Instrument | Trades | Netto % p. a. | Ø R netto |
|---|---|---|---|
| EURUSD | 269 | -0.67 | -0.089 |
| GBPUSD | 276 | -1.58 | -0.206 |
| USDJPY | 306 | +0.61 | +0.071 |
| AUDUSD | 253 | -1.50 | -0.214 |
| NZDUSD | 272 | -2.26 | -0.299 |
| USDCAD | 260 | -1.09 | -0.151 |
| USDCHF | 246 | -0.74 | -0.109 |
| US500 | 271 | -0.60 | -0.080 |
| US100 | 275 | -0.03 | -0.004 |
| FRA40 | 324 | -1.74 | -0.193 |
| UK100 | 256 | -0.63 | -0.088 |
| JP225 | 275 | +0.26 | +0.034 |
| HK50 | 358 | -0.59 | -0.059 |
| AUS200 | 225 | -0.26 | -0.041 |

**Ergebnis: Keine Variante erfüllt alle In-Sample-Kriterien. Strategien Nr. 48 und 49 sind gescheitert; der Hold-out bleibt unberührt.**
