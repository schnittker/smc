# Strategie Nr. 100 – Swing-Portfolio (Ensemble)

Teil der Testreihe `../STRATEGIEN.md`. Ziel ist ein autonomer MT5-EA für die FTMO 2-Step-Challenge (Swing, 100.000 USD). Feste Rahmenbedingungen: 10 % max. Verlust, 5 % max. Tagesverlust, Ziele +10 % / +5 %, News und Wochenende erlaubt.

**Idee:** Die vier besten Swing-Kandidaten der Reihe zu einem Portfolio bündeln, jeder normiert auf 10 % Jahresvola:
- P-SPX (Nr. 9)
- T-FRÜH (Nr. 10)
- V-VOL (Nr. 14)
- F-CARRY (Nr. 24)

Entscheidend sind der gemeinsame Hold-out 2024–2026 und ein FTMO-Block-Bootstrap.

**Status (24.10.2026):** **Gescheitert im Hold-out.**
- IS war Sharpe 1,13, aber verzerrt.
- Hold-out: Sharpe 0,17 (+1,4 bp/Tag), unter der unteren IS-Grenze von +4,6 bp/Tag.
- Nur V-VOL (US500-Long mit Vola-Steuerung) hielt.
- Der Hold-out von Nr. 9, 10, 14 und 24 ist damit verbraucht.

| Dokument | Inhalt |
|---|---|
| [docs/00_Recherche.md](docs/00_Recherche.md) | Bausteine, Auswahlverzerrung |
| [docs/01_Vorregistrierung.md](docs/01_Vorregistrierung.md) | Gewichtung, Hold-out- und FTMO-Kriterien, Trial-Log |
| [docs/02_Ergebnisse.md](docs/02_Ergebnisse.md) | Ergebnis und Einordnung |
| [research/results/](research/results/) | vollständige Tabellen IS und Hold-out |

**Abhängigkeiten:** `../smart-money-concept` (`smc`), `../06-fx-carry`, `../09-pre-fomc-drift`, `../10-turn-of-the-month`, `../14-vol-managed-index`, `../24-fomc-fx`; venv aus dem SMC-Projekt.

```sh
cd research
../../smart-money-concept/research/.venv/bin/python -I scripts/run_s.py              # In-Sample (T306)
../../smart-money-concept/research/.venv/bin/python -I scripts/run_s.py --holdout    # Hold-out (T307), genau einmal
../../smart-money-concept/research/.venv/bin/python -I -m pytest -q tests/           # Tests
```
