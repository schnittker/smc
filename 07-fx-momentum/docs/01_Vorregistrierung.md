# Vorregistrierung: Modell X „FX Querschnitts-Momentum G8“ (Strategie Nr. 7)

Festgelegt am 24.10.2026, **bevor** Code für dieses Modell geschrieben oder Daten dafür ausgewertet wurden. Änderungen nach diesem Commit zählen als neuer Versuch im Trial-Log (`../TRIAL_LOG.md`).

## 0. Feste Rahmenbedingungen (für alle Strategien gleich)

- Expert Advisor für MetaTrader 5, handelt vollständig autonom
- FTMO 2-Step, Swing, 100.000 USD
- Max. Verlust gesamt 10 %, max. Tagesverlust 5 %
- Ziel Phase 1 +10 %, Ziel Phase 2 +5 %
- News-Trading und Halten übers Wochenende erlaubt

## 1. Hypothese

Ein dollar-neutrales Portfolio, das die G8-Währungen mit der höchsten vergangenen Überschussrendite gegen die mit der niedrigsten hält, erzielt nach Kosten eine positive Rendite (Menkhoff et al. 2012; Asness et al. 2013; Details in `docs/00_Recherche.md`).

**Erwartung vor dem Test: Scheitern** (Sharpe Ratio um 0).

## 2. Daten und Zeiträume

Wie Strategie Nr. 6 (`../06-fx-carry/docs/01_Vorregistrierung.md` §2):
- HistData M5 der 24 FX-Paare, FRED-Zinsen aus dem SMC-Swap-Modell
- Engine aus `../06-fx-carry/research/carry` (Commit `ebc877b`), Buchhaltung von Modell G
- **Warm-up:** 2014
- **In-Sample (IS):** Handelstage 01.01.2015–31.12.2023
- **Hold-out (HO):** 01.01.2024 bis Datenende, einmalig und nur, wenn IS besteht

## 3. Regeln

Alles wie Modell K (Nr. 6), **außer der Rangfolge**:

**Signal: Überschussrendite jeder Währung c gegen den USD**
- `x_c(t)` = log. USD-Wert von c (aus den 16:50-New-York-Kursen der USD-Paare) plus aufgelaufener Zinsvorteil.
- Der Zinsvorteil wird je Handelstag mit `(r_c − r_USD) / 261` angerechnet. Dabei gelten die Zinsen des Vormonats des jeweiligen Tages.
- USD hat immer `x = 0`.

**Varianten (je ein Trial)**

| Variante | Formationsrendite am Umschichtungstag z (in gemeinsamen Handelstagen) |
|---|---|
| **X-1** | `x(z) − x(z − 21)`, also der letzte Monat |
| **X-12** | `x(z − 21) − x(z − 252)`, also 12 Monate ohne den letzten (12-1) |

- **Rangfolge** absteigend nach Formationsrendite, bei Gleichstand alphabetisch.
- **Carry-Positionen wie K-3:** (1 / 8), (2 / 7), (3 / 6), also Long die drei Gewinner und Short die drei Verlierer, jeweils paarweise.
- **Umsetzung, Größe, Umschichtung, Bewertung und Kosten** wie Modell K:
  - Direkte Crosses oder zwei USD-Beine
  - `N = 10 % / σ` des Crosses (EWMA, Schwerpunkt 60 Tage)
  - Am ersten Handelstag jedes Monats um 16:50 New York
  - Spread, Slippage, Kommission, Swaps mit 1 % Aufschlag, 0,7-%-Gebühr
- Erste Umschichtung, sobald 252 gemeinsame Handelstage (X-12) bzw. 60 (X-1) vorliegen.

## 4. Akzeptanzkriterien

Identisch mit Modell K (`../06-fx-carry/docs/01_Vorregistrierung.md` §4):

**In-Sample, je Variante** (alle müssen erfüllt sein)

| # | Kriterium |
|---|---|
| 1 | Mittleres Netto-Tagesergebnis > 0 mit t-Wert ≥ **3,0** (kleinster aus iid, Woche, Monat) |
| 2 | ≥ 6 von 9 Jahren positiv |
| 3 | ≥ 60 % der gehandelten Instrumente (≥ 250 Positionstage) mit positivem Netto-Beitrag |
| 4 | Mittleres Tagesergebnis bei doppelten Kosten > 0 |

**Variantenwahl:** höherer t-Wert, falls beide bestehen. Besteht keine, ist **Strategie Nr. 7 gescheitert**, und der Hold-out bleibt unberührt.

**Beschreibend:** Zerlegung in Kurs, Swaps, Handel und Gebühr; Teilzeiträume 2015–2019 und 2020–2023; Häufigkeit der Währungen auf Long- und Short-Seite; Korrelation der Tagesergebnisse mit K-3 (Carry).

**Hold-out und FTMO:** wie Modell K.

## 5. Umsetzbarkeit als MT5-EA

- **Signal ohne externe Daten:** Formationsrenditen aus den D1-Kursen der 7 USD-Paare im EA. Den Zinsanteil liefern die Swap-Sätze der Paare (wie bei Nr. 6).
- **Ausführung:** einmal im Monat Marktorders auf die Zielgewichte, kein Stop. Das Risiko begrenzen der FtmoGuard und die Volatilitätsskalierung.

## 6. Trial-Log (Fortsetzung des globalen Logs)

| # | Test |
|---|---|
| T27 | X-1, In-Sample |
| T28 | X-12, In-Sample |
| T29 | Hold-out der gewählten Variante (nur falls T27 oder T28 besteht) |
| T30 | FTMO-Bootstrap (nur falls T29 besteht) |
