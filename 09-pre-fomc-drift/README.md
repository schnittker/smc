# Strategie Nr. 9 – Pre-FOMC-Drift

Teil der Testreihe `../STRATEGIEN.md`. Ziel ist ein autonomer MT5-EA für die FTMO 2-Step-Challenge (Swing, 100.000 USD). Feste Rahmenbedingungen: 10 % max. Verlust, 5 % max. Tagesverlust, Ziele +10 % / +5 %, News und Wochenende erlaubt.

**Idee:** Long US500 bzw. US100 von 14:00 New York am Vortag bis 13:55 am Tag eines planmäßigen FOMC-Zinsentscheids (Lucca & Moench 2015).

**Status (24.10.2026):** Vorregistrierung festgelegt, Test läuft.

| Dokument | Inhalt |
|---|---|
| [docs/00_Recherche.md](docs/00_Recherche.md) | Effekt, Evidenz (inkl. Verschwinden nach 2015), Erwartung |
| [docs/01_Vorregistrierung.md](docs/01_Vorregistrierung.md) | Regeln, Varianten, Akzeptanzkriterien, Trial-Log |
| [research/fomc_dates.csv](research/fomc_dates.csv) | Planmäßige FOMC-Entscheidungstage 2013–2027 (Federal Reserve) |

**Abhängigkeit:** `../smart-money-concept` (Paket `smc`: Daten, Zeit-, Kosten- und Swap-Modell); venv aus dem SMC-Projekt. Die Fed-Kalenderseiten liegen unter `data/raw/` (nicht im Repo) und werden so geladen:

```sh
mkdir -p data/raw && curl -s -o data/raw/fomccalendars.html https://www.federalreserve.gov/monetarypolicy/fomccalendars.htm
for y in 2013 2014 2015 2016 2017 2018 2019 2020; do curl -s -o data/raw/fomchistorical$y.html https://www.federalreserve.gov/monetarypolicy/fomchistorical$y.htm; done
../smart-money-concept/research/.venv/bin/python -I research/scripts/build_fomc_dates.py     # Terminliste
../smart-money-concept/research/.venv/bin/python -I research/scripts/run_p.py                # In-Sample (T31, T32)
../smart-money-concept/research/.venv/bin/python -I research/scripts/run_p.py --holdout P-SPX  # Hold-out, genau einmal
cd research && ../../smart-money-concept/research/.venv/bin/python -I -m pytest -q tests/     # Tests
```
