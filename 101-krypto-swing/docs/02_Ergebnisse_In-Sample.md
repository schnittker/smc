# Ergebnisse In-Sample: Modell K (Strategie Nr. 101)

Lauf vom 25.10.2026, vollständige Tabellen in `research/results/k_in_sample.md`.

| | K-TSM (long/short) | K-LONG (nur long) |
|---|---|---|
| Netto je Tag | +7,3 bp | +7,9 bp |
| vor Kosten | +11,4 bp | +10,0 bp |
| Handelskosten / Swap | 1,8 / 2,3 bp | 0,9 / 1,2 bp |
| Sharpe p. a. | 0,80 | **1,18** |
| t (kleinster) | 1,97 | **2,57** |
| Jahre positiv | 4 von 6 | 4 von 6 |
| Coins positiv | 5 von 5 | 5 von 5 |
| doppelte Kosten | +3,2 bp | +5,9 bp |

**Beide nicht bestanden** (t < 3). Der Hold-out bleibt unberührt.

## Einordnung

- **Das ist der bisher stärkste Kandidat der Reihe.**
  - K-LONG erfüllt 3 von 4 Kriterien und hat die höchste Netto-Sharpe aller 135 Versuche.
  - Auch bei doppelten Kosten (40 % Swap) bleibt K-LONG positiv.
  - Für t ≥ 3 über 6 Jahre wäre Sharpe ≥ 1,22 nötig; 1,18 verfehlt das knapp.
- **Alter des Effekts:**
  - K-TSM verdient 2018–2021 (+17 bis +68 %) und verliert 2022 und 2023 (−4 % je Jahr).
  - K-LONG verliert 2018 (−13 %) und 2022 (−13 %), gewinnt 2023 aber +21 %.
  - Die Short-Seite bringt vor Kosten fast nichts (+5 % p. a.) und kostet Swap.
  - Das passt zur Literatur: Der Effekt ist stark in den Krypto-Hausse-Phasen und schwächer seit 2022.
- **Beta-Anteil:**
  - BTC halten (1× Nominal, 20 % Swap) kam auf Sharpe 0,34.
  - K-LONG hält im Schnitt nur 0,21 Nominal und vermeidet die Bärenphasen größtenteils.
  - Der Mehrwert gegenüber dem Halten liegt also im Timing, nicht nur im Markt.
- **Größte Unsicherheit sind die Kosten:**
  - Die FTMO-Swaps für Krypto sind unbekannt (angenommen 20 % p. a.); bei 10 % wäre K-LONG +8,5 bp/Tag.
  - Die Spreads sind Annahmen. Die echten FTMO-Spezifikationen sollten aus MT5 ausgelesen werden.
