# Strategien Nr. 56 und 57 – Optionsverfall (OPEX) und Santa Rally

Teil der Testreihe `../STRATEGIEN.md`. Ziel ist ein autonomer MT5-EA für die FTMO 2-Step-Challenge (Swing, 100.000 USD). Feste Rahmenbedingungen: 10 % max. Verlust, 5 % max. Tagesverlust, Ziele +10 % / +5 %, News und Wochenende erlaubt.

**Idee:** US500 mit Kursen um 15:55 New York und Positionsmechanik wie Nr. 9/10:
- Long in der OPEX-Woche (Handelstag −5 bis zum Verfallstag)
- Short in der Woche danach
- Long in der Santa-Rally-Phase (letzte 5 Handelstage im Dezember plus erste 2 im Januar)

**Status (24.10.2026):** In-Sample getestet. **Alle drei Varianten sind gescheitert** (netto −6,7 / −30,3 / +0,1 bp je Ereignis). Der Hold-out bleibt unberührt.

| Dokument | Inhalt |
|---|---|
| [docs/00_Recherche.md](docs/00_Recherche.md) | Idee, Quellen, Erwartung |
| [docs/01_Vorregistrierung.md](docs/01_Vorregistrierung.md) | Regeln, Varianten, Akzeptanzkriterien, Trial-Log |
| [docs/02_Ergebnisse_In-Sample.md](docs/02_Ergebnisse_In-Sample.md) | Ergebnis und Einordnung |
| [research/results/ka_in_sample.md](research/results/ka_in_sample.md) | vollständige Tabellen |

**Abhängigkeiten:** `../smart-money-concept` (`smc`), `../09-pre-fomc-drift` (`fomc`), `../10-turn-of-the-month` (`tom`); venv aus dem SMC-Projekt.

```sh
../smart-money-concept/research/.venv/bin/python -I research/scripts/run_ka.py                  # In-Sample (T201–T203)
../smart-money-concept/research/.venv/bin/python -I research/scripts/run_ka.py --holdout K-OPEX  # Hold-out, genau einmal
cd research && ../../smart-money-concept/research/.venv/bin/python -I -m pytest -q tests/       # Tests
```
