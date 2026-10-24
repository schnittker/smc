# Strategie Nr. 22 – Gold/Silber-Ratio

Teil der Testreihe `../STRATEGIEN.md`. Ziel ist ein autonomer MT5-EA für die FTMO 2-Step-Challenge (Swing, 100.000 USD). Feste Rahmenbedingungen: 10 % max. Verlust, 5 % max. Tagesverlust, Ziele +10 % / +5 %, News und Wochenende erlaubt.

**Idee:** Bei extremer Gold/Silber-Ratio (z-Score ≥ 2 über 60 bzw. 250 Tage) gegen die Ratio handeln: Long Silber / Short Gold bzw. umgekehrt, bis die Ratio zum Mittel zurückkehrt.

**Status (24.10.2026): gescheitert.** G-60 Sharpe −0,07 (t −0,22), G-250 0,09 (t 0,25, nur 10 Trades). Hold-out unberührt.

| Dokument | Inhalt |
|---|---|
| [docs/00_Recherche.md](docs/00_Recherche.md) | Idee, Evidenz, Gegenargumente, Erwartung |
| [docs/01_Vorregistrierung.md](docs/01_Vorregistrierung.md) | Regeln, Varianten, Akzeptanzkriterien, Trial-Log |
| [docs/02_Ergebnisse_In-Sample.md](docs/02_Ergebnisse_In-Sample.md) | Ergebnis (gescheitert), Einordnung |
| [research/results/g_in_sample.md](research/results/g_in_sample.md) | Vollständige Tabellen des In-Sample-Laufs |

**Abhängigkeiten:** `../smart-money-concept` (`smc`), `../06-fx-carry` (`carry`), `../21-pairs-mean-reversion` (`pmr`: z-Score, Trade-Liste); venv aus dem SMC-Projekt.

```sh
../smart-money-concept/research/.venv/bin/python -I research/scripts/run_g.py                 # In-Sample (T76, T77)
../smart-money-concept/research/.venv/bin/python -I research/scripts/run_g.py --holdout G-60    # Hold-out, genau einmal
cd research && ../../smart-money-concept/research/.venv/bin/python -I -m pytest -q tests/       # Tests
```
