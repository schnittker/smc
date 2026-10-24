# Smart Money Concept (SMC/ICT) – Deep-Research-Zusammenfassung

Stand: 24.10.2026 · Ziel: Grundlage für einen autonom handelnden MT5-EA auf 25 Instrumenten (24 FX-Paare + XAUUSD)

**Einsatzziel:** Die **FTMO 2-Step Challenge** bestehen, Swing-Konto, 100.000 USD.
- Phase 1: +10 %, Phase 2: +5 %
- Max Loss 10 % statisch, Max Daily Loss 5.000 USD auf Basis der Balance um 00:00 Prager Zeit
- 4 Handelstage je Phase, kein Zeitlimit
- Übernacht- und News-Trading erlaubt

Regeln, Risikoleiter und Schutzmodul stehen in `02_FTMO_Challenge_Plan.md`.

**Wo was steht**
- `docs/00_SMC_Deepsearch_Zusammenfassung.md`: dieses Dokument, der Einstieg und die Kurzreferenz.
- `docs/01_EA_Blueprint.md`: die daraus abgeleitete EA-Spezifikation v0.1 mit Architektur, Regeln, Parametern, Risiko und Testplan.
- `docs/02_FTMO_Challenge_Plan.md`: FTMO-Regelwerk als EA-Spezifikation (FtmoGuard), Monte-Carlo-Bestehenschancen, Risikoleiter, Margin- und Kostenfolgen, Ablauf bis zum Kauf.
- `docs/research/01–08_*.md`: acht ausführliche Research-Kapitel mit insgesamt rund 44.000 Wörtern, Pseudocode und allen Quellen-URLs. Verweise in diesem Dokument: `K3 §4` = Kapitel 3, Abschnitt 4.

**Zur Quellenlage:** ICT (Michael J. Huddleston) hat kein schriftliches Regelwerk veröffentlicht. ICT-Aussagen stammen aus Transkripten und Mitschriften der 2022 Mentorship sowie aus Drittseiten; die meisten Zahlenschwellen stammen von Educators, nicht von ICT. Code-Implementierungen wurden im Quelltext gelesen (LuxAlgo-Pine, Python-Library, MQL5-Artikel, GitHub). Bei einigen Papern war nur das Abstract zugänglich; das ist in den Kapiteln markiert.

---

## 1. Die wichtigsten Erkenntnisse

1. **SMC ist kein festes Regelwerk.** Es ist ein Sammelbegriff aus ICT-Konzepten und Community-Varianten. Fast jeder Begriff hat mehrere konkurrierende Definitionen: Order Block, CHoCH vs. MSS, Inducement, Dealing Range, Mitigation. ICT nennt kaum Zahlen. *Jede* Definition im EA ist deshalb eine Design-Entscheidung, die parametriert und empirisch geprüft werden muss.

2. **Der Kern lässt sich objektiv programmieren:**
   - Swings als Pivots mit Bestätigungs-Lag
   - BOS und CHoCH per Kerzen-Close
   - Liquiditätspools: Swings, EQH/EQL, Session-Hochs und -Tiefs, PDH/PDL, PWH/PWL
   - Sweep (Docht durch das Level, Close zurück) vs. Break (Akzeptanz jenseits)
   - Fair Value Gap aus drei Kerzen
   - Order Block als letzte Gegenkerze vor dem Displacement
   - Displacement als Body in ATR-Einheiten
   - Premium/Discount als 50 % der Dealing Range
   - Killzones in New-York-Zeit

3. **Schwer zu automatisieren** sind Inducement, die Wahl des „richtigen“ OB, der Anker der Dealing Range, der Bias und das ICT-„Narrativ“. Market-Maker-Modelle und Weekly Profiles lassen sich praktisch nur im Nachhinein klassifizieren.

4. **Lookahead ist die größte Falle.** Die populäre Python-Library `smartmoneyconcepts` erkennt Swings mit einem zentrierten Fenster, das zukünftige Bars nutzt. Dieselbe Strategie (XAUUSD M15, 10 Jahre) zeigt damit **PF 7,32**, kausal korrekt nur **PF 1,82** (→ K1 §1.3, K4 §2). Auch viele MQL5-Artikel lesen die offene Bar oder HTF-Daten mit Lookahead (→ K4 §3).

