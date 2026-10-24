# Vorregistrierung: Modell X „VIX-Regime“ (Strategie Nr. 19)

Festgelegt am 24.10.2026, **bevor** Code für dieses Modell geschrieben oder Daten dafür ausgewertet wurden. Vorher geprüft wurde nur die Abdeckung der Cboe-VIX-Datei (1990–23.10.2026). Änderungen nach diesem Commit zählen als neuer Versuch im Trial-Log (`../TRIAL_LOG.md`).

**Vorab festgehalten:** US500 (Nr. 9–16), JPY, CHF und Gold (Nr. 3, 6, 7, 18) wurden mit anderen Regeln ausgewertet. Ein VIX-Signal wurde nie verwendet.

## 0. Feste Rahmenbedingungen (für alle Strategien gleich)

- Expert Advisor für MetaTrader 5, handelt vollständig autonom
- FTMO 2-Step, Swing, 100.000 USD
- Max. Verlust gesamt 10 %, max. Tagesverlust 5 %
- Ziel Phase 1 +10 %, Ziel Phase 2 +5 %
- News-Trading und Halten übers Wochenende erlaubt

## 1. Hypothese

In einem Risk-off-Regime (VIX hoch gegenüber dem letzten Jahr) verdienen Long-Positionen in sicheren Häfen (X-HAVEN) bzw. in US500 (X-FEAR, Giot 2005) nach Kosten mit t ≥ 3.

**Erwartung vor dem Test: Scheitern beider Varianten.**

## 2. Daten und Zeiträume

- VIX: Cboe-Tagesschlusskurse (`data/raw/VIX_History.csv`)
- Kurse: HistData M5; Tagesbuchhaltung von Modell G über `run_weights` aus Nr. 6
  - FX und Gold: Bewertung 16:50 New York, FX-Kosten, Swaps (Zinsdifferenz − 1 %), 0,7-%-Gebühr
  - US500: Bewertung 15:50 New York, Index-Kosten und -Swaps (Modell H)
- **Warm-up:** 2014
- **In-Sample (IS):** Handelstage 2015–2023
- **Hold-out (HO):** ab 01.01.2024, einmalig und nur, wenn IS besteht

## 3. Regeln

**Regime** je VIX-Handelstag t: Risk-off, wenn der VIX-Schluss ≥ 90-%-Quantil der VIX-Schlüsse der 252 Handelstage vor t (ohne t). Sonst normal.

**Varianten (je ein Trial)**

| Variante | Position im Risk-off | Ausführung des Signals von Tag t | sonst |
|---|---|---|---|
| **X-HAVEN** | Long JPY (Short USDJPY), Long CHF (Short USDCHF), Long XAUUSD, je `10 % / σ` | 16:50 New York am Tag t (VIX-Schluss 16:15 bekannt) | flat |
| **X-FEAR** | Long US500, `10 % / σ` | 15:50 New York am nächsten US500-Handelstag | flat |

- σ = EWMA-Volatilität des Instruments (Schwerpunkt 60 Tage, Untergrenze 4 %), festgelegt beim Einstieg. Bis zum Regimewechsel wird nicht nachjustiert.
- Fehlt am Ausführungstag die exakte Kerze, wird am nächsten Tag mit Kerze gehandelt.

## 4. Akzeptanzkriterien

**In-Sample, je Variante** (alle müssen erfüllt sein)

| # | Kriterium |
|---|---|
| 1 | Mittleres Netto-Tagesergebnis > 0 mit t-Wert ≥ **3,0** (kleinster aus iid, Woche, Monat) |
| 2 | ≥ 6 von 9 Jahren positiv (Jahre ohne Position zählen nicht als positiv) |
| 3 | Beide Teilzeiträume 2015–2019 und 2020–2023 mit positivem Netto-Mittel |
| 4 | Mittleres Ergebnis bei doppelten Kosten > 0 |

**Variantenwahl:** höherer t-Wert, falls beide bestehen. Besteht keine, ist **Strategie Nr. 19 gescheitert**, und der Hold-out bleibt unberührt.

**Beschreibend, ohne Einfluss auf die Entscheidung:** Zeit im Risk-off-Regime, Anzahl der Episoden, Ergebnis je Instrument, Ergebnis je Jahr.

**Hold-out und FTMO:** wie Strategie Nr. 6.

## 5. Umsetzbarkeit als MT5-EA

⚠ Den VIX gibt es bei FTMO nicht. Der EA müsste den Tagesschluss per `WebRequest` laden (Cboe oder FRED). Der Rest (Quantil, Orders) ist einfach.

## 6. Trial-Log (Fortsetzung des globalen Logs)

| # | Test |
|---|---|
| T64 | X-HAVEN, In-Sample |
| T65 | X-FEAR, In-Sample |
| T66 | Hold-out der gewählten Variante (nur falls T64 oder T65 besteht) |
| T67 | FTMO-Bootstrap (nur falls T66 besteht) |
