# Ergebnisse Strategie Nr. 8 – Modell V „FX Value“

Stand: 24.10.2026

Grundlagen:
- Regeln: unverändert aus der Vorregistrierung `docs/01_Vorregistrierung.md` (Commit `87be6f4`)
- Code: `research/fval/`, Lauf `research/scripts/run_v8.py`; 3 Tests grün
- Daten: FRED CPI und Wechselkurse (Download 24.10.2026)
- In-Sample: 2015–2023, 24 FX-Paare
- Vollständige Tabellen: `research/results/v_in_sample.md`

## 1. Ergebnis

**Beide Varianten liegen nach Kosten bei null. Strategie Nr. 8 ist damit gescheitert.** Der Hold-out bleibt unberührt, T301 und T302 entfallen.

| Kennzahl | V-5Y | V-PPP |
|---|---|---|
| Sharpe Ratio p. a. (netto) | **−0,06** | **−0,07** |
| t-Wert (kleinster) | −0,18 | −0,29 |
| Rendite p. a. bei 10 % Vol. | −0,6 % | −0,7 % |
| Kurs / Swaps / Handel + Gebühr p. a. | +1,8 / −2,0 / −0,4 % | +2,2 / −2,6 / −0,3 % |
| Jahre positiv | 3 von 9 | 5 von 9 |
| ohne Swap-Aufschlag | Sharpe +0,15 | – |

## 2. Einordnung

- **Value hat vor Kosten einen kleinen positiven Kursbeitrag:** +1,8 bis +2,2 % p. a. bei 10 % Volatilität, also Sharpe ≈ 0,2. Die Swaps fressen ihn vollständig auf.
- **Der Grund ist der Swap:** Das Portfolio war meist Short USD (86 von 104 Monaten) und Long AUD/JPY. 2015–2023 lag der USD-Zins oft über dem der Long-Währungen; dazu kommt der Swap-Aufschlag. Die Korrelation mit Carry K-3 ist uneinheitlich (V-5Y +0,15, V-PPP −0,19).
- **Fazit für die G8-Faktoren:** Carry (Nr. 6), Momentum (Nr. 7), Zins-Momentum (Nr. 20) und Value (Nr. 8) sind bei FTMO-Kosten und -Swaps alle gescheitert. Keiner hat 2015–2023 einen Netto-Edge.

## 3. Trial-Log (Fortsetzung)

| # | Datum | Test | Ergebnis |
|---|---|---|---|
| T299 | 24.10.2026 | V-5Y, In-Sample | nicht bestanden: Sharpe −0,06, t −0,18 |
| T300 | 24.10.2026 | V-PPP, In-Sample | nicht bestanden: Sharpe −0,07, t −0,29 |
| T301, T302 | – | Hold-out, FTMO | entfallen, Hold-out unberührt |
