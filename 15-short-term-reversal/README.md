# Strategie Nr. 15 – Kurzfrist-Reversal US500 (Connors)

Teil der Testreihe `../STRATEGIEN.md`. Ziel ist ein autonomer MT5-EA für die FTMO 2-Step-Challenge (Swing, 100.000 USD). Feste Rahmenbedingungen: 10 % max. Verlust, 5 % max. Tagesverlust, Ziele +10 % / +5 %, News und Wochenende erlaubt.

**Idee:** Rücksetzer im Aufwärtstrend kaufen: RSI(2) < 10 bzw. 7-Tage-Tief über dem 200-Tage-Durchschnitt; Ausstieg nach der Erholung (Connors & Alvarez 2008).

**Status (24.10.2026): gescheitert.** R-RSI2 Sharpe 0,31 (t 0,78), R-7S 0,28 (t 0,83); US500 halten 0,51. Trefferquoten 70–77 % wie im Buch, aber zu wenig Ertrag. Hold-out unberührt.

| Dokument | Inhalt |
|---|---|
| [docs/00_Recherche.md](docs/00_Recherche.md) | Idee, Evidenz, Gegenargumente, Erwartung |
| [docs/01_Vorregistrierung.md](docs/01_Vorregistrierung.md) | Regeln, Varianten, Akzeptanzkriterien, Trial-Log |
| [docs/02_Ergebnisse_In-Sample.md](docs/02_Ergebnisse_In-Sample.md) | Ergebnis (gescheitert), Einordnung |
| [research/results/r_in_sample.md](research/results/r_in_sample.md) | Vollständige Tabellen des In-Sample-Laufs |

**Abhängigkeiten:** `../smart-money-concept` (`smc`), `../06-fx-carry` (`carry`: Tagesbuchhaltung); venv aus dem SMC-Projekt.

```sh
../smart-money-concept/research/.venv/bin/python -I research/scripts/run_r.py                  # In-Sample (T52, T53)
../smart-money-concept/research/.venv/bin/python -I research/scripts/run_r.py --holdout R-RSI2  # Hold-out, genau einmal
cd research && ../../smart-money-concept/research/.venv/bin/python -I -m pytest -q tests/       # Tests
```
