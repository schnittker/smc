# FTMO 2-Step Swing (100.000 USD) – Plan für den SMC-EA

Stand: 24.10.2026

Grundlagen:
- `research/08_FTMO_Regeln.md`: FTMO-Regeln und -Handelsbedingungen mit Quellen (→ K8)
- Monte-Carlo-Simulation `research/ftmo_mc.py`, Ergebnisse in `research/results/ftmo_mc_results.md`
- Blueprint `01_EA_Blueprint.md`

Dieses Dokument legt fest, wie der EA die Challenge regelkonform angeht und mit welchem Risiko. Wo es vom Blueprint abweicht, gilt im FTMO-Modus dieses Dokument.

---

## 1. Das Regelwerk, auf das der EA programmiert wird (→ K8)

| Regel | Genaue Definition | EA-Folge |
|---|---|---|
| **Profitziel** | Phase 1: Balance ≥ 110.000, Phase 2: Balance ≥ 105.000, jeweils **mit allen Positionen geschlossen**. Die Ziele müssen **gleichzeitig** mit den Mindesthandelstagen erfüllt sein | Zielsicherung: bei Erreichen alles schließen, Pending-Orders löschen, Balance prüfen, Handel stoppen |
| **Max Daily Loss** | Fix 5.000 USD. Basis ist die **Balance um 00:00 Prager Zeit**. Geprüft wird **laufend auf Equity**, inklusive Floating-P/L, Swaps und Kommissionen. Bei Verletzung schließt FTMO sofort alles; die Phase ist verloren | eigene Tagesgrenze mit Puffer, Prüfung vor jedem Trade, Kill-Switch |
| **Max Loss** | Equity nie unter 90.000 (statisch, nicht trailing) | Risikoleiter, harte Stopps vor der Grenze |
| **Reset Daily Loss** | Prager Mitternacht = **01:00 Serverzeit**. In den Sommerzeit-Lückenwochen ist es **02:00** Serverzeit (26.10.–01.11.2026, 14.–28.03.2027, 31.10.–07.11.2027) | „FTMO-Tag“ als eigener Kalender im EA |
| **Serverzeit** | GMT+2/+3 mit **US**-Sommerzeit, also NY = Server − 7 h. Die D1-Kerze schließt um 17:00 NY | passt zum Zeitmodell `SRV_TZ_NY_CLOSE` im Blueprint |
| **Mindesthandelstage** | 4 je Phase. Gezählt werden Prager Kalendertage, an denen mindestens eine Position **eröffnet** wurde | Zähler über die Eröffnungs-Deals |
| **Zeitlimit** | keines (seit Juli 2023) | Risiko kann klein bleiben; keine Eile |
| **Inaktivität** | 30 Kalendertage ohne eröffneten Trade → Kündigung möglich. Jede Phase muss innerhalb von 30 Tagen nach Bereitstellung aktiviert werden | Watchdog |
| **Swing-Konto** | Halten über Nacht und Wochenende erlaubt, News-Trading erlaubt. Hebel FX 1:30, XAUUSD 1:15. Nur im 2-Step erhältlich | Margin-Budget (Abschnitt 4.11) |
| **Kosten** | FX: 2,50 USD je Lot und Seite (5 USD Round Turn). Metalle: 0,0007 % vom Nominal je Seite. „Volume Bands“: Größere Orders bekommen breitere Spreads. **0,7 % Umrechnungsabschlag** auf realisierte Ergebnisse, wenn die Profit-Währung nicht USD ist; das betrifft 20 der 25 Instrumente | Kostenmodell im Kosten-Gate (Abschnitt 4.16) |
| **News und Wochenende** | Beim Swing-2-Step **erlaubt** (Swing-FAQ, vom User bestätigt): Positionen dürfen über News, über Nacht und übers Wochenende eröffnet und gehalten werden | keine Handelssperren; nur Risiko-Reserven im FtmoGuard (Abschnitt 4.12–4.13) |
| **Verbotene Praktiken** | u. a.: Fehler oder Latenz ausnutzen; Hedging über mehrere Konten; Hyperaktivität (> 2.000 Server-Requests pro Tag); Overleveraging bzw. One-sided Bets (z. B. „one big dollar bet“); Aufstocken nach Verlusten; Positionsgrößen sprunghaft ändern | Compliance-Regeln in Abschnitt 4 |
| **Stop-Out / Limits** | Stop-Out bei 50 % Margin-Level; höchstens 200 Orders gleichzeitig, 2.000 Positionen pro Tag | weit unterschritten |
| **Nach dem Bestehen** | FTMO Account mit denselben Verlustgrenzen, ohne Profitziel; 80 % Gewinnanteil (bis 90 %); erste Auszahlung frühestens 14 Tage nach dem ersten Trade; die Gebühr wird mit der ersten Auszahlung erstattet | eigener Risiko-Modus „Funded“ |
| **Preis und Test** | 100k laut Liste 540 EUR, Aktion 439 EUR; den Swing-Preis im Konfigurator prüfen. Der **Free Trial** ist kostenlos und beliebig oft möglich (14 Tage) | Free Trial als Live-Testumgebung vor dem Kauf |

