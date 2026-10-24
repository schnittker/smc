# Vorregistrierung: Modell N „Overnight-Drift US500“ (Strategie Nr. 12)

Festgelegt am 24.10.2026, **bevor** Code für dieses Modell geschrieben oder Daten dafür ausgewertet wurden. Änderungen nach diesem Commit zählen als neuer Versuch im Trial-Log (`../TRIAL_LOG.md`).

**Vorab festgehalten:** US500 wurde in Nr. 4, 9, 10 und 11 ausgewertet. Nr. 9 zeigte beschreibend, dass die FOMC-Drift über Nacht entsteht (16:00–09:30). Dieses Modell testet die Nacht aber an allen Tagen, mit Regeln aus der Literatur. Uhrzeitfenster um 02:00 wurden noch nicht angesehen.

## 0. Feste Rahmenbedingungen (für alle Strategien gleich)

- Expert Advisor für MetaTrader 5, handelt vollständig autonom
- FTMO 2-Step, Swing, 100.000 USD
- Max. Verlust gesamt 10 %, max. Tagesverlust 5 %
- Ziel Phase 1 +10 %, Ziel Phase 2 +5 %
- News-Trading und Halten übers Wochenende erlaubt

## 1. Hypothese

Long US500 außerhalb der US-Handelszeit verdient nach Kosten (Cliff et al. 2008), vor allem bei Eröffnung in Europa und nach Verlusttagen (Boyarchenko et al. 2023; `docs/00_Recherche.md`).

**Erwartung vor dem Test: Scheitern** (zu klein gegen die Kosten, seit 2021 laut Autoren verschwunden).

## 2. Daten und Zeiträume

- HistData M5 und D1 (Bid): SPXUSD → US500.cash. NSXUSD → US100.cash nur beschreibend.
- Positionsmechanik, Kosten und Swaps wie Nr. 9 (`../09-pre-fomc-drift/research/fomc/model.py`, `Index.trade_long`):
  - FTMO-Durchschnittsspread relativ, ¼ Spread Slippage je Ausführung, keine Kommission
  - Swap je Rollover `(Dividendenrendite − USD-Zins − 2,5 %) / 365`, mittwochs dreifach
  - Notfall-Stop 3 × ATR14(D1)
- NYSE-Kalender aus Nr. 10. Kurs zum Zeitpunkt t = Eröffnung der M5-Kerze, die um t beginnt; fehlt sie, entfällt der Tag.
- **In-Sample (IS):** Handelstage (Ausstiegstag) 2015–2023
- **Hold-out (HO):** ab 01.01.2024 bis Datenende, einmalig und nur, wenn IS besteht

## 3. Regeln (alle Zeiten New York, alle Positionen long)

Für jeden NYSE-Handelstag d mit vorherigem Handelstag p gilt:

| Variante | Einstieg | Ausstieg | Bedingung |
|---|---|---|---|
| **N-NACHT** | 16:00 an p | 09:30 an d | keine |
| **N-EU** | 02:00 an d | 03:00 an d | keine |
| **N-EU-DOWN** | 02:00 an d | 03:00 an d | Schluss-zu-Schluss-Rendite von p negativ: Kurs 16:00 an p < Kurs 16:00 am Handelstag vor p |

- Nach Wochenenden und Feiertagen gilt das Paar (p, d) entsprechend. N-NACHT hält dann über das Wochenende (erlaubt).
- **Bewertungseinheit:** Netto-Ergebnis je Handelstag d in bp des Einstiegskurses.

## 4. Akzeptanzkriterien

**In-Sample, je Variante** (alle müssen erfüllt sein)

| # | Kriterium |
|---|---|
| 1 | Mittleres Netto-Ergebnis je Trade > 0 mit t-Wert ≥ **3,0** (kleinster aus iid, Woche, Monat) |
| 2 | ≥ 6 von 9 Jahren positiv |
| 3 | Beide Teilzeiträume 2015–2019 und 2020–2023 mit positivem Netto-Mittel |
| 4 | Mittleres Ergebnis bei doppelten Kosten > 0 |

**Variantenwahl:** höchster t-Wert unter den bestandenen Varianten. Besteht keine, ist **Strategie Nr. 12 gescheitert**, und der Hold-out bleibt unberührt.

**Beschreibend, ohne Einfluss auf die Entscheidung:**
- Intraday-Long (09:30–16:00) zum Vergleich
- N-EU nach Gewinntagen
- Teilzeitraum ab 2021
- Alle drei Varianten auf US100
- Ergebnis je Jahr

**Hold-out und FTMO:** wie Strategie Nr. 11 (`../11-intraday-momentum/docs/01_Vorregistrierung.md` §4).

## 5. Umsetzbarkeit als MT5-EA

Feste Uhrzeiten, NYSE-Kalender, für N-EU-DOWN der Vergleich zweier Schlusskurse, Server-Stop. Es werden keine externen Daten benötigt.

## 6. Trial-Log (Fortsetzung des globalen Logs)

| # | Test |
|---|---|
| T43 | N-NACHT, In-Sample |
| T44 | N-EU, In-Sample |
| T45 | N-EU-DOWN, In-Sample |
| T46 | Hold-out der gewählten Variante (nur falls eine besteht) |
| T47 | FTMO-Bootstrap (nur falls T46 besteht) |
