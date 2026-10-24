# Strategie Nr. 10 – Turn-of-the-Month US500

Teil der Testreihe `../STRATEGIEN.md`. Ziel ist ein autonomer MT5-EA für die FTMO 2-Step-Challenge (Swing, 100.000 USD). Feste Rahmenbedingungen: 10 % max. Verlust, 5 % max. Tagesverlust, Ziele +10 % / +5 %, News und Wochenende erlaubt.

**Idee:** Long US500 nur in den Handelstagen um den Monatswechsel (McConnell & Xu 2008).

**Status (24.10.2026): gescheitert.** T-KLASSIK +22 bp je Monatswechsel (t 1,17), T-FRÜH +36 bp (t 1,68). Positiv, aber weit unter t ≥ 3; der klassische Tag −1 ist heute negativ. Hold-out unberührt.

| Dokument | Inhalt |
|---|---|
| [docs/00_Recherche.md](docs/00_Recherche.md) | Effekt, Evidenz (inkl. Verschiebung des Fensters), Erwartung |
| [docs/01_Vorregistrierung.md](docs/01_Vorregistrierung.md) | Regeln, Varianten, Akzeptanzkriterien, Trial-Log |
| [docs/02_Ergebnisse_In-Sample.md](docs/02_Ergebnisse_In-Sample.md) | Ergebnis (gescheitert), Einordnung |
| [research/results/t_in_sample.md](research/results/t_in_sample.md) | Vollständige Tabellen des In-Sample-Laufs |

**Abhängigkeiten:** `../smart-money-concept` (Paket `smc`) und `../09-pre-fomc-drift` (Paket `fomc`: Index-Positionen mit Kosten und Swaps); venv aus dem SMC-Projekt.

```sh
../smart-money-concept/research/.venv/bin/python -I research/scripts/run_t.py                     # In-Sample (T35, T36)
../smart-money-concept/research/.venv/bin/python -I research/scripts/run_t.py --holdout T-KLASSIK   # Hold-out, genau einmal
cd research && ../../smart-money-concept/research/.venv/bin/python -I -m pytest -q tests/           # Tests
```
