# Modell C (Multi-Asset-Trend, CTA), In-Sample 2015–2023 (Trial T313 C-FIX, T314 C-WF)

Lauf vom 25.10.2026. Regeln laut `docs/01_Vorregistrierung.md`, Code `research/cta/`. 24 Märkte in 4 Klassen (FX 7, Indizes 8, Rohstoffe 4, Krypto 5 ab 2018); je Klasse 10 % Risikobudget. Netto = nach Spread, Slippage, Kommission, Swaps (Krypto 20 % p. a.) und Gebühren; Tagesrendite als Anteil des Kapitals vor der FTMO-Skalierung, Kalendertage (Wochenende nur Krypto).

## C-FIX

| Kennzahl | Wert |
|---|---|
| Kalendertage | 3,287 |
| Netto je Tag (Anteil des Kapitals, unskaliert) | +0.35 bp (σ 77.1 bp) |
| Rendite p. a. (unskaliert) | +1.3% bei 14.7% Vola |
| Sharpe Ratio p. a. | 0.09 |
| t-Wert iid / Woche / Monat | 0.26 / 0.26 / 0.25 |
| Kosten + Swap-Belastung p. a. (davon Umstellung) | 4.37% (0.00%) |
| Long / Short vor Kosten p. a. | +7.07% / -1.75% |
| Margin-Auslastung Ø / max. (unskaliert) | 0.127 / 0.317 |
| bei doppelten Kosten | -0.84 bp/Tag |

| Kriterium | Ergebnis | erfüllt |
|---|---|---|
| Mittleres Netto-Tagesergebnis > 0 mit t ≥ 3,0 (kleinster aus iid / Woche / Monat) | +0.35 bp/Tag, t = 0.25 | **nein** |
| ≥ 6 von 9 Jahren positiv | 6 von 9 | ja |
| ≥ 3 von 4 Klassen positiv | 2 von 4 | **nein** |
| bei doppelten Kosten > 0 | -0.84 bp/Tag | **nein** |

**C-FIX: nicht bestanden.**

| Klasse | Netto p. a. |
|---|---|
| FX | -0.93% |
| Indizes | +2.12% |
| Rohstoffe | -0.99% |
| Krypto | +1.10% |

| Jahr | Netto |
|---|---|
| 2015 | -1.35% |
| 2016 | -13.29% |
| 2017 | +2.21% |
| 2018 | +0.52% |
| 2019 | -13.78% |
| 2020 | +19.38% |
| 2021 | +6.49% |
| 2022 | +0.47% |
| 2023 | +11.00% |

## C-WF

| Kennzahl | Wert |
|---|---|
| Kalendertage | 3,287 |
| Netto je Tag (Anteil des Kapitals, unskaliert) | +1.46 bp (σ 107.1 bp) |
| Rendite p. a. (unskaliert) | +5.3% bei 20.5% Vola |
| Sharpe Ratio p. a. | 0.26 |
| t-Wert iid / Woche / Monat | 0.78 / 0.77 / 0.80 |
| Kosten + Swap-Belastung p. a. (davon Umstellung) | 7.14% (0.01%) |
| Long / Short vor Kosten p. a. | +15.38% / -3.00% |
| Margin-Auslastung Ø / max. (unskaliert) | 0.217 / 1.145 |
| bei doppelten Kosten | -0.50 bp/Tag |

| Kriterium | Ergebnis | erfüllt |
|---|---|---|
| Mittleres Netto-Tagesergebnis > 0 mit t ≥ 3,0 (kleinster aus iid / Woche / Monat) | +1.46 bp/Tag, t = 0.77 | **nein** |
| ≥ 6 von 9 Jahren positiv | 2 von 9 | **nein** |
| ≥ 3 von 4 Klassen positiv | 1 von 4 | **nein** |
| bei doppelten Kosten > 0 | -0.50 bp/Tag | **nein** |

**C-WF: nicht bestanden.**

| Klasse | Netto p. a. |
|---|---|
| FX | -0.67% |
| Indizes | -3.68% |
| Rohstoffe | -0.34% |
| Krypto | +10.03% |

| Jahr | Netto |
|---|---|
| 2015 | -1.35% |
| 2016 | -13.74% |
| 2017 | -0.02% |
| 2018 | -4.26% |
| 2019 | -19.92% |
| 2020 | +62.08% |
| 2021 | +35.97% |
| 2022 | -8.97% |
| 2023 | -1.90% |

| Jahr | FX | Indizes | Rohstoffe | Krypto |
|---|---|---|---|---|
| 2015 | MITTEL ×1.00 | MITTEL ×1.00 | MITTEL ×1.00 | MITTEL ×1.00 |
| 2016 | LANGSAM ×1.51 | MITTEL ×1.49 | LANGSAM ×0.00 | MITTEL ×1.00 |
| 2017 | LANGSAM ×0.00 | MITTEL ×0.00 | SCHNELL ×0.00 | MITTEL ×1.00 |
| 2018 | LANGSAM ×0.00 | LANGSAM ×3.00 | SCHNELL ×0.00 | MITTEL ×1.00 |
| 2019 | MITTEL ×0.00 | LANGSAM ×3.00 | SCHNELL ×0.00 | MITTEL ×1.00 |
| 2020 | MITTEL ×0.00 | LANGSAM ×0.00 | SCHNELL ×0.00 | SCHNELL ×4.00 |
| 2021 | MITTEL ×0.00 | LANGSAM ×0.00 | SCHNELL ×0.31 | SCHNELL ×3.69 |
| 2022 | LANGSAM ×0.00 | LANGSAM ×0.36 | SCHNELL ×0.06 | SCHNELL ×3.59 |
| 2023 | LANGSAM ×0.00 | LANGSAM ×0.00 | SCHNELL ×0.03 | SCHNELL ×3.97 |

**Ergebnis: Keine Variante erfüllt alle In-Sample-Kriterien. Strategie Nr. 102 ist gescheitert; der Hold-out bleibt unberührt.**
