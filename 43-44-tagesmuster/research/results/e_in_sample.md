# Modell E (Tagesmuster), In-Sample 2015–2023 (Trial T144 E-REV, T145 E-CONT, T146 E-WD)

Lauf vom 24.10.2026. Regeln laut `docs/01_Vorregistrierung.md`, Code `research/dpat/`. 17 Instrumente, Servertage; Position von der Eröffnung bis zum Schluss des Servertags, Nominal 0,5 % je ATR14. Netto = nach Spread, Slippage und Kommission; Ergebnisse in bp bzw. % des Kapitals, Portfolio = Summe aller Instrumente je Tag.

## E-REV

| Kennzahl | Wert |
|---|---|
| Handelstage / Trades | 2,291 / 402 |
| Netto je Tag (bp des Kapitals, Portfolio) | -0.30 bp (σ 31.1 bp) |
| vor Kosten je Tag | -0.12 bp |
| Kosten je Tag | 0.18 bp |
| Rendite p. a. (netto, 0,5 % je ATR) | -0.76 % |
| Sharpe Ratio p. a. (netto) | -0.15 |
| t-Wert iid / Woche / Monat | -0.46 / -0.54 / -0.48 |
| Ø Ergebnis je Trade in ATR vor / nach Kosten | -0.014 / -0.034 |
| Trefferquote | 51% |
| bei doppelten Kosten | -0.48 bp/Tag |

| Kriterium | Ergebnis | erfüllt |
|---|---|---|
| Mittleres Netto-Tagesergebnis > 0 mit t ≥ 3,0 (kleinster aus iid / Woche / Monat) | -0.30 bp/Tag, t = -0.54 | **nein** |
| ≥ 6 von 9 Jahren positiv | 2 von 9 | **nein** |
| ≥ 60 % der Instrumente positiv | 5 von 17 | **nein** |
| bei doppelten Kosten > 0 | -0.48 bp/Tag | **nein** |

**E-REV: nicht bestanden.**

| Jahr | Tage | Netto % |
|---|---|---|
| 2015 | 254 | -4.66 |
| 2016 | 255 | -2.99 |
| 2017 | 255 | -1.21 |
| 2018 | 254 | -0.34 |
| 2019 | 254 | -2.59 |
| 2020 | 255 | +4.84 |
| 2021 | 254 | +3.03 |
| 2022 | 255 | -2.03 |
| 2023 | 255 | -0.90 |

| Instrument | Trades | Netto % p. a. | Ø ATR netto |
|---|---|---|---|
| EURUSD | 15 | -0.25 | -0.299 |
| GBPUSD | 27 | -0.40 | -0.264 |
| USDJPY | 30 | +0.36 | +0.215 |
| AUDUSD | 7 | +0.01 | +0.018 |
| NZDUSD | 12 | -0.24 | -0.356 |
| USDCAD | 12 | -0.14 | -0.209 |
| USDCHF | 17 | -0.19 | -0.200 |
| XAUUSD | 18 | -0.15 | -0.152 |
| US500 | 28 | -0.01 | -0.009 |
| US100 | 31 | -0.09 | -0.055 |
| FRA40 | 32 | -0.07 | -0.038 |
| UK100 | 31 | +0.34 | +0.195 |
| JP225 | 24 | +0.31 | +0.234 |
| HK50 | 29 | -0.14 | -0.087 |
| AUS200 | 31 | +0.43 | +0.253 |
| Brent | 25 | -0.20 | -0.144 |
| Silber | 33 | -0.33 | -0.179 |

## E-CONT

| Kennzahl | Wert |
|---|---|
| Handelstage / Trades | 2,291 / 402 |
| Netto je Tag (bp des Kapitals, Portfolio) | -0.06 bp (σ 31.1 bp) |
| vor Kosten je Tag | +0.12 bp |
| Kosten je Tag | 0.18 bp |
| Rendite p. a. (netto, 0,5 % je ATR) | -0.15 % |
| Sharpe Ratio p. a. (netto) | -0.03 |
| t-Wert iid / Woche / Monat | -0.09 / -0.11 / -0.10 |
| Ø Ergebnis je Trade in ATR vor / nach Kosten | +0.014 / -0.007 |
| Trefferquote | 48% |
| bei doppelten Kosten | -0.24 bp/Tag |

| Kriterium | Ergebnis | erfüllt |
|---|---|---|
| Mittleres Netto-Tagesergebnis > 0 mit t ≥ 3,0 (kleinster aus iid / Woche / Monat) | -0.06 bp/Tag, t = -0.11 | **nein** |
| ≥ 6 von 9 Jahren positiv | 6 von 9 | ja |
| ≥ 60 % der Instrumente positiv | 10 von 17 | **nein** |
| bei doppelten Kosten > 0 | -0.24 bp/Tag | **nein** |

**E-CONT: nicht bestanden.**

| Jahr | Tage | Netto % |
|---|---|---|
| 2015 | 254 | +3.91 |
| 2016 | 255 | +2.21 |
| 2017 | 255 | +0.01 |
| 2018 | 254 | -0.59 |
| 2019 | 254 | +1.30 |
| 2020 | 255 | -6.20 |
| 2021 | 254 | -3.85 |
| 2022 | 255 | +1.57 |
| 2023 | 255 | +0.24 |

