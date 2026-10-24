# Vorregistrierung: Modell OS „Oszillatoren, Divergenzen, Renko“ (Strategien Nr. 65–68, 74, 75)

Festgelegt am 24.10.2026, **bevor** Code für dieses Modell geschrieben oder Daten dafür ausgewertet wurden. Änderungen nach diesem Commit zählen als neuer Versuch im Trial-Log (`../TRIAL_LOG.md`).

**Vorab festgehalten:** H1- und H4-Daten der 17 Instrumente wurden mit vielen Trend- und Umkehrregeln ausgewertet, u. a. RSI2 in Nr. 15 (US500, D1). RSI14, Stochastik, Williams %R, CCI, Divergenzen und Renko wurden nicht angesehen.

## 0. Feste Rahmenbedingungen (für alle Strategien gleich)

- Expert Advisor für MetaTrader 5, handelt vollständig autonom
- FTMO 2-Step, Swing, 100.000 USD
- Max. Verlust gesamt 10 %, max. Tagesverlust 5 %
- Ziel Phase 1 +10 %, Ziel Phase 2 +5 %
- News-Trading und Halten übers Wochenende erlaubt

## 1. Hypothese

Jede der sechs Regeln verdient nach Kosten mit t ≥ 3. **Erwartung vor dem Test: Scheitern aller sechs.**

## 2. Daten, Universum, Kosten, Zeiträume

Wie Nr. 61–76:
- **Universum:** 17 Instrumente
- **Kerzen:** H1- bzw. H4-Serverkerzen
- **Kosten:** Spread, Kommission, Slippage und Swaps
- **In-Sample:** Einstiege 2015–2023, Kurse bis 31.12.2023
- **Hold-out:** ab 2024, einmalig je bestandener Variante

## 3. Regeln (Signal am Schluss der Kerze i, Einstieg zur Eröffnung von i+1)

**Indikatoren**
- **RSI14:** Wilder
- **Stochastik:** schnelles %K = 100 (C − LL14)/(HH14 − LL14); langsames %K = SMA3 davon; %D = SMA3 des langsamen %K
- **Williams %R14** = −100 (HH14 − C)/(HH14 − LL14)
- **CCI20** = (TP − SMA20(TP)) / (0,015 × mittlere absolute Abweichung von TP über 20), TP = (H + L + C)/3

**Umkehr- und Momentum-Regeln (Engine mit Ausstiegssignal, festem Stop 2 × ATR14(i) intrabar und Zeitstopp)**

| Variante | Nr. | TF | Long-Einstieg | Short-Einstieg | Ausstieg Long / Short (nächste Eröffnung) | Zeitstopp |
|---|---|---|---|---|---|---|
| **OS-RSI** | 65 | H1 | RSI(i−1) < 30 ≤ RSI(i) | RSI(i−1) > 70 ≥ RSI(i) | RSI ≥ 50 / RSI ≤ 50 | 48 |
| **OS-STOCH** | 66 | H1 | %K kreuzt %D von unten (K(i−1) ≤ D(i−1), K(i) > D(i)), K(i) < 20, D(i) < 20 | gespiegelt über 80 | %K ≥ 50 / %K ≤ 50 | 48 |
| **OS-WPR** | 67 | H1 | %R(i−1) < −80 ≤ %R(i) | %R(i−1) > −20 ≥ %R(i) | %R ≥ −50 / %R ≤ −50 | 48 |
| **OS-CCI** | 68 | H4 | CCI(i−1) ≤ 100 < CCI(i) | CCI(i−1) ≥ −100 > CCI(i) | CCI < 0 / CCI > 0 | 30 |

**OS-DIV (Nr. 75, H4, Engine wie Nr. 50/51 mit Ziel 2R)**
- **Swings** 3/3 (`chart.swings`)
- **Bullische Divergenz:** die letzten zwei bestätigten Swing-Tiefs j1 < j2 mit 5 ≤ j2 − j1 ≤ 60, L(j2) < L(j1), RSI(j2) > RSI(j1) und RSI(j1) < 30
- **Signal** am Bestätigungsbar i = j2 + 3. **Stop:** L(j2) − 0,25 ATR14(i), mindestens 1 ATR. **Ziel:** 2R. **Zeitstopp:** 30 Kerzen.
- **Bärisch** gespiegelt (Swing-Hochs, RSI(j1) > 70)

**OS-RENKO (Nr. 74, H1, Stop-and-Reverse-Engine wie Nr. 61–76)**
- Ziegel auf H1-Schlusskursen. Die Ziegelgröße ist 2 × ATR14_H1, festgelegt beim Entstehen des jeweils letzten Ziegels.
- Ein neuer Ziegel in Richtung des letzten entsteht, wenn der Schluss den letzten Ziegel um eine Ziegelgröße übersteigt. Eine Umkehr entsteht, wenn der Schluss um zwei Ziegelgrößen gegen den letzten Ziegel läuft.
- **Zustand** = Richtung des letzten Ziegels. Bei einem Wechsel folgt Stop-and-Reverse zur nächsten Eröffnung mit Notfall-Stop 3 × ATR14 und 0,25 % Risiko am Notfall-Stop.
- Ziegel entstehen nur auf Schlusskursen abgeschlossener Kerzen, also ohne die übliche Renko-Backtest-Falle der Zukunftsinformation. Abweichung von der Listenangabe „M1-basiert“: H1-Schlusskurse.

**Gemeinsam**
- Je Instrument höchstens eine Position; ein neues Signal frühestens am Schluss der Kerze nach dem Ausstieg (bei OS-RENKO Stop-and-Reverse)
- Keine neuen Einstiege an Servertagen 24.12.–01.01.
- **Größe:** Nominal = min(0,25 % Kapital / (R / Einstieg), 10 × Kapital), R = Stop-Abstand
- **Portfolio:** Summe aller Instrumente; Ergebnis am Servertag des Ausstiegs, Tage ohne Ausstieg zählen als 0

## 4. Akzeptanzkriterien

Wie Nr. 33–76 (alle müssen erfüllt sein): t ≥ **3,0** (kleinster aus iid, Woche, Monat) bei positivem Mittel; ≥ 6 von 9 Jahren positiv; ≥ 60 % der Instrumente positiv; doppelte Kosten > 0. Jede Variante wird für sich bewertet. Vor einem Hold-out gilt die Artefakt-Prüfung (Spielregel 6).

**Hold-out und FTMO:** wie Nr. 16.

## 5. Umsetzbarkeit als MT5-EA

Alle Indikatoren sind Standard in MT5. Renko wird im EA aus H1-Schlusskursen gebaut. Gehandelt wird mit Marktorders und festem Stop. Es werden keine externen Daten benötigt.

## 6. Trial-Log (Fortsetzung des globalen Logs)

| # | Test |
|---|---|
| T249 | OS-RSI (Nr. 65), In-Sample |
| T250 | OS-STOCH (Nr. 66), In-Sample |
| T251 | OS-WPR (Nr. 67), In-Sample |
| T252 | OS-CCI (Nr. 68), In-Sample |
| T253 | OS-RENKO (Nr. 74), In-Sample |
| T254 | OS-DIV (Nr. 75), In-Sample |
| T255–T266 | Hold-out und FTMO je bestandener Variante |