5. **Die Evidenz ist dünn bis negativ** (→ K5, K4 §4, K7 §9):
   - **Peer-Review:** keine Arbeit zu SMC/ICT als Gesamtsystem.
   - **Mechanische Tests mit Kosten bzw. Out-of-Sample:**

     | Test | Ergebnis |
     |---|---|
     | Silver Bullet auf NQ | PF 0,58 |
     | ICT-Bot EURUSD | PF 0,81 |
     | London-Breakout EURUSD | PF 0,64–0,80 |
     | StatOasis, 648 Backtests | 31 von 32 Ereignistests nicht signifikant |
     | fxbacktest, Sweep/Reclaim an PDH/PDL (22 Instrumente, 11.990 Trades) | kein signifikanter Effekt |

   - **Ohne Bestätigung schadet es:** Unbestätigtes Fading an Liquidität ist signifikant **schlechter** als Zufall (40,9 % gegenüber 49,4 %).
   - **Richtung nach dem Sweep:** Ein SSRN-Preprint findet, dass Sweeps eher **Fortsetzung** als Umkehr vorhersagen; gelesen wurde nur das Abstract.

6. **Gut belegte Mechanismen** (→ K5 §1):
   - Order- und Stop-Cluster an runden Zahlen und Extremen sowie Stop-Kaskaden (Osler)
   - starke Intraday-Saisonalität von Volatilität und Volumen
   - Fixing-Effekte (WM/R 16:00 London, Tokio-Fix; Krohn et al. 2024)

   Sie erklären, **wo und wann** Bewegung entsteht, aber **nicht die Richtung**. Killzones sind als Volatilitätsfilter begründet, nicht als Richtungssignal.

7. **Das beste gefundene Ergebnis ist ein kleiner Edge vor Kosten** (MrOwl1011, → K4 §4):
   - Setup: H1-Order-Block, dann M5-CISD, mit Trendfilter.
   - 813 Trades, **+0,109 R pro Trade, PF 1,25**.
   - Ohne Trendfilter ≈ 0 R. Der **Trendfilter ist der dominante Faktor**.
   - Mit Kosten bleibt davon voraussichtlich wenig.

8. **Kosten entscheiden über die Paarwahl** (→ K7 §9.3):
   - Für M5-Entries günstig genug (Kosten < 15 % eines 1×ATR(M5)-Stops) sind nur **EURUSD, GBPUSD, USDJPY, EURJPY, GBPJPY und XAUUSD**.
   - AUDNZD liegt bei ≈ 47 % und ist damit praktisch nicht handelbar.
   - Die teuren Crosses kommen nur mit M15/H1 in Frage.

9. **Die 25 Symbole sind faktisch 8 Währungen plus Gold.**
   - USD steckt in 8 Symbolen, JPY in 7.
   - Realistisch sind 4–6 unabhängige Positionen gleichzeitig möglich.
   - Das Risiko muss deshalb **pro Währung** gesteuert werden (Exposure-Vektor), nicht pro Symbol (→ K5 §6.3, K6 §10, K7 §4).

10. **MT5 hat Plattform-Fallen** (→ K6):
    - `OnTick` feuert nur für ein Symbol, also braucht ein Multi-Symbol-EA Timer-Polling.
    - Im Tester gilt `TimeGMT()` = Serverzeit, deshalb ist eine eigene Sommerzeit-Logik nötig.
    - Der Wirtschaftskalender ist im Tester gesperrt, daher CSV-Export.
    - Tick-Value-Fehler, unterschiedliche Filling-Konstanten, Minimal-Spread im Tester.
    - Die Tick-Historie beim Broker ist oft kurz, daher externe Tickdaten.

11. **Alle ICT-Zeitfenster sind in NY-Zeit definiert.**
    - US- und EU-Sommerzeit wechseln an verschiedenen Tagen. In den Abweichungswochen verschieben sich London-Zeiten gegenüber NY.
    - Die nächste Abweichungswoche ist **25.10.–01.11.2026, ab morgen**.

12. **Realistische Erwartung:**
    - Nach Kosten bestenfalls PF ≈ 1,1–1,4 bzw. +0,05 bis +0,2 R pro Trade.
    - Vom Backtest zum Live-Handel fällt die Sharpe Ratio im Median um 73 %.
    - Ein statistischer Nachweis braucht **mehrere hundert bis ≈ 2.000 Out-of-Sample-Trades** (→ K5 §5.4, §7).

