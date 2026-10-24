# Vorregistrierung: Modell J „Multi-Timeframe-Pullback“ (Strategie Nr. 45)

Festgelegt am 24.10.2026, **bevor** Code für dieses Modell geschrieben oder Daten dafür ausgewertet wurden. Änderungen nach diesem Commit zählen als neuer Versuch im Trial-Log (`../TRIAL_LOG.md`).

**Vorab festgehalten:** D1-, H4- und H1-Daten derselben 17 Instrumente wurden für Trend-, Ausbruchs- und Umkehrregeln ausgewertet (Nr. 3, 4, 28, 30, 33–40). Ein kombinierter Pullback-Einstieg wurde nicht angesehen.

## 0. Feste Rahmenbedingungen (für alle Strategien gleich)

- Expert Advisor für MetaTrader 5, handelt vollständig autonom
- FTMO 2-Step, Swing, 100.000 USD
- Max. Verlust gesamt 10 %, max. Tagesverlust 5 %
- Ziel Phase 1 +10 %, Ziel Phase 2 +5 %
- News-Trading und Halten übers Wochenende erlaubt

## 1. Hypothese

Rücksetzer auf H1 in Richtung des D1/H4-Trends verdienen nach Kosten mit t ≥ 3.

**Erwartung vor dem Test: Scheitern.**

## 2. Daten, Universum, Kosten, Zeiträume

- **Daten:** H1-Serverkerzen und D1-Servertage aus HistData M5 (`dbo.model.server_days`, Mo–Fr). H4-Werte werden aus H1 berechnet (H4-Serverkerzen).
- **Universum, Kosten, Swaps:** wie Nr. 36/38 (17 Instrumente; Spread, Kommission, Slippage, Swaps je Rollover)
- **In-Sample:** Einstiege 2015–2023, Kurse bis 31.12.2023. **Hold-out:** ab 2024, einmalig.

## 3. Regeln (je Instrument; Signal am Schluss der H1-Kerze i, Ausführung zur Eröffnung von i+1)

**Trend (nur abgeschlossene Kerzen)**

| Ebene | Aufwärtstrend | Abwärtstrend |
|---|---|---|
| D1 (letzter abgeschlossener Servertag) | Schluss > EMA50 der D1-Schlusskurse | Schluss < EMA50 |
| H4 (letzte abgeschlossene H4-Kerze) | EMA20 > EMA50 der H4-Schlusskurse | EMA20 < EMA50 |

Nur wenn beide Ebenen übereinstimmen, wird in diese Richtung gehandelt.

**Pullback und Einstieg auf H1 (Long, Short gespiegelt)**
- Signal, wenn C(i−1) < EMA20_H1(i−1) und C(i) > EMA20_H1(i) und der Trend aufwärts ist; Einstieg zur Eröffnung von i+1
- **Stop:** fest am tiefsten Tief der letzten 10 H1-Kerzen (i−9 … i) minus 0,5 × ATR14_H1(i), mindestens 1 × ATR14_H1(i) unter dem Einstieg
- **Ziel:** Einstieg + 2 × (Einstieg − Stop), Limit ohne Slippage
- **Zeitstopp:** Ausstieg zur Eröffnung nach 48 gehaltenen H1-Kerzen
- Stop und Ziel intrabar (Long: Bid-Tief/-Hoch; Short: Bid + Spread). Ein Gap wird zur Eröffnung gefüllt. Treffen beide in derselben Kerze, zählt der Stop.
- Je Instrument höchstens eine Position; ein neues Signal frühestens am Schluss der Kerze nach dem Ausstieg; keine neuen Einstiege an Servertagen 24.12.–01.01.
- **Größe:** Nominal = min(0,25 % Kapital / (R / Einstieg), 10 × Kapital)
- **Portfolio:** Summe aller Instrumente; Ergebnis am Servertag des Ausstiegs, Tage ohne Ausstieg zählen als 0

## 4. Akzeptanzkriterien

Wie Nr. 33–44 (alle müssen erfüllt sein): t ≥ **3,0** (kleinster aus iid, Woche, Monat) bei positivem Mittel; ≥ 6 von 9 Jahren positiv; ≥ 60 % der Instrumente positiv; doppelte Kosten > 0. Vor einem Hold-out gilt die Artefakt-Prüfung (Spielregel 6).

**Beschreibend:** Trades, Ø R vor und nach Kosten, Ziel-, Stop- und Zeitausstiege, Haltedauer, Ergebnis je Instrument und Anlageklasse.

**Hold-out und FTMO:** wie Nr. 16.

## 5. Umsetzbarkeit als MT5-EA

EMA- und ATR-Indikatoren auf D1, H4 und H1 aus Serverkerzen, Marktorder mit festem Stop und Limit-Ziel. Es werden keine externen Daten benötigt.

## 6. Trial-Log (Fortsetzung des globalen Logs)

| # | Test |
|---|---|
| T153 | J-MTF (Nr. 45), In-Sample |
| T154, T155 | Hold-out, FTMO (nur bei Bestehen) |
