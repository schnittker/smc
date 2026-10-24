# Ergebnisse P7 – Modell H „Trendfolge Indizes und Rohstoffe“

Stand: 24.10.2026

Grundlagen:
- Regeln: unverändert aus der Vorregistrierung `docs/12_P7_Vorregistrierung_ModellH.md` einschließlich des Nachtrags §7, der vor dem ersten Lauf geschrieben wurde
- Code: `research/smc/strategy_h.py` mit der Trend-Engine `strategy_g.run_trend` (reproduziert P6 bitgenau), Lauf `research/scripts/run_p7.py`; 68 Tests grün
- In-Sample: Handelstage 01.01.2015–31.12.2023
- Vollständige Tabellen: `research/results/p7_modell_h_in_sample.md`; Datenqualität: `research/results/data_quality_cfd.md`

## 1. Daten: drei Instrumente vor dem Lauf ausgeschlossen

| Instrument | Problem in den HistData-Dateien |
|---|---|
| Euro Stoxx 50 (ETXEUR) | Daten nur bis Anfang 2019 |
| DAX (GRXEUR) | Juni 2020 bis November 2023 enthält Kurse auf Euro-Stoxx-Niveau statt DAX (Sprünge von −75 % und +270 %) |
| WTI (WTIUSD) | keine Daten 2024 bis Mai 2026; künstlicher Sprung von +30 % am 19.04.2020 (Kontraktwechsel nach den negativen Ölpreisen) |

**Getestet wurden 10 Instrumente:** US500, US100, FRA40, UK100, JP225, HK50, AUS200, Brent, Silber und Gold.

## 2. Ergebnis

**Modell H verfehlt alle vier Kriterien. P7 ist damit gescheitert.** Der Hold-out 2024–2026 bleibt unberührt, T17 und T18 entfallen.

| Kriterium | Schwelle | Modell H |
|---|---|---|
| t-Wert (kleinster aus iid, Woche, Monat) | ≥ 3,0 | **−1,14** |
| Sharpe Ratio p. a. netto | (≈ 1,0) | **−0,37** |
| Jahre positiv | ≥ 6 von 9 | **3 von 9** |
| Instrumente positiv | ≥ 6 von 10 | **4 von 10** |
| bei doppelten Kosten | > 0 | **−6,9 % p. a.** |

**Skaliert auf 10 % Portfolio-Volatilität:**
- Rendite −3,7 % p. a., maximaler Drawdown 43 %
- Kosten p. a.: Handel 0,91 %, Swaps netto 1,93 %, Gebühr 0,12 %

**Nach Jahren** (bei 10 % Volatilität): 2017 +10,7 % und 2020 +9,3 % liefen gut. 2016 (−16,1 %) und 2022 (−17,3 %) liefen schlecht.

## 3. Einordnung

1. **Schon vor Kosten kein Trend-Ertrag.** Allein die Kursergebnisse ergeben eine Sharpe Ratio von −0,07. Die Kosten drücken sie auf −0,37; der größte Posten sind die Finanzierungskosten der Index-CFDs (angenommener Aufschlag 2,5 % p. a.).
2. **Die US-Indizes liegen nur durch ihre Long-Lastigkeit vorn.**
   - Positiv waren US100 (Sharpe vor Kosten +0,46), US500 (+0,30) und Brent (+0,29).
   - US100 und US500 waren zu etwa drei Vierteln der Zeit long. In einem steigenden Aktienmarkt ist das überwiegend Marktrendite und kein Trend-Effekt.
   - Silber (−0,54), ASX (−0,43), FTSE (−0,31) und CAC (−0,25) verloren.
3. **2022 ist kein Gegenbeispiel.** Im Jahr mit den stärksten Trends seit Langem verlor das Portfolio. Die Bärenmarkt-Rallyes bei Aktien und die Wende beim Öl im Sommer kosteten mehr, als die Abwärtstrends brachten.
4. **Passt zur Literatur.**
   - Die dokumentierten Trendrenditen stammen aus breiten Futures-Portfolios. Dort tragen Anleihen und Zinsen sowie viele Rohstoffe (Energie, Metalle, Agrar) einen großen Teil.
   - Bei FTMO gibt es keine Anleihen, und für Agrarrohstoffe haben wir keine Daten.
   - Mit Aktienindizes allein ist Trendfolge im Wesentlichen ein gesteuertes Aktien-Exposure.

## 4. Gesamtbild nach P2–P7

| Phase | Hypothese | Ergebnis |
|---|---|---|
| P2 | 13 SMC-Bausteine einzeln | kein Baustein nach Kosten profitabel |
| P3 | Modell C: SMC-Trend-Fortsetzung | +0,015 R bzw. −0,016 R pro Trade |
| P4 | Modell D: Trendfolge mit Struktur-Exit | −0,040 R pro Trade |
| P5 | Modell F: Fix-Reversal | Effekt nur so groß wie die Kosten (Sharpe 0,31) |
| P6 | Modell G: Trendfolge D1 auf FX und Gold | Sharpe −0,53, vor Kosten −0,18 |
| P7 | Modell H: Trendfolge auf Indizes und Rohstoffen | Sharpe −0,37, vor Kosten −0,07 |

- **Sechs vorregistrierte Tests über vier Strategieansätze, keiner bestanden.** Die Ansätze waren SMC, Saisonalität um die Fixings, Trendfolge auf FX und Trendfolge auf Indizes und Rohstoffe.
- Kein Ansatz zeigt im FTMO-Instrumentarium 2015–2023 einen Vorteil, der nach Kosten trägt.
- Der Hold-out 2024–2026 wurde nie angefasst.
- **Mehrfachtesten:** Jeder weitere Versuch auf denselben In-Sample-Daten erhöht die Gefahr eines Zufallstreffers. Eine einzelne neue Idee sollte deshalb nur mit starker externer Begründung getestet werden.

## 5. Empfehlung

**Projekt beenden bzw. pausieren und keine Challenge kaufen.** Ohne nachgewiesenen Vorteil liegt die Bestehenschance bei etwa 35–42 %, das wäre ein Glücksspiel mit der Gebühr als Einsatz.

**Was bleibt:**
- Datenpipeline und Zeitmodell
- kausale Engine
- Kosten- und Swap-Modelle für FX und CFDs
- Testkette mit Vorregistrierung, In-Sample, einmaligem Hold-out und FTMO-Bootstrap
- unberührter Hold-out

## 6. Trial-Log (Fortsetzung)

| # | Datum | Test | Ergebnis |
|---|---|---|---|
| T16 | 24.10.2026 | Modell H, In-Sample (10 Instrumente) | nicht bestanden: Sharpe −0,37, t −1,14, 3 von 9 Jahren positiv |
| T17 | – | Hold-out | entfällt, Hold-out unberührt |
| T18 | – | FTMO-Bootstrap | entfällt |