**Konsequenz:**
- Der EA wird als **kausal saubere SMC-Feature-Engine mit Research- und Validierungsschicht** gebaut.
- Handelsmodelle sind Module. Sie gehen erst live, wenn sie Ereignisstudien gegen Placebo und Walk-Forward-Tests bestanden haben (Blueprint §16).

---

## 2. Begriffslandkarte: SMC-Konzept → EA-Regel (Kurzreferenz)

„Default“ ist die Entscheidung im Blueprint; Alternativen und Herleitung stehen im jeweiligen Kapitel.

### 2.1 Marktstruktur

| Konzept | Bedeutung | EA-Regel (Default) | Kapitel |
|---|---|---|---|
| Swing High/Low | lokales Extrem | Leg-Pivot (LuxAlgo-Logik), bestätigt nach L Bars; Ursprungs- und Bestätigungszeit getrennt. ICT-STH/STL = 3-Kerzen-Fraktal (n = 1) | K1 §1 |
| HH/HL/LH/LL | Vergleich mit dem Vorgänger-Pivot | Innerhalb ±0,1·ATR200 als EQH/EQL labeln | K1 §2.1 |
| Internal vs. External | kleine vs. große Swings | L_int = 5; L_ext je TF (D1 10, H4 20, H1 30, M15 40, M5 50) | K1 §2.3 |
| **BOS** | Bruch in Trendrichtung | **Close** jenseits eines bestätigten, noch ungebrochenen Swings, ein Bruch pro Pivot | K1 §3 |
| **CHoCH** | erster Bruch gegen den Trend | INT-Layer: jeder Gegenbruch. EXT-Layer: Trend kippt nur bei Close jenseits des Protected Level | K1 §2–3 |
| **MSS** | CHoCH mit Displacement nach einem Sweep | LTF-CHoCH (Close über STH) + Sweep ≤ 20 Bars davor + Displacement (+ FVG im Leg) | K1 §3 |
| Strong/Weak, Protected High/Low | „geschützte“ Extreme | `protL` = tiefstes Low zwischen gebrochenem Hoch und Bruch-Bar | K1 §2.4 |
| Inducement (IDM) | Köder-Liquidität vor dem POI | erstes internes Pivot nach dem Swing-BOS; ein POI ist erst nach dem IDM-Sweep „armed“ | K1 §3.5 |
| CISD | Change in State of Delivery | Close über dem Open der Down-Close-Serie ins Tief (früher als MSS, mehr Fehlsignale) | K3 §3 |
| Dealing Range | aktuelle Handelsspanne | Trailing-Extreme der EXT-Struktur auf H4 | K1 §5 |
| Premium/Discount | obere bzw. untere Hälfte der Range | Long nur bei Position < 0,5, Short nur > 0,5 | K1 §5, K2 §5 |
| OTE | 62–79 % Retracement | Zone 0,62–0,79, Sweet Spot 0,705 (Entry-Variante) | K2 §5, K3 §4c |

### 2.2 Liquidität

| Konzept | Bedeutung | EA-Regel (Default) | Kapitel |
|---|---|---|---|
| BSL / SSL | Buy-Stops über Hochs, Sell-Stops unter Tiefs | Pools auf bestätigten Pivots und Perioden-Extremen | K1 §4 |
| EQH / EQL | (fast) gleiche Hochs/Tiefe, „engineered liquidity“ | ≥ 2 Pivots innerhalb 0,1·ATR200, mit Pullback dazwischen | K1 §4.2 |
| Session-H/L, PDH/PDL, PWH/PWL, PMH/PML, IPDA20 | Perioden-Extreme | nur abgeschlossene Perioden, NY-Zeit (Tag 17:00–17:00 NY) | K1 §4.3 |
| Sweep / Raid / Stop Hunt | Docht durch das Level, Close zurück | `SWEPT` (gleiche Bar oder Reclaim ≤ 3 Bars) | K1 §3.4 |
| Break | Akzeptanz jenseits des Levels | `BROKEN` (2 Closes jenseits); auch ein Break verbraucht den Pool | K1 §3.4 |
| IRL / ERL | interne vs. externe Range-Liquidität | IRL = offene FVGs und interne Pivots; ERL = Range-Extreme | K1 §4.4 |
| Draw on Liquidity | wohin der Preis „gezogen“ wird | Ranking: HTF > LTF, EQ > einzelner Swing, frisch > angetestet | K1 §4.4, K3 §2 |

### 2.3 PD-Arrays (Points of Interest)

