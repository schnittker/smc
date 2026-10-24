# P6 – Modell G (Trendfolge D1), In-Sample 2015–2023 (Trial T13)

Lauf vom 24.10.2026. Regeln laut `docs/10_P6_Vorregistrierung_ModellG.md`, Code `research/smc/strategy_g.py`. Handelstage 01.01.2015–31.12.2023 (Warm-up 2014), 25 Instrumente. Netto = nach Handelskosten, Swaps und 0,7-%-Gebühr. Renditen und Drawdown sind auf eine Portfolio-Volatilität von 10 % p. a. skaliert (Kalibrierung auf diesen Zeitraum, nur zur Einordnung).

| Kennzahl | Wert |
|---|---|
| Handelstage | 2,340 |
| Sharpe Ratio p. a. (netto) | -0.53 |
| t-Wert iid / Woche / Monat | -1.59 / -1.62 / -1.77 |
| Rendite p. a. bei 10 % Volatilität | -5.31% |
| Max. Drawdown bei 10 % Volatilität | 52.9% |
| Kosten p. a. bei 10 % Vol.: Handel / Swaps (+ = Gutschrift) / 0,7-%-Gebühr | 0.84% / -2.43% / 0.21% |
| Ø Brutto-Exposure (Summe \|w\|, unskaliert) | 19.3 |

| Kriterium | Ergebnis | erfüllt |
|---|---|---|
| Mittleres Netto-Tagesergebnis > 0 mit t ≥ 3,0 (kleinster aus iid / Woche / Monat) | t = -1.77 (Sharpe -0.53) | **nein** |
| ≥ 6 von 9 Jahren positiv | 1 von 9 | **nein** |
| ≥ 60 % der Instrumente positiv | 6 von 25 | **nein** |
| bei doppelten Kosten > 0 | -9.31% p. a. bei 10 % Vol. | **nein** |

**Modell G In-Sample: nicht bestanden. P6 ist gescheitert; der Hold-out bleibt unberührt.**

| Jahr | Rendite bei 10 % Vol. | Sharpe |
|---|---|---|
| 2015 | -5.6% | -0.56 |
| 2016 | -5.1% | -0.53 |
| 2017 | -6.1% | -0.76 |
| 2018 | -5.1% | -0.51 |
| 2019 | -7.0% | -0.77 |
| 2020 | -4.3% | -0.32 |
| 2021 | -11.0% | -1.17 |
| 2022 | +1.9% | +0.16 |
| 2023 | -5.2% | -0.69 |

| Instrument | Beitrag bei 10 % Portfolio-Vol. (Summe) | Sharpe einzeln |
|---|---|---|
| EURCHF | +3.0% | +0.17 |
| USDJPY | +2.3% | +0.26 |
| GBPJPY | +2.1% | +0.25 |
| GBPUSD | +1.0% | +0.12 |
| CADJPY | +0.9% | +0.10 |
| CHFJPY | +0.3% | +0.03 |
| NZDUSD | -0.3% | -0.04 |
| AUDJPY | -0.4% | -0.05 |
| AUDUSD | -0.4% | -0.05 |
| EURNZD | -0.9% | -0.10 |
| GBPAUD | -1.0% | -0.12 |
| EURJPY | -1.4% | -0.16 |
| EURUSD | -1.5% | -0.18 |
| USDCAD | -1.8% | -0.22 |
| XAUUSD | -1.9% | -0.23 |
| EURAUD | -2.1% | -0.24 |
| NZDJPY | -2.1% | -0.26 |
| GBPNZD | -2.3% | -0.27 |
| AUDCAD | -3.8% | -0.46 |
| EURCAD | -4.6% | -0.56 |
| GBPCAD | -5.1% | -0.63 |
| AUDNZD | -5.5% | -0.65 |
| GBPCHF | -6.0% | -0.50 |
| USDCHF | -7.8% | -0.71 |
| CADCHF | -8.1% | -0.76 |

