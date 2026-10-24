# Modell Y (Währungsstärke), In-Sample 2015–2023 (Trial T156 Y-ASIA, T157 Y-LDN, T158 Y-USDB)

Lauf vom 24.10.2026. Regeln laut `docs/01_Vorregistrierung.md`, Code `research/cst/`. Stärke der 8 Währungen aus den 7 USD-Paaren; Y-ASIA/Y-LDN: stärkste gegen schwächste Währung bis 16:00 London; Y-USDB: Fade währungsspezifischer Abweichungen (|z| > 2). Stop 2 ATR14 H1, 0,25 % Risiko je Trade. Netto = nach Spread, Slippage, Kommission und Swaps; Ergebnis am Tag des Ausstiegs.

## Y-ASIA

| Kennzahl | Wert |
|---|---|
| Werktage / Trades | 2,347 / 1,932 |
| Netto je Tag (bp des Kapitals, Portfolio) | -0.56 bp (σ 24.2 bp) |
| vor Kosten je Tag | +0.53 bp |
| Handelskosten + Swap-Belastung je Tag | 1.09 bp |
| Rendite p. a. (netto, 0,25 % Risiko je Trade) | -1.45 % |
| Sharpe Ratio p. a. (netto) | -0.37 |
| t-Wert iid / Woche / Monat | -1.11 / -1.16 / -1.20 |
| Ø R je Trade vor / nach Kosten | +0.026 / -0.027 |
| Trefferquote / Anteil Stops | 44% / 38% |
| Ø Haltedauer | 7.6 H1-Kerzen |
| bei doppelten Kosten | -1.65 bp/Tag |

| Kriterium | Ergebnis | erfüllt |
|---|---|---|
| Mittleres Netto-Tagesergebnis > 0 mit t ≥ 3,0 (kleinster aus iid / Woche / Monat) | -0.56 bp/Tag, t = -1.20 | **nein** |
| ≥ 6 von 9 Jahren positiv | 4 von 9 | **nein** |
| ≥ 60 % der 8 Währungen positiv | 1 von 8 | **nein** |
| bei doppelten Kosten > 0 | -1.65 bp/Tag | **nein** |

**Y-ASIA: nicht bestanden.**

| Jahr | Tage | Netto % |
|---|---|---|
| 2015 | 261 | +0.18 |
| 2016 | 261 | +2.60 |
| 2017 | 260 | -4.57 |
| 2018 | 261 | +4.26 |
| 2019 | 261 | -8.20 |
| 2020 | 262 | +2.93 |
| 2021 | 261 | -3.32 |
| 2022 | 260 | -3.10 |
| 2023 | 260 | -3.87 |

| Währung | Trades | gekauft | verkauft | Netto % p. a. |
|---|---|---|---|---|
| USD | 543 | 273 | 270 | -0.25 |
| EUR | 226 | 126 | 100 | -0.38 |
| GBP | 290 | 158 | 132 | -0.61 |
| JPY | 955 | 465 | 490 | +0.74 |
| AUD | 823 | 412 | 411 | -1.38 |
| NZD | 738 | 384 | 354 | -0.86 |
| CAD | 192 | 89 | 103 | -0.01 |
| CHF | 97 | 25 | 72 | -0.16 |

Häufigste Paare: AUDJPY (344), NZDJPY (281), NZDUSD (185), AUDUSD (174), AUDNZD (114), USDJPY (98), GBPNZD (89), CADJPY (87)

## Y-LDN

| Kennzahl | Wert |
|---|---|
| Werktage / Trades | 2,347 / 1,847 |
| Netto je Tag (bp des Kapitals, Portfolio) | +0.07 bp (σ 17.7 bp) |
| vor Kosten je Tag | +0.96 bp |
| Handelskosten + Swap-Belastung je Tag | 0.89 bp |
| Rendite p. a. (netto, 0,25 % Risiko je Trade) | +0.17 % |
| Sharpe Ratio p. a. (netto) | 0.06 |
| t-Wert iid / Woche / Monat | 0.18 / 0.19 / 0.18 |
| Ø R je Trade vor / nach Kosten | +0.049 / +0.003 |
| Trefferquote / Anteil Stops | 48% / 20% |
| Ø Haltedauer | 3.8 H1-Kerzen |
| bei doppelten Kosten | -0.83 bp/Tag |

