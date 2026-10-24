# Modell U (H1-Mean-Reversion), In-Sample 2015–2023 (Trial T129 U-BB, T130 U-OU)

Lauf vom 24.10.2026. Regeln laut `docs/01_Vorregistrierung.md`, Code `research/hmr/`. 17 FX-Crosses, H1-Serverkerzen; Einstieg zur nächsten Eröffnung, Stop 2 ATR14, Ausstieg an der Mittellinie oder nach 48 Kerzen; 0,25 % Risiko je Trade. Netto = nach Spread, Slippage, Kommission und Swaps; Ergebnis eines Trades am Tag des Ausstiegs; Portfolio = Summe aller Paare je Tag.

## U-BB

| Kennzahl | Wert |
|---|---|
| Handelstage / Trades | 2,340 / 20,069 |
| Netto je Tag (bp des Kapitals, Portfolio) | -11.12 bp (σ 86.9 bp) |
| vor Kosten je Tag | +2.24 bp |
| Handelskosten + Swap-Belastung je Tag (Swap netto) | 13.53 bp (-0.91 bp) |
| Rendite p. a. (netto, 0,25 % Risiko je Trade) | -28.92 % |
| Sharpe Ratio p. a. (netto) | -2.06 |
| t-Wert iid / Woche / Monat | -6.19 / -6.18 / -5.62 |
| Ø R je Trade vor / nach Kosten | +0.010 / -0.052 |
| Trefferquote / Stops / Zeitstopps / Long | 54% / 42% / 0% / 49% |
| Ø Haltedauer | 7.6 H1-Kerzen |
| bei doppelten Kosten | -24.65 bp/Tag |

| Kriterium | Ergebnis | erfüllt |
|---|---|---|
| Mittleres Netto-Tagesergebnis > 0 mit t ≥ 3,0 (kleinster aus iid / Woche / Monat) | -11.12 bp/Tag, t = -6.19 | **nein** |
| ≥ 6 von 9 Jahren positiv | 1 von 9 | **nein** |
| ≥ 60 % der Paare positiv | 1 von 17 | **nein** |
| bei doppelten Kosten > 0 | -24.65 bp/Tag | **nein** |

**U-BB: nicht bestanden.**

| Jahr | Tage | Netto % |
|---|---|---|
| 2015 | 260 | +1.68 |
| 2016 | 260 | -18.21 |
| 2017 | 259 | -26.84 |
| 2018 | 260 | -19.77 |
| 2019 | 260 | -19.98 |
| 2020 | 261 | -57.47 |
| 2021 | 260 | -44.43 |
| 2022 | 260 | -25.90 |
| 2023 | 260 | -49.34 |

| Paar | Trades | Netto % p. a. | Ø R netto |
|---|---|---|---|
| EURJPY | 1085 | -3.75 | -0.124 |
| GBPJPY | 1153 | -2.38 | -0.074 |
| AUDJPY | 1119 | -3.25 | -0.104 |
| NZDJPY | 1142 | -3.23 | -0.102 |
| CADJPY | 1076 | -2.52 | -0.084 |
| CHFJPY | 1239 | -1.67 | -0.048 |
| EURCAD | 1182 | -1.83 | -0.056 |
| EURCHF | 1369 | -0.46 | -0.013 |
| EURNZD | 1175 | -1.62 | -0.050 |
| EURAUD | 1158 | -1.35 | -0.042 |
| GBPCHF | 1241 | -1.95 | -0.056 |
| GBPNZD | 1215 | -1.22 | -0.036 |
| GBPCAD | 1181 | -0.89 | -0.027 |
| GBPAUD | 1158 | -0.59 | -0.018 |
| AUDNZD | 1147 | -1.84 | -0.058 |
| AUDCAD | 1207 | -0.62 | -0.019 |
| CADCHF | 1222 | +0.23 | +0.007 |

## U-OU

| Kennzahl | Wert |
|---|---|
| Handelstage / Trades | 2,340 / 1,799 |
| Netto je Tag (bp des Kapitals, Portfolio) | -1.81 bp (σ 31.9 bp) |
| vor Kosten je Tag | -0.49 bp |
| Handelskosten + Swap-Belastung je Tag (Swap netto) | 1.35 bp (-0.22 bp) |
| Rendite p. a. (netto, 0,25 % Risiko je Trade) | -4.70 % |
| Sharpe Ratio p. a. (netto) | -0.91 |
| t-Wert iid / Woche / Monat | -2.74 / -2.81 / -2.84 |
| Ø R je Trade vor / nach Kosten | -0.026 / -0.094 |
| Trefferquote / Stops / Zeitstopps / Long | 37% / 60% / 8% / 49% |
| Ø Haltedauer | 19.1 H1-Kerzen |
| bei doppelten Kosten | -3.16 bp/Tag |

| Kriterium | Ergebnis | erfüllt |
|---|---|---|
| Mittleres Netto-Tagesergebnis > 0 mit t ≥ 3,0 (kleinster aus iid / Woche / Monat) | -1.81 bp/Tag, t = -2.84 | **nein** |
| ≥ 6 von 9 Jahren positiv | 1 von 9 | **nein** |
| ≥ 60 % der Paare positiv | 4 von 17 | **nein** |
| bei doppelten Kosten > 0 | -3.16 bp/Tag | **nein** |

**U-OU: nicht bestanden.**

| Jahr | Tage | Netto % |
|---|---|---|
| 2015 | 260 | -5.26 |
| 2016 | 260 | -8.77 |
| 2017 | 259 | -7.01 |
| 2018 | 260 | -1.16 |
| 2019 | 260 | -1.32 |
| 2020 | 261 | -9.39 |
| 2021 | 260 | -10.30 |
| 2022 | 260 | -2.36 |
| 2023 | 260 | +3.26 |

| Paar | Trades | Netto % p. a. | Ø R netto |
|---|---|---|---|
| EURJPY | 64 | -0.28 | -0.156 |
| GBPJPY | 55 | -0.32 | -0.206 |
| AUDJPY | 92 | -0.51 | -0.198 |
| NZDJPY | 77 | -1.08 | -0.506 |
| CADJPY | 83 | -0.25 | -0.108 |
| CHFJPY | 115 | -0.45 | -0.141 |
| EURCAD | 120 | -0.27 | -0.080 |
| EURCHF | 201 | -0.43 | -0.077 |
| EURNZD | 115 | -0.80 | -0.252 |
| EURAUD | 117 | -0.13 | -0.040 |
| GBPCHF | 102 | +0.15 | +0.053 |
| GBPNZD | 126 | +0.52 | +0.148 |
| GBPCAD | 104 | -0.49 | -0.170 |
| GBPAUD | 88 | +0.11 | +0.043 |
| AUDNZD | 86 | -0.57 | -0.239 |
| AUDCAD | 116 | -0.07 | -0.021 |
| CADCHF | 138 | +0.16 | +0.042 |

**Ergebnis: Keine Variante erfüllt alle In-Sample-Kriterien. Strategien Nr. 37 und 39 sind gescheitert; der Hold-out bleibt unberührt.**