**Realität laut FTMO-CEO (2024 und 2026):** Nur etwa **8–10 %** bestehen die Challenge (→ K8 §10).

---

## 2. Was die Simulation sagt

**Modellannahmen:**
- 1 Trade pro Handelstag im Mittel (höchstens 3), Gewinn = 2 R, Verlust = 1 R
- Tageskorrelation 0,3, internes Tageslimit nach 2 Verlusten
- Max Loss und Daily Loss werden auf Equity geprüft
- kein Zeitlimit, 20.000 Läufe je Zelle
- Die Simulation stimmt mit den analytischen Werten überein (Random Walk: 49,7 % bzw. 65,9 % bei null Edge)

**Lesart:** E = Netto-Erwartungswert pro Trade in R, **nach allen Kosten**. In Klammern steht die Median-Dauer für beide Phasen in Monaten.

| Netto-Edge E | Fest 0,5 % | Fest 1 % | **Leiter 1 % / 0,75 % (Empfehlung)** | Leiter 1 % / 0,5 % | Leiter 0,75 % / 0,5 % |
|---|---|---|---|---|---|
| −0,10 R | 8 % (8,8) | 16 % (2,5) | 13 % (3,5) | 11 % (4,3) | 9 % (5,9) |
| −0,05 R | 20 % (10,0) | 24 % (2,6) | 24 % (4,0) | 23 % (5,6) | 21 % (7,6) |
| ±0,00 R | 40 % (10,2) | 35 % (2,7) | 42 % (4,9) | 43 % (6,6) | 45 % (9,3) |
| +0,05 R | 61 % (9,2) | 46 % (2,6) | 62 % (5,3) | 67 % (7,1) | 71 % (9,6) |
| **+0,10 R** | 78 % (8,1) | 57 % (2,5) | **80 % (5,0)** | 83 % (6,2) | 90 % (8,0) |
| +0,20 R | 95 % (5,9) | 75 % (2,2) | 96 % (3,6) | 97 % (4,1) | 99 % (5,1) |

„Leiter x / y“: Basisrisiko x in Phase 1 und y in Phase 2. Ab 3 % Drawdown (vom Anfangskapital) wird das Risiko halbiert, ab 6 % geviertelt.

**Erkenntnisse:**
1. **Der Edge entscheidet, nicht die Positionsgröße.** Bei E ≤ 0 hilft keine Risikowahl. Selbst eine Strategie **ohne** Edge besteht beide Phasen in etwa 40 % der Fälle. Ein Bestehen ist also **kein Beweis** für eine funktionierende Strategie.
2. **Ein realistischer kleiner Edge bringt gute Chancen.** Mit E ≈ +0,1 R netto erreicht die Risikoleiter etwa 80 % in etwa 5 Monaten. Fest 1 % wäre schneller (2,5 Monate), hätte aber nur 57 % Erfolgschance.
3. **Die bindende Grenze ist der Gesamtverlust von 10 %.** Der Tagesverlust von 5 % wurde in keinem Szenario ausgelöst, weil das interne Limit (2 Verluste pro Tag) greift.
4. **Die Handelsfrequenz ändert nur die Dauer, nicht die Chance.** Bei 0,5 Trades pro Tag dauert es doppelt so lange.
5. **Die reale Bestehensquote von 8–10 % in Phase 1** entspricht in diesem Modell einem Netto-Edge von etwa −0,1 R oder schlechter. Das ist meine Einordnung, keine FTMO-Aussage. Ohne nachgewiesenen positiven Edge ist die Challenge also eher eine Wette als ein Test.

