# Vorregistrierung: Modell L „London Breakout“ (Strategie Nr. 31)

Festgelegt am 24.10.2026, **bevor** Code für dieses Modell geschrieben oder Daten dafür ausgewertet wurden. Änderungen nach diesem Commit zählen als neuer Versuch im Trial-Log (`../TRIAL_LOG.md`).

**Vorab festgehalten:** EURUSD und GBPUSD wurden intraday in Nr. 2 (Fix-Fenster) und Nr. 5 (Monatsende) ausgewertet. Die Asien-Range wurde nie betrachtet.

## 0. Feste Rahmenbedingungen (für alle Strategien gleich)

- Expert Advisor für MetaTrader 5, handelt vollständig autonom
- FTMO 2-Step, Swing, 100.000 USD
- Max. Verlust gesamt 10 %, max. Tagesverlust 5 %
- Ziel Phase 1 +10 %, Ziel Phase 2 +5 %
- News-Trading und Halten übers Wochenende erlaubt

## 1. Hypothese

Der erste Ausbruch aus der Asien-Range nach 07:00 London setzt sich bis zum Nachmittag fort. Ein Trade in Ausbruchsrichtung verdient nach Kosten mit t ≥ 3.

**Erwartung vor dem Test: Scheitern.**

## 2. Daten und Zeiträume

- HistData M5 (Bid); FX-Kostenmodell des SMC-Projekts: typischer Raw-Spread + 0,3 Pip, Kommission 5 USD pro Lot Round Turn, Slippage 0,1 Pip je Marktausführung (Stop-Order zählt als Marktausführung)
- Londoner Zeit über die EU-Sommerzeitregel (`mer.events.london_utc`, Nr. 5)
- Handelstage: Mo–Fr, ohne 24.12.–01.01.
- **In-Sample:** 2015–2023. **Hold-out:** ab 2024, einmalig und nur, wenn IS besteht.

## 3. Regeln (Londoner Zeit)

| Variante | Instrument |
|---|---|
| **L-GBP** | GBPUSD |
| **L-EUR** | EURUSD |

1. **Asien-Range:** Hoch H und Tief L (Bid) aller M5-Kerzen von 00:00 bis 07:00. Fehlen mehr als 12 der 84 Kerzen, entfällt der Tag.
2. **Orders ab 07:00:** Buy-Stop bei H + Spread (Ask erreicht H), Sell-Stop bei L (Bid erreicht L), One-Cancels-Other. Nur der erste Ausbruch bis 12:00 wird gehandelt. Gap über die Marke: Ausführung zur Eröffnung.
3. **Stop:** am anderen Ende der Range (Long: Bid ≤ L; Short: Ask ≥ H + Spread).
4. **Ausstieg:** spätestens zur Eröffnung der M5-Kerze um 16:00. Kein Take-Profit.
5. Treffen Einstieg und Stop in derselben Kerze, zählt der Stop (konservativ).
6. **Risiko R** = Einstieg − Stop (Long) bzw. Stop − Einstieg (Short), inklusive Spread.
7. **Positionsgröße:** Nominal = min(0,5 % Kapital / (R / Kurs), 10 × Kapital)

**Bewertungseinheit:** Netto-Tagesergebnis in Kapitalanteilen. Tage ohne Ausbruch zählen mit 0.

## 4. Akzeptanzkriterien

Wie Nr. 16 (alle müssen erfüllt sein): t ≥ **3,0** (kleinster aus iid, Woche, Monat) bei positivem Mittel; ≥ 6 von 9 Jahren positiv; beide Teilzeiträume positiv; doppelte Kosten > 0. Variantenwahl über den t-Wert. Besteht keine, ist **Strategie Nr. 31 gescheitert**, und der Hold-out bleibt unberührt.

**Beschreibend:** Ergebnis in R je Trade, Trefferquote, Anteil Stop / Tagesende, Range-Größe, Long gegen Short.

**Hold-out und FTMO:** wie Nr. 16.

## 5. Umsetzbarkeit als MT5-EA

Pending-Orders um 07:00 London, Löschen um 12:00, Schließen um 16:00, Server-Stop. Es werden keine externen Daten benötigt.

## 6. Trial-Log (Fortsetzung des globalen Logs)

| # | Test |
|---|---|
| T106 | L-GBP, In-Sample |
| T107 | L-EUR, In-Sample |
| T108 | Hold-out der gewählten Variante (nur falls T106 oder T107 besteht) |
| T109 | FTMO-Bootstrap (nur falls T108 besteht) |
