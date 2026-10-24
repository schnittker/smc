# Modell A (Asien-Range-Fade), In-Sample 2015–2023 (Trial T110 A-EURCHF, T111 A-AUDCAD)

Lauf vom 24.10.2026. Regeln laut `docs/01_Vorregistrierung.md`, Code `research/arf/`. Fade von M5-Bollinger-Ausschlägen 00:00–06:00 London, Ausstieg an der Mitte, Stop = Bandbreite; Risiko 0,25 % je Trade, Hebel ≤ 10. Netto = nach Spread, Kommission und Slippage; Ergebnisse je Nacht in bp des Kapitals, Nächte ohne Trade mit 0.

## A-EURCHF

| Kennzahl | Wert |
|---|---|
| Nächte | 2,289 |
| Netto je Tag (bp des Kapitals) | -14.12 bp (σ 28.9 bp) |
| vor Kosten je Tag | +9.08 bp |
| Kosten je Tag | 23.20 bp |
| Sharpe Ratio p. a. (netto) | -7.79 |
| t-Wert iid / Woche / Monat | -23.38 / -19.89 / -13.82 |
| Trefferquote | 34% |
| Nächte mit mindestens einem Stop | 1000 |
| bei doppelten Kosten | -37.32 bp/Tag |

| Kriterium | Ergebnis | erfüllt |
|---|---|---|
| Mittleres Netto-Tagesergebnis > 0 mit t ≥ 3,0 (kleinster aus iid / Woche / Monat) | -14.12 bp/Tag, t = -23.38 | **nein** |
| ≥ 6 von 9 Jahren positiv | 0 von 9 | **nein** |
| beide Teilzeiträume 2015–2019 und 2020–2023 positiv | -12.95 / -15.57 bp | **nein** |
| bei doppelten Kosten > 0 | -37.32 bp/Tag | **nein** |

**A-EURCHF: nicht bestanden.**

| Jahr | Tage | Netto Ø bp | t |
|---|---|---|---|
| 2015 | 254 | -3.05 | -1.71 |
| 2016 | 255 | -3.94 | -2.38 |
| 2017 | 254 | -17.91 | -10.41 |
| 2018 | 254 | -13.89 | -8.00 |
| 2019 | 253 | -26.05 | -13.46 |
| 2020 | 255 | -18.84 | -10.67 |
| 2021 | 254 | -20.30 | -11.22 |
| 2022 | 255 | -5.56 | -3.38 |
| 2023 | 255 | -17.60 | -10.51 |

### Trades (beschreibend)

| Teilmenge | Trades | Ø R netto | Ø R vor Kosten | Treffer | Stops |
|---|---|---|---|---|---|
| alle | 6902 | -0.208 | +0.123 | 49% | 18% |
| Long | 3113 | -0.178 | +0.148 | 52% | 17% |
| Short | 3789 | -0.232 | +0.103 | 47% | 18% |

## A-AUDCAD

| Kennzahl | Wert |
|---|---|
| Nächte | 2,289 |
| Netto je Tag (bp des Kapitals) | -11.80 bp (σ 31.0 bp) |
| vor Kosten je Tag | +4.02 bp |
| Kosten je Tag | 15.82 bp |
| Sharpe Ratio p. a. (netto) | -6.07 |
| t-Wert iid / Woche / Monat | -18.20 / -17.50 / -15.09 |
| Trefferquote | 36% |
| Nächte mit mindestens einem Stop | 1286 |
| bei doppelten Kosten | -27.62 bp/Tag |

| Kriterium | Ergebnis | erfüllt |
|---|---|---|
| Mittleres Netto-Tagesergebnis > 0 mit t ≥ 3,0 (kleinster aus iid / Woche / Monat) | -11.80 bp/Tag, t = -18.20 | **nein** |
| ≥ 6 von 9 Jahren positiv | 0 von 9 | **nein** |
| beide Teilzeiträume 2015–2019 und 2020–2023 positiv | -10.09 / -13.94 bp | **nein** |
| bei doppelten Kosten > 0 | -27.62 bp/Tag | **nein** |

**A-AUDCAD: nicht bestanden.**

| Jahr | Tage | Netto Ø bp | t |
|---|---|---|---|
| 2015 | 254 | -7.79 | -3.71 |
| 2016 | 255 | -3.04 | -1.61 |
| 2017 | 254 | -11.84 | -6.14 |
| 2018 | 254 | -9.99 | -5.64 |
| 2019 | 253 | -17.83 | -9.20 |
| 2020 | 255 | -7.66 | -4.34 |
| 2021 | 254 | -17.84 | -9.48 |
| 2022 | 255 | -12.75 | -6.42 |
| 2023 | 255 | -17.50 | -8.61 |

### Trades (beschreibend)

| Teilmenge | Trades | Ø R netto | Ø R vor Kosten | Treffer | Stops |
|---|---|---|---|---|---|
| alle | 7523 | -0.144 | +0.049 | 54% | 22% |
| Long | 3696 | -0.152 | +0.041 | 54% | 23% |
| Short | 3827 | -0.136 | +0.056 | 54% | 21% |

**Ergebnis: Keine Variante erfüllt alle In-Sample-Kriterien. Strategie Nr. 32 ist gescheitert; der Hold-out bleibt unberührt.**
