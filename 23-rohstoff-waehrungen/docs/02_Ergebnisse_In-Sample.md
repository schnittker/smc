# Ergebnisse Strategie Nr. 23 – Modell R „Rohstoff-Lead-Lag“

Stand: 24.10.2026

Grundlagen:
- Regeln: unverändert aus der Vorregistrierung `docs/01_Vorregistrierung.md` (Commit `e9edc1d`)
- Code: `research/cfx/`, Lauf `research/scripts/run_r.py` (Commit `c8bc1ce`); 2 Tests grün
- In-Sample: Handelstage 2015–2023
- Vollständige Tabellen: `research/results/r_in_sample.md`

## 1. Ergebnis

**Beide Varianten verfehlen das Hauptkriterium. Strategie Nr. 23 ist damit gescheitert.** Der Hold-out 2024–2026 bleibt unberührt, T82 und T83 entfallen.

| Kriterium | Schwelle | R-OEL (Brent → USDCAD) | R-GOLD (Gold → AUDUSD) |
|---|---|---|---|
| Sharpe Ratio p. a. netto | (≈ 1,0) | **−0,41** | **0,21** |
| t-Wert (kleinster aus iid, Woche, Monat) | ≥ 3,0 | **−1,23** | **0,63** |
| Jahre positiv | ≥ 6 von 9 | **2 von 9** | 6 von 9 |
| Teilzeiträume | beide > 0 | **nein** | ja |
| bei doppelten Kosten | > 0 | **nein** | **nein** |

## 2. Einordnung

| Korrelation der Tagesrenditen (beschreibend) | Brent / CAD | Gold / AUD |
|---|---|---|
| gleicher Tag | +0,42 | +0,38 |
| Signal heute → Währung morgen | +0,01 | +0,03 |

- **Genau das Bild der Literatur** (Ferraro, Rogoff & Rossi 2015): Rohstoff und Währung bewegen sich am selben Tag eng gemeinsam, mit einem Tag Verzögerung praktisch nicht.
- Die tägliche Umschichtung kostet bei R-GOLD 2,1 % p. a. und frisst den kleinen Kursvorteil (+5,3 % p. a. vor Kosten, unskaliert).
- Wie bei Nr. 19: Zusammenhänge, die gleichzeitig entstehen, sind mit Tagesschlusskursen nicht handelbar.

## 3. Trial-Log (Fortsetzung)

| # | Datum | Test | Ergebnis |
|---|---|---|---|
| T80 | 24.10.2026 | R-OEL, In-Sample | nicht bestanden: Sharpe −0,41, t −1,23 |
| T81 | 24.10.2026 | R-GOLD, In-Sample | nicht bestanden: Sharpe 0,21, t 0,63 |
| T82 | – | Hold-out | entfällt, Hold-out unberührt |
| T83 | – | FTMO-Bootstrap | entfällt |
