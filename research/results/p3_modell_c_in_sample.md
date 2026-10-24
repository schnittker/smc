# P3 – Modell C, In-Sample 2015–2023 (Trial T2 C-MKT, T3 C-LMT)

Lauf vom 24.10.2026, Regeln laut `docs/04_P3_Vorregistrierung_ModellC.md`, Code `research/smc/strategy_c.py`. Signale 01.01.2015–31.12.2023, alle 25 Instrumente, HistData-M1 (Bid). Netto = nach Spread (über Ask/Bid-Fills), FTMO-Kommission und Slippage; ohne 0,7-%-Umrechnungsgebühr. Der t-Wert für das Kriterium ist der kleinste aus iid, Cluster nach FTMO-Tag und Cluster nach Woche (Einstiegstag).

## C-MKT

1,586 Signale (strikter H1-Wechsel in Richtung des strikten H4-Trends).

| Status | Anzahl |
|---|---|
| gehandelt | 1,586 |

| Kennzahl | Wert |
|---|---|
| Trades | 1,586 |
| Netto-Erwartungswert | +0.015 R (σ 0.66) |
| vor Kosten (netto + Kosten) | +0.026 R |
| Ø Kosten (Spread, Kommission, Slippage) | 0.011 R |
| t-Wert iid / Tages-Cluster / Wochen-Cluster | 0.91 / 0.81 / 0.77 |
| Profit-Factor netto | 1.06 |
| Trefferquote | 50.2% |
| bei doppelten Kosten | +0.004 R |

- Ausstieg: Ziel 2%, Stop 10%, Zeit-Stopp 88% (Ø +0.10 R)
- Ziel-Abstand Ø 2.08 R; Ziel-Typ: 4 R (Deckel) 1%, 2 R (kein Pool) 86%, swing_ext 11%, pwhl 0%, pmhl 2%
- Haltedauer Median 120.0 h; Kosten Median 0.010 R
- Long 786 Trades Ø +0.022 R; Short 800 Trades Ø +0.009 R

| Kriterium | Ergebnis | erfüllt |
|---|---|---|
| Netto-Erwartungswert ≥ +0,10 R | +0.015 R | **nein** |
| t-Wert ≥ 2,5 (kleinster aus iid / Tag / Woche) | 0.77 | **nein** |
| Netto-Profit-Factor ≥ 1,2 | 1.06 | **nein** |
| ≥ 6 von 9 Jahren positiv | 6 von 9 | ja |
| ≥ 60 % der Instrumente (≥ 10 Trades) positiv | 12 von 25 (48%) | **nein** |
| bei doppelten Kosten > 0 | +0.004 R | ja |

**C-MKT: nicht bestanden.**

| Jahr | Trades | Netto Ø R |
|---|---|---|
| 2015 | 180 | +0.010 |
| 2016 | 189 | +0.092 |
| 2017 | 187 | +0.002 |
| 2018 | 180 | +0.021 |
| 2019 | 189 | +0.034 |
| 2020 | 176 | +0.075 |
| 2021 | 168 | -0.091 |
| 2022 | 174 | -0.011 |
| 2023 | 143 | -0.010 |

| Instrument | Trades | Netto Ø R |
|---|---|---|
| EURUSD | 64 | +0.160 |
| CADCHF | 59 | +0.158 |
| CHFJPY | 56 | +0.134 |
| XAUUSD | 57 | +0.133 |
| GBPNZD | 68 | +0.111 |
| AUDJPY | 54 | +0.063 |
| NZDUSD | 65 | +0.037 |
| USDJPY | 57 | +0.036 |
| EURAUD | 66 | +0.025 |
| EURCHF | 66 | +0.024 |
| NZDJPY | 71 | +0.019 |
| AUDNZD | 60 | +0.001 |
| GBPCAD | 70 | -0.000 |
| AUDCAD | 74 | -0.007 |
| EURCAD | 68 | -0.008 |
| EURJPY | 61 | -0.008 |
| GBPUSD | 67 | -0.008 |
| EURNZD | 64 | -0.008 |
| GBPJPY | 72 | -0.009 |
| USDCHF | 51 | -0.012 |
| GBPAUD | 62 | -0.027 |
| USDCAD | 63 | -0.044 |
| CADJPY | 59 | -0.059 |
| AUDUSD | 66 | -0.082 |
| GBPCHF | 66 | -0.200 |

