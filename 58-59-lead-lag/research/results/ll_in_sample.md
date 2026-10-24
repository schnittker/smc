# Modell LL (Lead-Lag), In-Sample 2015–2023 (Trial T210 LL-AJ, T211 LL-Y1, T212 LL-Y20)

Lauf vom 24.10.2026. Regeln laut `docs/01_Vorregistrierung.md`, Code `research/ll/`. LL-AJ: AUDJPY 3 h in Richtung einer US500-H1-Bewegung > 1,5σ (Stop 2 ATR, 0,25 % Risiko); LL-Y1/LL-Y20: USDJPY in Richtung der Vortagesänderung bzw. 20-Tage-Änderung der 10-jährigen US-Rendite (10 %/σ, Tagesbuchhaltung Modell G). Netto = nach allen Kosten und Swaps.

## LL-AJ

| Kennzahl | Wert |
|---|---|
| Werktage / Trades bzw. Positionswechsel | 2,347 / 3,437 |
| Netto je Tag (bp des Kapitals) | -1.45 bp (σ 18.1 bp) |
| Kosten je Tag | 2.00 bp |
| Rendite p. a. (netto) | -3.77 % |
| Sharpe Ratio p. a. (netto) | -1.29 |
| t-Wert iid / Woche / Monat | -3.88 / -4.33 / -4.28 |
| Ø R je Trade vor / nach Kosten | +0.015 / -0.039 |
| bei doppelten Kosten | -3.45 bp/Tag |

| Kriterium | Ergebnis | erfüllt |
|---|---|---|
| Mittleres Netto-Tagesergebnis > 0 mit t ≥ 3,0 (kleinster aus iid / Woche / Monat) | -1.45 bp/Tag, t = -4.33 | **nein** |
| ≥ 6 von 9 Jahren positiv | 1 von 9 | **nein** |
| beide Teilzeiträume 2015–2019 und 2020–2023 positiv | -1.36 / -1.55 bp | **nein** |
| bei doppelten Kosten > 0 | -3.45 bp/Tag | **nein** |

**LL-AJ: nicht bestanden.**

| Jahr | Netto % |
|---|---|
| 2015 | -6.64 |
| 2016 | +3.73 |
| 2017 | -5.46 |
| 2018 | -4.22 |
| 2019 | -5.18 |
| 2020 | -6.90 |
| 2021 | -0.73 |
| 2022 | -3.83 |
| 2023 | -4.70 |

## LL-Y1

| Kennzahl | Wert |
|---|---|
| Werktage / Trades bzw. Positionswechsel | 2,347 / 2,253 |
| Netto je Tag (bp des Kapitals) | -0.99 bp (σ 60.7 bp) |
| Kosten je Tag | 1.65 bp |
| Rendite p. a. (netto) | -2.59 % |
| Sharpe Ratio p. a. (netto) | -0.26 |
| t-Wert iid / Woche / Monat | -0.79 / -0.80 / -0.85 |
| Kurs-Ergebnis / Swap je Tag | +0.50 / -0.47 bp (Ø Gewicht 1.16) |
| bei doppelten Kosten | -2.64 bp/Tag |

| Kriterium | Ergebnis | erfüllt |
|---|---|---|
| Mittleres Netto-Tagesergebnis > 0 mit t ≥ 3,0 (kleinster aus iid / Woche / Monat) | -0.99 bp/Tag, t = -0.85 | **nein** |
| ≥ 6 von 9 Jahren positiv | 4 von 9 | **nein** |
| beide Teilzeiträume 2015–2019 und 2020–2023 positiv | +2.06 / -4.81 bp | **nein** |
| bei doppelten Kosten > 0 | -2.64 bp/Tag | **nein** |

**LL-Y1: nicht bestanden.**

| Jahr | Netto % |
|---|---|
| 2015 | +5.61 |
| 2016 | +14.02 |
| 2017 | +1.58 |
| 2018 | -1.72 |
| 2019 | +7.34 |
| 2020 | -10.43 |
| 2021 | -1.23 |
| 2022 | -17.17 |
| 2023 | -21.31 |

## LL-Y20

| Kennzahl | Wert |
|---|---|
| Werktage / Trades bzw. Positionswechsel | 2,347 / 264 |
| Netto je Tag (bp des Kapitals) | -0.13 bp (σ 68.3 bp) |
| Kosten je Tag | 0.92 bp |
| Rendite p. a. (netto) | -0.33 % |
| Sharpe Ratio p. a. (netto) | -0.03 |
| t-Wert iid / Woche / Monat | -0.09 / -0.09 / -0.09 |
| Kurs-Ergebnis / Swap je Tag | +0.62 / -0.50 bp (Ø Gewicht 1.27) |
| bei doppelten Kosten | -1.04 bp/Tag |

| Kriterium | Ergebnis | erfüllt |
|---|---|---|
| Mittleres Netto-Tagesergebnis > 0 mit t ≥ 3,0 (kleinster aus iid / Woche / Monat) | -0.13 bp/Tag, t = -0.09 | **nein** |
| ≥ 6 von 9 Jahren positiv | 4 von 9 | **nein** |
| beide Teilzeiträume 2015–2019 und 2020–2023 positiv | -0.85 / +0.78 bp | **nein** |
| bei doppelten Kosten > 0 | -1.04 bp/Tag | **nein** |

**LL-Y20: nicht bestanden.**

| Jahr | Netto % |
|---|---|
| 2015 | +5.96 |
| 2016 | +7.18 |
| 2017 | -3.79 |
| 2018 | -5.60 |
| 2019 | -14.88 |
| 2020 | -7.18 |
| 2021 | -2.33 |
| 2022 | +9.51 |
| 2023 | +8.18 |

## Beschreibend

| AUDJPY Open i+1 → Open i+4 (bp, vor Kosten) | Anzahl | Ø | t |
|---|---|---|---|
| nach US500 z > 1.5 | 2,629 | -0.14 | -0.22 |
| nach US500 z < −1.5 | 2,843 | -0.83 | -1.12 |
| alle Stunden | 55,173 | -0.01 | -0.09 |

| USDJPY-Tagesrendite (Marke) gegen ΔDGS10 (bp) | Korrelation |
|---|---|
| gleicher Tag | +0.488 |
| ΔDGS10 des Vortags → USDJPY heute | +0.035 |

**Ergebnis: Keine Variante erfüllt alle In-Sample-Kriterien. Strategien Nr. 58 und 59 sind gescheitert; der Hold-out bleibt unberührt.**
