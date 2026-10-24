# Strategien Nr. 33, 34, 35 – Tages-Ausbruch (NR7, Inside Bar, Volatility Breakout)

Teil der Testreihe `../STRATEGIEN.md`. Ziel ist ein autonomer MT5-EA für die FTMO 2-Step-Challenge (Swing, 100.000 USD). Feste Rahmenbedingungen: 10 % max. Verlust, 5 % max. Tagesverlust, Ziele +10 % / +5 %, News und Wochenende erlaubt.

**Idee:** Stop-Orders am Folgetag über Hoch/Tief einer NR7- bzw. Inside-Bar-Kerze oder bei Eröffnung ± halber Vortagesrange; Stop am Gegenlevel, Schluss am Tagesende; 17 Instrumente.

**Status (24.10.2026):** In-Sample getestet. **Alle drei Varianten sind gescheitert** (netto −0,5 / +0,1 / −4,2 bp je Tag, t −0,50 / 0,15 / −2,07). Der Hold-out bleibt unberührt.

| Dokument | Inhalt |
|---|---|
| [docs/00_Recherche.md](docs/00_Recherche.md) | Idee, Quellen, Erwartung |
| [docs/01_Vorregistrierung.md](docs/01_Vorregistrierung.md) | Regeln, Varianten, Akzeptanzkriterien, Trial-Log |
| [docs/02_Ergebnisse_In-Sample.md](docs/02_Ergebnisse_In-Sample.md) | Ergebnis und Einordnung |
| [research/results/t_in_sample.md](research/results/t_in_sample.md) | vollständige Tabellen |

**Abhängigkeiten:** `../smart-money-concept` (`smc`); venv aus dem SMC-Projekt.

```sh
../smart-money-concept/research/.venv/bin/python -I research/scripts/run_t.py                  # In-Sample (T114–T116)
../smart-money-concept/research/.venv/bin/python -I research/scripts/run_t.py --holdout T-NR7    # Hold-out, genau einmal
cd research && ../../smart-money-concept/research/.venv/bin/python -I -m pytest -q tests/        # Tests
```
