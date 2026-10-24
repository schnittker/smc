# Strategien Nr. 61–64, 69–73, 76 – Klassische Trendindikatoren

Teil der Testreihe `../STRATEGIEN.md`. Ziel ist ein autonomer MT5-EA für die FTMO 2-Step-Challenge (Swing, 100.000 USD). Feste Rahmenbedingungen: 10 % max. Verlust, 5 % max. Tagesverlust, Ziele +10 % / +5 %, News und Wochenende erlaubt.

**Idee:** Zehn Trendindikatoren als Stop-and-Reverse-Regeln mit Notfall-Stop 3 ATR auf 17 Instrumenten:
- D1: SMA 50/200
- H1: EMA 9/21
- H4: Triple MA, MACD, ADX/DMI, Parabolic SAR, Supertrend, Ichimoku, Heikin-Ashi, Kalman-Trend

**Status (24.10.2026):** Vorregistrierung festgelegt, Test läuft.

| Dokument | Inhalt |
|---|---|
| [docs/00_Recherche.md](docs/00_Recherche.md) | Idee, Quellen, Erwartung |
| [docs/01_Vorregistrierung.md](docs/01_Vorregistrierung.md) | Regeln, Varianten, Akzeptanzkriterien, Trial-Log |

**Abhängigkeiten:** `../smart-money-concept` (`smc`), `../33-35-tagesausbruch` (`dbo`), `../36-38-h4-kanalausbruch` (`hkb`), `../50-51-sr-trendlinien` (`chart`); venv aus dem SMC-Projekt.

```sh
../smart-money-concept/research/.venv/bin/python -I research/scripts/run_ti.py                    # In-Sample (T219–T228)
../smart-money-concept/research/.venv/bin/python -I research/scripts/run_ti.py --holdout TI-MACD   # Hold-out, genau einmal
cd research && ../../smart-money-concept/research/.venv/bin/python -I -m pytest -q tests/          # Tests
```
