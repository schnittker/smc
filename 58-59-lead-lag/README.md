# Strategien Nr. 58 und 59 – Lead-Lag (US500 → AUDJPY, US-Renditen → USDJPY)

Teil der Testreihe `../STRATEGIEN.md`. Ziel ist ein autonomer MT5-EA für die FTMO 2-Step-Challenge (Swing, 100.000 USD). Feste Rahmenbedingungen: 10 % max. Verlust, 5 % max. Tagesverlust, Ziele +10 % / +5 %, News und Wochenende erlaubt.

**Idee:**
- **Nr. 58:** Nach einer US500-H1-Bewegung über 1,5σ wird AUDJPY für 3 Stunden in dieselbe Richtung gehandelt.
- **Nr. 59:** USDJPY wird in Richtung der Vortagesänderung bzw. des 20-Tage-Trends der 10-jährigen US-Rendite (FRED DGS10) gehandelt.

**Status (24.10.2026):** Vorregistrierung festgelegt, Test läuft.

| Dokument | Inhalt |
|---|---|
| [docs/00_Recherche.md](docs/00_Recherche.md) | Idee, Quellen, Daten, Erwartung |
| [docs/01_Vorregistrierung.md](docs/01_Vorregistrierung.md) | Regeln, Varianten, Akzeptanzkriterien, Trial-Log |

**Abhängigkeiten:** `../smart-money-concept` (`smc`), `../33-35-tagesausbruch` (`dbo`), `../36-38-h4-kanalausbruch` (`hkb`), `../50-51-sr-trendlinien` (`chart`), `../06-fx-carry` (`carry`); venv aus dem SMC-Projekt. Daten: `research/scripts/download_dgs10.sh`.

```sh
../smart-money-concept/research/.venv/bin/python -I research/scripts/run_ll.py                 # In-Sample (T210–T212)
../smart-money-concept/research/.venv/bin/python -I research/scripts/run_ll.py --holdout LL-AJ  # Hold-out, genau einmal
cd research && ../../smart-money-concept/research/.venv/bin/python -I -m pytest -q tests/       # Tests
```
