# Strategie Nr. 19 – VIX-Regime

Teil der Testreihe `../STRATEGIEN.md`. Ziel ist ein autonomer MT5-EA für die FTMO 2-Step-Challenge (Swing, 100.000 USD). Feste Rahmenbedingungen: 10 % max. Verlust, 5 % max. Tagesverlust, Ziele +10 % / +5 %, News und Wochenende erlaubt.

**Idee:** Im Risk-off-Regime (VIX im obersten Dezil des letzten Jahres) long in sicheren Häfen JPY, CHF, Gold (X-HAVEN) bzw. long US500 als konträrer Kauf (X-FEAR, Giot 2005).

**Status (24.10.2026):** Vorregistrierung festgelegt, Test läuft.

| Dokument | Inhalt |
|---|---|
| [docs/00_Recherche.md](docs/00_Recherche.md) | Idee, Evidenz, Daten, Erwartung |
| [docs/01_Vorregistrierung.md](docs/01_Vorregistrierung.md) | Regeln, Varianten, Akzeptanzkriterien, Trial-Log |

**Abhängigkeiten:** `../smart-money-concept` (`smc`), `../06-fx-carry` (`carry`); venv aus dem SMC-Projekt. VIX-Daten (nicht im Repo):

```sh
mkdir -p data/raw && curl -sL -o data/raw/VIX_History.csv https://cdn.cboe.com/api/global/us_indices/daily_prices/VIX_History.csv
../smart-money-concept/research/.venv/bin/python -I research/scripts/run_x.py                   # In-Sample (T64, T65)
../smart-money-concept/research/.venv/bin/python -I research/scripts/run_x.py --holdout X-FEAR   # Hold-out, genau einmal
cd research && ../../smart-money-concept/research/.venv/bin/python -I -m pytest -q tests/        # Tests
```
