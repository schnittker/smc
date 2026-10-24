# Vorregistrierung: Modell M „Monatsend-Rebalancing am London-Fix“ (Strategie Nr. 5)

Festgelegt am 24.10.2026, **bevor** Code für dieses Modell geschrieben oder Daten dafür ausgewertet wurden. Änderungen nach diesem Commit zählen als neuer Versuch im Trial-Log (`../TRIAL_LOG.md`).

## 0. Feste Rahmenbedingungen (für alle Strategien gleich)

- Expert Advisor für MetaTrader 5, handelt vollständig autonom
- FTMO 2-Step, Swing, 100.000 USD
- Max. Verlust gesamt 10 %, max. Tagesverlust 5 %
- Ziel Phase 1 +10 %, Ziel Phase 2 +5 %
- News-Trading und Halten übers Wochenende erlaubt

## 1. Hypothese

Die Währung des Aktienmarkts, der im Monat besser lief als der US-Markt, wertet in der Zeit vor dem Monatsend-Fix (16:00 London) gegen den USD ab. Lief der US-Markt besser, wertet der USD ab (Melvin & Prins 2015; Details in `docs/00_Recherche.md`).

**Erwartung vor dem Test: eher Scheitern.** Gründe: Die Idee ist bekannt, das Fix-Fenster wurde 2015 reformiert, und es gibt nur ein Ereignis pro Monat.

## 2. Daten und Zeiträume

- HistData M5 (Bid) aus `../smart-money-concept/data/bars`, Zeitmodell und Kostenmodell aus dem SMC-Projekt (Stand Commit `e4236a9`)
- **In-Sample (IS):** Monatsenden vom 01.01.2015 bis 31.12.2023 (108 Ereignisse)
- **Hold-out (HO):** Monatsenden vom 01.01.2024 bis Datenende (16.10.2026)
  - Er wird genau **einmal** ausgewertet, nur für die gewählte Variante und nur, wenn sie IS besteht.
- **Beschreibend:** 2014 wird nur berichtet, weil es vor der Fix-Reform vom Februar 2015 liegt. Es geht in keine Entscheidung ein.

**Paare und Aktienindizes**

| Paar | Fremdwährung | Fremdindex (HistData → FTMO) | US-Index |
|---|---|---|---|
| EURUSD | EUR | FRXEUR → FRA40.cash (CAC 40) | SPXUSD → US500.cash |
| GBPUSD | GBP | UKXGBP → UK100.cash | SPXUSD |
| USDJPY | JPY | JPXJPY → JP225.cash | SPXUSD |
| AUDUSD | AUD | AUXAUD → AUS200.cash | SPXUSD |

- Für den EUR ist der CAC 40 der Stellvertreter, denn die HistData-DAX-Daten sind 2020–2023 fehlerhaft (SMC `docs/13`). Der EA verwendet denselben Index, damit Test und EA übereinstimmen.
- CAD, CHF und NZD entfallen. Für ihre Aktienmärkte haben wir keine Daten, und FTMO bietet sie nicht an.

## 3. Regeln

**Ereignistag** = letzter Londoner Geschäftstag des Kalendermonats
- Das ist der letzte Werktag (Mo–Fr) des Monats, der kein englischer Bankfeiertag ist.
- Berücksichtigte Feiertage: Karfreitag, Ostermontag, letzter Montag im Mai, letzter Montag im August, 25./26.12., 01.01.
- Dezember wird normal gehandelt.
- Londoner Ortszeit = UTC + 1 h während der EU-Sommerzeit, sonst UTC.

**Varianten (je ein Trial)**

| Variante | Signalzeitpunkt | Einstieg | Ausstieg |
|---|---|---|---|
| **M-1H** | 14:55 London | 14:55 London | 16:00 London |
| **M-DAY** | 08:00 London | 08:00 London | 16:00 London |

- M-1H folgt dem Paper (Stunde vor dem Fix). Es beginnt 5 Minuten früher, damit US-Daten um 10:00 New York nicht genau auf den Einstieg fallen.
- M-DAY prüft, ob sich der Druck seit der Veröffentlichung früher am Tag aufbaut.

**Signal je Paar** (zum Signalzeitpunkt `ts`)
- `R_US` = log. Rendite von US500, `R_c` = log. Rendite des Fremdindex, jeweils vom Signalzeitpunkt des vorigen Ereignistags (gleiche Londoner Uhrzeit) bis `ts`.
- **Kurs zum Zeitpunkt t:** Close der letzten M5-Kerze, die bis t endet. Ist diese Kerze älter als 6 Stunden, entfällt das Paar in diesem Monat (beim US500 der ganze Monat).
- `x_c = R_US − R_c`
  - `x_c > 0` (US besser): **Long Fremdwährung**, also Long EURUSD, GBPUSD, AUDUSD bzw. Short USDJPY
  - `x_c < 0` (Fremdmarkt besser): **Short Fremdwährung**
  - `x_c = 0`: kein Trade
- Jede Position hat denselben Nominalwert, gehandelt wird nur das Vorzeichen.

**Ausführung** (wie Modell F)
- Markt zur Eröffnung der M5-Kerze, die zum Einstiegszeitpunkt beginnt. Ausstieg zur Eröffnung der M5-Kerze, die zum Ausstiegszeitpunkt beginnt.
- Fehlt eine der beiden Kerzen, entfällt das Paar in diesem Monat.
- Kauf zum Ask (Bid + Spread), Verkauf zum Bid.
- **Notfall-Stop:** 3 × ATR14(H1) ab Einstieg, ATR der letzten geschlossenen H1-Kerze. Long: Bid-Low ≤ Stop; Short: Bid-High + Spread ≥ Stop. Bei einem Gap wird zur Eröffnung gefüllt.

