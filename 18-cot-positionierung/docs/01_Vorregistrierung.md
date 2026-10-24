# Vorregistrierung: Modell C „COT-Extreme“ (Strategie Nr. 18)

Festgelegt am 24.10.2026, **bevor** Code für dieses Modell geschrieben oder Daten dafür ausgewertet wurden. Vorher geprüft wurde nur, dass die CFTC-Jahresdateien 2011–2026 die 8 Kontrakte vollständig enthalten (Codes unten). Änderungen nach diesem Commit zählen als neuer Versuch im Trial-Log (`../TRIAL_LOG.md`).

## 0. Feste Rahmenbedingungen (für alle Strategien gleich)

- Expert Advisor für MetaTrader 5, handelt vollständig autonom
- FTMO 2-Step, Swing, 100.000 USD
- Max. Verlust gesamt 10 %, max. Tagesverlust 5 %
- Ziel Phase 1 +10 %, Ziel Phase 2 +5 %
- News-Trading und Halten übers Wochenende erlaubt

## 1. Hypothese

Extreme der Netto-Position der Spekulanten in Währungs- und Goldfutures sagen die Kursrichtung der folgenden Wochen voraus: Umkehr (C-KONTRA, Praktiker) oder Fortsetzung (C-FOLGE, Tornell & Yuan 2012). Eine der beiden Richtungen verdient nach Kosten mit t ≥ 3.

**Erwartung vor dem Test: Scheitern beider Varianten.**

## 2. Daten und Zeiträume

- **COT:** CFTC Legacy Futures-only, Jahresdateien `deacot<Jahr>.zip` (https://www.cftc.gov/files/dea/history/), Abruf 24.10.2026. Spalten: „Noncommercial Positions-Long (All)“ minus „Noncommercial Positions-Short (All)“ = Netto-Position N.

| Kontrakt (CFTC-Code) | FTMO-Instrument | Long Fremdwährung/Gold = |
|---|---|---|
| Euro FX (099741) | EURUSD | Long EURUSD |
| British Pound (096742) | GBPUSD | Long GBPUSD |
| Japanese Yen (097741) | USDJPY | Short USDJPY |
| Australian Dollar (232741) | AUDUSD | Long AUDUSD |
| Canadian Dollar (090741) | USDCAD | Short USDCAD |
| Swiss Franc (092741) | USDCHF | Short USDCHF |
| NZ Dollar (112741) | NZDUSD | Long NZDUSD |
| Gold (088691) | XAUUSD | Long XAUUSD |

- **Kurse:** HistData M5; Tagesbuchhaltung von Modell G (16:50 New York) über `run_weights` aus Nr. 6, mit FX-Kosten, Swaps (Zinsdifferenz − 1 % Aufschlag, Gold Zins 0) und 0,7-%-Gebühr
- **Warm-up:** 2012–2014 (156 Wochen COT-Historie)
- **In-Sample (IS):** Handelstage 2015–2023
- **Hold-out (HO):** ab 01.01.2024, einmalig und nur, wenn IS besteht

## 3. Regeln

**COT-Index** je Kontrakt und Berichtstag (Dienstag): `I = (N − min N) / (max N − min N)` über die letzten 156 Berichte einschließlich des aktuellen. Ist max = min, gilt I = 0,5.

**Signal je Bericht**
- I ≥ 0,9: Spekulanten extrem long
- I ≤ 0,1: Spekulanten extrem short
- sonst: neutral

**Varianten (je ein Trial), gleiches Signal, entgegengesetzte Richtung**

| Variante | extrem long | extrem short | neutral |
|---|---|---|---|
| **C-KONTRA** | Short Fremdwährung/Gold | Long | flat |
| **C-FOLGE** | Long Fremdwährung/Gold | Short | flat |

**Ausführung:** am Montag nach dem Berichtstag (Berichtstag + 6 Kalendertage) um 16:50 New York, nach der Freitags-Veröffentlichung auch bei Feiertagsverschiebungen. Fehlt die exakte 16:50-Kerze, wird am nächsten Tag mit Kerze gehandelt.

**Sonderregel Shutdown:** Berichte mit Stand 24.12.2018 bis 04.03.2019 erschienen wegen des US-Regierungsstillstands mit Wochen Verspätung. Sie werden ignoriert, und die Positionen bleiben unverändert.

**Größe:** Nominalwert je Instrument `|w| = 10 % / σ`, σ = EWMA-Volatilität der Tagesrenditen (16:50), Schwerpunkt 60 Tage, Untergrenze 4 % p. a. (wie Modell G). Wird nur bei einem neuen Signal angepasst.

## 4. Akzeptanzkriterien

**In-Sample, je Variante** (alle müssen erfüllt sein)

| # | Kriterium |
|---|---|
| 1 | Mittleres Netto-Tagesergebnis > 0 mit t-Wert ≥ **3,0** (kleinster aus iid, Woche, Monat) |
| 2 | ≥ 6 von 9 Jahren positiv |
| 3 | ≥ 60 % der Instrumente mit ≥ 250 Positionstagen mit positivem Netto-Beitrag |
| 4 | Mittleres Ergebnis bei doppelten Kosten > 0 (Handel, Gebühr, belastende Swaps) |

**Variantenwahl:** höherer t-Wert, falls beide bestehen. Besteht keine, ist **Strategie Nr. 18 gescheitert**, und der Hold-out bleibt unberührt.

**Beschreibend, ohne Einfluss auf die Entscheidung:** Zeit im Markt, Ergebnis je Instrument, Ergebnis nach Signaltyp (extrem long / extrem short), Zerlegung in Kurs, Swaps und Kosten, Ergebnis je Jahr.

**Hold-out und FTMO:** wie Strategie Nr. 6.

## 5. Umsetzbarkeit als MT5-EA

⚠ Die COT-Daten muss der EA wöchentlich per `WebRequest` von der CFTC laden (öffentliche Socrata-API). Das ist eine externe Abhängigkeit. Alles Weitere (Index, Größe, Orders) rechnet er selbst.

## 6. Trial-Log (Fortsetzung des globalen Logs)

| # | Test |
|---|---|
| T60 | C-KONTRA, In-Sample |
| T61 | C-FOLGE, In-Sample |
| T62 | Hold-out der gewählten Variante (nur falls T60 oder T61 besteht) |
| T63 | FTMO-Bootstrap (nur falls T62 besteht) |
