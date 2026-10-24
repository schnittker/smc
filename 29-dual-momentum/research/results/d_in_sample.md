# Modell D (Dual Momentum), In-Sample 2015–2023 (Trial T102 D-TOP1, T103 D-TOP2)

Lauf vom 24.10.2026. Regeln laut `docs/01_Vorregistrierung.md`, Code `research/dmom/`. Monatliche Rotation in die Anlage(n) mit höchster 12-Monats-Rendite über dem USD-Zins; Tagesbuchhaltung von Modell G mit Kostenmodell H; Netto = nach Handelskosten, Swaps und Gebühr. Renditen unskaliert und zusätzlich auf 10 % Volatilität skaliert (nur zur Einordnung).

## D-TOP1

| Kennzahl | Wert |
|---|---|
| Handelstage | 2,333 |
| Rendite / Volatilität p. a. (unskaliert) | +1.70% / 10.3% |
| Sharpe Ratio p. a. (netto) | 0.17 |
| t-Wert iid / Woche / Monat | 0.49 / 0.48 / 0.55 |
| Zerlegung p. a. (unskaliert): Kurs / Swaps / Handel | +2.93% / -1.14% / -0.06% |
| Ø / max. Gewicht w | 0.57 / 1.67 |
| bei 10 % Vol.: Rendite p. a. / max. Drawdown / schlechtester Tag | +1.65% / 27.8% / -4.09% |

| Kriterium | Ergebnis | erfüllt |
|---|---|---|
| Mittleres Netto-Tagesergebnis > 0 mit t ≥ 3,0 (kleinster aus iid / Woche / Monat) | t = 0.48 (Sharpe 0.17) | **nein** |
| ≥ 6 von 9 Jahren positiv | 5 von 9 | **nein** |
| beide Teilzeiträume 2015–2019 und 2020–2023 positiv | +0.41 / +0.96 bp/Tag | ja |
| bei doppelten Kosten > 0 | +0.43% p. a. (unskaliert) | ja |

**D-TOP1: nicht bestanden.**

| Jahr | Rendite (unskaliert) |
|---|---|
| 2015 | -0.3% |
| 2016 | -17.2% |
| 2017 | +18.9% |
| 2018 | -5.0% |
| 2019 | +8.9% |
| 2020 | +12.9% |
| 2021 | +9.1% |
| 2022 | -13.2% |
| 2023 | +1.2% |

## D-TOP2

| Kennzahl | Wert |
|---|---|
| Handelstage | 2,333 |
| Rendite / Volatilität p. a. (unskaliert) | +2.33% / 16.7% |
| Sharpe Ratio p. a. (netto) | 0.14 |
| t-Wert iid / Woche / Monat | 0.42 / 0.38 / 0.43 |
| Zerlegung p. a. (unskaliert): Kurs / Swaps / Handel | +4.24% / -1.72% / -0.11% |
| Ø / max. Gewicht w | 1.13 / 2.51 |
| bei 10 % Vol.: Rendite p. a. / max. Drawdown / schlechtester Tag | +1.39% / 29.7% / -4.34% |

| Kriterium | Ergebnis | erfüllt |
|---|---|---|
| Mittleres Netto-Tagesergebnis > 0 mit t ≥ 3,0 (kleinster aus iid / Woche / Monat) | t = 0.38 (Sharpe 0.14) | **nein** |
| ≥ 6 von 9 Jahren positiv | 5 von 9 | **nein** |
| beide Teilzeiträume 2015–2019 und 2020–2023 positiv | +1.48 / +0.16 bp/Tag | ja |
| bei doppelten Kosten > 0 | +0.27% p. a. (unskaliert) | ja |

**D-TOP2: nicht bestanden.**

| Jahr | Rendite (unskaliert) |
|---|---|
| 2015 | -3.5% |
| 2016 | -18.0% |
| 2017 | +44.4% |
| 2018 | -12.8% |
| 2019 | +9.1% |
| 2020 | +14.0% |
| 2021 | +14.3% |
| 2022 | -33.2% |
| 2023 | +6.6% |

# Beschreibend

- D-TOP1: 107 Monate, davon 6 ganz in Cash; gewählt: NSXUSD 43, XAUUSD 20, JPXJPY 13, FRXEUR 9, HKXHKD 8, UKXGBP 4, SPXUSD 2, AUXAUD 2
- D-TOP2: 107 Monate, davon 6 ganz in Cash; gewählt: NSXUSD 69, XAUUSD 31, JPXJPY 28, FRXEUR 16, SPXUSD 15, HKXHKD 14, AUXAUD 10, UKXGBP 9

**Ergebnis: Keine Variante erfüllt alle In-Sample-Kriterien. Strategie Nr. 29 ist gescheitert; der Hold-out bleibt unberührt.**
