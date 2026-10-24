# Strategie Nr. 29 – Dual Momentum

Teil der Testreihe `../STRATEGIEN.md`. Ziel ist ein autonomer MT5-EA für die FTMO 2-Step-Challenge (Swing, 100.000 USD). Feste Rahmenbedingungen: 10 % max. Verlust, 5 % max. Tagesverlust, Ziele +10 % / +5 %, News und Wochenende erlaubt.

**Idee:** Monatlich die Anlage(n) mit der höchsten 12-Monats-Rendite aus 7 Aktienindizes und Gold halten, nur wenn die Rendite über dem USD-Zins liegt (Antonacci 2014).

**Status (24.10.2026): gescheitert.** D-TOP1 Sharpe 0,17 (t 0,48), D-TOP2 0,14 (t 0,38); unter dem bloßen Halten von US100. Hold-out unberührt.

| Dokument | Inhalt |
|---|---|
| [docs/00_Recherche.md](docs/00_Recherche.md) | Idee, Evidenz, Gegenargumente, Erwartung |
| [docs/01_Vorregistrierung.md](docs/01_Vorregistrierung.md) | Regeln, Varianten, Akzeptanzkriterien, Trial-Log |
| [docs/02_Ergebnisse_In-Sample.md](docs/02_Ergebnisse_In-Sample.md) | Ergebnis (gescheitert), Einordnung |
| [research/results/d_in_sample.md](research/results/d_in_sample.md) | Vollständige Tabellen des In-Sample-Laufs |

**Abhängigkeiten:** `../smart-money-concept` (`smc`), `../06-fx-carry` (`carry`); venv aus dem SMC-Projekt.

```sh
../smart-money-concept/research/.venv/bin/python -I research/scripts/run_d.py                  # In-Sample (T102, T103)
../smart-money-concept/research/.venv/bin/python -I research/scripts/run_d.py --holdout D-TOP1   # Hold-out, genau einmal
cd research && ../../smart-money-concept/research/.venv/bin/python -I -m pytest -q tests/        # Tests
```
