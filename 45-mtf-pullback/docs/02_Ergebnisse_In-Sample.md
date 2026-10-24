# Ergebnisse Strategie Nr. 45 – Modell J „Multi-Timeframe-Pullback“

Stand: 24.10.2026

Grundlagen:
- Regeln: unverändert aus der Vorregistrierung `docs/01_Vorregistrierung.md` (Commit `473e542`)
- Code: `research/mtf/`, Lauf `research/scripts/run_j.py`; 3 Tests grün
- In-Sample: Einstiege 2015–2023, 17 Instrumente, 0,25 % Risiko je Trade
- Vollständige Tabellen: `research/results/j_in_sample.md`

## 1. Ergebnis

**Schon vor Kosten negativ und nach Kosten stark negativ. Strategie Nr. 45 ist damit gescheitert.** Der Hold-out bleibt unberührt, T154 und T155 entfallen.

| Kennzahl | J-MTF |
|---|---|
| Netto je Tag (bp des Kapitals, Portfolio) | **−14,70** (σ 116 bp) |
| vor Kosten je Tag | −5,04 |
| Handelskosten und Swap-Belastung je Tag | 9,96 |
| Rendite p. a. netto | −38,2 % |
| t-Wert (kleinster) | −6,53 |
| Jahre positiv / Instrumente positiv | 0 von 9 / 2 von 17 |
| Trades (9 Jahre) | 16.194 |
| Ø R je Trade vor Kosten / netto | −0,029 / −0,085 |
| Ausstiege Ziel / Stop / Zeit | 22 % / 58 % / 20 % |

## 2. Einordnung

- **Der Pullback-Einstieg hat keinen Edge.** Nach dem Wiedereintritt über die H1-EMA20 läuft der Kurs nicht öfter als zufällig weiter. Das 2R-Ziel wird in 22 % der Fälle erreicht, bei Zufall wären etwa 33 % zu erwarten. Der Wert liegt sogar darunter, weil die Stops eng liegen und das H1-Rauschen sie oft auslöst.
- **Kosten:** Der enge Stop (≈ 1–2 ATR H1) erhöht die Kosten auf 0,06 R je Trade.
- **Fazit:** Trendfolge ist in keiner Form tragfähig, weder als Ausbruch (Nr. 28, 30, 33–38) noch als Rücksetzer-Einstieg (Nr. 45) und auf keinem Zeitrahmen (D1, H4, H1).

## 3. Trial-Log (Fortsetzung)

| # | Datum | Test | Ergebnis |
|---|---|---|---|
| T153 | 24.10.2026 | J-MTF, In-Sample | nicht bestanden: −14,7 bp/Tag, t −6,53 (vor Kosten −5,0) |
| T154, T155 | – | Hold-out, FTMO | entfallen, Hold-out unberührt |
