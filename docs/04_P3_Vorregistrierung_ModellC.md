# P3 – Vorregistrierung: Modell C „Trend-Fortsetzung“

Festgelegt am 24.10.2026, **bevor** Code für dieses Modell geschrieben oder Ergebnisse angesehen wurden. Änderungen nach diesem Commit zählen als neuer Versuch im Trial-Log.

## 1. Hypothese

Wenn ein H1-Gegen-Swing gegen den H4-Trend endet, setzt sich der Kurs in Richtung des H4-Trends weit genug fort. Endet heißt: Der strikte H1-Trend kippt zurück in die H4-Richtung. „Weit genug“ heißt: Unter FTMO-Kosten bleiben im Mittel mindestens **+0,10 R netto pro Trade**.

Herkunft: In der Ereignisstudie P2 war dies der größte Brutto-Effekt (+0,14 R), aber nach Korrektur nicht signifikant. Die externe Evidenz (MrOwl1011) zeigt einen Trendfilter als dominanten Faktor.

## 2. Daten und Zeiträume

- HistData M1 (Bid), umgerechnet in FTMO-Serverzeit; alle 25 Instrumente.
- **In-Sample (IS):** Signale vom 01.01.2015 bis 31.12.2023.
- **Hold-out (HO):** Signale vom 01.01.2024 bis zum Datenende am 16.10.2026. Der HO wird genau **einmal** ausgewertet, nur für die in IS gewählte Variante und nur wenn sie die IS-Kriterien erfüllt.

## 3. Regeln (beide Richtungen spiegelbildlich, hier Long)

**Signal (bei Close der H1-Kerze k)**
- Es gibt einen strikten H1-Trendwechsel nach oben (`CHOCH_STRICT`, Richtung +1).
- Der strikte H4-Trend, gelesen an der letzten geschlossenen H4-Kerze, ist ebenfalls +1.
- Auf dem Symbol ist keine Position und keine Pending-Order offen. Signale während einer offenen Position werden ignoriert.

**Stop**
- Anker ist das neue H1-Protected-Low, also das Tief des beendeten Gegen-Swings (`ref_i` des Ereignisses).
- `SL = Anker − Puffer` mit `Puffer = max(2 × typischer Spread, 0,1 × ATR14(M15))`, ATR gelesen an der letzten geschlossenen M15-Kerze.
- Short spiegelbildlich: Der Stop liegt über dem Protected High.

**Einstieg, zwei Varianten**
- **C-MKT:** Markt zur Eröffnung der ersten M5-Kerze nach dem Signal. Long kauft zum Ask (= Open + Spread), Short verkauft zum Bid.
- **C-LMT:** Limit-Order in einer Zone des Bestätigungs-Legs, also von der H1-Kerze des Ankers bis zur Signal-Kerze.
  - **Zonenwahl:**
    1. jüngstes M15-FVG in Richtung +1, entstanden in diesem Fenster und bis zum Signal unberührt; Einstieg am CE
    2. sonst der jüngste unberührte M15-Order-Block in Richtung +1 aus dem Fenster; Einstieg am Mean Threshold
    3. sonst kein Trade
  - **Gültigkeit** bis zum Fill, längstens 288 M5-Kerzen (24 Handelsstunden).
  - **Storno vor dem Fill**, wenn:
    - das Ziel erreicht wird,
    - der Stop-Level erreicht wird,
    - oder der H4-Trend dreht.

**Ziel (beim Fill festgelegt)**
- **Nächster aktiver Pool:** Gesucht ist der nächstgelegene Buy-Side-Liquiditätspool, der zum Fill-Zeitpunkt aktiv ist und mindestens **2 R** über dem Einstieg liegt.
  - Aktiv heißt: bekannt, nicht abgelaufen und vor dem Fill noch nicht durchstochen.
  - In Frage kommen alle Pool-Typen der Pipeline.
- **Deckel:** Liegt dieser Pool weiter als 4 R entfernt, gilt TP = 4 R.
- **Kein Pool:** Gibt es keinen, gilt TP = 2 R.

**Ausstieg**
- TP, SL oder Zeit-Stopp nach 864 M5-Kerzen (≈ 3 Handelstage) zum Close dieser Kerze.
- Halten über Nacht und Wochenende ist erlaubt (Swing-Konto).

**Fill-Regeln** (Bid-Kerzen; Ask-seitige Trigger um den Spread korrigiert)

