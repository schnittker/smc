# Vorregistrierung: Modell SR „S/R-Zonen und Trendlinien“ (Strategien Nr. 50 und 51)

Festgelegt am 24.10.2026, **bevor** Code für dieses Modell geschrieben oder Daten dafür ausgewertet wurden. Änderungen nach diesem Commit zählen als neuer Versuch im Trial-Log (`../TRIAL_LOG.md`).

**Vorab festgehalten:** H4-Daten der 17 Instrumente wurden für Kanal-Ausbrüche (Nr. 36, 38), Hurst (Nr. 40) und Pullbacks (Nr. 45, H1) ausgewertet. Pivot-Level wurden in Nr. 49 getestet, Swing-basierte Zonen und Trendlinien nicht.

## 0. Feste Rahmenbedingungen (für alle Strategien gleich)

- Expert Advisor für MetaTrader 5, handelt vollständig autonom
- FTMO 2-Step, Swing, 100.000 USD
- Max. Verlust gesamt 10 %, max. Tagesverlust 5 %
- Ziel Phase 1 +10 %, Ziel Phase 2 +5 %
- News-Trading und Halten übers Wochenende erlaubt

## 1. Hypothesen

- **Nr. 50:** Abpraller an (SR-BOUNCE) bzw. Ausbrüche aus (SR-BREAK) algorithmischen S/R-Zonen verdienen nach Kosten mit t ≥ 3.
- **Nr. 51:** Trendlinien-Ausbrüche (SR-TLINE) verdienen nach Kosten mit t ≥ 3.

**Erwartung vor dem Test: Scheitern aller drei.**

## 2. Daten, Universum, Kosten, Zeiträume

Wie Nr. 36/38:
- H4-Serverkerzen der 17 Instrumente
- Kosten: Spread, Kommission, Slippage und Swaps
- In-Sample: Einstiege 2015–2023, Kurse bis 31.12.2023
- Hold-out: ab 2024, einmalig je bestandener Variante

## 3. Regeln (je Instrument; Signal am Schluss der H4-Kerze i, Einstieg zur Eröffnung von i+1)

**Swing-Punkte**
- Kerze j ist ein Swing-Hoch, wenn H(j) > max H(j−3 … j−1) und H(j) ≥ max H(j+1 … j+3). Swing-Tief gespiegelt.
- Bekannt ist der Swing erst am Schluss von j+3.
- Verwendet werden nur Swings, die bis zum Schluss von i bestätigt sind und deren Kerze j ≥ i−120 liegt.

**Zonen (Nr. 50)**
- Ein Swing-Level L ist eine Zone, wenn mindestens ein weiterer bestätigter Swing (Hoch oder Tief) im Fenster innerhalb ±0,25 × ATR14(i) von L liegt.
- **Unterstützung:** die höchste Zone unter C(i). **Widerstand:** die niedrigste Zone über C(i).

| Variante | Long | Short | Stop |
|---|---|---|---|
| **SR-BOUNCE** | L(i) ≤ Unterstützung + 0,25 ATR und C(i) > Unterstützung + 0,25 ATR | H(i) ≥ Widerstand − 0,25 ATR und C(i) < Widerstand − 0,25 ATR | Zone ∓ 1 × ATR14(i) |
| **SR-BREAK** | C(i) > Z + 0,25 ATR und C(i−1) ≤ Z + 0,25 ATR, mit Z = höchste Zone ≤ C(i−1) + 0,25 ATR … C(i), d. h. eine Zone wird von unten durchbrochen | gespiegelt | Z ∓ 1 × ATR14(i) |

Bei SR-BREAK wird jede Zone mit Z zwischen C(i−1) − 0,25 ATR und C(i) − 0,25 ATR geprüft (Long); maßgeblich ist die oberste durchbrochene.

**Trendlinie (Nr. 51, SR-TLINE)**
- **Fallende Linie:** durch die letzten zwei bestätigten Swing-Hochs j1 < j2 mit H(j2) < H(j1), Wert bei i: H(j2) + (H(j2) − H(j1)) / (j2 − j1) × (i − j2)
- **Long:** C(i) > Linie(i) und C(i−1) ≤ Linie(i−1)
- **Stop:** letztes bestätigtes Swing-Tief − 0,5 × ATR14(i)
- **Short:** gespiegelt mit steigender Linie durch zwei Swing-Tiefs

**Gemeinsam**
- Stop-Abstand mindestens 1 × ATR14(i) vom Einstieg; liegt der Stop nach dem Einstieg auf der falschen Seite, gibt es keinen Trade.
- **Ziel:** 2R als Limit. **Zeitstopp:** Eröffnung nach 30 gehaltenen H4-Kerzen.
- Stop und Ziel intrabar (Long: Bid; Short: Bid + Spread). Ein Gap wird zur Eröffnung gefüllt; Stop und Ziel in derselben Kerze zählen als Stop; im Einstiegsbar zählt nur der Stop.
- Je Instrument höchstens eine Position; ein neues Signal frühestens am Schluss der Kerze nach dem Ausstieg; keine neuen Einstiege an Servertagen 24.12.–01.01.
- **Größe:** Nominal = min(0,25 % Kapital / (R / Einstieg), 10 × Kapital)
- **Portfolio:** Summe aller Instrumente; Ergebnis am Servertag des Ausstiegs, Tage ohne Ausstieg zählen als 0

## 4. Akzeptanzkriterien

Wie Nr. 33–49 (alle müssen erfüllt sein): t ≥ **3,0** (kleinster aus iid, Woche, Monat) bei positivem Mittel; ≥ 6 von 9 Jahren positiv; ≥ 60 % der Instrumente positiv; doppelte Kosten > 0. Jede Variante wird für sich bewertet. Vor einem Hold-out gilt die Artefakt-Prüfung (Spielregel 6).

**Beschreibend:** Trades, Ø R vor und nach Kosten, Ziel-, Stop- und Zeitausstiege, Ergebnis je Instrument und Anlageklasse.

**Hold-out und FTMO:** wie Nr. 16.

## 5. Umsetzbarkeit als MT5-EA

Swing-Erkennung, Zonen und Linien aus H4-Serverkerzen; Marktorder mit festem Stop und Limit-Ziel. Es werden keine externen Daten benötigt.

## 6. Trial-Log (Fortsetzung des globalen Logs)

| # | Test |
|---|---|
| T174 | SR-BOUNCE (Nr. 50), In-Sample |
| T175 | SR-BREAK (Nr. 50), In-Sample |
| T176 | SR-TLINE (Nr. 51), In-Sample |
| T177–T182 | Hold-out und FTMO je bestandener Variante |
