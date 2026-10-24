# Strategien Nr. 81, 82, 85, 90 – Statistische Modelle (HMM, GARCH, k-NN, Gold-Saisonalität)

Teil der Testreihe `../STRATEGIEN.md`. Ziel ist ein autonomer MT5-EA für die FTMO 2-Step-Challenge (Swing, 100.000 USD). Feste Rahmenbedingungen: 10 % max. Verlust, 5 % max. Tagesverlust, Ziele +10 % / +5 %, News und Wochenende erlaubt.

**Idee:** Tagesbuchhaltung auf 34 Instrumenten:
- **HMM-Regimefilter** für eine 20-Tage-Trendregel
- **GARCH-Vol-Prognose** für deren Größe
- **k-NN-Analogien** der letzten 10 Tagesrenditen

Dazu kommt Gold long im September und November. Alle Modelle werden jährlich nur mit vergangenen Daten geschätzt.

**Status (24.10.2026):** Vorregistrierung festgelegt, Test läuft.

| Dokument | Inhalt |
|---|---|
| [docs/00_Recherche.md](docs/00_Recherche.md) | Idee, Quellen, Erwartung |
| [docs/01_Vorregistrierung.md](docs/01_Vorregistrierung.md) | Regeln, Varianten, Akzeptanzkriterien, Trial-Log |

**Abhängigkeiten:** `../smart-money-concept` (`smc`; venv mit scipy und scikit-learn), `../06-fx-carry` (`carry`), `../28-30-kanal-ausbruch` (`brk`).

```sh
../smart-money-concept/research/.venv/bin/python -I research/scripts/run_st.py                    # In-Sample (T276–T279)
../smart-money-concept/research/.venv/bin/python -I research/scripts/run_st.py --holdout ST-HMM    # Hold-out, genau einmal
cd research && ../../smart-money-concept/research/.venv/bin/python -I -m pytest -q tests/          # Tests
```
