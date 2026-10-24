# Vorregistrierung: Modell N „NFP-Straddle“ (Strategie Nr. 94)

Festgelegt am 24.10.2026, **bevor** Code für dieses Modell geschrieben oder Daten dafür ausgewertet wurden. Änderungen nach diesem Commit zählen als neuer Versuch im Trial-Log (`../TRIAL_LOG.md`).

**Vorab festgehalten:** M1-Daten um 08:30 New York wurden nicht ausgewertet. In Nr. 31/32 wurden M5-Daten der Majors in anderen Sitzungen verwendet.

## 0. Feste Rahmenbedingungen (für alle Strategien gleich)

- Expert Advisor für MetaTrader 5, handelt vollständig autonom
- FTMO 2-Step, Swing, 100.000 USD
- Max. Verlust gesamt 10 %, max. Tagesverlust 5 %
- Ziel Phase 1 +10 %, Ziel Phase 2 +5 %
- News-Trading und Halten übers Wochenende erlaubt

## 1. Hypothese

Ein OCO-Straddle zur NFP-Veröffentlichung verdient nach pessimistischen Kosten mit t ≥ 3. **Erwartung: Scheitern.**

## 2. Daten, Kosten, Zeiträume

- **Kurse:** HistData M1 (Bid) für EURUSD, GBPUSD, USDJPY, XAUUSD
- **NFP-Termine 2015–2023** nach der BLS-Regel aus der Recherche (Feiertagsregel: Januar +7 Tage, sonst Donnerstag davor)
- **Kosten:** FX-Kostenmodell. Bei Ausführungen zwischen 08:30 und 08:34 gilt der **5-fache** effektive Spread und eine Slippage von **0,03 % des Kurses**; danach gelten die normalen Werte. Keine Swaps (Ausstieg vor dem Rollover).
- **In-Sample:** 2015–2023. **Hold-out:** ab 2024, einmalig bei Bestehen.

## 3. Regeln (New-York-Zeit, je Instrument und Termin)

1. **Referenz** P = Eröffnung der M1-Kerze 08:29. Abstand k = 0,10 % von P.
2. **Buy-Stop** bei P + k (Ask erreicht das Level), **Sell-Stop** bei P − k (Bid erreicht das Level), One-Cancels-Other, aktiv von 08:30 bis 08:39. Ein Gap über das Level wird zur Eröffnung der Kerze gefüllt.
3. Werden beide Level in derselben Kerze erreicht, gilt die Seite, die der Eröffnung näher liegt.
4. **Stop:** Einstieg ∓ 2k (Long: Bid ≤ Stop; Short: Ask ≥ Stop). Einstieg und Stop in derselben Kerze zählen als gestoppt.
5. **Ausstieg:** Markt zur Eröffnung der M1-Kerze 09:30
6. **Größe:** Nominal = min(0,25 % Kapital / (R / Einstieg), 10 × Kapital), R = Abstand Einstieg–Stop
7. **Portfolio:** Summe der 4 Instrumente je Termin

## 4. Akzeptanzkriterien

Alle müssen erfüllt sein:
- mittleres Netto-Ergebnis je Termin > 0 mit t ≥ **3,0** (kleinster aus iid, Quartal)
- ≥ 6 von 9 Jahren positiv
- ≥ 3 von 4 Instrumenten positiv
- doppelte Kosten > 0

Vor einem Hold-out gilt die Artefakt-Prüfung (Spielregel 6).

**Beschreibend:** Auslösequote, Stops, Ø R vor und nach Kosten, Ergebnis bei normalen statt 5-fachen Spreads (zur Einordnung, nicht entscheidend).

## 5. Umsetzbarkeit als MT5-EA

Ein Kalender mit NFP-Terminen wird nach der BLS-Regel berechnet oder hinterlegt. Der EA platziert um 08:29 New York Pending-Orders mit Stop und schließt um 09:30. Es werden keine externen Daten benötigt.

## 6. Trial-Log (Fortsetzung des globalen Logs)

| # | Test |
|---|---|
| T303 | N-NFP (Nr. 94), In-Sample |
| T304, T305 | Hold-out, FTMO (nur bei Bestehen) |
