# P4 – Modell D, In-Sample 2015–2023 (Trial T6)

Lauf vom 24.10.2026. Regeln laut `docs/06_P4_Vorregistrierung_ModellD.md`, Code `research/smc/strategy_d.py`. Signale 01.01.2015–31.12.2023, 25 Instrumente, HistData-M1 (Bid). Netto = nach Spread (Ask/Bid-Fills), Kommission, Slippage, Swaps (Zinsdifferenz − 1 % p. a.) und 0,7-%-Umrechnungsgebühr.

1,586 Signale (strikter H1-Wechsel in Richtung des strikten H4-Trends).

| Status | Anzahl |
|---|---|
| gehandelt | 1,586 |

| Kennzahl | Wert |
|---|---|
| Trades | 1,586 |
| Netto-Erwartungswert | -0.040 R (σ 1.20) |
| t-Wert iid / Tag / Woche / Monat | -1.33 / -1.18 / -1.02 / -1.05 |
| Profit-Factor netto | 0.91 |
| Trefferquote | 36.3% |
| Ø Gewinner / Ø Verlierer | +1.13 R / -0.70 R |
| größter Gewinner, P90 der Gewinner | +10.06 R, +2.65 R |
| Ø Kosten gesamt (Spread, Kommission, Slippage, Gebühr, belastende Swaps) | 0.050 R |
| davon Ø Swap (+ = Gutschrift) / Ø 0,7-%-Gebühr | -0.029 R / 0.005 R |
| bei doppelten Kosten | -0.090 R |
| Haltedauer Median / Mittel | 9.5 / 10.7 Handelstage |

- Struktur-Exit: 51% der Trades, Ø +0.043 R
- Stop: 31% der Trades, Ø -1.040 R
- Zeit-Stopp: 18% der Trades, Ø +1.448 R
- Long 786 Trades Ø -0.029 R; Short 800 Trades Ø -0.051 R

| Kriterium | Ergebnis | erfüllt |
|---|---|---|
| Netto-Erwartungswert ≥ +0,10 R | -0.040 R | **nein** |
| t-Wert ≥ 3,0 (kleinster aus iid / Tag / Woche / Monat) | -1.33 | **nein** |
| Netto-Profit-Factor ≥ 1,2 | 0.91 | **nein** |
| ≥ 6 von 9 Jahren positiv | 4 von 9 | **nein** |
| ≥ 60% der Instrumente (≥ 10 Trades) positiv | 11 von 25 (44%) | **nein** |
| bei doppelten Kosten > 0 | -0.090 R | **nein** |

**Modell D In-Sample: nicht bestanden. P4 ist gescheitert; der Hold-out bleibt unberührt.**

| Jahr | Trades | Netto Ø R |
|---|---|---|
| 2015 | 180 | +0.033 |
| 2016 | 189 | -0.061 |
| 2017 | 187 | +0.023 |
| 2018 | 180 | -0.136 |
| 2019 | 189 | -0.020 |
| 2020 | 176 | +0.035 |
| 2021 | 168 | -0.155 |
| 2022 | 174 | +0.041 |
| 2023 | 143 | -0.150 |

| Instrument | Trades | Netto Ø R |
|---|---|---|
| XAUUSD | 57 | +0.414 |
| AUDJPY | 54 | +0.220 |
| EURUSD | 64 | +0.184 |
| CADCHF | 59 | +0.171 |
| USDCHF | 51 | +0.134 |
| NZDUSD | 65 | +0.065 |
| CADJPY | 59 | +0.034 |
| EURCHF | 66 | +0.029 |
| GBPJPY | 72 | +0.029 |
| NZDJPY | 71 | +0.017 |
| GBPUSD | 67 | +0.002 |
| CHFJPY | 56 | -0.024 |
| EURJPY | 61 | -0.090 |
| EURNZD | 64 | -0.095 |
| USDJPY | 57 | -0.102 |
| GBPCAD | 70 | -0.113 |
| USDCAD | 63 | -0.115 |
| EURAUD | 66 | -0.130 |
| GBPNZD | 68 | -0.133 |
| AUDUSD | 66 | -0.176 |
| AUDNZD | 60 | -0.195 |
| EURCAD | 68 | -0.207 |
| GBPAUD | 62 | -0.215 |
| GBPCHF | 66 | -0.245 |
| AUDCAD | 74 | -0.282 |

