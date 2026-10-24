# smcea – Smart-Money-Concept-EA für MetaTrader 5

Ziel: ein autonom handelnder MT5-Expert-Advisor nach dem Smart Money Concept (SMC/ICT), mit dem die **FTMO 2-Step Challenge (Swing, 100.000 USD)** bestanden werden soll. Instrumente:

- EURUSD, GBPUSD, USDJPY, AUDUSD, NZDUSD, USDCAD, USDCHF
- EURJPY, GBPJPY, AUDJPY, NZDJPY, CADJPY, CHFJPY
- EURCAD, EURCHF, EURNZD, EURAUD
- GBPCHF, GBPNZD, GBPCAD, GBPAUD
- AUDNZD, AUDCAD, CADCHF
- XAUUSD

**Status (24.10.2026):**
- **Research-Pipeline in Python steht:** Daten 2014–2026 von HistData, kausale SMC-Engine, 31 Tests.
- **Gate P2 (Ereignisstudie) ist ausgewertet:** Kein Baustein ist allein nach Kosten profitabel. Das ICT-Kernmodell (Sweep → MSS) zeigt keinen Effekt. Einziger Kandidat ist Trend-Fortsetzung (Modell C). Details stehen in `docs/03_Ergebnisse_P2_Ereignisstudie.md`.
- **Nächster Schritt:** P3, ein vorregistrierter Test von Modell C.
- **MQL5-Code:** noch keiner.

| Dokument | Inhalt |
|---|---|
| [docs/00_SMC_Deepsearch_Zusammenfassung.md](docs/00_SMC_Deepsearch_Zusammenfassung.md) | **Einstieg:** Kernerkenntnisse, Begriffslandkarte (Konzept → EA-Regel), Evidenz, Instrumente, Plattform-Fallstricke |
| [docs/01_EA_Blueprint.md](docs/01_EA_Blueprint.md) | EA-Spezifikation v0.1: Architektur, Zeitmodell, Engines, Modelle, Risiko, Filter, Instrument-Konfiguration, Validierungsplan, Roadmap |
| [docs/02_FTMO_Challenge_Plan.md](docs/02_FTMO_Challenge_Plan.md) | FTMO-Modus: Regelwerk, Monte-Carlo-Bestehenschancen, Risikoleiter, FtmoGuard, Margin und Kosten, Ablauf bis zum Kauf |
| [docs/03_Ergebnisse_P2_Ereignisstudie.md](docs/03_Ergebnisse_P2_Ereignisstudie.md) | Ergebnisse der Ereignisstudie (Gate P2) und Vorschlag für P3 |
| [docs/research/](docs/research/) | 8 ausführliche Research-Kapitel mit Pseudocode und Quellen |
| [research/smc/](research/smc/) | Python-Referenz-Engine: Zeitmodell, Daten, Struktur, Zonen, Liquidität, MSS, Ereignisstudie |
| [research/ftmo_mc.py](research/ftmo_mc.py) | Monte-Carlo-Simulation der Challenge; Ergebnisse in `research/results/ftmo_mc_results.md` |

Einrichtung und Abläufe:

```sh
python3 -m venv research/.venv && research/.venv/bin/pip install -r research/requirements.txt   # einmalig
research/.venv/bin/python -I research/scripts/download_histdata.py      # M1-Daten laden (≈ 45 min, fortsetzbar)
research/.venv/bin/python -I research/scripts/build_data.py             # Bars M5..D1 in FTMO-Serverzeit (≈ 2 min)
research/.venv/bin/python -I research/scripts/run_event_study.py        # Ereignisstudie P2 (≈ 15 min)
research/.venv/bin/python -I research/ftmo_mc.py                        # FTMO-Monte-Carlo (≈ 4 min)
cd research && .venv/bin/python -I -m pytest -q tests/                  # Tests
```
