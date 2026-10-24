# Strategie Nr. 26 – Pre-Holiday US-Indizes

Teil der Testreihe `../STRATEGIEN.md`. Ziel ist ein autonomer MT5-EA für die FTMO 2-Step-Challenge (Swing, 100.000 USD). Feste Rahmenbedingungen: 10 % max. Verlust, 5 % max. Tagesverlust, Ziele +10 % / +5 %, News und Wochenende erlaubt.

**Idee:** Long US500 bzw. US100 über den letzten Handelstag vor einem NYSE-Feiertag (Ariel 1990).

**Status (24.10.2026): gescheitert.** H-SPX +13,9 bp je Ereignis (t 1,68), H-NDX +10,6 bp (t 0,88). Hold-out unberührt.

| Dokument | Inhalt |
|---|---|
| [docs/00_Recherche.md](docs/00_Recherche.md) | Effekt, Evidenz, Erwartung |
| [docs/01_Vorregistrierung.md](docs/01_Vorregistrierung.md) | Regeln, Varianten, Akzeptanzkriterien, Trial-Log |
| [docs/02_Ergebnisse_In-Sample.md](docs/02_Ergebnisse_In-Sample.md) | Ergebnis (gescheitert), Einordnung |
| [research/results/h_in_sample.md](research/results/h_in_sample.md) | Vollständige Tabellen des In-Sample-Laufs |

**Abhängigkeiten:** `../smart-money-concept` (`smc`), `../09-pre-fomc-drift` (`fomc`), `../10-turn-of-the-month` (`tom`), `../11-intraday-momentum` (`imom`); venv aus dem SMC-Projekt.

```sh
../smart-money-concept/research/.venv/bin/python -I research/scripts/run_h.py                  # In-Sample (T88, T89)
../smart-money-concept/research/.venv/bin/python -I research/scripts/run_h.py --holdout H-SPX    # Hold-out, genau einmal
cd research && ../../smart-money-concept/research/.venv/bin/python -I -m pytest -q tests/        # Tests
```
