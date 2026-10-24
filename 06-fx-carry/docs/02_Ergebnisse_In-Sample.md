# Ergebnisse Strategie Nr. 6 – Modell K „FX Carry G8“

Stand: 24.10.2026

Grundlagen:
- Regeln: unverändert aus der Vorregistrierung `docs/01_Vorregistrierung.md` (Commit `8a61595`)
- Code: `research/carry/`, Lauf `research/scripts/run_k.py` (Commit `72b665c`); 19 Tests grün
  - Die Positions-Engine reproduziert die Buchhaltung von Modell G aus dem SMC-Projekt exakt (Test `test_run_weights_reproduces_model_g`).
- In-Sample: Handelstage 2015–2023, 24 FX-Paare, Warm-up 2014
- Vollständige Tabellen: `research/results/k_in_sample.md`

## 1. Ergebnis

**Beide Varianten verfehlen das Hauptkriterium deutlich. Strategie Nr. 6 ist damit gescheitert.** Der Hold-out 2024–2026 bleibt unberührt, T25 und T26 entfallen.

| Kriterium | Schwelle | K-3 (3 Carry-Positionen) | K-1 (höchste gegen niedrigste) |
|---|---|---|---|
| t-Wert (kleinster aus iid, Woche, Monat) | ≥ 3,0 | **−0,51** | **−0,06** |
| Sharpe Ratio p. a. netto | (≈ 1,0) | **−0,16** | **−0,02** |
| Jahre positiv | ≥ 6 von 9 | **3 von 9** | **4 von 9** |
| Instrumente positiv | ≥ 60 % | **4 von 10** | 2 von 3 |
| bei doppelten Kosten | > 0 | **−2,0 % p. a.** | **−0,5 % p. a.** |

**Zerlegung p. a.** (skaliert auf 10 % Portfolio-Volatilität)

| | Kurs | Swaps (netto, nach Aufschlag) | Handel | Gebühr | Summe | Max. Drawdown |
|---|---|---|---|---|---|---|
| K-3 | −2,57 % | +1,05 % | −0,04 % | −0,05 % | **−1,62 %** | 31 % |
| K-1 | −1,43 % | +1,30 % | −0,02 % | −0,02 % | **−0,17 %** | 24 % |

## 2. Einordnung

1. **Der Zinsvorteil kommt an, wird aber vom Wechselkurs aufgezehrt.**
   - Die Swaps bringen netto +1,0 bis +1,3 % p. a., vor dem Aufschlag etwa +2,9 bis +3,0 %.
   - Die Hochzinswährungen NZD, AUD und CAD werteten 2015–2023 im Mittel stärker ab, als ihr Zinsvorteil betrug. Das ist das Gegenteil des Forward-Premium-Puzzles, das Carry trägt.
   - Am schlechtesten lief 2015 mit −13,6 % (K-3): Rohstoffcrash, AUD, NZD und CAD fielen stark.
2. **Auch ohne Swap-Aufschlag kein Vorteil.** K-3 hätte dann eine Sharpe Ratio von +0,02, K-1 von +0,15. Der Aufschlag von 1 % je Position kostet etwa 1,7–1,8 Prozentpunkte p. a., entscheidend ist er aber nicht.
3. **Die Zinsen ließen kaum Auswahl.**
   - JPY, CHF und EUR standen in allen 104 Monaten auf der Short-Seite, NZD in allen 104 auf der Long-Seite (K-3).
   - Das Portfolio war also im Kern eine feste Wette „NZD/CAD/AUD/USD gegen JPY/CHF/EUR“, ohne Diversifikation über wechselnde Zinsregime.
   - K-1 hielt meist NZD gegen CHF. Positiv war nur USDCHF (+13 %, davon 6 % Swaps), NZDUSD verlor 8 %.
4. **2022, das große Zinsjahr, rettet nichts.** K-3 −1,8 %, K-1 −5,3 %. Der stärkste Carry-Trade 2022 (Long USD gegen JPY) war wegen NZD auf Rang 1 nur teilweise im Portfolio, und der NZD fiel 2022 deutlich.
5. **Passt zur Erwartung** (Sharpe Ratio unter 0,5) und zur Literatur, nach der dollar-neutraler G10-Carry nach 2008 kaum Ertrag brachte.

**Datenhinweis:** Von März bis Juni 2023 fehlt bei HistData häufig die M5-Kerze um 16:50 New York. Es gab keinen Tag, an dem alle 7 USD-Paare sie hatten. Nach der vorregistrierten Regel wurde in diesen 4 Monaten nicht umgeschichtet (104 statt 108 Umschichtungen); die Positionen vom Februar liefen weiter. Die Zinsrangfolge war in diesen Monaten unverändert (NZD, USD, CAD gegen EUR, CHF, JPY). Es fehlte also nur die Neuanpassung an die Volatilität, und das Urteil ändert sich nicht.

## 3. Gesamtbild nach Strategie 1–6

| Nr. | Strategie | Ergebnis |
|---|---|---|
| 1 | SMC | kein Baustein nach Kosten profitabel |
| 2 | Fix-Reversal | Effekt nur so groß wie die Kosten (Sharpe 0,31) |
| 3 | Trendfolge FX/Gold | Sharpe −0,53 |
| 4 | Trendfolge Indizes/Rohstoffe | Sharpe −0,37 |
| 5 | Monatsend-Rebalancing | Effekt seit 2015 auf ein Zehntel geschrumpft |
| 6 | FX Carry G8 | Sharpe −0,16 bzw. −0,02; Zinsvorteil vom Kurs aufgezehrt |

Damit sind die beiden bekanntesten FX-Faktoren, Trend (Nr. 3) und Carry (Nr. 6), auf dem FTMO-Instrumentarium 2015–2023 gescheitert. Der nächste Faktor aus der Literatur, Querschnitts-Momentum (Nr. 7), ist mit Trend verwandt. Sein Prior ist nach Nr. 3 gering.

## 4. Trial-Log (Fortsetzung)

| # | Datum | Test | Ergebnis |
|---|---|---|---|
| T23 | 24.10.2026 | K-3, In-Sample | nicht bestanden: Sharpe −0,16, t −0,51, 3 von 9 Jahren positiv |
| T24 | 24.10.2026 | K-1, In-Sample | nicht bestanden: Sharpe −0,02, t −0,06, 4 von 9 Jahren positiv |
| T25 | – | Hold-out | entfällt, Hold-out unberührt |
| T26 | – | FTMO-Bootstrap | entfällt |

Die Rechnung ohne Swap-Aufschlag, die Teilzeiträume und die Prüfung der Datenlücke 2023 sind beschreibende Diagnosen, keine neuen Trials.
