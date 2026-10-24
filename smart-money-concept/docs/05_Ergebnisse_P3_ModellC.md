# Ergebnisse P3 – Modell C „Trend-Fortsetzung“

Stand: 24.10.2026

Grundlagen:
- Regeln: unverändert aus der Vorregistrierung `docs/04_P3_Vorregistrierung_ModellC.md`
- Code: `research/smc/strategy_c.py`, Lauf: `research/scripts/run_p3.py`; 11 neue Tests, darunter ein History-Invarianz-Test des ganzen Modells (42 Tests grün)
- In-Sample: Signale 01.01.2015–31.12.2023, 25 Instrumente, HistData M1 (Bid)
- Vollständige Tabellen je Jahr und Instrument: `research/results/p3_modell_c_in_sample.md`

## 1. Ergebnis

**Beide Varianten verfehlen die Kriterien deutlich. P3 ist damit gescheitert.** Der Hold-out 2024–2026 bleibt unberührt, T4 und T5 entfallen.

| Kriterium | Schwelle | C-MKT | C-LMT |
|---|---|---|---|
| Trades | | 1.586 | 803 |
| Netto-Erwartungswert | ≥ +0,10 R | **+0,015 R** | **−0,016 R** |
| t-Wert (kleinster aus iid, Tag, Woche) | ≥ 2,5 | **0,77** | **−0,56** |
| Netto-Profit-Factor | ≥ 1,2 | **1,06** | **0,95** |
| Jahre positiv | ≥ 6 von 9 | 6 von 9 | **4 von 9** |
| Instrumente positiv (≥ 10 Trades) | ≥ 60 % | **48 %** | **48 %** |
| Erwartungswert bei doppelten Kosten | > 0 | +0,004 R | **−0,028 R** |
| Trefferquote | | 50,2 % | 45,8 % |
| Ø Kosten | | 0,011 R | 0,013 R |

Fett = Kriterium verfehlt. C-MKT ist in 2021–2023 jedes Jahr negativ.

**Ausstiege**

| | Ziel | Stop | Zeit-Stopp (3 Handelstage) |
|---|---|---|---|
| C-MKT | 2 % (Ø +2,01 R) | 10 % (Ø −1,04 R) | 88 % (Ø +0,10 R) |
| C-LMT | 2 % (Ø +2,30 R) | 17 % (Ø −1,06 R) | 81 % (Ø +0,13 R) |

**C-LMT im Detail**
- Von 1.586 Signalen wurden 803 gefüllt. 612 Orders liefen nach 24 Handelsstunden ab, 129 wurden storniert, weil der Kurs vorher das Ziel erreichte. Bei 14 Signalen gab es keine Zone, 28 scheiterten am Kosten-Gate.
- Fast alle Einstiege kamen über ein FVG (788), nur 15 über einen Order-Block.
- Gefüllte Limit-Trades sind schlechter als der Markteinstieg. Das passt zu adverser Selektion: Gefüllt wird vor allem, wenn die Fortsetzung zunächst ausbleibt.

## 2. Warum es nicht trägt

Diese Diagnose entstand nach dem Lauf. Sie erklärt das Ergebnis, ist aber kein neuer Befund.

1. **Der Struktur-Stop ist sehr weit.**
   - Abstand Einstieg → Stop im Median 9,3 × ATR14(H1), Spanne P10–P90 5,8–15,1.
   - Das sind 2,2 × ATR14(D1), bei EURUSD im Median 171 Pips (P10–P90 106–324).
   - Grund: Der Anker ist das Extrem des ganzen beendeten H1-Gegen-Swings, und der H1-Swing-Layer arbeitet mit 30er-Pivots.
2. **Ziel und Zeit-Stopp passen nicht zu diesem Stop.**
   - 2 R entsprechen hier etwa 4–5 Tagesspannen. Das schafft der Kurs in 3 Handelstagen fast nie: Nur 2 % der Trades erreichen das Ziel.
   - Bei 86 % der Trades gab es keinen Liquiditätspool jenseits von 2 R. Das Ziel war dann pauschal 2 R.
3. **Der Effekt in Kursbewegung ist derselbe wie in P2.**
   - Vor Kosten bringt C-MKT +0,026 R pro Trade. In ATR(H1) gemessen sind das +0,13 ATR(H1) je Trade.
   - P2 hatte mit engem Stop (1 ATR(H1)) fast genau denselben Wert gemessen: +0,14 ATR(H1).
   - Das Signal bewegt den Kurs also im Mittel um gut ein Achtel einer Stundenspanne. Am weiten Stop gemessen ist das nahe null.
   - Der positive Schnitt der Zeit-Stopp-Trades (+0,10 R) taugt nicht als Beleg. Diese Gruppe enthält nur Trades, die den Stop nicht erreicht haben, und ist daher nach oben verzerrt.
4. **Kosten sind diesmal nicht das Problem.**
   - Bei diesem Stop machen sie nur 0,01 R aus.
   - Damit entfällt auch die Begründung des Ausweichplans aus P2 (`docs/03`, §4.4), auf H4/D1 zu wechseln, um Kosten zu sparen.
   - Das Problem ist das fehlende Brutto-Edge in R.

