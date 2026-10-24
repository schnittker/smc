# Modell N (NFP-Straddle), In-Sample 2015–2023 (Trial T303 N-NFP)

Lauf vom 24.10.2026. Regeln laut `docs/01_Vorregistrierung.md`, Code `research/nws/`. OCO ±0,10 % um 08:29 New York, Stop 0,20 %, Ausstieg 09:30; News-Kosten 5-facher Spread und 0,03 % Slippage (08:30–08:34). Ergebnisse in bp des Kapitals, 0,25 % Risiko je Trade.

## N-NFP

| Kennzahl | Wert |
|---|---|
| Termine / Trades | 105 / 186 |
| Netto je Termin (bp des Kapitals, 4 Instrumente) | -8.81 bp |
| vor Kosten / Kosten je Termin | +5.35 / 14.15 bp |
| t-Wert iid / Quartal | -1.22 / -1.09 |
| Auslösequote / Anteil Stops | 45% / 59% |
| Ø R je Trade vor / nach Kosten | +0.121 / -0.199 |

| Kriterium | Ergebnis | erfüllt |
|---|---|---|
| Netto je Termin > 0 mit t ≥ 3,0 (iid / Quartal) | -8.81 bp, t = -1.22 | **nein** |
| ≥ 6 von 9 Jahren positiv | 2 von 9 | **nein** |
| ≥ 3 von 4 Instrumenten positiv | 0 von 4 | **nein** |
| bei doppelten Kosten > 0 | -22.96 bp | **nein** |

**N-NFP: nicht bestanden.**

| Jahr | Netto Summe bp |
|---|---|
| 2015 | +490.0 |
| 2016 | -448.8 |
| 2017 | -390.0 |
| 2018 | -161.0 |
| 2019 | -43.4 |
| 2020 | -285.8 |
| 2021 | -402.6 |
| 2022 | -1.5 |
| 2023 | +318.5 |

| Instrument | Netto Summe bp |
|---|---|
| EURUSD | -253.9 |
| GBPUSD | -217.1 |
| USDJPY | -157.2 |
| XAUUSD | -296.3 |

## Beschreibend: normale Kosten (1-facher Spread, ≈ 0,1 Pip Slippage)

Netto +4.28 bp je Termin (t 0.49), vor Kosten +6.72 bp, Ø R netto +0.102.

**Ergebnis: N-NFP erfüllt die In-Sample-Kriterien nicht. Strategie Nr. 94 ist gescheitert; der Hold-out bleibt unberührt.**
