# Vorregistrierung: Modell ML „Machine Learning“ (Strategien Nr. 83, 84, 86)

Festgelegt am 24.10.2026, **bevor** Code für dieses Modell geschrieben oder Daten dafür ausgewertet wurden. Änderungen nach diesem Commit zählen als neuer Versuch im Trial-Log (`../TRIAL_LOG.md`).

**Vorab festgehalten:** H1- und H4-Daten der 17 Instrumente wurden mit vielen Einzelregeln ausgewertet (Nr. 33–80). Die hier verwendeten Merkmale sind Kombinationen daraus. Die Supertrend-Basis (Nr. 71) wurde In-Sample ausgewertet (T225: vor Kosten +0,021 R je Trade). Das Meta-Modell lernt aber nur aus Trainingsjahren vor dem jeweiligen Jahr.

## 0. Feste Rahmenbedingungen (für alle Strategien gleich)

- Expert Advisor für MetaTrader 5, handelt vollständig autonom
- FTMO 2-Step, Swing, 100.000 USD
- Max. Verlust gesamt 10 %, max. Tagesverlust 5 %
- Ziel Phase 1 +10 %, Ziel Phase 2 +5 %
- News-Trading und Halten übers Wochenende erlaubt

## 1. Hypothese

Jedes der drei Modelle verdient nach Kosten mit t ≥ 3. **Erwartung vor dem Test: Scheitern aller drei.**

## 2. Daten, Universum, Kosten, Zeiträume

- **Daten:** H1- bzw. H4-Serverkerzen der 17 Instrumente
- **Kosten und Swaps:** wie Nr. 36/38
- **Training:** walk-forward. Das Modell für Jahr Y wird nur auf Daten 2014 … Y−1 trainiert; Labels, deren Zielfenster in Jahr Y reicht, werden verworfen.
- **Feste Hyperparameter**, Zufallszustand 0
- **In-Sample:** Einstiege 2015–2023. **Hold-out:** ab 2024 (Modelle für 2024–2026 dürfen die In-Sample-Jahre zum Training nutzen), einmalig je bestandener Variante.

## 3. Regeln

**Merkmale H1 (ML-GBM) am Schluss der Kerze i**
- s = Standardabweichung der 1-Kerzen-Log-Renditen über 500 Kerzen
- Log-Renditen über 1, 3, 6, 12, 24, 48 Kerzen, je durch s · √n geteilt
- RSI14
- Abstand von C zu EMA20 und zu EMA100 in Einheiten von s · √20 bzw. s · √100
- Volatilitätsverhältnis σ24 / σ500
- Lage von C in der 24-Kerzen-Spanne (0–1)
- Uhrzeit London als sin/cos, Wochentag
- Anlageklasse (0 FX, 1 Metall, 2 Index, 3 Öl)

**Label (ML-GBM, ML-MLP):** 1, wenn O(i+7) > O(i+1), sonst 0; Zielfenster = 6 Kerzen ab der nächsten Eröffnung. Trainiert wird nur auf jeder 6. Kerze, damit sich die Label-Fenster nicht überlappen.

| Variante | Nr. | Modell | Eingaben |
|---|---|---|---|
| **ML-GBM** | 83 | HistGradientBoostingClassifier (max_iter 200, learning_rate 0,05, max_leaf_nodes 15, l2 1,0) | Merkmale H1 |
| **ML-MLP** | 86 | MLPClassifier (Schichten 32/16, ReLU, alpha 1e-3, early_stopping, max_iter 200) | die letzten 24 1-Kerzen-Renditen / s |

**Handel ML-GBM / ML-MLP (H1)**
- p = vorhergesagte Wahrscheinlichkeit „aufwärts“; p > 0,55 → Long, p < 0,45 → Short zur Eröffnung von i+1
- **Ausstieg** zur Eröffnung nach 6 gehaltenen Kerzen
- **Stop:** fest 2 × ATR14_H1, intrabar

**ML-META (Nr. 84, H4)**
- **Basis:** Supertrend-Zustandswechsel wie TI-SUPER (Nr. 71, Stop-and-Reverse, Notfall-Stop 3 ATR)
- **Meta-Label** eines Basis-Trades = 1, wenn sein Netto-Ergebnis > 0
- **Meta-Modell:** HistGradientBoostingClassifier (wie ML-GBM) auf den H4-Merkmalen zum Signalbar (dieselben Definitionen auf H4; ohne Uhrzeit, mit Wochentag), dazu die Basis-Richtung als Merkmal
- **Trainiert** auf den Basis-Trades der Jahre bis Y−1, deren Ausstieg vor dem 1.1. des Jahres Y liegt
- **Im Jahr Y** wird ein Basis-Einstieg nur genommen, wenn p > 0,55. Sonst bleibt das Instrument bis zum nächsten Zustandswechsel flat.

**Gemeinsam**
- Je Instrument höchstens eine Position; ein neues Signal frühestens am Schluss der Kerze nach dem Ausstieg (ML-META: Basisregel)
- Keine neuen Einstiege an Servertagen 24.12.–01.01.
- **Größe:** Nominal = min(0,25 % Kapital / (Stop-Abstand / Kurs), 10 × Kapital)
- **Portfolio:** Summe aller Instrumente; Ergebnis am Servertag des Ausstiegs

## 4. Akzeptanzkriterien

Wie Nr. 33–80 (alle müssen erfüllt sein): t ≥ **3,0** (kleinster aus iid, Woche, Monat) bei positivem Mittel; ≥ 6 von 9 Jahren positiv; ≥ 60 % der Instrumente positiv; doppelte Kosten > 0. Jede Variante wird für sich bewertet. Vor einem Hold-out gilt die Artefakt-Prüfung (Spielregel 6).

**Beschreibend:** Treffergüte der Prognosen (AUC und Trefferquote je Jahr out-of-sample), Trades, Ø R vor und nach Kosten.

**Hold-out und FTMO:** wie Nr. 16.

## 5. Umsetzbarkeit als MT5-EA

Trainierte Modelle lassen sich als ONNX exportieren und in MT5 ausführen (`OnnxRun`). Die Merkmale sind Standard-Indikatoren. Es werden keine externen Daten benötigt.

## 6. Trial-Log (Fortsetzung des globalen Logs)

| # | Test |
|---|---|
| T288 | ML-GBM (Nr. 83), In-Sample |
| T289 | ML-META (Nr. 84), In-Sample |
| T290 | ML-MLP (Nr. 86), In-Sample |
| T291–T296 | Hold-out und FTMO je bestandener Variante |

Nr. 87 (RL) wird nach diesem Test entschieden; Nr. 88 (GP) wird nicht getestet (⛔, siehe Recherche).
