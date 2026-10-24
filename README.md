# smcea – Smart-Money-Concept-EA für MetaTrader 5

Ziel: ein autonom handelnder MT5-Expert-Advisor nach dem Smart Money Concept (SMC/ICT), mit dem die **FTMO 2-Step Challenge (Swing, 100.000 USD)** bestanden werden soll. Instrumente:

- EURUSD, GBPUSD, USDJPY, AUDUSD, NZDUSD, USDCAD, USDCHF
- EURJPY, GBPJPY, AUDJPY, NZDJPY, CADJPY, CHFJPY
- EURCAD, EURCHF, EURNZD, EURAUD
- GBPCHF, GBPNZD, GBPCAD, GBPAUD
- AUDNZD, AUDCAD, CADCHF
- XAUUSD

**Status (24.10.2026):**
- **Research-Pipeline in Python steht:** Daten 2014–2026 von HistData, kausale SMC-Engine, Kosten- und Swap-Modell, 59 Tests.
- **Vier vorregistrierte Tests, keiner bestanden:**
  - Gate P2, Ereignisstudie (`docs/03`): Kein SMC-Baustein ist allein nach Kosten profitabel.
  - P3, Modell C, Trend-Fortsetzung (`docs/05`): gescheitert.
  - P4, Modell D, Trendfolge mit Struktur-Exit (`docs/07`): gescheitert; damit ist der SMC-Ansatz beendet.
  - P5, Modell F, Fix-Reversal nach Krohn/Mueller/Whelan 2024 (`docs/09`): Der Effekt ist vorhanden, aber nur so groß wie die FTMO-Kosten; gescheitert.
- **Der Hold-out 2024–2026 ist unberührt.**
- **Empfehlung:** pausieren und keine Challenge kaufen, solange kein Modell alle Tests besteht.
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
| [docs/08_P5_Vorregistrierung_ModellF.md](docs/08_P5_Vorregistrierung_ModellF.md) | Vorregistrierung P5: Fix-Reversal (Fenster, Kosten, Varianten, FTMO-Regeln) |
| [docs/09_Ergebnisse_P5_ModellF.md](docs/09_Ergebnisse_P5_ModellF.md) | Ergebnis P5 (gescheitert), Gesamtbild P2–P5, Optionen |
| [docs/research/](docs/research/) | 8 ausführliche Research-Kapitel mit Pseudocode und Quellen |
| [research/smc/](research/smc/) | Python-Referenz-Engine: Zeitmodell, Daten, Struktur, Zonen, Liquidität, MSS, Ereignisstudie, Modelle C, D und F, Swaps |
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
research/.venv/bin/python -I research/scripts/run_p5.py                  # Modell F In-Sample, P5 (≈ 10 s)
research/.venv/bin/python -I research/ftmo_mc.py                        # FTMO-Monte-Carlo (≈ 4 min)
cd research && .venv/bin/python -I -m pytest -q tests/                  # Tests
```
