# Vorregistrierung: Modell G „Gold/Silber-Ratio“ (Strategie Nr. 22)

Festgelegt am 24.10.2026, **bevor** Code für dieses Modell geschrieben oder Daten dafür ausgewertet wurden. Änderungen nach diesem Commit zählen als neuer Versuch im Trial-Log (`../TRIAL_LOG.md`).

**Vorab festgehalten:** XAUUSD und XAGUSD waren Teil der Trendfolge (Nr. 3, 4) und von Nr. 18/19 (Gold). Die Ratio wurde nie ausgewertet.

## 0. Feste Rahmenbedingungen (für alle Strategien gleich)

- Expert Advisor für MetaTrader 5, handelt vollständig autonom
- FTMO 2-Step, Swing, 100.000 USD
- Max. Verlust gesamt 10 %, max. Tagesverlust 5 %
- Ziel Phase 1 +10 %, Ziel Phase 2 +5 %
- News-Trading und Halten übers Wochenende erlaubt

## 1. Hypothese

Extreme der Gold/Silber-Ratio gegenüber ihrem Mittel kehren zurück. Eine Spread-Position verdient nach Kosten mit t ≥ 3.

**Erwartung vor dem Test: Scheitern.**

## 2. Daten und Zeiträume

- HistData M5 XAUUSD und XAGUSD; Kosten und Swaps nach Modell H (SMC `smc/strategy_h.py`): FTMO-Durchschnittsspread relativ, ¼ Spread Slippage, Kommission 0,0007 % je Seite, Swap `(0 − USD-Zins) − 1 %` p. a. je Bein
- Tagesbuchhaltung von Modell G über `run_weights` (Nr. 6), Signal 15:45, Ausführung und Bewertung 15:50 New York
- **Warm-up:** 2014. Bei der 250-Tage-Variante beginnt das erste Signal Anfang 2015.
- **In-Sample (IS):** Handelstage 2015–2023
- **Hold-out (HO):** ab 01.01.2024, einmalig und nur, wenn IS besteht

## 3. Regeln

**Ratio** `q = ln(XAU) − ln(XAG)` aus den 15:45-Kursen, nur an Tagen mit Kursen beider Metalle. `z = (q − Mittel_n) / Std_n` über die letzten n Tage einschließlich heute.

**Varianten (je ein Trial)**

| Variante | n |
|---|---|
| **G-60** | 60 Tage |
| **G-250** | 250 Tage |

**Position** (Einstieg nur an Tagen, an denen beide Metalle eine exakte 15:50-Kerze haben)
- Flat und z ≥ +2 (Ratio hoch): Short Gold, Long Silber
- Flat und z ≤ −2: Long Gold, Short Silber
- Ausstieg, wenn z die Null kreuzt (Short-Ratio bei z ≤ 0, Long-Ratio bei z ≥ 0)
- **Größe:** gleicher Nominalwert `N` in beiden Beinen, `N = 10 % / σ_q` (EWMA-Volatilität der täglichen Änderung von q wie Modell G), beim Einstieg festgelegt
- Kein Stop, kein Zeitlimit

## 4. Akzeptanzkriterien

**In-Sample, je Variante** (alle müssen erfüllt sein)

| # | Kriterium |
|---|---|
| 1 | Mittleres Netto-Tagesergebnis > 0 mit t-Wert ≥ **3,0** (kleinster aus iid, Woche, Monat) |
| 2 | ≥ 6 von 9 Jahren positiv |
| 3 | Beide Teilzeiträume 2015–2019 und 2020–2023 mit positivem Netto-Mittel |
| 4 | Mittleres Ergebnis bei doppelten Kosten > 0 |

**Variantenwahl:** höherer t-Wert. Besteht keine, ist **Strategie Nr. 22 gescheitert**, und der Hold-out bleibt unberührt.

**Beschreibend:** Trades, Trefferquote, Haltedauer, Zeit im Markt, Verlauf der Ratio, Ergebnis je Jahr.

**Hold-out und FTMO:** wie Nr. 14.

## 5. Umsetzbarkeit als MT5-EA

Ratio und z-Score aus den eigenen D1-Kursen, zwei Marktorders um 15:50 New York. Es werden keine externen Daten benötigt.

## 6. Trial-Log (Fortsetzung des globalen Logs)

| # | Test |
|---|---|
| T76 | G-60, In-Sample |
| T77 | G-250, In-Sample |
| T78 | Hold-out der gewählten Variante (nur falls T76 oder T77 besteht) |
| T79 | FTMO-Bootstrap (nur falls T78 besteht) |
