# Vorregistrierung: Modell HP „Harmonische Muster, Wyckoff-Spring, Scalping“ (Strategien Nr. 77, 79, 80)

Festgelegt am 24.10.2026, **bevor** Code für dieses Modell geschrieben oder Daten dafür ausgewertet wurden. Änderungen nach diesem Commit zählen als neuer Versuch im Trial-Log (`../TRIAL_LOG.md`).

**Vorab festgehalten:** Folgende verwandte Tests liegen vor:
- H4-Swings (3/3) und Swing-basierte Regeln in Nr. 50–55, 60, 75
- EMA 9/21 auf H1 in Nr. 62
- M5-Daten der Majors für Nr. 31/32 (Sitzungen)

XABCD-Muster, Springs/Upthrusts und M5-Crossovers wurden nicht angesehen.

**Nr. 78 (Elliott-Wellen) wird nicht getestet:** Die Zählung ist nicht vorab eindeutig formalisierbar (⊘).

## 0. Feste Rahmenbedingungen (für alle Strategien gleich)

- Expert Advisor für MetaTrader 5, handelt vollständig autonom
- FTMO 2-Step, Swing, 100.000 USD
- Max. Verlust gesamt 10 %, max. Tagesverlust 5 %
- Ziel Phase 1 +10 %, Ziel Phase 2 +5 %
- News-Trading und Halten übers Wochenende erlaubt

## 1. Hypothese

Jede der drei Regeln verdient nach Kosten mit t ≥ 3. **Erwartung vor dem Test: Scheitern aller drei.**

## 2. Daten, Universum, Kosten, Zeiträume

- **HP-HARM, HP-SPRING:** H4-Serverkerzen der 17 Instrumente, Engine `chart.engine` (Einstieg zur nächsten Eröffnung, fester Stop, Limit-Ziel, Zeitstopp 30 Kerzen, im Einstiegsbar nur Stop)
- **HP-SCALP:** M5-Kerzen der 7 Majors, Engine wie Nr. 65–67 (Ausstiegssignal, Stop, Zeitstopp)
- **Kosten und Swaps:** wie Nr. 36/38
- **In-Sample:** Einstiege 2015–2023, Kurse bis 31.12.2023. **Hold-out:** ab 2024, einmalig je bestandener Variante.

## 3. Regeln (Signal am Schluss der Kerze i, Einstieg zur Eröffnung von i+1)

**HP-HARM (Nr. 77)**
- Die letzten fünf bestätigten, abwechselnden Swing-Punkte X, A, B, C, D, wobei D am Bar i bestätigt wird (D = i − 3)
- **Bullisch:** X Tief, A Hoch, B Tief, C Hoch, D Tief

| Muster | AB / XA | BC / AB | AD / XA |
|---|---|---|---|
| Gartley | 0,568–0,668 | 0,382–0,886 | 0,736–0,836 |
| Bat | 0,382–0,500 | 0,382–0,886 | 0,836–0,936 |

- **Long** bei D. **Stop:** X − 0,25 ATR14 (mindestens 1 ATR vom Einstieg). **Ziel:** D + 0,618 × (A − D) als Limit.
- **Bärisch** gespiegelt.
- Folgen aufeinanderfolgende Swings nicht abwechselnd, wird je Folge gleicher Art nur der jeweils extremste verwendet: höchstes Hoch bzw. tiefstes Tief.

**HP-SPRING (Nr. 79)**
- **Handelsspanne:** Hoch RH und Tief RL der Kerzen i−40 … i−1 mit RH − RL ≤ 6 × ATR14(i)
- **Spring:** L(i) < RL und C(i) > RL → Long. **Stop:** L(i) − 0,25 ATR (mindestens 1 ATR). **Ziel:** RH als Limit.
- **Upthrust** gespiegelt: H(i) > RH und C(i) < RH → Short. **Stop:** H(i) + 0,25 ATR. **Ziel:** RL.

**HP-SCALP (Nr. 80)**
- Nur Signale, deren Einstiegskerze zwischen 07:00 und 15:55 London liegt
- **Long:** EMA9 kreuzt EMA21 der M5-Schlusskurse von unten (EMA9(i−1) ≤ EMA21(i−1), EMA9(i) > EMA21(i)). **Short** gespiegelt.
- **Ausstieg** zur nächsten Eröffnung bei der Gegenkreuzung oder nach 12 gehaltenen Kerzen (1 h)
- **Stop:** fest 1,5 × ATR14(M5)

**Gemeinsam**
- Je Instrument höchstens eine Position; ein neues Signal frühestens am Schluss der Kerze nach dem Ausstieg
- Keine neuen Einstiege an Servertagen 24.12.–01.01.
- **Größe:** Nominal = min(0,25 % Kapital / (R / Einstieg), 10 × Kapital)
- **Portfolio:** Summe aller Instrumente; Ergebnis am Servertag des Ausstiegs, Tage ohne Ausstieg zählen als 0

## 4. Akzeptanzkriterien

Wie Nr. 33–76 (alle müssen erfüllt sein): t ≥ **3,0** (kleinster aus iid, Woche, Monat) bei positivem Mittel; ≥ 6 von 9 Jahren positiv; ≥ 60 % der Instrumente positiv; doppelte Kosten > 0. Jede Variante wird für sich bewertet. Vor einem Hold-out gilt die Artefakt-Prüfung (Spielregel 6).

**Hold-out und FTMO:** wie Nr. 16.

## 5. Umsetzbarkeit als MT5-EA

Swings und Muster aus H4-Serverkerzen bzw. EMAs auf M5, Marktorders mit festem Stop. Es werden keine externen Daten benötigt.

## 6. Trial-Log (Fortsetzung des globalen Logs)

| # | Test |
|---|---|
| T267 | HP-HARM (Nr. 77), In-Sample |
| T268 | HP-SPRING (Nr. 79), In-Sample |
| T269 | HP-SCALP (Nr. 80), In-Sample |
| T270–T275 | Hold-out und FTMO je bestandener Variante |
