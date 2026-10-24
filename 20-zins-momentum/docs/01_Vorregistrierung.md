# Vorregistrierung: Modell Z „Zins-Momentum G8“ (Strategie Nr. 20)

Festgelegt am 24.10.2026, **bevor** Code für dieses Modell geschrieben oder Daten dafür ausgewertet wurden. Änderungen nach diesem Commit zählen als neuer Versuch im Trial-Log (`../TRIAL_LOG.md`).

**Vorab festgehalten:** Dieselben 8 Währungen, Zinsreihen und Kurse wurden in Nr. 6 (Rangfolge nach Zinsniveau) und Nr. 7 (nach Kursrendite) ausgewertet. Die Rangfolge nach Zinsänderung wurde nicht angesehen.

## 0. Feste Rahmenbedingungen (für alle Strategien gleich)

- Expert Advisor für MetaTrader 5, handelt vollständig autonom
- FTMO 2-Step, Swing, 100.000 USD
- Max. Verlust gesamt 10 %, max. Tagesverlust 5 %
- Ziel Phase 1 +10 %, Ziel Phase 2 +5 %
- News-Trading und Halten übers Wochenende erlaubt

## 1. Hypothese

Long die drei Währungen mit dem stärksten Anstieg des Kurzfristzinses, Short die drei mit dem schwächsten, verdient nach Kosten mit t ≥ 3 (Proxy für die geldpolitische Seite von Dahlquist & Hasseltoft 2020; `docs/00_Recherche.md`).

**Erwartung vor dem Test: Scheitern.**

## 2. Daten und Zeiträume

Wie Nr. 6 und 7: FRED-Monatszinsen aus dem SMC-Swap-Modell, HistData M5 der 24 FX-Paare, Engine `carry.model` (Nr. 6), Warm-up 2014, In-Sample 2015–2023, Hold-out ab 2024 einmalig und nur, wenn IS besteht.

## 3. Regeln

Alles wie Modell K-3 (Nr. 6), **außer der Rangfolge**:

**Signal am ersten Handelstag von Monat m:** `Δ_c = r_c(m−1) − r_c(m−1−L)`, die Änderung des Monatsmittels des Kurzfristzinses der Währung c (USD eingeschlossen).

| Variante | L (Monate) |
|---|---|
| **Z-12** | 12 |
| **Z-3** | 3 |

- Rangfolge absteigend nach Δ, bei Gleichstand nach dem Zinsniveau `r_c(m−1)` (höher zuerst), dann alphabetisch.
- Carry-Positionen (1 / 8), (2 / 7), (3 / 6): Long die höchsten, Short die niedrigsten Δ, paarweise.
- Umsetzung (direkte Crosses oder zwei USD-Beine), Größe `10 % / σ` des Crosses, monatliche Umschichtung, Bewertung und Kosten (Spread, Slippage, Kommission, Swaps mit 1 % Aufschlag, 0,7-%-Gebühr) wie K-3.

## 4. Akzeptanzkriterien

Wie Nr. 6 (alle müssen erfüllt sein):

| # | Kriterium |
|---|---|
| 1 | Mittleres Netto-Tagesergebnis > 0 mit t-Wert ≥ **3,0** (kleinster aus iid, Woche, Monat) |
| 2 | ≥ 6 von 9 Jahren positiv |
| 3 | ≥ 60 % der gehandelten Instrumente (≥ 250 Positionstage) positiv |
| 4 | Mittleres Ergebnis bei doppelten Kosten > 0 |

**Variantenwahl:** höherer t-Wert. Besteht keine, ist **Strategie Nr. 20 gescheitert**, und der Hold-out bleibt unberührt.

**Beschreibend:** ohne Swap-Aufschlag; Teilzeiträume 2015–2019 und 2020–2023; Häufigkeit der Währungen auf Long- und Short-Seite; Korrelation mit K-3.

**Hold-out und FTMO:** wie Nr. 6.

## 5. Umsetzbarkeit als MT5-EA

Wie bei Nr. 6: Zinsdifferenzen aus den Swap-Sätzen der USD-Paare; der EA merkt sich die Werte der Vormonate. Es werden keine externen Daten benötigt.

## 6. Trial-Log (Fortsetzung des globalen Logs)

| # | Test |
|---|---|
| T68 | Z-12, In-Sample |
| T69 | Z-3, In-Sample |
| T70 | Hold-out der gewählten Variante (nur falls T68 oder T69 besteht) |
| T71 | FTMO-Bootstrap (nur falls T70 besteht) |
