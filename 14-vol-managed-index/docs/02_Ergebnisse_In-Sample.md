# Ergebnisse Strategie Nr. 14 – Modell V „Volatilitätsgesteuertes US500-Long“

Stand: 24.10.2026

Grundlagen:
- Regeln: unverändert aus der Vorregistrierung `docs/01_Vorregistrierung.md` (Commit `f30bf47`)
- Code: `research/volm/`, Lauf `research/scripts/run_v.py` (Commit `3df7f95`); 4 Tests grün
- In-Sample: Handelstage 2015–2023, US500, Warm-up 2014
- Vollständige Tabellen: `research/results/v_in_sample.md`

## 1. Ergebnis

**Beide Varianten verfehlen das Hauptkriterium (t ≥ 3,0). Strategie Nr. 14 ist damit gescheitert.** Der Hold-out 2024–2026 bleibt unberührt, T50 und T51 entfallen.

| Kriterium | Schwelle | V-VOL (täglich, 15 % / σ21) | V-MM (monatlich, 15 %² / RV) | Referenz: US500 halten (w = 1) |
|---|---|---|---|---|
| Sharpe Ratio p. a. netto | (≈ 1,0) | **0,56** | **0,32** | 0,51 |
| t-Wert (kleinster aus iid, Woche, Monat) | ≥ 3,0 | **1,68** | **0,96** | 1,51 |
| Jahre positiv | ≥ 6 von 9 | 6 von 9 | **5 von 9** | 6 von 9 |
| Teilzeiträume | beide > 0 | ja | ja | ja |
| bei doppelten Kosten | > 0 | ja | ja | – |
| Rendite p. a. (unskaliert) | – | +9,5 % | +7,9 % | +8,9 % |
| Swaps p. a. (unskaliert) | – | −2,7 % | −3,4 % | −2,1 % |
| max. Drawdown bei 10 % Vol. | – | **15,8 %** | 17,9 % | 23,3 % |

## 2. Einordnung

1. **Die Steuerung verbessert die Sharpe Ratio kaum.** V-VOL liegt mit 0,56 nur knapp über dem bloßen Halten (0,51). V-MM nach Moreira & Muir liegt sogar darunter (0,32), weil es nach ruhigen Monaten mit bis zu dreifachem Hebel in Einbrüche lief (2015: −18,7 %, 2020: −4,6 % gegenüber +18,8 % beim Halten). Das passt zu Cederburg et al. (2020): Out-of-Sample bringt die Varianzsteuerung keinen systematischen Vorteil.
2. **Was sie bringt, ist ein kleinerer Drawdown.** Bei gleicher Volatilität (10 %) sinkt der maximale Drawdown bei V-VOL von 23 % auf 16 %. Für die FTMO-Grenze von 10 % ist das relevant, für die Profitabilität aber nicht.
3. **Die CFD-Finanzierung kostet 2–3,4 % p. a.** Bei einer Aktienprämie von etwa 11 % p. a. (Kurs) bleibt netto eine Sharpe Ratio um 0,5. Für t ≥ 3 in 9 Jahren bräuchte es etwa 1,0.
4. **US100** ist etwas stärker (V-VOL Sharpe 0,77, t 2,29; Halten 0,69), aber ebenfalls unter der Schwelle.

## 3. Bezug zu den festen Rahmenbedingungen

Diese Strategie liefert die **Referenz für alle Index-Strategien:** US500 halten bringt netto etwa Sharpe 0,5. Bei 10 % Volatilität sind das rund 5 % p. a. Für FTMO (+10 %, dann +5 %, bei höchstens 10 % Gesamtverlust) ist das zu langsam. Mit höherer Volatilität steigt die Gefahr, die Verlustgrenzen zu reißen.

## 4. Trial-Log (Fortsetzung)

| # | Datum | Test | Ergebnis |
|---|---|---|---|
| T48 | 24.10.2026 | V-VOL, In-Sample | nicht bestanden: Sharpe 0,56, t 1,68 |
| T49 | 24.10.2026 | V-MM, In-Sample | nicht bestanden: Sharpe 0,32, t 0,96 |
| T50 | – | Hold-out | entfällt, Hold-out unberührt |
| T51 | – | FTMO-Bootstrap | entfällt |

Referenz „Halten“ und US100 sind beschreibende Diagnosen, keine neuen Trials.
