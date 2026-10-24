# Strategien Nr. 36 und 38 – H4-Kanal-Ausbruch (Bollinger Squeeze, Keltner-Channel)

Teil der Testreihe `../STRATEGIEN.md`. Ziel ist ein autonomer MT5-EA für die FTMO 2-Step-Challenge (Swing, 100.000 USD). Feste Rahmenbedingungen: 10 % max. Verlust, 5 % max. Tagesverlust, Ziele +10 % / +5 %, News und Wochenende erlaubt.

**Idee:** H4-Schluss außerhalb der Bollinger-Bänder nach einem Bandbreiten-Tief bzw. außerhalb EMA20 ± 2 ATR in Richtung EMA200. Ausstieg an der Mittellinie, Stop 2 ATR, 17 Instrumente.

**Status (24.10.2026):** Vorregistrierung festgelegt, Test läuft.

| Dokument | Inhalt |
|---|---|
| [docs/00_Recherche.md](docs/00_Recherche.md) | Idee, Quellen, Erwartung |
| [docs/01_Vorregistrierung.md](docs/01_Vorregistrierung.md) | Regeln, Varianten, Akzeptanzkriterien, Trial-Log |

**Abhängigkeiten:** `../smart-money-concept` (`smc`), `../33-35-tagesausbruch` (`dbo`, Universum und Kosten); venv aus dem SMC-Projekt.

```sh
../smart-money-concept/research/.venv/bin/python -I research/scripts/run_k.py                  # In-Sample (T123, T124)
../smart-money-concept/research/.venv/bin/python -I research/scripts/run_k.py --holdout K-BBSQ   # Hold-out, genau einmal
cd research && ../../smart-money-concept/research/.venv/bin/python -I -m pytest -q tests/        # Tests
```
