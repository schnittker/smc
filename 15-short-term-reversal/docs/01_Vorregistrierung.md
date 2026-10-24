# Vorregistrierung: Modell R „Kurzfrist-Reversal US500 (Connors)“ (Strategie Nr. 15)

Festgelegt am 24.10.2026, **bevor** Code für dieses Modell geschrieben oder Daten dafür ausgewertet wurden. Änderungen nach diesem Commit zählen als neuer Versuch im Trial-Log (`../TRIAL_LOG.md`).

**Vorab festgehalten:** US500 wurde in Nr. 4, 9–12 und 14 ausgewertet (Referenz Halten: Sharpe 0,51). Rücksetzer-Regeln wurden nicht ausgewertet.

## 0. Feste Rahmenbedingungen (für alle Strategien gleich)

- Expert Advisor für MetaTrader 5, handelt vollständig autonom
- FTMO 2-Step, Swing, 100.000 USD
- Max. Verlust gesamt 10 %, max. Tagesverlust 5 %
- Ziel Phase 1 +10 %, Ziel Phase 2 +5 %
- News-Trading und Halten übers Wochenende erlaubt

## 1. Hypothese

Rücksetzer-Käufe im Aufwärtstrend nach den Regeln von Connors & Alvarez (2008) erzielen nach Kosten eine Sharpe Ratio von ≥ 1.

**Erwartung vor dem Test: eher Scheitern am t-Kriterium.**

## 2. Daten und Zeiträume

- HistData M5 (Bid): SPXUSD → US500.cash. NSXUSD → US100.cash nur beschreibend.
- Tagesbuchhaltung, Kosten und Swaps wie Nr. 14 (Modell G aus der Engine von Nr. 6, Index-Kosten Modell H):
  - Signalkurs 15:45 New York, Ausführung und Bewertung 15:50
  - Halber Spread plus ¼ Spread Slippage je gehandeltem Nominal
  - Swap je Rollover `(Dividendenrendite − USD-Zins − 2,5 %) / 365`
- **Warm-up:** 2014 (SMA200)
- **In-Sample (IS):** Handelstage 2015–2023
- **Hold-out (HO):** ab 01.01.2024, einmalig und nur, wenn IS besteht

## 3. Regeln

Alle Indikatoren aus den täglichen 15:45-Kursen `C` (Handelstag = Tag mit exakter 15:50-Kerze), einschließlich des aktuellen Tages.

**Varianten (je ein Trial), Position Long mit Nominal = 1 × Kapital, sonst flat**

| Variante | Einstieg (wenn flat) | Ausstieg (wenn long) |
|---|---|---|
| **R-RSI2** | `C > SMA200(C)` und `RSI2(C) < 10` | `C > SMA5(C)` |
| **R-7S** | `C > SMA200(C)` und `C` = niedrigster Schluss der letzten 7 Tage | `C` = höchster Schluss der letzten 7 Tage |

- RSI2 nach Wilder (Glättung über 2 Tage, Startwert = Mittel der ersten 2 Gewinne bzw. Verluste)
- Ausführung am selben Tag um 15:50 (Signal 15:45)
- Kein Stop, kein Zeitlimit (wie im Original)

**Bewertungseinheit:** Netto-Tagesergebnis in Kapitalanteilen, flat = 0.

## 4. Akzeptanzkriterien

**In-Sample, je Variante** (alle müssen erfüllt sein)

| # | Kriterium |
|---|---|
| 1 | Mittleres Netto-Tagesergebnis > 0 mit t-Wert ≥ **3,0** (kleinster aus iid, Woche, Monat) |
| 2 | ≥ 6 von 9 Jahren positiv |
| 3 | Beide Teilzeiträume 2015–2019 und 2020–2023 mit positivem Netto-Mittel |
| 4 | Mittleres Ergebnis bei doppelten Kosten > 0 |

**Variantenwahl:** höherer t-Wert, falls beide bestehen. Besteht keine, ist **Strategie Nr. 15 gescheitert**, und der Hold-out bleibt unberührt.

**Beschreibend, ohne Einfluss auf die Entscheidung:**
- Anzahl Trades, Trefferquote, Ø Ergebnis und Ø Haltedauer je Trade, Zeit im Markt
- Vergleich mit US500 halten (Nr. 14)
- US100
- Ergebnis je Jahr

**Hold-out und FTMO:** wie Strategie Nr. 14.

## 5. Umsetzbarkeit als MT5-EA

Tägliche Prüfung um 15:45 New York aus den eigenen D1-Daten (SMA200, SMA5, RSI2, 7-Tage-Extrem), Marktorder um 15:50. Es werden keine externen Daten benötigt.

## 6. Trial-Log (Fortsetzung des globalen Logs)

| # | Test |
|---|---|
| T52 | R-RSI2, In-Sample |
| T53 | R-7S, In-Sample |
| T54 | Hold-out der gewählten Variante (nur falls T52 oder T53 besteht) |
| T55 | FTMO-Bootstrap (nur falls T54 besteht) |