**Konsequenz:** Die Challenge wird erst gekauft, wenn die Out-of-Sample-Tests einen Netto-Edge von mindestens **+0,1 R** zeigen (Blueprint §16). Zusätzlich muss eine Bootstrap-Simulation mit der **echten** OOS-Trade-Verteilung eine Bestehenschance von mindestens 70 % ergeben (Abschnitt 6).

---

## 3. Risikopolitik im FTMO-Modus [D]

| Phase | Basisrisiko pro Trade (vom Anfangskapital) | Leiter | Offenes Gesamtrisiko | Ziel |
|---|---|---|---|---|
| Challenge (+10 %) | **1,0 %** = 1.000 USD | ab 3 % DD → 0,5 %; ab 6 % DD → 0,25 % | ≤ 3 % (inkl. Pendings) | 110.000 Balance, alles geschlossen |
| Verification (+5 %) | **0,75 %** = 750 USD | dito | ≤ 2,25 % | 105.000 |
| FTMO Account | **0,5 %** = 500 USD | dito | ≤ 2 % | Auszahlung frühestens nach 14 Tagen, monatlich |

- **Internes Tageslimit:** nach 2 Verlusten oder −2 R realisiert keine neuen Trades mehr an diesem FTMO-Tag (00:00–24:00 Prag).
- **Compliance:** Das Risiko wird nur **verkleinert**, nie nach Verlusten vergrößert. FTMO wertet Aufstocken nach Verlusten als Overleveraging.
- **Positionsgrößen** bleiben innerhalb einer Leiterstufe konstant. Kein Grid, kein Martingale, kein Nachkaufen.
- **Exposure-Grenzen** aus Blueprint §9 bleiben: netto ≤ 1,5 R je Währung, Cluster-Regeln, 1 Position je Symbol. Sie decken auch FTMOs Kritik an „one big dollar bet“ ab.

---

## 4. FtmoGuard – Spezifikation (eigenes Modul `Risk/FtmoGuard.mqh`)

**4.1 Zeit**
- Der FTMO-Tag ist der Prager Kalendertag: Prag = UTC+1, plus 1 h während der EU-Sommerzeit.
- Die Server→UTC-Umrechnung nutzt das Blueprint-Modell `SRV_TZ_NY_CLOSE`.
- Reset normalerweise um 01:00 Serverzeit, in den Lückenwochen um 02:00 Serverzeit. Im Free Trial gegen den Tooltip „Today's permitted loss“ in Account MetriX validieren.

**4.2 Referenzbalance**
- `B_ref` = Anfangskapital + Σ(DEAL_PROFIT + DEAL_COMMISSION + DEAL_SWAP + DEAL_FEE) aller Deals vor dem letzten Reset.
- Wird aus der Deal-History berechnet, ist damit **neustartsicher** und braucht keinen gespeicherten Zustand.

**4.3 Grenzen**
- `dailyFloor = B_ref − 5.000`, `maxFloor = 90.000`, `floor = max(dailyFloor, maxFloor)`.

**4.4 Konservative Equity**
- `E* = ACCOUNT_EQUITY − geschätzte Schließkommission − 0,7 % × Floating-Verluste` der Nicht-USD-Profit-Symbole `− Spread- und Slippage-Puffer`.

**4.5 Prüfung vor jedem Trade**
- `E* − Σ Worst-Case-Verlust(offene + Pending + neue Position) ≥ floor + 1.000`.
- Der Worst-Case-Verlust je Position umfasst:
  - SL-Distanz × Lots
  - 20 % Slippage-Reserve, **50 %** für Positionen und Pending-Orders, die während eines Tier-1-Events ihrer Währungen offen sind (Abschnitt 4.13)
  - 0,7 %-Zuschlag, wo er anfällt
  - Kommission
  - für Positionen über das Wochenende zusätzlich eine Gap-Reserve (Abschnitt 4.12)
- Sonst die Lots verkleinern; fällt das Risiko dadurch unter 50 % des geplanten, den Trade auslassen.

**4.6 Schutzstufen**
- **Weich:** `E* ≤ floor + 2.000`: keine neuen Entries an diesem FTMO-Tag, Pending-Orders löschen.
- **Hart:** `E* ≤ floor + 1.000`: alles schließen, bis zum nächsten FTMO-Tag sperren.
- **Max-Loss-Nähe:**
  - Equity ≤ 94.000: Die Leiter steht bereits auf 0,25 %.
  - Equity ≤ 91.500: Handel komplett stoppen. Danach ist eine manuelle Entscheidung nötig.

