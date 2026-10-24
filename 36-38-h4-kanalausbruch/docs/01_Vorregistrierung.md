# Vorregistrierung: Modell K „H4-Kanal-Ausbruch“ (Strategien Nr. 36 und 38)

Festgelegt am 24.10.2026, **bevor** Code für dieses Modell geschrieben oder Daten dafür ausgewertet wurden. Änderungen nach diesem Commit zählen als neuer Versuch im Trial-Log (`../TRIAL_LOG.md`).

**Vorab festgehalten:** Alle Instrumente wurden in früheren Tests mit D1-Trend- und Ausbruchsregeln ausgewertet (Nr. 3, 4, 28, 30, 33–35); diese sind alle gescheitert. H4-Bänder wurden nicht angesehen.

## 0. Feste Rahmenbedingungen (für alle Strategien gleich)

- Expert Advisor für MetaTrader 5, handelt vollständig autonom
- FTMO 2-Step, Swing, 100.000 USD
- Max. Verlust gesamt 10 %, max. Tagesverlust 5 %
- Ziel Phase 1 +10 %, Ziel Phase 2 +5 %
- News-Trading und Halten übers Wochenende erlaubt

## 1. Hypothese

Bollinger-Squeeze- und Keltner-Ausbrüche auf H4 verdienen über ein diversifiziertes Universum nach Kosten mit t ≥ 3.

**Erwartung vor dem Test: Scheitern beider.**

## 2. Daten und Zeiträume

- **H4-Kerzen** des FTMO-Servers aus HistData: 17/21/01/05/09/13 Uhr New York, Bid-Kurse.
- **Universum (17):** wie Nr. 33–35. EURUSD, GBPUSD, USDJPY, AUDUSD, NZDUSD, USDCAD, USDCHF, XAUUSD; US500, US100, FRA40, UK100, JP225, HK50, AUS200, Brent, Silber.
- **Kosten:**
  - Spread (Kauf und Short-Schluss zum Ask), Kommission, Slippage je Marktausführung (FX 0,1 Pip, CFD ¼ Spread)
  - Swaps je Rollover (Mittwoch dreifach) nach `smc.swaps` bzw. Kostenmodell H (Index: Dividende − Zins − 2,5 %)
- **In-Sample:** Einstiege 2015–2023, Kurse nur bis 31.12.2023 (offene Positionen werden zum letzten Schluss 2023 bewertet). **Hold-out:** Einstiege ab 2024, einmalig je bestandener Variante.

## 3. Regeln (je Instrument, Signale am Schluss der H4-Kerze i, Ausführung zur Eröffnung von i+1)

| Variante | Listen-Nr. | Long-Einstieg | Short-Einstieg | Ausstieg (Schluss) |
|---|---|---|---|---|
| **K-BBSQ** | 36 | Squeeze aktiv und C(i) > SMA20 + 2σ20 | Squeeze aktiv und C(i) < SMA20 − 2σ20 | C(i) kreuzt SMA20 zurück |
| **K-KELT** | 38 | C(i) > EMA20 + 2 × ATR10 und C(i) > EMA200 | C(i) < EMA20 − 2 × ATR10 und C(i) < EMA200 | C(i) kreuzt EMA20 zurück |

- **Squeeze aktiv:** Das Minimum der Bandbreite 4σ20/SMA20 über die Kerzen i−5 … i−1 ist gleich dem Minimum über i−125 … i−1, d. h. in den letzten 5 Kerzen lag ein 125-Kerzen-Tief (≈ 1 Monat für FX). σ20 ist die Standardabweichung der Grundgesamtheit.
- **ATR:** Wilder-Glättung aus True Ranges der H4-Kerzen. ATR10 dient dem Kanal, ATR14 dem Stop.
- **Stop:** fest bei Einstieg ∓ 2 × ATR14(i), intrabar über Hoch und Tief der H4-Kerzen (Long: Bid-Tief; Short: Bid-Hoch + Spread). Gap über den Stop wird zur Eröffnung gefüllt. Wird in derselben Kerze der Stop berührt und das Ausstiegssignal ausgelöst, zählt der Stop.
- **Je Instrument höchstens eine Position.** Ein neuer Einstieg ist frühestens am Schluss der Kerze nach dem Ausstieg möglich. Keine neuen Einstiege an Servertagen 24.12.–01.01.
- **Größe:** Nominal = min(0,25 % Kapital / (2 × ATR14 / Kurs), 10 × Kapital)
- **Portfolio:** Summe aller Instrumente. Das Ergebnis eines Trades wird dem Servertag seines Ausstiegs zugeordnet; Tage ohne Ausstieg zählen als 0.

## 4. Akzeptanzkriterien

Wie Nr. 33–35 (alle müssen erfüllt sein): t ≥ **3,0** (kleinster aus iid, Woche, Monat) bei positivem Mittel; ≥ 6 von 9 Jahren positiv; ≥ 60 % der Instrumente positiv; doppelte Kosten > 0. **Jede Variante wird für sich bewertet.**

**Beschreibend:** Trades, Ø R vor und nach Kosten, Swaps, Haltedauer, Trefferquote, Ergebnis je Instrument und Anlageklasse.

**Hold-out und FTMO:** wie Nr. 16, je bestandener Variante.

## 5. Umsetzbarkeit als MT5-EA

H4-Indikatoren aus Serverkerzen, Marktorder zur nächsten Kerzeneröffnung, fester Stop. Es werden keine externen Daten benötigt.

## 6. Trial-Log (Fortsetzung des globalen Logs)

| # | Test |
|---|---|
| T123 | K-BBSQ (Nr. 36), In-Sample |
| T124 | K-KELT (Nr. 38), In-Sample |
| T125–T128 | Hold-out und FTMO je bestandener Variante |
