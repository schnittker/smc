# Strategien Nr. 50 und 51 – Horizontale S/R-Zonen und Trendlinien-Ausbruch

Teil der Testreihe `../STRATEGIEN.md`. Ziel ist ein autonomer MT5-EA für die FTMO 2-Step-Challenge (Swing, 100.000 USD). Feste Rahmenbedingungen: 10 % max. Verlust, 5 % max. Tagesverlust, Ziele +10 % / +5 %, News und Wochenende erlaubt.

**Idee:** Swing-Punkte auf H4 (3 Kerzen je Seite).
- **Zonen** sind Level mit mindestens zwei Swings innerhalb von ±0,25 ATR; gehandelt wird der Abpraller oder der Ausbruch.
- **Trendlinien** verlaufen durch die letzten zwei Swing-Hochs bzw. -Tiefs; gehandelt wird der Ausbruch.
- Stop 1 ATR hinter der Zone bzw. hinter dem Swing, Ziel 2R, Zeitstopp 30 Kerzen, 17 Instrumente.

**Status (24.10.2026):** Vorregistrierung festgelegt, Test läuft.

| Dokument | Inhalt |
|---|---|
| [docs/00_Recherche.md](docs/00_Recherche.md) | Idee, Quellen, Erwartung |
| [docs/01_Vorregistrierung.md](docs/01_Vorregistrierung.md) | Regeln, Varianten, Akzeptanzkriterien, Trial-Log |

**Abhängigkeiten:** `../smart-money-concept` (`smc`), `../33-35-tagesausbruch` (`dbo`), `../36-38-h4-kanalausbruch` (`hkb`); venv aus dem SMC-Projekt. Das Paket `chart` (Swings, Trade-Engine) wird von späteren Chart-Strategien wiederverwendet.

```sh
../smart-money-concept/research/.venv/bin/python -I research/scripts/run_sr.py                      # In-Sample (T174–T176)
../smart-money-concept/research/.venv/bin/python -I research/scripts/run_sr.py --holdout SR-BOUNCE   # Hold-out, genau einmal
cd research && ../../smart-money-concept/research/.venv/bin/python -I -m pytest -q tests/            # Tests
```
