# Vorregistrierung: Modell O „Opening Range Breakout 5 Minuten“ (Strategie Nr. 16)

Festgelegt am 24.10.2026, **bevor** Code für dieses Modell geschrieben oder Daten dafür ausgewertet wurden. Änderungen nach diesem Commit zählen als neuer Versuch im Trial-Log (`../TRIAL_LOG.md`).

**Vorab festgehalten:** US100 und US500 wurden in Nr. 9–15 mit anderen Regeln ausgewertet. Die erste 5-Minuten-Kerze ab 09:30 wurde nicht angesehen.

## 0. Feste Rahmenbedingungen (für alle Strategien gleich)

- Expert Advisor für MetaTrader 5, handelt vollständig autonom
- FTMO 2-Step, Swing, 100.000 USD
- Max. Verlust gesamt 10 %, max. Tagesverlust 5 %
- Ziel Phase 1 +10 %, Ziel Phase 2 +5 %
- News-Trading und Halten übers Wochenende erlaubt

## 1. Hypothese

Die Regel von Zarattini & Aziz (2023) verdient auf den FTMO-Index-CFDs nach Kosten mit einer Sharpe Ratio von ≥ 1 (`docs/00_Recherche.md`).

**Erwartung vor dem Test: Scheitern.**

## 2. Daten und Zeiträume

- HistData M5 (Bid): NSXUSD → US100.cash, SPXUSD → US500.cash
- Kostenmodell H aus dem SMC-Projekt: FTMO-Durchschnittsspread relativ zum Kurs, ¼ Spread Slippage je Ausführung, keine Kommission, keine Swaps (Position vor 17:00 geschlossen)
- Volle NYSE-Handelstage (Kalender aus Nr. 10, verkürzte Tage wie in Nr. 11 ausgeschlossen)
- **In-Sample (IS):** 2015–2023
- **Hold-out (HO):** ab 01.01.2024, einmalig und nur, wenn IS besteht

## 3. Regeln (New York-Zeit)

**Varianten (je ein Trial), identische Regeln**

| Variante | Instrument |
|---|---|
| **O-NDX** | US100 (Paper: QQQ) |
| **O-SPX** | US500 |

**Je Handelstag**
1. **Opening Range** = M5-Kerze 09:30–09:35 mit Eröffnung O1, Hoch H1, Tief L1, Schluss C1. Fehlt sie, kein Trade.
2. **Richtung:** C1 > O1 → Long, C1 < O1 → Short, C1 = O1 → kein Trade.
3. **Einstieg:** Markt zur Eröffnung der Kerze 09:35, Long zum Ask, Short zum Bid, Slippage ¼ Spread.
4. **Stop:** Long bei L1 (gegen Bid-Tief), Short bei H1 (gegen Bid-Hoch + Spread); bei einem Gap zur Eröffnung gefüllt; Slippage ¼ Spread.
5. **Risiko R** = |Einstiegskurs − Stop|. Ist R ≤ 0 (Einstieg jenseits des Stops), kein Trade.
6. **Ziel:** Einstieg ± 10 R (Limit, ohne Slippage).
7. **Tagesende:** Fehlen Stop und Ziel, Ausstieg zur Eröffnung der Kerze 16:00 (fehlt sie, zum Schluss der Kerze 15:55), Slippage ¼ Spread.
8. Treffen Stop und Ziel in derselben M5-Kerze, zählt der Stop (konservativ).

**Positionsgröße (wie im Paper):** Nominalwert = min(1 % Kapital / (R / Einstiegskurs), 4 × Kapital).

**Bewertungseinheit:** Netto-Tagesergebnis in Kapitalanteilen. Tage ohne Trade zählen mit 0.

## 4. Akzeptanzkriterien

**In-Sample, je Variante** (alle müssen erfüllt sein)

| # | Kriterium |
|---|---|
| 1 | Mittleres Netto-Tagesergebnis > 0 mit t-Wert ≥ **3,0** (kleinster aus iid, Woche, Monat) |
| 2 | ≥ 6 von 9 Jahren positiv |
| 3 | Beide Teilzeiträume 2015–2019 und 2020–2023 mit positivem Netto-Mittel |
| 4 | Mittleres Ergebnis bei doppelten Kosten > 0 (Spread und Slippage verdoppelt) |

**Variantenwahl:** höherer t-Wert, falls beide bestehen. Besteht keine, ist **Strategie Nr. 16 gescheitert**, und der Hold-out bleibt unberührt.

**Beschreibend, ohne Einfluss auf die Entscheidung:**
- Ergebnis in R je Trade (netto und vor Kosten)
- Trefferquote, Anteil Stop / Ziel / Tagesende
- Long gegen Short
- Kosten in R
- Ergebnis je Jahr
- Anteil der Tage mit Hebel-Obergrenze

**Hold-out und FTMO:** wie Strategie Nr. 11 (Tagesergebnisse, Skalierung auf 0,5–1,25 % Tagesschwankung, Worst Case aus M5, Block-Bootstrap über Monate, ≥ 70 % Bestehenschance, ≤ 6 Monate Median-Dauer).

## 5. Umsetzbarkeit als MT5-EA

- Um 09:35 New York die erste Kerze auswerten und eine Marktorder mit Server-Stop und Take-Profit senden.
- Schließen um 16:00, NYSE-Kalender.
- Positionsgröße aus dem Risiko. Es werden keine externen Daten benötigt.

## 6. Trial-Log (Fortsetzung des globalen Logs)

| # | Test |
|---|---|
| T56 | O-NDX, In-Sample |
| T57 | O-SPX, In-Sample |
| T58 | Hold-out der gewählten Variante (nur falls T56 oder T57 besteht) |
| T59 | FTMO-Bootstrap (nur falls T58 besteht) |