| Konzept | Bedeutung | EA-Regel (Default) | Kapitel |
|---|---|---|---|
| **Order Block** | letzte Gegenkerze vor dem Displacement | Hybrid ICT/LuxAlgo. Entry-Zone = Body, Mean Threshold = 50 % Body, Stop am Leg-Tief. Gültig nur mit Displacement, Trade-through und FVG im Leg | K2 §1 |
| Breaker Block | gebrochener OB nach einem Sweep | Full Range; entsteht beim CHoCH, wenn vorher ein älteres Extrem gesweept wurde | K2 §2.1 |
| Mitigation Block | gebrochener OB ohne Sweep (Failure Swing) | Body-Zone | K2 §2.2 |
| Rejection, Propulsion, Vacuum, Reclaimed OB | Spezialformen | nur Research | K2 §2 |
| **Fair Value Gap** (BISI/SIBI) | Lücke zwischen Kerze 1 und Kerze 3 | Gap ≥ max(0,2·ATR, 3·Spread); Mittelkerze schließt jenseits; CE = 50 %. Zustände TOUCHED → CE → FILLED → INVALIDATED | K2 §3 |
| Inverse FVG | durchschlagene FVG mit umgekehrter Rolle | Body-Close jenseits der fernen Kante | K2 §3.3 |
| BPR, Volume Imbalance, Liquidity Void, NWOG/NDOG, 1st Presented FVG | Varianten | nur Research; NDOG nur bei echter Tagespause (meist Gold) | K2 §3 |
| **Displacement** | energischer, impulsiver Move | Σ Body ≥ 1,2·ATR14 (1 Bar) bzw. 1,8·ATR (2–3 Bars). ATR **vor** dem Impuls gemessen; Body/Range ≥ 0,6 | K2 §4 |
| Supply/Demand | klassisches Vorbild des OB | gemeinsame Zonen-Engine; Seiden-„Odds Enhancer“ als Scoring-Features | K2 §6 |

### 2.4 Zeit (alle Zeiten New York)

| Konzept | Zeit | Rolle im EA | Kapitel |
|---|---|---|---|
| Asian Range / Asian KZ | 20:00–00:00 / 20:00–23:00 | Liquiditätspool; Asia-Preset optional | K3 §1 |
| London Killzone | 02:00–05:00 | Entry-Fenster | K3 §1.2 |
| NY AM Killzone (FX) | 07:00–10:00 | Entry-Fenster | K3 §1.2 |
| Silver Bullet | 03–04, 10–11, 14–15 | Preset mit FVG-Entry im Fenster | K3 §1.3 |
| London Close / NY Lunch | 10:00–12:00 / 12:00–13:00 | nur Management bzw. keine Entries | K3 §1.2 |
| Midnight Open / True Day Open | 00:00 | Referenzpreis (Feature) | K3 §1.5 |
| CBDR / Flout / SD-Projektionen | 14:00–20:00 / 14:00–00:00 | Zielvariante (Konvention, keine Messung) | K3 §1.6 |
| Judas Swing / Power of 3 (AMD) | Fehlausbruch zur London-Eröffnung | London-Preset mit Asia-Range-Sweep | K3 §1.7 |
| Macros | z. B. 08:50–09:10, 09:50–10:10 | Feature | K3 §1.4 |
| Weekly Profiles | Wochenmuster | höchstens Risikofilter | K3 §1.8 |
| Rollover | 17:00 | Sperre 16:45–18:15 (Spreads 5–7× breiter) | K6 §6, K7 §8 |

### 2.5 Bias, Korrelation, Entry-Modelle

| Konzept | EA-Regel bzw. Bewertung | Kapitel |
|---|---|---|
| Daily Bias | Tageskerzen-Regel (Close über bzw. unter dem Vortages-Extrem, Sweep-Logik) plus EXT-Trend auf D1 und H4 | K3 §2 |
| SMT-Divergenz | korrelierte Paare bestätigen ein Extrem nicht. EURUSD/GBPUSD ist mathematisch eine EURGBP-Bewegung. DXY wird synthetisch aus 5 Paaren gebildet. Nur als Filter | K3 §5, K7 §5 |
| **ICT 2022 Model** | Sweep → Displacement/MSS → FVG-Limit. Bestens automatisierbar, daher **Modell A** | K3 §4a |
| Silver Bullet | dasselbe mit härterem Zeitfilter, daher Preset A-SB | K3 §4b |
| Judas / Asia-Range-Sweep | London-Preset A-LDN | K3 §4h |
| HTF-POI + LTF-CHoCH/CISD | klassisches SMC bzw. MrOwl-Setup, daher **Modell C** (Trend-Fortsetzung) | K3 §4g, K4 §4 |
| Unicorn, OTE, Turtle Soup, MMXM | Qualitäts-Flag, Entry-Variante, Baseline bzw. nicht automatisierbar | K3 §4 |

