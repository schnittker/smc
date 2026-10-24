# Strategie Nr. 16 – Opening Range Breakout 5 Minuten

Teil der Testreihe `../STRATEGIEN.md`. Ziel ist ein autonomer MT5-EA für die FTMO 2-Step-Challenge (Swing, 100.000 USD). Feste Rahmenbedingungen: 10 % max. Verlust, 5 % max. Tagesverlust, Ziele +10 % / +5 %, News und Wochenende erlaubt.

**Idee:** Richtung der ersten 5-Minuten-Kerze ab 09:30 New York handeln, Stop am Gegenende der Kerze, Ziel 10 R, Schluss um 16:00; Risiko 1 % je Trade (Zarattini & Aziz 2023).

**Status (24.10.2026):** Vorregistrierung festgelegt, Test läuft.

| Dokument | Inhalt |
|---|---|
| [docs/00_Recherche.md](docs/00_Recherche.md) | Idee, Evidenz, Gegenargumente, Erwartung |
| [docs/01_Vorregistrierung.md](docs/01_Vorregistrierung.md) | Regeln, Varianten, Akzeptanzkriterien, Trial-Log |

**Abhängigkeiten:** `../smart-money-concept` (`smc`), `../09-pre-fomc-drift` (`fomc`), `../10-turn-of-the-month` (`tom`), `../11-intraday-momentum` (`imom`); venv aus dem SMC-Projekt.

```sh
../smart-money-concept/research/.venv/bin/python -I research/scripts/run_o.py                 # In-Sample (T56, T57)
../smart-money-concept/research/.venv/bin/python -I research/scripts/run_o.py --holdout O-NDX   # Hold-out, genau einmal
cd research && ../../smart-money-concept/research/.venv/bin/python -I -m pytest -q tests/       # Tests
```
