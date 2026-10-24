# Strategie Nr. 31 – London Breakout

Teil der Testreihe `../STRATEGIEN.md`. Ziel ist ein autonomer MT5-EA für die FTMO 2-Step-Challenge (Swing, 100.000 USD). Feste Rahmenbedingungen: 10 % max. Verlust, 5 % max. Tagesverlust, Ziele +10 % / +5 %, News und Wochenende erlaubt.

**Idee:** Ausbruch aus der Asien-Range (00:00–07:00 London) zwischen 07:00 und 12:00 handeln, Stop am anderen Ende der Range, Ausstieg spätestens 16:00; Risiko 0,5 % je Trade.

**Status (24.10.2026): gescheitert.** L-GBP +0,75 bp/Tag (t 0,47), L-EUR −1,46 bp/Tag (t −1,01); vor Kosten nur +0,02 bis +0,06 R je Trade. Hold-out unberührt.

| Dokument | Inhalt |
|---|---|
| [docs/00_Recherche.md](docs/00_Recherche.md) | Idee, Evidenz, Erwartung |
| [docs/01_Vorregistrierung.md](docs/01_Vorregistrierung.md) | Regeln, Varianten, Akzeptanzkriterien, Trial-Log |
| [docs/02_Ergebnisse_In-Sample.md](docs/02_Ergebnisse_In-Sample.md) | Ergebnis (gescheitert), Einordnung |
| [research/results/l_in_sample.md](research/results/l_in_sample.md) | Vollständige Tabellen des In-Sample-Laufs |

**Abhängigkeiten:** `../smart-money-concept` (`smc`), `../05-monatsend-rebalancing` (`mer`: Londoner Zeit); venv aus dem SMC-Projekt.

```sh
../smart-money-concept/research/.venv/bin/python -I research/scripts/run_l.py                 # In-Sample (T106, T107)
../smart-money-concept/research/.venv/bin/python -I research/scripts/run_l.py --holdout L-GBP   # Hold-out, genau einmal
cd research && ../../smart-money-concept/research/.venv/bin/python -I -m pytest -q tests/       # Tests
```
