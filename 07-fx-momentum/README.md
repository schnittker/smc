# Strategie Nr. 7 – FX Querschnitts-Momentum G8

Teil der Testreihe `../STRATEGIEN.md`. Ziel ist ein autonomer MT5-EA für die FTMO 2-Step-Challenge (Swing, 100.000 USD). Feste Rahmenbedingungen: 10 % max. Verlust, 5 % max. Tagesverlust, Ziele +10 % / +5 %, News und Wochenende erlaubt.

**Idee:** Long die drei Währungen mit der höchsten vergangenen Überschussrendite, Short die drei schwächsten; monatlich umgeschichtet (Menkhoff, Sarno, Schmeling & Schrimpf 2012).

**Status (24.10.2026):** Vorregistrierung festgelegt, Test läuft.

| Dokument | Inhalt |
|---|---|
| [docs/00_Recherche.md](docs/00_Recherche.md) | Mechanismus, Evidenz, Gegenargumente, Erwartung |
| [docs/01_Vorregistrierung.md](docs/01_Vorregistrierung.md) | Regeln, Varianten, Akzeptanzkriterien, Trial-Log |

**Abhängigkeiten:** `../smart-money-concept` (Paket `smc`: Daten, Zeit- und Kostenmodell) und `../06-fx-carry` (Paket `carry`: Portfolio-Engine); venv aus dem SMC-Projekt.

```sh
../smart-money-concept/research/.venv/bin/python -I research/scripts/run_x.py               # In-Sample (T27, T28)
../smart-money-concept/research/.venv/bin/python -I research/scripts/run_x.py --holdout X-1   # Hold-out, genau einmal
cd research && ../../smart-money-concept/research/.venv/bin/python -I -m pytest -q tests/     # Tests
```
