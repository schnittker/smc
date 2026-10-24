# Recherche: Machine Learning (Nr. 83 Gradient Boosting, 84 Meta-Labeling, 86 Sequenzmodell, 87 RL, 88 GP)

Stand: 24.10.2026

## 1. Idee

| Nr. | Ansatz | Umsetzung hier |
|---|---|---|
| 83 | Gradient Boosting sagt die Richtung der nächsten n Kerzen voraus | `HistGradientBoostingClassifier`, H1, 6-Stunden-Richtung, gepoolt über 17 Instrumente |
| 84 | Meta-Labeling (López de Prado 2018): ein ML-Modell filtert die Signale einer Basisstrategie | Basis Supertrend H4 (Nr. 71, bester Trendindikator vor Kosten); GBM sagt voraus, ob ein Trade gewinnt |
| 86 | LSTM/Transformer auf Renditesequenzen | **Ersatz:** mehrschichtiges Perzeptron (MLP) auf den letzten 24 normierten H1-Renditen. torch ist nicht installiert, und ein LSTM würde die Rechenzeit vervielfachen. Das Sequenz-Prinzip bleibt erhalten (Fenster statt Rekurrenz). |
| 87 | Reinforcement Learning | Wird erst nach Nr. 83/86 entschieden: Haben dieselben Merkmale keine Vorhersagekraft, kann ein Agent daraus keinen Edge lernen (⊘). |
| 88 | Genetic Programming | **⛔ nicht getestet:** Automatische Regelsuche über Tausende Kandidaten verletzt das Trial-Log-Prinzip (Spielregel 1). Jede Kandidatenregel wäre ein eigener Versuch. |

## 2. Evidenz

| Quelle | Inhalt |
|---|---|
| Gu, Kelly & Xiu (2020), *RFS* | ML (Bäume, Netze) verbessert Aktien-Renditeprognosen im Querschnitt; Zeitreihen-Prognosen einzelner Märkte bleiben schwach |
| López de Prado (2018), *Advances in Financial ML* | Meta-Labeling, Triple Barrier, Purging gegen Leckage |
| Bailey et al. (2014) | Hohes Overfitting-Risiko bei ML-Backtests |
| Fischer & Krauss (2018) | LSTM auf S&P-500-Aktien vor Kosten positiv, nach 2010 stark abnehmend |

## 3. Schutz gegen Leckage

- Training jährlich nur mit Daten bis zum Vorjahresende. Die letzten Labels werden abgeschnitten, damit sich die Zielfenster nicht überlappen.
- Alle Merkmale stammen aus abgeschlossenen Kerzen.
- Feste Hyperparameter, kein Tuning auf In-Sample-Ergebnisse.

## 4. Einschätzung vor dem Test

Alle Bausteine dieser Merkmale (Momentum, Umkehr, Volatilität, Uhrzeit) waren einzeln ohne Netto-Edge. **Erwartung: Scheitern aller drei.**
