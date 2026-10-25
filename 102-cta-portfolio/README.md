# Strategie Nr. 102 – Multi-Asset-Trend (CTA-Stil)

Teil der Testreihe `../STRATEGIEN.md`. Ziel ist ein autonomer MT5-EA für die FTMO 2-Step-Challenge (Swing, 100.000 USD). Feste Rahmenbedingungen: 10 % max. Verlust, 5 % max. Tagesverlust, Ziele +10 % / +5 %, News und Wochenende erlaubt.

**Idee:** Trendfolge wie Managed-Futures-Fonds über 24 FTMO-Märkte:
- FX 7, Indizes 8, Rohstoffe 4, Krypto 5
- Signal: Vorzeichen über 1/3/6/12 Monate
- vola-gesteuert, gleiches Risikobudget je Klasse

**Varianten:**
- **C-FIX:** Standardparameter
- **C-WF:** jährliches Walk-Forward von Rückblick und Klassengewicht

**Status (25.10.2026):** In-Sample 2015–2023 getestet. **Gescheitert** (C-FIX Sharpe 0,09, C-WF 0,26). Der Hold-out bleibt unberührt.

| Dokument | Inhalt |
|---|---|
| [docs/00_Recherche.md](docs/00_Recherche.md) | CTA-Prinzip, bekannte Teilergebnisse, Hebel |
| [docs/01_Vorregistrierung.md](docs/01_Vorregistrierung.md) | Regeln, Walk-Forward, Kriterien, Trial-Log |
| [docs/02_Ergebnisse_In-Sample.md](docs/02_Ergebnisse_In-Sample.md) | Ergebnis und Einordnung |
| [research/results/c_in_sample.md](research/results/c_in_sample.md) | vollständige Tabellen |

**Abhängigkeiten:** `../smart-money-concept` (`smc`), `../06-fx-carry` (`carry`), `../101-krypto-swing` (`kry`, Daten via `download_binance.sh`), `../100-swing-portfolio` (`swp`); venv aus dem SMC-Projekt.

```sh
cd research
../../smart-money-concept/research/.venv/bin/python -I scripts/run_c.py                 # In-Sample (T313, T314)
../../smart-money-concept/research/.venv/bin/python -I -m pytest -q tests/             # Tests
```
