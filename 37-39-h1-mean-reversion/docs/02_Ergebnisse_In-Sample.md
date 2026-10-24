# Ergebnisse Strategien Nr. 37 und 39 – Modell U „H1-Mean-Reversion“

Stand: 24.10.2026

Grundlagen:
- Regeln: unverändert aus der Vorregistrierung `docs/01_Vorregistrierung.md` (Commit `202a0f6`)
- Code: `research/hmr/`, Lauf `research/scripts/run_u.py`; 6 Tests grün
- In-Sample: Einstiege 2015–2023, 17 FX-Crosses, 0,25 % Risiko je Trade
- Vollständige Tabellen: `research/results/u_in_sample.md`

## 1. Ergebnis

**Beide Regeln sind nach Kosten deutlich negativ. Die Strategien Nr. 37 und 39 sind damit gescheitert.** Der Hold-out bleibt unberührt, T131–T134 entfallen.

| Kennzahl | U-BB (37) | U-OU (39) |
|---|---|---|
| Netto je Tag (bp des Kapitals, Portfolio) | **−11,12** | **−1,81** |
| vor Kosten je Tag | +2,24 | −0,49 |
| Handelskosten und Swap-Belastung je Tag | 13,53 | 1,35 |
| Rendite p. a. netto | −28,9 % | −4,7 % |
| t-Wert (kleinster) | −6,19 | −2,84 |
| Jahre positiv | 1 von 9 | 1 von 9 |
| Paare positiv | 1 von 17 | 4 von 17 |
| Trades (9 Jahre) | 20.069 | 1.799 |
| Ø R je Trade vor Kosten / netto | +0,010 / −0,052 | −0,026 / −0,094 |
| Trefferquote / Stops / Zeitstopps | 54 % / 42 % / 0 % | 37 % / 60 % / 8 % |
| Ø Haltedauer | 7,6 h | 19,1 h |

## 2. Einordnung

- **U-BB:** Vor Kosten bleibt fast nichts übrig, nämlich +0,01 R je Trade. Die Kosten liegen bei 0,06 R je Trade, weil die Bänder in ruhigen Phasen eng sind. Damit ist es dasselbe Muster wie bei Nr. 32 (Asien-Range-Fade), nur mit noch kleinerem Vorteil vor Kosten.
- **U-OU:** Schon vor Kosten negativ. Die Halbwertszeit aus 500 Kerzen sagt kaum etwas über die Zukunft. 60 % der Trades enden im Stop: Ausschläge über 2σ100 laufen häufiger weiter als zurück.
- **Kein Paar ist stabil positiv.** Die Crosses, die als „Range-Paare“ gelten (EURCHF, AUDNZD, AUDCAD), sind bei U-BB alle negativ.
- **Fazit:** Mean Reversion ist auf M5 (Nr. 32), H1 (Nr. 37, 39) und D1 (Nr. 15, 21) gescheitert. Bei FTMO-Kosten ist kurzfristige Umkehr auf FX nicht handelbar.

## 3. Trial-Log (Fortsetzung)

| # | Datum | Test | Ergebnis |
|---|---|---|---|
| T129 | 24.10.2026 | U-BB, In-Sample | nicht bestanden: −11,1 bp/Tag, t −6,19 (vor Kosten +2,2) |
| T130 | 24.10.2026 | U-OU, In-Sample | nicht bestanden: −1,8 bp/Tag, t −2,84 (vor Kosten −0,5) |
| T131–T134 | – | Hold-out, FTMO | entfallen, Hold-out unberührt |
