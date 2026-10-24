# Strategie Nr. 14 – Volatilitätsgesteuertes US500-Long

Teil der Testreihe `../STRATEGIEN.md`. Ziel ist ein autonomer MT5-EA für die FTMO 2-Step-Challenge (Swing, 100.000 USD). Feste Rahmenbedingungen: 10 % max. Verlust, 5 % max. Tagesverlust, Ziele +10 % / +5 %, News und Wochenende erlaubt.

**Idee:** US500 long halten, die Größe umgekehrt zur jüngsten Volatilität (V-VOL, täglich) bzw. Varianz des Vormonats (V-MM, monatlich) skaliert (Moreira & Muir 2017).

**Status (24.10.2026):** Vorregistrierung festgelegt, Test läuft.

| Dokument | Inhalt |
|---|---|
| [docs/00_Recherche.md](docs/00_Recherche.md) | Idee, Evidenz und Gegenevidenz, Erwartung |
| [docs/01_Vorregistrierung.md](docs/01_Vorregistrierung.md) | Regeln, Varianten, Akzeptanzkriterien, Trial-Log |

**Abhängigkeiten:** `../smart-money-concept` (`smc`) und `../06-fx-carry` (`carry`: Tagesbuchhaltung); venv aus dem SMC-Projekt.

```sh
../smart-money-concept/research/.venv/bin/python -I research/scripts/run_v.py                 # In-Sample (T48, T49)
../smart-money-concept/research/.venv/bin/python -I research/scripts/run_v.py --holdout V-VOL   # Hold-out, genau einmal
cd research && ../../smart-money-concept/research/.venv/bin/python -I -m pytest -q tests/       # Tests
```
