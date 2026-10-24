# Vorregistrierung: Modell V „Volatilitätsgesteuertes US500-Long“ (Strategie Nr. 14)

Festgelegt am 24.10.2026, **bevor** Code für dieses Modell geschrieben oder Daten dafür ausgewertet wurden. Änderungen nach diesem Commit zählen als neuer Versuch im Trial-Log (`../TRIAL_LOG.md`).

**Vorab festgehalten:** US500 wurde in Nr. 4 (Trend), 9, 10, 11 und 12 bereits ausgewertet. Die Nebenergebnisse zeigen, dass Long US500 2015–2023 vor Kosten positiv war (z. B. Nr. 12 intraday und overnight). Eine Volatilitätssteuerung wurde nicht ausgewertet.

## 0. Feste Rahmenbedingungen (für alle Strategien gleich)

- Expert Advisor für MetaTrader 5, handelt vollständig autonom
- FTMO 2-Step, Swing, 100.000 USD
- Max. Verlust gesamt 10 %, max. Tagesverlust 5 %
- Ziel Phase 1 +10 %, Ziel Phase 2 +5 %
- News-Trading und Halten übers Wochenende erlaubt

## 1. Hypothese

Ein US500-Long, dessen Nominalwert umgekehrt zur jüngsten Volatilität bzw. Varianz skaliert wird, erzielt nach Spreads und Swaps eine Sharpe Ratio von ≥ 1 (Moreira & Muir 2017; `docs/00_Recherche.md`).

**Erwartung vor dem Test: Scheitern am t-Kriterium.**

## 2. Daten und Zeiträume

- HistData M5 (Bid): SPXUSD → US500.cash. NSXUSD → US100.cash nur beschreibend.
- **Engine:** Tagesbuchhaltung von Modell G in der verallgemeinerten Form aus Nr. 6 (`../06-fx-carry/research/carry/model.py`, `run_weights`) mit dem Index-Kostenmodell von Modell H (SMC `smc/strategy_h.py`):
  - Bewertung um 15:50 New York, Signalkurs 15:45
  - Handelskosten je gehandeltem Nominal: halber Spread plus ¼ Spread Slippage
  - Swap je Rollover `(Dividendenrendite − USD-Zins − 2,5 %) / 365`, mittwochs dreifach
- **Warm-up:** 2014
- **In-Sample (IS):** Handelstage 2015–2023
- **Hold-out (HO):** ab 01.01.2024 bis Datenende, einmalig und nur, wenn IS besteht

## 3. Regeln

**Tagesrenditen:** log. Änderung des 15:45-Kurses von Handelstag zu Handelstag. Handelstag = Tag mit exakter 15:50-Kerze.

**Varianten (je ein Trial)**

| Variante | Umschichtung | Zielgewicht w (Nominal in Vielfachen des Kapitals) |
|---|---|---|
| **V-VOL** | täglich | `w = 15 % / σ`, σ = Standardabweichung der letzten 21 Tagesrenditen × √261 |
| **V-MM** | erster Handelstag jedes Monats | `w = (15 %)² / RV`, RV = Summe der quadrierten Tagesrenditen des Vormonats × 12 (Moreira & Muir) |

- Beide Varianten: **Obergrenze w ≤ 3**, kein Short.
- Erste Umschichtung, sobald 21 Renditen bzw. ein voller Vormonat vorliegen.
- Kein Umschichten an Tagen ohne exakte 15:50-Kerze; dann bleibt das Gewicht stehen.

**Bewertungseinheit:** Netto-Tagesergebnis des Portfolios in Kapitalanteilen.

## 4. Akzeptanzkriterien

**In-Sample, je Variante** (alle müssen erfüllt sein)

| # | Kriterium |
|---|---|
| 1 | Mittleres Netto-Tagesergebnis > 0 mit t-Wert ≥ **3,0** (kleinster aus iid, Woche, Monat) |
| 2 | ≥ 6 von 9 Jahren positiv |
| 3 | Beide Teilzeiträume 2015–2019 und 2020–2023 mit positivem Netto-Mittel |
| 4 | Mittleres Ergebnis bei doppelten Kosten > 0 (Handelskosten und belastende Swaps verdoppelt) |

**Variantenwahl:** höherer t-Wert, falls beide bestehen. Besteht keine, ist **Strategie Nr. 14 gescheitert**, und der Hold-out bleibt unberührt.

**Beschreibend, ohne Einfluss auf die Entscheidung:**
- Referenz „konstant w = 1“ (Index halten mit CFD-Kosten)
- Zerlegung in Kurs, Swaps und Handel
- Maximaler Drawdown und schlechtester Tag bei 10 % Volatilität
- US100
- Ergebnis je Jahr

**Hold-out und FTMO:** wie Strategie Nr. 6 (`../06-fx-carry/docs/01_Vorregistrierung.md` §4: Ziel-Volatilität 10/15/20 %, Worst Case aus M5, Block-Bootstrap über Monate, ≥ 70 % Bestehenschance, ≤ 6 Monate Median-Dauer).

## 5. Umsetzbarkeit als MT5-EA

Täglich bzw. monatlich um 15:50 New York auf das Zielgewicht umschichten; die Volatilität berechnet der EA aus den eigenen Kursen. Es werden keine externen Daten benötigt.

## 6. Trial-Log (Fortsetzung des globalen Logs)

| # | Test |
|---|---|
| T48 | V-VOL, In-Sample |
| T49 | V-MM, In-Sample |
| T50 | Hold-out der gewählten Variante (nur falls T48 oder T49 besteht) |
| T51 | FTMO-Bootstrap (nur falls T50 besteht) |
