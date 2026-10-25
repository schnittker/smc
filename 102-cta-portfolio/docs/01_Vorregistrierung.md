# Vorregistrierung: Modell C „Multi-Asset-Trend (CTA)“ (Strategie Nr. 102)

Festgelegt am 25.10.2026, **bevor** Code für dieses Modell geschrieben oder das Portfolio ausgewertet wurde. Änderungen nach diesem Commit zählen als neuer Versuch im Trial-Log (`../TRIAL_LOG.md`).

**Vorab bekannt:** die IS-Ergebnisse von Nr. 3, 4, 14, 101 und die Hold-out-Daten von US500 und den USD-Majors aus Nr. 100 (siehe Recherche). **Erwartung:** C-FIX scheitert; C-WF hängt an Krypto.

## 0. Feste Rahmenbedingungen (für alle Strategien gleich)

- Expert Advisor für MetaTrader 5, handelt vollständig autonom
- FTMO 2-Step, Swing, 100.000 USD
- Max. Verlust gesamt 10 %, max. Tagesverlust 5 %
- Ziel Phase 1 +10 %, Ziel Phase 2 +5 %
- News-Trading und Halten übers Wochenende erlaubt

## 1. Universum (24 Märkte, 4 Klassen)

| Klasse | Märkte | Daten, Kosten |
|---|---|---|
| FX | EURUSD, GBPUSD, AUDUSD, NZDUSD, USDJPY, USDCAD, USDCHF | HistData; FX-Kostenmodell (`carry.CarrySpec`, Swap aus Zinsdifferenz − 1 % p. a.) |
| Indizes | US500, US100, GER40, FRA40, UK100, JP225, HK50, AUS200 | HistData; Modell H (`smc.strategy_h`) |
| Rohstoffe | XAUUSD, XAGUSD, WTI, Brent | HistData; Modell H |
| Krypto | BTC, ETH, LTC, XRP, ADA | Binance-Tageskerzen 00:00 UTC; Kosten und Swap (20 % p. a.) wie Nr. 101 |

## 2. Regeln je Markt

1. **Kurse:**
   - FX und CFDs: tägliche Signal- und Bewertungskurse wie in Modell G/H (`daily_prices`, Bewertung je Markt zu seiner Sitzungszeit)
   - Krypto: Tagesschluss 00:00 UTC
2. **Signal:** s = Mittel von sign(ln(P_t / P_{t−L})) über das Rückblick-Set
   - Standard MITTEL: L = 21, 63, 126, 252 Handelstage; Krypto 30, 91, 182, 365 Kalendertage
   - Ein Markt handelt erst, wenn der längste Rückblick verfügbar ist.
3. **Volatilität:** σ = Standardabweichung der letzten 60 täglichen Log-Renditen, annualisiert (×√261 bzw. Krypto ×√365), mindestens 4 %
4. **Zielgewicht** (Nominal / Kapital): w* = s · (0,10 / N_Klasse) / σ
   - Jede Klasse hat dasselbe Risikobudget, jeder Markt darin denselben Anteil.
5. **Umschichtung:**
   - Nur wenn das Vorzeichen wechselt (inkl. auf bzw. von 0) oder |w* − w| > 0,25 · |w|
   - FX und CFDs nur an Tagen, an denen Modell G handeln darf (Mo–Do, kein Feiertag, exakte Bewertungskerze)
   - Krypto täglich
6. **Buchhaltung:** FX und CFDs mit `carry.model.run_weights` (Spread, Slippage, Kommission, Swaps, Gebühr, Worst-Case aus Hoch/Tief), Krypto wie Nr. 101
7. **Portfolio:** Summe aller Märkte je Tagesnummer (Servertag bzw. UTC-Tag). Wochenenden enthalten nur Krypto.

## 3. Varianten

- **C-FIX:** Rückblick MITTEL, alle Klassen Gewicht 1
- **C-WF (Walk-Forward, jährlich):** Vor jedem Kalenderjahr Y ab 2016 wird je Klasse festgelegt:
  - **Rückblick-Set** mit der höchsten Netto-Sharpe des Klassenbuchs über alle Vorjahre ab 2015 (wachsendes Fenster). Zur Wahl stehen:
    - SCHNELL: 10, 21, 42 Handelstage; Krypto 14, 30, 60
    - MITTEL
    - LANGSAM: 63, 126, 252; Krypto 91, 182, 365
  - **Klassengewicht** a_c = max(Sharpe_c, 0), normiert auf Summe 4. Sind alle ≤ 0, bleibt das Portfolio im Jahr Y flach.
  - Regeln für zu wenig Historie:
    - Klassen mit weniger als 1 Jahr Vorlauf: MITTEL, Gewicht 1, nicht in der Normierung
    - 2015: alles MITTEL, Gewicht 1
  - **Umstellkosten** am ersten Tag des Jahres: |a_neu · w_neu − a_alt · w_alt| × Kostensatz je Markt

## 4. Kriterien

**In-Sample 2015–2023:** alle müssen erfüllt sein.
- mittleres Netto-Tagesergebnis > 0 mit t ≥ **3,0** (kleinster aus iid, Woche, Monat)
- ≥ 6 von 9 Jahren positiv
- ≥ 3 von 4 Klassen netto positiv
- doppelte Kosten (Handel und Swap) > 0

Bestehen beide Varianten, geht die mit dem höheren t in den Hold-out. Vorher gilt die Artefakt-Prüfung (Spielregel 6).

**Beschreibend:**
- je Klasse und Jahr
- Long/Short
- Kosten und Swaps getrennt
- C-WF: gewählte Sets und Gewichte je Jahr
- maximale Margin-Auslastung

**Hold-out** (01.01.2024–16.10.2026, Ende der HistData-Daten, einmalig):

| # | Kriterium |
|---|---|
| 1 | Mittleres Netto-Tagesergebnis > 0 |
| 2 | ≥ untere Grenze des 95-%-Konfidenzintervalls von IS (Cluster-Bootstrap nach Monat) |

**FTMO** (Tagesreihe IS + Hold-out, nur falls der Hold-out besteht):
- wie Nr. 100/101: Stufen 0,5 / 0,75 / 1,0 / 1,25 % Tagesschwankung, Phase 2 × 0,75, De-Risk ab 3 %/6 %
- Worst-Case gegen 5 % und 10 %, Block-Bootstrap über Kalendermonate, 10.000 Pfade
- **Margin-Grenze:** Je Tag wird die Skalierung so begrenzt, dass Σ |w_i| / Hebel_i ≤ 0,5 (Hebel FX 30, Indizes 15, Metalle 9, Energie 9, Krypto 1)
- **Bestanden** bei mindestens einer Stufe mit ≥ 70 % Chance für beide Phasen und ≤ 12 Monaten Median-Dauer

## 5. Umsetzbarkeit als MT5-EA

Der EA berechnet einmal täglich je Markt zu dessen Bewertungszeit Signal und σ aus den D1-Kerzen und schichtet bei Bedarf per Marktorder um. C-WF stellt einmal pro Jahr Set und Gewichte um; die Werte können im EA auch als Parameter hinterlegt werden. Es werden keine externen Daten benötigt.

## 6. Trial-Log (Fortsetzung des globalen Logs)

| # | Test |
|---|---|
| T313 | C-FIX (Nr. 102), In-Sample |
| T314 | C-WF (Nr. 102), In-Sample |
| T315 | Hold-out der gewählten Variante (nur bei Bestehen) |
| T316 | FTMO-Bootstrap (nur falls T315 besteht) |
