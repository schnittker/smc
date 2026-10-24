# Ergebnisse Strategie Nr. 27 – Modell S „Halloween US-Indizes“

Stand: 24.10.2026

Grundlagen:
- Regeln: unverändert aus der Vorregistrierung `docs/01_Vorregistrierung.md` (Commit `f4dad36`)
- Code: `research/hallo/`, Lauf `research/scripts/run_s.py` (Commit `43233d4`); 1 Test grün
- In-Sample: Handelstage 2015–2023
- Vollständige Tabellen: `research/results/s_in_sample.md`

## 1. Ergebnis

**Beide Varianten verfehlen das Hauptkriterium. Strategie Nr. 27 ist damit gescheitert.** Der Hold-out 2024–2026 bleibt unberührt, T94 und T95 entfallen.

| Kriterium | Schwelle | S-SPX | S-NDX |
|---|---|---|---|
| Sharpe Ratio p. a. netto | (≈ 1,0) | **0,37** | **0,47** |
| t-Wert (kleinster aus iid, Woche, Monat) | ≥ 3,0 | **1,08** | **1,39** |
| Jahre positiv | ≥ 6 von 9 | 6 von 9 | 6 von 9 |
| Teilzeiträume | beide > 0 | ja | ja |
| bei doppelten Kosten | > 0 | ja | ja |
| Referenz: ganzjährig halten (Sharpe) | – | 0,51 | 0,69 |

## 2. Einordnung

- **Kein Halloween-Effekt 2015–2023.** Die mittlere Tagesrendite im Winterhalbjahr liegt nur wenig über der im Sommer (US500 +5,4 gegenüber +3,1 bp, t 0,50; US100 +7,3 gegenüber +6,4 bp, t 0,17).
- Die Strategie verdient deshalb etwa die halbe Aktienprämie bei halber Zeit im Markt und liegt in der Sharpe Ratio **unter** dem ganzjährigen Halten.
- Mit 9 Wintern ist ohnehin keine belastbare Aussage über einen Halbjahreseffekt möglich.

## 3. Trial-Log (Fortsetzung)

| # | Datum | Test | Ergebnis |
|---|---|---|---|
| T92 | 24.10.2026 | S-SPX, In-Sample | nicht bestanden: Sharpe 0,37, t 1,08 |
| T93 | 24.10.2026 | S-NDX, In-Sample | nicht bestanden: Sharpe 0,47, t 1,39 |
| T94 | – | Hold-out | entfällt, Hold-out unberührt |
| T95 | – | FTMO-Bootstrap | entfällt |
