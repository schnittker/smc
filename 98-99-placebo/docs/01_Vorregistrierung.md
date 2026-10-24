# Vorregistrierung: Modell PL „Placebo-Kontrollen“ (Nr. 98 und 99)

Festgelegt am 24.10.2026, **bevor** Code für dieses Modell geschrieben oder Daten dafür ausgewertet wurden. Änderungen nach diesem Commit zählen als neuer Versuch im Trial-Log (`../TRIAL_LOG.md`).

## 0. Feste Rahmenbedingungen (für alle Strategien gleich)

- Expert Advisor für MetaTrader 5, handelt vollständig autonom
- FTMO 2-Step, Swing, 100.000 USD
- Max. Verlust gesamt 10 %, max. Tagesverlust 5 %
- Ziel Phase 1 +10 %, Ziel Phase 2 +5 %
- News-Trading und Halten übers Wochenende erlaubt

## 1. Hypothese

Kontrollen: Beide **sollen scheitern**. Ein Bestehen wäre ein Warnsignal für die Pipeline.

## 2. Regeln

**PL-RANDOM (Nr. 98)**
- H4-Serverkerzen der 17 Instrumente, Engine `chart.engine` wie Nr. 50/51 mit Stop 2 × ATR14, Ziel 2R und Zeitstopp 30
- **Einstieg:** je Instrument und Kerze mit Wahrscheinlichkeit 1/30; Richtung ±1 gleichverteilt
- Zufallszahlen: `numpy.random.default_rng(98 + Index des Instruments)`, für jede Kerze gezogen, unabhängig davon, ob eine Position offen ist
- Kosten, Swaps, Größe (0,25 % Risiko) und Portfolio wie Nr. 50/51

**PL-MOON (Nr. 99)**
- Tagesbuchhaltung der 34 Instrumente wie Nr. 81/82
- **Mondphase** zur Tagesmarke: Alter = (t − 2000-01-06 18:14 UTC) mod 29,530588853 Tage
- Long, wenn das Alter < 14,765 Tage (Neumond → Vollmond), sonst Short
- **Gewicht** 10 % / σ, gesetzt bei jedem Phasenwechsel

**In-Sample:** 2015–2023. **Hold-out:** nicht vorgesehen; Kontrollen werden nicht weiterverfolgt.

## 3. Akzeptanzkriterien

Wie die jeweiligen Vorlagen: PL-RANDOM wie Nr. 50/51, PL-MOON wie Nr. 81/82. **Erwartung: nicht bestanden.**

**Beschreibend (PL-RANDOM):** Ø R vor Kosten mit 95-%-Intervall. Es muss 0 enthalten.

## 4. Trial-Log (Fortsetzung des globalen Logs)

| # | Test |
|---|---|
| T297 | PL-RANDOM (Nr. 98), In-Sample |
| T298 | PL-MOON (Nr. 99), In-Sample |
