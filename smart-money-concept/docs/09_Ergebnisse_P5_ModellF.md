# Ergebnisse P5 – Modell F „Fix-Reversal“

Stand: 24.10.2026

Grundlagen:
- Regeln: unverändert aus der Vorregistrierung `docs/08_P5_Vorregistrierung_ModellF.md`
- Code: `research/smc/strategy_f.py`, Lauf `research/scripts/run_p5.py`; 59 Tests grün
- In-Sample: FX-Tage 01.01.2015–31.12.2023, HistData M5
- Vollständige Tabellen: `research/results/p5_modell_f_in_sample.md`

## 1. Ergebnis

**Keine Variante besteht. P5 ist damit gescheitert.** Der Hold-out 2024–2026 bleibt unberührt, T11 und T12 entfallen.

| Kriterium | Schwelle | F-ALL (EUR, GBP, JPY; W1–W4) | F-EU (EUR, GBP; W3, W4) |
|---|---|---|---|
| Netto je Tag | > 0 | **−4,32 bp** | +1,36 bp |
| t-Wert (kleinster aus iid, Woche, Monat) | ≥ 3,0 | **−2,26** | **0,92** |
| Sharpe Ratio p. a. | (≈ 1,0) | −0,75 | 0,31 |
| Jahre positiv | ≥ 6 von 9 | **3 von 9** | 6 von 9 |
| Paare positiv | ≥ 60 % | **0 von 3** | 2 von 2 |
| bei doppelten Kosten | > 0 | **−15,1 bp** | **−2,3 bp** |

## 2. Je Fenster: Effekt gegen Kosten

Ø je Position in Basispunkten, In-Sample. Kosten je Position: etwa 1,0 bp bei EURUSD, 0,9 bp bei GBPUSD, 1,4 bp bei USDJPY (mit 0,7-%-Gebühr).

| Fenster | Richtung | EURUSD vor Kosten / netto | GBPUSD | USDJPY |
|---|---|---|---|---|
| W1 pre-Tokio | Long USD | −0,64 / −1,62 | −0,63 / −1,54 | −0,20 / −1,55 |
| W2 post-Tokio | Short USD | +0,46 / −0,52 | +0,16 / −0,75 | +0,81 / −0,59 |
| W3 pre-EZB | Long USD | **+1,47 / +0,49** | **+1,41 / +0,50** | +1,19 / −0,23 |
| W4 post-London | Short USD | +1,19 / +0,21 | +1,09 / +0,18 | – |

**Einordnung**
1. **Der Effekt existiert noch, ist aber so groß wie die Kosten.**
   - In den europäischen Fenstern bewegt sich der USD vor Kosten in die erwartete Richtung, um 1,1–1,5 bp je Fenster.
   - Das passt zum Paper: Für 2014–2019 nennt es im Dollar-Portfolio rund 1 bp pro Tag und Fenster (Tabelle II).
   - Unsere Pipeline reproduziert also den publizierten Effekt. Er reicht aber nicht über die FTMO-Kosten von rund 1 bp je Position.
2. **Das Tokio-Muster ist weg.**
   - Vor dem Tokio-Fix steigt der USD in 2015–2023 nicht mehr (W1 vor Kosten negativ).
   - Danach fällt er nur noch minimal (W2 +0,2 bis +0,8 bp).
   - Hinweis: W1 beginnt hier um 17:30 statt 17:00, um den Rollover-Spread zu meiden. Die erste halbe Stunde nach dem New-York-Schluss fehlt damit.
3. **Die beschreibenden Paare bestätigen das.** AUDUSD, NZDUSD, USDCAD und USDCHF liegen in allen Fenstern netto bei null oder darunter, auch weil ihre Kosten höher sind.
4. **Der Notfall-Stop verzerrt nichts.**
   - Er löste in W3 öfter aus als beabsichtigt (16–22 %), weil die ATR aus der ruhigen Asien-Stunde stammt.
   - Gegenprobe ohne Stop: F-EU +1,37 statt +1,36 bp pro Tag, gleiche Sharpe Ratio. Das Ergebnis hängt nicht am Stop.

## 3. Gesamtbild nach P2–P5

| Phase | Hypothese | Ergebnis |
|---|---|---|
| P2 | 13 SMC-Bausteine einzeln | kein Baustein nach Kosten profitabel |
| P3 | Modell C: Trend-Fortsetzung, 3 Tage | +0,015 R bzw. −0,016 R |
| P4 | Modell D: Trendfolge mit Struktur-Exit | −0,040 R |
| P5 | Modell F: Fix-Reversal (beste akademische Evidenz) | Effekt vorhanden, aber nur so groß wie die Kosten; Sharpe 0,3 |

- Alle vier Hypothesen sind an derselben Hürde gescheitert: Was es an Vorhersagbarkeit gibt, ist nach FTMO-Kosten zu klein. Das gilt für die SMC-Muster ebenso wie für den bestbelegten Intraday-Effekt der Literatur.
- Der Hold-out 2024–2026 ist weiterhin unberührt.
- **Positiv:** Die Pipeline ist validiert. Sie reproduziert den publizierten Fix-Effekt in der Größenordnung des Papers. Die negativen Ergebnisse sind also kein Artefakt der eigenen Daten oder des Codes.

## 4. Optionen

| Option | Inhalt | Einschätzung |
|---|---|---|
| **D – Pausieren** (Empfehlung) | Ergebnisse festhalten, keine Challenge kaufen | Vier vorregistrierte Tests ohne tragfähigen Vorteil; jeder weitere Versuch auf denselben Daten wird unwahrscheinlicher |
| C2 – Trendfolge auf D1 | Zeitreihen-Momentum über alle 25 Instrumente mit Volatilitäts-Sizing | Kosten unkritisch. Für FTMO in 6 Monaten bräuchte es aber eine Sharpe Ratio um 1 oder mehr. Diversifizierte Trendfolge auf G10-FX und Gold dürfte seit 2010 eher bei 0,3–0,5 liegen (eigene Einschätzung, nicht getestet). Erfolgsaussicht gering |
| Challenge ohne Vorteil | – | Bestehenschance etwa 35–42 % (Monte-Carlo), also ein Glücksspiel mit der Gebühr als Einsatz. Nicht empfohlen |

## 5. Trial-Log (Fortsetzung)

| # | Datum | Test | Ergebnis |
|---|---|---|---|
| T9 | 24.10.2026 | F-ALL, In-Sample | nicht bestanden: −4,32 bp/Tag, t −2,26 |
| T10 | 24.10.2026 | F-EU, In-Sample | nicht bestanden: +1,36 bp/Tag, t 0,92, Sharpe 0,31 |
| T11 | – | Hold-out | entfällt, Hold-out unberührt |
| T12 | – | FTMO-Bootstrap | entfällt |

Die Gegenprobe ohne Notfall-Stop ist eine beschreibende Diagnose, kein neuer Trial.
