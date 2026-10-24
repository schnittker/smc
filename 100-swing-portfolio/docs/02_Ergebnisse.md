# Ergebnisse: Swing-Portfolio (Strategie Nr. 100)

Läufe vom 24.10.2026. Die vollständigen Tabellen stehen in `research/results/s_in_sample.md` und `research/results/s_holdout.md`.

## In-Sample 2015–2023 (T306, beschreibend)

| Baustein | Gewicht | Sharpe | Beitrag p. a. |
|---|---|---|---|
| P-SPX | 5,83 | 0,84 | +8,4 % |
| T-FRÜH | 1,42 | 0,56 | +5,6 % |
| V-VOL | 0,59 | 0,56 | +5,6 % |
| F-CARRY | 1,93 | 0,69 | +6,9 % |
| **Portfolio** | | **1,13** (t 3,37) | +26,5 % bei 23 % Vola |

- Die Korrelationen der Tagesreihen liegen bei 0,03–0,32.
- 8 von 9 Jahren sind positiv.
- Das Ergebnis ist wie angekündigt verzerrt, weil nur die besten aus ~130 Versuchen ausgewählt wurden.

**Klumpenrisiko:** Selbst auf diesen geschönten IS-Daten erfüllt keine FTMO-Stufe das Kriterium.

| Tagesschwankung | P(beide Phasen) | Median-Dauer |
|---|---|---|
| 0,5 % | 81 % | 18 Monate |
| 0,75 % | 60 % | 10 Monate |
| 1,0 % | 38 % | – |

Der Grund sind die Tage, an denen drei US500-Long-Bausteine zusammenfallen. Am 27.01.2021 lagen FOMC-Tag, ein Monatswechsel-Trade (Stopp) und V-VOL gleichzeitig long, und der US500 fiel um 2,6 %. Auf der 1-%-Stufe sind das −17 % an einem Tag. Die niedrige Durchschnittskorrelation verdeckt, dass die Extreme gemeinsam auftreten. Das P-SPX-Gewicht von 5,8× auf wenige Ereignistage ist für das FTMO-Tageslimit ungeeignet.

## Hold-out 01.01.2024–16.10.2026 (T307, einmalig)

| Baustein | Sharpe IS | Sharpe Hold-out |
|---|---|---|
| P-SPX | 0,84 | 0,16 |
| T-FRÜH | 0,56 | 0,20 |
| V-VOL | 0,56 | **0,59** |
| F-CARRY | 0,69 | −0,98 |
| **Portfolio** | 1,13 | **0,17** |

**Portfolio:**
- +1,40 bp/Tag, IS-95-%-Intervall [+4,59; +15,99]
- Jahre: 2024 +23 %, 2025 +6 %, 2026 −19 %

**Kriterium 2 verfehlt: nicht bestanden.** T308 (FTMO) entfällt.

## Einordnung

- **Auswahlverzerrung bestätigt:** Die drei „Anomalie“-Bausteine (FOMC-Drift, Monatswechsel, FOMC-FX) fallen im Hold-out auf etwa null oder darunter. Ihre IS-t-Werte von 1,7–2,4 waren nach rund 130 Versuchen das, was man vom Zufall erwartet.
- **Nur V-VOL hält.** Das ist keine Anomalie, sondern die Aktien-Risikoprämie (US500 long) mit Volatilitätssteuerung; Sharpe ~0,55 in IS wie in Hold-out. Auch reines Halten kam in IS auf 0,51.
- **Der Hold-out von Nr. 9, 10, 14 und 24 ist verbraucht.** Die Marker liegen in deren `data/*/ho/DONE`.
