# Strategie Nr. 94 – News-Straddle (NFP)

Teil der Testreihe `../STRATEGIEN.md`. Ziel ist ein autonomer MT5-EA für die FTMO 2-Step-Challenge (Swing, 100.000 USD). Feste Rahmenbedingungen: 10 % max. Verlust, 5 % max. Tagesverlust, Ziele +10 % / +5 %, News und Wochenende erlaubt.

**Idee:**
- OCO-Stop-Orders ±0,10 % um den Kurs von 08:29 New York am NFP-Tag (Termine nach der BLS-Regel)
- Stop 0,20 %, Ausstieg um 09:30
- EURUSD, GBPUSD, USDJPY, XAUUSD
- pessimistische News-Kosten: 5-facher Spread, 0,03 % Slippage

**Status (24.10.2026):** In-Sample getestet. **Gescheitert** (−8,8 bp je Termin, t −1,22; auch mit normalen Kosten nur t 0,49). Der Hold-out bleibt unberührt.

| Dokument | Inhalt |
|---|---|
| [docs/00_Recherche.md](docs/00_Recherche.md) | Idee, Probleme, Termine, Quellen |
| [docs/01_Vorregistrierung.md](docs/01_Vorregistrierung.md) | Regeln, Akzeptanzkriterien, Trial-Log |
| [docs/02_Ergebnisse_In-Sample.md](docs/02_Ergebnisse_In-Sample.md) | Ergebnis und Einordnung |
| [research/results/n_in_sample.md](research/results/n_in_sample.md) | vollständige Tabellen |

**Abhängigkeiten:** `../smart-money-concept` (`smc`), `../09-pre-fomc-drift` (`fomc`), `../33-35-tagesausbruch` (`dbo`); venv aus dem SMC-Projekt.

```sh
../smart-money-concept/research/.venv/bin/python -I research/scripts/run_n.py              # In-Sample (T303)
../smart-money-concept/research/.venv/bin/python -I research/scripts/run_n.py --holdout    # Hold-out, genau einmal
cd research && ../../smart-money-concept/research/.venv/bin/python -I -m pytest -q tests/   # Tests
```
