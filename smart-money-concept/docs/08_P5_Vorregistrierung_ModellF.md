# P5 – Vorregistrierung: Modell F „Fix-Reversal“

Festgelegt am 24.10.2026, **bevor** Code für dieses Modell geschrieben oder Daten dafür ausgewertet wurden. Änderungen nach diesem Commit zählen als neuer Versuch im Trial-Log.

## 1. Hypothese und Evidenz

Der USD wertet vor den großen Fixings auf und danach wieder ab, ein „W-Muster“ über den Tag (Krohn, Mueller & Whelan, *Journal of Finance* 2024; Working Paper Bank of Canada 21-48). Daten des Papers: 1999–2019, Refinitiv-Quotes, G9-Währungen gegen USD.

| Fenster laut Paper (New-York-Zeit) | USD | EUR | GBP | JPY |
|---|---|---|---|---|
| pre-Tokio: 17:00 bis Tokio-Fix (9:55 Tokio) | steigt | −4,5 % p. a. | −4,8 % | −4,1 % |
| post-Tokio: Fix bis 8:00 Frankfurt | fällt | +5,9 % | +3,2 % | +7,9 % |
| pre-EZB: 8:00 Frankfurt bis EZB-Fix (14:15 Frankfurt) | steigt | −8,9 % | −5,8 % | −2,6 % |
| post-London: London-Fix (16:00 London) bis 17:00 | fällt | +6,9 % | +6,7 % | **−2,9 %** (Ausnahme) |

Prozent = annualisierte Rendite der Fremdwährung gegen USD.

**Bekannte Schwächen, vorab festgehalten:**
- Der Effekt ist geschrumpft. Für das Dollar-Portfolio 2014–2019 nennt das Paper je Fenster nur noch 1,6–3,1 % p. a. Das sind rund 1 bp pro Tag und Fenster und damit etwa so viel wie unsere FTMO-Kosten.
- Mit vollen Spreads sind die Strategien des Papers verlustreich, mit 50 % der Spreads leicht profitabel.
- Seit 2024 ist das Ergebnis veröffentlicht. Der Hold-out 2024–2026 liegt komplett danach.
- **Erwartung vor dem Test: eher Scheitern.**

## 2. Daten und Zeiträume

- HistData M5 (Bid), umgerechnet in UTC und FTMO-Serverzeit
- **In-Sample (IS):** FX-Tage vom 01.01.2015 bis 31.12.2023
- **Hold-out (HO):** FX-Tage vom 01.01.2024 bis Datenende (16.10.2026)
  - Er wird genau **einmal** ausgewertet, nur für die gewählte Variante und nur wenn sie IS besteht.
- **Instrumente:** EURUSD, GBPUSD, USDJPY. Das sind die drei Paare, die das Paper mit Kosten untersucht, und die mit den niedrigsten FTMO-Kosten.
  - AUDUSD, NZDUSD, USDCAD und USDCHF werden nur beschreibend mitgerechnet und gehen in keine Entscheidung ein.

## 3. Regeln

**Zeitfenster eines FX-Tags** (Ortszeiten mit der jeweiligen Sommerzeitregel; Tokio ohne Sommerzeit)

| Fenster | Einstieg | Ausstieg | Position |
|---|---|---|---|
| W1 pre-Tokio | 17:30 New York (Serverzeit 00:30) | Tokio-Fix 9:55 Tokio | Long USD |
| W2 post-Tokio | Tokio-Fix 9:55 Tokio | 8:00 Frankfurt | Short USD |
| W3 pre-EZB | 8:00 Frankfurt | EZB-Fix 14:15 Frankfurt | Long USD |
| W4 post-London | London-Fix 16:00 London | 16:50 New York (Serverzeit 23:50) | Short USD |

- „Long USD“ heißt Short EURUSD und GBPUSD bzw. Long USDJPY.
- **USDJPY handelt W4 nicht.** Das Paper weist den Yen als Ausnahme aus.

**Abweichungen vom Paper, aus Kostengründen festgelegt:**
- W1 beginnt um 17:30 statt 17:00 New York und W4 endet um 16:50 statt 17:00. So bleiben Einstiege und Ausstiege aus der Spread-Ausweitung am Rollover. Keine Position hält über den Rollover, es fallen also keine Swaps an.
- W1 entfällt am Sonntagabend (Wochenöffnung, dünne Liquidität).
- Vom 24.12. bis 01.01. wird nicht gehandelt.
- Fehlt die M5-Kerze zum Einstiegs- oder Ausstiegszeitpunkt (Datenlücke), entfällt das Fenster.

