# Ergebnisse P4 – Modell D „Trendfolge mit Struktur-Exit“

Stand: 24.10.2026

Grundlagen:
- Regeln: unverändert aus der Vorregistrierung `docs/06_P4_Vorregistrierung_ModellD.md`
- Code: `research/smc/strategy_d.py`, Swaps `research/smc/swaps.py`, Lauf `research/scripts/run_p4.py`; 50 Tests grün, darunter der History-Invarianz-Test von Modell D
- In-Sample: Signale 01.01.2015–31.12.2023, 25 Instrumente
- Vollständige Tabellen je Jahr und Instrument: `research/results/p4_modell_d_in_sample.md`

## 1. Ergebnis

**Modell D verfehlt alle sechs Kriterien. P4 ist damit gescheitert.** Der Hold-out 2024–2026 bleibt unberührt, T7 und T8 entfallen.

| Kriterium | Schwelle | Modell D |
|---|---|---|
| Trades | | 1.586 |
| Netto-Erwartungswert | ≥ +0,10 R | **−0,040 R** |
| t-Wert (kleinster aus iid, Tag, Woche, Monat) | ≥ 3,0 | **−1,33** |
| Netto-Profit-Factor | ≥ 1,2 | **0,91** |
| Jahre positiv | ≥ 6 von 9 | **4 von 9** |
| Instrumente positiv (≥ 10 Trades) | ≥ 60 % | **44 %** |
| Erwartungswert bei doppelten Kosten | > 0 | **−0,090 R** |

| Kennzahl | Wert |
|---|---|
| Trefferquote | 36,3 % |
| Ø Gewinner / Ø Verlierer | +1,13 R / −0,70 R |
| größter Gewinner / P90 der Gewinner | +10,1 R / +2,65 R |
| Ø Kosten gesamt | 0,050 R, davon Swaps 0,029 R und 0,7-%-Gebühr 0,005 R |
| Haltedauer | Median 9,5, Mittel 10,7 Handelstage |

| Ausstieg | Anteil | Ø Ergebnis |
|---|---|---|
| Struktur-Exit (H1-Trend kippt) | 51 % | +0,04 R |
| Stop | 31 % | −1,04 R |
| Zeit-Stopp nach 20 Handelstagen | 18 % | +1,45 R |

## 2. Einordnung

1. **Längeres Halten bringt keinen Vorteil.**
   - Vor Kosten liegt Modell D bei etwa +0,01 R pro Trade. C-MKT kam mit 3 Tagen Haltedauer auf +0,026 R.
   - Die Fortsetzung nach dem Signal wächst also nicht mit der Haltedauer.
2. **Die Gewinner laufen, gleichen aber nur die Verluste aus.**
   - Die Trend-Trades bis zum Zeit-Stopp bringen +1,45 R.
   - Dem stehen 31 % Stop-Treffer mit je −1 R gegenüber, dazu die vielen Struktur-Exits um null.
3. **Swaps sind spürbar, aber nicht der Grund.**
   - Bei etwa 10 Handelstagen Haltedauer kosten sie 0,03 R pro Trade.
   - Ohne Swaps und Gebühr läge Modell D immer noch bei −0,006 R.
4. **Kein Muster trägt.**
   - Nur 4 von 9 Jahren und 11 von 25 Instrumenten sind positiv.
   - Einzelne Instrumente stechen heraus (XAUUSD +0,41 R, AUDJPY +0,22 R). Bei 25 Instrumenten ist das auch zufällig zu erwarten. Sie nachträglich herauszupicken wäre Data Snooping.

## 3. Gesamtbild nach P2–P4

| Phase | Getestet | Ergebnis |
|---|---|---|
| P2 | 13 SMC-Bausteine einzeln, gegen Placebo | Kein Baustein nach Kosten profitabel. Sweep → MSS ohne Effekt |
| P3 | Bestes Signal als vollständige Strategie, Markt- und Limit-Einstieg | +0,015 R bzw. −0,016 R, kein Edge |
| P4 | Dasselbe Signal als Trendfolge mit Struktur-Exit | −0,040 R, kein Edge |

- **Laut Vorregistrierung (`docs/06`, §5) ist der SMC-Ansatz damit beendet.** Der Hold-out 2024–2026 wurde nie angefasst und steht für eine andere Hypothese weiter unverbraucht zur Verfügung.
- Das deckt sich mit der Literatur (Kapitel 5, §1.6): Regelbasierte technische Analyse auf G10-FX zeigt seit den 1990er-Jahren nach realistischen Kosten kaum noch Überrenditen.
- **Bleibender Nutzen:** Folgendes ist wiederverwendbar:
  - Zeitmodell und Daten
  - kausale Engine
  - Kosten- und Swap-Modell
  - Testkette aus Vorregistrierung, In-Sample, einmaligem Hold-out und FTMO-Bootstrap
- Das Ergebnis kam heraus, ohne Geld in eine Challenge zu stecken.

**FTMO ohne Edge:** Bei einem Erwartungswert um 0 liegt die Bestehenschance beider Phasen bei etwa 35–42 % (Monte-Carlo, `research/results/ftmo_mc_results.md`). Das ist ein Glücksspiel mit der Challenge-Gebühr als Einsatz.

## 4. Optionen

| Option | Inhalt | Einschätzung |
|---|---|---|
| **C1 – Fixing-Effekt** | USD wertet vor dem Tokio-, EZB- und London-Fix auf und danach wieder ab (Krohn, Mueller & Whelan 2024, Journal of Finance; 21 Jahre, 9 Währungen) | Beste Evidenz mit klarem Mechanismus (Inventarrisiko der Dealer). Ohne Kosten stark positiv; ob das nach FTMO-Kosten trägt, ist offen, weil die Bewegungen intraday und klein sind. Kein SMC mehr |
| C2 – Trendfolge auf D1 | Zeitreihen-Momentum über alle 25 Instrumente mit Volatilitäts-Sizing | Gut dokumentiert, Kosten unkritisch. Bei G10-FX seit etwa 2010 aber schwach, und wenige Trades machen die Challenge langsam |
| D – Pausieren | Ergebnisse festhalten, keine Challenge kaufen | Ehrlichste Option, wenn der SMC-Ansatz das Ziel war |

Jede neue Hypothese läuft durch dieselbe Testkette: Vorregistrierung, In-Sample, einmal Hold-out, FTMO-Bootstrap. Eine Challenge wird erst gekauft, wenn ein Modell alle Stufen besteht.

## 5. Trial-Log (Fortsetzung)

| # | Datum | Test | Ergebnis |
|---|---|---|---|
| T6 | 24.10.2026 | Modell D, In-Sample 2015–2023 | nicht bestanden: −0,040 R netto, t −1,33, PF 0,91 |
| T7 | – | Hold-out | entfällt, Hold-out unberührt |
| T8 | – | Portfolio und FTMO-Bootstrap | entfällt |

Bisher verbraucht: T1 (110 Hypothesen der Ereignisstudie), T2, T3 und T6. Der Hold-out 2024–2026 ist unberührt.
