# Vorregistrierung: Modell PA „Price Action“ (Strategien Nr. 54, 55 und 60)

Festgelegt am 24.10.2026, **bevor** Code für dieses Modell geschrieben oder Daten dafür ausgewertet wurden. Änderungen nach diesem Commit zählen als neuer Versuch im Trial-Log (`../TRIAL_LOG.md`).

**Vorab festgehalten:** Folgende verwandte Tests liegen bereits vor:
- H4-Swings und S/R-Zonen derselben 17 Instrumente in Nr. 50/51: ohne Wirkung
- Order Blocks und FVG im SMC-Projekt (Nr. 1, FX/Gold)

Candlestick-Muster, Doppelformationen und Basis-Impuls-Zonen wurden nicht angesehen.

## 0. Feste Rahmenbedingungen (für alle Strategien gleich)

- Expert Advisor für MetaTrader 5, handelt vollständig autonom
- FTMO 2-Step, Swing, 100.000 USD
- Max. Verlust gesamt 10 %, max. Tagesverlust 5 %
- Ziel Phase 1 +10 %, Ziel Phase 2 +5 %
- News-Trading und Halten übers Wochenende erlaubt

## 1. Hypothesen

Jede der folgenden Regeln verdient auf H4 nach Kosten mit t ≥ 3: Pin Bar an einer Zone (PA-PIN), Engulfing an einer Zone (PA-ENG), Doppelboden/-top (PA-DT), Supply/Demand-Retest (PA-SD).

**Erwartung vor dem Test: Scheitern aller vier.**

## 2. Daten, Universum, Kosten, Zeiträume

Wie Nr. 50/51: H4-Serverkerzen der 17 Instrumente; Spread, Kommission, Slippage und Swaps. In-Sample sind Einstiege 2015–2023, der Hold-out ab 2024 wird einmalig je bestandener Variante ausgewertet. Als Engine dient `chart.engine` (Einstieg zur nächsten Eröffnung, fester Stop, Limit-Ziel, Zeitstopp, im Einstiegsbar nur Stop).

## 3. Regeln (Signal am Schluss der H4-Kerze i; ATR = ATR14(i); R = Range H − L)

**Zonen (PA-PIN, PA-ENG):** wie Nr. 50 (Swings 3/3 der letzten 120 Kerzen; Level mit einem weiteren Swing in ±0,25 ATR). S = höchste Zone unter C(i), W = niedrigste Zone über C(i).

| Variante | Long-Signal | Stop | Ziel |
|---|---|---|---|
| **PA-PIN** (54) | R(i) ≥ 1 ATR; unterer Docht ≥ 2/3 R; Körper im oberen Drittel (min(O, C) ≥ L + 2/3 R); L(i) ≤ S + 0,25 ATR < C(i) | L(i) − 0,25 ATR | 2R |
| **PA-ENG** (54) | C(i−1) < O(i−1), C(i) > O(i), O(i) ≤ C(i−1), C(i) ≥ O(i−1); min(L(i−1), L(i)) ≤ S + 0,25 ATR < C(i) | min(L(i−1), L(i)) − 0,25 ATR | 2R |
| **PA-DT** (55) | Doppelboden: die letzten zwei bestätigten Swing-Tiefs j1 < j2 mit \|L(j1) − L(j2)\| ≤ 0,5 ATR und j2 − j1 ≥ 6; Nackenlinie N = höchstes Hoch zwischen j1 und j2; N − max(L(j1), L(j2)) ≥ 2 ATR; C(i) > N ≥ C(i−1), i > j2 | min(L(j1), L(j2)) − 0,25 ATR | N + (N − min L) |
| **PA-SD** (60) | Demand-Zone aus Basis-Kerze k (R(k) ≤ 0,8 ATR(k)) und Impuls-Kerze k+1 mit C − O ≥ 2 ATR(k+1), k ≥ i−120; proximal = max(O(k), C(k)), distal = L(k). Erster Rücklauf: L(i) ≤ proximal und C(i) > distal, wobei seit k+1 noch kein Tief ≤ proximal lag. Bei mehreren Zonen gilt die jüngste. | distal − 0,25 ATR | 2R |

Short-Signale sind jeweils gespiegelt: oberer Docht, bärisches Engulfing an W, Doppeltop, Supply-Zone. Gibt es Long und Short in derselben Kerze, entfällt das Signal.

**Gemeinsam:**
- Stop-Abstand mindestens 1 ATR vom Einstieg; Zeitstopp nach 30 Kerzen
- Je Instrument höchstens eine Position; ein neues Signal frühestens am Schluss der Kerze nach dem Ausstieg; keine neuen Einstiege an Servertagen 24.12.–01.01.
- **Größe:** Nominal = min(0,25 % Kapital / (R / Einstieg), 10 × Kapital)
- **Portfolio:** Summe aller Instrumente; Ergebnis am Servertag des Ausstiegs, Tage ohne Ausstieg zählen als 0

## 4. Akzeptanzkriterien

Wie Nr. 33–53 (alle müssen erfüllt sein): t ≥ **3,0** (kleinster aus iid, Woche, Monat) bei positivem Mittel; ≥ 6 von 9 Jahren positiv; ≥ 60 % der Instrumente positiv; doppelte Kosten > 0. Jede Variante wird für sich bewertet. Vor einem Hold-out gilt die Artefakt-Prüfung (Spielregel 6).

**Beschreibend:** Trades, Ø R vor und nach Kosten, Ausstiegsarten, Ergebnis je Instrument und Anlageklasse.

**Hold-out und FTMO:** wie Nr. 16.

## 5. Umsetzbarkeit als MT5-EA

Muster aus H4-Serverkerzen, Marktorder mit festem Stop und Limit-Ziel. Es werden keine externen Daten benötigt.

## 6. Trial-Log (Fortsetzung des globalen Logs)

| # | Test |
|---|---|
| T189 | PA-PIN (Nr. 54), In-Sample |
| T190 | PA-ENG (Nr. 54), In-Sample |
| T191 | PA-DT (Nr. 55), In-Sample |
| T192 | PA-SD (Nr. 60), In-Sample |
| T193–T200 | Hold-out und FTMO je bestandener Variante |