**Ausführung**
- Markt zur Eröffnung der M5-Kerze, die zum Einstiegszeitpunkt beginnt.
- Ausstieg zur Eröffnung der M5-Kerze, die zum Ausstiegszeitpunkt beginnt.
- Kauf zum Ask (Bid + Spread), Verkauf zum Bid.
- **Notfall-Stop:** 3 × ATR14(H1) ab Einstieg, ATR an der letzten geschlossenen H1-Kerze. Long: Bid-Low ≤ Stop; Short: Bid-High + Spread ≥ Stop. Bei einem Gap wird zur Eröffnung gefüllt.

**Kosten** (je Position, in Basispunkten des Einstiegskurses)
- Spread: typischer Raw-Spread + 0,3 Pip Volume-Band-Zuschlag, über die Ask-Seite
- Kommission: 5 USD pro Lot Round Turn
- Slippage: 0,1 Pip bei Einstieg und bei Ausstieg bzw. Stop
- 0,7-%-Umrechnungsgebühr auf das Kursergebnis von USDJPY

**Varianten (je ein Trial)**
- **F-ALL:** alle Fenster wie oben, also 11 Positionen je Tag (EUR und GBP je W1–W4, JPY W1–W3)
- **F-EU:** nur die europäischen Fenster W3 und W4 für EURUSD und GBPUSD, also 4 Positionen je Tag. Sie haben laut Paper die stärksten und zuletzt noch signifikanten Effekte.

**Bewertungseinheit:** Tagesergebnis = Summe der Netto-Ergebnisse (bp) aller Positionen des FX-Tags, gleicher Nominalwert je Position. Ein FX-Tag läuft von 17:00 bis 17:00 New York.

## 4. Akzeptanzkriterien

**In-Sample, je Variante** (alle müssen erfüllt sein)

| # | Kriterium |
|---|---|
| 1 | Mittleres Netto-Tagesergebnis > 0 mit t-Wert ≥ **3,0**, als kleinster Wert aus iid (Tage) und Clustern nach Woche und Monat. Über 9 Jahre entspricht das einer Sharpe Ratio von etwa ≥ 1,0. |
| 2 | ≥ 6 von 9 Jahren mit positivem Netto-Ergebnis |
| 3 | ≥ 60 % der gehandelten Paare mit positivem Netto-Ergebnis (F-ALL: ≥ 2 von 3, F-EU: 2 von 2) |
| 4 | Mittleres Tagesergebnis bei doppelten Kosten > 0 |

**Variantenwahl:** Bestehen beide Varianten, gewinnt die mit dem höheren t-Wert. Besteht keine, ist **P5 gescheitert**, und der Hold-out bleibt unberührt.

**Hold-out** (einmalig, gewählte Variante)

| # | Kriterium |
|---|---|
| 1 | Mittleres Netto-Tagesergebnis > 0 |
| 2 | Mittleres Netto-Tagesergebnis ≥ untere Grenze des 95-%-Konfidenzintervalls von IS (Cluster-Bootstrap nach Monat) |

**FTMO** (Tagesergebnisse IS + HO, nur falls der Hold-out besteht)

- **Skalierung auf Ziel-Volatilität:** Die Tagesschwankung des Kontos (Standardabweichung) liegt bei 0,5 %, 0,75 %, 1,0 % bzw. 1,25 % des Anfangskapitals.
  - Kalibriert wird auf die IS-Tagesergebnisse.
  - In Phase 2 gilt das 0,75-Fache. Ab 3 % Drawdown wird halbiert, ab 6 % geviertelt.
- **Worst Case für Daily Loss und Max Loss:** Je Fenster zählt die Summe der ungünstigsten Kursausschläge aller offenen Positionen (M5-Extreme).
  - Der FTMO-Tag ist der Prager Kalendertag. Maßgeblich ist die Balance zum Tagesbeginn.
- **Bootstrap:** Block-Bootstrap über Kalendermonate, 10.000 Pfade, höchstens 120 Monate je Pfad.
- **Bestanden:** wenn für mindestens eine Ziel-Volatilität gilt:
  - Bestehenschance beider Phasen ≥ 70 %
  - Median-Dauer ≤ 6 Monate
- Alle vier Stufen werden berichtet.

**FTMO-Konformität, vorab festgehalten**
- FTMO bezeichnet mehrere USD-Paare gleichzeitig als „one big dollar bet“ (Forbidden Trading Practices, Punkt Overexposure). F-ALL hält bis zu drei USD-Positionen in dieselbe Richtung.
- Bevor Geld eingesetzt wird, klären wir beim Support, ob das als eine Trade-Idee mit begrenztem Gesamtrisiko akzeptiert wird.
- F-EU ist mit zwei Paaren weniger betroffen.

## 5. Trial-Log (Fortsetzung)

| # | Test |
|---|---|
| T9 | F-ALL, In-Sample |
| T10 | F-EU, In-Sample |
| T11 | Hold-out der gewählten Variante (nur falls T9 oder T10 besteht) |
| T12 | FTMO-Bootstrap (nur falls T11 besteht) |
