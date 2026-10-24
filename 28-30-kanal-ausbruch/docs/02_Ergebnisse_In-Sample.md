# Ergebnisse Strategien Nr. 28 und Nr. 30 – Modell B „Kanal-Ausbruch“

Stand: 24.10.2026

Grundlagen:
- Regeln: unverändert aus der Vorregistrierung `docs/01_Vorregistrierung.md` (Commit `9ed2118`)
- Code: `research/brk/`, Lauf `research/scripts/run_b.py` (Commit `8d83972`); 3 Tests grün
- In-Sample: Handelstage 2015–2023, 34 Instrumente
- Vollständige Tabellen: `research/results/b_in_sample.md`

## 1. Ergebnis

**Beide Varianten verfehlen alle Kriterien deutlich. Strategien Nr. 28 und Nr. 30 sind damit gescheitert.** Der Hold-out bleibt unberührt.

| Kriterium | Schwelle | B-52W (Nr. 28) | B-TURTLE (Nr. 30) |
|---|---|---|---|
| Sharpe Ratio p. a. netto | (≈ 1,0) | **−0,54** | **−0,54** |
| t-Wert (kleinster aus iid, Woche, Monat) | ≥ 3,0 | **−1,75** | **−2,01** |
| Jahre positiv | ≥ 6 von 9 | **1 von 9** | **1 von 9** |
| Instrumente positiv | ≥ 60 % | **8 von 34** | **8 von 34** |
| Kurs p. a. vor Kosten (bei 10 % Vol.) | – | −3,0 % | −2,8 % |
| Swaps p. a. (bei 10 % Vol.) | – | −2,3 % | −2,2 % |

| Beitrag nach Anlageklasse (Summe 2015–2023, 10 % Vol.) | B-52W | B-TURTLE |
|---|---|---|
| FX | −35,4 % | −38,7 % |
| Metalle | −3,0 % | −3,8 % |
| Indizes | −10,7 % | −7,4 % |
| Öl | +0,9 % | +1,2 % |

## 2. Einordnung

- **Dasselbe Ergebnis wie Nr. 3 (Sharpe −0,53) und Nr. 4 (−0,37):** Auf diesem Universum gab es 2015–2023 keinen nutzbaren Trend, unabhängig davon, ob er als Zeitreihen-Momentum oder als Kanal-Ausbruch formuliert wird.
- **FX trägt den größten Teil der Verluste.** Die G10-Währungen liefen 2015–2023 überwiegend seitwärts mit Fehlausbrüchen; Nr. 7 zeigte sogar eine Umkehr über 12 Monate.
- Swaps kosten zusätzlich, weil Trendpositionen oft gegen die Zinsdifferenz laufen.
- **Folgerung für die Liste:** Nr. 29 (Dual Momentum) und weitere Trendvarianten (z. B. Nr. 53, 61–63, 70–72) haben nach drei unabhängigen Trendtests auf denselben Daten einen sehr geringen Prior.

## 3. Trial-Log (Fortsetzung)

| # | Datum | Test | Ergebnis |
|---|---|---|---|
| T96 | 24.10.2026 | B-52W (Nr. 28), In-Sample | nicht bestanden: Sharpe −0,54, t −1,75 |
| T97 | 24.10.2026 | B-TURTLE (Nr. 30), In-Sample | nicht bestanden: Sharpe −0,54, t −2,01 |
| T98–T101 | – | Hold-out, FTMO | entfallen, Hold-out unberührt |
