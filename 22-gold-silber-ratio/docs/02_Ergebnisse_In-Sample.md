# Ergebnisse Strategie Nr. 22 – Modell G „Gold/Silber-Ratio“

Stand: 24.10.2026

Grundlagen:
- Regeln: unverändert aus der Vorregistrierung `docs/01_Vorregistrierung.md` (Commit `c6d5afa`)
- Code: `research/gsr/`, Lauf `research/scripts/run_g.py` (Commit `705de7b`); 2 Tests grün
- In-Sample: Handelstage 2015–2023, XAUUSD und XAGUSD
- Vollständige Tabellen: `research/results/g_in_sample.md`

## 1. Ergebnis

**Beide Varianten verfehlen alle Kriterien. Strategie Nr. 22 ist damit gescheitert.** Der Hold-out 2024–2026 bleibt unberührt, T78 und T79 entfallen.

| Kriterium | Schwelle | G-60 | G-250 |
|---|---|---|---|
| Sharpe Ratio p. a. netto | (≈ 1,0) | **−0,07** | **0,09** |
| t-Wert (kleinster aus iid, Woche, Monat) | ≥ 3,0 | **−0,22** | **0,25** |
| Jahre positiv | ≥ 6 von 9 | **3 von 9** | **5 von 9** |
| Teilzeiträume | beide > 0 | **nein** | **nein** |
| bei doppelten Kosten | > 0 | **nein** | **nein** |
| Trades / Trefferquote | – | 32 / 56 % | 10 / 50 % |
| Ø Haltedauer / Zeit im Markt | – | 41 Tage / 56 % | 152 Tage / 65 % |
| schlechtester Tag bei 10 % Vol. | – | −9,2 % | −9,0 % |

## 2. Einordnung

1. **Keine verlässliche Rückkehr der Ratio.** Vor Kosten bringt G-60 +0,5 % und G-250 +1,7 % p. a. (unskaliert). Swaps auf beide Beine (−0,8 %) und Handelskosten nehmen das fast vollständig weg.
2. **Wenige, lange Trades.** G-250 hat in 9 Jahren nur 10 Trades mit 152 Tagen Haltedauer. Eine statistische Aussage ist damit nicht möglich.
3. **Großes Einzelrisiko:** Schlechteste Tage um −9 % bei 10 % Volatilität, also Silber-Schocks (März 2020, Februar 2021 „Silver Squeeze“). Für die 5-%-Tagesgrenze ist das ungeeignet.
4. Passt zur Literatur: Die Kointegration von Gold und Silber ist seit den 1990ern schwach.

## 3. Trial-Log (Fortsetzung)

| # | Datum | Test | Ergebnis |
|---|---|---|---|
| T76 | 24.10.2026 | G-60, In-Sample | nicht bestanden: Sharpe −0,07, t −0,22 |
| T77 | 24.10.2026 | G-250, In-Sample | nicht bestanden: Sharpe 0,09, t 0,25 |
| T78 | – | Hold-out | entfällt, Hold-out unberührt |
| T79 | – | FTMO-Bootstrap | entfällt |
