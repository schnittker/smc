# Vorregistrierung: Swing-Portfolio (Strategie Nr. 100, Ensemble)

Festgelegt am 24.10.2026, **bevor** Code für dieses Portfolio geschrieben oder Daten ab 2024 für irgendeinen Baustein ausgewertet wurden. Änderungen nach diesem Commit zählen als neuer Versuch im Trial-Log (`../TRIAL_LOG.md`).

**Vorab festgehalten:**
- Die IS-Ergebnisse der vier Bausteine sind bekannt; sie wurden gerade wegen dieser Ergebnisse ausgewählt.
- In keinem Projekt existiert ein Hold-out-Marker (`DONE`). Daten ab 2024 wurden für keinen Baustein ausgewertet.

## 0. Feste Rahmenbedingungen (für alle Strategien gleich)

- Expert Advisor für MetaTrader 5, handelt vollständig autonom
- FTMO 2-Step, Swing, 100.000 USD
- Max. Verlust gesamt 10 %, max. Tagesverlust 5 %
- Ziel Phase 1 +10 %, Ziel Phase 2 +5 %
- News-Trading und Halten übers Wochenende erlaubt

## 1. Hypothese

Ein Portfolio aus vier Swing-Bausteinen mit je Sharpe 0,5–0,9 hat im Hold-out 2024–2026 eine positive Rendite, die mit dem IS-Ergebnis verträglich ist. Mit dieser Rendite besteht es die FTMO-Challenge in beiden Phasen mit ≥ 70 % Wahrscheinlichkeit. **Erwartung: offen; wegen der Auswahlverzerrung eher Scheitern im Hold-out.**

## 2. Bausteine, Daten, Kosten

Bausteine wie in der Recherche, mit **Code und Kostenmodell unverändert** aus den Projekten 09, 10, 14 und 24:
- **P-SPX:** `fomc.model.run_model_p`
- **T-FRÜH:** `tom.model.run_model_t`
- **V-VOL:** `volm.model.run_model_v`
- **F-CARRY:** `ffx.model.run_model_f` und `per_event`

Die Kurs- und Spread-Daten werden genauso geladen wie in den jeweiligen `run_*.py`.

**Zeiträume:**
- **In-Sample:** Servertage 2015–2023
- **Hold-out:** 01.01.2024 bis Datenende (16.10.2026)

## 3. Portfolio-Regeln

1. **Tagesbuchung** je Servertag d (Mo–Fr, Tag endet 17:00 New York):
   - **P-SPX, T-FRÜH:** Netto (Anteil des Nominals) am Servertag des Ausstiegs. Als Tages-Worst-Case gilt der gesamte MAE des Trades, konservativ an diesem Tag.
   - **V-VOL:** Netto und Worst-Case je Zeile am Tag der Zeile
   - **F-CARRY:** Netto je Termin am Ausstiegstag. Worst-Case = Summe `worst` der gehandelten Paare an diesem Tag.
   - Tage ohne Buchung zählen mit 0.
   - Der Kalender ist die Vereinigung aller Tage mit V-VOL-Zeile und aller Buchungstage.
2. **Gewichte (inverse Volatilität):**
   - g_c = 0,10 / (σ_c · √261), wobei σ_c die Standardabweichung der Tagesreihe von Baustein c über den IS-Kalender ist
   - Jeder Baustein wird also auf 10 % Jahresvola normiert.
   - Die Gewichte werden **nur aus IS** bestimmt und für den Hold-out eingefroren.
3. **Portfolio:**
   - Tagesrendite r = Σ g_c · r_c
   - Tages-Worst-Case w = Σ g_c · worst_c (Annahme: alle Extreme treffen gleichzeitig ein)
4. **Hebel:**
   - Das US500-Nominal je Tag ist g_P + g_T + g_V · w_V (bei offenen Positionen), jeweils mal FTMO-Skalierung.
   - Es muss auf jeder gewählten Stufe stets ≤ 10 × Kapital bleiben, sonst ist die Stufe ungültig.

