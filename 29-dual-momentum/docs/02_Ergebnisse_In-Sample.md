# Ergebnisse Strategie Nr. 29 – Modell D „Dual Momentum“

Stand: 24.10.2026

Grundlagen:
- Regeln: unverändert aus der Vorregistrierung `docs/01_Vorregistrierung.md` (Commit `8023fec`)
- Code: `research/dmom/`, Lauf `research/scripts/run_d.py` (Commit `9b6cd26`); 2 Tests grün
- In-Sample: Handelstage 2015–2023, 8 Anlagen
- Vollständige Tabellen: `research/results/d_in_sample.md`

## 1. Ergebnis

**Beide Varianten verfehlen das Hauptkriterium deutlich. Strategie Nr. 29 ist damit gescheitert.** Der Hold-out bleibt unberührt, T104 und T105 entfallen.

| Kriterium | Schwelle | D-TOP1 | D-TOP2 |
|---|---|---|---|
| Sharpe Ratio p. a. netto | (≈ 1,0) | **0,17** | **0,14** |
| t-Wert (kleinster aus iid, Woche, Monat) | ≥ 3,0 | **0,48** | **0,38** |
| Jahre positiv | ≥ 6 von 9 | **5 von 9** | **5 von 9** |
| Teilzeiträume | beide > 0 | ja | ja |
| bei doppelten Kosten | > 0 | ja | ja |
| Monate ganz in Cash | – | 6 von 107 | 6 von 107 |

Am häufigsten gewählt: US100 (43 bzw. 69 Monate), Gold (20 bzw. 31), JP225 (13 bzw. 28).

## 2. Einordnung

- **Die Rotation kostet mehr, als sie bringt.** US100 allein zu halten brachte 2015–2023 eine Sharpe Ratio von 0,69 (Nr. 14). Die Strategie war zwar meist in US100, wechselte aber regelmäßig zu spät in Gold oder andere Indizes und wieder zurück. Typisch für Momentum, das Wendepunkte mit Verzögerung erkennt.
- **Absolutes Momentum schützte selten:** Nur 6 Monate in Cash. Die Einbrüche 2018, 2020 und 2022 kamen schneller, als ein 12-Monats-Signal reagiert.
- Passt zu den übrigen Trendtests (Nr. 3, 4, 28, 30): Momentum-Signale haben auf diesem Universum 2015–2023 keinen Vorteil gebracht.

## 3. Trial-Log (Fortsetzung)

| # | Datum | Test | Ergebnis |
|---|---|---|---|
| T102 | 24.10.2026 | D-TOP1, In-Sample | nicht bestanden: Sharpe 0,17, t 0,48 |
| T103 | 24.10.2026 | D-TOP2, In-Sample | nicht bestanden: Sharpe 0,14, t 0,38 |
| T104 | – | Hold-out | entfällt, Hold-out unberührt |
| T105 | – | FTMO-Bootstrap | entfällt |
