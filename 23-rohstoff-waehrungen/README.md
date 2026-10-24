# Strategie Nr. 23 – Rohstoff-Lead-Lag (Öl → CAD, Gold → AUD)

Teil der Testreihe `../STRATEGIEN.md`. Ziel ist ein autonomer MT5-EA für die FTMO 2-Step-Challenge (Swing, 100.000 USD). Feste Rahmenbedingungen: 10 % max. Verlust, 5 % max. Tagesverlust, Ziele +10 % / +5 %, News und Wochenende erlaubt.

**Idee:** Die Tagesrendite von Brent bzw. Gold bestimmt die Position in USDCAD bzw. AUDUSD für den folgenden Tag.

**Status (24.10.2026):** Vorregistrierung festgelegt, Test läuft.

| Dokument | Inhalt |
|---|---|
| [docs/00_Recherche.md](docs/00_Recherche.md) | Idee, Evidenz (spricht dagegen), Erwartung |
| [docs/01_Vorregistrierung.md](docs/01_Vorregistrierung.md) | Regeln, Varianten, Akzeptanzkriterien, Trial-Log |

**Abhängigkeiten:** `../smart-money-concept` (`smc`), `../06-fx-carry` (`carry`); venv aus dem SMC-Projekt.

```sh
../smart-money-concept/research/.venv/bin/python -I research/scripts/run_r.py                 # In-Sample (T80, T81)
../smart-money-concept/research/.venv/bin/python -I research/scripts/run_r.py --holdout R-OEL   # Hold-out, genau einmal
cd research && ../../smart-money-concept/research/.venv/bin/python -I -m pytest -q tests/       # Tests
```
