# P4 – Vorregistrierung: Modell D „Trendfolge mit Struktur-Exit“

Festgelegt am 24.10.2026, **bevor** Code für dieses Modell geschrieben oder Ergebnisse angesehen wurden. Änderungen nach diesem Commit zählen als neuer Versuch im Trial-Log.

## 1. Hypothese und Herkunft

Wenn ein H1-Gegen-Swing gegen den H4-Trend endet, läuft der Trend oft deutlich weiter als 3 Tage. Lässt man Gewinner laufen, bis die H1-Struktur bricht, bleiben unter FTMO-Kosten im Mittel mindestens **+0,10 R netto pro Trade**.

**Herkunft:** Option A aus `docs/05_Ergebnisse_P3_ModellC.md`. Modell C nutzte dasselbe Signal mit weitem Struktur-Stop und hatte nur 3 Tage Zeit. Fast alle Trades endeten am Zeit-Stopp. Modell D gibt dem Trade die Zeit, die zum weiten Stop passt.

**Wichtig:** Die Idee entstand nach Sichtung der In-Sample-Daten von P3, denn die Signalmenge ist dieselbe wie bei C-MKT. Deshalb gilt eine strengere Schwelle für den t-Wert (≥ 3,0 statt 2,5). Der Hold-out ist weiterhin unberührt.

## 2. Daten und Zeiträume

- HistData M1 (Bid), umgerechnet in FTMO-Serverzeit; alle 25 Instrumente
- **In-Sample (IS):** Signale vom 01.01.2015 bis 31.12.2023
- **Hold-out (HO):** Signale vom 01.01.2024 bis Datenende (16.10.2026)
  - Er wird genau **einmal** ausgewertet, und nur wenn IS alle Kriterien erfüllt.
- **Zinsen für Swaps:** monatliche Kurzfristzinsen von FRED (OECD-Reihen)
  - Tagesgeld (`IRSTCI01…M156N`) für USD, EUR, GBP, JPY, AUD, CAD
  - 3-Monats-Interbank (`IR3TIB01…M156N`) für NZD und CHF, weil deren Tagesgeldreihen 2024 enden
  - Fehlende Monate am Reihenende: letzter verfügbarer Wert

## 3. Regeln (Long, Short spiegelbildlich)

**Signal und Einstieg: identisch mit C-MKT** (`docs/04`, §3)
- **Signal:** Strikter H1-Trendwechsel nach oben (`CHOCH_STRICT`, +1) bei Close der H1-Kerze. Der strikte H4-Trend an der letzten geschlossenen H4-Kerze ist +1.
- **Keine offene Position** auf dem Symbol. Signale während einer offenen Position werden ignoriert.
- **Einstieg:** Markt zur Eröffnung der ersten M5-Kerze nach dem Signal, zum Ask (Open + Spread).
- **Stop:** Anker = neues H1-Protected-Low (`ref_i`). `SL = Anker − max(2 × typischer Raw-Spread, 0,1 × ATR14(M15))`, ATR an der letzten geschlossenen M15-Kerze. Der Stop bleibt fest, er wird nicht nachgezogen.
- **Kosten-Gate wie in P3:** Spread + Kommission + einmal Slippage ≤ 0,10 R, sonst kein Trade.

**Ausstieg** (es zählt das Erste davon)
1. **Stop:** Bid-Low ≤ SL; Short: Bid-High ≥ SL − Spread. Bei einem Gap über den Stop wird zur Eröffnung gefüllt.
2. **Struktur-Exit:** Der strikte H1-Trend kippt gegen die Position, das heißt, das nächste `CHOCH_STRICT`-Ereignis auf H1 tritt ein.
   - Ausstieg zum Markt bei Eröffnung der ersten M5-Kerze nach diesem H1-Close (Long zum Bid, Short zum Ask).
   - Der Trendwechsel bedeutet: H1-Close jenseits des Protected Levels. Die Engine verschiebt dieses Level bei jedem H1-Swing-BOS in Trendrichtung auf das Extrem zwischen gebrochenem Pivot und Break-Kerze. Das wirkt wie ein Trailing-Stop auf Schlusskursbasis.
