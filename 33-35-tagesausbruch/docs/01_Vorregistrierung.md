# Vorregistrierung: Modell T „Tages-Ausbruch“ (Strategien Nr. 33, 34, 35)

Festgelegt am 24.10.2026, **bevor** Code für dieses Modell geschrieben oder Daten dafür ausgewertet wurden. Änderungen nach diesem Commit zählen als neuer Versuch im Trial-Log (`../TRIAL_LOG.md`).

**Vorab festgehalten:** Alle Instrumente wurden in früheren Tests ausgewertet, z. B. Trend (Nr. 3, 4, 28, 30), ORB (Nr. 16) und London Breakout (Nr. 31). Tagesmuster wie NR7, Inside Bar und Volatility Breakout wurden nicht angesehen.

## 0. Feste Rahmenbedingungen (für alle Strategien gleich)

- Expert Advisor für MetaTrader 5, handelt vollständig autonom
- FTMO 2-Step, Swing, 100.000 USD
- Max. Verlust gesamt 10 %, max. Tagesverlust 5 %
- Ziel Phase 1 +10 %, Ziel Phase 2 +5 %
- News-Trading und Halten übers Wochenende erlaubt

## 1. Hypothese

Die Tages-Ausbruchsregeln NR7, Inside Bar und Volatility Breakout verdienen über ein diversifiziertes Universum nach Kosten mit t ≥ 3.

**Erwartung vor dem Test: Scheitern aller drei.**

## 2. Daten und Zeiträume

- **D1-Kerzen** des FTMO-Servertags (17:00–17:00 New York) aus HistData. Intraday-Pfad aus M5.
- **Universum** (17): EURUSD, GBPUSD, USDJPY, AUDUSD, NZDUSD, USDCAD, USDCHF, XAUUSD (FX-Kostenmodell); US500, US100, FRA40, UK100, JP225, HK50, AUS200, Brent, Silber (Kostenmodell H)
- **Kosten:** Spread (Kauf zum Ask), Kommission, Slippage je Marktausführung (FX 0,1 Pip, CFD ¼ Spread); Stop-Orders zählen als Marktausführung. Keine Swaps, weil vor dem Rollover geschlossen wird.
- Kein Handel an Servertagen vom 24.12. bis 01.01.
- **In-Sample:** 2015–2023. **Hold-out:** ab 2024, einmalig je bestandener Variante.

## 3. Regeln (je Instrument und Servertag i, Signal aus den abgeschlossenen D1-Kerzen bis i−1)

| Variante | Listen-Nr. | Bedingung (aus i−1) | Kauf-Level | Verkaufs-Level |
|---|---|---|---|---|
| **T-NR7** | 33 | Range(i−1) = kleinste der letzten 7 Ranges | Hoch(i−1) | Tief(i−1) |
| **T-INSIDE** | 34 | Hoch(i−1) < Hoch(i−2) und Tief(i−1) > Tief(i−2) | Hoch(i−1) | Tief(i−1) |
| **T-LW** | 35 | jeder Tag | Eröffnung(i) + 0,5 × Range(i−1) | Eröffnung(i) − 0,5 × Range(i−1) |

**Gemeinsam**
- Buy-Stop (Ask erreicht das Kauf-Level) und Sell-Stop (Bid erreicht das Verkaufs-Level), One-Cancels-Other, aktiv vom Tagesbeginn bis 1 Stunde vor Tagesende. Gap über ein Level: Ausführung zur Eröffnung.
- **Stop:** am jeweils anderen Level
- **Ausstieg:** Schluss der letzten M5-Kerze des Servertags (16:55–17:00 New York)
- Einstieg und Stop in derselben M5-Kerze zählen als gestoppt.
- **Größe:** Nominal = min(0,25 % Kapital / (R / Kurs), 10 × Kapital), R = Abstand Einstieg–Stop
- **Portfolio:** Summe aller Instrumente je Tag

## 4. Akzeptanzkriterien

Wie Nr. 3 (alle müssen erfüllt sein): t ≥ **3,0** (kleinster aus iid, Woche, Monat) bei positivem Mittel; ≥ 6 von 9 Jahren positiv; ≥ 60 % der Instrumente positiv; doppelte Kosten > 0. **Jede Variante wird für sich bewertet** (eigene Listennummer).

**Beschreibend:** Trades, Ø R vor und nach Kosten, Trefferquote, Stops, Ergebnis je Instrument.

**Hold-out und FTMO:** wie Nr. 16, je bestandener Variante.

## 5. Umsetzbarkeit als MT5-EA

D1-Muster aus den Serverkerzen, Pending-Orders zu Tagesbeginn, Schließen vor dem Rollover. Es werden keine externen Daten benötigt.

## 6. Trial-Log (Fortsetzung des globalen Logs)

| # | Test |
|---|---|
| T114 | T-NR7 (Nr. 33), In-Sample |
| T115 | T-INSIDE (Nr. 34), In-Sample |
| T116 | T-LW (Nr. 35), In-Sample |
| T117–T122 | Hold-out und FTMO je bestandener Variante |
