# Ergebnisse Strategien Nr. 61–64, 69–73, 76 – Modell TI „Trendindikatoren“

Stand: 24.10.2026

Grundlagen:
- Regeln: unverändert aus der Vorregistrierung `docs/01_Vorregistrierung.md` (Commit `c38801d`)
- Code: `research/tind/` (Indikatoren, Stop-and-Reverse-Engine), Lauf `research/scripts/run_ti.py`; 5 Tests grün
- In-Sample: Einstiege 2015–2023, 17 Instrumente, 0,25 % Risiko je Trade am Notfall-Stop (3 ATR)
- Vollständige Tabellen: `research/results/ti_in_sample.md`

## 1. Ergebnis

**Alle zehn Indikatoren sind nach Kosten negativ. Die Strategien Nr. 61–64, 69–73 und 76 sind damit gescheitert.** Der Hold-out bleibt unberührt, T229–T248 entfallen.

| Variante | Nr. | TF | Trades | Netto bp/Tag | vor Kosten bp/Tag | Ø R vor / nach Kosten | t | Jahre + | Instr. + |
|---|---|---|---|---|---|---|---|---|---|
| TI-MA200 | 61 | D1 | 221 | −0,52 | −0,18 | −0,077 / −0,220 | −1,39 | 4 | 5 |
| TI-EMA921 | 62 | H1 | 36.667 | −13,37 | +5,20 | +0,013 / −0,034 | −3,49 | 1 | 4 |
| TI-TRIPLE | 63 | H4 | 7.170 | −2,26 | +0,56 | +0,007 / −0,030 | −1,55 | 2 | 4 |
| TI-MACD | 64 | H4 | 17.852 | −3,84 | +1,78 | +0,009 / −0,020 | −1,89 | 3 | 4 |
| TI-ADX | 69 | H4 | 7.952 | −1,75 | +0,73 | +0,009 / −0,021 | −1,55 | 2 | 4 |
| TI-PSAR | 70 | H4 | 19.944 | −5,18 | +0,65 | +0,003 / −0,024 | −2,78 | 2 | 2 |
| TI-SUPER | 71 | H4 | 6.249 | −1,51 | +1,41 | +0,021 / −0,023 | −1,04 | 4 | 5 |
| TI-ICHI | 72 | H4 | 10.386 | −2,68 | +0,57 | +0,005 / −0,024 | −2,01 | 3 | 2 |
| TI-HA | 73 | H4 | 34.431 | −6,72 | +2,19 | +0,006 / −0,018 | −3,23 | 2 | 1 |
| TI-KALMAN | 76 | H4 | 12.526 | −3,12 | +1,31 | +0,010 / −0,023 | −1,72 | 2 | 4 |

## 2. Einordnung

- **Einheitliches Bild:** Vor Kosten bringen alle Intraday-Trendindikatoren +0,003 bis +0,021 R je Trade, also eine Spur von Trend. Kosten und Swaps kosten 0,025–0,05 R je Trade.
- Supertrend ist der beste (+0,021 R vor Kosten, 4 von 9 Jahren positiv), aber weit von t ≥ 3 entfernt.
- **Golden/Death Cross (D1):** Nur 221 Signale in 9 Jahren über 17 Instrumente, schon vor Kosten negativ.
- **Fazit:** Das deckt sich mit Sullivan, Timmermann & White (1999) und Neely et al. (2009). Klassische Trendindikatoren haben seit Jahrzehnten keinen Netto-Vorteil mehr. Für die FTMO-Kosten fehlt um den Faktor 2–5 Ertrag.

## 3. Trial-Log (Fortsetzung)

| # | Datum | Test | Ergebnis |
|---|---|---|---|
| T219 | 24.10.2026 | TI-MA200 (61), In-Sample | nicht bestanden: −0,52 bp/Tag, t −1,39 |
| T220 | 24.10.2026 | TI-EMA921 (62), In-Sample | nicht bestanden: −13,37 bp/Tag, t −3,49 |
| T221 | 24.10.2026 | TI-TRIPLE (63), In-Sample | nicht bestanden: −2,26 bp/Tag, t −1,55 |
| T222 | 24.10.2026 | TI-MACD (64), In-Sample | nicht bestanden: −3,84 bp/Tag, t −1,89 |
| T223 | 24.10.2026 | TI-ADX (69), In-Sample | nicht bestanden: −1,75 bp/Tag, t −1,55 |
| T224 | 24.10.2026 | TI-PSAR (70), In-Sample | nicht bestanden: −5,18 bp/Tag, t −2,78 |
| T225 | 24.10.2026 | TI-SUPER (71), In-Sample | nicht bestanden: −1,51 bp/Tag, t −1,04 |
| T226 | 24.10.2026 | TI-ICHI (72), In-Sample | nicht bestanden: −2,68 bp/Tag, t −2,01 |
| T227 | 24.10.2026 | TI-HA (73), In-Sample | nicht bestanden: −6,72 bp/Tag, t −3,23 |
| T228 | 24.10.2026 | TI-KALMAN (76), In-Sample | nicht bestanden: −3,12 bp/Tag, t −1,72 |
| T229–T248 | – | Hold-out, FTMO | entfallen, Hold-out unberührt |
