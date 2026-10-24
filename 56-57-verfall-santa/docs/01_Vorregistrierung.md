# Vorregistrierung: Modell KA „Verfall und Santa Rally“ (Strategien Nr. 56 und 57)

Festgelegt am 24.10.2026, **bevor** Code für dieses Modell geschrieben oder Daten dafür ausgewertet wurden. Änderungen nach diesem Commit zählen als neuer Versuch im Trial-Log (`../TRIAL_LOG.md`).

**Vorab festgehalten:** US500 und US100 wurden mit Kalenderregeln ausgewertet: Monatswechsel (Nr. 10), Pre-Holiday (Nr. 26), Halloween (Nr. 27), FOMC (Nr. 9). Die tägliche Renditetabelle um den Monatswechsel in Nr. 10 enthält indirekt Tage der OPEX-Wochen. OPEX-Fenster und das Santa-Fenster wurden nicht ausgewertet.

## 0. Feste Rahmenbedingungen (für alle Strategien gleich)

- Expert Advisor für MetaTrader 5, handelt vollständig autonom
- FTMO 2-Step, Swing, 100.000 USD
- Max. Verlust gesamt 10 %, max. Tagesverlust 5 %
- Ziel Phase 1 +10 %, Ziel Phase 2 +5 %
- News-Trading und Halten übers Wochenende erlaubt

## 1. Hypothesen

- **Nr. 56:** US500 ist in OPEX-Wochen positiv (K-OPEX, Long) bzw. in der Woche danach negativ (K-POST, Short). Beides verdient nach Kosten mit t ≥ 3.
- **Nr. 57:** US500 ist in der Santa-Rally-Phase positiv (K-SANTA, Long).

**Erwartung vor dem Test: Scheitern aller drei.**

## 2. Daten, Kosten, Zeiträume

- **US500** entscheidet, US100 wird beschreibend mitgeführt.
- NYSE-Handelstage (`tom.nyse`), Kurse um 15:55 New York
- Positionsmechanik und Kosten wie Nr. 9/10 (`fomc.model.Index`): Kostenmodell H, Notfall-Stop 3 × ATR14 (D1), Swaps; Position 1 × Kapital. Für Shorts gilt dieselbe Mechanik gespiegelt.
- **In-Sample:** Ereignisse mit Ausstieg 2015–2023. **Hold-out:** Ausstieg ab 2024, einmalig je bestandener Variante.

## 3. Regeln

**OPEX-Tag:** dritter Freitag des Monats; ist er kein NYSE-Handelstag, gilt der vorherige Handelstag. Relative Handelstage zählen ab OPEX = 0.

| Variante | Listen-Nr. | Richtung | Einstieg (15:55) | Ausstieg (15:55) |
|---|---|---|---|---|
| **K-OPEX** | 56 | Long | Handelstag −5 | OPEX-Tag (0) |
| **K-POST** | 56 | Short | OPEX-Tag (0) | Handelstag +5 |
| **K-SANTA** | 57 | Long | 6. letzter Handelstag im Dezember (vor den letzten 5) | 2. Handelstag im Januar |

## 4. Akzeptanzkriterien

Wie Nr. 10 (alle müssen erfüllt sein):
- mittleres Netto-Ergebnis je Ereignis > 0 mit t ≥ **3,0** (kleinster aus iid, Quartal)
- ≥ 6 von 9 Jahren positiv
- beide Teilzeiträume 2015–2019 und 2020–2023 positiv
- doppelte Kosten > 0

Jede Variante wird für sich bewertet. Vor einem Hold-out gilt die Artefakt-Prüfung (Spielregel 6).

**Beschreibend:** US100 mit denselben Fenstern; Quartals-OPEX (März, Juni, September, Dezember) gegenüber den übrigen Monaten.

**Hold-out und FTMO:** wie Nr. 10.

## 5. Umsetzbarkeit als MT5-EA

NYSE-Kalender und Verfallstermine sind im EA hinterlegt. Gehandelt wird eine Marktorder um 15:55 New York mit Server-Stop. Es werden keine externen Daten benötigt.

## 6. Trial-Log (Fortsetzung des globalen Logs)

| # | Test |
|---|---|
| T201 | K-OPEX (Nr. 56), In-Sample |
| T202 | K-POST (Nr. 56), In-Sample |
| T203 | K-SANTA (Nr. 57), In-Sample |
| T204–T209 | Hold-out und FTMO je bestandener Variante |
