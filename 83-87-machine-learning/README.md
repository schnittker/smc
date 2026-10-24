# Strategien Nr. 83, 84, 86 (87, 88) – Machine Learning

Teil der Testreihe `../STRATEGIEN.md`. Ziel ist ein autonomer MT5-EA für die FTMO 2-Step-Challenge (Swing, 100.000 USD). Feste Rahmenbedingungen: 10 % max. Verlust, 5 % max. Tagesverlust, Ziele +10 % / +5 %, News und Wochenende erlaubt.

**Idee:** Walk-forward-Modelle, jährlich nur auf Vergangenheitsdaten trainiert, 17 Instrumente:
- Gradient Boosting auf H1-Merkmalen für die 6-Stunden-Richtung
- MLP auf 24 H1-Renditen (Ersatz für LSTM)
- Meta-Labeling der Supertrend-Signale auf H4

**Status (24.10.2026):** Vorregistrierung festgelegt, Test läuft.

| Dokument | Inhalt |
|---|---|
| [docs/00_Recherche.md](docs/00_Recherche.md) | Idee, Leckage-Schutz, Quellen, Nr. 87/88 |
| [docs/01_Vorregistrierung.md](docs/01_Vorregistrierung.md) | Regeln, Varianten, Akzeptanzkriterien, Trial-Log |

**Abhängigkeiten:** `../smart-money-concept` (`smc`; venv mit scikit-learn), `../33-35-tagesausbruch` (`dbo`), `../36-38-h4-kanalausbruch` (`hkb`), `../50-51-sr-trendlinien` (`chart`), `../61-76-trendindikatoren` (`tind`), `../65-75-oszillatoren` (`osc`).

```sh
../smart-money-concept/research/.venv/bin/python -I research/scripts/run_ml.py                   # In-Sample (T288–T290)
../smart-money-concept/research/.venv/bin/python -I research/scripts/run_ml.py --holdout ML-GBM   # Hold-out, genau einmal
cd research && ../../smart-money-concept/research/.venv/bin/python -I -m pytest -q tests/         # Tests
```
