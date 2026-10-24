# Vorregistrierung: Modell TI „Trendindikatoren“ (Strategien Nr. 61–64, 69–73, 76)

Festgelegt am 24.10.2026, **bevor** Code für dieses Modell geschrieben oder Daten dafür ausgewertet wurden. Änderungen nach diesem Commit zählen als neuer Versuch im Trial-Log (`../TRIAL_LOG.md`).

**Vorab festgehalten:** D1-, H4- und H1-Daten der 17 Instrumente wurden für viele Trend- und Ausbruchsregeln ausgewertet (Nr. 3, 4, 28, 30, 33–40, 45, 53). Die hier genannten Indikatoren wurden nicht ausgewertet. Nur EMA20/EMA200 (Nr. 38) und ADX < 20 als Filter (Nr. 37) kamen vor.

## 0. Feste Rahmenbedingungen (für alle Strategien gleich)

- Expert Advisor für MetaTrader 5, handelt vollständig autonom
- FTMO 2-Step, Swing, 100.000 USD
- Max. Verlust gesamt 10 %, max. Tagesverlust 5 %
- Ziel Phase 1 +10 %, Ziel Phase 2 +5 %
- News-Trading und Halten übers Wochenende erlaubt

## 1. Hypothese

Jeder der zehn Indikatoren verdient als Trendregel nach Kosten mit t ≥ 3. **Erwartung vor dem Test: Scheitern aller zehn.**

## 2. Daten, Universum, Kosten, Zeiträume

- **Universum:** die 17 Instrumente aus Nr. 33–38
- **Kerzen:** H1- und H4-Serverkerzen; D1 = Servertage Mo–Fr aus M5 (`dbo.model.server_days`)
- **Kosten und Swaps:** wie Nr. 36/38
- **In-Sample:** Einstiege 2015–2023, Kurse bis 31.12.2023. **Hold-out:** ab 2024, einmalig je bestandener Variante.

## 3. Regeln

**Zustand Z(i) je Variante am Schluss der Kerze i (+1 long, −1 short, 0 flat)**

| Variante | Nr. | TF | Z = +1 | Z = −1 | sonst |
|---|---|---|---|---|---|
| **TI-MA200** | 61 | D1 | SMA50 > SMA200 (Schlusskurse) | SMA50 < SMA200 | – |
| **TI-EMA921** | 62 | H1 | EMA9 > EMA21 | EMA9 < EMA21 | – |
| **TI-TRIPLE** | 63 | H4 | EMA10 > EMA20 > EMA50 | EMA10 < EMA20 < EMA50 | 0 |
| **TI-MACD** | 64 | H4 | MACD(12,26) > Signal(9) | MACD < Signal | – |
| **TI-ADX** | 69 | H4 | ADX14 > 25 und +DI > −DI | ADX14 > 25 und −DI > +DI | 0 |
| **TI-PSAR** | 70 | H4 | Parabolic SAR (Start 0,02, Schritt 0,02, max. 0,2) unter dem Kurs | SAR über dem Kurs | – |
| **TI-SUPER** | 71 | H4 | Supertrend (ATR10 Wilder, Faktor 3, Mittel (H+L)/2) aufwärts | abwärts | – |
| **TI-ICHI** | 72 | H4 | C > max(Senkou A, Senkou B) der Wolke bei i und Tenkan > Kijun | C < min(…) und Tenkan < Kijun | 0 |
| **TI-HA** | 73 | H4 | die letzten 2 Heikin-Ashi-Kerzen grün (HA-Close > HA-Open) | die letzten 2 rot | vorheriger Zustand |
| **TI-KALMAN** | 76 | H4 | geschätzte Steigung > 0 | < 0 | – |

**Indikator-Details**
- EMA mit α = 2/(n+1); MACD = EMA12 − EMA26, Signal = EMA9 des MACD
- ADX/DI nach Wilder wie Nr. 37
- **Ichimoku:** Tenkan = Mitte der 9-Kerzen-Spanne, Kijun = Mitte der 26-Kerzen-Spanne. Senkou A = (Tenkan + Kijun)/2 und Senkou B = Mitte der 52er-Spanne, beide 26 Kerzen nach vorn verschoben (die Wolke bei i stammt aus i−26).
- **Kalman:** lokales lineares Trendmodell auf ln C. Beobachtungsrauschen R = Varianz der 1-Kerzen-Log-Renditen der letzten 500 Kerzen; Zustandsrauschen nur auf der Steigung mit Q = 0,001 × R; Start mit großer Unsicherheit. Die Steigung ist der gefilterte Schätzwert bei i.

**Handel**
- Wechselt Z(i) gegenüber Z(i−1), wird zur Eröffnung von i+1 die laufende Position geschlossen und gegebenenfalls in Richtung Z(i) neu eröffnet (Stop-and-Reverse).
- Ein Einstieg erfolgt nur bei einem Zustandswechsel. Nach einem Notfall-Stop wird erst beim nächsten Wechsel wieder eingestiegen.
- **Notfall-Stop:** fest 3 × ATR14(i) vom Einstieg, intrabar (Long: Bid; Short: Bid + Spread); ein Gap wird zur Eröffnung gefüllt
- **Größe:** Nominal = min(0,25 % Kapital / (3 × ATR14 / Kurs), 10 × Kapital)
- Keine neuen Einstiege an Servertagen 24.12.–01.01.
- **Portfolio:** Summe aller Instrumente; Ergebnis am Servertag des Ausstiegs, Tage ohne Ausstieg zählen als 0

## 4. Akzeptanzkriterien

Wie Nr. 33–59 (alle müssen erfüllt sein): t ≥ **3,0** (kleinster aus iid, Woche, Monat) bei positivem Mittel; ≥ 6 von 9 Jahren positiv; ≥ 60 % der Instrumente positiv; doppelte Kosten > 0. Jede Variante wird für sich bewertet. Vor einem Hold-out gilt die Artefakt-Prüfung (Spielregel 6).

**Beschreibend:** Trades, Ø R vor und nach Kosten, Notfall-Stops, Haltedauer, Ergebnis je Anlageklasse.

**Hold-out und FTMO:** wie Nr. 16.

## 5. Umsetzbarkeit als MT5-EA

Alle Indikatoren sind Standard in MT5 oder einfach nachzubauen (Kalman). Marktorders bei Zustandswechsel, fester Notfall-Stop. Es werden keine externen Daten benötigt.

## 6. Trial-Log (Fortsetzung des globalen Logs)

| # | Test |
|---|---|
| T219 | TI-MA200 (Nr. 61), In-Sample |
| T220 | TI-EMA921 (Nr. 62), In-Sample |
| T221 | TI-TRIPLE (Nr. 63), In-Sample |
| T222 | TI-MACD (Nr. 64), In-Sample |
| T223 | TI-ADX (Nr. 69), In-Sample |
| T224 | TI-PSAR (Nr. 70), In-Sample |
| T225 | TI-SUPER (Nr. 71), In-Sample |
| T226 | TI-ICHI (Nr. 72), In-Sample |
| T227 | TI-HA (Nr. 73), In-Sample |
| T228 | TI-KALMAN (Nr. 76), In-Sample |
| T229–T248 | Hold-out und FTMO je bestandener Variante |
