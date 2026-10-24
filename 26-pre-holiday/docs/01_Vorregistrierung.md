# Vorregistrierung: Modell H „Pre-Holiday US-Indizes“ (Strategie Nr. 26)

Festgelegt am 24.10.2026, **bevor** Code für dieses Modell geschrieben oder Daten dafür ausgewertet wurden. Änderungen nach diesem Commit zählen als neuer Versuch im Trial-Log (`../TRIAL_LOG.md`).

**Vorab festgehalten:** US500 und US100 wurden in Nr. 9–16 ausgewertet. Die Tage vor Feiertagen wurden nicht gesondert angesehen. In Nr. 10 lagen einige davon (z. B. 24.12. und 03.07.) in den Monatswechsel-Fenstern.

## 0. Feste Rahmenbedingungen (für alle Strategien gleich)

- Expert Advisor für MetaTrader 5, handelt vollständig autonom
- FTMO 2-Step, Swing, 100.000 USD
- Max. Verlust gesamt 10 %, max. Tagesverlust 5 %
- Ziel Phase 1 +10 %, Ziel Phase 2 +5 %
- News-Trading und Halten übers Wochenende erlaubt

## 1. Hypothese

Long US-Index über den letzten Handelstag vor einem NYSE-Feiertag verdient nach Kosten mit t ≥ 3 (Ariel 1990).

**Erwartung vor dem Test: Scheitern.**

## 2. Daten und Zeiträume

- HistData M5 und D1 (Bid); Positionsmechanik, Kosten, Swaps und Notfall-Stop wie Nr. 9 (`fomc.model.Index.trade_long`, Kostenmodell H)
- NYSE-Kalender aus Nr. 10 (reguläre Feiertage, ohne die Sonderschließungen 2018 und 2025); verkürzte Tage nach Nr. 11
- **In-Sample:** Feiertage 2015–2023. **Hold-out:** ab 2024, einmalig und nur, wenn IS besteht.

## 3. Regeln

- **Ereignis:** jeder reguläre NYSE-Feiertag h an einem Werktag. Vortag p = letzter NYSE-Handelstag vor h, q = Handelstag vor p.
- **Einstieg:** 15:55 New York an q. **Ausstieg:** 15:55 an p, bzw. 12:55, wenn p ein verkürzter Tag ist (Schluss 13:00).
- Long, Nominal = 1 × Kapital. Notfall-Stop 3 × ATR14(D1). Fehlt eine Kerze, entfällt das Ereignis.

| Variante | Instrument |
|---|---|
| **H-SPX** | US500 |
| **H-NDX** | US100 |

**Bewertungseinheit:** Netto-Ergebnis je Ereignis in bp.

## 4. Akzeptanzkriterien

Wie Nr. 10 (alle müssen erfüllt sein): t ≥ **3,0** (kleinster aus iid und Clustern nach Quartal) bei positivem Mittel; ≥ 6 von 9 Jahren positiv; beide Teilzeiträume 2015–2019 und 2020–2023 positiv; doppelte Kosten > 0. Variantenwahl über den t-Wert. Besteht keine, ist **Strategie Nr. 26 gescheitert**, und der Hold-out bleibt unberührt.

**Beschreibend:** Vergleich mit allen übrigen Handelstagen (15:55 bis 15:55); Ergebnis je Feiertag.

**Hold-out und FTMO:** wie Nr. 10.

## 5. Umsetzbarkeit als MT5-EA

NYSE-Feiertagskalender im EA (Nr. 10), Orders um 15:55 New York. Es werden keine externen Daten benötigt.

## 6. Trial-Log (Fortsetzung des globalen Logs)

| # | Test |
|---|---|
| T88 | H-SPX, In-Sample |
| T89 | H-NDX, In-Sample |
| T90 | Hold-out der gewählten Variante (nur falls T88 oder T89 besteht) |
| T91 | FTMO-Bootstrap (nur falls T90 besteht) |
