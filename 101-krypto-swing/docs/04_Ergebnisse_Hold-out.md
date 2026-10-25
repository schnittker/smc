# Ergebnisse Hold-out: K-LONG nach Ausnahmeregel (Strategie Nr. 101, T317)

Läufe vom 25.10.2026, Regeln laut `03_Nachtrag_Hold-out.md`. Vollständige Tabellen in `research/results/k_holdout.md`.

## Zwei Läufe – Fehler in der Datumsgrenze

- **Lauf 1 (fehlerhaft):** Die Konstante `LAST_DAY` war um genau ein Jahr falsch (24.10.2025 statt 24.10.2026). Der Hold-out umfasste dadurch nur 2024 bis Oktober 2025.
  - +5,34 bp/Tag, Sharpe 0,81; alle drei Hold-out-Kriterien erfüllt
  - FTMO-Bootstrap: keine Stufe bestanden (0,5 %: 76 % in 16 Monaten; 0,75 %: 42 %)
  - Die Datei ist aufbewahrt in `research/results/k_holdout_lauf1_bis_2025-10-24.md`.
- **Lauf 2 (maßgeblich, vorregistrierter Zeitraum bis 24.10.2026):** Er wurde nach Fix und Commit (`97616a9`) einmal wiederholt.

## Ergebnis (Lauf 2)

| | IS 2018–2023 | Hold-out 2024–10/2026 |
|---|---|---|
| Netto je Tag | +7,93 bp | +2,93 bp |
| Sharpe | 1,18 | **0,48** |
| t (kleinster) | 2,57 | 0,54 |
| Jahre | 4 von 6 positiv | 2024 +44,6 %, 2025 −9,3 %, 2026 −5,1 % |

| Kriterium | Ergebnis | erfüllt |
|---|---|---|
| Mittel > 0 | +2,93 bp/Tag | ja |
| ≥ untere IS-Grenze | +2,93 vs. [+2,17; +14,35] | ja |
| Sharpe ≥ 0,5 (Nachtrag) | 0,48 | **nein** |

**T317 nicht bestanden, T318 (FTMO) entfällt.** Auch Lauf 1 hätte am FTMO-Kriterium nicht bestanden.

## Einordnung

- **Der gesamte Hold-out-Gewinn stammt aus dem Krypto-Bullenjahr 2024.** Seit 2025 verliert die Regel.
- **Die Hälfte des Ergebnisses fällt am Wochenende an** (52 % des Gewinns an 29 % der Tage). Dort hat FTMO Wartungsfenster.
- **Gegen das reine Halten von BTC:** Halten kam im Hold-out auf Sharpe 0,30 (mit 20 % Swap). Die Regel lag mit 0,48 darüber, aber nicht weit genug für FTMO.
- **Bei 10 % statt 20 % Swap:** +3,61 bp/Tag, Sharpe ~0,6. Das hätte die Nachtrags-Hürde knapp genommen. Die Kostenannahme ist hier also mitentscheidend.
- **FTMO-Bootstrap aus Lauf 1:** Selbst mit dem günstigeren Zeitraum bestand keine Stufe. Grund sind die Krypto-Crashtage gegen das 5-%-Tageslimit; die Bestehenschance fiel ab 0,75 % Tagesschwankung auf ≤ 42 %.
- **Der Hold-out für Krypto-Trendfolge ist verbraucht.**
