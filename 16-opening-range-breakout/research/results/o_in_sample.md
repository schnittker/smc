# Modell O (Opening Range Breakout 5 Minuten), In-Sample 2015–2023 (Trial T56 O-NDX, T57 O-SPX)

Lauf vom 24.10.2026. Regeln laut `docs/01_Vorregistrierung.md`, Code `research/orb/`. Volle NYSE-Handelstage; Risiko 1 % je Trade, Hebel ≤ 4. Netto = nach Spread (FTMO-Durchschnitt) und Slippage (¼ Spread je Marktausführung); Tagesergebnisse in Basispunkten des Kapitals, Tage ohne Signal mit 0.

## O-NDX

| Kennzahl | Wert |
|---|---|
| Handelstage | 2,166 |
| Netto je Tag (bp des Kapitals) | -1.60 bp (σ 142.9 bp) |
| vor Kosten je Tag | +1.67 bp |
| Kosten je Tag | 3.27 bp |
| Sharpe Ratio p. a. (netto) | -0.17 |
| t-Wert iid / Woche / Monat | -0.52 / -0.54 / -0.51 |
| Trefferquote | 15% |
| Notfall-Stops | 1812 |
| bei doppelten Kosten | -4.87 bp/Tag |

| Kriterium | Ergebnis | erfüllt |
|---|---|---|
| Mittleres Netto-Tagesergebnis > 0 mit t ≥ 3,0 (kleinster aus iid / Woche / Monat) | -1.60 bp/Tag, t = -0.54 | **nein** |
| ≥ 6 von 9 Jahren positiv | 4 von 9 | **nein** |
| beide Teilzeiträume 2015–2019 und 2020–2023 positiv | +0.09 / -3.88 bp | **nein** |
| bei doppelten Kosten > 0 | -4.87 bp/Tag | **nein** |

**O-NDX: nicht bestanden.**

| Jahr | Tage | Netto Ø bp | t |
|---|---|---|---|
| 2015 | 248 | -7.23 | -0.96 |
| 2016 | 251 | +9.29 | +1.15 |
| 2017 | 245 | +10.86 | +1.72 |
| 2018 | 248 | -8.37 | -0.98 |
| 2019 | 249 | -4.06 | -0.55 |
| 2020 | 248 | -11.96 | -1.29 |
| 2021 | 251 | +0.41 | +0.04 |
| 2022 | 250 | +13.63 | +1.02 |
| 2023 | 176 | -23.47 | -1.98 |

### Trades (beschreibend)

| Teilmenge | Trades | Ø R netto | Ø R vor Kosten | Treffer | Stop / Ziel / Tagesende | Ø Risiko R (bp) | Hebel-Obergrenze |
|---|---|---|---|---|---|---|---|
| alle | 2144 | -0.105 | +0.033 | 15% | 85%/4%/11% | 11.1 | 79% |
| Long | 1064 | -0.100 | +0.027 | 16% | 83%/3%/14% | 11.7 | 78% |
| Short | 1080 | -0.110 | +0.040 | 13% | 86%/5%/9% | 10.5 | 80% |

## O-SPX

| Kennzahl | Wert |
|---|---|
| Handelstage | 2,173 |
| Netto je Tag (bp des Kapitals) | -0.41 bp (σ 124.0 bp) |
| vor Kosten je Tag | +3.75 bp |
| Kosten je Tag | 4.15 bp |
| Sharpe Ratio p. a. (netto) | -0.05 |
| t-Wert iid / Woche / Monat | -0.15 / -0.16 / -0.16 |
| Trefferquote | 14% |
| Notfall-Stops | 1763 |
| bei doppelten Kosten | -4.56 bp/Tag |

| Kriterium | Ergebnis | erfüllt |
|---|---|---|
| Mittleres Netto-Tagesergebnis > 0 mit t ≥ 3,0 (kleinster aus iid / Woche / Monat) | -0.41 bp/Tag, t = -0.16 | **nein** |
| ≥ 6 von 9 Jahren positiv | 3 von 9 | **nein** |
| beide Teilzeiträume 2015–2019 und 2020–2023 positiv | +1.74 / -3.25 bp | **nein** |
| bei doppelten Kosten > 0 | -4.56 bp/Tag | **nein** |

**O-SPX: nicht bestanden.**

| Jahr | Tage | Netto Ø bp | t |
|---|---|---|---|
| 2015 | 249 | +4.01 | +0.47 |
| 2016 | 251 | +3.39 | +0.48 |
| 2017 | 240 | -3.59 | -1.18 |
| 2018 | 248 | -0.36 | -0.05 |
| 2019 | 249 | +5.05 | +0.73 |
| 2020 | 248 | -6.95 | -0.77 |
| 2021 | 251 | -0.98 | -0.14 |
| 2022 | 250 | -2.17 | -0.20 |
| 2023 | 187 | -2.81 | -0.30 |

### Trades (beschreibend)

| Teilmenge | Trades | Ø R netto | Ø R vor Kosten | Treffer | Stop / Ziel / Tagesende | Ø Risiko R (bp) | Hebel-Obergrenze |
|---|---|---|---|---|---|---|---|
| alle | 2076 | -0.151 | +0.092 | 14% | 85%/4%/11% | 8.8 | 89% |
| Long | 1035 | -0.120 | +0.065 | 16% | 83%/3%/14% | 9.3 | 88% |
| Short | 1041 | -0.183 | +0.118 | 13% | 87%/6%/8% | 8.3 | 90% |

**Ergebnis: Keine Variante erfüllt alle In-Sample-Kriterien. Strategie Nr. 16 ist gescheitert; der Hold-out bleibt unberührt.**
