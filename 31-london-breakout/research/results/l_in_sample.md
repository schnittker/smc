# Modell L (London Breakout), In-Sample 2015–2023 (Trial T106 L-GBP, T107 L-EUR)

Lauf vom 24.10.2026. Regeln laut `docs/01_Vorregistrierung.md`, Code `research/lbo/`. Asien-Range 00:00–07:00 London, Ausbruch 07:00–12:00, Stop am anderen Range-Ende, Ausstieg 16:00; Risiko 0,5 % je Trade, Hebel ≤ 10. Netto = nach Spread, Kommission und Slippage; Tagesergebnisse in bp des Kapitals, Tage ohne Ausbruch mit 0.

## L-GBP

| Kennzahl | Wert |
|---|---|
| Handelstage | 2,282 |
| Netto je Tag (bp des Kapitals) | +0.75 bp (σ 75.2 bp) |
| vor Kosten je Tag | +2.89 bp |
| Kosten je Tag | 2.14 bp |
| Sharpe Ratio p. a. (netto) | 0.16 |
| t-Wert iid / Woche / Monat | 0.48 / 0.47 / 0.47 |
| Trefferquote | 36% |
| Stops | 1172 |
| bei doppelten Kosten | -1.39 bp/Tag |

| Kriterium | Ergebnis | erfüllt |
|---|---|---|
| Mittleres Netto-Tagesergebnis > 0 mit t ≥ 3,0 (kleinster aus iid / Woche / Monat) | +0.75 bp/Tag, t = 0.47 | **nein** |
| ≥ 6 von 9 Jahren positiv | 5 von 9 | **nein** |
| beide Teilzeiträume 2015–2019 und 2020–2023 positiv | +1.29 / +0.06 bp | ja |
| bei doppelten Kosten > 0 | -1.39 bp/Tag | **nein** |

**L-GBP: nicht bestanden.**

| Jahr | Tage | Netto Ø bp | t |
|---|---|---|---|
| 2015 | 254 | -8.44 | -1.72 |
| 2016 | 255 | +6.53 | +1.40 |
| 2017 | 254 | -1.35 | -0.31 |
| 2018 | 254 | +4.67 | +0.82 |
| 2019 | 253 | +5.05 | +0.97 |
| 2020 | 254 | +5.63 | +1.24 |
| 2021 | 252 | -5.41 | -1.44 |
| 2022 | 255 | +0.02 | +0.01 |
| 2023 | 251 | -0.03 | -0.01 |

### Trades (beschreibend)

| Teilmenge | Trades | Ø R netto | Ø R vor Kosten | Treffer | Stop / Tagesende | Median Risiko R (bp) | Hebel-Obergrenze |
|---|---|---|---|---|---|---|---|
| alle | 2231 | +0.015 | +0.059 | 37% | 53%/47% | 21.9 | 0% |
| Long | 1086 | -0.056 | -0.012 | 35% | 55%/45% | 21.7 | 0% |
| Short | 1145 | +0.083 | +0.127 | 39% | 50%/50% | 22.1 | 0% |

Median der Asien-Range: 21.8 bp; Tage mit Ausbruch: 2231 von 2282.

## L-EUR

| Kennzahl | Wert |
|---|---|
| Handelstage | 2,284 |
| Netto je Tag (bp des Kapitals) | -1.46 bp (σ 68.7 bp) |
| vor Kosten je Tag | +1.06 bp |
| Kosten je Tag | 2.52 bp |
| Sharpe Ratio p. a. (netto) | -0.34 |
| t-Wert iid / Woche / Monat | -1.01 / -1.01 / -0.94 |
| Trefferquote | 38% |
| Stops | 1124 |
| bei doppelten Kosten | -3.98 bp/Tag |

| Kriterium | Ergebnis | erfüllt |
|---|---|---|
| Mittleres Netto-Tagesergebnis > 0 mit t ≥ 3,0 (kleinster aus iid / Woche / Monat) | -1.46 bp/Tag, t = -1.01 | **nein** |
| ≥ 6 von 9 Jahren positiv | 4 von 9 | **nein** |
| beide Teilzeiträume 2015–2019 und 2020–2023 positiv | -2.82 / +0.25 bp | **nein** |
| bei doppelten Kosten > 0 | -3.98 bp/Tag | **nein** |

**L-EUR: nicht bestanden.**

| Jahr | Tage | Netto Ø bp | t |
|---|---|---|---|
| 2015 | 254 | +5.17 | +0.97 |
| 2016 | 255 | +2.85 | +0.68 |
| 2017 | 254 | -2.78 | -0.68 |
| 2018 | 254 | -4.67 | -1.18 |
| 2019 | 253 | -14.74 | -4.04 |
| 2020 | 254 | +1.30 | +0.30 |
| 2021 | 252 | +0.86 | +0.21 |
| 2022 | 255 | -0.48 | -0.13 |
| 2023 | 253 | -0.68 | -0.13 |

### Trades (beschreibend)

| Teilmenge | Trades | Ø R netto | Ø R vor Kosten | Treffer | Stop / Tagesende | Median Risiko R (bp) | Hebel-Obergrenze |
|---|---|---|---|---|---|---|---|
| alle | 2215 | -0.030 | +0.022 | 39% | 51%/49% | 20.4 | 0% |
| Long | 1122 | -0.098 | -0.047 | 37% | 51%/49% | 20.7 | 0% |
| Short | 1093 | +0.040 | +0.092 | 40% | 50%/50% | 20.1 | 0% |

Median der Asien-Range: 20.3 bp; Tage mit Ausbruch: 2215 von 2284.

**Ergebnis: Keine Variante erfüllt alle In-Sample-Kriterien. Strategie Nr. 31 ist gescheitert; der Hold-out bleibt unberührt.**