| Ereignis | Long | Short |
|---|---|---|
| Limit-Fill (Einstieg P) | Low ≤ P − Spread − 1 Tick | High ≥ P + 1 Tick |
| Stop ausgelöst | Low ≤ SL | High ≥ SL − Spread |
| Ziel ausgelöst | High ≥ TP + 1 Tick | Low ≤ TP − Spread − 1 Tick |

- Treffen SL und TP in derselben Kerze, gilt der **Verlust**.
- In der Fill-Kerze wird nur der SL geprüft, das Ziel erst ab der Folgekerze.

**Kosten**
- Der Spread ist über Ask/Bid in den Fills enthalten. Spread = typischer Raw-Spread + 0,3 Pip Volume-Band-Zuschlag; bei XAUUSD + 0,05 USD.
- Zusätzlich abgezogen werden die FTMO-Kommission (5 USD pro Lot Round Turn bzw. 0,0014 % bei Gold) und Slippage: 0,1 Pip bei Markteinstieg und Zeit-Stopp sowie bei jedem Stop.
- **Kosten-Gate:** Liegen die gesamten Kosten inklusive Spread über 0,10 R, wird der Trade ausgelassen.

**Feste Parameter (keine Optimierung)**
- Pivots: H4 5/20, H1 5/30, M15 5/40
- FVG-Mindestgröße M15: 0,20 × ATR14
- Displacement M15: 1,3
- RRmin = 2, Deckel 4 R, Zeit-Stopp 864 Bars, Limit-Gültigkeit 288 Bars
- Kosten-Gate 0,10 R

## 4. Portfolio- und FTMO-Stufe

**Portfolio-Filter** (Trades in zeitlicher Reihenfolge über alle Symbole)
- höchstens 3 gleichzeitig offene Positionen
- je Cluster (A: EUR/GBP vs USD, B: AUD/NZD, D: JPY, E: CHF, F: CAD; laut Blueprint §11.3) höchstens 1 offene Position
- nach 2 Verlusten an einem FTMO-Tag (Prager Kalendertag) keine neuen Einstiege an diesem Tag

**FTMO-Simulation**
- Die gefilterten Netto-R-Ergebnisse laufen chronologisch durch die Challenge-Regeln: Risikoleiter 1 % / 0,75 %, ab 3 % Drawdown halbiert, ab 6 % geviertelt; Max Loss 10 %, Daily Loss 5 % mit offenen Positionen im Worst Case.
- Der Block-Bootstrap über Kalendermonate (10.000 Pfade) liefert die Bestehenschance und die Dauer.

## 5. Akzeptanzkriterien

**In-Sample, je Variante** (alle müssen erfüllt sein)

| # | Kriterium |
|---|---|
| 1 | Netto-Erwartungswert ≥ +0,10 R pro Trade |
| 2 | t-Wert des Netto-Erwartungswerts ≥ 2,5 |
| 3 | Netto-Profit-Factor ≥ 1,2 |
| 4 | ≥ 6 von 9 Jahren mit positivem Netto-Erwartungswert |
| 5 | ≥ 60 % der Instrumente (mit ≥ 10 Trades) mit positivem Netto-Erwartungswert |
| 6 | bei doppelten Kosten Netto-Erwartungswert > 0 |

**Variantenwahl:** Erfüllen beide Varianten alle Kriterien, gewinnt die mit dem höheren t-Wert. Erfüllt keine, ist **P3 gescheitert**, und der Hold-out bleibt unberührt.

**Hold-out, nur die gewählte Variante, einmalig**

| # | Kriterium |
|---|---|
| 1 | Netto-Erwartungswert > 0 und Netto-PF > 1,1 |
| 2 | Netto-Erwartungswert nicht signifikant schlechter als In-Sample (Differenz innerhalb des 95-%-Konfidenzintervalls von In-Sample) |

**FTMO** (portfolio-gefilterte Trades IS + HO)

| # | Kriterium |
|---|---|
| 1 | Bestehenschance für beide Phasen ≥ 70 % |
| 2 | Median-Dauer ≤ 6 Monate |

## 6. Trial-Log (Fortsetzung)

| # | Test |
|---|---|
| T2 | C-MKT, In-Sample |
| T3 | C-LMT, In-Sample |
| T4 | Hold-out der gewählten Variante (nur falls T2 oder T3 besteht) |
| T5 | Portfolio-Filter und FTMO-Bootstrap |
