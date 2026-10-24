# Strategien Nr. 41 und 42 – Gap-Fade (Index-Eröffnung, FX-Wochenende)

Teil der Testreihe `../STRATEGIEN.md`. Ziel ist ein autonomer MT5-EA für die FTMO 2-Step-Challenge (Swing, 100.000 USD). Feste Rahmenbedingungen: 10 % max. Verlust, 5 % max. Tagesverlust, Ziele +10 % / +5 %, News und Wochenende erlaubt.

**Idee:** Gap zwischen Vorschluss und Eröffnung (Kassa-Eröffnung bei US500, US100, FRA40, UK100; Sonntag 18:00 New York bei 7 FX-Majors) wird gefadet. Ziel ist der Vorschluss, der Stop liegt eine Gapgröße weiter, Ausstieg spätestens zum Sitzungs- bzw. Tagesende.

**Status (24.10.2026):** In-Sample getestet. Q-IDX ist gescheitert (−3,15 bp je Tag). Q-FXW hat formal bestanden (+11,9 bp je Montag, t 5,08), wird aber verworfen: Der Ertrag stammt vollständig aus der ersten Wochenkerze des HistData-Feeds (siehe Ergebnisbericht). Der Hold-out bleibt unberührt.

| Dokument | Inhalt |
|---|---|
| [docs/00_Recherche.md](docs/00_Recherche.md) | Idee, Quellen, Erwartung |
| [docs/01_Vorregistrierung.md](docs/01_Vorregistrierung.md) | Regeln, Varianten, Akzeptanzkriterien, Trial-Log |
| [docs/02_Ergebnisse_In-Sample.md](docs/02_Ergebnisse_In-Sample.md) | Ergebnis, Artefakt-Analyse, Entscheidung |
| [research/results/q_in_sample.md](research/results/q_in_sample.md) | vollständige Tabellen |
| [research/results/q_fxw_robustheit.md](research/results/q_fxw_robustheit.md) | Robustheitsprüfung Q-FXW |

**Abhängigkeiten:** `../smart-money-concept` (`smc`), `../33-35-tagesausbruch` (`dbo`), `../05-monatsend-rebalancing` (`mer`), `../09-pre-fomc-drift` (`fomc`), `../10-turn-of-the-month` (`tom`), `../11-intraday-momentum` (`imom`); venv aus dem SMC-Projekt.

```sh
../smart-money-concept/research/.venv/bin/python -I research/scripts/run_q.py                  # In-Sample (T138, T139)
../smart-money-concept/research/.venv/bin/python -I research/scripts/run_q.py --holdout Q-IDX    # Hold-out, genau einmal
cd research && ../../smart-money-concept/research/.venv/bin/python -I -m pytest -q tests/        # Tests
```
