# Kontrollen Nr. 98 und 99 – Zufalls-Einstiege und Mondphasen (Placebo)

Teil der Testreihe `../STRATEGIEN.md`. Die beiden Regeln ohne ökonomische Begründung kalibrieren die Pipeline und müssen scheitern:
- **Nr. 98:** Zufalls-Einstiege auf H4 mit derselben Engine und denselben Kosten wie Nr. 50/51
- **Nr. 99:** Long ab Neumond, Short ab Vollmond auf 34 Instrumenten

**Status (24.10.2026):** Vorregistrierung festgelegt, Test läuft.

| Dokument | Inhalt |
|---|---|
| [docs/00_Recherche.md](docs/00_Recherche.md) | Zweck, Erwartung |
| [docs/01_Vorregistrierung.md](docs/01_Vorregistrierung.md) | Regeln, Trial-Log |

**Abhängigkeiten:** `../smart-money-concept` (`smc`), `../50-51-sr-trendlinien` (`chart`) samt Abhängigkeiten, `../81-90-statistik` (`stm`); venv aus dem SMC-Projekt.

```sh
../smart-money-concept/research/.venv/bin/python -I research/scripts/run_pl.py                 # In-Sample (T297, T298)
cd research && ../../smart-money-concept/research/.venv/bin/python -I -m pytest -q tests/       # Tests
```
