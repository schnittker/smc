# Ergebnisse Strategie Nr. 7 – Modell X „FX Querschnitts-Momentum G8“

Stand: 24.10.2026

Grundlagen:
- Regeln: unverändert aus der Vorregistrierung `docs/01_Vorregistrierung.md` (Commit `66f9551`)
- Code: `research/xmom/` mit der Engine aus `../06-fx-carry`, Lauf `research/scripts/run_x.py` (Commit `c98594b`); 7 Tests grün
- In-Sample: Handelstage 2015–2023, 24 FX-Paare, Warm-up 2014
- Vollständige Tabellen: `research/results/x_in_sample.md`
  - Nach dem Lauf wurde dort nur eine falsch kopierte Tabellenüberschrift korrigiert („Rangfolge der Zinsen“ statt „Rangfolge nach Formationsrendite“). Zahlen und Regeln sind unverändert.

## 1. Ergebnis

**Beide Varianten verfehlen alle Kriterien. Strategie Nr. 7 ist damit gescheitert.** Der Hold-out 2024–2026 bleibt unberührt, T29 und T30 entfallen.

| Kriterium | Schwelle | X-1 (letzter Monat) | X-12 (12-1 Monate) |
|---|---|---|---|
| t-Wert (kleinster aus iid, Woche, Monat) | ≥ 3,0 | **−0,87** | **−2,49** |
| Sharpe Ratio p. a. netto | (≈ 1,0) | **−0,28** | **−0,81** |
| Jahre positiv | ≥ 6 von 9 | **2 von 9** | **1 von 9** |
| Instrumente positiv | ≥ 60 % | **6 von 14** | **5 von 14** |
| bei doppelten Kosten | > 0 | **−5,4 % p. a.** | **−10,4 % p. a.** |

**Zerlegung p. a.** (skaliert auf 10 % Portfolio-Volatilität)

| | Kurs | Swaps | Handel | Gebühr | Summe | Max. Drawdown |
|---|---|---|---|---|---|---|
| X-1 | −0,63 % | −1,65 % | −0,30 % | −0,19 % | **−2,77 %** | 44 % |
| X-12 | −6,41 % | −1,31 % | −0,23 % | −0,16 % | **−8,10 %** | 76 % |

## 2. Einordnung

1. **Kein Momentum in den G8-Währungen 2015–2023.**
   - X-1 ist vor Kosten etwa null (Kurs −0,6 % p. a.). Nur 2015 lief gut (+12 %), danach war die Variante in 7 von 8 Jahren negativ.
   - Das passt zur Literatur: Der Effekt sitzt in kleinen Währungen mit hohen Spreads, nicht in den Hauptwährungen. Bei FTMO gibt es diese Währungen nicht.
2. **X-12 ist signifikant negativ** (t −2,49). Die Verlierer der letzten 12 Monate liefen im Folgemonat besser als die Gewinner, also eine **Umkehr**, kein Momentum.
   - Das passt zum Scheitern der Trendfolge auf denselben Paaren (Nr. 3: Sharpe −0,53).
   - **Vorsicht:** Die Gegenposition („Verlierer kaufen“) wäre eine aus diesen Daten abgeleitete Hypothese. Nach Kosten und mit Swap-Aufschlag läge sie grob bei einer Sharpe Ratio um +0,5 und damit ohnehin unter dem Kriterium. Sie wird nicht als eigener Trial nachgeschoben.
   - **Bezug zu Nr. 8 (FX Value):** Value kauft langfristig unterbewertete Währungen, das sind oft die Verlierer der Vergangenheit. Die Hypothese ist extern begründet (Kaufkraftparität). Ein Test von Nr. 8 ist aber nicht mehr unabhängig von dieser Beobachtung und muss das in der Vorregistrierung festhalten.
3. **Swaps kosten statt zu bringen.** Momentum hält oft Niedrigzinswährungen long. Mit dem Aufschlag von 1 % je Position zahlen beide Varianten 1,3–1,7 % p. a. Ohne Aufschlag bleiben X-1 bei −0,09 und X-12 bei −0,62.
4. **Kaum Diversifikation zu Carry:** Die Korrelation der Tagesergebnisse mit K-3 (Nr. 6) liegt bei −0,08 (X-1) bzw. +0,15 (X-12). Eine Kombination aus zwei Strategien ohne Ertrag ergibt aber keinen Ertrag.

## 3. Gesamtbild nach Strategie 1–7

| Nr. | Strategie | Ergebnis |
|---|---|---|
| 1 | SMC | kein Baustein nach Kosten profitabel |
| 2 | Fix-Reversal | Effekt nur so groß wie die Kosten (Sharpe 0,31) |
| 3 | Trendfolge FX/Gold | Sharpe −0,53 |
| 4 | Trendfolge Indizes/Rohstoffe | Sharpe −0,37 |
| 5 | Monatsend-Rebalancing | Effekt seit 2015 auf ein Zehntel geschrumpft |
| 6 | FX Carry G8 | Sharpe −0,16 / −0,02 |
| 7 | FX Querschnitts-Momentum G8 | Sharpe −0,28 / −0,81 |

**Die drei großen FX-Faktoren Trend, Carry und Momentum tragen auf den FTMO-Währungen 2015–2023 nicht.** Auch die Kalender- und Flow-Effekte am Fix (Nr. 2, 5) sind zu klein für die Kosten. Die nächsten Kandidaten mit anderer Ertragsquelle sind die Index-Effekte (Nr. 9 Pre-FOMC, Nr. 10 Turn-of-the-Month, Nr. 11 Intraday-Momentum).

## 4. Trial-Log (Fortsetzung)

| # | Datum | Test | Ergebnis |
|---|---|---|---|
| T27 | 24.10.2026 | X-1, In-Sample | nicht bestanden: Sharpe −0,28, t −0,87, 2 von 9 Jahren positiv |
| T28 | 24.10.2026 | X-12, In-Sample | nicht bestanden: Sharpe −0,81, t −2,49, 1 von 9 Jahren positiv |
| T29 | – | Hold-out | entfällt, Hold-out unberührt |
| T30 | – | FTMO-Bootstrap | entfällt |

Die Rechnung ohne Swap-Aufschlag, die Teilzeiträume und die Korrelation mit Carry sind beschreibende Diagnosen, keine neuen Trials.
