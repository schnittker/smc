# Modell B (Kanal-Ausbruch), In-Sample 2015–2023 (Trial T96 B-52W = Nr. 28, T97 B-TURTLE = Nr. 30)

Lauf vom 24.10.2026. Regeln laut `docs/01_Vorregistrierung.md`, Code `research/brk/`. Handelstage 01.01.2015–31.12.2023 (Warm-up 2014), 34 Instrumente. Netto = nach Handelskosten, Swaps und 0,7-%-Gebühr (Kostenmodelle G und H). Renditen und Drawdown sind auf eine Portfolio-Volatilität von 10 % p. a. skaliert (Kalibrierung auf diesen Zeitraum, nur zur Einordnung).

## B-52W

| Kennzahl | Wert |
|---|---|
| Handelstage | 2,340 |
| Sharpe Ratio p. a. (netto) | -0.54 |
| t-Wert iid / Woche / Monat | -1.61 / -1.62 / -1.75 |
| Rendite p. a. bei 10 % Volatilität | -5.39% |
| Max. Drawdown bei 10 % Volatilität | 51.4% |
| Zerlegung p. a. bei 10 % Vol.: Kurs / Swaps / Handel / Gebühr | -2.96% / -2.31% / -0.05% / -0.07% |
| Ø Brutto-Exposure (Summe \|w\|, unskaliert) | 25.09 |

| Kriterium | Ergebnis | erfüllt |
|---|---|---|
| Mittleres Netto-Tagesergebnis > 0 mit t ≥ 3,0 (kleinster aus iid / Woche / Monat) | t = -1.75 (Sharpe -0.54) | **nein** |
| ≥ 6 von 9 Jahren positiv | 1 von 9 | **nein** |
| ≥ 60 % der Instrumente (≥ 250 Positionstage) positiv | 8 von 34 | **nein** |
| bei doppelten Kosten > 0 | -8.30% p. a. bei 10 % Vol. | **nein** |

**B-52W: nicht bestanden.**

| Jahr | Rendite bei 10 % Vol. | Sharpe |
|---|---|---|
| 2015 | -6.4% | -0.66 |
| 2016 | -3.4% | -0.27 |
| 2017 | -0.4% | -0.07 |
| 2018 | -10.9% | -1.40 |
| 2019 | -10.3% | -1.30 |
| 2020 | -11.1% | -0.77 |
| 2021 | -1.9% | -0.22 |
| 2022 | +1.2% | +0.10 |
| 2023 | -5.1% | -0.87 |

| Instrument | Positionstage | Beitrag netto bei 10 % Vol. (Summe) | davon Swaps |
|---|---|---|---|
| EURJPY | 1790 | +1.4% | -0.3% |
| EURCHF | 1701 | +0.9% | -1.2% |
| BCOUSD | 1832 | +0.9% | -0.4% |
| GBPJPY | 1759 | +0.7% | -0.3% |
| CHFJPY | 1810 | +0.7% | -0.7% |
| NSXUSD | 2068 | +0.1% | -0.8% |
| USDJPY | 1429 | +0.1% | -0.5% |
| EURUSD | 1719 | +0.1% | -0.3% |
| AUDJPY | 1897 | -0.1% | -0.8% |
| XAUUSD | 1476 | -0.5% | -0.6% |
| GBPCAD | 1584 | -0.6% | -0.6% |
| NZDJPY | 1991 | -0.6% | -0.1% |
| HKXHKD | 1442 | -0.7% | -0.6% |
| SPXUSD | 2041 | -0.7% | -0.8% |
| EURCAD | 1913 | -1.0% | -0.6% |
| AUDUSD | 1511 | -1.1% | -0.5% |
| CADJPY | 1616 | -1.1% | -0.4% |
| JPXJPY | 1822 | -1.2% | -0.6% |
| GBPAUD | 1711 | -1.6% | -0.7% |
| NZDUSD | 1582 | -1.8% | -0.7% |
| FRXEUR | 1774 | -1.8% | -0.4% |
| EURAUD | 1650 | -1.9% | -1.0% |
| GBPUSD | 1531 | -1.9% | -0.5% |
| USDCAD | 1591 | -2.0% | -0.7% |
| GBPNZD | 1384 | -2.2% | -0.5% |
| XAGUSD | 1665 | -2.5% | -0.2% |
| AUXAUD | 1600 | -2.7% | -0.4% |
| USDCHF | 1734 | -2.8% | -0.6% |
| CADCHF | 1522 | -3.1% | -1.0% |
| UKXGBP | 1745 | -3.8% | -0.6% |
| GBPCHF | 1778 | -3.9% | -1.4% |
| EURNZD | 1915 | -4.0% | -0.8% |
| AUDCAD | 1759 | -4.2% | -0.7% |
| AUDNZD | 1388 | -5.4% | -0.6% |

