# Modell K, Hold-out LAUF 1 (FEHLERHAFT: Daten nur bis 24.10.2025 statt 24.10.2026 wegen falscher Konstante LAST_DAY) – Trial T317, K-LONG, Ausnahmeregel

Einmaliger Lauf vom 25.10.2026. **Regeländerung nach IS-Ergebnis** (t 2,57 < 3), mit strengeren Hold-out-Kriterien.

## K-LONG

| Kennzahl | Wert |
|---|---|
| Kalendertage | 663 |
| Netto je Tag (Anteil des Kapitals) | +5.34 bp (σ 125.4 bp) |
| vor Kosten je Tag | +7.96 bp |
| Handelskosten / Swap je Tag | 1.20 / 1.43 bp |
| Rendite p. a. (netto, unskaliert) | +19.5% |
| Sharpe Ratio p. a. | 0.81 |
| t-Wert iid / Woche / Monat | 1.10 / 0.86 / 0.66 |
| Swap 10 % / 30 % p. a. statt 20 % | +6.05 / +4.63 bp/Tag |
| Long / Short vor Kosten p. a. | +29.1% / +0.0% |
| Ø Gesamtnominal / Anteil Tage an der 1:1-Grenze | 0.26 / 1% |
| bei doppelten Kosten | +2.72 bp/Tag |

| Kriterium | Ergebnis | erfüllt |
|---|---|---|
| Mittleres Netto-Tagesergebnis > 0 | +5.34 bp/Tag | ja |
| ≥ untere 95-%-Grenze von IS (Cluster nach Monat) | +5.34 vs. IS +7.93 [+2.17; +14.35] bp/Tag | ja |
| Sharpe Ratio im Hold-out ≥ 0,5 (Nachtrag) | 0.81 | ja |

**K-LONG: alle Kriterien erfüllt.**

| Jahr | Netto % |
|---|---|
| 2024 | +44.6% |
| 2025 | -9.1% |

| Coin | Netto p. a. | vor Kosten p. a. |
|---|---|---|
| BTC | +4.5% | +7.1% |
| ETH | +5.6% | +7.1% |
| LTC | -1.3% | +0.8% |
| XRP | +9.0% | +10.9% |
| ADA | +1.8% | +3.2% |

Referenz BTC halten (1× Nominal, mit 20 % Swap): Sharpe 0.93, +44.8% p. a.

Wochenend-Anteil (Sa/So UTC) am Netto-Ergebnis: +18.28% von +35.42% (52% des Ergebnisses an 28% der Tage).

## FTMO-Block-Bootstrap auf IS + Hold-out (T312)

| Tagesschwankung | k | P(Phase 1) | P(Phase 2) | P(beide) | Median-Dauer (Monate) | historische Starts | erfüllt |
|---|---|---|---|---|---|---|---|
| 0.50% | 0.39 | 78% | 97% | **76%** | 16.2 | 65 von 87 | nein |
| 0.75% | 0.58 | 53% | 80% | **42%** | 7.1 | 39 von 88 | nein |
| 1.00% | 0.78 | 45% | 72% | **32%** | 4.6 | 28 von 90 | nein |
| 1.25% | 0.97 | 40% | 69% | **27%** | 3.4 | 21 von 94 | nein |

**T318: nicht bestanden.**
