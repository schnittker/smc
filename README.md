# smcea – Smart-Money-Concept-EA für MetaTrader 5

Ziel: ein autonom handelnder MT5-Expert-Advisor nach dem Smart Money Concept (SMC/ICT), mit dem die **FTMO 2-Step Challenge (Swing, 100.000 USD)** bestanden werden soll. Instrumente:

- EURUSD, GBPUSD, USDJPY, AUDUSD, NZDUSD, USDCAD, USDCHF
- EURJPY, GBPJPY, AUDJPY, NZDJPY, CADJPY, CHFJPY
- EURCAD, EURCHF, EURNZD, EURAUD
- GBPCHF, GBPNZD, GBPCAD, GBPAUD
- AUDNZD, AUDCAD, CADCHF
- XAUUSD

**Status (24.10.2026):**
- **Research-Pipeline in Python steht:** Daten 2014–2026 von HistData, kausale SMC-Engine, Kosten- und Swap-Modell, 50 Tests.
- **Gate P2 (Ereignisstudie):** Kein SMC-Baustein ist allein nach Kosten profitabel. Das ICT-Kernmodell (Sweep → MSS) zeigt keinen Effekt (`docs/03`).
- **P3, Modell C (Trend-Fortsetzung): gescheitert** mit +0,015 R bzw. −0,016 R netto pro Trade (`docs/05`).
- **P4, Modell D (Trendfolge mit Struktur-Exit): gescheitert** mit −0,040 R netto pro Trade (`docs/07`).
- **Damit ist der SMC-Ansatz laut Vorregistrierung beendet.** Der Hold-out 2024–2026 ist unberührt.
- **Nächster Schritt:** Entscheidung zwischen einer anderen Strategieklasse (z. B. Fixing-Effekt) und Pausieren. Keine bezahlte Challenge ohne bestandenen Test.
- **MQL5-Code:** keiner.

| Dokument | Inhalt |
|---|---|
| [docs/00_SMC_Deepsearch_Zusammenfassung.md](docs/00_SMC_Deepsearch_Zusammenfassung.md) | **Einstieg:** Kernerkenntnisse, Begriffslandkarte (Konzept → EA-Regel), Evidenz, Instrumente, Plattform-Fallstricke |
| [docs/01_EA_Blueprint.md](docs/01_EA_Blueprint.md) | EA-Spezifikation v0.1: Architektur, Zeitmodell, Engines, Modelle, Risiko, Filter, Instrument-Konfiguration, Validierungsplan, Roadmap |
| [docs/02_FTMO_Challenge_Plan.md](docs/02_FTMO_Challenge_Plan.md) | FTMO-Modus: Regelwerk, Monte-Carlo-Bestehenschancen, Risikoleiter, FtmoGuard, Margin und Kosten, Ablauf bis zum Kauf |
| [docs/03_Ergebnisse_P2_Ereignisstudie.md](docs/03_Ergebnisse_P2_Ereignisstudie.md) | Ergebnisse der Ereignisstudie (Gate P2) und Vorschlag für P3 |
| [docs/04_P3_Vorregistrierung_ModellC.md](docs/04_P3_Vorregistrierung_ModellC.md) | Vorregistrierung P3: Regeln, Varianten und Akzeptanzkriterien von Modell C |
| [docs/05_Ergebnisse_P3_ModellC.md](docs/05_Ergebnisse_P3_ModellC.md) | Ergebnis P3 (gescheitert), Diagnose, Optionen für den nächsten Schritt |
| [docs/06_P4_Vorregistrierung_ModellD.md](docs/06_P4_Vorregistrierung_ModellD.md) | Vorregistrierung P4: Modell D, Kostenmodell mit Swaps, Portfolio- und FTMO-Simulation |
| [docs/07_Ergebnisse_P4_ModellD.md](docs/07_Ergebnisse_P4_ModellD.md) | Ergebnis P4 (gescheitert), Gesamtbild P2–P4, Optionen |
| [docs/research/](docs/research/) | 8 ausführliche Research-Kapitel mit Pseudocode und Quellen |
| [research/smc/](research/smc/) | Python-Referenz-Engine: Zeitmodell, Daten, Struktur, Zonen, Liquidität, MSS, Ereignisstudie, Modelle C und D, Swaps |
| [research/ftmo_mc.py](research/ftmo_mc.py) | Monte-Carlo-Simulation der Challenge; Ergebnisse in `research/results/ftmo_mc_results.md` |

Einrichtung und Abläufe:

```sh
python3 -m venv research/.venv && research/.venv/bin/pip install -r research/requirements.txt   # einmalig
research/.venv/bin/python -I research/scripts/download_histdata.py      # M1-Daten laden (≈ 45 min, fortsetzbar)
research/.venv/bin/python -I research/scripts/build_data.py             # Bars M5..D1 in FTMO-Serverzeit (≈ 2 min)
research/.venv/bin/python -I research/scripts/run_event_study.py        # Ereignisstudie P2 (≈ 15 min)
research/.venv/bin/python -I research/scripts/run_p3.py                  # Modell C In-Sample, P3 (≈ 1 min, nach der Ereignisstudie)
research/.venv/bin/python -I research/scripts/download_rates.py          # Zinsreihen für Swaps (FRED)
research/.venv/bin/python -I research/scripts/run_p4.py                  # Modell D In-Sample, P4 (≈ 1 min)
research/.venv/bin/python -I research/ftmo_mc.py                        # FTMO-Monte-Carlo (≈ 4 min)
cd research && .venv/bin/python -I -m pytest -q tests/                  # Tests
```
