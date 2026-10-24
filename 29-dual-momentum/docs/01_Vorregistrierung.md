# Vorregistrierung: Modell D „Dual Momentum“ (Strategie Nr. 29)

Festgelegt am 24.10.2026, **bevor** Code für dieses Modell geschrieben oder Daten dafür ausgewertet wurden. Änderungen nach diesem Commit zählen als neuer Versuch im Trial-Log (`../TRIAL_LOG.md`).

**Vorab festgehalten:** Alle Anlagen des Universums wurden in Nr. 4, 14, 28 und 30 ausgewertet. Die Kennzahlen dieser Tests sind bekannt, z. B. US500 halten: Sharpe 0,51.

## 0. Feste Rahmenbedingungen (für alle Strategien gleich)

- Expert Advisor für MetaTrader 5, handelt vollständig autonom
- FTMO 2-Step, Swing, 100.000 USD
- Max. Verlust gesamt 10 %, max. Tagesverlust 5 %
- Ziel Phase 1 +10 %, Ziel Phase 2 +5 %
- News-Trading und Halten übers Wochenende erlaubt

## 1. Hypothese

Monatliche Rotation in die Anlage(n) mit der höchsten 12-Monats-Rendite, nur bei Rendite über dem USD-Zins, verdient nach Kosten mit t ≥ 3.

**Erwartung vor dem Test: Scheitern.**

## 2. Daten und Zeiträume

- **Universum** (8 Anlagen, Kostenmodell H, Bewertung zur Kassazeit): US500, US100, FRA40, UK100, JP225, HK50, AUS200, XAUUSD
- Tagesbuchhaltung über `run_weights` (Nr. 6) mit Index- bzw. Metall-Swaps
- USD-Zins: FRED-Monatsreihe aus dem SMC-Swap-Modell
- **Warm-up:** 2014 (12-Monats-Renditen ab Anfang 2015)
- **In-Sample:** Handelstage 2015–2023. **Hold-out:** ab 2024, einmalig und nur, wenn IS besteht.

## 3. Regeln

**Am ersten Handelstag jedes Monats** (exakte Bewertungskerze je Anlage):
- 12-Monats-Rendite `R12` = Signalkurs heute / Signalkurs vor 252 Handelstagen − 1, je Anlage
- Hürde = USD-Zins des Vormonats (p. a.)

| Variante | Auswahl | Position |
|---|---|---|
| **D-TOP1** | Anlage mit dem höchsten R12 | Long, wenn R12 > Hürde, sonst flat |
| **D-TOP2** | die zwei Anlagen mit dem höchsten R12 | je Anlage long, wenn ihr R12 > Hürde |

- Größe je Position `10 % / σ` (EWMA wie Modell G), monatlich neu gesetzt
- Fehlt einer Anlage der Kurs am Umschichtungstag, wird ihre Zielposition am nächsten Tag mit Kurs gesetzt.

## 4. Akzeptanzkriterien

Wie Nr. 14 (alle müssen erfüllt sein): t ≥ **3,0** (kleinster aus iid, Woche, Monat) bei positivem Mittel; ≥ 6 von 9 Jahren positiv; beide Teilzeiträume 2015–2019 und 2020–2023 positiv; doppelte Kosten > 0. Variantenwahl über den t-Wert. Besteht keine, ist **Strategie Nr. 29 gescheitert**, und der Hold-out bleibt unberührt.

**Beschreibend:** Häufigkeit der gewählten Anlagen, Monate in Cash, Vergleich mit US500 halten.

**Hold-out und FTMO:** wie Nr. 14.

## 5. Umsetzbarkeit als MT5-EA

Monatliche Rotation über die eigenen D1-Kurse. Den USD-Zins liefert der Swap-Satz (wie Nr. 6). Es werden keine externen Daten benötigt.

## 6. Trial-Log (Fortsetzung des globalen Logs)

| # | Test |
|---|---|
| T102 | D-TOP1, In-Sample |
| T103 | D-TOP2, In-Sample |
| T104 | Hold-out der gewählten Variante (nur falls T102 oder T103 besteht) |
| T105 | FTMO-Bootstrap (nur falls T104 besteht) |
