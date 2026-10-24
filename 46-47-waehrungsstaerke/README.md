# Strategien Nr. 46 und 47 – Währungsstärke-Ranking und USD-Basket Mean Reversion

Teil der Testreihe `../STRATEGIEN.md`. Ziel ist ein autonomer MT5-EA für die FTMO 2-Step-Challenge (Swing, 100.000 USD). Feste Rahmenbedingungen: 10 % max. Verlust, 5 % max. Tagesverlust, Ziele +10 % / +5 %, News und Wochenende erlaubt.

**Idee:** Synthetische Stärke der 8 Hauptwährungen aus den USD-Paaren.
- **Nr. 46:** Stärkste gegen schwächste Währung der Asien- bzw. Londoner Morgensitzung bis 16:00 London handeln.
- **Nr. 47:** Währungsspezifische Abweichung eines USD-Paares (z > 2 über 24 h) faden.

**Status (24.10.2026):** Vorregistrierung festgelegt, Test läuft.

| Dokument | Inhalt |
|---|---|
| [docs/00_Recherche.md](docs/00_Recherche.md) | Idee, Quellen, Erwartung |
| [docs/01_Vorregistrierung.md](docs/01_Vorregistrierung.md) | Regeln, Varianten, Akzeptanzkriterien, Trial-Log |

**Abhängigkeiten:** `../smart-money-concept` (`smc`), `../33-35-tagesausbruch` (`dbo`), `../36-38-h4-kanalausbruch` (`hkb`), `../05-monatsend-rebalancing` (`mer`); venv aus dem SMC-Projekt.

```sh
../smart-money-concept/research/.venv/bin/python -I research/scripts/run_y.py                  # In-Sample (T156–T158)
../smart-money-concept/research/.venv/bin/python -I research/scripts/run_y.py --holdout Y-ASIA   # Hold-out, genau einmal
cd research && ../../smart-money-concept/research/.venv/bin/python -I -m pytest -q tests/        # Tests
```
