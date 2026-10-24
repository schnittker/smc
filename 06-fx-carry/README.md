# Strategie Nr. 6 – FX Carry G8

Teil der Testreihe `../STRATEGIEN.md`. Ziel ist ein autonomer MT5-EA für die FTMO 2-Step-Challenge (Swing, 100.000 USD). Feste Rahmenbedingungen: 10 % max. Verlust, 5 % max. Tagesverlust, Ziele +10 % / +5 %, News und Wochenende erlaubt.

**Idee:** Long die höchstverzinsten, Short die niedrigstverzinsten der 8 Hauptwährungen; der Zinsvorteil fließt über die Swaps (Lustig, Roussanov & Verdelhan 2011).

**Status (24.10.2026):** Vorregistrierung festgelegt, Test läuft.

| Dokument | Inhalt |
|---|---|
| [docs/00_Recherche.md](docs/00_Recherche.md) | Mechanismus, Evidenz, Gegenargumente, Erwartung |
| [docs/01_Vorregistrierung.md](docs/01_Vorregistrierung.md) | Regeln, Varianten, Akzeptanzkriterien, Trial-Log |

**Abhängigkeit:** Kursdaten, Zinsen, Zeitmodell, Kostenmodell und die Positions-Engine von Modell G kommen aus `../smart-money-concept` (Paket `smc`); dieses Projekt nutzt dessen venv.

```sh
../smart-money-concept/research/.venv/bin/python -I research/scripts/run_k.py              # In-Sample (T23, T24)
../smart-money-concept/research/.venv/bin/python -I research/scripts/run_k.py --holdout K-3   # Hold-out, genau einmal
cd research && ../../smart-money-concept/research/.venv/bin/python -I -m pytest -q tests/    # Tests
```
