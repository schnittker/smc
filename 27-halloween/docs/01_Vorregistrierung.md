# Vorregistrierung: Modell S „Halloween US-Indizes“ (Strategie Nr. 27)

Festgelegt am 24.10.2026, **bevor** Code für dieses Modell geschrieben oder Daten dafür ausgewertet wurden. Änderungen nach diesem Commit zählen als neuer Versuch im Trial-Log (`../TRIAL_LOG.md`).

**Vorab festgehalten:** US500 halten wurde in Nr. 14 ausgewertet (Sharpe 0,51, Jahresrenditen bekannt). Eine Aufteilung nach Jahreshälften wurde nicht angesehen.

## 0. Feste Rahmenbedingungen (für alle Strategien gleich)

- Expert Advisor für MetaTrader 5, handelt vollständig autonom
- FTMO 2-Step, Swing, 100.000 USD
- Max. Verlust gesamt 10 %, max. Tagesverlust 5 %
- Ziel Phase 1 +10 %, Ziel Phase 2 +5 %
- News-Trading und Halten übers Wochenende erlaubt

## 1. Hypothese

Long US-Index nur von November bis April verdient nach Kosten mit t ≥ 3 (Bouman & Jacobsen 2002).

**Erwartung vor dem Test: Scheitern.**

## 2. Daten und Zeiträume

- HistData M5; Tagesbuchhaltung von Modell G über `run_weights` (Nr. 6) mit Index-Kosten und -Swaps (Modell H), Bewertung 15:50 New York
- **In-Sample:** Handelstage 2015–2023 (Einstieg erst im November 2014, damit Januar–April 2015 investiert sind)
- **Hold-out:** ab 2024, einmalig und nur, wenn IS besteht

## 3. Regeln

| Variante | Instrument |
|---|---|
| **S-SPX** | US500 |
| **S-NDX** | US100 |

- Am ersten Handelstag (mit exakter 15:50-Kerze) im **November**: Long, Nominal = 1 × Kapital
- Am ersten Handelstag im **Mai**: flat
- Keine weiteren Anpassungen

## 4. Akzeptanzkriterien

Wie Nr. 14 (alle müssen erfüllt sein): t ≥ **3,0** (kleinster aus iid, Woche, Monat) bei positivem Mittel; ≥ 6 von 9 Jahren positiv; beide Teilzeiträume 2015–2019 und 2020–2023 positiv; doppelte Kosten > 0. Variantenwahl über den t-Wert. Besteht keine, ist **Strategie Nr. 27 gescheitert**, und der Hold-out bleibt unberührt.

**Beschreibend:** Renditen Winter- gegen Sommerhalbjahr je Jahr; Vergleich mit dem Halten.

**Hold-out und FTMO:** wie Nr. 14.

## 5. Umsetzbarkeit als MT5-EA

Zwei Orders pro Jahr. Es werden keine externen Daten benötigt.

## 6. Trial-Log (Fortsetzung des globalen Logs)

| # | Test |
|---|---|
| T92 | S-SPX, In-Sample |
| T93 | S-NDX, In-Sample |
| T94 | Hold-out der gewählten Variante (nur falls T92 oder T93 besteht) |
| T95 | FTMO-Bootstrap (nur falls T94 besteht) |
