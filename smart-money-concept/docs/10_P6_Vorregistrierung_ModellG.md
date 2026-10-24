# P6 – Vorregistrierung: Modell G „Trendfolge D1“ (Zeitreihen-Momentum)

Festgelegt am 24.10.2026, **bevor** Code für dieses Modell geschrieben oder Daten dafür ausgewertet wurden. Änderungen nach diesem Commit zählen als neuer Versuch im Trial-Log.

## 1. Hypothese und Evidenz

Instrumente, die in den letzten 1, 3 und 12 Monaten gestiegen sind, steigen im Mittel weiter, fallende fallen weiter. Ein volatilitätsskaliertes Portfolio daraus hat eine positive Sharpe Ratio.

**Grundlage:**
- Moskowitz, Ooi & Pedersen (2012, *Journal of Financial Economics*), „Time series momentum“
- Hurst, Ooi & Pedersen (2017, *Journal of Portfolio Management*), „A Century of Evidence on Trend-Following Investing“
  - Signale aus 1-, 3- und 12-Monats-Renditen
  - jede Position auf gleiche Volatilität skaliert

**Vorab festgehalten:**
- Die Evidenz stammt aus breiten Futures-Portfolios (Aktienindizes, Anleihen, Rohstoffe, Währungen). Hier stehen nur G10-FX und Gold zur Verfügung, und viele der 25 Instrumente sind eng korreliert.
- Für FTMO in 6 Monaten bräuchte es eine Sharpe Ratio um 1. **Erwartung vor dem Test: deutlich darunter.**

## 2. Daten und Zeiträume

- HistData M5 (Bid), alle 25 Instrumente
- Warm-up 2014 für die 12-Monats-Signale
- **In-Sample (IS):** Handelstage 01.01.2015–31.12.2023
- **Hold-out (HO):** 01.01.2024 bis Datenende (16.10.2026)
  - Er wird genau **einmal** ausgewertet und nur, wenn IS besteht.
- Zinsen für Swaps wie in P4 (FRED)

## 3. Regeln

**Tagespreise** (Handelstag = Server-Tag Mo–Fr, 17:00–17:00 New York)
- **Signalpreis:** Kurs um 16:45 New York, also der Close der letzten M5-Kerze, die bis dahin endet.
- **Bewertungs- und Ausführungspreis:** Kurs um 16:50 New York, kurz vor dem Rollover.
- Tagesrendite = log. Änderung des Signalpreises gegenüber dem vorigen Handelstag.

**Signal und Positionsgröße je Instrument** (an jedem Handelstag mit Signalpreis)
- **Trend:** `s = (sign(R21) + sign(R63) + sign(R252)) / 3`
  - `Rk` = log. Rendite des Signalpreises über k Handelstage
  - Ergebnis ∈ {−1, −⅓, +⅓, +1}; Long bei s > 0, Short bei s < 0
- **Volatilität:** EWMA der quadrierten Tagesrenditen mit Schwerpunkt 60 Tage (α = 1/61), annualisiert mit √261.
  - Untergrenze 4 % p. a.
  - Startwert: Varianz der ersten 60 Tagesrenditen.
- **Zielposition** (Nominalwert in Vielfachen des Kapitals): `w = s × 10 % / σ`
  - Je Instrument gleiches Risiko. Die Skalierung des Gesamtportfolios folgt erst in der FTMO-Stufe.

**Umschichten**
- **Wann:** Montag bis Donnerstag um 16:50 New York auf die Zielposition.
  - **Freitags nie**, wegen FTMOs Verbot, in den letzten 2 Stunden vor dem Wochenende Trades zu eröffnen.
  - Kein Umschichten an FX-Tagen vom 24.12. bis 01.01.
  - Kein Umschichten, wenn die M5-Kerze bis 16:50 fehlt.
  - Sonst bleibt die Position stehen.
- **Ergebnis je Instrument und Tag** (in Kapitalanteilen): Position × relative Änderung des Bewertungspreises.
- Halten über Nacht und Wochenende ist erlaubt (Swing-Konto).

