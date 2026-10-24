# Strategie Nr. 12 – Overnight-Drift US500

Teil der Testreihe `../STRATEGIEN.md`. Ziel ist ein autonomer MT5-EA für die FTMO 2-Step-Challenge (Swing, 100.000 USD). Feste Rahmenbedingungen: 10 % max. Verlust, 5 % max. Tagesverlust, Ziele +10 % / +5 %, News und Wochenende erlaubt.

**Idee:** Long US500 nur über Nacht (16:00–09:30) bzw. nur in der Stunde der Eröffnung in Europa (02:00–03:00 New York), dort optional nur nach Verlusttagen (Cliff et al. 2008; Boyarchenko et al. 2023).

**Status (24.10.2026): gescheitert.** N-NACHT +0,22 bp/Nacht (t 0,14), N-EU −0,51 bp (t −1,54), N-EU-DOWN −0,10 bp (t −0,18). Vor Kosten +0,6 bis +2,1 bp, Kosten 1,1 bis 1,9 bp. Hold-out unberührt.

| Dokument | Inhalt |
|---|---|
| [docs/00_Recherche.md](docs/00_Recherche.md) | Effekt, Evidenz (inkl. Verschwinden seit 2021), Erwartung |
| [docs/01_Vorregistrierung.md](docs/01_Vorregistrierung.md) | Regeln, Varianten, Akzeptanzkriterien, Trial-Log |
| [docs/02_Ergebnisse_In-Sample.md](docs/02_Ergebnisse_In-Sample.md) | Ergebnis (gescheitert), Einordnung |
| [research/results/n_in_sample.md](research/results/n_in_sample.md) | Vollständige Tabellen des In-Sample-Laufs |

**Abhängigkeiten:** `../smart-money-concept` (`smc`), `../09-pre-fomc-drift` (`fomc`), `../10-turn-of-the-month` (`tom`); venv aus dem SMC-Projekt.

```sh
../smart-money-concept/research/.venv/bin/python -I research/scripts/run_n.py                   # In-Sample (T43–T45)
../smart-money-concept/research/.venv/bin/python -I research/scripts/run_n.py --holdout N-NACHT   # Hold-out, genau einmal
cd research && ../../smart-money-concept/research/.venv/bin/python -I -m pytest -q tests/         # Tests
```
