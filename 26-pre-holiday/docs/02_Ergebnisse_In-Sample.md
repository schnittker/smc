# Ergebnisse Strategie Nr. 26 – Modell H „Pre-Holiday US-Indizes“

Stand: 24.10.2026

Grundlagen:
- Regeln: unverändert aus der Vorregistrierung `docs/01_Vorregistrierung.md` (Commit `d33868c`)
- Code: `research/preh/`, Lauf `research/scripts/run_h.py` (Commit `a405e31`); 2 Tests grün
- In-Sample: reguläre NYSE-Feiertage 2015–2023
- Vollständige Tabellen: `research/results/h_in_sample.md`

## 1. Ergebnis

**Beide Varianten verfehlen das Hauptkriterium und die Jahresschwelle. Strategie Nr. 26 ist damit gescheitert.** Der Hold-out 2024–2026 bleibt unberührt, T90 und T91 entfallen.

| Kriterium | Schwelle | H-SPX | H-NDX |
|---|---|---|---|
| Netto je Ereignis | > 0 | +13,9 bp | +10,6 bp |
| t-Wert (kleinster aus iid, Quartal) | ≥ 3,0 | **1,68** | **0,88** |
| Jahre positiv | ≥ 6 von 9 | **5 von 9** | **5 von 9** |
| Teilzeiträume | beide > 0 | ja | ja |
| bei doppelten Kosten | > 0 | ja | ja |

## 2. Einordnung

- Vortage von Feiertagen bringen vor Kosten etwa **15 bp mehr** als normale Handelstage (US500 +19,1 gegenüber +3,6 bp, t 1,81). Der Effekt aus Ariel (1990) ist also in abgeschwächter Form noch da.
- Mit etwa 80 Ereignissen und rund 1 % Tagesschwankung reicht das bei weitem nicht für t ≥ 3. Dafür bräuchte es etwa 35 bp netto je Ereignis.
- Gleiches Muster wie Nr. 10 (Monatswechsel): ein kleiner, positiver Kalendereffekt, der an der Statistik scheitert.

## 3. Trial-Log (Fortsetzung)

| # | Datum | Test | Ergebnis |
|---|---|---|---|
| T88 | 24.10.2026 | H-SPX, In-Sample | nicht bestanden: +13,9 bp/Ereignis, t 1,68 |
| T89 | 24.10.2026 | H-NDX, In-Sample | nicht bestanden: +10,6 bp/Ereignis, t 0,88 |
| T90 | – | Hold-out | entfällt, Hold-out unberührt |
| T91 | – | FTMO-Bootstrap | entfällt |
