# Strategie Nr. 101 – Krypto-Swing-Trendfolge

Teil der Testreihe `../STRATEGIEN.md`. Ziel ist ein autonomer MT5-EA für die FTMO 2-Step-Challenge (Swing, 100.000 USD). Feste Rahmenbedingungen: 10 % max. Verlust, 5 % max. Tagesverlust, Ziele +10 % / +5 %, News und Wochenende erlaubt.

**Idee:**
- Tägliche Zeitreihen-Trendfolge auf BTC, ETH, LTC, XRP, ADA
- Signal: Mittel der Vorzeichen über 7/14/28/56 Tage
- je Coin 10 % Zielvola, Hebel ≤ 1:1 (FTMO Swing)
- Swap pessimistisch 20 % p. a.
- Zwei Varianten: K-TSM (long/short), K-LONG (nur long)

**Status (25.10.2026):** **Gescheitert.**
- In-Sample knapp verfehlt: K-LONG Sharpe 1,18, t 2,57
- Per Nachtrag (Regeländerung, T317) mit strengeren Kriterien in den Hold-out gelassen
- Hold-out 2024–10/2026: Sharpe 0,48 < 0,5; Gewinn nur 2024, 2025/26 negativ
- Ein erster Lauf war wegen einer falschen Datumskonstante zu kurz und ist dokumentiert.

| Dokument | Inhalt |
|---|---|
| [docs/00_Recherche.md](docs/00_Recherche.md) | FTMO-Krypto-Bedingungen, Literatur, Daten |
| [docs/01_Vorregistrierung.md](docs/01_Vorregistrierung.md) | Regeln, Kosten, Kriterien, Trial-Log |
| [docs/02_Ergebnisse_In-Sample.md](docs/02_Ergebnisse_In-Sample.md) | Ergebnis und Einordnung |
| [docs/03_Nachtrag_Hold-out.md](docs/03_Nachtrag_Hold-out.md) | Ausnahmeregel für den Hold-out |
| [docs/04_Ergebnisse_Hold-out.md](docs/04_Ergebnisse_Hold-out.md) | Hold-out (zwei Läufe) und Einordnung |
| [research/results/k_in_sample.md](research/results/k_in_sample.md) | vollständige Tabellen |

**Daten:** `research/scripts/download_binance.sh` lädt die Binance-Tageskerzen nach `data/raw/binance/` (nicht im Repo).

**Abhängigkeiten:** `../smart-money-concept` (`smc`), `../100-swing-portfolio` (`swp`, FTMO-Simulation); venv aus dem SMC-Projekt.

```sh
research/scripts/download_binance.sh
cd research
../../smart-money-concept/research/.venv/bin/python -I scripts/run_k.py                  # In-Sample (T309, T310)
../../smart-money-concept/research/.venv/bin/python -I scripts/run_k.py --ausnahme       # Hold-out K-LONG nach Nachtrag (bereits gelaufen)
../../smart-money-concept/research/.venv/bin/python -I -m pytest -q tests/              # Tests
```
