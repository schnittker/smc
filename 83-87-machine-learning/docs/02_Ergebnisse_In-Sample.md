# Ergebnisse Strategien Nr. 83, 84, 86 – Modell ML „Machine Learning“ (Nr. 87 ⊘, Nr. 88 ⛔)

Stand: 24.10.2026

Grundlagen:
- Regeln: unverändert aus der Vorregistrierung `docs/01_Vorregistrierung.md` (Commit `2304ee7`)
- Code: `research/mlx/`, Lauf `research/scripts/run_ml.py`; 2 Tests grün (u. a. keine Prognosegüte auf reinem Rauschen)
- In-Sample: Einstiege 2015–2023, 17 Instrumente, Modelle jährlich walk-forward trainiert
- Vollständige Tabellen: `research/results/ml_in_sample.md`

## 1. Ergebnis

**Alle drei Modelle sind nach Kosten negativ. Die Strategien Nr. 83, 84 und 86 sind damit gescheitert.** Der Hold-out bleibt unberührt, T291–T296 entfallen.

| Variante | Nr. | TF | Trades | Netto bp/Tag | vor Kosten bp/Tag | Ø R vor / nach Kosten | t | Jahre + | Instr. + |
|---|---|---|---|---|---|---|---|---|---|
| ML-GBM | 83 | H1 | 29.512 | −9,10 | +9,31 | +0,030 / −0,029 | −4,64 | 1 | 4 |
| ML-META | 84 | H4 | 344 | −0,24 | −0,10 | −0,028 / −0,065 | −0,99 | 3 | 5 |
| ML-MLP | 86 | H1 | 67.350 | −39,74 | +0,96 | +0,001 / −0,055 | −13,37 | 0 | 0 |

**Prognosegüte out-of-sample (gepoolt, alle H1-Kerzen, 6-Stunden-Richtung)**

| Modell | AUC 2015–2023 (je Jahr) | Trefferquote |
|---|---|---|
| ML-GBM | 0,514–0,525, in allen 9 Jahren > 0,51 | 51,0–52,3 % |
| ML-MLP | 0,501–0,508 | 50,0–51,3 % |

## 2. Einordnung

- **Gradient Boosting:** Das Modell hat eine kleine, aber in allen 9 Jahren stabile Vorhersagekraft (AUC ≈ 0,52). Das ist der stabilste Prognose-Befund der ganzen Reihe. Vor Kosten bringt es +0,030 R je Trade und +9,3 bp je Tag. Bei 6-Stunden-Haltedauer und rund 3.300 Trades pro Jahr fressen die Kosten das Doppelte davon.
- **Vorsicht bei der Deutung:** Die Merkmale enthalten Uhrzeit und Wochentag. Das Modell kann damit auch das HistData-Artefakt der ersten Wochenkerze aus Nr. 42 lernen. Die Stabilität ist also kein Beleg für einen handelbaren Effekt.
- **MLP auf Renditefenstern:** praktisch keine Prognosegüte (AUC ≈ 0,505). Reine Renditesequenzen enthalten auf H1 keine nutzbare Information.
- **Meta-Labeling:** Der Filter lässt nur 344 Supertrend-Trades durch (9 Jahre), und diese sind vor Kosten negativ. Das Modell erkennt die Gewinner-Trades nicht.
- **Folgerung für Nr. 87 (Reinforcement Learning) → ⊘:** Ein Agent auf denselben Merkmalen hätte dieselbe Informationsbasis (AUC ≤ 0,52) und dieselben Kosten. Er kann daraus keinen Netto-Edge lernen, und ein Test würde nur Freiheitsgrade hinzufügen.
- **Nr. 88 (Genetic Programming) → ⛔:** siehe Recherche (Trial-Log-Prinzip).
- **Möglicher späterer Ansatz** (nicht Teil dieses Tests, nur mit eigener Vorregistrierung): die GBM-Prognose ohne Uhrzeitmerkmale und mit längerem Horizont (D1) als Filter für eine Strategie mit wenig Umsatz.

## 3. Trial-Log (Fortsetzung)

| # | Datum | Test | Ergebnis |
|---|---|---|---|
| T288 | 24.10.2026 | ML-GBM (83), In-Sample | nicht bestanden: −9,10 bp/Tag, t −4,64 (vor Kosten +9,3) |
| T289 | 24.10.2026 | ML-META (84), In-Sample | nicht bestanden: −0,24 bp/Tag, t −0,99 |
| T290 | 24.10.2026 | ML-MLP (86), In-Sample | nicht bestanden: −39,7 bp/Tag, t −13,4 |
| T291–T296 | – | Hold-out, FTMO | entfallen, Hold-out unberührt |