| Instrument | Trades | Netto % p. a. | Ø ATR netto |
|---|---|---|---|
| EURUSD | 15 | +0.23 | +0.273 |
| GBPUSD | 27 | +0.36 | +0.243 |
| USDJPY | 30 | -0.41 | -0.245 |
| AUDUSD | 7 | -0.02 | -0.049 |
| NZDUSD | 12 | +0.21 | +0.315 |
| USDCAD | 12 | +0.12 | +0.177 |
| USDCHF | 17 | +0.16 | +0.169 |
| XAUUSD | 18 | +0.12 | +0.124 |
| US500 | 28 | -0.01 | -0.008 |
| US100 | 31 | +0.07 | +0.042 |
| FRA40 | 32 | -0.03 | -0.017 |
| UK100 | 31 | -0.38 | -0.223 |
| JP225 | 24 | -0.35 | -0.262 |
| HK50 | 29 | +0.07 | +0.044 |
| AUS200 | 31 | -0.49 | -0.287 |
| Brent | 25 | +0.08 | +0.058 |
| Silber | 33 | +0.12 | +0.063 |

## E-WD

| Kennzahl | Wert |
|---|---|
| Handelstage / Trades | 2,291 / 3,100 |
| Netto je Tag (bp des Kapitals, Portfolio) | +0.52 bp (σ 49.5 bp) |
| vor Kosten je Tag | +1.68 bp |
| Kosten je Tag | 1.16 bp |
| Rendite p. a. (netto, 0,5 % je ATR) | +1.32 % |
| Sharpe Ratio p. a. (netto) | 0.17 |
| t-Wert iid / Woche / Monat | 0.50 / 0.53 / 0.56 |
| Ø Ergebnis je Trade in ATR vor / nach Kosten | +0.025 / +0.008 |
| Trefferquote | 51% |
| bei doppelten Kosten | -0.64 bp/Tag |

| Kriterium | Ergebnis | erfüllt |
|---|---|---|
| Mittleres Netto-Tagesergebnis > 0 mit t ≥ 3,0 (kleinster aus iid / Woche / Monat) | +0.52 bp/Tag, t = 0.50 | **nein** |
| ≥ 6 von 9 Jahren positiv | 6 von 9 | ja |
| ≥ 60 % der Instrumente positiv | 7 von 17 | **nein** |
| bei doppelten Kosten > 0 | -0.64 bp/Tag | **nein** |

**E-WD: nicht bestanden.**

| Jahr | Tage | Netto % |
|---|---|---|
| 2015 | 254 | -5.58 |
| 2016 | 255 | +14.77 |
| 2017 | 255 | -19.85 |
| 2018 | 254 | -1.29 |
| 2019 | 254 | +1.65 |
| 2020 | 255 | +7.70 |
| 2021 | 254 | +2.15 |
| 2022 | 255 | +10.92 |
| 2023 | 255 | +1.41 |

| Instrument | Trades | Netto % p. a. | Ø ATR netto |
|---|---|---|---|
| EURUSD | 204 | -0.30 | -0.027 |
| GBPUSD | 357 | +1.13 | +0.057 |
| USDJPY | 51 | +0.36 | +0.128 |
| AUDUSD | 204 | +0.34 | +0.030 |
| NZDUSD | 204 | -0.05 | -0.004 |
| USDCAD | 255 | -0.50 | -0.035 |
| USDCHF | 305 | +1.05 | +0.062 |
| XAUUSD | 101 | -0.02 | -0.004 |
| US500 | 306 | +0.35 | +0.020 |
| US100 | 357 | +0.20 | +0.010 |
| FRA40 | 0 | +0.00 | +nan |
| UK100 | 248 | -0.42 | -0.030 |
| JP225 | 51 | -0.33 | -0.115 |
| HK50 | 0 | +0.00 | +nan |
| AUS200 | 153 | +0.35 | +0.042 |
| Brent | 304 | -0.84 | -0.050 |
| Silber | 0 | +0.00 | +nan |

## Beschreibend: E-WD gewählte Wochentage (− = kein |t| ≥ 2)

| Instrument | 2015 | 2016 | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 |
|---|---|---|---|---|---|---|---|---|---|
| EURUSD | − | Fr S | Fr S | − | − | − | Mo L | Mo L | − |
| GBPUSD | − | Fr S | Fr S | Fr S | Fr S | Fr S | − | Fr S | Fr S |
| USDJPY | − | − | − | − | − | − | − | − | Mo L |
| AUDUSD | − | − | Fr S | − | − | − | Mo L | Mo L | Mo L |
| NZDUSD | − | − | Fr S | − | − | − | Mo L | Mo L | Mo L |
| USDCAD | − | Fr L | Fr L | − | Mo L | Mo L | − | − | Mo L |
| USDCHF | − | − | − | Mo L | Mo L | Mo L | Mo L | Mo L | Mo L |
| XAUUSD | − | − | − | − | Fr L | − | Fr L | − | − |
| US500 | − | − | − | Mi L | Mi L | Mi L | Mi L | Mi L | Mi L |
| US100 | Di L | − | − | Mi L | Mi L | Mi L | Mi L | Mi L | Mi L |
| FRA40 | − | − | − | − | − | − | − | − | − |
| UK100 | − | − | Mo S | Mi L | Mo S | − | − | Mi L | Mi L |
| JP225 | − | − | − | − | − | − | Di L | − | − |
| HK50 | − | − | − | − | − | − | − | − | − |
| AUS200 | − | − | − | − | Mi L | Mi L | − | − | Mi L |
| Brent | Di S | Mo S | Mo S | Mo S | Mo S | Mo S | − | − | − |
| Silber | − | − | − | − | − | − | − | − | − |

**Ergebnis: Keine Variante erfüllt alle In-Sample-Kriterien. Strategien Nr. 43 und 44 sind gescheitert; der Hold-out bleibt unberührt.**
