# Ergebnisse Strategien Nr. 33, 34, 35 – Modell T „Tages-Ausbruch“

Stand: 24.10.2026

Grundlagen:
- Regeln: unverändert aus der Vorregistrierung `docs/01_Vorregistrierung.md` (Commit `fb482e2`)
- Code: `research/dbo/`, Lauf `research/scripts/run_t.py` (Commit `40bb5b1`, Korrektur `6cb19d5`); 9 Tests grün
- In-Sample: Servertage 2015–2023, 17 Instrumente, 0,25 % Risiko je Trade
- Vollständige Tabellen: `research/results/t_in_sample.md`

## 1. Ergebnis

**Alle drei Regeln sind nach Kosten bei null oder negativ. Die Strategien Nr. 33, 34 und 35 sind damit gescheitert.** Der Hold-out bleibt unberührt, T117–T122 entfallen.

| Kennzahl | T-NR7 (33) | T-INSIDE (34) | T-LW (35) |
|---|---|---|---|
| Netto je Tag (bp des Kapitals, Portfolio) | **−0,54** | **+0,13** | **−4,23** |
| vor Kosten je Tag | +1,83 | +1,90 | +4,52 |
| Kosten je Tag | 2,38 | 1,77 | 8,75 |
| Rendite p. a. netto | −1,4 % | +0,3 % | −10,8 % |
| t-Wert (kleinster) | −0,50 | 0,15 | −2,07 |
| Jahre positiv | 4 von 9 | 3 von 9 | 2 von 9 |
| Instrumente positiv | 8 von 17 | 8 von 17 | 4 von 17 |
| Trades (9 Jahre) | 5.717 | 4.778 | 29.338 |
| Ø R je Trade vor Kosten / netto | +0,029 / −0,009 | +0,036 / +0,003 | +0,014 / −0,013 |
| Trefferquote / Stops | 46 % / 27 % | 47 % / 22 % | 47 % / 13 % |

## 2. Einordnung

- **Vor Kosten ist ein Hauch von Ausbruchs-Momentum da**, nämlich +0,01 bis +0,04 R je Trade. Das ist zu wenig für die Kosten von 0,03–0,04 R je Trade, und es ist instabil: Die Jahresergebnisse schwanken ohne Muster.
- **Kein Instrument und keine Anlageklasse sticht stabil heraus.** Selbst die Zielmärkte der Originalregeln sind uneinheitlich: Beim Volatility Breakout auf Indizes und Gold (Nr. 35) sind HK50 +2,0, US100 +1,1 und JP225 +0,8 % p. a., aber UK100 −2,1, FRA40 −1,7 und AUS200 −2,3 % p. a.
- **Abweichung von der Listenbeschreibung:** Nr. 34 („in Trendrichtung“) und Nr. 35 („Indizes, Gold“) wurden wie vorregistriert in beide Richtungen und auf allen 17 Instrumenten getestet. Die Ergebnisse je Instrument (`research/results/t_in_sample.md`) zeigen keine Teilmenge, der eine eigene Vorregistrierung rechtfertigen würde.
- **Zusammen mit Nr. 16 (ORB) und Nr. 31 (London Breakout)** sind jetzt fünf Ausbruchsregeln auf Intraday- und Tagesbasis gescheitert. Einfache Preis-Ausbrüche haben bei FTMO-Kosten 2015–2023 keinen Vorteil.

**Korrektur nach dem ersten Lauf:** Eine einstündige HistData-Restkerze am Server-Samstag wurde fälschlich als D1-Kerze gezählt. Sie wird jetzt ausgeschlossen (siehe `research/results/t_in_sample.md`). Das Ergebnis bleibt dasselbe: Auch der fehlerhafte Lauf war negativ.

## 3. Trial-Log (Fortsetzung)

| # | Datum | Test | Ergebnis |
|---|---|---|---|
| T114 | 24.10.2026 | T-NR7, In-Sample | nicht bestanden: −0,54 bp/Tag, t −0,50 |
| T115 | 24.10.2026 | T-INSIDE, In-Sample | nicht bestanden: +0,13 bp/Tag, t 0,15 |
| T116 | 24.10.2026 | T-LW, In-Sample | nicht bestanden: −4,23 bp/Tag, t −2,07 |
| T117–T122 | – | Hold-out, FTMO | entfallen, Hold-out unberührt |
