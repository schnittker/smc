# Strategien Nr. 77, 79, 80 – Harmonische Muster, Wyckoff-Spring, M5-Scalping (Nr. 78 nicht formalisierbar)

Teil der Testreihe `../STRATEGIEN.md`. Ziel ist ein autonomer MT5-EA für die FTMO 2-Step-Challenge (Swing, 100.000 USD). Feste Rahmenbedingungen: 10 % max. Verlust, 5 % max. Tagesverlust, Ziele +10 % / +5 %, News und Wochenende erlaubt.

**Idee:**
- Gartley/Bat-Muster aus H4-Swings
- falsche Ausbrüche aus H4-Handelsspannen (Spring/Upthrust)
- EMA-9/21-Scalps auf M5 der Majors in der London/NY-Sitzung

Elliott-Wellen (Nr. 78) werden mangels eindeutiger Formalisierung nicht getestet.

**Status (24.10.2026):** Vorregistrierung festgelegt, Test läuft.

| Dokument | Inhalt |
|---|---|
| [docs/00_Recherche.md](docs/00_Recherche.md) | Idee, Formalisierbarkeit, Quellen |
| [docs/01_Vorregistrierung.md](docs/01_Vorregistrierung.md) | Regeln, Varianten, Akzeptanzkriterien, Trial-Log |

**Abhängigkeiten:** `../smart-money-concept` (`smc`), `../33-35-tagesausbruch` (`dbo`), `../36-38-h4-kanalausbruch` (`hkb`), `../50-51-sr-trendlinien` (`chart`), `../61-76-trendindikatoren` (`tind`), `../65-75-oszillatoren` (`osc`), `../05-monatsend-rebalancing` (`mer`); venv aus dem SMC-Projekt.

```sh
../smart-money-concept/research/.venv/bin/python -I research/scripts/run_hp.py                    # In-Sample (T267–T269)
../smart-money-concept/research/.venv/bin/python -I research/scripts/run_hp.py --holdout HP-HARM   # Hold-out, genau einmal
cd research && ../../smart-money-concept/research/.venv/bin/python -I -m pytest -q tests/          # Tests
```
