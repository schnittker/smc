# P5 – Modell F (Fix-Reversal), In-Sample 2015–2023 (Trial T9 F-ALL, T10 F-EU)

Lauf vom 24.10.2026. Regeln laut `docs/08_P5_Vorregistrierung_ModellF.md`, Code `research/smc/strategy_f.py`. FX-Tage 01.01.2015–31.12.2023, HistData-M5 (Bid). Netto = nach Spread, Kommission, Slippage (Ein- und Ausstieg) und 0,7-%-Gebühr bei USDJPY; je Position gleicher Nominalwert, Ergebnisse in Basispunkten.

## Alle Paare und Fenster (beschreibend)

| Paar | Fenster | Positionen | netto Ø bp | vor Kosten Ø bp | t (netto) | Stops |
|---|---|---|---|---|---|---|
| EURUSD | W1 pre-Tokio | 1,763 | -1.62 | -0.64 | -8.08 | 0.2% |
| EURUSD | W2 post-Tokio | 2,237 | -0.52 | +0.46 | -1.68 | 1.1% |
| EURUSD | W3 pre-EZB | 2,227 | +0.49 | +1.47 | +0.84 | 16.4% |
| EURUSD | W4 post-London | 2,189 | +0.21 | +1.19 | +0.39 | 6.8% |
| GBPUSD | W1 pre-Tokio | 1,763 | -1.54 | -0.63 | -5.08 | 0.4% |
| GBPUSD | W2 post-Tokio | 2,234 | -0.75 | +0.16 | -2.26 | 0.9% |
| GBPUSD | W3 pre-EZB | 2,222 | +0.50 | +1.41 | +0.70 | 21.8% |
| GBPUSD | W4 post-London | 2,194 | +0.18 | +1.09 | +0.30 | 5.7% |
| USDJPY | W1 pre-Tokio | 1,754 | -1.55 | -0.20 | -4.82 | 1.1% |
| USDJPY | W2 post-Tokio | 2,229 | -0.59 | +0.81 | -1.08 | 5.4% |
| USDJPY | W3 pre-EZB | 2,233 | -0.23 | +1.19 | -0.43 | 9.7% |
| AUDUSD | W1 pre-Tokio | 1,760 | -2.14 | -0.62 | -5.48 | 1.1% |
| AUDUSD | W2 post-Tokio | 2,237 | -0.72 | +0.81 | -1.13 | 8.4% |
| AUDUSD | W3 pre-EZB | 2,228 | -0.96 | +0.57 | -1.36 | 8.6% |
| AUDUSD | W4 post-London | 2,186 | -0.95 | +0.57 | -1.39 | 5.8% |
| NZDUSD | W1 pre-Tokio | 1,763 | -2.68 | -0.63 | -5.41 | 2.0% |
| NZDUSD | W2 post-Tokio | 2,231 | -1.42 | +0.64 | -2.28 | 6.7% |
| NZDUSD | W3 pre-EZB | 2,226 | -1.67 | +0.38 | -2.34 | 9.1% |
| NZDUSD | W4 post-London | 2,193 | -1.96 | +0.08 | -2.81 | 6.2% |
| USDCAD | W1 pre-Tokio | 1,760 | -0.52 | +0.59 | -2.57 | 0.1% |
| USDCAD | W2 post-Tokio | 2,227 | -0.53 | +0.61 | -1.76 | 1.0% |
| USDCAD | W3 pre-EZB | 2,225 | +0.16 | +1.35 | +0.35 | 8.0% |
| USDCAD | W4 post-London | 2,195 | +0.08 | +1.30 | +0.14 | 11.4% |
| USDCHF | W1 pre-Tokio | 1,759 | -0.99 | +0.21 | -5.13 | 0.3% |
| USDCHF | W2 post-Tokio | 2,231 | -1.95 | -0.71 | -6.17 | 0.8% |
| USDCHF | W3 pre-EZB | 2,221 | -0.53 | +0.78 | -0.91 | 18.4% |
| USDCHF | W4 post-London | 2,190 | -0.98 | +0.31 | -1.62 | 7.9% |

## F-ALL

| Kennzahl | Wert |
|---|---|
| Handelstage / Positionen | 2,288 / 23,045 |
| Netto je Tag | -4.32 bp (σ 91.7 bp) |
| Kosten je Tag | 10.74 bp |
| Sharpe Ratio p. a. (netto) | -0.75 |
| t-Wert iid / Woche / Monat | -2.26 / -2.21 / -2.16 |
| bei doppelten Kosten | -15.07 bp/Tag |

| Kriterium | Ergebnis | erfüllt |
|---|---|---|
| Mittleres Netto-Tagesergebnis > 0 mit t ≥ 3,0 (kleinster aus iid / Woche / Monat) | -4.32 bp/Tag, t = -2.26 | **nein** |
| ≥ 6 von 9 Jahren positiv | 3 von 9 | **nein** |
| ≥ 60 % der Paare positiv | 0 von 3 | **nein** |
| bei doppelten Kosten > 0 | -15.07 bp/Tag | **nein** |

**F-ALL: nicht bestanden.**

| Jahr | Tage | Netto Summe bp |
|---|---|---|
| 2015 | 254 | +2343.6 |
| 2016 | 255 | +25.2 |
| 2017 | 255 | +1229.3 |
| 2018 | 254 | -2931.8 |
| 2019 | 254 | -1896.9 |
| 2020 | 254 | -972.8 |
| 2021 | 253 | -2447.7 |
| 2022 | 255 | -2995.3 |
| 2023 | 254 | -2248.2 |

| Paar | Netto Summe bp |
|---|---|
| EURUSD | -2472.2 |
| GBPUSD | -2861.6 |
| USDJPY | -4560.7 |

## F-EU

| Kennzahl | Wert |
|---|---|
| Handelstage / Positionen | 2,266 / 8,832 |
| Netto je Tag | +1.36 bp (σ 70.3 bp) |
| Kosten je Tag | 3.68 bp |
| Sharpe Ratio p. a. (netto) | 0.31 |
| t-Wert iid / Woche / Monat | 0.92 / 0.96 / 0.93 |
| bei doppelten Kosten | -2.33 bp/Tag |

| Kriterium | Ergebnis | erfüllt |
|---|---|---|
| Mittleres Netto-Tagesergebnis > 0 mit t ≥ 3,0 (kleinster aus iid / Woche / Monat) | +1.36 bp/Tag, t = 0.92 | **nein** |
| ≥ 6 von 9 Jahren positiv | 6 von 9 | ja |
| ≥ 60 % der Paare positiv | 2 von 2 | ja |
| bei doppelten Kosten > 0 | -2.33 bp/Tag | **nein** |

**F-EU: nicht bestanden.**

| Jahr | Tage | Netto Summe bp |
|---|---|---|
| 2015 | 254 | +1939.1 |
| 2016 | 255 | +324.5 |
| 2017 | 255 | +1569.4 |
| 2018 | 254 | -715.8 |
| 2019 | 254 | +298.6 |
| 2020 | 254 | +65.7 |
| 2021 | 253 | -728.8 |
| 2022 | 255 | -358.1 |
| 2023 | 232 | +677.2 |

| Paar | Netto Summe bp |
|---|---|
| EURUSD | +1550.0 |
| GBPUSD | +1521.8 |

**Ergebnis: Keine Variante erfüllt alle In-Sample-Kriterien. P5 ist gescheitert; der Hold-out bleibt unberührt.**
