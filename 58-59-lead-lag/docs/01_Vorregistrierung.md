# Vorregistrierung: Modell LL „Lead-Lag“ (Strategien Nr. 58 und 59)

Festgelegt am 24.10.2026, **bevor** Code für dieses Modell geschrieben oder Daten dafür ausgewertet wurden. Die DGS10-Datei wurde heruntergeladen, aber nur auf Format und Länge geprüft (erste und letzte Zeilen). Änderungen nach diesem Commit zählen als neuer Versuch im Trial-Log (`../TRIAL_LOG.md`).

**Vorab festgehalten:** AUDJPY (H1) wurde in Nr. 37/39 und 46 verwendet, USDJPY in vielen FX-Tests. US500 H1 kam in Nr. 11/12 vor. Querbezüge zwischen diesen Märkten wurden nicht ausgewertet.

## 0. Feste Rahmenbedingungen (für alle Strategien gleich)

- Expert Advisor für MetaTrader 5, handelt vollständig autonom
- FTMO 2-Step, Swing, 100.000 USD
- Max. Verlust gesamt 10 %, max. Tagesverlust 5 %
- Ziel Phase 1 +10 %, Ziel Phase 2 +5 %
- News-Trading und Halten übers Wochenende erlaubt

## 1. Hypothesen

- **Nr. 58 (LL-AJ):** Nach einer starken US500-H1-Bewegung zieht AUDJPY in den folgenden 3 Stunden nach, und zwar so stark, dass es nach Kosten mit t ≥ 3 verdient.
- **Nr. 59:** USDJPY folgt der Änderung der 10-jährigen US-Rendite des Vortags (LL-Y1) bzw. deren 20-Tage-Trend (LL-Y20) nach Kosten mit t ≥ 3.

**Erwartung vor dem Test: Scheitern aller drei.**

## 2. Daten, Kosten, Zeiträume

- **LL-AJ:** H1-Serverkerzen von AUDJPY (gehandelt) und US500 (Signal), zeitgleich über die UTC-Öffnungszeit verbunden. FX-Kostenmodell und Swaps; Engine `chart.engine` (Einstieg zur nächsten Eröffnung, fester Stop, Zeitausstieg).
- **LL-Y1, LL-Y20:** USDJPY-Tagesbuchhaltung wie Nr. 6/20 (`carry.model.run_weights`). Die Position wird zur Marke 16:50 New York gesetzt; Kosten nach FX-Modell, Swaps mit 1 % Aufschlag. DGS10 von FRED.
- **In-Sample:** 2015–2023, Kurse nur bis 31.12.2023. **Hold-out:** ab 2024, einmalig je bestandener Variante.

## 3. Regeln

**LL-AJ (Nr. 58)**
- r(i) = ln C_US500(i) − ln C_US500(i−1) der H1-Kerze i
- σ(i) = Standardabweichung von r über die 500 Kerzen bis i
- Ist z = r(i) / σ(i) > 1,5, wird AUDJPY zur Eröffnung von i+1 gekauft; bei z < −1,5 verkauft. Voraussetzung: Beide Kerzen i existieren.
- **Ausstieg** zur Eröffnung nach 3 gehaltenen Kerzen. **Stop** fest 2 × ATR14_H1(AUDJPY), intrabar. Kein Ziel.
- Je Position höchstens eine; ein neues Signal frühestens am Schluss der Kerze nach dem Ausstieg; keine Einstiege 24.12.–01.01.
- **Größe:** Nominal = min(0,25 % / (2 ATR14 / Kurs), 10) × Kapital

**LL-Y1 / LL-Y20 (Nr. 59, je Servertag d, Marke 16:50 New York)**
- y(x) = DGS10 zum Kalendertag x; fehlende Werte (Feiertage) werden mit dem letzten verfügbaren Wert gefüllt.
- **LL-Y1:** Signal = sign(y(d−1) − y(d−2)), wobei d−1 und d−2 die beiden letzten DGS10-Beobachtungen vor dem Kalendertag d sind
- **LL-Y20:** Signal = sign(y(d−1) − y(d−21)) über die letzten 21 DGS10-Beobachtungen vor d
- Signal > 0 → Long USDJPY, < 0 → Short, = 0 → flat
- **Größe:** 10 % / σ (EWMA wie Modell G), festgelegt bei jeder Änderung des Vorzeichens. Bei LL-Y1 wird täglich neu festgelegt, auch wenn das Vorzeichen gleich bleibt.

## 4. Akzeptanzkriterien

Alle müssen erfüllt sein: t ≥ **3,0** (kleinster aus iid, Woche, Monat) bei positivem Mittel; ≥ 6 von 9 Jahren positiv; beide Teilzeiträume 2015–2019 und 2020–2023 positiv (Einzelinstrument statt Instrumente-Regel); doppelte Kosten > 0. Jede Variante wird für sich bewertet. Vor einem Hold-out gilt die Artefakt-Prüfung (Spielregel 6).

**Beschreibend:**
- LL-AJ: Ø R vor und nach Kosten; Regression der AUDJPY-Rendite der Folgestunden auf z
- LL-Y1/LL-Y20: gleichzeitige und verzögerte Korrelation der Tagesrenditen USDJPY ↔ ΔDGS10

**Hold-out und FTMO:** wie Nr. 16.

## 5. Umsetzbarkeit als MT5-EA

- **LL-AJ:** Der EA liest die H1-Kurse von US500.cash und handelt AUDJPY. Es werden keine externen Daten benötigt.
- **LL-Y1/LL-Y20:** Die tägliche US-Rendite muss per WebRequest kommen, z. B. von Treasury oder FRED (⚠).

## 6. Trial-Log (Fortsetzung des globalen Logs)

| # | Test |
|---|---|
| T210 | LL-AJ (Nr. 58), In-Sample |
| T211 | LL-Y1 (Nr. 59), In-Sample |
| T212 | LL-Y20 (Nr. 59), In-Sample |
| T213–T218 | Hold-out und FTMO je bestandener Variante |
