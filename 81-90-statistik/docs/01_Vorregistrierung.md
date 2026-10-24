# Vorregistrierung: Modell ST „Statistische Modelle“ (Strategien Nr. 81, 82, 85, 90)

Festgelegt am 24.10.2026, **bevor** Code für dieses Modell geschrieben oder Daten dafür ausgewertet wurden. Änderungen nach diesem Commit zählen als neuer Versuch im Trial-Log (`../TRIAL_LOG.md`).

**Vorab festgehalten:** Die Tageskurse (Marke 16:50 New York bzw. Index-Marke Modell H) der 34 Instrumente aus Nr. 28/30 wurden für Trend- und Ausbruchsregeln ausgewertet. Monatsrenditen von Gold kamen indirekt in Nr. 3 und 29 vor. HMM-, GARCH- und k-NN-Modelle sowie eine Gold-Monatsregel wurden nicht angesehen.

## 0. Feste Rahmenbedingungen (für alle Strategien gleich)

- Expert Advisor für MetaTrader 5, handelt vollständig autonom
- FTMO 2-Step, Swing, 100.000 USD
- Max. Verlust gesamt 10 %, max. Tagesverlust 5 %
- Ziel Phase 1 +10 %, Ziel Phase 2 +5 %
- News-Trading und Halten übers Wochenende erlaubt

## 1. Hypothese

Jede der vier Regeln verdient nach Kosten mit t ≥ 3. **Erwartung vor dem Test: Scheitern aller vier.**

## 2. Daten, Universum, Kosten, Zeiträume

- **Tagesbuchhaltung** wie Nr. 28/30 (`carry.model.run_weights`): 25 FX-Paare und Gold (FX-Kostenmodell, Swaps mit 1 % Aufschlag) sowie 9 CFDs (Kostenmodell H). Positionen werden zur Tagesmarke gesetzt.
- Tagesrendite r(d) = ln p_mark(d) − ln p_mark(d−1)
- σ = EWMA-Volatilität wie Modell G
- **Modellschätzung** nur mit Daten vor dem jeweiligen Jahr (expandierendes Fenster ab 2014), danach fest für das Jahr
- **In-Sample:** 2015–2023, Kurse nur bis 31.12.2023. **Hold-out:** ab 2024, einmalig je bestandener Variante.

## 3. Regeln (Entscheidung zur Marke von Tag d, Position bis zur nächsten Änderung)

**ST-HMM (Nr. 81, 34 Instrumente)**
- Je Instrument und Jahr Y ein 2-Zustands-Gauss-HMM auf r(d) aller Tage 2014 … Y−1
- Baum-Welch mit 100 Iterationen; Start: Mittel 0, Varianzen = 0,5- bzw. 2-fache Stichprobenvarianz; Zustände nach Varianz geordnet
- Im Jahr Y wird die gefilterte Wahrscheinlichkeit p_ruhig(d) mit den festen Parametern fortgeschrieben
- **Signal:** sign(ln p_mark(d) − ln p_mark(d−20)), wenn p_ruhig(d) > 0,5; sonst 0
- **Gewicht** = Signal × 10 % / σ(d), gesetzt bei jeder Signaländerung

**ST-GARCH (Nr. 82, 34 Instrumente)**
- Je Instrument und Jahr Y ein GARCH(1,1) ohne Mittelwert, ML-Schätzung (L-BFGS-B) auf r(d) aller Tage 2014 … Y−1
- Im Jahr Y wird die bedingte Varianz fortgeschrieben; Prognose h(d+1)
- **Signal:** sign(20-Tage-Rendite)
- **Gewicht** = Signal × 10 % / √(252 × h(d+1)), gesetzt bei Signaländerung und am ersten Handelstag jeder Woche

**ST-KNN (Nr. 85, 34 Instrumente)**
- **Merkmale** an Tag t: r(t−9) … r(t), geteilt durch σ_tag(t) = σ(t)/√252
- **Ziel:** r(t+1)/σ_tag(t)
- **Trainingsmenge** an Tag d: alle Tage t ≥ 2014 mit t+1 ≤ d−1 und vollständigen Merkmalen
- **Prognose:** Mittel des Ziels über die k = 20 nächsten Nachbarn (euklidisch)
- **Signal:** sign(Prognose). **Gewicht** = Signal × 10 % / σ(d), gesetzt bei Signaländerung

**ST-GOLD (Nr. 90, XAUUSD)**
- Long von der Marke des letzten Handelstags im August bis zur Marke des letzten Handelstags im September
- ebenso Oktober → November
- sonst flat
- **Gewicht** = 10 % / σ zur Einstiegsmarke

## 4. Akzeptanzkriterien

Wie Nr. 28/30 (alle müssen erfüllt sein): t ≥ **3,0** (kleinster aus iid, Woche, Monat) bei positivem Mittel; ≥ 6 von 9 Jahren positiv; ≥ 60 % der Instrumente (mit ≥ 250 Positionstagen) positiv; doppelte Kosten > 0. Für ST-GOLD (Einzelinstrument) gilt statt der Instrumente-Regel: beide Teilzeiträume 2015–2019 und 2020–2023 positiv. Jede Variante wird für sich bewertet. Vor einem Hold-out gilt die Artefakt-Prüfung (Spielregel 6).

**Hold-out und FTMO:** wie Nr. 16.

## 5. Umsetzbarkeit als MT5-EA

Die Parameter von HMM und GARCH werden jährlich offline geschätzt und als Konstanten im EA hinterlegt. Die Fortschreibung läuft im EA. k-NN erfordert die Renditehistorie im EA (≈ 2.500 Tage × 34), das ist machbar. Es werden keine externen Daten benötigt.

## 6. Trial-Log (Fortsetzung des globalen Logs)

| # | Test |
|---|---|
| T276 | ST-HMM (Nr. 81), In-Sample |
| T277 | ST-GARCH (Nr. 82), In-Sample |
| T278 | ST-KNN (Nr. 85), In-Sample |
| T279 | ST-GOLD (Nr. 90), In-Sample |
| T280–T287 | Hold-out und FTMO je bestandener Variante |
