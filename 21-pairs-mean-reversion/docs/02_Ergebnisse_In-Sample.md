# Ergebnisse Strategie Nr. 21 – Modell P „z-Score Mean Reversion AUDNZD / EURCHF“

Stand: 24.10.2026

Grundlagen:
- Regeln: unverändert aus der Vorregistrierung `docs/01_Vorregistrierung.md` (Commit `b9eb904`)
- Code: `research/pmr/`, Lauf `research/scripts/run_p.py` (Commit `756a6f3`); 4 Tests grün
- In-Sample: Handelstage 2015–2023
- Vollständige Tabellen: `research/results/p_in_sample.md`

## 1. Ergebnis

**Beide Varianten verfehlen das Hauptkriterium deutlich. Strategie Nr. 21 ist damit gescheitert.** Der Hold-out 2024–2026 bleibt unberührt, T74 und T75 entfallen.

| Kriterium | Schwelle | P-AUDNZD | P-EURCHF |
|---|---|---|---|
| Sharpe Ratio p. a. netto | (≈ 1,0) | **0,13** | **−0,20** |
| t-Wert (kleinster aus iid, Woche, Monat) | ≥ 3,0 | **0,40** | **−0,77** |
| Jahre positiv | ≥ 6 von 9 | 6 von 9 | **5 von 9** |
| Teilzeiträume | beide > 0 | **nein** | **nein** |
| bei doppelten Kosten | > 0 | **nein** | **nein** |
| Trades / Trefferquote | – | 34 / 62 % | 36 / 61 % |
| Ø Haltedauer / Zeit im Markt | – | 35 Tage / 50 % | 39 Tage / 60 % |
| schlechtester Tag bei 10 % Vol. | – | −4,3 % | **−24,8 %** |

## 2. Einordnung

1. **Kaum Mean Reversion nach Kosten.** Bei AUDNZD kehren 62 % der Abweichungen zurück, Kurs +2,0 % p. a. Swaps und Kosten nehmen davon 1 % p. a. weg. Übrig bleibt eine Sharpe Ratio von 0,13.
2. **EURCHF zeigt das Kernrisiko der Strategie.** Am 15.01.2015 hob die SNB den Mindestkurs auf. Die Long-Position (EURCHF war unter das Mittel gefallen) verlor in einem Monat 33 % (unskaliert), der schlechteste Tag lag bei −24,8 % bei 10 % Volatilität. Ohne Januar 2015 läge die Sharpe Ratio bei 0,02. Gerettet hätte das die Strategie also nicht, und ein solcher Tag würde jede FTMO-Challenge sofort beenden.
3. **Lange Haltedauern (35–39 Tage)** zeigen, dass die Rückkehr langsam ist. Die Crosses laufen oft wochenlang in Trends, bevor sie umkehren.

## 3. Trial-Log (Fortsetzung)

| # | Datum | Test | Ergebnis |
|---|---|---|---|
| T72 | 24.10.2026 | P-AUDNZD, In-Sample | nicht bestanden: Sharpe 0,13, t 0,40 |
| T73 | 24.10.2026 | P-EURCHF, In-Sample | nicht bestanden: Sharpe −0,20, t −0,77 |
| T74 | – | Hold-out | entfällt, Hold-out unberührt |
| T75 | – | FTMO-Bootstrap | entfällt |