**4.7 Zielsicherung**
1. Bei `E* ≥ Ziel + 300 USD`: alle Positionen schließen und Pending-Orders löschen.
2. Balance prüfen. Liegt sie noch unter dem Ziel, normal weiterhandeln.
3. Bei Balance ≥ Ziel und ≥ 4 Handelstagen: **Handel beenden** und den Nutzer benachrichtigen.
4. Fehlen Handelstage: „Mindesttage-Modus“. Pro FTMO-Tag eine Minimalposition eröffnen (Mindestvolumen, Stop wenige Pips, nach wenigen Minuten schließen), bis 4 Tage erreicht sind. FTMO nennt kein Mindestvolumen. Ob solche Mini-Trades toleriert werden, vorher beim Support klären (Abschnitt 7).

**4.8 Handelstage-Zähler**
- Gezählt werden die Prager Daten aller Eröffnungs-Deals (`DEAL_ENTRY_IN`) der aktuellen Phase.

**4.9 Inaktivitäts-Watchdog**
- Hinweis an den Nutzer nach 20 Tagen ohne Eröffnung.
- Optionaler Minimal-Trade nach 25 Tagen (default aus).

**4.10 Request-Budget**
- Alle Trade-Requests (Eröffnen, Ändern, Schließen, Pendings) werden gezählt. **Harte Obergrenze 500 pro Tag**; FTMO stuft ab 2.000 als hyperaktiv ein.
- Kein Trailing pro Tick; SL-Änderungen nur bei Bar-Close.

**4.11 Margin-Budget**
- Σ Margin (offene Positionen + Pendings, als wären sie gefüllt; berechnet per `OrderCalcMargin`) ≤ **80 % der Equity**. Passt eine Position nicht, die Lots verkleinern (Regel wie in 4.5).
- Größenordnung bei 100k und FTMO-Swing-Hebel:

  | Fall | Risiko 1 %: Lots / Margin | Risiko 0,5 %: Lots / Margin |
  |---|---|---|
  | EURUSD, SL 10 Pips | 10,0 / 37.300 USD | 5,0 / 18.700 USD |
  | EURUSD, SL 20 Pips | 5,0 / 18.700 USD | 2,5 / 9.300 USD |
  | USDJPY, SL 15 Pips | 10,5 / 34.800 USD | 5,2 / 17.400 USD |
  | XAUUSD (100 oz, 1:15), SL 8 USD | 1,25 / 34.200 USD | 0,62 / 17.100 USD |
  | XAUUSD, SL 15 USD | 0,67 / 18.200 USD | 0,33 / 9.100 USD |

  Bei 1 % Risiko und engen Intraday-Stops passen also **nur 2–3 Positionen gleichzeitig**. Das spricht im FTMO-Modus für weitere Stops (Abschnitt 5).

**4.12 Wochenende** (beim Swing-2-Step erlaubt)
- **Kein Zwangs-Close vor dem Wochenende** [D `CloseBeforeWeekend = false`]. Positionen laufen bis TP, SL oder Zeit-Stopp weiter, auch übers Wochenende.
- **Risiko-Schutz statt Verbot.** Ein Wochenend-Gap kann über den SL springen. Er zählt auf den Tagesverlust des Prager Sonntags, dessen Basis die Freitags-Balance ist (→ K8 §1). Deshalb gilt:
  - **Gap-Reserve je Position** = 3 × durchschnittliches Wochenend-Gap des Symbols. Der Durchschnitt wird laufend aus der eigenen History gemessen. Startwerte aus FTMO-Daten (ca. 2021, Pips): EURUSD 8, GBPUSD 17, GBPJPY 22, EURCHF 9; XAUUSD 27 (Einheit laut FTMO unklar, daher selbst messen).
  - **Wochenend-Prüfung Freitag ab 15:00 NY:** floatender Verlust + Σ Worst-Case aller offenen Positionen inklusive Gap-Reserve ≤ 4.000 USD (Tageslimit des Sonntags 5.000 − 1.000 Puffer). Passt das nicht, werden die Positionen mit dem größten Beitrag geschlossen, bis es passt.
