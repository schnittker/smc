# Modell W (Hurst-Regime-Switch), In-Sample 2015–2023 (Trial T135 W-HURST)

Lauf vom 24.10.2026. Regeln laut `docs/01_Vorregistrierung.md`, Code `research/hrs/`. 17 Instrumente, H4-Serverkerzen; H > 0,55 Keltner-Ausbruch, H < 0,45 Bollinger-Fade; Stop 2 ATR14; 0,25 % Risiko je Trade. Netto = nach Spread, Slippage, Kommission und Swaps; Ergebnis eines Trades am Tag des Ausstiegs; Portfolio = Summe aller Instrumente je Tag.

## W-HURST

| Kennzahl | Wert |
|---|---|
| Handelstage / Trades | 2,342 / 1,942 |
| Netto je Tag (bp des Kapitals, Portfolio) | -2.27 bp (σ 23.9 bp) |
| vor Kosten je Tag | -1.51 bp |
| Handelskosten + Swap-Belastung je Tag (Swap netto) | 0.80 bp (-0.21 bp) |
| Rendite p. a. (netto, 0,25 % Risiko je Trade) | -5.91 % |
| Sharpe Ratio p. a. (netto) | -1.53 |
| t-Wert iid / Woche / Monat | -4.60 / -4.70 / -4.29 |
| Ø R je Trade vor / nach Kosten | -0.073 / -0.110 |
| Trefferquote / Anteil Stops / Anteil Long | 44% / 41% / 51% |
| Ø Haltedauer | 7.9 H4-Kerzen |
| Trades Trend / Umkehr | 98 / 1,844 |
| bei doppelten Kosten | -3.07 bp/Tag |

| Kriterium | Ergebnis | erfüllt |
|---|---|---|
| Mittleres Netto-Tagesergebnis > 0 mit t ≥ 3,0 (kleinster aus iid / Woche / Monat) | -2.27 bp/Tag, t = -4.70 | **nein** |
| ≥ 6 von 9 Jahren positiv | 1 von 9 | **nein** |
| ≥ 60 % der Instrumente positiv | 1 von 17 | **nein** |
| bei doppelten Kosten > 0 | -3.07 bp/Tag | **nein** |

**W-HURST: nicht bestanden.**

| Jahr | Tage | Netto % |
|---|---|---|
| 2015 | 260 | -9.35 |
| 2016 | 260 | -4.15 |
| 2017 | 260 | -1.56 |
| 2018 | 261 | -9.83 |
| 2019 | 260 | -12.68 |
| 2020 | 261 | -1.28 |
| 2021 | 260 | +0.84 |
| 2022 | 260 | -8.84 |
| 2023 | 260 | -6.33 |

| Anlageklasse | Trades | Netto % p. a. |
|---|---|---|
| FX | 713 | -2.16 |
| Metalle | 177 | -1.40 |
| Indizes | 960 | -2.15 |
| Öl | 92 | -0.19 |

| Instrument | Trades | Netto % p. a. | Ø R netto |
|---|---|---|---|
| EURUSD | 122 | -0.11 | -0.034 |
| GBPUSD | 84 | -0.65 | -0.279 |
| USDJPY | 65 | -0.46 | -0.254 |
| AUDUSD | 114 | -0.21 | -0.066 |
| NZDUSD | 107 | -0.10 | -0.033 |
| USDCAD | 124 | -0.18 | -0.051 |
| USDCHF | 97 | -0.45 | -0.169 |
| XAUUSD | 84 | -0.71 | -0.304 |
| US500 | 193 | -0.06 | -0.011 |
| US100 | 130 | -0.07 | -0.019 |
| FRA40 | 131 | -0.51 | -0.141 |
| UK100 | 125 | -0.67 | -0.192 |
| JP225 | 98 | -0.55 | -0.201 |
| HK50 | 62 | +0.02 | +0.010 |
| AUS200 | 221 | -0.32 | -0.051 |
| Brent | 92 | -0.19 | -0.075 |
| Silber | 93 | -0.69 | -0.267 |

| Regime | Ø R vor Kosten | Ø R netto |
|---|---|---|
| Trend (H > 0,55) | -0.077 | -0.123 |
| Umkehr (H < 0,45) | -0.072 | -0.109 |

## Beschreibend: Verteilung von H (H4-Kerzen 2015–2023, alle Instrumente)

| Anteil H > 0,55 (Trend) | Anteil H < 0,45 (Umkehr) | Quantile 5 / 25 / 50 / 75 / 95 % |
|---|---|---|
| 1.3% | 14.6% | 0.427 / 0.464 / 0.486 / 0.507 / 0.534 |

## Beschreibend: Bausteine ohne Filter

| Regel | Trades | Netto bp/Tag | vor Kosten bp/Tag | Ø R vor Kosten / netto | t | Jahre positiv |
|---|---|---|---|---|---|---|
| W-TREND | 5,594 | -1.38 | +1.30 | +0.022 / -0.023 | -0.86 | 3 von 9 |
| W-MR | 11,576 | -7.35 | -2.80 | -0.023 / -0.059 | -4.79 | 0 von 9 |

**Ergebnis: W-HURST erfüllt die In-Sample-Kriterien nicht. Strategie Nr. 40 ist gescheitert; der Hold-out bleibt unberührt.**
