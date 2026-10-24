# Strategie Nr. 31 – London Breakout

Teil der Testreihe `../STRATEGIEN.md`. Ziel ist ein autonomer MT5-EA für die FTMO 2-Step-Challenge (Swing, 100.000 USD). Feste Rahmenbedingungen: 10 % max. Verlust, 5 % max. Tagesverlust, Ziele +10 % / +5 %, News und Wochenende erlaubt.

**Idee:** Ausbruch aus der Asien-Range (00:00–07:00 London) zwischen 07:00 und 12:00 handeln, Stop am anderen Ende der Range, Ausstieg spätestens 16:00; Risiko 0,5 % je Trade.

**Status (24.10.2026):** Vorregistrierung festgelegt, Test läuft.

| Dokument | Inhalt |
|---|---|
| [docs/00_Recherche.md](docs/00_Recherche.md) | Idee, Evidenz, Erwartung |
| [docs/01_Vorregistrierung.md](docs/01_Vorregistrierung.md) | Regeln, Varianten, Akzeptanzkriterien, Trial-Log |

**Abhängigkeiten:** `../smart-money-concept` (`smc`), `../05-monatsend-rebalancing` (`mer`: Londoner Zeit); venv aus dem SMC-Projekt.

```sh
../smart-money-concept/research/.venv/bin/python -I research/scripts/run_l.py                 # In-Sample (T106, T107)
../smart-money-concept/research/.venv/bin/python -I research/scripts/run_l.py --holdout L-GBP   # Hold-out, genau einmal
cd research && ../../smart-money-concept/research/.venv/bin/python -I -m pytest -q tests/       # Tests
```