---

## 3. Evidenzlage kompakt (→ K5 §1.7, K4 §4, K7 §9)

| SMC-Baustein | Nächstliegende Evidenz | Status |
|---|---|---|
| Liquidity Pools (EQH/EQL, runde Zahlen) | Osler 2003 (Order-Cluster einer FX-Bank); Kavajecz & Odders-White 2004 (S/R = Tiefe im Orderbuch) | Existenz von Order-Clustern belegt (ältere Daten) |
| Sweep mit Umkehr | Osler 2005: Stop-Kaskaden bedeuten **Fortsetzung**. SSRN-Preprint: Fortsetzung in 65 von 66 Folds. fxbacktest: kein Effekt | **Umkehr nicht belegt**; Fortsetzung plausibler |
| Order Block | StatOasis: t ≤ 1,22 (Tagesdaten, Indizes); MrOwl1011: +0,1 R vor Kosten nur **mit** Trendfilter | unbelegt bis schwach |
| FVG „wird gefüllt“ | keine peer-reviewte Studie; Fill-Raten ohne Nullmodell sind wertlos | unbelegt |
| Killzones und Sessions | Andersen & Bollerslev, BIS, fxbacktest-Stundenprofile | **als Volatilitätsfilter belegt**, Richtung nicht |
| Judas Swing / Power of 3 | fxbacktest: Asia-Break-Umkehr 49,4 % (n. s.); Fix-Flows (Krohn et al.) | in ICT-Form unbelegt |
| BOS/CHoCH (Marktstruktur) | entspricht Dow-Theorie und Trendfolge; im G10-FX seit ≈ 1990 weitgehend arbitriert | schwach; als Trendfilter am ehesten nützlich |
| OTE / Fibonacci | StatOasis: 1 von 8 Tests mit t > 2 (bei Mehrfachtests zufällig erwartbar) | unbelegt |
| „Smart Money“-Absicht | informierte Flows existieren (Evans & Lyons, Menkhoff), sind aber aus OHLC nicht beobachtbar | Konzept real, Ableitung unbelegt |

**Kritik in der Literatur** (→ K5 §4):
- **Rebranding:** OB ≈ Supply/Demand, Sweep ≈ Wyckoff Spring/Turtle Soup, BOS ≈ Dow, PO3 ≈ Wyckoff-Zyklus, OTE ≈ Fibonacci.
- **Methodik:** Rückschaufehler, Unfalsifizierbarkeit, viele Freiheitsgrade.
- **ICT:** keine verifizierbare Performance-Historie.
- **Broker-Kontext:** Im Retail-CFD-Umfeld kann ein „Stop Hunt“ auch Spread-Ausweitung oder ein Broker-Effekt sein.

---

## 4. Bestehende Implementierungen: übernehmen oder nicht (→ K4)

**Übernehmen (Konzepte, nicht Code 1:1)**
- **Struktur-Engine nach LuxAlgo-Muster:** kausale Leg-Pivots, `crossed`-Flag, Bias je Layer, Unterdrückung von Duplikaten. Wichtig: LuxAlgo steht unter CC BY-NC-SA. Für eine kommerzielle Nutzung eigenständig implementieren, nicht portieren.
- **Explizites, symmetrisches Zonen-Lebenszyklusmodell** statt „mitigated = gelöscht“.
- **Sweep als Sequenz** (Penetration, Close zurück, Reaktion) und Pool-Merging mit ATR-Toleranz (MQL5-Artikel 24184).
- **Architekturmuster** aus MrOwl1011 und dem LuxAlgo-MQL5-Port:
  - Detection → Events → Strategie → genau ein Order-Modul
  - committed vs. working state
  - Parity-Tests gegen TradingView
- **Kausale Hilfsfunktionen** `previous_high_low` und `sessions` der Python-Library, ergänzt um Sommerzeit.

