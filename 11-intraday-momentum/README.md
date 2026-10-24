# Strategie Nr. 11 – Intraday-Momentum US500

Teil der Testreihe `../STRATEGIEN.md`. Ziel ist ein autonomer MT5-EA für die FTMO 2-Step-Challenge (Swing, 100.000 USD). Feste Rahmenbedingungen: 10 % max. Verlust, 5 % max. Tagesverlust, Ziele +10 % / +5 %, News und Wochenende erlaubt.

**Idee:** Die Indexrendite vom Vortagsschluss bis 10:00 (bzw. bis 15:30) sagt die Richtung der letzten halben Stunde voraus; gehandelt wird 15:30–16:00 New York (Gao et al. 2018; Baltussen et al. 2021).

**Status (24.10.2026): gescheitert.** I-ONFH +0,44 bp/Tag (t 0,52), I-ROD +1,00 bp/Tag (t 1,31). Effekt vorhanden (Regression t 3,45), aber vor Kosten nur ≈ 2 bp/Tag bei 1,1 bp Kosten. Hold-out unberührt.

| Dokument | Inhalt |
|---|---|
| [docs/00_Recherche.md](docs/00_Recherche.md) | Effekt, Evidenz, Gegenargumente, Erwartung |
| [docs/01_Vorregistrierung.md](docs/01_Vorregistrierung.md) | Regeln, Varianten, Akzeptanzkriterien, Trial-Log |
| [docs/02_Ergebnisse_In-Sample.md](docs/02_Ergebnisse_In-Sample.md) | Ergebnis (gescheitert), Einordnung |
| [research/results/i_in_sample.md](research/results/i_in_sample.md) | Vollständige Tabellen des In-Sample-Laufs |

**Abhängigkeiten:** `../smart-money-concept` (Paket `smc`) und `../10-turn-of-the-month` (Paket `tom`: NYSE-Kalender), über diesen auch `../09-pre-fomc-drift`; venv aus dem SMC-Projekt.

```sh
../smart-money-concept/research/.venv/bin/python -I research/scripts/run_i.py                  # In-Sample (T39, T40)
../smart-money-concept/research/.venv/bin/python -I research/scripts/run_i.py --holdout I-ONFH   # Hold-out, genau einmal
cd research && ../../smart-money-concept/research/.venv/bin/python -I -m pytest -q tests/        # Tests
```
