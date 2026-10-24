# Ergebnisse Strategie Nr. 11 – Modell I „Intraday-Momentum US500“

Stand: 24.10.2026

Grundlagen:
- Regeln: unverändert aus der Vorregistrierung `docs/01_Vorregistrierung.md` (Commit `a06f4db`)
- Code: `research/imom/`, Lauf `research/scripts/run_i.py` (Commit `b6b0027`); 11 Tests grün
- In-Sample: volle NYSE-Handelstage 2015–2023, US500, HistData M5
- Vollständige Tabellen: `research/results/i_in_sample.md`

## 1. Ergebnis

**Beide Varianten verfehlen alle bzw. drei von vier Kriterien. Strategie Nr. 11 ist damit gescheitert.** Der Hold-out 2024–2026 bleibt unberührt, T41 und T42 entfallen.

| Kriterium | Schwelle | I-ONFH (Signal bis 10:00) | I-ROD (Signal bis 15:30) |
|---|---|---|---|
| Netto je Tag | > 0 | +0,44 bp | +1,00 bp |
| t-Wert (kleinster aus iid, Woche, Monat) | ≥ 3,0 | **0,52** | **1,31** |
| Jahre positiv | ≥ 6 von 9 | **5 von 9** | **4 von 9** |
| Teilzeiträume 2015–2019 / 2020–2023 | beide > 0 | **−0,18** / +1,29 bp | +0,61 / +1,54 bp |
| bei doppelten Kosten | > 0 | **−0,69 bp** | **−0,13 bp** |
| vor Kosten je Tag | – | +1,58 bp | +2,14 bp |
| Kosten je Tag | – | 1,13 bp | 1,13 bp |
| Sharpe Ratio p. a. netto | – | 0,22 | 0,49 |

## 2. Einordnung

1. **Der Effekt existiert, ist aber nur doppelt so groß wie die Kosten.**
   - Die Regression der letzten halben Stunde auf die Rendite bis 15:30 ist signifikant: Steigung +0,038, t 3,45, R² 1,8 %. Das bestätigt Baltussen et al. (2021) auch für 2015–2023. Auf die Rendite bis 10:00 ist der Zusammenhang schwächer (t 1,52).
   - Als Handelsregel ergibt das nur +1,6 bzw. +2,1 bp je Tag vor Kosten. Spread plus Slippage kosten 1,1 bp. Netto bleibt zu wenig für einen t-Wert ≥ 3, und bei doppelten Kosten ist das Ergebnis negativ.
   - Das ist dasselbe Muster wie bei Nr. 2 (Fix-Reversal) und Nr. 5: Die Wissenschaft misst den Effekt richtig, aber er ist für FTMO-Kosten zu klein.
2. **An Tagen mit großem Signal ist er größer** (beschreibend): Im obersten Drittel von |Signal| bringt I-ROD +3,4 bp netto (t 2,03), an den übrigen Tagen −0,2 bp. Das passt zum Gamma-Hedging-Mechanismus. Die Teilmenge wurde aber nicht vorab als Variante festgelegt.
3. **US100 ist etwas stärker** (I-ROD +1,85 bp, t 2,18, 6 von 9 Jahren positiv), erreicht die Schwelle aber ebenfalls nicht.
4. **Datenhinweis:** 2023 enthält nur 139 Handelstage, wegen der bekannten HistData-Lücke März bis Juli 2023. Das Urteil hängt daran nicht.

## 3. Folgerung für die weitere Testreihe

Nach Nr. 2, 5, 9 und 11 zeigt sich ein klares Muster: Die gut belegten Effekte sind in unseren Daten **vor Kosten meist vorhanden**, aber zu klein oder zu selten für FTMO-Kosten und die Schwelle t ≥ 3. Für die FX-Faktoren (Nr. 3, 6, 7) gilt das nicht einmal vor Kosten.

Möglicher Ausweg für später, **nicht als Nachtest auf diesen Daten**: mehrere kleine, voneinander unabhängige Effekte kombinieren (Nr. 100, Ensemble). Kandidaten sind Nr. 9 (Pre-FOMC), Nr. 11 (I-ROD) und Nr. 10. Ein solches Ensemble müsste vorab festgelegt und vor allem im unberührten Hold-out geprüft werden.

## 4. Trial-Log (Fortsetzung)

| # | Datum | Test | Ergebnis |
|---|---|---|---|
| T39 | 24.10.2026 | I-ONFH, In-Sample | nicht bestanden: +0,44 bp/Tag, t 0,52 |
| T40 | 24.10.2026 | I-ROD, In-Sample | nicht bestanden: +1,00 bp/Tag, t 1,31 |
| T41 | – | Hold-out | entfällt, Hold-out unberührt |
| T42 | – | FTMO-Bootstrap | entfällt |

Regressionen, Teilmengen und US100 sind beschreibende Diagnosen, keine neuen Trials.
