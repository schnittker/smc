# Strategie Nr. 8 – FX Value (Kaufkraftparität)

Teil der Testreihe `../STRATEGIEN.md`. Ziel ist ein autonomer MT5-EA für die FTMO 2-Step-Challenge (Swing, 100.000 USD). Feste Rahmenbedingungen: 10 % max. Verlust, 5 % max. Tagesverlust, Ziele +10 % / +5 %, News und Wochenende erlaubt.

**Idee:** Die G8-Währungen werden monatlich nach dem realen Wechselkurs gerankt (CPI und Wechselkurse von FRED). Gekauft werden die billigsten, verkauft die teuersten. Das Ranking basiert entweder auf der 5-Jahres-Änderung oder auf der Abweichung vom Mittel seit 1999; Positionen wie Carry K-3. Nachgeholt, weil die CPI-Daten jetzt verfügbar sind.

**Status (24.10.2026):** Vorregistrierung festgelegt, Test läuft.

| Dokument | Inhalt |
|---|---|
| [docs/00_Recherche.md](docs/00_Recherche.md) | Idee, Quellen, Daten und Lücken |
| [docs/01_Vorregistrierung.md](docs/01_Vorregistrierung.md) | Regeln, Varianten, Akzeptanzkriterien, Trial-Log |

**Abhängigkeiten:** `../smart-money-concept` (`smc`), `../06-fx-carry` (`carry`); venv aus dem SMC-Projekt. Daten: `research/scripts/download_fred.sh`.

```sh
../smart-money-concept/research/.venv/bin/python -I research/scripts/run_v8.py                 # In-Sample (T299, T300)
../smart-money-concept/research/.venv/bin/python -I research/scripts/run_v8.py --holdout V-5Y   # Hold-out, genau einmal
cd research && ../../smart-money-concept/research/.venv/bin/python -I -m pytest -q tests/       # Tests
```