**Nicht übernehmen**
- Swing-, BOS-, OB- und Liquidity-Funktionen von `smartmoneyconcepts`: Lookahead.
- Von LuxAlgo:
  - HTF-FVG mit `lookahead_on`
  - kumulative Schwellen (`cum/bar_index`)
  - die fehlerhafte Confluence-Formel
  - asymmetrische FVG-Löschung
  - die 5-%-Premium/Discount-Bänder als Regel
- Aus MQL5-Artikeln: feste Punkt-Distanzen, Konsolidierungs-„OBs“, `CHART_VISIBLE_BARS` als Verfallslogik, Market-Orders ohne Stops- und Spread-Prüfung.
- Aus dem MQL5 Market: Grid, Martingale, Recovery, Pyramiding, Stealth-SL. „SMC“ ist dort oft nur ein Etikett.

---

## 5. Instrumente kompakt (→ K7)

| Tier | Symbole | Entry-TF | Begründung |
|---|---|---|---|
| **1 Kern** | EURUSD, GBPUSD, USDJPY, EURJPY, GBPJPY, XAUUSD | M5 | Kostenklasse A (< 15 % ATR(M5)), hohe Liquidität; JPY und Gold mit leichtem Fortsetzungs-Bias |
| **2 selektiv** | AUDUSD, USDCAD, USDCHF, AUDJPY, CADJPY, CHFJPY, EURAUD, GBPAUD, EURCAD, NZDUSD | M5, max. 1 Position pro Cluster | Kostenklasse B (15–25 %) |
| **3 langsam** | GBPCAD, EURNZD, NZDJPY, GBPNZD, GBPCHF, EURCHF, CADCHF, AUDCAD | M15 | Kostenklasse C bzw. dünne Märkte, Mean-Reversion-Tendenz |
| **aus (Default)** | AUDNZD | (H1) | Kosten ≈ 47 % ATR(M5), auch auf M15 noch ≈ 27 % |

**Liquidität (BIS 2025)**
- Weltumsatz 9,6 Bio. USD pro Tag.
- Paaranteile: EURUSD 21,2 %, USDJPY 14,3 %, GBPUSD 7,6 %, USDCAD 5,3 %, AUDUSD 4,9 %, USDCHF 4,9 %.
- Alle CAD-Crosses zusammen kommen auf höchstens ≈ 0,5 %.

**Sessions**
- JPY-, AUD- und NZD-Paare machen 55–65 % ihrer Tagesrange in Asia.
- EUR-, GBP- und CHF-Paare sind in London am aktivsten, CAD-Paare in NY.
- Alle Instrumente haben ihre Spitze um ≈ 13–14 UTC (NY-Vormittag).
- Nach ≈ 09–10 NY sind im Mittel 80 % der Tagesrange erreicht.

**Cluster:** EUR/GBP gegen USD (ρ ≈ 0,9), AUD/NZD-Block (ρ ≈ 0,92), JPY-Block (ρ bis 0,95), CHF-Block (SNB), CAD/Öl, Gold (zählt zum USD-Bein).

**Tail-Risiken**
- JPY: MoF-Interventionen bei 152, 160 und 164; im Juli 2026 erstmals gemeinsam mit dem US-Treasury.
- CHF: SNB-Schock 2015 mit ≈ +30 % intraday.
- GBP: Flash-Crash 2016.
- Gold:
  - ADR von ≈ 60 auf ≈ 132 USD verdoppelt
  - Allzeithoch 5.595 USD am 29.01.2026
  - Wochenend-Gaps bis 153 USD
  - tägliche Pause 17–18 NY

**Kontraktdaten**
- Gold: 1, 10 oder 100 oz je nach Broker, 2 oder 3 Digits; „Pip“ ist nicht standardisiert.
- Positionsgrößen deshalb nur über `OrderCalcProfit` bzw. Tick-Value rechnen.

---

## 6. MT5-Plattform: die wichtigsten Fallstricke (→ K6, Liste mit 21 Punkten in K6 am Ende)

1. **Ein Portfolio-EA bekommt nur Ticks des Chart-Symbols.** Alle anderen Symbole müssen per `OnTimer` gepollt werden. Die New-Bar-Erkennung läuft je Symbol und TF über `SERIES_LASTBAR_DATE`.
2. **Im Strategy Tester gilt `TimeGMT()` = `TimeLocal()` = Serverzeit.**
   - Das Zeitmodell (z. B. NY-Close-Server = NY + 7 h) muss per Input kommen und an der History validiert werden.
   - Prüfung: Die letzte H1-Bar vor dem Wochenende muss um 16:00 NY öffnen.
