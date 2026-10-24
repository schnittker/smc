# Modell G (Gold/Silber-Ratio), In-Sample 2015–2023 (Trial T76 G-60, T77 G-250)

Lauf vom 24.10.2026. Regeln laut `docs/01_Vorregistrierung.md`, Code `research/gsr/`. Spread-Position Gold gegen Silber bei |z| ≥ 2. Tagesbuchhaltung von Modell G mit Kostenmodell H; Netto = nach Handelskosten, Swaps und Gebühr. Renditen unskaliert und zusätzlich auf 10 % Volatilität skaliert (nur zur Einordnung).

## G-60

| Kennzahl | Wert |
|---|---|
| Handelstage | 2,330 |
| Rendite / Volatilität p. a. (unskaliert) | -0.64% / 8.7% |
| Sharpe Ratio p. a. (netto) | -0.07 |
| t-Wert iid / Woche / Monat | -0.22 / -0.22 / -0.20 |
| Zerlegung p. a. (unskaliert): Kurs / Swaps / Handel | +0.53% / -0.78% / -0.39% |
| Ø / max. Gewicht w | 0.00 / 0.00 |
| bei 10 % Vol.: Rendite p. a. / max. Drawdown / schlechtester Tag | -0.74% / 52.9% / -9.24% |

| Kriterium | Ergebnis | erfüllt |
|---|---|---|
| Mittleres Netto-Tagesergebnis > 0 mit t ≥ 3,0 (kleinster aus iid / Woche / Monat) | t = -0.22 (Sharpe -0.07) | **nein** |
| ≥ 6 von 9 Jahren positiv | 3 von 9 | **nein** |
| beide Teilzeiträume 2015–2019 und 2020–2023 positiv | +0.27 / -0.89 bp/Tag | **nein** |
| bei doppelten Kosten > 0 | -2.09% p. a. (unskaliert) | **nein** |

**G-60: nicht bestanden.**

| Jahr | Rendite (unskaliert) |
|---|---|
| 2015 | +16.7% |
| 2016 | -4.6% |
| 2017 | -3.1% |
| 2018 | -3.2% |
| 2019 | -2.3% |
| 2020 | -19.2% |
| 2021 | -5.0% |
| 2022 | +2.9% |
| 2023 | +12.1% |

## G-250

| Kennzahl | Wert |
|---|---|
| Handelstage | 2,330 |
| Rendite / Volatilität p. a. (unskaliert) | +0.74% / 8.7% |
| Sharpe Ratio p. a. (netto) | 0.09 |
| t-Wert iid / Woche / Monat | 0.26 / 0.26 / 0.25 |
| Zerlegung p. a. (unskaliert): Kurs / Swaps / Handel | +1.71% / -0.85% / -0.12% |
| Ø / max. Gewicht w | 0.00 / 0.00 |
| bei 10 % Vol.: Rendite p. a. / max. Drawdown / schlechtester Tag | +0.86% / 29.4% / -9.03% |

| Kriterium | Ergebnis | erfüllt |
|---|---|---|
| Mittleres Netto-Tagesergebnis > 0 mit t ≥ 3,0 (kleinster aus iid / Woche / Monat) | t = 0.25 (Sharpe 0.09) | **nein** |
| ≥ 6 von 9 Jahren positiv | 5 von 9 | **nein** |
| beide Teilzeiträume 2015–2019 und 2020–2023 positiv | +0.63 / -0.15 bp/Tag | **nein** |
| bei doppelten Kosten > 0 | -0.42% p. a. (unskaliert) | **nein** |

**G-250: nicht bestanden.**

| Jahr | Rendite (unskaliert) |
|---|---|
| 2015 | +9.3% |
| 2016 | +2.2% |
| 2017 | -3.8% |
| 2018 | -2.0% |
| 2019 | +2.5% |
| 2020 | +0.5% |
| 2021 | +0.1% |
| 2022 | -2.2% |
| 2023 | +0.0% |

# Beschreibend

| Variante | Trades | Trefferquote | Ø Ergebnis je Trade (Kapital) | Ø Haltedauer | Zeit im Markt |
|---|---|---|---|---|---|
| G-60 | 32 | 56% | -17.9 bp | 41 Tage | 56% |
| G-250 | 10 | 50% | +66.2 bp | 152 Tage | 65% |

**Ergebnis: Keine Variante erfüllt alle In-Sample-Kriterien. Strategie Nr. 22 ist gescheitert; der Hold-out bleibt unberührt.**
