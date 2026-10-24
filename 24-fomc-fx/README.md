# Strategie Nr. 24 – USD an FOMC-Tagen

Teil der Testreihe `../STRATEGIEN.md`. Ziel ist ein autonomer MT5-EA für die FTMO 2-Step-Challenge (Swing, 100.000 USD). Feste Rahmenbedingungen: 10 % max. Verlust, 5 % max. Tagesverlust, Ziele +10 % / +5 %, News und Wochenende erlaubt.

**Idee:** Short USD gegen alle Hauptwährungen (F-USD) bzw. gegen die drei höchstverzinsten (F-CARRY) über den FX-Tag eines FOMC-Entscheids (Mueller, Tahbaz-Salehi & Vedolin 2017).

**Status (24.10.2026): knapp gescheitert, Ensemble-Kandidat.** F-USD +108 bp je Termin (t 2,10), F-CARRY +55 bp (t 2,11, 9 von 9 Jahren positiv); 3 von 4 Kriterien erfüllt. Hold-out unberührt.

| Dokument | Inhalt |
|---|---|
| [docs/00_Recherche.md](docs/00_Recherche.md) | Effekt, Evidenz, Gegenargumente, Erwartung |
| [docs/01_Vorregistrierung.md](docs/01_Vorregistrierung.md) | Regeln, Varianten, Akzeptanzkriterien, Trial-Log |
| [docs/02_Ergebnisse_In-Sample.md](docs/02_Ergebnisse_In-Sample.md) | Ergebnis, Vergleich mit übrigen Tagen, Einordnung |
| [research/results/f_in_sample.md](research/results/f_in_sample.md) | Vollständige Tabellen des In-Sample-Laufs |

**Abhängigkeiten:** `../smart-money-concept` (`smc`), `../06-fx-carry` (`carry`), `../09-pre-fomc-drift` (`fomc`: Termine); venv aus dem SMC-Projekt.

```sh
../smart-money-concept/research/.venv/bin/python -I research/scripts/run_f.py                  # In-Sample (T84, T85)
../smart-money-concept/research/.venv/bin/python -I research/scripts/run_f.py --holdout F-USD    # Hold-out, genau einmal
cd research && ../../smart-money-concept/research/.venv/bin/python -I -m pytest -q tests/        # Tests
```
