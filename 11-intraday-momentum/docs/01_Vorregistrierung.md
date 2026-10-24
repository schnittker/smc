# Vorregistrierung: Modell I „Intraday-Momentum US500“ (Strategie Nr. 11)

Festgelegt am 24.10.2026, **bevor** Code für dieses Modell geschrieben oder Daten dafür ausgewertet wurden. Änderungen nach diesem Commit zählen als neuer Versuch im Trial-Log (`../TRIAL_LOG.md`).

**Vorab festgehalten:** US500 wurde in Nr. 4, 9 und 10 bereits ausgewertet: Trend auf Tagesbasis, FOMC-Fenster, Monatswechsel. Die Uhrzeitfenster dieses Modells wurden dabei nicht angesehen.

## 0. Feste Rahmenbedingungen (für alle Strategien gleich)

- Expert Advisor für MetaTrader 5, handelt vollständig autonom
- FTMO 2-Step, Swing, 100.000 USD
- Max. Verlust gesamt 10 %, max. Tagesverlust 5 %
- Ziel Phase 1 +10 %, Ziel Phase 2 +5 %
- News-Trading und Halten übers Wochenende erlaubt

## 1. Hypothese

Die Richtung der Indexrendite vom Vortagsschluss bis 10:00 bzw. bis 15:30 New York sagt die Richtung von 15:30–16:00 voraus. Eine Position in diese Richtung verdient nach Kosten (Gao et al. 2018; Baltussen et al. 2021; `docs/00_Recherche.md`).

**Erwartung vor dem Test: eher Scheitern** (Effekt etwa so groß wie die Kosten).

## 2. Daten und Zeiträume

- HistData M5 und H1 (Bid): SPXUSD → US500.cash. NSXUSD → US100.cash nur beschreibend.
- Kostenmodell H aus dem SMC-Projekt (FTMO-Durchschnittsspread relativ zum Kurs, ¼ Spread Slippage je Ausführung, keine Kommission)
- NYSE-Kalender aus Strategie Nr. 10 (`../10-turn-of-the-month/research/tom/nyse.py`)
- **Kurs zum Zeitpunkt t:** Eröffnung der M5-Kerze, die um t beginnt
- **In-Sample (IS):** NYSE-Handelstage 2015–2023
- **Hold-out (HO):** ab 01.01.2024 bis Datenende, einmalig und nur, wenn IS besteht

## 3. Regeln

**Handelstage:** NYSE-Handelstage mit vollem Handel, deren vorheriger Handelstag ebenfalls voll war.
- Verkürzte Tage (Schluss 13:00) sind ausgeschlossen: Tag nach Thanksgiving, 24.12. und 03.07., sofern Handelstag.
- Fehlt einer der Kurse (Vortag 16:00, 10:00, 15:30, 16:00), entfällt der Tag.

**Renditen** (alle New York-Zeit)
- `r_ONFH` = Kurs 10:00 / Kurs 16:00 am Vortag − 1
- `r_ROD` = Kurs 15:30 / Kurs 16:00 am Vortag − 1
- `r_LAST` = Kurs 16:00 / Kurs 15:30 − 1 (nur Ergebnis, nicht Signal)

**Varianten (je ein Trial), beide auf US500**

| Variante | Signal | Quelle |
|---|---|---|
| **I-ONFH** | Vorzeichen von `r_ONFH` | Gao et al. 2018 |
| **I-ROD** | Vorzeichen von `r_ROD` | Baltussen et al. 2021 |

**Trade:** um 15:30 in Signalrichtung (Long bei positivem, Short bei negativem Signal, kein Trade bei 0), Ausstieg um 16:00.
- Kauf zum Ask (Bid + Spread), Verkauf zum Bid, Slippage ¼ Spread je Ausführung
- Notfall-Stop 3 × ATR14(H1) der letzten geschlossenen H1-Kerze; bei einem Gap zur Eröffnung gefüllt
- Keine Swaps, denn die Position ist um 17:00 New York geschlossen.

**Bewertungseinheit:** Netto-Ergebnis je Handelstag in bp des Einstiegskurses.

## 4. Akzeptanzkriterien

**In-Sample, je Variante** (alle müssen erfüllt sein)

| # | Kriterium |
|---|---|
| 1 | Mittleres Netto-Tagesergebnis > 0 mit t-Wert ≥ **3,0** (kleinster aus iid, Woche, Monat) |
| 2 | ≥ 6 von 9 Jahren positiv |
| 3 | Beide Teilzeiträume 2015–2019 und 2020–2023 mit positivem Netto-Mittel |
| 4 | Mittleres Ergebnis bei doppelten Kosten > 0 |

**Variantenwahl:** höherer t-Wert, falls beide bestehen. Besteht keine, ist **Strategie Nr. 11 gescheitert**, und der Hold-out bleibt unberührt.

**Beschreibend, ohne Einfluss auf die Entscheidung:**
- Regression von `r_LAST` auf `r_ONFH` bzw. `r_ROD` (Steigung, t, R²)
- Long- und Short-Trades getrennt
- Tage mit großem Signal (oberstes Drittel von |Signal|) gegen übrige
- Beide Varianten auf US100
- Ergebnis je Jahr

**Hold-out** (einmalig, gewählte Variante)

| # | Kriterium |
|---|---|
| 1 | Mittleres Netto-Tagesergebnis > 0 |
| 2 | ≥ untere Grenze des 95-%-Konfidenzintervalls von IS (Cluster-Bootstrap nach Monat) |

**FTMO** (Tagesergebnisse IS + HO, nur falls der Hold-out besteht):
- Skalierung auf eine Tagesschwankung von 0,5 %, 0,75 %, 1,0 % bzw. 1,25 % des Kapitals
- Phase 2 mit dem 0,75-Fachen; ab 3 % Drawdown wird halbiert, ab 6 % geviertelt
- Worst Case aus M5-Extremen gegen 5 % Tages- und 10 % Gesamtverlust; Mindesttage sind bei täglichem Handel automatisch erfüllt
- Block-Bootstrap über Kalendermonate, 10.000 Pfade
- Bestanden bei ≥ 70 % Bestehenschance beider Phasen und ≤ 6 Monaten Median-Dauer

## 5. Umsetzbarkeit als MT5-EA

Der EA kennt den Kurs um 16:00 des Vortags und um 10:00 bzw. 15:30, eröffnet um 15:30 eine Marktorder und schließt um 16:00. Dazu kommen der NYSE-Kalender (Nr. 10) und ein Server-Stop. Es werden keine externen Daten benötigt.

## 6. Trial-Log (Fortsetzung des globalen Logs)

| # | Test |
|---|---|
| T39 | I-ONFH, In-Sample |
| T40 | I-ROD, In-Sample |
| T41 | Hold-out der gewählten Variante (nur falls T39 oder T40 besteht) |
| T42 | FTMO-Bootstrap (nur falls T41 besteht) |