**Kosten** (je Position, in Basispunkten des Einstiegskurses)
- Spread: typischer Raw-Spread + 0,3 Pip Volume-Band-Zuschlag (SMC-Kostenmodell)
- Kommission: 5 USD pro Lot Round Turn
- Slippage: 0,1 Pip beim Einstieg, **0,5 Pip beim Ausstieg am Fix** (breitere Spreads am Monatsend-Fix), 0,1 Pip bei einem Stop
- 0,7-%-Umrechnungsgebühr auf das Kursergebnis von USDJPY
- Swaps fallen nicht an, weil keine Position über den Rollover gehalten wird.

**Bewertungseinheit:** Ereignisergebnis = Summe der Netto-Ergebnisse (bp) aller Positionen eines Monatsendes.

## 4. Akzeptanzkriterien

**In-Sample, je Variante** (alle müssen erfüllt sein)

| # | Kriterium |
|---|---|
| 1 | Mittleres Netto-Ereignisergebnis > 0 mit t-Wert ≥ **3,0**, als kleinster Wert aus iid (Ereignisse) und Clustern nach Quartal. Bei 108 Ereignissen entspricht das einer Sharpe Ratio von etwa ≥ 1,0 p. a. |
| 2 | ≥ 6 von 9 Jahren mit positivem Netto-Ergebnis |
| 3 | ≥ 3 von 4 Paaren mit positivem Netto-Ergebnis |
| 4 | Mittleres Ereignisergebnis bei doppelten Kosten > 0 |

**Variantenwahl:** Bestehen beide Varianten, gewinnt die mit dem höheren t-Wert. Besteht keine, ist **Strategie Nr. 5 gescheitert**, und der Hold-out bleibt unberührt.

**Beschreibend, ohne Einfluss auf die Entscheidung:**
- Ergebnis je Paar, vor und nach Kosten
- Regression der Fensterrendite der Fremdwährung (bp) auf `R_c − R_US` (%). Zum Vergleich: Steigung laut Paper etwa −1,4.
- Gewichtung mit `x_c` statt Vorzeichen
- Quartalsenden gegen übrige Monate
- Umkehr nach dem Fix: Gegenposition von 16:05 London bis 12:00 London am nächsten Londoner Geschäftstag
- Jahr 2014 (vor der Fix-Reform)

**Hold-out** (einmalig, gewählte Variante)

| # | Kriterium |
|---|---|
| 1 | Mittleres Netto-Ereignisergebnis > 0 |
| 2 | Mittleres Netto-Ereignisergebnis ≥ untere Grenze des 95-%-Konfidenzintervalls von IS (Bootstrap über Ereignisse) |

**FTMO** (Ereignisergebnisse IS + HO, nur falls der Hold-out besteht)

- **Skalierung:** Standardabweichung des Ereignisergebnisses = 0,5 %, 1,0 %, 1,5 % bzw. 2,0 % des Anfangskapitals, kalibriert auf IS.
  - Phase 2 mit dem 0,75-Fachen.
  - Ab 3 % Drawdown wird halbiert, ab 6 % geviertelt.
- **Tagesverlust und Max Loss:**
  - Je Ereignis zählt im Worst Case die Summe der ungünstigsten M5-Ausschläge aller offenen Positionen.
  - Bezug ist die Balance zu Beginn des Prager Tags (5 %) bzw. das Anfangskapital (10 %).
- **Mindesthandelstage:** 4 je Phase. Fehlende Tage füllt der „Mindesttage-Modus“ aus dem SMC-FTMO-Plan, also Minimalpositionen ohne Ergebniswirkung.
- **Bootstrap:** über Ereignisse, 10.000 Pfade, höchstens 120 Ereignisse je Pfad.
- **Bestanden:** wenn für mindestens eine Skalierung gilt:
  - Bestehenschance beider Phasen ≥ 70 %
  - Median-Dauer ≤ 6 Monate
- Alle vier Stufen werden berichtet.
- **Vorab festgehalten:** Mit einem Ereignis pro Monat ist das FTMO-Kriterium allein kaum erreichbar. Besteht das Modell IS und HO, aber nicht die FTMO-Stufe, wird es als Baustein für ein Ensemble (Strategie Nr. 100) vorgemerkt.

**FTMO-Konformität**
- Bis zu vier USD-Paare gleichzeitig, aber mit Richtungen, die vom Signal je Paar abhängen. Eine „one big dollar bet“ ist also nicht systematisch.
- Haltedauer 65 Minuten (M-1H) bzw. 8 Stunden (M-DAY). Damit ist es kein Tick-Scalping und keine Latenz-Arbitrage.

## 5. Umsetzbarkeit als MT5-EA

- **Daten im EA:** Kurse von US500.cash, FRA40.cash, UK100.cash, JP225.cash und AUS200.cash liegen auf dem FTMO-Server vor. Es werden keine externen Daten benötigt.
- **Zeit:** Serverzeit = New York + 7 h. Die Londoner Zeit leitet der EA aus den EU-Sommerzeitregeln ab.
- **Kalender:** Der EA enthält einen Kalender der englischen Bankfeiertage, mit Osterberechnung.
- **Logik:** Signal einmal zum Signalzeitpunkt berechnen, vier Marktorders senden, zur Ausstiegszeit schließen, Notfall-Stop als Server-Stop.

## 6. Trial-Log (Fortsetzung des globalen Logs)

| # | Test |
|---|---|
| T19 | M-1H, In-Sample |
| T20 | M-DAY, In-Sample |
| T21 | Hold-out der gewählten Variante (nur falls T19 oder T20 besteht) |
| T22 | FTMO-Bootstrap (nur falls T21 besteht) |
