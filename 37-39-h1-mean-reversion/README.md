# Strategien Nr. 37 und 39 – H1-Mean-Reversion auf FX-Crosses (Bollinger, z-Score/OU)

Teil der Testreihe `../STRATEGIEN.md`. Ziel ist ein autonomer MT5-EA für die FTMO 2-Step-Challenge (Swing, 100.000 USD). Feste Rahmenbedingungen: 10 % max. Verlust, 5 % max. Tagesverlust, Ziele +10 % / +5 %, News und Wochenende erlaubt.

**Idee:** H1-Schluss außerhalb der Bollinger-Bänder bei ADX < 20 bzw. |z| > 2 bei OU-Halbwertszeit ≤ 24 h → Gegenposition bis zur Mittellinie; Stop 2 ATR, Zeitstopp 48 h; 17 Crosses.

**Status (24.10.2026):** In-Sample getestet. **Beide Varianten sind gescheitert** (netto −11,1 / −1,8 bp je Tag, t −6,19 / −2,84). Der Hold-out bleibt unberührt.

| Dokument | Inhalt |
|---|---|
| [docs/00_Recherche.md](docs/00_Recherche.md) | Idee, Quellen, Erwartung |
| [docs/01_Vorregistrierung.md](docs/01_Vorregistrierung.md) | Regeln, Varianten, Akzeptanzkriterien, Trial-Log |
| [docs/02_Ergebnisse_In-Sample.md](docs/02_Ergebnisse_In-Sample.md) | Ergebnis und Einordnung |
| [research/results/u_in_sample.md](research/results/u_in_sample.md) | vollständige Tabellen |

**Abhängigkeiten:** `../smart-money-concept` (`smc`), `../33-35-tagesausbruch` (`dbo`), `../36-38-h4-kanalausbruch` (`hkb`); venv aus dem SMC-Projekt.

```sh
../smart-money-concept/research/.venv/bin/python -I research/scripts/run_u.py                 # In-Sample (T129, T130)
../smart-money-concept/research/.venv/bin/python -I research/scripts/run_u.py --holdout U-BB    # Hold-out, genau einmal
cd research && ../../smart-money-concept/research/.venv/bin/python -I -m pytest -q tests/       # Tests
```
