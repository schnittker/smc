# Modell Q (Gap-Fade), In-Sample 2015–2023 (Trial T138 Q-IDX, T139 Q-FXW)

Lauf vom 24.10.2026. Regeln laut `docs/01_Vorregistrierung.md`, Code `research/gap/`. Fade des Gaps zur Kassa-Eröffnung (US500, US100, FRA40, UK100) bzw. zur Montagseröffnung 01:00 Server (7 Majors); Ziel Vorschluss, Stop eine Gapgröße weiter, Zeitausstieg zum Sitzungs- bzw. Tagesende; 0,25 % Risiko je Trade. Netto = nach Spread, Slippage und Kommission; Portfolio = Summe je Tag.

## Q-IDX

| Kennzahl | Wert |
|---|---|
| Handelstage / Trades | 2,250 / 6,069 |
| Netto je Tag (bp des Kapitals, Portfolio) | -3.15 bp (σ 45.1 bp) |
| vor Kosten je Tag | +1.13 bp |
| Kosten je Tag | 4.28 bp |
| Rendite p. a. (netto, 0,25 % Risiko je Trade) | -7.87 % |
| Sharpe Ratio p. a. (netto) | -1.10 |
| t-Wert iid / Woche / Monat | -3.31 / -3.37 / -3.61 |
| Ø R je Trade vor / nach Kosten | +0.017 / -0.047 |
| Trefferquote | 49% |
| Ausstiege Ziel / Stop / Zeit | 43% / 43% / 14% |
| bei doppelten Kosten | -7.43 bp/Tag |

| Kriterium | Ergebnis | erfüllt |
|---|---|---|
| Mittleres Netto-Tagesergebnis > 0 mit t ≥ 3,0 (kleinster aus iid / Woche / Monat) | -3.15 bp/Tag, t = -3.61 | **nein** |
| ≥ 6 von 9 Jahren positiv | 0 von 9 | **nein** |
| ≥ 60 % der Instrumente positiv | 1 von 4 | **nein** |
| bei doppelten Kosten > 0 | -7.43 bp/Tag | **nein** |

**Q-IDX: nicht bestanden.**

| Jahr | Tage | Netto % |
|---|---|---|
| 2015 | 253 | -1.03 |
| 2016 | 254 | -15.25 |
| 2017 | 249 | -10.99 |
| 2018 | 253 | -8.26 |
| 2019 | 253 | -11.10 |
| 2020 | 254 | -0.88 |
| 2021 | 253 | -5.29 |
| 2022 | 254 | -1.39 |
| 2023 | 227 | -16.62 |

| Gap-Größe (Terzil) | Trades | Füllquote | Ø R vor Kosten | Ø R netto |
|---|---|---|---|---|
| klein (0–25 bp) | 2023 | 48% | +0.023 | -0.087 |
| mittel (25–48 bp) | 2023 | 47% | +0.062 | +0.011 |
| groß (≥ 48 bp) | 2023 | 33% | -0.035 | -0.064 |

| Instrument | Trades | Netto % p. a. | Ø R netto |
|---|---|---|---|
| US500 | 1502 | -0.32 | -0.008 |
| US100 | 1458 | +0.13 | +0.003 |
| FRA40 | 1558 | -4.92 | -0.114 |
| UK100 | 1551 | -2.76 | -0.064 |

## Q-FXW

| Kennzahl | Wert |
|---|---|
| Handelstage / Trades | 453 / 1,042 |
| Netto je Tag (bp des Kapitals, Portfolio) | +11.88 bp (σ 43.0 bp) |
| vor Kosten je Tag | +17.92 bp |
| Kosten je Tag | 6.04 bp |
| Rendite p. a. (netto, 0,25 % Risiko je Trade) | +5.98 % |
| Sharpe Ratio p. a. (netto) | 1.96 |
| t-Wert iid / Woche / Monat | 5.88 / 5.88 / 5.08 |
| Ø R je Trade vor / nach Kosten | +0.312 / +0.207 |
| Trefferquote | 67% |
| Ausstiege Ziel / Stop / Zeit | 64% / 31% / 4% |
| bei doppelten Kosten | +5.84 bp/Tag |

| Kriterium | Ergebnis | erfüllt |
|---|---|---|
| Mittleres Netto-Tagesergebnis > 0 mit t ≥ 3,0 (kleinster aus iid / Woche / Monat) | +11.88 bp/Tag, t = 5.08 | ja |
| ≥ 6 von 9 Jahren positiv | 9 von 9 | ja |
| ≥ 60 % der Instrumente positiv | 7 von 7 | ja |
| bei doppelten Kosten > 0 | +5.84 bp/Tag | ja |

**Q-FXW: alle Kriterien erfüllt.**

| Jahr | Tage | Netto % |
|---|---|---|
| 2015 | 51 | +7.65 |
| 2016 | 50 | +7.24 |
| 2017 | 50 | +8.21 |
| 2018 | 50 | +10.02 |
| 2019 | 50 | +3.02 |
| 2020 | 51 | +2.07 |
| 2021 | 50 | +4.75 |
| 2022 | 51 | +5.56 |
| 2023 | 50 | +5.30 |

| Gap-Größe (Terzil) | Trades | Füllquote | Ø R vor Kosten | Ø R netto |
|---|---|---|---|---|
| klein (0–14 bp) | 347 | 73% | +0.416 | +0.269 |
| mittel (14–22 bp) | 347 | 66% | +0.296 | +0.186 |
| groß (≥ 22 bp) | 348 | 55% | +0.224 | +0.164 |

| Instrument | Trades | Netto % p. a. | Ø R netto |
|---|---|---|---|
| EURUSD | 120 | +0.48 | +0.144 |
| GBPUSD | 137 | +0.55 | +0.145 |
| USDJPY | 155 | +1.16 | +0.270 |
| AUDUSD | 184 | +1.39 | +0.273 |
| NZDUSD | 208 | +0.92 | +0.160 |
| USDCAD | 117 | +0.66 | +0.204 |
| USDCHF | 121 | +0.81 | +0.240 |

**Ergebnis:** bestanden: Q-FXW; Hold-out je bestandener Variante.
