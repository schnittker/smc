# Strategien Nr. 54, 55 und 60 – Price Action (Candlesticks an Levels, Doppeltop/-boden, Supply/Demand)

Teil der Testreihe `../STRATEGIEN.md`. Ziel ist ein autonomer MT5-EA für die FTMO 2-Step-Challenge (Swing, 100.000 USD). Feste Rahmenbedingungen: 10 % max. Verlust, 5 % max. Tagesverlust, Ziele +10 % / +5 %, News und Wochenende erlaubt.

**Idee:** H4, 17 Instrumente:
- Pin Bar bzw. Engulfing an S/R-Zonen aus Nr. 50
- Doppelboden/-top mit Nackenlinienbruch und Measured-Move-Ziel
- erster Rücklauf in eine Basis-Impuls-Zone (Supply/Demand)

Stop hinter dem Muster (≥ 1 ATR), Ziel 2R bzw. Measured Move, Zeitstopp 30 Kerzen.

**Status (24.10.2026):** Vorregistrierung festgelegt, Test läuft.

| Dokument | Inhalt |
|---|---|
| [docs/00_Recherche.md](docs/00_Recherche.md) | Idee, Quellen, Erwartung |
| [docs/01_Vorregistrierung.md](docs/01_Vorregistrierung.md) | Regeln, Varianten, Akzeptanzkriterien, Trial-Log |

**Abhängigkeiten:** `../smart-money-concept` (`smc`), `../33-35-tagesausbruch` (`dbo`), `../36-38-h4-kanalausbruch` (`hkb`), `../50-51-sr-trendlinien` (`chart`); venv aus dem SMC-Projekt.

```sh
../smart-money-concept/research/.venv/bin/python -I research/scripts/run_pa.py                   # In-Sample (T189–T192)
../smart-money-concept/research/.venv/bin/python -I research/scripts/run_pa.py --holdout PA-PIN   # Hold-out, genau einmal
cd research && ../../smart-money-concept/research/.venv/bin/python -I -m pytest -q tests/         # Tests
```