- **Neueröffnungen am Freitag** bis 15:00 NY [D]. Das ist keine Regel, sondern Kostenschutz: Danach sind die Liquidität dünn und die Spreads breit.
- **Pending-Orders** werden Freitag um 16:00 NY gelöscht, damit sie nicht zum Gap der Wiedereröffnung gefüllt werden.
- **XAUUSD:** keine Pending-Orders über die tägliche Pause (≈ 1 h); die Rollover-Sperre des Blueprints gilt.

**4.13 News** (beim Swing-2-Step erlaubt)
- **Keine Handelssperre** [D `NewsMode = ALLOW`]. Der EA handelt Setups auch rund um High-Impact-Events.
- **Risiko-Schutz:** Positionen und Pending-Orders, die während eines Tier-1-Events ihrer Währungen offen sind, bekommen in der Prüfung 4.5 eine Slippage-Reserve von 50 % statt 20 %. Grund: Der SL kann bei News rutschen.
- **Evidenz entscheidet:** Die Nähe zu News wird als Feature exportiert. Die Ereignisstudie zeigt, ob News-Phasen die Ergebnisse verbessern oder verschlechtern.
  - Die Variante `NewsMode = AVOID` (keine Neueröffnungen von −30 bis +30 min, Pending-Orders −15 min löschen) bleibt als Testvariante. Sie zählt dann als eigener Versuch im Trial-Log.
- Der Wirtschaftskalender wird trotzdem gebraucht (Reserven, Feature), im Tester als CSV-Export.

**4.14 Konto und Phase**
- Inputs: `Phase ∈ {CHALLENGE, VERIFICATION, FUNDED, FREE_TRIAL}` und `InitialBalance` (100.000; Free Trial je nach Größe).
- Ändert sich `ACCOUNT_LOGIN`, wird der Zustand zurückgesetzt. Jede Phase ist ein neues MT5-Konto.
- `ACCOUNT_MARGIN_MODE` (Hedging oder Netting) beim Start prüfen.

**4.15 Volume Bands**
- `maxLotsPerOrder` je Symbol [D: FX 15 Lots]. Grund: Der Spread steigt laut FTMO-Beispiel mit der Ordergröße, bei EURUSD von 0 über 0,4 und 0,8 bis 1,2 Pips.
- Ob das Aufteilen einer Order in mehrere kleinere erlaubt ist, ist offen (Abschnitt 7). Deshalb [D] nicht aufteilen: Übersteigt eine Position die Grenze, wird sie verkleinert.

**4.16 Kostenmodell im Kosten-Gate**
- `costR = (Band-Spread(lots) + Slippage) / SL-Distanz + Kommission RT / Verlust pro Lot + 0,7 % × (erwarteter |P/L| / R)`, Letzteres nur bei Nicht-USD-Profit-Währung.
- Schwelle wie im Blueprint: ≤ 0,10 R.
- Beispiele (Größenordnung, abgeleitet):

  | Fall | Kosten |
  |---|---|
  | EURUSD, SL 10 Pips, 10 Lots | 0,4 Pips Spread + 0,5 Pips Kommission + Slippage ≈ **10 % von R**, an der Grenze |
  | EURUSD, SL 20 Pips | ≈ 4–5 % |
  | USDJPY, SL 15 Pips | ≈ 8–9 % inklusive 0,7 %-Abschlag |
  | XAUUSD, SL 8 USD | ≈ 3–5 % |

---

## 5. Strategische Folgen für die Challenge

1. **Weitere Stops.** Margin, Kommission pro Lot und Volume Bands machen enge Intraday-Stops teuer. Deshalb im FTMO-Modus:
   - **Modell C** (H1-POI → M5/M15-Bestätigung mit Trendfilter) wird **Primärmodell**. Es hat die weiteren Stops, den Trendfilter als dominanten Faktor in der besten Evidenz und weniger Trades.
   - **Modell A** ist nach der Ereignisstudie P2 zurückgestellt: Sweep → MSS ohne Effekt (→ `03_Ergebnisse_P2_Ereignisstudie.md`).
   - Trigger-TF M15 für Tier 2 und 3 (wie Blueprint §11.2).
