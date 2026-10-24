# Strategien Nr. 28 und Nr. 30 – Kanal-Ausbruch (52-Wochen-Hoch, Turtle)

Teil der Testreihe `../STRATEGIEN.md`. Ziel ist ein autonomer MT5-EA für die FTMO 2-Step-Challenge (Swing, 100.000 USD). Feste Rahmenbedingungen: 10 % max. Verlust, 5 % max. Tagesverlust, Ziele +10 % / +5 %, News und Wochenende erlaubt.

**Idee:** Ausbruch über das Hoch/Tief der letzten 252 Tage (B-52W, Nr. 28) bzw. 55 Tage (B-TURTLE, Nr. 30) über 34 Instrumente; Ausstieg beim Gegenausbruch eines kürzeren Kanals.

**Status (24.10.2026):** Vorregistrierung festgelegt, Test läuft.

| Dokument | Inhalt |
|---|---|
| [docs/00_Recherche.md](docs/00_Recherche.md) | Idee, Evidenz, eigene Vorbefunde, Erwartung |
| [docs/01_Vorregistrierung.md](docs/01_Vorregistrierung.md) | Regeln, Varianten, Akzeptanzkriterien, Trial-Log |

**Abhängigkeiten:** `../smart-money-concept` (`smc`), `../06-fx-carry` (`carry`); venv aus dem SMC-Projekt.

```sh
../smart-money-concept/research/.venv/bin/python -I research/scripts/run_b.py                 # In-Sample (T96, T97)
../smart-money-concept/research/.venv/bin/python -I research/scripts/run_b.py --holdout B-52W   # Hold-out, genau einmal
cd research && ../../smart-money-concept/research/.venv/bin/python -I -m pytest -q tests/       # Tests
```
