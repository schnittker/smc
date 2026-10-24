# Vorregistrierung: Modell T „Turn-of-the-Month US500“ (Strategie Nr. 10)

Festgelegt am 24.10.2026, **bevor** Code für dieses Modell geschrieben oder Daten dafür ausgewertet wurden. Änderungen nach diesem Commit zählen als neuer Versuch im Trial-Log (`../TRIAL_LOG.md`).

**Vorab festgehalten:** Strategie Nr. 9 hat US500 bereits an FOMC-Terminen ausgewertet. Für die Monatswechsel-Fenster wurden keine Daten angesehen.

## 0. Feste Rahmenbedingungen (für alle Strategien gleich)

- Expert Advisor für MetaTrader 5, handelt vollständig autonom
- FTMO 2-Step, Swing, 100.000 USD
- Max. Verlust gesamt 10 %, max. Tagesverlust 5 %
- Ziel Phase 1 +10 %, Ziel Phase 2 +5 %
- News-Trading und Halten übers Wochenende erlaubt

## 1. Hypothese

US500 steigt in den Handelstagen um den Monatswechsel stärker als sonst, so stark, dass ein Long nur in diesem Fenster nach Kosten einen t-Wert ≥ 3 erreicht (McConnell & Xu 2008; `docs/00_Recherche.md`).

**Erwartung vor dem Test: Scheitern am t-Kriterium.**

## 2. Daten und Zeiträume

- HistData M5 und D1 (Bid): SPXUSD → US500.cash. NSXUSD → US100.cash nur beschreibend.
- Positionsmechanik, Kosten und Swaps wie Strategie Nr. 9 (`../09-pre-fomc-drift/research/fomc/model.py`, Klasse `Index`; Kostenmodell H aus dem SMC-Projekt)
- **Handelstage:** NYSE-Kalender, also Mo–Fr ohne NYSE-Feiertage:
  - Neujahr, Martin Luther King Day, Presidents Day, Karfreitag, Memorial Day, Juneteenth (ab 2022), Independence Day, Labor Day, Thanksgiving, Weihnachten
  - Verschiebung bei Samstag auf Freitag, bei Sonntag auf Montag. Ausnahme: Neujahr am Samstag wird nicht vorgezogen.
  - Außerdem die Sonderschließungen 05.12.2018 und 09.01.2025.
- **Ereignis:** Monatswechsel von Monat m auf m+1. Zugeordnet wird er dem Monat m+1.
- **In-Sample (IS):** Monatswechsel mit Tag +1 in 2015–2023 (108 Ereignisse)
- **Hold-out (HO):** Tag +1 ab 01.01.2024 bis Datenende, einmalig und nur, wenn IS besteht

## 3. Regeln

**Tageszählung:** Tag −1 = letzter NYSE-Handelstag des Monats, Tag +1 = erster Handelstag des neuen Monats. Rendite von Tag k = Schlusskurs Tag k−1 bis Schlusskurs Tag k. Als „Schlusskurs“ dient die Eröffnung der M5-Kerze um 15:55 New York.

**Varianten (je ein Trial), beide Long US500**

| Variante | Fenster | Einstieg (15:55 New York) | Ausstieg (15:55 New York) |
|---|---|---|---|
| **T-KLASSIK** | Tag −1 bis +3 (McConnell & Xu) | Tag −2 | Tag +3 |
| **T-FRÜH** | Tag −4 bis +2 (verschobenes Fenster) | Tag −5 | Tag +2 |

**Ausführung, Stop und Kosten** wie Strategie Nr. 9:
- Markt zur Eröffnung der M5-Kerze. Fehlt eine Kerze, entfällt das Ereignis.
- Notfall-Stop 3 × ATR14(D1)
- Spread als FTMO-Durchschnitt (relativ), Slippage ¼ Spread je Ausführung, keine Kommission
- Swap je Rollover `(Dividendenrendite − USD-Zins − 2,5 %) / 365`, mittwochs dreifach

**Bewertungseinheit:** Netto-Ergebnis je Ereignis in bp des Einstiegskurses.

## 4. Akzeptanzkriterien

**In-Sample, je Variante** (alle müssen erfüllt sein)

| # | Kriterium |
|---|---|
| 1 | Mittleres Netto-Ergebnis je Ereignis > 0 mit t-Wert ≥ **3,0** (kleinster aus iid und Clustern nach Quartal) |
| 2 | ≥ 6 von 9 Jahren positiv |
| 3 | Beide Teilzeiträume 2015–2019 und 2020–2023 mit positivem Netto-Mittel |
| 4 | Mittleres Ergebnis bei doppelten Kosten > 0 |

**Variantenwahl:** höherer t-Wert, falls beide bestehen. Besteht keine, ist **Strategie Nr. 10 gescheitert**, und der Hold-out bleibt unberührt.

**Beschreibend, ohne Einfluss auf die Entscheidung:**
- Mittlere Tagesrendite (15:55 bis 15:55) je relativem Tag −8 bis +5 sowie aller übrigen Tage. Zeigt, wo der Effekt heute liegt.
- Beide Fenster auf US100
- Ergebnis je Jahr

**Hold-out und FTMO:** wie Strategie Nr. 9 (Bootstrap über Ereignisse, Skalierung je Ereignis, Kriterien ≥ 70 % Bestehenschance und ≤ 6 Monate Median-Dauer).

## 5. Umsetzbarkeit als MT5-EA

- NYSE-Feiertagskalender im EA (regelbasiert wie oben, Sonderschließungen als Liste)
- Kauf und Verkauf um 15:55 New York, Notfall-Stop als Server-Stop. Es sind keine externen Daten nötig.

## 6. Trial-Log (Fortsetzung des globalen Logs)

| # | Test |
|---|---|
| T35 | T-KLASSIK, In-Sample |
| T36 | T-FRÜH, In-Sample |
| T37 | Hold-out der gewählten Variante (nur falls T35 oder T36 besteht) |
| T38 | FTMO-Bootstrap (nur falls T37 besteht) |
