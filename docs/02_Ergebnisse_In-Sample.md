# Ergebnisse Strategie Nr. 5 – Modell M „Monatsend-Rebalancing am London-Fix“

Stand: 24.10.2026

Grundlagen:
- Regeln: unverändert aus der Vorregistrierung `docs/01_Vorregistrierung.md` (Commit `153252e`)
- Code: `research/mer/`, Lauf `research/scripts/run_m.py` (Commit `fff8ff1`); 37 Tests grün
  - Die Trade-Mechanik reproduziert Modell F aus dem SMC-Projekt exakt (Test `test_trade_reproduces_model_f`).
- In-Sample: Monatsenden 2015–2023, HistData M5
- Vollständige Tabellen: `research/results/m_in_sample.md`

## 1. Ergebnis

**Beide Varianten verfehlen alle vier Kriterien. Strategie Nr. 5 ist damit gescheitert.** Der Hold-out 2024–2026 bleibt unberührt, T21 und T22 entfallen.

| Kriterium | Schwelle | M-1H (14:55–16:00) | M-DAY (08:00–16:00) |
|---|---|---|---|
| Netto je Ereignis | > 0 | **−4,41 bp** | **−7,10 bp** |
| t-Wert (kleinster aus iid, Quartal) | ≥ 3,0 | **−1,01** | **−1,04** |
| Sharpe Ratio p. a. | (≈ 1,0) | −0,34 | −0,31 |
| Jahre positiv | ≥ 6 von 9 | **3 von 9** | **3 von 9** |
| Paare positiv | ≥ 3 von 4 | **1 von 4** | **1 von 4** |
| bei doppelten Kosten | > 0 | **−10,2 bp** | **−11,8 bp** |
| vor Kosten je Ereignis | – | +1,35 bp | −2,42 bp |
| Kosten je Ereignis | – | 5,76 bp | 4,68 bp |

Ein Ereignis umfasst bis zu 4 Positionen. Die Kosten liegen bei etwa 1,2–2,1 bp je Position, einschließlich 0,5 Pip Slippage am Fix.

## 2. Einordnung

1. **Der Effekt aus dem Paper ist 2015–2023 nicht mehr messbar.**

   | Regression wie im Paper | Steigung (bp je % relativer Aktienrendite) | t-Wert | R² |
   |---|---|---|---|
   | Melvin & Prins, 2004–2012, 15–16 Uhr | ≈ −1,4 | signifikant | 0,03 |
   | hier, 2015–2023, 14:55–16:00 | −0,15 | −0,31 | 0,000 |
   | hier, 2015–2023, 08:00–16:00 | +0,51 | +0,61 | 0,002 |

   Das Vorzeichen stimmt in der Fix-Stunde noch, die Stärke liegt aber bei einem Zehntel. Das passt zu den vorab genannten Gründen: Fix-Reform 2015 mit 5-Minuten-Fenster, Strafverfahren wegen Fix-Manipulation und Vorab-Veröffentlichung der Flow-Schätzungen durch die Banken.
2. **Schon vor Kosten kein Vorteil.**
   - M-1H bringt vor Kosten +1,35 bp je Ereignis, also etwa +0,3 bp je Position. Die Kosten sind fünfmal so hoch.
   - M-DAY ist schon vor Kosten negativ.
3. **Keine Teilmenge rettet das Ergebnis** (beschreibend, ohne Einfluss auf die Entscheidung):
   - Gewichtung mit der Größe des Signals: M-1H −2,0 bp (t −0,3), M-DAY −13,7 bp
   - Nur Quartalsenden: −3,2 bp bzw. −10,7 bp
   - 2014, vor der Fix-Reform: M-1H vor Kosten +4,6 bp, netto −0,9 bp. Mit 11 Ereignissen ist das keine Aussage.
   - GBPUSD ist in M-1H als einziges Paar positiv (+3,2 bp netto, t 1,55). Bei 4 Paaren und 2 Varianten ist das im Rahmen des Zufalls.
4. **Kein Ausreißer-Artefakt.**
   - Das schlechteste Ereignis ist der 30.11.2021 mit −199 bp in M-1H: alle vier Positionen ausgestoppt, zeitgleich mit Powells „transitory“-Aussage vor dem US-Senat um 10:00 New York.
   - Ohne die zwei schlechtesten Ereignisse bleibt M-1H negativ (−1,7 bp). Der Median liegt bei −5,9 bp.
5. **Umkehr nach dem Fix** (beschreibend):
   - Die Gegenposition von 16:05 bis 12:00 am nächsten Geschäftstag bringt +14,6 bp netto je Ereignis (t 1,26), bei M-DAY-Signalen +16,6 bp (t 1,38).
   - Das ist nicht signifikant. Die Position hält über den Rollover (Swaps nicht gerechnet), und 20–27 % der Positionen werden ausgestoppt.
   - Die Idee stammt aus denselben In-Sample-Daten. Ein Test als eigene Strategie hätte deshalb nur im Hold-out echte Aussagekraft.
   - **Nicht weiterverfolgen**, solange es bessere Kandidaten mit externer Evidenz gibt.

**Datenhinweis M-DAY:** HistData hat für den CAC 40 erst ab 07:00 UTC Kurse, für den FTSE erst ab 08:00 UTC. Um 08:00 London fehlt im Sommer deshalb ein aktueller Indexkurs, und nach der vorregistrierten 6-Stunden-Regel entfällt das Paar. EURUSD wurde in M-DAY nur in 31 Monaten gehandelt (fast nur im Winter), GBPUSD in 67. Das Urteil ändert sich dadurch nicht: Auch USDJPY und AUDUSD liegen nicht über den Kosten, und die gepoolte Regression zeigt keinen Effekt. Im Live-Betrieb hätte der EA um 08:00 London Kurse für FRA40.cash.

## 3. Bezug zu den festen Rahmenbedingungen

Selbst mit Effekt wäre die Strategie allein für FTMO kaum geeignet, wie vorab festgehalten: ein Handelsfenster pro Monat bei +10 % und +5 % Ziel und 5 % Tagesgrenze. Diese Frage stellt sich nicht mehr.

## 4. Trial-Log (Fortsetzung)

| # | Datum | Test | Ergebnis |
|---|---|---|---|
| T19 | 24.10.2026 | M-1H, In-Sample | nicht bestanden: −4,41 bp/Ereignis, t −1,01, Sharpe −0,34 |
| T20 | 24.10.2026 | M-DAY, In-Sample | nicht bestanden: −7,10 bp/Ereignis, t −1,04, Sharpe −0,31 |
| T21 | – | Hold-out | entfällt, Hold-out unberührt |
| T22 | – | FTMO-Bootstrap | entfällt |

Die Ausreißer- und Abdeckungsprüfungen in Abschnitt 2 sind beschreibende Diagnosen, keine neuen Trials.
