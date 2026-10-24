# Strategie Nr. 45 – Multi-Timeframe-Pullback

Teil der Testreihe `../STRATEGIEN.md`. Ziel ist ein autonomer MT5-EA für die FTMO 2-Step-Challenge (Swing, 100.000 USD). Feste Rahmenbedingungen: 10 % max. Verlust, 5 % max. Tagesverlust, Ziele +10 % / +5 %, News und Wochenende erlaubt.

**Idee:** Der Trend kommt aus D1 (Schluss gegenüber EMA50) und H4 (EMA20 gegenüber EMA50). Eingestiegen wird, wenn H1 nach einem Rücksetzer wieder über bzw. unter die EMA20 schließt. Stop unter dem 10-Kerzen-Tief, Ziel 2R, Zeitstopp 48 h, 17 Instrumente.

**Status (24.10.2026):** In-Sample getestet. **Gescheitert** (netto −14,7 bp je Tag, t −6,53; schon vor Kosten negativ). Der Hold-out bleibt unberührt.

| Dokument | Inhalt |
|---|---|
| [docs/00_Recherche.md](docs/00_Recherche.md) | Idee, Quellen, Erwartung |
| [docs/01_Vorregistrierung.md](docs/01_Vorregistrierung.md) | Regeln, Akzeptanzkriterien, Trial-Log |
| [docs/02_Ergebnisse_In-Sample.md](docs/02_Ergebnisse_In-Sample.md) | Ergebnis und Einordnung |
| [research/results/j_in_sample.md](research/results/j_in_sample.md) | vollständige Tabellen |

**Abhängigkeiten:** `../smart-money-concept` (`smc`), `../33-35-tagesausbruch` (`dbo`), `../36-38-h4-kanalausbruch` (`hkb`); venv aus dem SMC-Projekt.

```sh
../smart-money-concept/research/.venv/bin/python -I research/scripts/run_j.py              # In-Sample (T153)
../smart-money-concept/research/.venv/bin/python -I research/scripts/run_j.py --holdout    # Hold-out, genau einmal
cd research && ../../smart-money-concept/research/.venv/bin/python -I -m pytest -q tests/   # Tests
```
