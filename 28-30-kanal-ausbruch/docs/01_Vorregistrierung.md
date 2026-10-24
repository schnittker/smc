# Vorregistrierung: Modell B „Kanal-Ausbruch“ (Strategien Nr. 28 und Nr. 30)

Festgelegt am 24.10.2026, **bevor** Code für dieses Modell geschrieben oder Daten dafür ausgewertet wurden. Änderungen nach diesem Commit zählen als neuer Versuch im Trial-Log (`../TRIAL_LOG.md`).

**Vorab festgehalten:** Dasselbe Universum wurde mit Zeitreihen-Momentum in Nr. 3 und Nr. 4 ausgewertet (beide negativ).

## 0. Feste Rahmenbedingungen (für alle Strategien gleich)

- Expert Advisor für MetaTrader 5, handelt vollständig autonom
- FTMO 2-Step, Swing, 100.000 USD
- Max. Verlust gesamt 10 %, max. Tagesverlust 5 %
- Ziel Phase 1 +10 %, Ziel Phase 2 +5 %
- News-Trading und Halten übers Wochenende erlaubt

## 1. Hypothese

Kanal-Ausbrüche über ein diversifiziertes Universum verdienen nach Kosten mit t ≥ 3.

**Erwartung vor dem Test: Scheitern.**

## 2. Daten und Zeiträume

- **Universum** (34 Instrumente):
  - 24 FX-Paare und XAUUSD mit FX-Kostenmodell (Modell G, Bewertung 16:50 New York)
  - 9 CFDs mit Kostenmodell H (Bewertung zur Kassazeit): US500, US100, FRA40, UK100, JP225, HK50, AUS200, Brent, Silber
  - DAX, Euro Stoxx 50 und WTI wie in Nr. 4 ausgeschlossen (fehlerhafte Daten)
- Tagesbuchhaltung über `run_weights` (Nr. 6), Swaps und Gebühren wie in Nr. 3 und Nr. 4
- **Warm-up:** 2014 (der 252-Tage-Kanal beginnt Anfang 2015 zu wirken)
- **In-Sample:** Handelstage 2015–2023. **Hold-out:** ab 2024, einmalig und nur, wenn IS besteht.

## 3. Regeln

Je Instrument aus den täglichen Signalkursen C (Modell G/H: 5 Minuten vor der Bewertung), nur an Tagen mit exakter Bewertungskerze:

| Variante | Listen-Nr. | Einstieg Long / Short | Ausstieg Long / Short |
|---|---|---|---|
| **B-52W** | 28 | C > Max(C der letzten 252 Tage) / C < Min(252) | C < Min(C der letzten 126 Tage) / C > Max(126) |
| **B-TURTLE** | 30 | C > Max(55) / C < Min(55) | C < Min(20) / C > Max(20) |

- Kanäle ohne den heutigen Tag
- Nach dem Ausstieg flat bis zum nächsten Einstieg. Ein Gegeneinstieg am Ausstiegstag ist möglich, wenn dessen Bedingung erfüllt ist.
- **Größe:** `10 % / σ` beim Einstieg (EWMA wie Modell G), danach unverändert bis zum Ausstieg
- **Portfolio:** Summe über alle Instrumente

## 4. Akzeptanzkriterien

Wie Nr. 3 (alle müssen erfüllt sein): t ≥ **3,0** (kleinster aus iid, Woche, Monat) bei positivem Mittel; ≥ 6 von 9 Jahren positiv; ≥ 60 % der Instrumente (≥ 250 Positionstage) positiv; doppelte Kosten > 0.

**Jede Variante wird für sich bewertet** (eigene Listennummer). Besteht eine, wird ihr Hold-out einzeln ausgewertet.

**Beschreibend:** Zerlegung in Kurs, Swaps und Kosten; Ergebnis je Anlageklasse (FX, Metalle, Indizes, Öl); je Jahr.

**Hold-out und FTMO:** wie Nr. 3.

## 5. Umsetzbarkeit als MT5-EA

Kanäle aus den eigenen D1-Kursen, eine Order je Ausbruch. Es werden keine externen Daten benötigt.

## 6. Trial-Log (Fortsetzung des globalen Logs)

| # | Test |
|---|---|
| T96 | B-52W (Nr. 28), In-Sample |
| T97 | B-TURTLE (Nr. 30), In-Sample |
| T98, T99 | Hold-out je bestandener Variante |
| T100, T101 | FTMO-Bootstrap je bestandenem Hold-out |
