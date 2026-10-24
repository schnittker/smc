# Strategie Nr. 14 – Volatilitätsgesteuertes US500-Long

Teil der Testreihe `../STRATEGIEN.md`. Ziel ist ein autonomer MT5-EA für die FTMO 2-Step-Challenge (Swing, 100.000 USD). Feste Rahmenbedingungen: 10 % max. Verlust, 5 % max. Tagesverlust, Ziele +10 % / +5 %, News und Wochenende erlaubt.

**Idee:** US500 long halten, die Größe umgekehrt zur jüngsten Volatilität (V-VOL, täglich) bzw. Varianz des Vormonats (V-MM, monatlich) skaliert (Moreira & Muir 2017).

**Status (24.10.2026): gescheitert.** V-VOL Sharpe 0,56 (t 1,68), V-MM 0,32 (t 0,96); US500 halten 0,51. Die Steuerung senkt den Drawdown (23 % → 16 % bei 10 % Vol.), nicht aber die Sharpe-Lücke zu 1,0. Hold-out unberührt.

| Dokument | Inhalt |
|---|---|
| [docs/00_Recherche.md](docs/00_Recherche.md) | Idee, Evidenz und Gegenevidenz, Erwartung |
| [docs/01_Vorregistrierung.md](docs/01_Vorregistrierung.md) | Regeln, Varianten, Akzeptanzkriterien, Trial-Log |
| [docs/02_Ergebnisse_In-Sample.md](docs/02_Ergebnisse_In-Sample.md) | Ergebnis (gescheitert), Einordnung, Referenz Index halten |
| [research/results/v_in_sample.md](research/results/v_in_sample.md) | Vollständige Tabellen des In-Sample-Laufs |

**Abhängigkeiten:** `../smart-money-concept` (`smc`) und `../06-fx-carry` (`carry`: Tagesbuchhaltung); venv aus dem SMC-Projekt.

```sh
../smart-money-concept/research/.venv/bin/python -I research/scripts/run_v.py                 # In-Sample (T48, T49)
../smart-money-concept/research/.venv/bin/python -I research/scripts/run_v.py --holdout V-VOL   # Hold-out, genau einmal
cd research && ../../smart-money-concept/research/.venv/bin/python -I -m pytest -q tests/       # Tests
```
