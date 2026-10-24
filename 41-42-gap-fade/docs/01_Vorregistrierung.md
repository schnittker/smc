# Vorregistrierung: Modell Q „Gap-Fade“ (Strategien Nr. 41 und 42)

Festgelegt am 24.10.2026, **bevor** Code für dieses Modell geschrieben oder Daten dafür ausgewertet wurden. Änderungen nach diesem Commit zählen als neuer Versuch im Trial-Log (`../TRIAL_LOG.md`).

**Vorab festgehalten:** In Nr. 11 wurden US500 und US100 um 09:30–10:00 New York ausgewertet; die Übernachtrendite wurde dort als Teil des Signals verwendet. In Nr. 12 ging es um die Übernachtrenditen von US500. Gap-Fades und Montags-Gaps in FX wurden nicht angesehen.

## 0. Feste Rahmenbedingungen (für alle Strategien gleich)

- Expert Advisor für MetaTrader 5, handelt vollständig autonom
- FTMO 2-Step, Swing, 100.000 USD
- Max. Verlust gesamt 10 %, max. Tagesverlust 5 %
- Ziel Phase 1 +10 %, Ziel Phase 2 +5 %
- News-Trading und Halten übers Wochenende erlaubt

## 1. Hypothese

Gaps zur Kassa-Eröffnung (Indizes) bzw. zur Montagseröffnung (FX) schließen sich so oft, dass ein Fade zum Vorschluss nach Kosten mit t ≥ 3 verdient.

**Erwartung vor dem Test: Scheitern beider.**

## 2. Daten, Kosten und Zeiträume

- HistData M5, Bid-Kurse
- **Q-IDX:** US500, US100, FRA40, UK100 mit Kostenmodell H (FTMO-Spread relativ, Slippage ¼ Spread je Marktausführung)
- **Q-FXW:** EURUSD, GBPUSD, USDJPY, AUDUSD, NZDUSD, USDCAD, USDCHF mit FX-Kostenmodell (effektiver Spread, Kommission, 0,1 Pip Slippage). Zur Montagseröffnung wird der **dreifache** effektive Spread angesetzt (Annahme für die geweiteten Sonntagsspreads).
- **Limit-Ausführung:** Ziel-Ausführungen sind Limit-Orders zum Ziel ohne Slippage; Long verkauft zum Bid, Short kauft zum Ask.
- Keine Swaps, weil alle Positionen vor dem Rollover geschlossen werden.
- **In-Sample:** 2015–2023. **Hold-out:** ab 2024, einmalig je bestandener Variante.

## 3. Regeln

| | **Q-IDX (Nr. 41)** | **Q-FXW (Nr. 42)** |
|---|---|---|
| Vorschluss P | Schluss der Kassasitzung am vorigen Handelstag: Bid zur Eröffnung der M5-Kerze zur Schlusszeit (US 16:00 New York, an NYSE-Halbtagen 13:00; FRA40 17:30 Paris; UK100 16:30 London) | Schluss der letzten M5-Kerze des Server-Freitags |
| Einstieg (Marktorder) | Eröffnung O der M5-Kerze zur Kassa-Eröffnung: US 09:30 New York, FRA40 09:00 Paris, UK100 08:00 London | Eröffnung O der M5-Kerze Server-Montag 01:00 (Sonntag 18:00 New York) |
| Gap g = (O − P) / P | Handel, wenn 0,10 % ≤ \|g\| ≤ 1,00 % | Handel, wenn \|g\| ≥ 0,10 % |
| Richtung | gegen das Gap (−sign g) | gegen das Gap |
| Ziel (Limit) | P | P |
| Stop | O ± \|O − P\| auf der Gegenseite (Long: Bid ≤ O − \|O − P\|; Short: Ask ≥ O + \|O − P\|) | wie Q-IDX |
| Zeitausstieg (Markt) | Kassa-Schluss desselben Tages (Zeit wie bei P) | Schluss der letzten M5-Kerze des Server-Montags |
| Handelstage | US: NYSE-Kalender; EU: Werktage mit M5-Kerzen zur Eröffnungs- und Schlusszeit am Handelstag und am Vortag | jedes Wochenende mit Freitags- und Montagsdaten |

**Gemeinsam**
- Treffen Ziel und Stop in derselben M5-Kerze, zählt der Stop.
- **Größe:** Nominal = min(0,25 % Kapital / (R / Einstieg), 10 × Kapital), R = Abstand Einstieg–Stop
- Keine Trades an Tagen 24.12.–01.01.
- **Portfolio:** Summe aller Instrumente je Tag; Tage ohne Trade zählen als 0 (Q-IDX: alle Handelstage; Q-FXW: alle Montage)

## 4. Akzeptanzkriterien

Wie Nr. 33–40 (alle müssen erfüllt sein): t ≥ **3,0** (kleinster aus iid, Woche, Monat) bei positivem Mittel; ≥ 6 von 9 Jahren positiv; ≥ 60 % der Instrumente positiv; doppelte Kosten > 0. **Jede Variante wird für sich bewertet.**

**Beschreibend:** Füllquote (Ziel erreicht), Stops, Zeitausstiege, Ø R vor und nach Kosten, Ergebnis nach Gap-Größe (Terzile) und je Instrument.

**Hold-out und FTMO:** wie Nr. 16, je bestandener Variante.

## 5. Umsetzbarkeit als MT5-EA

Zeitgesteuerte Marktorder mit Limit-Ziel und Stop, Schließen zur festen Uhrzeit. Der NYSE-Kalender für US-Halbtage ist im EA hinterlegt. Es werden keine externen Daten benötigt.

## 6. Trial-Log (Fortsetzung des globalen Logs)

| # | Test |
|---|---|
| T138 | Q-IDX (Nr. 41), In-Sample |
| T139 | Q-FXW (Nr. 42), In-Sample |
| T140–T143 | Hold-out und FTMO je bestandener Variante |
