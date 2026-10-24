# Ergebnisse Strategien Nr. 50 und 51 – Modell SR „S/R-Zonen und Trendlinien“

Stand: 24.10.2026

Grundlagen:
- Regeln: unverändert aus der Vorregistrierung `docs/01_Vorregistrierung.md` (Commit `5cbe8f2`)
- Code: `research/chart/` (Swings, Engine, Signale), Lauf `research/scripts/run_sr.py`; 5 Tests grün
- In-Sample: Einstiege 2015–2023, 17 Instrumente, 0,25 % Risiko je Trade
- Vollständige Tabellen: `research/results/sr_in_sample.md`

## 1. Ergebnis

**Alle drei Varianten liegen vor Kosten bei null und sind nach Kosten deutlich negativ. Die Strategien Nr. 50 und 51 sind damit gescheitert.** Der Hold-out bleibt unberührt, T177–T182 entfallen.

| Kennzahl | SR-BOUNCE (50) | SR-BREAK (50) | SR-TLINE (51) |
|---|---|---|---|
| Netto je Tag (bp des Kapitals) | **−8,48** | **−6,97** | **−3,48** |
| vor Kosten je Tag | −2,08 | −0,71 | +0,09 |
| t-Wert (kleinster) | −4,85 | −3,74 | −2,81 |
| Jahre positiv | 1 von 9 | 1 von 9 | 2 von 9 |
| Instrumente positiv | 2 von 17 | 3 von 17 | 2 von 17 |
| Trades (9 Jahre) | 12.608 | 12.088 | 7.638 |
| Ø R je Trade vor Kosten / netto | −0,015 / −0,063 | −0,006 / −0,054 | +0,001 / −0,043 |
| Ausstiege Ziel / Stop / Zeit | 27 % / 63 % / 10 % | 28 % / 63 % / 9 % | 19 % / 51 % / 30 % |

## 2. Einordnung

- **Swing-basierte Zonen haben keine Wirkung.** Weder prallt der Kurs an ihnen ab noch bricht er durch sie hindurch. Ziel (2R) und Stop werden etwa im Zufallsverhältnis 1 : 2 erreicht.
- **Trendlinien-Ausbrüche:** Vor Kosten ergibt sich exakt null (+0,001 R).
- **Fazit:** Zusammen mit Nr. 48/49 haben jetzt fünf Level- und Linienregeln vor Kosten keinen messbaren Effekt. Chartformationen aus Swing-Punkten (Nr. 54, 55, 60) haben damit eine niedrige Vorab-Wahrscheinlichkeit.

## 3. Trial-Log (Fortsetzung)

| # | Datum | Test | Ergebnis |
|---|---|---|---|
| T174 | 24.10.2026 | SR-BOUNCE, In-Sample | nicht bestanden: −8,48 bp/Tag, t −4,85 |
| T175 | 24.10.2026 | SR-BREAK, In-Sample | nicht bestanden: −6,97 bp/Tag, t −3,74 |
| T176 | 24.10.2026 | SR-TLINE, In-Sample | nicht bestanden: −3,48 bp/Tag, t −2,81 |
| T177–T182 | – | Hold-out, FTMO | entfallen, Hold-out unberührt |
