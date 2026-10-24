# Vorregistrierung: Modell U „H1-Mean-Reversion“ (Strategien Nr. 37 und 39)

Festgelegt am 24.10.2026, **bevor** Code für dieses Modell geschrieben oder Daten dafür ausgewertet wurden. Änderungen nach diesem Commit zählen als neuer Versuch im Trial-Log (`../TRIAL_LOG.md`).

**Vorab festgehalten:** Folgende frühere Tests betreffen die Crosses:
- Nr. 32: Fade der Asien-Range auf EURCHF und AUDCAD (M5), vor Kosten positiv, nach Kosten negativ
- Nr. 21: Pairs auf D1
- SMC-Projekt: alle 24 Paare

H1-Bänder und z-Scores wurden nicht angesehen.

## 0. Feste Rahmenbedingungen (für alle Strategien gleich)

- Expert Advisor für MetaTrader 5, handelt vollständig autonom
- FTMO 2-Step, Swing, 100.000 USD
- Max. Verlust gesamt 10 %, max. Tagesverlust 5 %
- Ziel Phase 1 +10 %, Ziel Phase 2 +5 %
- News-Trading und Halten übers Wochenende erlaubt

## 1. Hypothese

Fades von H1-Ausschlägen auf FX-Crosses verdienen nach Kosten mit t ≥ 3, entweder über Bollinger-Bänder in Seitwärtsphasen oder über z-Scores bei kurzer OU-Halbwertszeit.

**Erwartung vor dem Test: Scheitern beider.**

## 2. Daten und Zeiträume

- **H1-Kerzen** des FTMO-Servers aus HistData, Bid-Kurse
- **Universum (17 Crosses):** EURJPY, GBPJPY, AUDJPY, NZDJPY, CADJPY, CHFJPY, EURCAD, EURCHF, EURNZD, EURAUD, GBPCHF, GBPNZD, GBPCAD, GBPAUD, AUDNZD, AUDCAD, CADCHF
- **Kosten:** FX-Kostenmodell (effektiver Spread, Kommission 5 USD je Lot, Slippage 0,1 Pip je Marktausführung, Kauf und Short-Schluss zum Ask); Swaps je Rollover (Zinsdifferenz − 1 %, Mittwoch dreifach)
- **In-Sample:** Einstiege 2015–2023, Kurse nur bis 31.12.2023. **Hold-out:** Einstiege ab 2024, einmalig je bestandener Variante.

## 3. Regeln (je Paar, Signal am Schluss der H1-Kerze i, Ausführung zur Eröffnung von i+1)

| Variante | Listen-Nr. | Long-Einstieg | Short-Einstieg | Mittellinie |
|---|---|---|---|---|
| **U-BB** | 37 | ADX14(i) < 20 und C(i) < SMA20 − 2σ20 | ADX14(i) < 20 und C(i) > SMA20 + 2σ20 | SMA20 |
| **U-OU** | 39 | HL(i) ≤ 24 und z(i) < −2 | HL(i) ≤ 24 und z(i) > +2 | SMA100 |

- **σ20:** Standardabweichung der Grundgesamtheit der letzten 20 Schlusskurse
- **z(i)** = (C(i) − SMA100(i)) / σ100(i)
- **HL(i):** OU-Halbwertszeit in Stunden aus der OLS-Regression ΔC(t) = a + β·C(t−1) über die letzten 500 Kerzen (t = i−499 … i); HL = −ln 2 / ln(1 + β), bei β ≥ 0 unendlich
- **ADX14:** nach Wilder (+DI/−DI, DX, Wilder-Glättung über 14)

**Ausstieg und Risiko (beide Varianten)**
- Ausstieg zur nächsten Eröffnung, sobald der Schluss die Mittellinie erreicht oder überschreitet (Long: C ≥ Mitte; Short: C ≤ Mitte)
- Zeitstopp: Ausstieg zur Eröffnung nach 48 gehaltenen H1-Kerzen
- **Stop:** fest bei Einstieg ∓ 2 × ATR14(i), intrabar über Hoch und Tief der H1-Kerzen (Long: Bid-Tief; Short: Bid-Hoch + Spread). Gap über den Stop wird zur Eröffnung gefüllt. Der Stop hat Vorrang vor einem Ausstiegssignal derselben Kerze.
- **Je Paar höchstens eine Position.** Ein neues Signal ist frühestens am Schluss der Kerze nach dem Ausstieg möglich. Keine neuen Einstiege an Servertagen 24.12.–01.01.
- **Größe:** Nominal = min(0,25 % Kapital / (2 × ATR14 / Kurs), 10 × Kapital)
- **Portfolio:** Summe aller Paare. Das Ergebnis eines Trades wird dem Servertag seines Ausstiegs zugeordnet; Tage ohne Ausstieg zählen als 0.

## 4. Akzeptanzkriterien

Wie Nr. 33–38 (alle müssen erfüllt sein): t ≥ **3,0** (kleinster aus iid, Woche, Monat) bei positivem Mittel; ≥ 6 von 9 Jahren positiv; ≥ 60 % der Paare positiv; doppelte Kosten > 0. **Jede Variante wird für sich bewertet.**

**Beschreibend:** Trades, Ø R vor und nach Kosten, Anteil Stops und Zeitstopps, Haltedauer, Ergebnis je Paar.

**Hold-out und FTMO:** wie Nr. 16, je bestandener Variante.

## 5. Umsetzbarkeit als MT5-EA

Indikatoren aus H1-Serverkerzen, die OU-Regression rollierend über 500 Kerzen. Marktorder zur nächsten Kerzeneröffnung, fester Stop. Es werden keine externen Daten benötigt.

## 6. Trial-Log (Fortsetzung des globalen Logs)

| # | Test |
|---|---|
| T129 | U-BB (Nr. 37), In-Sample |
| T130 | U-OU (Nr. 39), In-Sample |
| T131–T134 | Hold-out und FTMO je bestandener Variante |
