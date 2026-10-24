# Ergebnisse Strategie Nr. 40 – Modell W „Hurst-Regime-Switch“

Stand: 24.10.2026

Grundlagen:
- Regeln: unverändert aus der Vorregistrierung `docs/01_Vorregistrierung.md` (Commit `1bf8230`)
- Code: `research/hrs/`, Lauf `research/scripts/run_w.py`; 4 Tests grün
- In-Sample: Einstiege 2015–2023, 17 Instrumente, 0,25 % Risiko je Trade
- Vollständige Tabellen: `research/results/w_in_sample.md`

## 1. Ergebnis

**Der Hurst-Filter macht beide Bausteine schlechter, nicht besser. Strategie Nr. 40 ist damit gescheitert.** Der Hold-out bleibt unberührt, T136 und T137 entfallen.

| Kennzahl | W-HURST | ohne Filter: Trend | ohne Filter: Umkehr |
|---|---|---|---|
| Netto je Tag (bp des Kapitals) | **−2,27** | −1,38 | −7,35 |
| vor Kosten je Tag | −1,51 | +1,30 | −2,80 |
| Ø R je Trade vor Kosten / netto | −0,073 / −0,110 | +0,022 / −0,023 | −0,023 / −0,059 |
| t-Wert (kleinster) | −4,70 | −0,86 | −4,79 |
| Jahre positiv | 1 von 9 | 3 von 9 | 0 von 9 |
| Trades (9 Jahre) | 1.942 (98 Trend, 1.844 Umkehr) | 5.594 | 11.576 |

## 2. Einordnung

- **H aus 500 H4-Kerzen liegt fast immer nahe 0,5.** Der Median ist 0,486, 90 % der Werte liegen zwischen 0,43 und 0,53. Nur 1,3 % der Kerzen gelten als Trendregime, 14,6 % als Umkehrregime.
- **Gerade die „Umkehr“-Phasen (H < 0,45) sind für den Fade schlecht:** −0,07 R je Trade vor Kosten gegenüber −0,02 R ohne Filter. Ein niedriges H aus der Vergangenheit sagt keine Umkehr in der Zukunft voraus. Das deckt sich mit Lo (1991): Kurzfenster-Hurst ist von 0,5 kaum unterscheidbar.
- **Fazit:** Regime-Filter aus Persistenzmaßen helfen hier nicht. Mit Nr. 37–40 sind H4- und H1-Umkehr- und Ausbruchsregeln auf Majors, Crosses, Indizes und Rohstoffen jetzt umfassend gescheitert.

## 3. Trial-Log (Fortsetzung)

| # | Datum | Test | Ergebnis |
|---|---|---|---|
| T135 | 24.10.2026 | W-HURST, In-Sample | nicht bestanden: −2,27 bp/Tag, t −4,70 (vor Kosten −1,5) |
| T136, T137 | – | Hold-out, FTMO | entfallen, Hold-out unberührt |
