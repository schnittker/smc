# Ergebnisse Strategien Nr. 48 und 49 – Modell LV „Intraday-Level“

Stand: 24.10.2026

Grundlagen:
- Regeln: unverändert aus der Vorregistrierung `docs/01_Vorregistrierung.md` (Commit `66d7d2e`)
- Code: `research/lvl/`, Lauf `research/scripts/run_lv.py` (Commit `b6be561`, danach nur eine Performance-Korrektur ohne Logikänderung); 5 Tests grün
- In-Sample: 2015–2023, 0,25 % Risiko je Trade
- Vollständige Tabellen: `research/results/lv_in_sample.md`

## 1. Ergebnis

**Alle drei Varianten sind schon vor Kosten bei null oder negativ. Die Strategien Nr. 48 und 49 sind damit gescheitert.** Der Hold-out bleibt unberührt, T168–T173 entfallen.

| Kennzahl | LV-VA80 (48) | LV-PFADE (49) | LV-PBRK (49) |
|---|---|---|---|
| Netto je Tag (bp des Kapitals) | **−0,83** | **−12,63** | **−4,25** |
| vor Kosten je Tag | +0,07 | −1,76 | −1,91 |
| t-Wert (kleinster) | −2,10 | −7,30 | −3,26 |
| Jahre positiv | 3 von 9 | 0 von 9 | 1 von 9 |
| Instrumente positiv | 1 von 4 | 0 von 14 | 2 von 14 |
| Trades (9 Jahre) | 1.800 | 24.300 | 3.866 |
| Ø R je Trade vor Kosten / netto | +0,004 / −0,042 | −0,005 / −0,048 | −0,045 / −0,101 |
| Ausstiege Ziel / Stop / Zeit | 45 % / 26 % / 29 % | 29 % / 38 % / 32 % | – / 42 % / 58 % |

## 2. Einordnung

- **80-%-Regel:** Die Value Area wird zwar in 45 % der Fälle durchquert, also deutlich seltener als die behaupteten 80 %. Der Gewinn reicht nur, um die Stops auszugleichen. Vor Kosten bleibt praktisch null.
- **Pivot-Fade:** An S1/R1 prallt der Kurs nicht systematisch ab, vor Kosten ergibt sich −0,005 R. Die Order wird an etwa drei von vier Tagen ausgelöst, das Kostenvolumen ist entsprechend hoch.
- **Pivot-Ausbruch:** Ausbrüche über R3/S3 laufen nicht weiter, sie kehren eher um (−0,045 R vor Kosten).
- Die Befunde passen zu Osler (2000): Veröffentlichte Level haben höchstens einen winzigen, kurzlebigen Effekt. Bei FTMO-Kosten ist er nicht handelbar.

## 3. Trial-Log (Fortsetzung)

| # | Datum | Test | Ergebnis |
|---|---|---|---|
| T165 | 24.10.2026 | LV-VA80, In-Sample | nicht bestanden: −0,83 bp/Tag, t −2,10 |
| T166 | 24.10.2026 | LV-PFADE, In-Sample | nicht bestanden: −12,6 bp/Tag, t −7,30 |
| T167 | 24.10.2026 | LV-PBRK, In-Sample | nicht bestanden: −4,25 bp/Tag, t −3,26 |
| T168–T173 | – | Hold-out, FTMO | entfallen, Hold-out unberührt |
