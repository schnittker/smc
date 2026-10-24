# Ergebnisse Strategie Nr. 94 – Modell N „NFP-Straddle“

Stand: 24.10.2026

Grundlagen:
- Regeln: unverändert aus der Vorregistrierung `docs/01_Vorregistrierung.md` (Commit `d5442ea`)
- Code: `research/nws/`, Lauf `research/scripts/run_n.py`; 2 Tests grün (NFP-Termine inkl. Feiertagsregel)
- In-Sample: 105 NFP-Termine 2015–2023 (3 ohne M1-Daten), EURUSD, GBPUSD, USDJPY, XAUUSD
- Vollständige Tabellen: `research/results/n_in_sample.md`

## 1. Ergebnis

**Der Straddle ist nach den pessimistischen News-Kosten negativ und selbst bei normalen Kosten nicht signifikant. Strategie Nr. 94 ist damit gescheitert.** Der Hold-out bleibt unberührt, T304 und T305 entfallen.

| Kennzahl | N-NFP (vorregistriert, News-Kosten) | beschreibend: normale Kosten |
|---|---|---|
| Netto je Termin (bp des Kapitals, 4 Instrumente) | **−8,81** (t −1,22) | +4,28 (t 0,49) |
| vor Kosten je Termin | +5,35 | +6,72 |
| Ø R je Trade vor / nach Kosten | +0,121 / −0,199 | – / +0,102 |
| Auslösequote / Stops | 45 % / 59 % | |
| Jahre positiv / Instrumente positiv | 2 von 9 / 0 von 4 | |

## 2. Einordnung

- **Vor Kosten bringt der Straddle etwas** (+0,12 R je Trade). Die NFP-Bewegung trägt also, aber nur knapp und sehr ungleichmäßig: 2015 +490 bp, 2016 −449 bp.
- **Die Kosten zur Veröffentlichung sind das Problem:** Mit 5-fachem Spread und 0,03 % Slippage kostet ein Trade 0,32 R. Das ist das Dreifache des Vorteils.
- Selbst mit normalen Kosten (unrealistisch für 08:30) wäre t = 0,49. Bei nur 105 Terminen in 9 Jahren reicht das statistisch nicht.
- Die ⚠-Einschätzung der Liste bestätigt sich: Spreads und Slippage zur Veröffentlichung lassen sich nur grob abbilden, und sie entscheiden über das Ergebnis.

## 3. Trial-Log (Fortsetzung)

| # | Datum | Test | Ergebnis |
|---|---|---|---|
| T303 | 24.10.2026 | N-NFP, In-Sample | nicht bestanden: −8,81 bp/Termin, t −1,22 (normale Kosten +4,3, t 0,49) |
| T304, T305 | – | Hold-out, FTMO | entfallen, Hold-out unberührt |