## C-LMT

1,586 Signale (strikter H1-Wechsel in Richtung des strikten H4-Trends).

| Status | Anzahl |
|---|---|
| gehandelt | 803 |
| keine Zone | 14 |
| Kosten-Gate (> 0,10 R) | 28 |
| Storno: Ziel erreicht | 129 |
| abgelaufen (288 Bars) | 612 |

| Kennzahl | Wert |
|---|---|
| Trades | 803 |
| Netto-Erwartungswert | -0.016 R (σ 0.80) |
| vor Kosten (netto + Kosten) | -0.003 R |
| Ø Kosten (Spread, Kommission, Slippage) | 0.013 R |
| t-Wert iid / Tages-Cluster / Wochen-Cluster | -0.56 / -0.55 / -0.53 |
| Profit-Factor netto | 0.95 |
| Trefferquote | 45.8% |
| bei doppelten Kosten | -0.028 R |

- Ausstieg: Ziel 2%, Stop 17%, Zeit-Stopp 81% (Ø +0.13 R)
- Ziel-Abstand Ø 2.17 R; Ziel-Typ: 4 R (Deckel) 2%, 2 R (kein Pool) 76%, swing_int 1%, swing_ext 17%, pwhl 1%, pmhl 3%
- Haltedauer Median 120.0 h; Kosten Median 0.010 R
- Long 409 Trades Ø +0.001 R; Short 394 Trades Ø -0.033 R
- Einstieg: FVG-CE 788 Trades Ø -0.013 R; OB-MT 15 Trades Ø -0.175 R

| Kriterium | Ergebnis | erfüllt |
|---|---|---|
| Netto-Erwartungswert ≥ +0,10 R | -0.016 R | **nein** |
| t-Wert ≥ 2,5 (kleinster aus iid / Tag / Woche) | -0.56 | **nein** |
| Netto-Profit-Factor ≥ 1,2 | 0.95 | **nein** |
| ≥ 6 von 9 Jahren positiv | 4 von 9 | **nein** |
| ≥ 60 % der Instrumente (≥ 10 Trades) positiv | 12 von 25 (48%) | **nein** |
| bei doppelten Kosten > 0 | -0.028 R | **nein** |

**C-LMT: nicht bestanden.**

| Jahr | Trades | Netto Ø R |
|---|---|---|
| 2015 | 88 | -0.102 |
| 2016 | 103 | +0.082 |
| 2017 | 94 | -0.021 |
| 2018 | 92 | -0.089 |
| 2019 | 83 | +0.002 |
| 2020 | 77 | +0.064 |
| 2021 | 87 | -0.125 |
| 2022 | 104 | -0.037 |
| 2023 | 75 | +0.104 |

| Instrument | Trades | Netto Ø R |
|---|---|---|
| EURUSD | 27 | +0.309 |
| XAUUSD | 27 | +0.178 |
| AUDNZD | 20 | +0.160 |
| GBPCAD | 40 | +0.156 |
| GBPAUD | 36 | +0.151 |
| CADCHF | 31 | +0.128 |
| AUDJPY | 25 | +0.105 |
| CHFJPY | 26 | +0.100 |
| GBPNZD | 26 | +0.090 |
| AUDCAD | 37 | +0.069 |
| USDCHF | 32 | +0.029 |
| CADJPY | 30 | +0.014 |
| NZDJPY | 40 | -0.004 |
| EURCHF | 36 | -0.009 |
| EURJPY | 40 | -0.036 |
| USDJPY | 30 | -0.043 |
| GBPJPY | 45 | -0.049 |
| AUDUSD | 35 | -0.078 |
| NZDUSD | 32 | -0.079 |
| EURAUD | 34 | -0.159 |
| EURCAD | 26 | -0.162 |
| EURNZD | 35 | -0.178 |
| USDCAD | 36 | -0.208 |
| GBPUSD | 29 | -0.242 |
| GBPCHF | 28 | -0.533 |

**Ergebnis: Keine Variante erfüllt alle In-Sample-Kriterien. P3 ist gescheitert; der Hold-out bleibt unberührt.**
