# Strategie Nr. 18 – COT-Extreme

Teil der Testreihe `../STRATEGIEN.md`. Ziel ist ein autonomer MT5-EA für die FTMO 2-Step-Challenge (Swing, 100.000 USD). Feste Rahmenbedingungen: 10 % max. Verlust, 5 % max. Tagesverlust, Ziele +10 % / +5 %, News und Wochenende erlaubt.

**Idee:** Extreme der Spekulanten-Netto-Position (CFTC Commitments of Traders, COT-Index über 3 Jahre) in 7 Währungs- und dem Goldfuture handeln, konträr (C-KONTRA) oder mit den Spekulanten (C-FOLGE, Tornell & Yuan 2012).

**Status (24.10.2026):** Vorregistrierung festgelegt, Test läuft.

| Dokument | Inhalt |
|---|---|
| [docs/00_Recherche.md](docs/00_Recherche.md) | Idee, Evidenz (Fortsetzung statt Umkehr), Erwartung |
| [docs/01_Vorregistrierung.md](docs/01_Vorregistrierung.md) | Regeln, Varianten, Akzeptanzkriterien, Trial-Log |

**Abhängigkeiten:** `../smart-money-concept` (`smc`) und `../06-fx-carry` (`carry`); venv aus dem SMC-Projekt. Die CFTC-Dateien liegen unter `data/raw/` (nicht im Repo):

```sh
mkdir -p data/raw && for y in $(seq 2011 2026); do curl -s -o data/raw/deacot$y.zip https://www.cftc.gov/files/dea/history/deacot$y.zip; done
../smart-money-concept/research/.venv/bin/python -I research/scripts/run_c.py                    # In-Sample (T60, T61)
../smart-money-concept/research/.venv/bin/python -I research/scripts/run_c.py --holdout C-FOLGE   # Hold-out, genau einmal
cd research && ../../smart-money-concept/research/.venv/bin/python -I -m pytest -q tests/         # Tests
```
