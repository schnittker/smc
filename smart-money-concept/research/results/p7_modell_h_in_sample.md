# P7 – Modell H (Trendfolge Indizes und Rohstoffe), In-Sample 2015–2023 (Trial T16)

Lauf vom 24.10.2026. Regeln laut `docs/12_P7_Vorregistrierung_ModellH.md`, Code `research/smc/strategy_h.py` und `strategy_g.run_trend`. Handelstage 01.01.2015–31.12.2023 (Warm-up 2014), 10 Instrumente (ohne ETXEUR, GRXEUR, WTIUSD wegen Datenfehlern). Netto = nach Handelskosten, Swaps und 0,7-%-Gebühr. Renditen und Drawdown sind auf eine Portfolio-Volatilität von 10 % p. a. skaliert (Kalibrierung auf diesen Zeitraum, nur zur Einordnung).

| Kennzahl | Wert |
|---|---|
| Handelstage | 2,333 |
| Sharpe Ratio p. a. (netto) | -0.37 |
| t-Wert iid / Woche / Monat | -1.10 / -1.05 / -1.14 |
| Rendite p. a. bei 10 % Volatilität | -3.67% |
| Max. Drawdown bei 10 % Volatilität | 42.6% |
| Kosten p. a. bei 10 % Vol.: Handel / Swaps (+ = Gutschrift) / 0,7-%-Gebühr | 0.91% / -1.93% / 0.12% |
| Ø Brutto-Exposure (Summe \|w\|, unskaliert) | 4.0 |

| Kriterium | Ergebnis | erfüllt |
|---|---|---|
| Mittleres Netto-Tagesergebnis > 0 mit t ≥ 3,0 (kleinster aus iid / Woche / Monat) | t = -1.14 (Sharpe -0.37) | **nein** |
| ≥ 6 von 9 Jahren positiv | 3 von 9 | **nein** |
| ≥ 60 % der Instrumente positiv | 4 von 10 | **nein** |
| bei doppelten Kosten > 0 | -6.89% p. a. bei 10 % Vol. | **nein** |

**Modell H In-Sample: nicht bestanden. P7 ist gescheitert; der Hold-out bleibt unberührt.**

| Jahr | Rendite bei 10 % Vol. | Sharpe |
|---|---|---|
| 2015 | -3.0% | -0.29 |
| 2016 | -16.1% | -1.64 |
| 2017 | +10.7% | +1.25 |
| 2018 | -3.3% | -0.28 |
| 2019 | -5.1% | -0.56 |
| 2020 | +9.3% | +0.72 |
| 2021 | +0.7% | +0.08 |
| 2022 | -17.3% | -1.63 |
| 2023 | -8.7% | -1.30 |

| Instrument | Beitrag bei 10 % Portfolio-Vol. (Summe) | Sharpe einzeln |
|---|---|---|
| NSXUSD | +5.6% | +0.29 |
| BCOUSD | +3.5% | +0.17 |
| SPXUSD | +2.8% | +0.14 |
| JPXJPY | +0.7% | +0.03 |
| HKXHKD | -1.7% | -0.09 |
| XAUUSD | -4.9% | -0.25 |
| FRXEUR | -6.5% | -0.37 |
| UKXGBP | -8.5% | -0.44 |
| AUXAUD | -10.0% | -0.56 |
| XAGUSD | -13.7% | -0.71 |

