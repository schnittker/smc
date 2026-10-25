# Strategie Nr. 101 – Krypto-Swing-Trendfolge

Teil der Testreihe `../STRATEGIEN.md`. Ziel ist ein autonomer MT5-EA für die FTMO 2-Step-Challenge (Swing, 100.000 USD). Feste Rahmenbedingungen: 10 % max. Verlust, 5 % max. Tagesverlust, Ziele +10 % / +5 %, News und Wochenende erlaubt.

**Idee:**
- Tägliche Zeitreihen-Trendfolge auf BTC, ETH, LTC, XRP, ADA
- Signal: Mittel der Vorzeichen über 7/14/28/56 Tage
- je Coin 10 % Zielvola, Hebel ≤ 1:1 (FTMO Swing)
- Swap pessimistisch 20 % p. a.
- Zwei Varianten: K-TSM (long/short), K-LONG (nur long)

**Status (25.10.2026):** In-Sample 2018–2023 getestet. **Gescheitert, aber knapp:**
- K-LONG: Sharpe 1,18, t 2,57; 3 von 4 Kriterien erfüllt
- K-TSM: Sharpe 0,80, t 1,97

Der Hold-out bleibt unberührt.

| Dokument | Inhalt |
|---|---|
| [docs/00_Recherche.md](docs/00_Recherche.md) | FTMO-Krypto-Bedingungen, Literatur, Daten |
| [docs/01_Vorregistrierung.md](docs/01_Vorregistrierung.md) | Regeln, Kosten, Kriterien, Trial-Log |
| [docs/02_Ergebnisse_In-Sample.md](docs/02_Ergebnisse_In-Sample.md) | Ergebnis und Einordnung |
| [research/results/k_in_sample.md](research/results/k_in_sample.md) | vollständige Tabellen |

**Daten:** `research/scripts/download_binance.sh` lädt die Binance-Tageskerzen nach `data/raw/binance/` (nicht im Repo).

**Abhängigkeiten:** `../smart-money-concept` (`smc`), `../100-swing-portfolio` (`swp`, FTMO-Simulation); venv aus dem SMC-Projekt.

```sh
research/scripts/download_binance.sh
cd research
../../smart-money-concept/research/.venv/bin/python -I scripts/run_k.py                  # In-Sample (T309, T310)
../../smart-money-concept/research/.venv/bin/python -I scripts/run_k.py --holdout K-LONG # Hold-out, genau einmal, nur bei Bestehen
../../smart-money-concept/research/.venv/bin/python -I -m pytest -q tests/              # Tests
```