3. **Zeit-Stopp:** zum Close der 5.760. M5-Kerze ab Einstieg (20 Handelstage).

- Kein festes Ziel.
- Halten über Nacht, Wochenende und News ist erlaubt (Swing-Konto).
- In der Einstiegskerze wird nur der Stop geprüft.
- Reihenfolge in einer Kerze: Ein Struktur-Exit zur Eröffnung geht einem Stop-Treffer derselben Kerze vor.
- Ein Struktur-Exit gibt das Symbol mit dem Ausstiegszeitpunkt frei. Ein gleichzeitiges Gegensignal darf also sofort handeln (Stop-and-Reverse).

**Kosten** (alle in R abgezogen)

| Posten | Höhe |
|---|---|
| Spread | typischer Raw-Spread + 0,3 Pip Volume-Band-Zuschlag, bei XAUUSD + 0,05 USD; über Ask/Bid-Fills |
| Kommission | 5 USD pro Lot Round Turn, Gold 0,0014 % vom Nominal |
| Slippage | 0,1 Pip (Gold 0,02 USD) bei Einstieg und bei jedem Ausstieg |
| **Swaps (neu)** | siehe unten |
| **0,7-%-Umrechnungsgebühr (neu)** | auf den realisierten Kursgewinn oder -verlust bei Symbolen mit Profit-Währung ≠ USD (20 von 25) |

**Swap-Berechnung**
- Je Rollover (00:00 Serverzeit, nur nach Handelstagen Mo–Fr) mit `Einstiegskurs × Satz / 365`.
- Satz Long: `(Zins Basis − Zins Quote − 1,0 %)`; Short: `(Zins Quote − Zins Basis − 1,0 %)`.
- XAU hat Zins 0. Die 1,0 % p. a. sind ein angenommener Broker-Aufschlag.
- Der Rollover nach dem Mittwoch zählt dreifach.
- Belastet wird jeder Rollover-Zeitpunkt R mit Einstieg < R ≤ Ausstieg. Bei Stop-Ausstieg gilt das Ende der Ausstiegskerze.

In P3 fehlten Swaps und Gebühr. Bei 3 Tagen Haltedauer machen sie etwa 0,01–0,02 R aus und ändern das Ergebnis von P3 nicht.

**Feste Parameter (keine Optimierung)**
- Pivots H4 5/20, H1 5/30, M15 5/40 (wie P3)
- Zeit-Stopp 5.760 M5-Kerzen
- Kosten-Gate 0,10 R
- Swap-Aufschlag 1,0 % p. a.

## 4. Portfolio- und FTMO-Stufe

**Portfolio-Filter** (alle Trades in zeitlicher Reihenfolge der Einstiege, vor dem Bootstrap angewendet)
- höchstens 3 gleichzeitig offene Positionen
- höchstens 1 offene Position je Cluster laut Blueprint §11.3:
  - A: EURUSD, GBPUSD, USDCHF
  - B: AUDUSD, NZDUSD, AUDJPY, NZDJPY, EURAUD, EURNZD, GBPAUD, GBPNZD, AUDCAD
  - D: USDJPY, EURJPY, GBPJPY, AUDJPY, NZDJPY, CADJPY, CHFJPY
  - E: USDCHF, EURCHF, GBPCHF, CADCHF, CHFJPY
  - F: USDCAD, EURCAD, GBPCAD, AUDCAD, CADJPY, CADCHF
  - G: XAUUSD
  - Ein Symbol in mehreren Clustern belegt alle davon. AUDNZD gehört zu keinem Cluster.
- nach 2 Verlusten an einem FTMO-Tag (Prager Kalendertag) keine neuen Einstiege an diesem Tag