**Kosten**
- **Handel:** je gehandeltem Nominal `(Spread / 2 + Slippage + Kommission Round Turn / 2) / Kurs`.
  - Spread = typischer Raw-Spread + 0,3 Pip Volume-Band-Zuschlag; Gold + 0,05 USD
  - Slippage 0,1 Pip bzw. 0,02 USD
  - Kommission 5 USD pro Lot Round Turn bzw. 0,0014 % bei Gold
- **Swaps:** wie P4 (Zinsdifferenz − 1 % p. a., Mittwoch dreifach), je Rollover auf den gehaltenen Nominalwert.
- **0,7-%-Gebühr:** auf das realisierte Ergebnis bei Profit-Währung ≠ USD.
  - Vereinfacht: Realisiert wird je Episode, das ist die Haltephase mit gleichem Vorzeichen.
  - Fällig wird die Gebühr beim Vorzeichenwechsel oder Schließen.

**Portfolio**
- Tagesergebnis = Summe über alle Instrumente.
- Die Bewertung (Kriterien 1–4) ist unabhängig von der Gesamtskalierung.

## 4. Akzeptanzkriterien

**In-Sample** (alle müssen erfüllt sein)

| # | Kriterium |
|---|---|
| 1 | Mittleres Netto-Tagesergebnis > 0 mit t-Wert ≥ **3,0**, als kleinster Wert aus iid (Tage) und Clustern nach Woche und Monat. Über 9 Jahre entspricht das einer Sharpe Ratio von etwa ≥ 1,0. |
| 2 | ≥ 6 von 9 Jahren positiv |
| 3 | ≥ 60 % der Instrumente mit positivem Netto-Beitrag (≥ 15 von 25) |
| 4 | Mittleres Tagesergebnis bei doppelten Kosten > 0 (Handelskosten, Gebühr und belastende Swaps verdoppelt; Swap-Gutschriften nicht) |

Besteht Modell G nicht, ist **P6 gescheitert**, und der Hold-out bleibt unberührt.

**Hold-out** (einmalig)

| # | Kriterium |
|---|---|
| 1 | Mittleres Netto-Tagesergebnis > 0 |
| 2 | ≥ untere Grenze des 95-%-Konfidenzintervalls von IS (Cluster-Bootstrap nach Monat) |

**FTMO** (Tagesergebnisse IS + HO, nur falls der Hold-out besteht)

- **Skalierung:** Ziel-Volatilität des Portfolios 10 %, 15 % bzw. 20 % p. a., kalibriert auf die IS-Tagesergebnisse.
  - Phase 2 mit dem 0,75-Fachen.
  - Ab 3 % Drawdown wird halbiert, ab 6 % geviertelt.
- **Daily Loss:**
  - Bezug ist das Maximum aus Equity und Balance zu Beginn des Prager Tags, minus 5.000.
  - Die Balance wird nach Episoden realisiert. Das Maximum ist mindestens so streng wie FTMOs Regel „Balance zu Tagesbeginn“.
  - Für den Tagesverlauf zählt im Worst Case die Summe der ungünstigsten M5-Ausschläge aller offenen Positionen.
- **Max Loss:** Equity im Worst Case ≥ 90.000.
- **Ziel:** Equity zum Tagesbewertungskurs ≥ Ziel + 300. Dann wird alles geschlossen (Zielsicherung), und die Phase ist bestanden, sofern 4 Handelstage erreicht sind.
- **Block-Bootstrap:** über Kalendermonate, 10.000 Pfade, höchstens 120 Monate.
- **Bestanden:** wenn für mindestens eine Ziel-Volatilität gilt:
  - Bestehenschance beider Phasen ≥ 70 %
  - Median-Dauer ≤ 6 Monate
- Alle drei Stufen werden berichtet.

**FTMO-Konformität, vorab festgehalten**
- Ein Trendportfolio hält oft mehrere USD-Paare in dieselbe Richtung („one big dollar bet“, Forbidden Trading Practices).
- Vor einem Kauf muss beim Support geklärt sein, ob ein volatilitätsbegrenztes Portfolio aus bis zu 25 Positionen akzeptiert wird.

## 5. Trial-Log (Fortsetzung)

| # | Test |
|---|---|
| T13 | Modell G, In-Sample |
| T14 | Hold-out (nur falls T13 besteht) |
| T15 | FTMO-Bootstrap (nur falls T14 besteht) |
