# Ergebnisse Strategien Nr. 52 und 53 – Modell FC „Fibonacci-Pullback und Chandelier-Trend“

Stand: 24.10.2026

Grundlagen:
- Regeln: unverändert aus der Vorregistrierung `docs/01_Vorregistrierung.md` (Commit `e257df1`)
- Code: `research/fch/` (dazu `chart.engine` mit Ziel-Level), Lauf `research/scripts/run_fc.py`; 3 Tests grün
- In-Sample: Einstiege 2015–2023, 17 Instrumente, 0,25 % Risiko je Trade
- Vollständige Tabellen: `research/results/fc_in_sample.md`

## 1. Ergebnis

**Beide Regeln liegen nach Kosten im Minus. Die Strategien Nr. 52 und 53 sind damit gescheitert.** Der Hold-out bleibt unberührt, T185–T188 entfallen.

| Kennzahl | FC-FIB (52) | FC-CHAND (53) |
|---|---|---|
| Netto je Tag (bp des Kapitals) | **−1,76** | **−0,14** |
| vor Kosten je Tag | −0,40 | +0,20 |
| t-Wert (kleinster) | −2,69 | −0,38 |
| Jahre positiv | 2 von 9 | 2 von 9 |
| Instrumente positiv | 7 von 17 | 6 von 17 |
| Trades (9 Jahre) | 3.490 | 938 |
| Ø R je Trade vor Kosten / netto | −0,011 / −0,047 | +0,020 / −0,014 |
| Ausstiege Ziel / Stop / Zeit | 42 % / 48 % / 10 % | – / 99 % / – |
| Ø Haltedauer | 11,7 H4-Kerzen | 19,5 Tage |

## 2. Einordnung

- **Fibonacci:** Das Impulshoch wird in 42 % der Fälle erreicht. Das entspricht etwa dem Zufallsverhältnis bei rund 1 : 1,2 zwischen Ziel- und Stopabstand. Die 50–61,8-%-Zone hat keine besondere Wirkung.
- **Chandelier:** Der Trailing-Stop verbessert die Turtle-Regel gegenüber Nr. 30 (dort Sharpe −0,54). Vor Kosten bleibt aber nur +0,02 R, mit nur 2 positiven Jahren; 2020 macht den Großteil aus.
- **Fazit:** Trendfolge auf D1 ist mit allen getesteten Ein- und Ausstiegen (Momentum, Kanäle, Chandelier) 2015–2023 bestenfalls neutral.

## 3. Trial-Log (Fortsetzung)

| # | Datum | Test | Ergebnis |
|---|---|---|---|
| T183 | 24.10.2026 | FC-FIB, In-Sample | nicht bestanden: −1,76 bp/Tag, t −2,69 |
| T184 | 24.10.2026 | FC-CHAND, In-Sample | nicht bestanden: −0,14 bp/Tag, t −0,38 |
| T185–T188 | – | Hold-out, FTMO | entfallen, Hold-out unberührt |
