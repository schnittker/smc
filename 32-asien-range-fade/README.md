# Strategie Nr. 32 – Asien-Range-Fade („Nachtscalper“)

Teil der Testreihe `../STRATEGIEN.md`. Ziel ist ein autonomer MT5-EA für die FTMO 2-Step-Challenge (Swing, 100.000 USD). Feste Rahmenbedingungen: 10 % max. Verlust, 5 % max. Tagesverlust, Ziele +10 % / +5 %, News und Wochenende erlaubt.

**Idee:** In der Asien-Session (00:00–06:00 London) Ausschläge über die M5-Bollinger-Bänder (20, 2) faden, Ausstieg an der Mittellinie; EURCHF und AUDCAD.

**Status (24.10.2026):** Vorregistrierung festgelegt, Test läuft.

| Dokument | Inhalt |
|---|---|
| [docs/00_Recherche.md](docs/00_Recherche.md) | Idee, Evidenz, Erwartung |
| [docs/01_Vorregistrierung.md](docs/01_Vorregistrierung.md) | Regeln, Varianten, Akzeptanzkriterien, Trial-Log |

**Abhängigkeiten:** `../smart-money-concept` (`smc`), `../05-monatsend-rebalancing` (`mer`), `../31-london-breakout` (Auswertung); venv aus dem SMC-Projekt.

```sh
../smart-money-concept/research/.venv/bin/python -I research/scripts/run_a.py                    # In-Sample (T110, T111)
../smart-money-concept/research/.venv/bin/python -I research/scripts/run_a.py --holdout A-EURCHF   # Hold-out, genau einmal
cd research && ../../smart-money-concept/research/.venv/bin/python -I -m pytest -q tests/          # Tests
```