**FTMO-Simulation**
- Risiko pro Trade vom Anfangskapital: Phase 1 1,0 %, Phase 2 0,75 %.
  - Ab 3 % Drawdown halbiert, ab 6 % geviertelt; Drawdown = Anfangskapital − Balance beim Einstieg.
- Ergebnis eines Trades: Risiko × Netto-R, gebucht zum Ausstiegszeitpunkt.
- **Prüfung bei jedem Ein- und Ausstieg, offene Positionen im Worst Case mit −1 R:**
  - **Max Loss:** Balance − Σ offenes Risiko ≥ 90.000
  - **Daily Loss:** Balance − Σ offenes Risiko ≥ Balance zu Beginn des FTMO-Tags − 5.000
- **Ziel** (Phase 1 +10 %, Phase 2 +5 %):
  - Ist die Balance ≥ Ziel, gibt es keine neuen Einstiege mehr.
  - Bestanden ist die Phase, wenn die letzte offene Position geschlossen ist und die Balance dann noch ≥ Ziel liegt.
  - Fehlende Mindest-Handelstage (4) werden mit Minimal-Trades an den folgenden Handelstagen ergänzt.
  - Lücken von mehr als 30 Tagen ohne Einstieg werden mit einem Minimal-Trade ohne Ergebniswirkung überbrückt (Inaktivitätsregel). Ihre Häufigkeit wird berichtet.
- Phase 2 beginnt mit 100.000 und den nächsten Trades nach dem Bestehen von Phase 1.
- **Block-Bootstrap über Kalendermonate:**
  - 10.000 Pfade aus den gefilterten Trades IS + HO.
  - Ein Trade gehört zum Monat seines Einstiegs und behält Haltedauer und Lage im Monat.
  - Ein Pfad ist höchstens 120 Monate lang, danach gilt er als unfertig.
  - Ergebnis: Bestehenschance beider Phasen und Dauer in Monaten.

## 5. Akzeptanzkriterien

**In-Sample** (alle müssen erfüllt sein)

| # | Kriterium |
|---|---|
| 1 | Netto-Erwartungswert ≥ +0,10 R pro Trade (inkl. Swaps und 0,7-%-Gebühr) |
| 2 | t-Wert ≥ **3,0**, als kleinster Wert aus iid und Clustern nach Einstiegstag, -woche und -monat |
| 3 | Netto-Profit-Factor ≥ 1,2 |
| 4 | ≥ 6 von 9 Jahren mit positivem Netto-Erwartungswert |
| 5 | ≥ 60 % der Instrumente (mit ≥ 10 Trades) mit positivem Netto-Erwartungswert |
| 6 | bei doppelten Kosten Netto-Erwartungswert > 0 (Spread, Kommission, Slippage, Gebühr und belastende Swaps verdoppelt; Swap-Gutschriften nicht) |

Erfüllt Modell D nicht alle Kriterien, ist **P4 gescheitert**. Der Hold-out bleibt dann unberührt, und der SMC-Ansatz wird laut `docs/05` §4 beendet (Option C oder D).

**Hold-out** (einmalig)

| # | Kriterium |
|---|---|
| 1 | Netto-Erwartungswert > 0 und Netto-PF > 1,1 |
| 2 | Netto-Erwartungswert ≥ untere Grenze des 95-%-Konfidenzintervalls von IS (Cluster-Bootstrap nach Einstiegsmonat) |

**FTMO** (portfolio-gefilterte Trades IS + HO)

| # | Kriterium |
|---|---|
| 1 | Bestehenschance für beide Phasen ≥ 70 % |
| 2 | Median-Dauer ≤ 6 Monate |

## 6. Trial-Log (Fortsetzung)

| # | Test |
|---|---|
| T6 | Modell D, In-Sample |
| T7 | Hold-out von Modell D (nur falls T6 besteht) |
| T8 | Portfolio-Filter und FTMO-Bootstrap (nur falls T7 besteht) |
