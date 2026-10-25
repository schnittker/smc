# Modell K, Hold-out 01.01.2024–24.10.2026 (Trial T317, K-LONG, Ausnahmeregel laut docs/03_Nachtrag_Hold-out.md)

Einmaliger Lauf vom 25.10.2026. **Regeländerung nach IS-Ergebnis** (t 2,57 < 3), mit strengeren Hold-out-Kriterien.

## K-LONG

| Kennzahl | Wert |
|---|---|
| Kalendertage | 1,028 |
| Netto je Tag (Anteil des Kapitals) | +2.93 bp (σ 116.1 bp) |
| vor Kosten je Tag | +5.46 bp |
| Handelskosten / Swap je Tag | 1.17 / 1.36 bp |
| Rendite p. a. (netto, unskaliert) | +10.7% |
| Sharpe Ratio p. a. | 0.48 |
| t-Wert iid / Woche / Monat | 0.81 / 0.64 / 0.54 |
| Swap 10 % / 30 % p. a. statt 20 % | +3.61 / +2.25 bp/Tag |
| Long / Short vor Kosten p. a. | +19.9% / +0.0% |
| Ø Gesamtnominal / Anteil Tage an der 1:1-Grenze | 0.25 / 1% |
| bei doppelten Kosten | +0.40 bp/Tag |

| Kriterium | Ergebnis | erfüllt |
|---|---|---|
| Mittleres Netto-Tagesergebnis > 0 | +2.93 bp/Tag | ja |
| ≥ untere 95-%-Grenze von IS (Cluster nach Monat) | +2.93 vs. IS +7.93 [+2.17; +14.35] bp/Tag | ja |
| Sharpe Ratio im Hold-out ≥ 0,5 (Nachtrag) | 0.48 | **nein** |

**K-LONG: nicht bestanden.**

| Jahr | Netto % |
|---|---|
| 2024 | +44.6% |
| 2025 | -9.3% |
| 2026 | -5.1% |

| Coin | Netto p. a. | vor Kosten p. a. |
|---|---|---|
| BTC | +3.0% | +5.5% |
| ETH | +4.0% | +5.6% |
| LTC | -0.2% | +1.9% |
| XRP | +4.4% | +6.1% |
| ADA | -0.5% | +0.9% |

Referenz BTC halten (1× Nominal, mit 20 % Swap): Sharpe 0.30, +14.0% p. a.

Wochenend-Anteil (Sa/So UTC) am Netto-Ergebnis: +15.74% von +30.16% (52% des Ergebnisses an 29% der Tage).

**Ergebnis: Hold-out nicht bestanden; kein FTMO-Bootstrap (T318 entfällt).**