| Anlageklasse | Beitrag netto bei 10 % Vol. (Summe 2015–2023) |
|---|---|
| FX | -35.4% |
| Metalle | -3.0% |
| Indizes | -10.7% |
| Öl | +0.9% |

## B-TURTLE

| Kennzahl | Wert |
|---|---|
| Handelstage | 2,340 |
| Sharpe Ratio p. a. (netto) | -0.54 |
| t-Wert iid / Woche / Monat | -1.63 / -1.62 / -2.01 |
| Rendite p. a. bei 10 % Volatilität | -5.43% |
| Max. Drawdown bei 10 % Volatilität | 54.9% |
| Zerlegung p. a. bei 10 % Vol.: Kurs / Swaps / Handel / Gebühr | -2.81% / -2.16% / -0.29% / -0.17% |
| Ø Brutto-Exposure (Summe \|w\|, unskaliert) | 21.16 |

| Kriterium | Ergebnis | erfüllt |
|---|---|---|
| Mittleres Netto-Tagesergebnis > 0 mit t ≥ 3,0 (kleinster aus iid / Woche / Monat) | t = -2.01 (Sharpe -0.54) | **nein** |
| ≥ 6 von 9 Jahren positiv | 1 von 9 | **nein** |
| ≥ 60 % der Instrumente (≥ 250 Positionstage) positiv | 8 von 34 | **nein** |
| bei doppelten Kosten > 0 | -8.42% p. a. bei 10 % Vol. | **nein** |

**B-TURTLE: nicht bestanden.**

| Jahr | Rendite bei 10 % Vol. | Sharpe |
|---|---|---|
| 2015 | -4.9% | -0.46 |
| 2016 | -4.4% | -0.48 |
| 2017 | -4.8% | -0.77 |
| 2018 | -5.7% | -0.66 |
| 2019 | -9.3% | -1.26 |
| 2020 | +1.5% | +0.08 |
| 2021 | -9.0% | -1.16 |
| 2022 | -1.5% | -0.15 |
| 2023 | -10.6% | -1.70 |

| Instrument | Positionstage | Beitrag netto bei 10 % Vol. (Summe) | davon Swaps |
|---|---|---|---|
| HKXHKD | 1299 | +1.7% | -0.5% |
| USDJPY | 1319 | +1.6% | -0.4% |
| GBPNZD | 1478 | +1.2% | -0.6% |
| BCOUSD | 1453 | +1.2% | -0.3% |
| SPXUSD | 1494 | +0.7% | -0.8% |
| GBPAUD | 1494 | +0.7% | -0.6% |
| GBPJPY | 1284 | +0.3% | -0.3% |
| CADJPY | 1335 | +0.1% | -0.4% |
| USDCAD | 1328 | -0.1% | -0.7% |
| GBPUSD | 1406 | -0.1% | -0.5% |
| GBPCAD | 1494 | -0.2% | -0.6% |
| CHFJPY | 1405 | -0.2% | -0.6% |
| NSXUSD | 1600 | -0.6% | -0.8% |
| XAUUSD | 1452 | -0.7% | -0.5% |
| EURUSD | 1451 | -0.9% | -0.5% |
| JPXJPY | 1318 | -1.5% | -0.5% |
| NZDJPY | 1405 | -1.5% | -0.5% |
| FRXEUR | 1377 | -1.7% | -0.5% |
| EURCHF | 1410 | -1.7% | -1.1% |
| NZDUSD | 1462 | -1.8% | -0.5% |
| AUDJPY | 1353 | -1.9% | -0.4% |
| AUXAUD | 1442 | -1.9% | -0.6% |
| AUDUSD | 1507 | -2.0% | -0.5% |
| EURNZD | 1457 | -2.0% | -0.6% |
| EURJPY | 1451 | -2.2% | -0.5% |
| AUDNZD | 1328 | -2.5% | -0.9% |
| XAGUSD | 1377 | -3.1% | -0.2% |
| EURCAD | 1403 | -3.3% | -0.5% |
| CADCHF | 1356 | -3.5% | -0.9% |
| AUDCAD | 1446 | -3.7% | -0.6% |
| EURAUD | 1374 | -3.9% | -0.6% |
| UKXGBP | 1309 | -4.2% | -0.6% |
| USDCHF | 1320 | -5.2% | -0.8% |
| GBPCHF | 1412 | -6.0% | -0.9% |

| Anlageklasse | Beitrag netto bei 10 % Vol. (Summe 2015–2023) |
|---|---|
| FX | -38.7% |
| Metalle | -3.8% |
| Indizes | -7.4% |
| Öl | +1.2% |

**Ergebnis: Keine Variante erfüllt alle In-Sample-Kriterien. Die Strategien Nr. 28 und Nr. 30 sind gescheitert; der Hold-out bleibt unberührt.**
