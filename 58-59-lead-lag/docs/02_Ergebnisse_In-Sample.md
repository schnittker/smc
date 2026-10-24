# Ergebnisse Strategien Nr. 58 und 59 – Modell LL „Lead-Lag“

Stand: 24.10.2026

Grundlagen:
- Regeln: unverändert aus der Vorregistrierung `docs/01_Vorregistrierung.md` (Commit `ec37d73`)
- Code: `research/ll/`, Lauf `research/scripts/run_ll.py`; 3 Tests grün
- Daten: FRED DGS10 (Download 24.10.2026)
- In-Sample: 2015–2023
- Vollständige Tabellen: `research/results/ll_in_sample.md`

## 1. Ergebnis

**Keine Variante besteht. Die Strategien Nr. 58 und 59 sind damit gescheitert.** Der Hold-out bleibt unberührt, T213–T218 entfallen.

| Kennzahl | LL-AJ (58) | LL-Y1 (59) | LL-Y20 (59) |
|---|---|---|---|
| Netto je Tag (bp des Kapitals) | **−1,45** | **−0,99** | **−0,13** |
| Kosten je Tag | 2,00 | 1,65 | 0,92 |
| t-Wert (kleinster) | −4,33 | −0,85 | −0,09 |
| Jahre positiv | 1 von 9 | 4 von 9 | 4 von 9 |
| Teilzeiträume 2015–2019 / 2020–2023 | −1,36 / −1,55 | +2,06 / −4,81 | −0,85 / +0,78 |
| Trades bzw. Positionswechsel | 3.437 | 2.253 | 264 |

## 2. Einordnung

- **US500 → AUDJPY:** Es gibt keinen verzögerten Effekt. In den 3 Stunden nach einer US500-Stunde über 1,5σ bewegt sich AUDJPY vor Kosten um −0,1 bis −0,8 bp, also nicht in Richtung des Impulses. Der Zusammenhang ist gleichzeitig: AUDJPY reagiert in derselben Stunde.
- **US-Rendite → USDJPY:** Am selben Tag korrelieren beide stark (0,49). Die Vortagesänderung sagt aber praktisch nichts voraus (0,035). Das Muster gleicht Nr. 23: Lead-Lag zwischen liquiden Märkten wird binnen Minuten arbitragiert.
- **Fazit:** Es bleibt nur der gleichzeitige Zusammenhang. Den kann man nicht handeln, ohne die Zukunft zu kennen.

## 3. Trial-Log (Fortsetzung)

| # | Datum | Test | Ergebnis |
|---|---|---|---|
| T210 | 24.10.2026 | LL-AJ, In-Sample | nicht bestanden: −1,45 bp/Tag, t −4,33 |
| T211 | 24.10.2026 | LL-Y1, In-Sample | nicht bestanden: −0,99 bp/Tag, t −0,85 |
| T212 | 24.10.2026 | LL-Y20, In-Sample | nicht bestanden: −0,13 bp/Tag, t −0,09 |
| T213–T218 | – | Hold-out, FTMO | entfallen, Hold-out unberührt |
