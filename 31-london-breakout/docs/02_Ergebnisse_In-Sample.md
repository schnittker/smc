# Ergebnisse Strategie Nr. 31 – Modell L „London Breakout“

Stand: 24.10.2026

Grundlagen:
- Regeln: unverändert aus der Vorregistrierung `docs/01_Vorregistrierung.md` (Commit `c695078`)
- Code: `research/lbo/`, Lauf `research/scripts/run_l.py` (Commit `57ca4f7`); 4 Tests grün
- In-Sample: Handelstage 2015–2023
- Vollständige Tabellen: `research/results/l_in_sample.md`

## 1. Ergebnis

**Beide Varianten verfehlen das Hauptkriterium deutlich. Strategie Nr. 31 ist damit gescheitert.** Der Hold-out bleibt unberührt, T108 und T109 entfallen.

| Kriterium | Schwelle | L-GBP | L-EUR |
|---|---|---|---|
| Netto je Tag (bp des Kapitals, Risiko 0,5 %) | > 0 | +0,75 | **−1,46** |
| t-Wert (kleinster aus iid, Woche, Monat) | ≥ 3,0 | **0,47** | **−1,01** |
| Sharpe Ratio p. a. | (≈ 1,0) | 0,16 | −0,34 |
| Jahre positiv | ≥ 6 von 9 | 5 von 9 | **4 von 9** |
| bei doppelten Kosten | > 0 | **−1,39** | **−3,98** |
| Ø R je Trade netto / vor Kosten | – | +0,015 / +0,059 | −0,030 / +0,022 |
| Trefferquote / Stop / Tagesende | – | 37 % / 53 % / 47 % | 39 % / 51 % / 49 % |
| Median Asien-Range | – | 21,8 bp | 20,3 bp |

## 2. Einordnung

- **Ausbrüche aus der Asien-Range setzen sich nicht verlässlich fort.** Vor Kosten bleiben +0,02 bis +0,06 R je Trade, netto nahezu null.
- **Die Kosten sind kleiner als beim Index-ORB (Nr. 16),** etwa 0,05 R statt 0,14–0,24 R, weil die Range mit etwa 20 bp größer ist. Den fehlenden Vorteil ersetzt das nicht.
- Beschreibend: Short-Ausbrüche lagen bei beiden Paaren etwas besser als Long (+0,08 bzw. +0,04 R netto). Das ist eine Nachauswertung ohne Vorhersagewert.

## 3. Trial-Log (Fortsetzung)

| # | Datum | Test | Ergebnis |
|---|---|---|---|
| T106 | 24.10.2026 | L-GBP, In-Sample | nicht bestanden: +0,75 bp/Tag, t 0,47 |
| T107 | 24.10.2026 | L-EUR, In-Sample | nicht bestanden: −1,46 bp/Tag, t −1,01 |
| T108 | – | Hold-out | entfällt, Hold-out unberührt |
| T109 | – | FTMO-Bootstrap | entfällt |