**FTMO-Folge:** Bei einem Erwartungswert um 0 liegt die Bestehenschance für beide Phasen laut Monte-Carlo bei etwa 35–42 % (`research/results/ftmo_mc_results.md`). Das wäre im Wesentlichen Glück.

## 3. Was bisher feststeht

- **P2:** 13 SMC-Bausteine einzeln getestet. Kein Baustein ist nach Kosten profitabel. Das ICT-Kernmodell (Sweep → MSS) zeigt keinen Effekt.
- **P3:** Der einzige Kandidat aus P2 ist als vollständige Strategie mit SMC-Stop und Liquiditätsziel getestet. Er zeigt kein Edge.
- **Mechanisch definiertes SMC hat in 9 Jahren × 25 Instrumenten bisher kein verwertbares Edge gezeigt.** Das gilt für die hier getesteten Definitionen. Die Engine selbst ist kausal und getestet und bleibt nutzbar.

## 4. Optionen für den nächsten Schritt

| Option | Inhalt | Einschätzung |
|---|---|---|
| **A – Trendfolge mit Struktur-Exit** (letzter SMC-Versuch) | Einstieg wie C-MKT, Stop am Anker. Kein festes Ziel: Ausstieg, wenn der strikte H1-Trend wieder kippt. Das wirkt wie ein Trailing-Stop am jeweils neuen Protected Level. Längste Haltedauer 20 Handelstage. | Behebt den Widerspruch zwischen weitem Stop und kurzem Horizont und ist die Trendfolge-Lesart des einzigen Signals mit messbarem Effekt. Die Idee entstand aber nach Sichtung der IS-Daten. Deshalb neue Vorregistrierung mit strengerer Schwelle (t ≥ 3,0). Erfolgsaussicht: eher gering. Aufwand: etwa ein halber Tag. |
| B – Swing-Variante H4/D1 (ursprünglicher Ausweichplan) | D1-Trend als Filter, H4-Trendwechsel als Signal, Stop am H4-Anker | Begründung „Kosten“ entfällt (siehe 2.4). In P2 zeigten H4-Trendwechsel keinen Effekt (+0,015 R). Nicht empfohlen. |
| C – SMC-Regelwerk verlassen | Strategieklassen mit besserer Evidenz, z. B. Fixing-Effekte (Kapitel 5, §1.4) oder Trendfolge auf D1 mit Volatilitäts-Sizing; gleiche Testkette | Weicht vom Projektziel „SMC-EA“ ab, ist aber ehrlicher, wenn A scheitert. |
| D – Pausieren | Ergebnisse festhalten, keine Challenge kaufen | Das negative Ergebnis ist selbst ein belastbarer Befund. |

**Empfehlung:** Option A als letzter vorregistrierter SMC-Test. Scheitert A, Entscheidung zwischen C und D. **Keine bezahlte Challenge**, bevor ein Modell In-Sample und Hold-out bestanden hat.

## 5. Umsetzungsdetails, die die Vorregistrierung offen ließ

Diese Punkte wurden vor dem ersten Lauf im Code festgelegt (Modul-Docstring `strategy_c.py`). Sie sind konservativ gewählt:

- **Storno „Ziel erreicht“:** Für Pending-Orders gilt das Ziel, das eine Order bei Fill in der ersten Kerze nach dem Signal bekäme.
- **Reihenfolge innerhalb einer Kerze:** Ein Storno geht dem Fill vor. Das betrifft H4-Trend zur Eröffnung, Eröffnung jenseits des Stops und erreichtes Ziel.
- **Gaps:** Ein Stop, über den der Kurs springt, wird zur Eröffnung gefüllt. Ziel und Limit-Einstieg werden zum eigenen Preis gefüllt, ohne Kursverbesserung.
- **Pools bei Limit-Fill:** Wird ein Pool in der Fill-Kerze durchstochen, gilt er als bereits durchstochen.
- **„Durchstochen“** heißt: erster Docht jenseits des Levels; Buy-Side-Pools auf Ask-Basis mit Raw-Spread, wie in der Pipeline.
- **Stop-Puffer:** Der „typische Spread“ ist der Raw-Spread.
- **Kosten-Gate:** Grundlage ist der P2-Round-Trip aus Spread, Kommission und einmal Slippage.
- **Zonen:** Eine Zone muss beim Signal noch ganz hinter dem Kurs liegen, sonst wäre die Limit-Order ungültig.

## 6. Trial-Log (Fortsetzung)

| # | Datum | Test | Ergebnis |
|---|---|---|---|
| T2 | 24.10.2026 | C-MKT, In-Sample 2015–2023 | nicht bestanden: +0,015 R netto, t 0,77, PF 1,06 |
| T3 | 24.10.2026 | C-LMT, In-Sample 2015–2023 | nicht bestanden: −0,016 R netto, t −0,56, PF 0,95 |
| T4 | – | Hold-out | entfällt, Hold-out unberührt |
| T5 | – | Portfolio und FTMO-Bootstrap | entfällt |
