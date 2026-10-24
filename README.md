# Strategie Nr. 5 – Monatsend-Rebalancing am London-Fix

Teil der Testreihe `../STRATEGIEN.md`. Ziel ist ein autonomer MT5-EA für die FTMO 2-Step-Challenge (Swing, 100.000 USD). Feste Rahmenbedingungen: 10 % max. Verlust, 5 % max. Tagesverlust, Ziele +10 % / +5 %, News und Wochenende erlaubt.

**Idee:** Internationale Aktienfonds passen ihre Währungsabsicherung am Monatsende zum 16:00-Fix in London an. Die Währung des Aktienmarkts, der im Monat besser lief, wertet deshalb vor dem Fix ab (Melvin & Prins 2015).

**Status (24.10.2026): gescheitert.** Beide Varianten verfehlen alle In-Sample-Kriterien (M-1H −4,4 bp je Ereignis, t −1,0; M-DAY −7,1 bp, t −1,0). Der Effekt aus dem Paper ist 2015–2023 nicht mehr messbar (Steigung −0,15 statt −1,4). Hold-out unberührt.

| Dokument | Inhalt |
|---|---|
| [docs/00_Recherche.md](docs/00_Recherche.md) | Mechanismus, Evidenz, Gegenargumente, Erwartung |
| [docs/01_Vorregistrierung.md](docs/01_Vorregistrierung.md) | Regeln, Varianten, Akzeptanzkriterien, Trial-Log |
| [docs/02_Ergebnisse_In-Sample.md](docs/02_Ergebnisse_In-Sample.md) | Ergebnis (gescheitert), Einordnung, Diagnosen |
| [research/results/m_in_sample.md](research/results/m_in_sample.md) | Vollständige Tabellen des In-Sample-Laufs |

**Abhängigkeit:** Kursdaten, Zeitmodell, Bars, Kostenmodell und Statistik kommen aus `../smart-money-concept` (Paket `smc`, Daten unter `data/`). Eingerichtet ist dort schon alles; dieses Projekt nutzt dessen venv.

```sh
../smart-money-concept/research/.venv/bin/python -I research/scripts/run_m.py              # In-Sample (T19, T20)
../smart-money-concept/research/.venv/bin/python -I research/scripts/run_m.py --holdout M-1H  # Hold-out, genau einmal
cd research && ../../smart-money-concept/research/.venv/bin/python -I -m pytest -q tests/    # Tests
```