2. **Übernacht- und Wochenend-Halten nutzen.** Das Swing-Konto erlaubt beides.
   - **Modell C** im FTMO-Modus: kein Exit zum Session-Ende, stattdessen [D] ein **Zeit-Stopp nach 3 FTMO-Tagen**. H1-POIs zielen auf H1/H4-Liquidität, die oft mehr als einen Tag braucht.
   - **Modell A** behält seine Intraday-Exits, weil seine Logik session-basiert ist. Als Variante wird „bis TP/SL halten“ getestet.
   - Der FTMO-Tag beginnt um 18:00 bzw. 19:00 NY. Asia-, London- und NY-Session liegen damit im selben FTMO-Tag.
   - Über Nacht offene Floating-Verluste verringern aber den Spielraum des nächsten Tages, weil die Basis die Balance ist (→ K8 §1). Die Prüfung vor jedem Trade (4.5) rechnet sie mit ein.
3. **Instrumentwahl.** EURUSD, GBPUSD, AUDUSD, NZDUSD und XAUUSD haben USD als Profit-Währung und **keinen 0,7 %-Abschlag**; bei Gleichstand bevorzugen. XAUUSD hat relativ zum Stop die niedrigsten Kosten, braucht aber viel Margin.
4. **Gleichzeitige Positionen** sind durch das Margin-Budget faktisch auf 2–3 begrenzt (bei 1 % Risiko). Das passt zu den Exposure-Regeln und senkt das Korrelationsrisiko.

---

## 6. Ablauf bis zur Challenge

| Schritt | Inhalt | Kriterium für den nächsten Schritt |
|---|---|---|
| 1 | EA und Research-Pipeline bauen (Blueprint M1–M4) inklusive FtmoGuard und FTMO-Kostenmodell | Unit-Tests und Lookahead-Freiheit (P1) |
| 2 | Ereignisstudien, Walk-Forward, Robustheit, Hold-out (Blueprint §16) mit FTMO-Kosten | Akzeptanzkriterien erfüllt, Netto-E ≥ +0,1 R |
| 3 | **Bootstrap-Bestehenschance:** die echten OOS-Trades (in R, mit Tagesstruktur) ziehen und durch die FTMO-Regeln laufen lassen (Erweiterung von `ftmo_mc.py`) | P(beide Phasen) ≥ 70 %, Median ≤ 6 Monate |
| 4 | **FTMO Free Trial** (kostenlos, 14 Tage, beliebig oft), 2–4 Durchläufe ≈ 1–2 Monate. Prüfen: Zeitmodell und Daily-Loss-Reset (MetriX-Tooltip), Spreads je Volume Band, Kommission, 0,7 %-Abschlag, Symbol-Spezifikationen, Kontomodus, Swap-Tage; Live- gegen Backtest-Ergebnisse vergleichen | Live-Expectancy im 95-%-Konfidenzintervall des Backtests, Kostenannahmen bestätigt |
| 5 | **Challenge kaufen** (Swing, 100k); Phase 1 mit 1 %-Leiter, Phase 2 mit 0,75 %-Leiter | – |
| 6 | FTMO Account mit 0,5 %-Leiter; Auszahlungen, Scaling Plan | Kill-Switch nach Blueprint §9 |

---

## 7. Fragen an den FTMO-Support vor dem Kauf (→ K8, Abschnitt b)

News- und Wochenendhandel sind beim Swing-2-Step erlaubt und deshalb keine offene Frage mehr.

1. Werden Minimal-Trades nur zum Erreichen der 4 Handelstage toleriert? Zählt das Auslösen einer Pending-Order als Eröffnung?
2. Ab wann gilt der 0,7 %-Umrechnungsabschlag für eine jetzt gekaufte Challenge?
3. MT5-Kontomodus: Hedging oder Netting? Wird Kommission beim Öffnen, beim Schließen oder hälftig belastet? Rechnet die FTMO-Equity die künftige Schließkommission schon ein?
4. Volume Bands: Bandgrenzen je Symbol; ist das Aufteilen von Orders erlaubt?
5. Grenzfall Equity = Limit; Umgang mit Spreadspitzen beim Rollover.
6. Bestätigung, dass ein **selbst entwickelter**, autonomer EA nicht unter die Klausel „AI/ultra-high-speed tools“ fällt.
7. Swing-Preis für 100k (540 EUR, Aktion 439 EUR oder Aufschlag?).
8. Wortlaut AGB 13.2.3: 30 Tage ohne Trade; Verlust von 8–10 % länger als 30 Tage.
9. Daily-Loss-Reset in der Lückenwoche (26.10.–01.11.2026): wirklich um 02:00 Serverzeit?
