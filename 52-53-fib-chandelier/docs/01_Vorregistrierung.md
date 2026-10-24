# Vorregistrierung: Modell FC „Fibonacci-Pullback und Chandelier-Trend“ (Strategien Nr. 52 und 53)

Festgelegt am 24.10.2026, **bevor** Code für dieses Modell geschrieben oder Daten dafür ausgewertet wurden. Änderungen nach diesem Commit zählen als neuer Versuch im Trial-Log (`../TRIAL_LOG.md`).

**Vorab festgehalten:** H4-Swings derselben Instrumente wurden in Nr. 50/51 verwendet, 55-Tage-Ausbrüche mit 20-Tage-Ausstieg in Nr. 30. Fibonacci-Zonen und Chandelier-Stops wurden nicht angesehen.

## 0. Feste Rahmenbedingungen (für alle Strategien gleich)

- Expert Advisor für MetaTrader 5, handelt vollständig autonom
- FTMO 2-Step, Swing, 100.000 USD
- Max. Verlust gesamt 10 %, max. Tagesverlust 5 %
- Ziel Phase 1 +10 %, Ziel Phase 2 +5 %
- News-Trading und Halten übers Wochenende erlaubt

## 1. Hypothesen

- **Nr. 52 (FC-FIB):** Einstiege im 50–61,8-%-Rücklauf eines H4-Impulses verdienen nach Kosten mit t ≥ 3.
- **Nr. 53 (FC-CHAND):** 55-Tage-Ausbrüche mit Chandelier-Trailing-Stop verdienen nach Kosten mit t ≥ 3.

**Erwartung vor dem Test: Scheitern beider.**

## 2. Daten, Universum, Kosten, Zeiträume

- **Universum:** die 17 Instrumente aus Nr. 33–38
- **Kosten:** Spread, Kommission, Slippage und Swaps
- **In-Sample:** Einstiege 2015–2023, Kurse bis 31.12.2023. **Hold-out:** ab 2024, einmalig je bestandener Variante.
- **FC-FIB:** H4-Serverkerzen
- **FC-CHAND:** D1-Servertage Mo–Fr aus M5 (`dbo.model.server_days`)

## 3. Regeln

**FC-FIB (Nr. 52)**

Swings wie in Nr. 50/51: 3 Kerzen je Seite, bestätigt 3 Kerzen später (`chart.swings`).

**Impuls aufwärts:** Das letzte bestätigte Swing-Hoch H (Kerze jH) liegt nach dem letzten bestätigten Swing-Tief L (jL < jH) und H − L ≥ 3 × ATR14(i).
- **Long-Signal** am Schluss von i, wenn H − 0,618 (H − L) ≤ C(i) ≤ H − 0,5 (H − L) und seit jH noch kein Schluss in dieser Zone lag (nur der erste Eintritt je Impuls)
- **Stop:** L − 0,25 × ATR14(i)
- **Ziel:** H (Limit)

**Impuls abwärts:** gespiegelt.

Weitere Regeln:
- Stop-Abstand mindestens 1 ATR; liegt das Ziel nach dem Einstieg nicht mehr in Gewinnrichtung, gibt es keinen Trade.
- Zeitstopp nach 30 Kerzen
- Engine wie Nr. 50/51 (`chart.engine`, mit Ziel-Level statt R-Vielfachem)

**FC-CHAND (Nr. 53)**
- **Long-Einstieg** zur Eröffnung des Servertags i+1, wenn C(i) > max C(i−55 … i−1). Short gespiegelt mit dem Minimum.
- **Chandelier-Stop (Long):** S(i) = max(S(i−1), HH − 3 × ATR22(i)) mit HH = höchstes Hoch seit Einstieg. Beim Einstieg gilt S = Einstieg − 3 × ATR22(i). Der Stop wird am Schluss jedes Tages nachgezogen und gilt ab der nächsten Kerze als Stop-Order (Long: Bid ≤ S; Short: Ask ≥ S). Ein Gap wird zur Eröffnung gefüllt.
- Kein Ziel und kein Zeitstopp
- Ein neues Signal ist frühestens am Schluss des Tages nach dem Ausstieg möglich.

**Gemeinsam**
- Je Instrument höchstens eine Position
- Keine neuen Einstiege an Servertagen 24.12.–01.01.
- **Größe:** Nominal = min(0,25 % Kapital / (R / Einstieg), 10 × Kapital), R = anfänglicher Stop-Abstand
- **Portfolio:** Summe aller Instrumente; Ergebnis am Servertag des Ausstiegs, Tage ohne Ausstieg zählen als 0

## 4. Akzeptanzkriterien

Wie Nr. 33–51 (alle müssen erfüllt sein): t ≥ **3,0** (kleinster aus iid, Woche, Monat) bei positivem Mittel; ≥ 6 von 9 Jahren positiv; ≥ 60 % der Instrumente positiv; doppelte Kosten > 0. Jede Variante wird für sich bewertet. Vor einem Hold-out gilt die Artefakt-Prüfung (Spielregel 6).

**Beschreibend:** Trades, Ø R vor und nach Kosten, Ausstiegsarten, Haltedauer, Ergebnis je Instrument und Anlageklasse.

**Hold-out und FTMO:** wie Nr. 16.

## 5. Umsetzbarkeit als MT5-EA

Swings und Fibonacci-Zonen aus H4, 55-Tage-Kanal und ATR aus D1-Serverkerzen. Marktorders, ein fester bzw. täglich nachgezogener Stop. Es werden keine externen Daten benötigt.

## 6. Trial-Log (Fortsetzung des globalen Logs)

| # | Test |
|---|---|
| T183 | FC-FIB (Nr. 52), In-Sample |
| T184 | FC-CHAND (Nr. 53), In-Sample |
| T185–T188 | Hold-out und FTMO je bestandener Variante |
