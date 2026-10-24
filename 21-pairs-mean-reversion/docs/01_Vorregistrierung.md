# Vorregistrierung: Modell P „z-Score Mean Reversion AUDNZD / EURCHF“ (Strategie Nr. 21)

Festgelegt am 24.10.2026, **bevor** Code für dieses Modell geschrieben oder Daten dafür ausgewertet wurden. Änderungen nach diesem Commit zählen als neuer Versuch im Trial-Log (`../TRIAL_LOG.md`).

**Vorab festgehalten:** AUDNZD und EURCHF waren Teil der Trendfolge (Nr. 3, Sharpe des Portfolios −0,53) und der Portfolios von Nr. 6, 7 und 20. Eine z-Score-Regel wurde nie angewandt.

## 0. Feste Rahmenbedingungen (für alle Strategien gleich)

- Expert Advisor für MetaTrader 5, handelt vollständig autonom
- FTMO 2-Step, Swing, 100.000 USD
- Max. Verlust gesamt 10 %, max. Tagesverlust 5 %
- Ziel Phase 1 +10 %, Ziel Phase 2 +5 %
- News-Trading und Halten übers Wochenende erlaubt

## 1. Hypothese

Starke Abweichungen der Crosses AUDNZD bzw. EURCHF von ihrem 60-Tage-Mittel kehren zurück. Eine Gegenposition verdient nach Kosten mit t ≥ 3.

**Erwartung vor dem Test: Scheitern.**

## 2. Daten und Zeiträume

- HistData M5; Tagesbuchhaltung von Modell G über `run_weights` (Nr. 6): Signal 16:45, Ausführung und Bewertung 16:50 New York, FX-Kosten, Swaps (Zinsdifferenz − 1 %), 0,7-%-Gebühr
- **Warm-up:** 2014
- **In-Sample (IS):** Handelstage 2015–2023 (beginnt zwei Wochen vor dem SNB-Schock vom 15.01.2015, der damit enthalten ist)
- **Hold-out (HO):** ab 01.01.2024, einmalig und nur, wenn IS besteht

## 3. Regeln

**z-Score** je Handelstag aus den 16:45-Kursen p: `z = (ln p − Mittel der letzten 60 ln p) / Standardabweichung der letzten 60 ln p` (einschließlich heute).

**Varianten (je ein Trial), identische Regeln**

| Variante | Instrument |
|---|---|
| **P-AUDNZD** | AUDNZD |
| **P-EURCHF** | EURCHF |

**Position**
- Flat und z ≥ +2: Short
- Flat und z ≤ −2: Long
- Short und z ≤ 0: schließen
- Long und z ≥ 0: schließen

Größe beim Einstieg `10 % / σ` (EWMA wie Modell G), danach unverändert bis zum Ausstieg. Kein Stop, kein Zeitlimit. Nur an Tagen mit exakter 16:50-Kerze.

## 4. Akzeptanzkriterien

**In-Sample, je Variante** (alle müssen erfüllt sein)

| # | Kriterium |
|---|---|
| 1 | Mittleres Netto-Tagesergebnis > 0 mit t-Wert ≥ **3,0** (kleinster aus iid, Woche, Monat) |
| 2 | ≥ 6 von 9 Jahren positiv |
| 3 | Beide Teilzeiträume 2015–2019 und 2020–2023 mit positivem Netto-Mittel |
| 4 | Mittleres Ergebnis bei doppelten Kosten > 0 |

**Variantenwahl:** höherer t-Wert. Besteht keine, ist **Strategie Nr. 21 gescheitert**, und der Hold-out bleibt unberührt.

**Beschreibend:** Trades, Trefferquote, Ø Haltedauer, Zeit im Markt, Ergebnis ohne Januar 2015 (EURCHF), je Jahr.

**Hold-out und FTMO:** wie Nr. 14.

## 5. Umsetzbarkeit als MT5-EA

Täglicher z-Score aus den eigenen D1-Kursen, Marktorder um 16:50 New York. Es werden keine externen Daten benötigt.

## 6. Trial-Log (Fortsetzung des globalen Logs)

| # | Test |
|---|---|
| T72 | P-AUDNZD, In-Sample |
| T73 | P-EURCHF, In-Sample |
| T74 | Hold-out der gewählten Variante (nur falls T72 oder T73 besteht) |
| T75 | FTMO-Bootstrap (nur falls T74 besteht) |
