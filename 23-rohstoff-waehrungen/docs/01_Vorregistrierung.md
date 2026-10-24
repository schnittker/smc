# Vorregistrierung: Modell R „Rohstoff-Lead-Lag“ (Strategie Nr. 23)

Festgelegt am 24.10.2026, **bevor** Code für dieses Modell geschrieben oder Daten dafür ausgewertet wurden. Änderungen nach diesem Commit zählen als neuer Versuch im Trial-Log (`../TRIAL_LOG.md`).

## 0. Feste Rahmenbedingungen (für alle Strategien gleich)

- Expert Advisor für MetaTrader 5, handelt vollständig autonom
- FTMO 2-Step, Swing, 100.000 USD
- Max. Verlust gesamt 10 %, max. Tagesverlust 5 %
- Ziel Phase 1 +10 %, Ziel Phase 2 +5 %
- News-Trading und Halten übers Wochenende erlaubt

## 1. Hypothese

Die Tagesrendite des Rohstoffs (bis 15:45 New York) sagt die Richtung der Rohstoffwährung über den folgenden Tag (16:50 bis 16:50 New York) voraus.

**Erwartung vor dem Test: Scheitern** (Literatur: nur gleichzeitiger Zusammenhang).

## 2. Daten und Zeiträume

- Signal: Brent (BCOUSD → UKOIL.cash) bzw. Gold (XAUUSD), 15:45-Kurse nach Modell H (WTI ist bei HistData 2024–2026 lückenhaft)
- Handel: USDCAD bzw. AUDUSD, Tagesbuchhaltung von Modell G über `run_weights` (Nr. 6), Bewertung 16:50 New York, FX-Kosten, Swaps, 0,7-%-Gebühr
- **Warm-up:** 2014. **In-Sample:** Handelstage 2015–2023. **Hold-out:** ab 2024, einmalig und nur, wenn IS besteht.

## 3. Regeln

`r = ln(Rohstoff 15:45 heute / Rohstoff 15:45 am letzten Tag mit Kurs)`, nur wenn der Rohstoff heute einen Kurs hat.

| Variante | Signal | Position ab 16:50 heute (bis zum nächsten Signal) |
|---|---|---|
| **R-OEL** | Brent | r > 0: Long CAD (Short USDCAD), r < 0: Short CAD (Long USDCAD) |
| **R-GOLD** | Gold | r > 0: Long AUDUSD, r < 0: Short AUDUSD |

- Größe `10 % / σ` (EWMA wie Modell G), täglich auf den aktuellen Wert gesetzt
- Ohne Rohstoffkurs oder bei r = 0 bleibt die Position stehen
- Nur an Tagen mit exakter 16:50-Kerze des FX-Paars

## 4. Akzeptanzkriterien

Wie Nr. 14 (alle müssen erfüllt sein): t ≥ **3,0** (kleinster aus iid, Woche, Monat) bei positivem Mittel; ≥ 6 von 9 Jahren positiv; beide Teilzeiträume 2015–2019 und 2020–2023 positiv; doppelte Kosten > 0. Variantenwahl über den t-Wert. Besteht keine, ist **Strategie Nr. 23 gescheitert**, und der Hold-out bleibt unberührt.

**Beschreibend:** gleichzeitige Korrelation (Rohstoff 15:45→15:45 gegen FX am selben Tag) zur Einordnung; Kursergebnis vor Kosten; Umschlag.

**Hold-out und FTMO:** wie Nr. 14.

## 5. Umsetzbarkeit als MT5-EA

UKOIL.cash bzw. XAUUSD als Signal, USDCAD bzw. AUDUSD als Handelsinstrument, täglich um 16:50 New York. Es werden keine externen Daten benötigt.

## 6. Trial-Log (Fortsetzung des globalen Logs)

| # | Test |
|---|---|
| T80 | R-OEL, In-Sample |
| T81 | R-GOLD, In-Sample |
| T82 | Hold-out der gewählten Variante (nur falls T80 oder T81 besteht) |
| T83 | FTMO-Bootstrap (nur falls T82 besteht) |
