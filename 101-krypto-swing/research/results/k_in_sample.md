# Modell K (Krypto-Swing-Trendfolge), In-Sample 2018–2023 (Trial T309 K-TSM, T310 K-LONG)

Lauf vom 25.10.2026. Regeln laut `docs/01_Vorregistrierung.md`, Code `research/kry/`. Binance-Spot-Tageskerzen 00:00 UTC, BTC/ETH/LTC/XRP/ADA; je Coin 10 % Zielvola, Hebel ≤ 1:1. Netto = nach Spread, Slippage, Kommission und 20 % p. a. Swap auf das Nominal.

## K-TSM

| Kennzahl | Wert |
|---|---|
| Kalendertage | 2,191 |
| Netto je Tag (Anteil des Kapitals) | +7.31 bp (σ 174.0 bp) |
| vor Kosten je Tag | +11.42 bp |
| Handelskosten / Swap je Tag | 1.83 / 2.28 bp |
| Rendite p. a. (netto, unskaliert) | +26.7% |
| Sharpe Ratio p. a. | 0.80 |
| t-Wert iid / Woche / Monat | 1.97 / 1.98 / 2.14 |
| Swap 10 % / 30 % p. a. statt 20 % | +8.45 / +6.17 bp/Tag |
| Long / Short vor Kosten p. a. | +36.2% / +5.4% |
| Ø Gesamtnominal / Anteil Tage an der 1:1-Grenze | 0.42 / 2% |
| bei doppelten Kosten | +3.20 bp/Tag |

| Kriterium | Ergebnis | erfüllt |
|---|---|---|
| Mittleres Netto-Tagesergebnis > 0 mit t ≥ 3,0 (kleinster aus iid / Woche / Monat) | +7.31 bp/Tag, t = 1.97 | **nein** |
| ≥ 4 von 6 Jahren positiv | 4 von 6 | ja |
| ≥ 3 von 5 Coins positiv | 5 von 5 | ja |
| bei doppelten Kosten > 0 | +3.20 bp/Tag | ja |

**K-TSM: nicht bestanden.**

| Jahr | Netto % |
|---|---|
| 2018 | +16.8% |
| 2019 | +32.8% |
| 2020 | +68.3% |
| 2021 | +49.6% |
| 2022 | -3.9% |
| 2023 | -3.5% |

| Coin | Netto p. a. | vor Kosten p. a. |
|---|---|---|
| BTC | +9.0% | +12.2% |
| ETH | +8.3% | +10.9% |
| LTC | +0.2% | +3.4% |
| XRP | +2.1% | +5.3% |
| ADA | +7.0% | +9.8% |

## K-LONG

| Kennzahl | Wert |
|---|---|
| Kalendertage | 2,191 |
| Netto je Tag (Anteil des Kapitals) | +7.93 bp (σ 128.3 bp) |
| vor Kosten je Tag | +9.97 bp |
| Handelskosten / Swap je Tag | 0.87 / 1.17 bp |
| Rendite p. a. (netto, unskaliert) | +28.9% |
| Sharpe Ratio p. a. | 1.18 |
| t-Wert iid / Woche / Monat | 2.89 / 2.66 / 2.57 |
| Swap 10 % / 30 % p. a. statt 20 % | +8.51 / +7.35 bp/Tag |
| Long / Short vor Kosten p. a. | +36.4% / +0.0% |
| Ø Gesamtnominal / Anteil Tage an der 1:1-Grenze | 0.21 / 1% |
| bei doppelten Kosten | +5.89 bp/Tag |

| Kriterium | Ergebnis | erfüllt |
|---|---|---|
| Mittleres Netto-Tagesergebnis > 0 mit t ≥ 3,0 (kleinster aus iid / Woche / Monat) | +7.93 bp/Tag, t = 2.57 | **nein** |
| ≥ 4 von 6 Jahren positiv | 4 von 6 | ja |
| ≥ 3 von 5 Coins positiv | 5 von 5 | ja |
| bei doppelten Kosten > 0 | +5.89 bp/Tag | ja |

**K-LONG: nicht bestanden.**

| Jahr | Netto % |
|---|---|
| 2018 | -13.0% |
| 2019 | +40.0% |
| 2020 | +80.0% |
| 2021 | +58.9% |
| 2022 | -13.2% |
| 2023 | +21.0% |

| Coin | Netto p. a. | vor Kosten p. a. |
|---|---|---|
| BTC | +9.6% | +11.3% |
| ETH | +7.7% | +9.2% |
| LTC | +1.1% | +2.7% |
| XRP | +4.0% | +5.4% |
| ADA | +6.6% | +7.8% |

Referenz BTC halten (1× Nominal, mit 20 % Swap): Sharpe 0.34, +24.2% p. a.

**Ergebnis: Keine Variante erfüllt alle In-Sample-Kriterien. Strategie Nr. 101 ist gescheitert; der Hold-out bleibt unberührt.**
