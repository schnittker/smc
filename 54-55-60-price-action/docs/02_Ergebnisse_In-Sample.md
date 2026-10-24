# Ergebnisse Strategien Nr. 54, 55 und 60 – Modell PA „Price Action“

Stand: 24.10.2026

Grundlagen:
- Regeln: unverändert aus der Vorregistrierung `docs/01_Vorregistrierung.md` (Commit `1183df7`)
- Code: `research/pa/` mit `chart.engine`, Lauf `research/scripts/run_pa.py`; 4 Tests grün
- In-Sample: Einstiege 2015–2023, 17 Instrumente, 0,25 % Risiko je Trade
- Vollständige Tabellen: `research/results/pa_in_sample.md`

## 1. Ergebnis

**Keine der vier Regeln besteht. Die Strategien Nr. 54, 55 und 60 sind damit gescheitert.** Der Hold-out bleibt unberührt, T193–T200 entfallen.

| Kennzahl | PA-PIN (54) | PA-ENG (54) | PA-DT (55) | PA-SD (60) |
|---|---|---|---|---|
| Netto je Tag (bp des Kapitals) | **−0,45** | **−5,80** | **−0,55** | **+0,15** |
| vor Kosten je Tag | +0,56 | −2,36 | −0,14 | +0,46 |
| t-Wert (kleinster) | −0,68 | −4,64 | −1,73 | 0,40 |
| Jahre positiv | 5 von 9 | 0 von 9 | 3 von 9 | 5 von 9 |
| Instrumente positiv | 6 von 17 | 3 von 17 | 5 von 17 | 8 von 17 |
| Trades (9 Jahre) | 1.825 | 6.276 | 1.571 | 473 |
| Ø R je Trade vor Kosten / netto | +0,029 / −0,023 | −0,035 / −0,087 | −0,009 / −0,033 | +0,092 / +0,031 |
| Ausstiege Ziel / Stop / Zeit | 30 % / 63 % / 7 % | 26 % / 64 % / 10 % | 50 % / 31 % / 19 % | 32 % / 64 % / 3 % |

## 2. Einordnung

- **Pin Bar und Engulfing:** Candlestick-Signale an Zonen haben keine Vorhersagekraft. Engulfing ist schon vor Kosten negativ und eher ein Fortsetzungs- als ein Umkehrsignal. Das deckt sich mit Marshall, Young & Rose (2006).
- **Doppelboden/-top:** Das Measured-Move-Ziel wird in 50 % der Fälle erreicht, der Stop in 31 %. Netto bleibt trotzdem nichts, weil das Ziel näher liegt als der Stop.
- **Supply/Demand:** Vor Kosten ergibt sich +0,09 R je Trade, das ist der höchste Wert der Gruppe. Bei nur 473 Trades in 9 Jahren (≈ 3 je Instrument und Jahr) reicht das statistisch nicht: t 0,40, und bei doppelten Kosten negativ. Mit SMC (Nr. 1) war das Bild ähnlich. Eine eigene Folgestudie hat keine Grundlage.

## 3. Trial-Log (Fortsetzung)

| # | Datum | Test | Ergebnis |
|---|---|---|---|
| T189 | 24.10.2026 | PA-PIN, In-Sample | nicht bestanden: −0,45 bp/Tag, t −0,68 |
| T190 | 24.10.2026 | PA-ENG, In-Sample | nicht bestanden: −5,80 bp/Tag, t −4,64 |
| T191 | 24.10.2026 | PA-DT, In-Sample | nicht bestanden: −0,55 bp/Tag, t −1,73 |
| T192 | 24.10.2026 | PA-SD, In-Sample | nicht bestanden: +0,15 bp/Tag, t 0,40 |
| T193–T200 | – | Hold-out, FTMO | entfallen, Hold-out unberührt |
