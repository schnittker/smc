# Vorregistrierung: Modell P „Pre-FOMC-Drift“ (Strategie Nr. 9)

Festgelegt am 24.10.2026, **bevor** Code für dieses Modell geschrieben oder Kursdaten dafür ausgewertet wurden. Vorher erstellt wurde nur die Terminliste `research/fomc_dates.csv` aus den Kalenderseiten der Federal Reserve (Abruf 24.10.2026, Skript `research/scripts/build_fomc_dates.py`). Änderungen nach diesem Commit zählen als neuer Versuch im Trial-Log (`../TRIAL_LOG.md`).

## 0. Feste Rahmenbedingungen (für alle Strategien gleich)

- Expert Advisor für MetaTrader 5, handelt vollständig autonom
- FTMO 2-Step, Swing, 100.000 USD
- Max. Verlust gesamt 10 %, max. Tagesverlust 5 %
- Ziel Phase 1 +10 %, Ziel Phase 2 +5 %
- News-Trading und Halten übers Wochenende erlaubt

## 1. Hypothese

US-Aktienindizes steigen in den 24 Stunden vor planmäßigen FOMC-Entscheiden (Lucca & Moench 2015).

**Erwartung vor dem Test: Scheitern.** Kurov, Wolfe & Gilbert (2021) finden nach 2015 keine Drift mehr (`docs/00_Recherche.md`).

## 2. Daten und Zeiträume

- HistData M5 (Bid): SPXUSD → US500.cash, NSXUSD → US100.cash
- Kostenmodell, Swaps und Zeitmodell aus dem SMC-Projekt (Modell H, `smc/strategy_h.py`)
- **Termine:** planmäßige FOMC-Sitzungen laut Fed, Entscheidungstag = zweiter Sitzungstag. Ausgeschlossen sind unplanmäßige und abgesagte Sitzungen sowie Notation Votes.
- **In-Sample (IS):** Entscheidungstage 2015–2023 (71 Termine; 2020 nur 7, weil die März-Sitzung abgesagt wurde)
- **Hold-out (HO):** Entscheidungstage ab 01.01.2024 bis Datenende (16.10.2026), einmalig und nur, wenn IS besteht

## 3. Regeln

**Zeiten** (New York; die Entscheidung kommt um 14:00)
- Einstieg: 14:00 am Vortag. Vortag = letzter Werktag (Mo–Fr) vor dem Entscheidungstag.
- Ausstieg: 13:55 am Entscheidungstag
- Markt zur Eröffnung der M5-Kerze, die zu diesem Zeitpunkt beginnt. Fehlt eine der beiden Kerzen, entfällt der Termin.

**Varianten (je ein Trial)**

| Variante | Instrument | Position |
|---|---|---|
| **P-SPX** | US500 | Long |
| **P-NDX** | US100 | Long |

**Notfall-Stop:** 3 × ATR14(D1), ATR der letzten geschlossenen D1-Kerze vor dem Einstieg. Long-Stop gegen das Bid-Low; bei einem Gap wird zur Eröffnung gefüllt.

**Kosten** (wie Modell H)
- Spread: FTMO-Durchschnitt 2026 relativ zum mittleren Kurs 2026, in bp auf alle Jahre angewandt. Kauf zum Ask.
- Slippage: ¼ Spread je Ausführung
- Keine Kommission
- **Swap:** je Rollover (17:00 New York) `(Dividendenrendite − USD-Zins − 2,5 %) / 365`, mittwochs dreifach. Bei Entscheiden am Mittwoch fällt ein Rollover an (Dienstag), bei Entscheiden am Donnerstag ein dreifacher (Mittwoch).
- Keine Umrechnungsgebühr (USD)

**Bewertungseinheit:** Netto-Ergebnis je Termin in bp des Einstiegskurses (Mittelkurs).

## 4. Akzeptanzkriterien

**In-Sample, je Variante** (alle müssen erfüllt sein)

| # | Kriterium |
|---|---|
| 1 | Mittleres Netto-Ergebnis je Termin > 0 mit t-Wert ≥ **3,0**, als kleinster Wert aus iid und Clustern nach Quartal |
| 2 | ≥ 6 von 9 Jahren mit positivem Netto-Ergebnis |
| 3 | Beide Teilzeiträume 2015–2019 und 2020–2023 mit positivem Netto-Mittel |
| 4 | Mittleres Ergebnis bei doppelten Kosten > 0 (Spread, Slippage und Swap verdoppelt) |

**Variantenwahl:** höherer t-Wert, falls beide bestehen. Besteht keine, ist **Strategie Nr. 9 gescheitert**, und der Hold-out bleibt unberührt.

**Beschreibend, ohne Einfluss auf die Entscheidung:**
- Vergleich mit demselben Uhrzeitfenster (14:00 Vortag bis 13:55) an allen anderen Handelstagen: Mittelwert und Differenz. Die Differenz ist der eigentliche FOMC-Effekt, denn ein Index-Long verdient auch ohne Ereignis.
- Teilfenster: 14:00–16:00 am Vortag, 16:00 Vortag bis 09:30 am Entscheidungstag, 09:30–13:55
- Reaktion nach der Entscheidung: 14:00–16:00 am Entscheidungstag
- Ergebnis je Jahr

**Hold-out** (einmalig, gewählte Variante)

| # | Kriterium |
|---|---|
| 1 | Mittleres Netto-Ergebnis je Termin > 0 |
| 2 | ≥ untere Grenze des 95-%-Konfidenzintervalls von IS (Bootstrap über Termine) |

**FTMO** (Termine IS + HO, nur falls der Hold-out besteht): Verfahren wie Strategie Nr. 5 (`../05-monatsend-rebalancing/docs/01_Vorregistrierung.md` §4):
- Skalierung auf 0,5–2,0 % Standardabweichung je Termin
- Worst Case aus M5-Extremen
- Mindesttage-Modus, Bootstrap über Termine
- Bestanden bei ≥ 70 % Bestehenschance und ≤ 6 Monaten Median-Dauer

**Vorab festgehalten:** Mit 8 Terminen pro Jahr ist das FTMO-Kriterium allein kaum erreichbar.

## 5. Umsetzbarkeit als MT5-EA

- **Termine live:** über den MT5-Wirtschaftskalender (`CalendarValueHistory`, Ereignis „Fed Interest Rate Decision“, Land US). Es sind keine externen Daten nötig.
- **Logik:** am Vortag um 14:00 New York kaufen, am Entscheidungstag um 13:55 verkaufen, Notfall-Stop als Server-Stop.

## 6. Trial-Log (Fortsetzung des globalen Logs)

| # | Test |
|---|---|
| T31 | P-SPX, In-Sample |
| T32 | P-NDX, In-Sample |
| T33 | Hold-out der gewählten Variante (nur falls T31 oder T32 besteht) |
| T34 | FTMO-Bootstrap (nur falls T33 besteht) |
