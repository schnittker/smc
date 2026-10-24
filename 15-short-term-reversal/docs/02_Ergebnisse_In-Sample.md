# Ergebnisse Strategie Nr. 15 – Modell R „Kurzfrist-Reversal US500 (Connors)“

Stand: 24.10.2026

Grundlagen:
- Regeln: unverändert aus der Vorregistrierung `docs/01_Vorregistrierung.md` (Commit `1a8bf40`)
- Code: `research/strev/`, Lauf `research/scripts/run_r.py` (Commit `4fc65ec`); 5 Tests grün
- In-Sample: Handelstage 2015–2023, US500, Warm-up 2014
- Vollständige Tabellen: `research/results/r_in_sample.md`

## 1. Ergebnis

**Beide Varianten verfehlen das Hauptkriterium deutlich. Strategie Nr. 15 ist damit gescheitert.** Der Hold-out 2024–2026 bleibt unberührt, T54 und T55 entfallen.

| Kriterium | Schwelle | R-RSI2 | R-7S (Double 7s) | Referenz: US500 halten |
|---|---|---|---|---|
| Sharpe Ratio p. a. netto | (≈ 1,0) | **0,31** | **0,28** | 0,51 |
| t-Wert (kleinster aus iid, Woche, Monat) | ≥ 3,0 | **0,78** | **0,83** | 1,51 |
| Jahre positiv | ≥ 6 von 9 | 6 von 9 | **5 von 9** | 6 von 9 |
| Teilzeiträume | beide > 0 | ja | ja | ja |
| bei doppelten Kosten | > 0 | ja | ja | – |
| Trades / Trefferquote | – | 69 / 70 % | 88 / 77 % | – |
| Ø Ergebnis je Trade | – | +25,7 bp | +33,4 bp | – |
| Ø Haltedauer / Zeit im Markt | – | 3,8 Tage / 11 % | 8,5 Tage / 32 % | 100 % |
| Rendite p. a. (unskaliert) | – | +2,0 % | +3,3 % | +8,9 % |

## 2. Einordnung

1. **Die Charakteristik aus dem Buch bestätigt sich, die Profitabilität nicht.** Die Trefferquoten von 70–77 % und die positiven Trades stimmen mit Connors überein. Die Strategien sind aber nur 11 bzw. 32 % der Zeit im Markt und verdienen in dieser Zeit nicht genug, um das bloße Halten zu schlagen.
2. **Ertrag je Zeit im Markt höher, Risiko konzentriert.**
   - R-RSI2 verdient +2,0 % p. a. mit 11 % Marktzeit. Hochgerechnet auf volle Marktzeit wären das etwa 18 % p. a., gegenüber 8,9 % beim Halten.
   - Die Verluste kommen aber gebündelt: Rücksetzer, die sich zu Crashs ausweiten (2018, 2020, 2022), mit einem schlechtesten Tag von −5,9 % bei 10 % Volatilität. Dadurch bleibt die Sharpe Ratio niedrig.
3. **Kein Stop, wie im Original.** Genau die Trades in fallende Märkte hinein bestimmen das Risiko. Ein Stop würde die Regel verändern und wäre ein neuer Versuch.
4. **US100:** Sharpe 0,40 bzw. 0,37, ebenfalls unter dem Halten (0,69).

## 3. Bezug zu den festen Rahmenbedingungen

Für FTMO müsste man die Positionen hebeln, um die Ziele zu erreichen (2–3 % p. a. bei 1 × Kapital). Dann treffen die gebündelten Crash-Verluste direkt die 5-%-Tagesgrenze. Ungeeignet.

## 4. Trial-Log (Fortsetzung)

| # | Datum | Test | Ergebnis |
|---|---|---|---|
| T52 | 24.10.2026 | R-RSI2, In-Sample | nicht bestanden: Sharpe 0,31, t 0,78 |
| T53 | 24.10.2026 | R-7S, In-Sample | nicht bestanden: Sharpe 0,28, t 0,83 |
| T54 | – | Hold-out | entfällt, Hold-out unberührt |
| T55 | – | FTMO-Bootstrap | entfällt |

Trade-Statistik, Referenz und US100 sind beschreibende Diagnosen, keine neuen Trials.
