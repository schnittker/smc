# Strategien Nr. 65–68, 74, 75 – Oszillatoren, Divergenzen, Renko

Teil der Testreihe `../STRATEGIEN.md`. Ziel ist ein autonomer MT5-EA für die FTMO 2-Step-Challenge (Swing, 100.000 USD). Feste Rahmenbedingungen: 10 % max. Verlust, 5 % max. Tagesverlust, Ziele +10 % / +5 %, News und Wochenende erlaubt.

**Idee:** 17 Instrumente:
- **H1:** RSI-, Stochastik- und Williams-%R-Umkehr aus den Extremzonen
- **H4:** CCI-±100-Momentum, RSI-Divergenzen an Swing-Punkten
- **H1:** Renko-Trend (Ziegel 2 ATR)

**Status (24.10.2026):** In-Sample getestet. **Alle sechs Regeln sind gescheitert** (netto −1,6 bis −50 bp je Tag). Der Hold-out bleibt unberührt.

| Dokument | Inhalt |
|---|---|
| [docs/00_Recherche.md](docs/00_Recherche.md) | Idee, Quellen, Erwartung |
| [docs/01_Vorregistrierung.md](docs/01_Vorregistrierung.md) | Regeln, Varianten, Akzeptanzkriterien, Trial-Log |
| [docs/02_Ergebnisse_In-Sample.md](docs/02_Ergebnisse_In-Sample.md) | Ergebnis und Einordnung |
| [research/results/os_in_sample.md](research/results/os_in_sample.md) | vollständige Tabellen |

**Abhängigkeiten:** `../smart-money-concept` (`smc`), `../33-35-tagesausbruch` (`dbo`), `../36-38-h4-kanalausbruch` (`hkb`), `../50-51-sr-trendlinien` (`chart`), `../61-76-trendindikatoren` (`tind`); venv aus dem SMC-Projekt.

```sh
../smart-money-concept/research/.venv/bin/python -I research/scripts/run_os.py                   # In-Sample (T249–T254)
../smart-money-concept/research/.venv/bin/python -I research/scripts/run_os.py --holdout OS-RSI   # Hold-out, genau einmal
cd research && ../../smart-money-concept/research/.venv/bin/python -I -m pytest -q tests/         # Tests
```
