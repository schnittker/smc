# Vorregistrierung: Modell K „Krypto-Swing-Trendfolge“ (Strategie Nr. 101)

Festgelegt am 25.10.2026, **bevor** Kursdaten für Krypto geladen oder Code für dieses Modell geschrieben wurde. Änderungen nach diesem Commit zählen als neuer Versuch im Trial-Log (`../TRIAL_LOG.md`).

**Vorab festgehalten:**
- In der Reihe wurden noch keine Krypto-Daten verwendet.
- Die Krypto-Kursentwicklung (z. B. die Bärenmärkte 2018 und 2022) ist allgemein bekannt.

## 0. Feste Rahmenbedingungen (für alle Strategien gleich)

- Expert Advisor für MetaTrader 5, handelt vollständig autonom
- FTMO 2-Step, Swing, 100.000 USD
- Max. Verlust gesamt 10 %, max. Tagesverlust 5 %
- Ziel Phase 1 +10 %, Ziel Phase 2 +5 %
- News-Trading und Halten übers Wochenende erlaubt

## 1. Hypothese

Zeitreihen-Trendfolge auf Tagesbasis in den großen Kryptowährungen verdient nach pessimistischen FTMO-Kosten und -Swaps mit t ≥ 3. **Erwartung: knapp bis Scheitern, wegen der Swaps.**

## 2. Daten, Kosten, Zeiträume

- **Instrumente:** BTC, ETH, LTC, XRP, ADA. Alle sind bei FTMO handelbar und haben bei Binance einen vollständigen IS-Zeitraum.
- **Kurse:** Binance-Spot XXXUSDT, Tageskerzen 00:00 UTC (Open, High, Low, Close), 7 Tage pro Woche
- **Kosten je gehandeltem Nominal:**
  - halber Spread + Slippage von ¼ Spread + Kommission 0,0325 %
  - Spread (Ask − Bid, relativ): BTC 0,05 %, ETH 0,08 %, LTC/XRP/ADA 0,20 %
- **Swap:** 20 % p. a. auf |Nominal|, long wie short, je Kalendertag 20 %/365
- **Doppelte Kosten:** Handelskosten und Swap jeweils doppelt
- **Zeiträume:**
  - In-Sample 01.01.2018–31.12.2023: Ein Coin nimmt teil, sobald er 120 Tage Historie hat.
  - Hold-out ab 01.01.2024 bis Datenende, einmalig bei Bestehen

## 3. Regeln (je Coin, Entscheidung zum Tagesschluss 00:00 UTC, Ausführung zum selben Kurs)

1. **Signal:** s = Mittel von sign(ln(C_t / C_{t−L})) über L ∈ {7, 14, 28, 56} Tage, also s ∈ [−1, 1]
2. **Volatilität:** σ = Standardabweichung der letzten 30 täglichen Log-Renditen × √365, mindestens 30 %
3. **Zielgewicht** (Nominal / Kapital), in zwei Varianten:
   - **K-TSM** (long und short): w* = s · 0,10 / σ, |w*| ≤ 0,5
   - **K-LONG** (nur long): w* = max(s, 0) · 0,10 / σ, w* ≤ 0,5
4. **Umschichtung**, nur wenn eine der Bedingungen gilt:
   - Vorzeichen wechselt (inkl. auf bzw. von 0)
   - |w* − w| > 0,25 · |w|
   Sonst bleibt w.
5. **Hebelgrenze 1:1:** Ist Σ|w*| über alle Coins > 1,0, werden alle Zielgewichte proportional auf Σ = 1,0 gekürzt.
6. **Tagesbuchung je Coin:**
   - P&L = w · (C_t / C_{t−1} − 1) − Kosten − Swap
   - Worst-Case intraday = w · (Low/C_{t−1} − 1) bei Long, w · (High/C_{t−1} − 1) bei Short (nur Verlust)
7. **Portfolio:** Summe der Coins je Kalendertag

## 4. Akzeptanzkriterien (IS 2018–2023)

Alle müssen erfüllt sein:
- mittleres Netto-Tagesergebnis > 0 mit t ≥ **3,0** (kleinster aus iid, Woche, Monat)
- ≥ 4 von 6 Jahren positiv
- ≥ 3 von 5 Coins positiv
- doppelte Kosten > 0

Bestehen beide Varianten, geht die mit dem höheren t in den Hold-out. Vor dem Hold-out gilt die Artefakt-Prüfung (Spielregel 6).

**Beschreibend:**
- Ergebnis vor Kosten
- Kosten und Swaps getrennt
- Swap 10 % und 30 % p. a.
- je Jahr und je Coin, Long/Short getrennt (K-TSM)
- Ø Gesamtnominal und Häufigkeit der Hebelkürzung
- Halten (Buy & Hold BTC) als Referenz

**Hold-out (einmalig):**

| # | Kriterium |
|---|---|
| 1 | Mittleres Netto-Tagesergebnis > 0 |
| 2 | ≥ untere Grenze des 95-%-Konfidenzintervalls von IS (Cluster-Bootstrap nach Monat) |

**FTMO** (Tagesreihe IS + Hold-out, nur falls der Hold-out besteht):
- **Skalierung:** k = s / σ_IS für s = 0,5 %, 0,75 %, 1,0 % bzw. 1,25 % Tagesschwankung. Phase 2 mit 0,75 k. Ab 3 % Verlust wird halbiert, ab 6 % geviertelt.
- **Hebelgrenze:** Je Tag wird k auf höchstens 1 / Σ|w| begrenzt.
- **Ablauf:** Worst-Case intraday gegen 5 % Tages- und 10 % Gesamtverlust, mindestens 4 Tage mit Position
- **Bootstrap:** Block-Bootstrap über Kalendermonate, 10.000 Pfade, höchstens 60 Monate je Phase
- **Bestanden** bei mindestens einer Stufe mit ≥ 70 % Chance für beide Phasen und ≤ 12 Monaten Median-Dauer (wie Nr. 100)

## 5. Umsetzbarkeit als MT5-EA

Der EA liest um 00:00 UTC die D1-Kerzen der 5 Krypto-CFDs, berechnet Signal und σ, schichtet per Marktorder um und kürzt bei Bedarf auf Hebel 1:1. Es werden keine externen Daten benötigt. Wartungsfenster am Wochenende: Die Order wird zur nächsten Handelsmöglichkeit ausgeführt.

## 6. Trial-Log (Fortsetzung des globalen Logs)

| # | Test |
|---|---|
| T309 | K-TSM (Nr. 101), In-Sample |
| T310 | K-LONG (Nr. 101), In-Sample |
| T311 | Hold-out der gewählten Variante (nur bei Bestehen) |
| T312 | FTMO-Bootstrap (nur falls T311 besteht) |
