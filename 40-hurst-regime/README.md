# Strategie Nr. 40 – Hurst-Regime-Switch

Teil der Testreihe `../STRATEGIEN.md`. Ziel ist ein autonomer MT5-EA für die FTMO 2-Step-Challenge (Swing, 100.000 USD). Feste Rahmenbedingungen: 10 % max. Verlust, 5 % max. Tagesverlust, Ziele +10 % / +5 %, News und Wochenende erlaubt.

**Idee:** Hurst-Exponent aus 500 H4-Kerzen. Bei H > 0,55 wird der Keltner-Ausbruch gehandelt, bei H < 0,45 der Bollinger-Fade, dazwischen nichts. Stop 2 ATR, 17 Instrumente.

**Status (24.10.2026):** In-Sample getestet. **Gescheitert** (netto −2,27 bp je Tag, t −4,70; schlechter als beide Bausteine ohne Filter). Der Hold-out bleibt unberührt.

| Dokument | Inhalt |
|---|---|
| [docs/00_Recherche.md](docs/00_Recherche.md) | Idee, Quellen, Erwartung |
| [docs/01_Vorregistrierung.md](docs/01_Vorregistrierung.md) | Regeln, Akzeptanzkriterien, Trial-Log |
| [docs/02_Ergebnisse_In-Sample.md](docs/02_Ergebnisse_In-Sample.md) | Ergebnis und Einordnung |
| [research/results/w_in_sample.md](research/results/w_in_sample.md) | vollständige Tabellen |

**Abhängigkeiten:** `../smart-money-concept` (`smc`), `../33-35-tagesausbruch` (`dbo`), `../36-38-h4-kanalausbruch` (`hkb`); venv aus dem SMC-Projekt.

```sh
../smart-money-concept/research/.venv/bin/python -I research/scripts/run_w.py              # In-Sample (T135)
../smart-money-concept/research/.venv/bin/python -I research/scripts/run_w.py --holdout    # Hold-out, genau einmal
cd research && ../../smart-money-concept/research/.venv/bin/python -I -m pytest -q tests/   # Tests
```
