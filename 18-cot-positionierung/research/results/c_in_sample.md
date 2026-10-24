# Modell C (COT-Extreme), In-Sample 2015–2023 (Trial T60 C-KONTRA, T61 C-FOLGE)

Lauf vom 24.10.2026. Regeln laut `docs/01_Vorregistrierung.md`, Code `research/cot/`. Handelstage 01.01.2015–31.12.2023, 7 FX-Paare und Gold, COT-Warm-up ab 2012. Netto = nach Handelskosten, Swaps (Zinsdifferenz − 1 % Aufschlag) und 0,7-%-Gebühr. Renditen und Drawdown sind auf eine Portfolio-Volatilität von 10 % p. a. skaliert (Kalibrierung auf diesen Zeitraum, nur zur Einordnung).

## C-KONTRA

| Kennzahl | Wert |
|---|---|
| Handelstage | 2,340 |
| Sharpe Ratio p. a. (netto) | 0.22 |
| t-Wert iid / Woche / Monat | 0.66 / 0.62 / 0.70 |
| Rendite p. a. bei 10 % Volatilität | +2.20% |
| Max. Drawdown bei 10 % Volatilität | 18.7% |
| Zerlegung p. a. bei 10 % Vol.: Kurs / Swaps / Handel / Gebühr | +3.69% / -1.27% / -0.15% / -0.07% |
| Ø Brutto-Exposure (Summe \|w\|, unskaliert) | 1.62 |

| Kriterium | Ergebnis | erfüllt |
|---|---|---|
| Mittleres Netto-Tagesergebnis > 0 mit t ≥ 3,0 (kleinster aus iid / Woche / Monat) | t = 0.62 (Sharpe 0.22) | **nein** |
| ≥ 6 von 9 Jahren positiv | 6 von 9 | ja |
| ≥ 60 % der Instrumente (≥ 250 Positionstage) positiv | 6 von 8 | ja |
| bei doppelten Kosten > 0 | +0.56% p. a. bei 10 % Vol. | ja |

**C-KONTRA: nicht bestanden.**

| Jahr | Rendite bei 10 % Vol. | Sharpe |
|---|---|---|
| 2015 | +0.4% | +0.05 |
| 2016 | -0.2% | -0.01 |
| 2017 | +4.3% | +0.37 |
| 2018 | +8.6% | +0.67 |
| 2019 | +1.4% | +0.26 |
| 2020 | -4.9% | -0.37 |
| 2021 | +14.3% | +1.79 |
| 2022 | -4.7% | -0.65 |
| 2023 | +0.6% | +0.07 |

| Instrument | Positionstage | Beitrag netto bei 10 % Vol. (Summe) | davon Swaps |
|---|---|---|---|
| AUDUSD | 360 | +11.6% | -1.6% |
| GBPUSD | 328 | +10.4% | -0.7% |
| USDCAD | 403 | +9.9% | -1.5% |
| EURUSD | 373 | +3.0% | +0.2% |
| XAUUSD | 433 | +2.1% | -1.3% |
| NZDUSD | 318 | +1.8% | -0.8% |
| USDJPY | 618 | -9.4% | -3.3% |
| USDCHF | 440 | -9.6% | -2.3% |

Zeit im Markt (Anteil Instrument-Tage mit Position): 17%; davon long 55%.

## C-FOLGE

| Kennzahl | Wert |
|---|---|
| Handelstage | 2,340 |
| Sharpe Ratio p. a. (netto) | -0.50 |
| t-Wert iid / Woche / Monat | -1.50 / -1.40 / -1.57 |
| Rendite p. a. bei 10 % Volatilität | -4.99% |
| Max. Drawdown bei 10 % Volatilität | 54.0% |
| Zerlegung p. a. bei 10 % Vol.: Kurs / Swaps / Handel / Gebühr | -3.69% / -1.10% / -0.15% / -0.07% |
| Ø Brutto-Exposure (Summe \|w\|, unskaliert) | 1.62 |

| Kriterium | Ergebnis | erfüllt |
|---|---|---|
| Mittleres Netto-Tagesergebnis > 0 mit t ≥ 3,0 (kleinster aus iid / Woche / Monat) | t = -1.57 (Sharpe -0.50) | **nein** |
| ≥ 6 von 9 Jahren positiv | 2 von 9 | **nein** |
| ≥ 60 % der Instrumente (≥ 250 Positionstage) positiv | 2 von 8 | **nein** |
| bei doppelten Kosten > 0 | -6.59% p. a. bei 10 % Vol. | **nein** |

**C-FOLGE: nicht bestanden.**

| Jahr | Rendite bei 10 % Vol. | Sharpe |
|---|---|---|
| 2015 | -1.8% | -0.23 |
| 2016 | -2.9% | -0.23 |
| 2017 | -8.6% | -0.75 |
| 2018 | -12.5% | -0.98 |
| 2019 | -3.0% | -0.55 |
| 2020 | +0.7% | +0.05 |
| 2021 | -17.0% | -2.13 |
| 2022 | +3.5% | +0.48 |
| 2023 | -3.2% | -0.40 |

| Instrument | Positionstage | Beitrag netto bei 10 % Vol. (Summe) | davon Swaps |
|---|---|---|---|
| USDCHF | 440 | +5.3% | -1.2% |
| USDJPY | 618 | +4.4% | -0.8% |
| NZDUSD | 318 | -4.1% | -1.2% |
| XAUUSD | 433 | -4.3% | -0.6% |
| EURUSD | 373 | -5.8% | -2.9% |
| GBPUSD | 328 | -12.5% | -1.1% |
| USDCAD | 403 | -13.3% | -1.3% |
| AUDUSD | 360 | -14.4% | -0.7% |

Zeit im Markt (Anteil Instrument-Tage mit Position): 17%; davon long 45%.

**Ergebnis: Keine Variante erfüllt alle In-Sample-Kriterien. Strategie Nr. 18 ist gescheitert; der Hold-out bleibt unberührt.**