| Kriterium | Ergebnis | erfüllt |
|---|---|---|
| Mittleres Netto-Tagesergebnis > 0 mit t ≥ 3,0 (kleinster aus iid / Woche / Monat) | +0.07 bp/Tag, t = 0.18 | **nein** |
| ≥ 6 von 9 Jahren positiv | 3 von 9 | **nein** |
| ≥ 60 % der 8 Währungen positiv | 5 von 8 | ja |
| bei doppelten Kosten > 0 | -0.83 bp/Tag | **nein** |

**Y-LDN: nicht bestanden.**

| Jahr | Tage | Netto % |
|---|---|---|
| 2015 | 261 | -2.82 |
| 2016 | 261 | +4.06 |
| 2017 | 260 | -1.46 |
| 2018 | 261 | -2.57 |
| 2019 | 261 | +2.16 |
| 2020 | 262 | -0.65 |
| 2021 | 261 | -2.78 |
| 2022 | 260 | +5.95 |
| 2023 | 260 | -0.34 |

| Währung | Trades | gekauft | verkauft | Netto % p. a. |
|---|---|---|---|---|
| USD | 443 | 247 | 196 | +0.02 |
| EUR | 344 | 154 | 190 | -0.32 |
| GBP | 736 | 349 | 387 | +0.82 |
| JPY | 660 | 309 | 351 | +0.43 |
| AUD | 452 | 235 | 217 | +0.13 |
| NZD | 444 | 240 | 204 | -0.62 |
| CAD | 265 | 132 | 133 | -0.16 |
| CHF | 350 | 181 | 169 | +0.05 |

Häufigste Paare: GBPJPY (172), GBPAUD (135), GBPNZD (130), AUDJPY (130), GBPCHF (124), NZDJPY (108), NZDUSD (96), GBPUSD (96)

## Y-USDB

| Kennzahl | Wert |
|---|---|
| Werktage / Trades | 2,347 / 4,064 |
| Netto je Tag (bp des Kapitals, Portfolio) | -1.05 bp (σ 46.1 bp) |
| vor Kosten je Tag | +0.87 bp |
| Handelskosten + Swap-Belastung je Tag | 1.98 bp |
| Rendite p. a. (netto, 0,25 % Risiko je Trade) | -2.74 % |
| Sharpe Ratio p. a. (netto) | -0.37 |
| t-Wert iid / Woche / Monat | -1.10 / -1.17 / -1.16 |
| Ø R je Trade vor / nach Kosten | +0.020 / -0.024 |
| Trefferquote / Anteil Stops | 43% / 48% |
| Ø Haltedauer | 13.8 H1-Kerzen |
| bei doppelten Kosten | -3.03 bp/Tag |

| Kriterium | Ergebnis | erfüllt |
|---|---|---|
| Mittleres Netto-Tagesergebnis > 0 mit t ≥ 3,0 (kleinster aus iid / Woche / Monat) | -1.05 bp/Tag, t = -1.17 | **nein** |
| ≥ 6 von 9 Jahren positiv | 3 von 9 | **nein** |
| ≥ 60 % der 8 Währungen positiv | 3 von 8 | **nein** |
| bei doppelten Kosten > 0 | -3.03 bp/Tag | **nein** |

**Y-USDB: nicht bestanden.**

| Jahr | Tage | Netto % |
|---|---|---|
| 2015 | 261 | -4.35 |
| 2016 | 261 | +13.61 |
| 2017 | 260 | -6.49 |
| 2018 | 261 | -5.40 |
| 2019 | 261 | +1.34 |
| 2020 | 262 | -17.96 |
| 2021 | 261 | -14.48 |
| 2022 | 260 | -0.60 |
| 2023 | 260 | +9.67 |

| Währung | Trades | gekauft | verkauft | Netto % p. a. |
|---|---|---|---|---|
| USD | 4064 | 2036 | 2028 | -2.74 |
| EUR | 543 | 254 | 289 | +1.34 |
| GBP | 597 | 316 | 281 | -1.25 |
| JPY | 617 | 276 | 341 | -1.51 |
| AUD | 633 | 360 | 273 | +0.66 |
| NZD | 553 | 300 | 253 | +0.22 |
| CAD | 558 | 279 | 279 | -1.28 |
| CHF | 563 | 243 | 320 | -0.92 |

Häufigste Paare: AUDUSD (633), USDJPY (617), GBPUSD (597), USDCHF (563), USDCAD (558), NZDUSD (553), EURUSD (543)

**Ergebnis: Keine Variante erfüllt alle In-Sample-Kriterien. Strategien Nr. 46 und 47 sind gescheitert; der Hold-out bleibt unberührt.**
