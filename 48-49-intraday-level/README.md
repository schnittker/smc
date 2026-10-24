# Strategien Nr. 48 und 49 – Intraday-Level (Market Profile 80-%-Regel, Pivot Points)

Teil der Testreihe `../STRATEGIEN.md`. Ziel ist ein autonomer MT5-EA für die FTMO 2-Step-Challenge (Swing, 100.000 USD). Feste Rahmenbedingungen: 10 % max. Verlust, 5 % max. Tagesverlust, Ziele +10 % / +5 %, News und Wochenende erlaubt.

**Idee:**
- **Nr. 48:** Value Area der vorigen Kassasitzung (TPO, 70 %). Nach einer Eröffnung außerhalb und zwei 30-Minuten-Schlüssen innerhalb wird die Durchquerung zur Gegenseite gehandelt.
- **Nr. 49:** Klassische Pivots. Limit-Fade an S1/R1 mit Ziel P bzw. Stop-Ausbruch über R3/S3.

**Status (24.10.2026):** In-Sample getestet. **Alle drei Varianten sind gescheitert** (netto −0,83 / −12,6 / −4,25 bp je Tag; vor Kosten ≤ 0). Der Hold-out bleibt unberührt.

| Dokument | Inhalt |
|---|---|
| [docs/00_Recherche.md](docs/00_Recherche.md) | Idee, Quellen, Erwartung |
| [docs/01_Vorregistrierung.md](docs/01_Vorregistrierung.md) | Regeln, Varianten, Akzeptanzkriterien, Trial-Log |
| [docs/02_Ergebnisse_In-Sample.md](docs/02_Ergebnisse_In-Sample.md) | Ergebnis und Einordnung |
| [research/results/lv_in_sample.md](research/results/lv_in_sample.md) | vollständige Tabellen |

**Abhängigkeiten:** `../smart-money-concept` (`smc`), `../33-35-tagesausbruch` (`dbo`), `../41-42-gap-fade` (`gap`) samt dessen Abhängigkeiten; venv aus dem SMC-Projekt.

```sh
../smart-money-concept/research/.venv/bin/python -I research/scripts/run_lv.py                    # In-Sample (T165–T167)
../smart-money-concept/research/.venv/bin/python -I research/scripts/run_lv.py --holdout LV-VA80   # Hold-out, genau einmal
cd research && ../../smart-money-concept/research/.venv/bin/python -I -m pytest -q tests/          # Tests
```
