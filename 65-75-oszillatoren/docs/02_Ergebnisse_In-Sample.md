# Ergebnisse Strategien Nr. 65–68, 74, 75 – Modell OS „Oszillatoren, Divergenzen, Renko“

Stand: 24.10.2026

Grundlagen:
- Regeln: unverändert aus der Vorregistrierung `docs/01_Vorregistrierung.md` (Commit `0da39b8`)
- Code: `research/osc/`, Lauf `research/scripts/run_os.py`; 4 Tests grün
- In-Sample: Einstiege 2015–2023, 17 Instrumente, 0,25 % Risiko je Trade
- Vollständige Tabellen: `research/results/os_in_sample.md`

## 1. Ergebnis

**Alle sechs Regeln sind nach Kosten negativ. Die Strategien Nr. 65–68, 74 und 75 sind damit gescheitert.** Der Hold-out bleibt unberührt, T255–T266 entfallen.

| Variante | Nr. | TF | Trades | Netto bp/Tag | vor Kosten bp/Tag | Ø R vor / nach Kosten | t | Jahre + | Instr. + |
|---|---|---|---|---|---|---|---|---|---|
| OS-RSI | 65 | H1 | 20.824 | −15,78 | −2,74 | −0,012 / −0,071 | −7,78 | 0 | 0 |
| OS-STOCH | 66 | H1 | 40.271 | −29,84 | −3,86 | −0,009 / −0,069 | −10,60 | 0 | 0 |
| OS-WPR | 67 | H1 | 77.419 | −50,26 | −1,03 | −0,001 / −0,061 | −16,77 | 0 | 0 |
| OS-CCI | 68 | H4 | 11.909 | −2,92 | +2,52 | +0,020 / −0,023 | −1,34 | 2 | 5 |
| OS-RENKO | 74 | H1 | 9.839 | −4,71 | +1,39 | +0,013 / −0,045 | −1,94 | 3 | 4 |
| OS-DIV | 75 | H4 | 1.629 | −1,59 | −0,75 | −0,043 / −0,091 | −2,59 | 2 | 4 |

## 2. Einordnung

- **Oszillator-Umkehr (RSI, Stochastik, Williams %R auf H1):** Schon vor Kosten bei null oder negativ. Wegen der vielen Signale summieren sich die Kosten auf −16 bis −50 bp je Tag (0 von 17 Instrumenten positiv).
- **CCI-Momentum und Renko:** Vor Kosten eine Spur von Trend (+0,01 bis +0,02 R), wie bei den Trendindikatoren in Nr. 61–76. Nach Kosten negativ.
- **RSI-Divergenzen:** Schon vor Kosten negativ (−0,04 R). Eine Divergenz an einem neuen Tief kündigt eher eine Fortsetzung an als eine Umkehr.
- **Fazit zu Abschnitt C:** 16 klassische Indikatorregeln, keine mit Netto-Edge. Trendindikatoren liegen vor Kosten leicht im Plus, Umkehrindikatoren bei null.

## 3. Trial-Log (Fortsetzung)

| # | Datum | Test | Ergebnis |
|---|---|---|---|
| T249 | 24.10.2026 | OS-RSI (65), In-Sample | nicht bestanden: −15,8 bp/Tag, t −7,78 |
| T250 | 24.10.2026 | OS-STOCH (66), In-Sample | nicht bestanden: −29,8 bp/Tag, t −10,60 |
| T251 | 24.10.2026 | OS-WPR (67), In-Sample | nicht bestanden: −50,3 bp/Tag, t −16,77 |
| T252 | 24.10.2026 | OS-CCI (68), In-Sample | nicht bestanden: −2,92 bp/Tag, t −1,34 |
| T253 | 24.10.2026 | OS-RENKO (74), In-Sample | nicht bestanden: −4,71 bp/Tag, t −1,94 |
| T254 | 24.10.2026 | OS-DIV (75), In-Sample | nicht bestanden: −1,59 bp/Tag, t −2,59 |
| T255–T266 | – | Hold-out, FTMO | entfallen, Hold-out unberührt |
