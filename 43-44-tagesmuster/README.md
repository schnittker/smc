# Strategien Nr. 43 und 44 – Tagesmuster (große Tagesbewegung, Wochentags-Effekt)

Teil der Testreihe `../STRATEGIEN.md`. Ziel ist ein autonomer MT5-EA für die FTMO 2-Step-Challenge (Swing, 100.000 USD). Feste Rahmenbedingungen: 10 % max. Verlust, 5 % max. Tagesverlust, Ziele +10 % / +5 %, News und Wochenende erlaubt.

**Idee:** Nach einem Tag mit mehr als 2 ATR wird am Folgetag gegen bzw. mit der Bewegung gehandelt (Nr. 43). Alternativ wird an einem rollierend gewählten Wochentag gehandelt (Nr. 44). Die Position läuft jeweils von der Eröffnung bis zum Schluss des Servertags, die Größe ist ATR-skaliert, 17 Instrumente.

**Status (24.10.2026):** Vorregistrierung festgelegt, Test läuft.

| Dokument | Inhalt |
|---|---|
| [docs/00_Recherche.md](docs/00_Recherche.md) | Idee, Quellen, Erwartung |
| [docs/01_Vorregistrierung.md](docs/01_Vorregistrierung.md) | Regeln, Varianten, Akzeptanzkriterien, Trial-Log |

**Abhängigkeiten:** `../smart-money-concept` (`smc`), `../33-35-tagesausbruch` (`dbo`), `../36-38-h4-kanalausbruch` (`hkb`); venv aus dem SMC-Projekt.

```sh
../smart-money-concept/research/.venv/bin/python -I research/scripts/run_e.py                 # In-Sample (T144–T146)
../smart-money-concept/research/.venv/bin/python -I research/scripts/run_e.py --holdout E-REV   # Hold-out, genau einmal
cd research && ../../smart-money-concept/research/.venv/bin/python -I -m pytest -q tests/       # Tests
```
