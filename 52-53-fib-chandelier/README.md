# Strategien Nr. 52 und 53 – Fibonacci-Pullback und Chandelier-Trailing-Trend

Teil der Testreihe `../STRATEGIEN.md`. Ziel ist ein autonomer MT5-EA für die FTMO 2-Step-Challenge (Swing, 100.000 USD). Feste Rahmenbedingungen: 10 % max. Verlust, 5 % max. Tagesverlust, Ziele +10 % / +5 %, News und Wochenende erlaubt.

**Idee:**
- **Nr. 52:** Einstieg im 50–61,8-%-Rücklauf eines H4-Impulses (≥ 3 ATR), Stop unter dem Impulsursprung, Ziel am Impulsextrem.
- **Nr. 53:** 55-Tage-Ausbruch auf D1, Ausstieg nur über den Chandelier-Trailing-Stop (HH − 3 ATR22).
- Beide auf 17 Instrumenten.

**Status (24.10.2026):** Vorregistrierung festgelegt, Test läuft.

| Dokument | Inhalt |
|---|---|
| [docs/00_Recherche.md](docs/00_Recherche.md) | Idee, Quellen, Erwartung |
| [docs/01_Vorregistrierung.md](docs/01_Vorregistrierung.md) | Regeln, Varianten, Akzeptanzkriterien, Trial-Log |

**Abhängigkeiten:** `../smart-money-concept` (`smc`), `../33-35-tagesausbruch` (`dbo`), `../36-38-h4-kanalausbruch` (`hkb`), `../50-51-sr-trendlinien` (`chart`); venv aus dem SMC-Projekt.

```sh
../smart-money-concept/research/.venv/bin/python -I research/scripts/run_fc.py                   # In-Sample (T183, T184)
../smart-money-concept/research/.venv/bin/python -I research/scripts/run_fc.py --holdout FC-FIB   # Hold-out, genau einmal
cd research && ../../smart-money-concept/research/.venv/bin/python -I -m pytest -q tests/         # Tests
```
