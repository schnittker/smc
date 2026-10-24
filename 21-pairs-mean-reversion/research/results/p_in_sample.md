# Modell P (z-Score Mean Reversion AUDNZD / EURCHF), In-Sample 2015–2023 (Trial T72 P-AUDNZD, T73 P-EURCHF)

Lauf vom 24.10.2026. Regeln laut `docs/01_Vorregistrierung.md`, Code `research/pmr/`. Tagesbuchhaltung von Modell G (16:50 New York), FX-Kosten, Swaps und 0,7-%-Gebühr. Positionen 10 % / σ; Renditen unskaliert und zusätzlich auf 10 % Volatilität skaliert (nur zur Einordnung).

## P-AUDNZD

| Kennzahl | Wert |
|---|---|
| Handelstage | 2,340 |
| Rendite / Volatilität p. a. (unskaliert) | +0.98% / 7.4% |
| Sharpe Ratio p. a. (netto) | 0.13 |
| t-Wert iid / Woche / Monat | 0.40 / 0.41 / 0.42 |
| Zerlegung p. a. (unskaliert): Kurs / Swaps / Handel | +1.98% / -0.82% / -0.13% |
| Ø / max. Gewicht w | 0.00 / 2.40 |
| bei 10 % Vol.: Rendite p. a. / max. Drawdown / schlechtester Tag | +1.32% / 19.1% / -4.25% |

| Kriterium | Ergebnis | erfüllt |
|---|---|---|
| Mittleres Netto-Tagesergebnis > 0 mit t ≥ 3,0 (kleinster aus iid / Woche / Monat) | t = 0.40 (Sharpe 0.13) | **nein** |
| ≥ 6 von 9 Jahren positiv | 6 von 9 | ja |
| beide Teilzeiträume 2015–2019 und 2020–2023 positiv | -0.07 / +0.93 bp/Tag | **nein** |
| bei doppelten Kosten > 0 | -0.12% p. a. (unskaliert) | **nein** |

**P-AUDNZD: nicht bestanden.**

| Jahr | Rendite (unskaliert) |
|---|---|
| 2015 | +3.3% |
| 2016 | +1.7% |
| 2017 | -2.4% |
| 2018 | -4.5% |
| 2019 | +1.0% |
| 2020 | +5.0% |
| 2021 | +4.4% |
| 2022 | -5.2% |
| 2023 | +5.4% |

| Trades | Trefferquote | Ø Ergebnis je Trade (Kapital) | Ø Haltedauer (Handelstage) | Zeit im Markt |
|---|---|---|---|---|
| 34 | 62% | +25.8 bp | 34.7 | 50% |

## P-EURCHF

| Kennzahl | Wert |
|---|---|
| Handelstage | 2,340 |
| Rendite / Volatilität p. a. (unskaliert) | -3.48% / 17.1% |
| Sharpe Ratio p. a. (netto) | -0.20 |
| t-Wert iid / Woche / Monat | -0.61 / -0.62 / -0.77 |
| Zerlegung p. a. (unskaliert): Kurs / Swaps / Handel | -2.23% / -1.06% / -0.11% |
| Ø / max. Gewicht w | 0.30 / 2.50 |
| bei 10 % Vol.: Rendite p. a. / max. Drawdown / schlechtester Tag | -2.04% / 27.0% / -24.75% |

| Kriterium | Ergebnis | erfüllt |
|---|---|---|
| Mittleres Netto-Tagesergebnis > 0 mit t ≥ 3,0 (kleinster aus iid / Woche / Monat) | t = -0.77 (Sharpe -0.20) | **nein** |
| ≥ 6 von 9 Jahren positiv | 5 von 9 | **nein** |
| beide Teilzeiträume 2015–2019 und 2020–2023 positiv | -2.50 / +0.12 bp/Tag | **nein** |
| bei doppelten Kosten > 0 | -4.81% p. a. (unskaliert) | **nein** |

**P-EURCHF: nicht bestanden.**

| Jahr | Rendite (unskaliert) |
|---|---|
| 2015 | -31.2% |
| 2016 | +5.4% |
| 2017 | -15.7% |
| 2018 | +6.4% |
| 2019 | +2.6% |
| 2020 | -1.9% |
| 2021 | -10.9% |
| 2022 | +10.7% |
| 2023 | +3.3% |

| Trades | Trefferquote | Ø Ergebnis je Trade (Kapital) | Ø Haltedauer (Handelstage) | Zeit im Markt |
|---|---|---|---|---|
| 36 | 61% | -86.8 bp | 38.7 | 60% |

# Beschreibend

P-EURCHF ohne Januar 2015 (SNB-Schock): Sharpe +0.02, t +0.07, Januar 2015 allein -32.93% (unskaliert).

**Ergebnis: Keine Variante erfüllt alle In-Sample-Kriterien. Strategie Nr. 21 ist gescheitert; der Hold-out bleibt unberührt.**