## 4. Kriterien

**In-Sample (T306):** nur beschreibend.
- Bausteine: Gewicht, Mittel, σ, Sharpe
- Korrelationen der Tagesreihen
- Portfolio: Mittel, σ, Sharpe, t (iid, Woche, Monat), Jahre positiv, doppelte Kosten
- FTMO-Bootstrap nur auf IS-Daten (zur Einordnung)

Der Hold-out läuft, sobald das IS-Mittel des Portfolios > 0 ist. Ein schärferes IS-Kriterium wäre wegen der Auswahl der Bausteine bedeutungslos.

**Hold-out (T307, einmalig):** beide müssen erfüllt sein.

| # | Kriterium |
|---|---|
| 1 | Mittleres Netto-Tagesergebnis des Portfolios > 0 |
| 2 | ≥ untere Grenze des 95-%-Konfidenzintervalls von IS (Cluster-Bootstrap nach Kalendermonat) |

**FTMO (T308, Tagesreihe IS + Hold-out, nur falls T307 besteht):**
- **Skalierung:** k = s / σ_IS(Portfolio) für s = 0,5 %, 0,75 %, 1,0 % bzw. 1,25 % Tagesschwankung. Phase 2 mit 0,75 k. Ab 3 % Verlust gegenüber dem Startkapital wird halbiert, ab 6 % geviertelt.
- **Ablauf je Tag:**
  - Start-Equity e0
  - Durchgefallen, wenn e0 + k·w ≤ e0 − 5 % oder e0 + k·w ≤ 90 %
  - Danach e = e0 + k·r
  - Ziel erreicht bei e ≥ 110 % (Phase 1) bzw. 105 % (Phase 2) und ≥ 4 Tagen mit offener Position
- **Bootstrap:** Block-Bootstrap über Kalendermonate (Ziehen mit Zurücklegen), 10.000 Pfade, Seed 0. Je Phase höchstens 60 Monate; wer bis dahin nicht durch ist, zählt als nicht bestanden.
- **Bestanden**, wenn auf mindestens einer der vier Stufen beide Bedingungen gelten:
  - Wahrscheinlichkeit, beide Phasen zu bestehen, ≥ 70 %
  - Median-Dauer beider Phasen zusammen ≤ 12 Monate (unter den bestandenen Pfaden). Begründung: FTMO hat keine Zeitgrenze mehr; bei Swing ist ein Jahr für beide Phasen akzeptabel. Die bisherigen 6 Monate galten für tägliches Intraday.
- **Gültigkeit der Stufe:** Das Hebel-Kriterium aus 3.4 muss erfüllt sein. Die vier Stufen sind vier Versuche; sie werden im Trial-Log als einer geführt, mit Hinweis auf die Mehrfachprüfung.

**Beschreibend:**
- Ergebnis je Baustein im Hold-out
- Ergebnis je Jahr
- Historische FTMO-Starts (Start an jedem Monatsersten auf dem echten Pfad, Anteil bestanden)

## 5. Umsetzbarkeit als MT5-EA

Ein EA mit vier Modulen, alle auf festen Uhrzeiten New York:
- FOMC-Kalender (hinterlegt)
- NYSE-Handelstage
- tägliche Umschichtung US500 um 16:50
- FX-Korb an FOMC-Tagen nach Zinsrangfolge (Zinsen als hinterlegte Tabelle bzw. Eingabeparameter)

Die Positionsgrößen ergeben sich aus g_c, k und dem De-Risk-Faktor. Es werden keine externen Daten zur Laufzeit benötigt außer der Zins-Rangfolge, die selten wechselt.

## 6. Trial-Log (Fortsetzung des globalen Logs)

| # | Test |
|---|---|
| T306 | Swing-Portfolio (Nr. 100), In-Sample beschreibend |
| T307 | Hold-out 2024–2026 (verbraucht den Hold-out von Nr. 9, 10, 14, 24) |
| T308 | FTMO-Block-Bootstrap, 4 Stufen (nur falls T307 besteht) |