3. **Wirtschaftskalender:**
   - Im Tester gesperrt (Fehler 4014), daher live als CSV exportieren.
   - Historische Kalenderzeiten sind mit dem *aktuellen* Server-Offset umgerechnet, also bei Sommerzeit um eine Stunde falsch.
4. **Tick-Value und Positionsgröße:**
   - `SYMBOL_TRADE_TICK_VALUE` kann falsch sein, etwa bei Gold oder bei JPY-Crosses im Tester.
   - Lots über `OrderCalcProfit` rechnen, mit Gegenprobe, abrunden und unter `VOLUME_MIN` auslassen.
5. **Filling Modes:**
   - Die Werte von `SYMBOL_FILLING_*` und `ORDER_FILLING_*` unterscheiden sich.
   - RETURN ist bei Market Execution verboten, Pending-Orders brauchen RETURN.
6. **`OrderSend == true` heißt nicht „ausgeführt“.** Bei TIMEOUT oder CONNECTION erst abgleichen, dann neu senden. Sonst entstehen doppelte Positionen.
7. **Tester-Spread:** Bei generierten Ticks ist er der **Minimal**-Spread der M1-Bar, das Ergebnis also zu optimistisch. Die finale Validierung mit Real Ticks und Delay durchführen.
8. **Tick-Historie:**
   - Echte Ticks reichen bei manchen Brokern nur Monate zurück.
   - „100 % real ticks“ im Report kann falsch sein; das Journal prüfen.
   - Für 2015–2026 externe Tickdaten als Custom Symbols importieren.
9. **Bid-Kerzen:**
   - Buy-Limits und Short-Stops triggern auf dem Ask, deshalb den Spread beim Entry und beim SL einrechnen.
   - Zum Rollover sind Spreads 5–7× breiter.
10. **Laufzeitfehler:** Ein einziger Critical Runtime Error beendet den Portfolio-EA für **alle** 25 Symbole. Defensive Checks sind Pflicht.

---

## 7. Empfehlung

1. **Research-first statt „SMC-Bot nach Lehrbuch“.** Zuerst eine kausal korrekte Feature-Engine bauen: Struktur, Liquidität, PD-Arrays, Zeit, Bias. Sie exportiert jedes Ereignis. Dann wird jeder Baustein in Ereignisstudien gegen Placebo getestet, in beide Richtungen (Umkehr und Fortsetzung).
2. **v1-Modelle**
   - **Modell A „Sweep → MSS → FVG“** mit Presets London, NY und Silver Bullet. Das ist das am besten automatisierbare ICT-Modell.
   - **Modell C „HTF-POI → LTF-Bestätigung mit Trendfilter“.** Es entspricht der besten gefundenen Evidenz.
   - Beide nutzen dieselben Engines.
3. **Risiko**
   - 0,25–0,5 % pro Trade.
   - Exposure-Vektor über die Währungen: netto ≤ 1,5 R je Währung, ≤ 4 R gesamt.
   - Cluster-Limits und ein Tagesstopp nach −2 R.
   - Kosten-Gate: Kosten ≤ 10 % des Risikos.
4. **Validierung mit harten Gates** (Blueprint §16)
   - Walk-Forward und Cross-Instrument-Prüfung.
   - Deflated Sharpe Ratio und PBO.
   - Kosten-Stresstest ×2.
   - Einmaliger Hold-out 2024–2026.
   - 3–6 Monate Inkubation vor echtem Kapital.

**Ergänzung für das FTMO-Ziel** (Details in `02_FTMO_Challenge_Plan.md`):
- **Simulation:** Bei einem Netto-Edge von +0,1 R pro Trade erreicht die Risikoleiter 1 % / 0,75 % etwa **80 % Bestehenschance in ≈ 5 Monaten**.
- **Ohne Edge** sind es trotzdem ≈ 40 %. Bestehen beweist also nichts.
- **Mit negativem Edge** bleibt die Chance unter 25 %, egal bei welchem Risiko.
- **Realität laut FTMO-CEO:** nur 8–10 % bestehen die Challenge.
- **FTMO-Kosten:** 5 USD Round Turn pro Lot, 0,7 % Umrechnungsabschlag bei 20 von 25 Instrumenten, Volume Bands.
- **FTMO-Hebel:** FX 1:30, Gold 1:15. Bei 1 % Risiko passen nur 2–3 Positionen gleichzeitig, und enge Intraday-Stops werden teuer. Deshalb ist **Modell C mit weiteren Stops das Primärmodell** im FTMO-Modus.
- **Testumgebung:** Der kostenlose **FTMO Free Trial** dient als Live-Test vor dem Kauf.

