# Vorregistrierung: Modell W „Hurst-Regime-Switch“ (Strategie Nr. 40)

Festgelegt am 24.10.2026, **bevor** Code für dieses Modell geschrieben oder Daten dafür ausgewertet wurden. Änderungen nach diesem Commit zählen als neuer Versuch im Trial-Log (`../TRIAL_LOG.md`).

**Vorab festgehalten:** Die beiden Bausteine wurden einzeln getestet und sind gescheitert: Keltner-Ausbruch auf H4 (Nr. 38, T124) und Bollinger-Fade auf H1 (Nr. 37, T129). Ein Hurst-Filter wurde nicht angesehen.

## 0. Feste Rahmenbedingungen (für alle Strategien gleich)

- Expert Advisor für MetaTrader 5, handelt vollständig autonom
- FTMO 2-Step, Swing, 100.000 USD
- Max. Verlust gesamt 10 %, max. Tagesverlust 5 %
- Ziel Phase 1 +10 %, Ziel Phase 2 +5 %
- News-Trading und Halten übers Wochenende erlaubt

## 1. Hypothese

Ein Hurst-Regime-Filter macht aus Trend- und Umkehrregeln auf H4 eine Strategie mit Netto-Ertrag und t ≥ 3.

**Erwartung vor dem Test: Scheitern.**

## 2. Daten, Universum, Kosten, Zeiträume

Wie Nr. 36/38: H4-Serverkerzen, die 17 Instrumente aus Nr. 33–38, Kosten mit Spread, Kommission, Slippage und Swaps. In-Sample sind Einstiege 2015–2023 mit Kursen bis 31.12.2023; der Hold-out umfasst Einstiege ab 2024 und wird einmalig ausgewertet.

## 3. Regeln (je Instrument, Signal am Schluss der H4-Kerze i, Ausführung zur Eröffnung von i+1)

**Hurst-Schätzer H(i)** (aggregierte Varianz):
- Log-Schlusskurse über die letzten 500 Kerzen
- Für k ∈ {1, 2, 4, 8, 16} die Varianz der überlappenden k-Kerzen-Renditen ln C(t) − ln C(t−k), t = i−499+k … i
- H = ½ × Steigung der OLS-Regression von ln Var_k auf ln k

**Regime und Einstieg**

| Regime | Bedingung | Einstieg | Ausstieg (Schluss → nächste Eröffnung) |
|---|---|---|---|
| Trend | H(i) > 0,55 | Long: C(i) > EMA20 + 2 × ATR10; Short: C(i) < EMA20 − 2 × ATR10 | C kreuzt EMA20 zurück |
| Umkehr | H(i) < 0,45 | Long: C(i) < SMA20 − 2σ20; Short: C(i) > SMA20 + 2σ20 | C erreicht SMA20 oder nach 12 gehaltenen Kerzen |
| neutral | 0,45 ≤ H ≤ 0,55 | kein Einstieg | – |

**Für beide Regime gilt**
- Ausstieg nach der Regel des Regimes beim Einstieg
- Stop fest bei Einstieg ∓ 2 × ATR14(i), intrabar über Hoch und Tief (Long: Bid-Tief; Short: Bid-Hoch + Spread). Ein Gap wird zur Eröffnung gefüllt; der Stop hat Vorrang.
- Je Instrument höchstens eine Position; ein neues Signal ist frühestens am Schluss der Kerze nach dem Ausstieg möglich
- Keine neuen Einstiege an Servertagen 24.12.–01.01.
- Größe: Nominal = min(0,25 % Kapital / (2 × ATR14 / Kurs), 10 × Kapital)
- Portfolio: Summe aller Instrumente; Ergebnis am Servertag des Ausstiegs, Tage ohne Ausstieg zählen als 0

## 4. Akzeptanzkriterien

Wie Nr. 33–39 (alle müssen erfüllt sein): t ≥ **3,0** (kleinster aus iid, Woche, Monat) bei positivem Mittel; ≥ 6 von 9 Jahren positiv; ≥ 60 % der Instrumente positiv; doppelte Kosten > 0.

**Beschreibend:**
- Anteil der Kerzen je Regime, Verteilung von H
- Ergebnis je Regime
- Vergleich: Trend- und Umkehrregel ohne Filter auf denselben Daten

**Hold-out und FTMO:** wie Nr. 16, nur bei Bestehen.

## 5. Umsetzbarkeit als MT5-EA

Der Hurst-Schätzer wird aus H4-Serverkerzen berechnet (500 Werte, 5 Skalen); dazu kommen Standard-Indikatoren. Es werden keine externen Daten benötigt.

## 6. Trial-Log (Fortsetzung des globalen Logs)

| # | Test |
|---|---|
| T135 | W-HURST (Nr. 40), In-Sample |
| T136, T137 | Hold-out, FTMO (nur bei Bestehen) |
