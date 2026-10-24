# Vorregistrierung: Modell E „Tagesmuster“ (Strategien Nr. 43 und 44)

Festgelegt am 24.10.2026, **bevor** Code für dieses Modell geschrieben oder Daten dafür ausgewertet wurden. Änderungen nach diesem Commit zählen als neuer Versuch im Trial-Log (`../TRIAL_LOG.md`).

**Vorab festgehalten:** D1-Serverkerzen derselben 17 Instrumente wurden in Nr. 33–35 ausgewertet, US500 in Nr. 15 (Connors-Reversal). Bewegungen über 2 ATR und Wochentage wurden nicht angesehen.

## 0. Feste Rahmenbedingungen (für alle Strategien gleich)

- Expert Advisor für MetaTrader 5, handelt vollständig autonom
- FTMO 2-Step, Swing, 100.000 USD
- Max. Verlust gesamt 10 %, max. Tagesverlust 5 %
- Ziel Phase 1 +10 %, Ziel Phase 2 +5 %
- News-Trading und Halten übers Wochenende erlaubt

## 1. Hypothesen

- **Nr. 43:** Nach einem Servertag mit |C − C_Vortag| > 2 × ATR14 verdient eine Position am Folgetag nach Kosten mit t ≥ 3, entweder gegen die Bewegung (E-REV) oder mit ihr (E-CONT).
- **Nr. 44:** Ein rollierend gewählter Wochentag je Instrument verdient nach Kosten mit t ≥ 3 (E-WD).

**Erwartung vor dem Test: Scheitern aller drei.**

## 2. Daten und Zeiträume

- **D1-Kerzen:** Servertage Mo–Fr (17:00–17:00 New York) aus HistData M5 wie in Nr. 33–35 (`dbo.model.server_days`, mindestens 12 M5-Kerzen). Daten ab 2014.
- **Universum (17):** wie Nr. 33–38
- **Kosten:** Spread (Kauf und Short-Schluss zum Ask), Kommission, Slippage je Marktausführung (FX 0,1 Pip, CFD ¼ Spread). Keine Swaps, weil die Position innerhalb des Servertags vor dem Rollover gehalten wird.
- Kein Handel an Servertagen 24.12.–01.01.
- **In-Sample:** 2015–2023. **Hold-out:** ab 2024, einmalig je bestandener Variante.

## 3. Regeln

**Gemeinsam (je Instrument und Servertag i)**
- **Position:** Marktorder zur Eröffnung der ersten M5-Kerze des Servertags i, Schluss zum Schluss der letzten M5-Kerze desselben Servertags. Kein Stop.
- **Größe:** Nominal = min(0,5 % Kapital / (ATR14(i−1) / Kurs), 10 × Kapital). ATR14 nach Wilder aus den D1-Kerzen bis i−1. Eine Bewegung von einer ATR kostet bzw. bringt also etwa 0,5 %.
- **Portfolio:** Summe aller Instrumente je Tag. Tage ohne Position zählen als 0.

| Variante | Listen-Nr. | Signal für Tag i | Richtung |
|---|---|---|---|
| **E-REV** | 43 | \|C(i−1) − C(i−2)\| > 2 × ATR14(i−2) | −sign(C(i−1) − C(i−2)) |
| **E-CONT** | 43 | wie E-REV | +sign(C(i−1) − C(i−2)) |
| **E-WD** | 44 | Wochentag w(i) = gewählter Wochentag des Instruments im Jahr von i | sign(Mittel) |

**Wahl bei E-WD (ohne Blick in die Zukunft):**
- Für jedes Jahr Y und Instrument werden aus allen Servertagen von 2014 bis Y−1 je Wochentag Mittel und t-Wert der Tagesrendite (Eröffnung → Schluss, relativ) berechnet.
- Gewählt wird der Wochentag mit dem größten |t|. Gehandelt wird nur bei |t| ≥ 2,0, in Richtung des Vorzeichens.
- Die Wahl gilt für alle Tage des Jahres Y.

## 4. Akzeptanzkriterien

Wie Nr. 33–42 (alle müssen erfüllt sein): t ≥ **3,0** (kleinster aus iid, Woche, Monat) bei positivem Mittel; ≥ 6 von 9 Jahren positiv; ≥ 60 % der Instrumente positiv; doppelte Kosten > 0. **Jede Variante wird für sich bewertet.** Vor einem Hold-out gilt die Artefakt-Prüfung (Spielregel 6).

**Beschreibend:**
- Anzahl der Signale, Ø Ergebnis je Trade in ATR vor und nach Kosten
- je Instrument; bei E-WD die gewählten Wochentage je Jahr

**Hold-out und FTMO:** wie Nr. 16, je bestandener Variante.

## 5. Umsetzbarkeit als MT5-EA

D1-Serverkerzen, eine Marktorder zu Tagesbeginn und Schließen vor dem Rollover. Die Wochentags-Tabelle für E-WD wird jährlich aus der Historie berechnet. Es werden keine externen Daten benötigt.

## 6. Trial-Log (Fortsetzung des globalen Logs)

| # | Test |
|---|---|
| T144 | E-REV (Nr. 43), In-Sample |
| T145 | E-CONT (Nr. 43), In-Sample |
| T146 | E-WD (Nr. 44), In-Sample |
| T147–T152 | Hold-out und FTMO je bestandener Variante |