**Offene Entscheidungen, bevor Code entsteht** (Details in Blueprint §18):
- Risikoleiter bestätigen.
- Stil: Default jetzt weitere Stops.
- Datenquelle für Backtests.
- Python-Research-Pipeline ja oder nein.
- Umfang v1.
- Prüfungen im Free Trial und die Support-Fragen an FTMO.

---

## 8. Dokumentenübersicht

| Datei | Inhalt |
|---|---|
| `research/01_Marktstruktur_Liquiditaet.md` | Swing-Erkennung (Fractal, Leg, ZigZag, Lag/Repainting), BOS/CHoCH/MSS, Strong/Weak/Protected, Inducement, Liquiditätspools, EQH/EQL-Toleranzen, Sessions, IRL/ERL, Dealing Range, MTF-Bias, Pseudocode, Parameter |
| `research/02_PD_Arrays_OB_FVG.md` | OB-Varianten (ICT 2016/2017/2022, Community, LuxAlgo), Breaker, Mitigation, Rejection, Propulsion, Vacuum, Reclaimed; FVG-Familie (CE, IFVG, BPR, VI, LV, NWOG/NDOG, FPFVG); Displacement; OTE; Supply/Demand; POI-Scoring; Zonen-Lebenszyklus mit Code |
| `research/03_ICT_Zeit_Bias_Entry_Modelle.md` | Killzones, Silver Bullet, Macros, Opens, CBDR/Asia/Flout/SD, Judas/PO3, Weekly Profiles; Daily-Bias-Regelwerk und Score; 8 Entry-Modelle als Pseudocode; SMT; Trade-Management; Sommerzeit-Umsetzung |
| `research/04_Bestehende_Implementierungen.md` | LuxAlgo-SMC-Algorithmus im Detail, Python-Library mit Lookahead-Analyse, MQL5-Artikelserie und CodeBase, GitHub-Projekte mit Bewertung, MQL5 Market, typische Bugs, Testprotokoll |
| `research/05_Evidenz_Kritik_Robustheit.md` | Osler und Order-Cluster, FX-Mikrostruktur, Saisonalität und Fixings, Profitabilität der TA im FX, SMC-spezifische Studien und Backtests, Kritik, Overfitting-Methodik (DSR, PBO, SPA), Validierungsdesign, Risk of Ruin und Kelly, Prop-Regeln, Akzeptanzkriterien |
| `research/06_MQL5_Technik.md` | Architektur Portfolio-EA, Ereignismodell, New-Bar/Sync, Strategy Tester, Zeit und Sommerzeit (`SessionClock`-Code), Lot-Berechnung (Code), Order-Ausführung (Code), Filter, News im Tester, Robustheit, Performance, Code-Organisation, Exposure-Vektor (Code), 21 Fallstricke |
| `research/07_Instrumente.md` | Tabelle der 25 Instrumente (Spreads, ADR, Sessions, Besonderheiten), BIS-Ranking, Stundenprofile, Fixings, Korrelations-Cluster, SMT und synthetischer DXY, Event-Risiken und Interventionen, XAUUSD im Detail, Swap/Rollover, Kostenklassen, Tiering, Handelsfenster |
| `research/08_FTMO_Regeln.md` | FTMO 2-Step Swing: Daily-Loss-Formel und Reset-Zeit, Max Loss, Profitziel, Handelstage, Swing vs. Standard, Kosten (Kommission, Volume Bands, 0,7 %), Serverzeit, verbotene Praktiken, FTMO Account, Preise, Statistiken, EA-Checkliste, offene Support-Fragen |
| `01_EA_Blueprint.md` | EA-Spezifikation v0.1 |
| `02_FTMO_Challenge_Plan.md` | FTMO-Modus: Regelwerk, Monte-Carlo-Ergebnisse, Risikoleiter, FtmoGuard-Spezifikation, Margin- und Kostenfolgen, Ablauf bis zur Challenge, Support-Fragen |
| `../research/ftmo_mc.py`, `../research/results/ftmo_mc_results.md` | Monte-Carlo-Simulation der Challenge (reproduzierbar, `research/.venv/bin/python -I research/ftmo_mc.py`) |
