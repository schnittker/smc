# Modell J (Multi-Timeframe-Pullback), In-Sample 2015–2023 (Trial T153 J-MTF)

Lauf vom 24.10.2026. Regeln laut `docs/01_Vorregistrierung.md`, Code `research/mtf/`. 17 Instrumente; Trend D1 (Schluss gegenüber EMA50) und H4 (EMA20 gegenüber EMA50), Einstieg bei H1-Schluss zurück über/unter EMA20; Stop 10-Kerzen-Extrem ± 0,5 ATR, Ziel 2R, Zeitstopp 48 h; 0,25 % Risiko je Trade. Netto = nach Spread, Slippage, Kommission und Swaps; Ergebnis am Tag des Ausstiegs; Portfolio = Summe aller Instrumente je Tag.

## J-MTF

| Kennzahl | Wert |
|---|---|
| Handelstage / Trades | 2,342 / 16,194 |
| Netto je Tag (bp des Kapitals, Portfolio) | -14.70 bp (σ 116.1 bp) |
| vor Kosten je Tag | -5.04 bp |
| Handelskosten + Swap-Belastung je Tag (Swap netto) | 9.96 bp (-1.40 bp) |
| Rendite p. a. (netto, 0,25 % Risiko je Trade) | -38.24 % |
| Sharpe Ratio p. a. (netto) | -2.04 |
| t-Wert iid / Woche / Monat | -6.12 / -6.05 / -6.53 |
| Ø R je Trade vor / nach Kosten | -0.029 / -0.085 |
| Trefferquote / Anteil Long | 36% / 54% |
| Ausstiege Ziel / Stop / Zeit | 22% / 58% / 20% |
| Ø Haltedauer | 22.6 H1-Kerzen |
| bei doppelten Kosten | -24.65 bp/Tag |

| Kriterium | Ergebnis | erfüllt |
|---|---|---|
| Mittleres Netto-Tagesergebnis > 0 mit t ≥ 3,0 (kleinster aus iid / Woche / Monat) | -14.70 bp/Tag, t = -6.53 | **nein** |
| ≥ 6 von 9 Jahren positiv | 0 von 9 | **nein** |
| ≥ 60 % der Instrumente positiv | 2 von 17 | **nein** |
| bei doppelten Kosten > 0 | -24.65 bp/Tag | **nein** |

**J-MTF: nicht bestanden.**

| Jahr | Tage | Netto % |
|---|---|---|
| 2015 | 260 | -50.02 |
| 2016 | 260 | -33.50 |
| 2017 | 260 | -64.18 |
| 2018 | 261 | -21.13 |
| 2019 | 260 | -56.60 |
| 2020 | 261 | -16.07 |
| 2021 | 260 | -54.49 |
| 2022 | 260 | -10.10 |
| 2023 | 260 | -38.09 |

| Anlageklasse | Trades | Netto % p. a. |
|---|---|---|
| FX | 7311 | -15.74 |
| Metalle | 1959 | -5.87 |
| Indizes | 5996 | -14.57 |
| Öl | 928 | -2.06 |

| Instrument | Trades | Netto % p. a. | Ø R netto |
|---|---|---|---|
| EURUSD | 1064 | -4.23 | -0.143 |
| GBPUSD | 996 | -1.80 | -0.065 |
| USDJPY | 1025 | -1.49 | -0.052 |
| AUDUSD | 1038 | -2.61 | -0.091 |
| NZDUSD | 1063 | -1.84 | -0.062 |
| USDCAD | 1044 | -1.12 | -0.039 |
| USDCHF | 1081 | -2.65 | -0.088 |
| XAUUSD | 991 | -0.86 | -0.031 |
| US500 | 995 | -2.51 | -0.091 |
| US100 | 1006 | +0.77 | +0.027 |
| FRA40 | 689 | -2.39 | -0.125 |
| UK100 | 795 | -4.62 | -0.209 |
| JP225 | 987 | -1.92 | -0.070 |
| HK50 | 596 | +0.25 | +0.015 |
| AUS200 | 928 | -4.13 | -0.160 |
| Brent | 928 | -2.06 | -0.080 |
| Silber | 968 | -5.02 | -0.187 |

**Ergebnis: J-MTF erfüllt die In-Sample-Kriterien nicht. Strategie Nr. 45 ist gescheitert; der Hold-out bleibt unberührt.**
