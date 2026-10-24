# Ergebnisse Strategien Nr. 46 und 47 – Modell Y „Währungsstärke“

Stand: 24.10.2026

Grundlagen:
- Regeln: unverändert aus der Vorregistrierung `docs/01_Vorregistrierung.md` (Commit `431f90a`)
- Code: `research/cst/`, Lauf `research/scripts/run_y.py`; 4 Tests grün
- In-Sample: Einstiege 2015–2023, 24 FX-Paare, 0,25 % Risiko je Trade
- Vollständige Tabellen: `research/results/y_in_sample.md`

## 1. Ergebnis

**Alle drei Varianten liegen nach Kosten bei null oder darunter. Die Strategien Nr. 46 und 47 sind damit gescheitert.** Der Hold-out bleibt unberührt, T159–T164 entfallen.

| Kennzahl | Y-ASIA (46) | Y-LDN (46) | Y-USDB (47) |
|---|---|---|---|
| Netto je Tag (bp des Kapitals) | **−0,56** | **+0,07** | **−1,05** |
| vor Kosten je Tag | +0,53 | +0,96 | +0,87 |
| Kosten und Swap-Belastung je Tag | 1,09 | 0,89 | 1,98 |
| t-Wert (kleinster) | −1,20 | 0,18 | −1,17 |
| Jahre positiv | 4 von 9 | 3 von 9 | 3 von 9 |
| Währungen positiv | 1 von 8 | 5 von 8 | 3 von 8 |
| Trades (9 Jahre) | 1.932 | 1.847 | 4.064 |
| Ø R je Trade vor Kosten / netto | +0,026 / −0,027 | +0,049 / +0,003 | +0,020 / −0,024 |

## 2. Einordnung

- **Sitzungs-Momentum (Nr. 46):** Vor Kosten setzt sich die Stärke der Londoner Morgensitzung leicht fort (+0,05 R je Trade). Das wird aber vollständig von den Kosten aufgezehrt. Die Ranking-Paare sind meist teure Crosses (GBPJPY, GBPAUD, GBPNZD).
- **Asien-Stärke** ist praktisch eine Wette auf AUD, NZD und JPY. Sie wirkt nicht.
- **USD-Basket-Fade (Nr. 47):** +0,02 R vor Kosten bei 48 % Stops. Währungsspezifische Ausschläge kehren nicht verlässlich zurück.
- Das Muster passt zu allen bisherigen Kurzfrist-Tests: Effekte von wenigen Hundertstel R vor Kosten, die nach den FTMO-Kosten nicht reichen.

## 3. Trial-Log (Fortsetzung)

| # | Datum | Test | Ergebnis |
|---|---|---|---|
| T156 | 24.10.2026 | Y-ASIA, In-Sample | nicht bestanden: −0,56 bp/Tag, t −1,20 |
| T157 | 24.10.2026 | Y-LDN, In-Sample | nicht bestanden: +0,07 bp/Tag, t 0,18 |
| T158 | 24.10.2026 | Y-USDB, In-Sample | nicht bestanden: −1,05 bp/Tag, t −1,17 |
| T159–T164 | – | Hold-out, FTMO | entfallen, Hold-out unberührt |
