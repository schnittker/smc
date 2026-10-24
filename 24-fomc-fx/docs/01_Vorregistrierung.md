# Vorregistrierung: Modell F „USD an FOMC-Tagen“ (Strategie Nr. 24)

Festgelegt am 24.10.2026, **bevor** Code für dieses Modell geschrieben oder Daten dafür ausgewertet wurden. Änderungen nach diesem Commit zählen als neuer Versuch im Trial-Log (`../TRIAL_LOG.md`).

**Vorab festgehalten:** Die FOMC-Termine stammen aus Nr. 9 (`../09-pre-fomc-drift/research/fomc_dates.csv`). Dort wurde US500 an diesen Terminen ausgewertet (+19 bp, t 2,4), nicht aber Wechselkurse.

## 0. Feste Rahmenbedingungen (für alle Strategien gleich)

- Expert Advisor für MetaTrader 5, handelt vollständig autonom
- FTMO 2-Step, Swing, 100.000 USD
- Max. Verlust gesamt 10 %, max. Tagesverlust 5 %
- Ziel Phase 1 +10 %, Ziel Phase 2 +5 %
- News-Trading und Halten übers Wochenende erlaubt

## 1. Hypothese

Short USD gegen andere Hauptwährungen über den FX-Tag eines planmäßigen FOMC-Entscheids verdient nach Kosten mit t ≥ 3 (Mueller, Tahbaz-Salehi & Vedolin 2017).

**Erwartung vor dem Test: Scheitern am t-Kriterium.**

## 2. Daten und Zeiträume

- FOMC-Entscheidungstage 2015–2023 (71) bzw. ab 2024 (Hold-out), aus Nr. 9
- HistData M5 der 7 USD-Paare; Tagesbuchhaltung von Modell G über `run_weights` (Nr. 6), 16:50 New York, FX-Kosten, Swaps (Zinsdifferenz − 1 %), 0,7-%-Gebühr
- FRED-Zinsen (Vormonat) für die Auswahl in F-CARRY
- **In-Sample:** Entscheidungstage 2015–2023. **Hold-out:** ab 2024, einmalig und nur, wenn IS besteht.

## 3. Regeln

**Fenster je Termin t:** Einstieg 16:50 New York am Werktag vor t, Ausstieg 16:50 New York an t. Die Entscheidung um 14:00 liegt im Fenster. Ein Rollover (am Vortag; mittwochs dreifach).

**Varianten (je ein Trial)**

| Variante | Positionen |
|---|---|
| **F-USD** | Short USD gegen alle 7 (Long EURUSD, GBPUSD, AUDUSD, NZDUSD; Short USDJPY, USDCAD, USDCHF) |
| **F-CARRY** | Short USD nur gegen die 3 Währungen mit dem höchsten Zins (Vormonat) über dem USD-Zins; liegen weniger als 3 über dem USD-Zins, nur gegen diese |

- Größe je Paar `10 % / σ` (EWMA wie Modell G)
- Fehlt einem Paar die exakte 16:50-Kerze an Ein- oder Ausstiegstag, entfällt das Paar für diesen Termin.

**Bewertungseinheit:** Netto-Ergebnis je Termin in Kapitalanteilen (Summe über die Paare).

## 4. Akzeptanzkriterien

**In-Sample, je Variante** (alle müssen erfüllt sein)

| # | Kriterium |
|---|---|
| 1 | Mittleres Netto-Ergebnis je Termin > 0 mit t-Wert ≥ **3,0** (kleinster aus iid und Clustern nach Quartal) |
| 2 | ≥ 6 von 9 Jahren positiv |
| 3 | Beide Teilzeiträume 2015–2019 und 2020–2023 mit positivem Netto-Mittel |
| 4 | Mittleres Ergebnis bei doppelten Kosten > 0 |

**Variantenwahl:** höherer t-Wert. Besteht keine, ist **Strategie Nr. 24 gescheitert**, und der Hold-out bleibt unberührt.

**Beschreibend:** dasselbe Fenster an allen übrigen Tagen (Short USD als Vergleich); Ergebnis je Paar; Ergebnis je Jahr.

**Hold-out und FTMO:** wie Nr. 9.

## 5. Umsetzbarkeit als MT5-EA

FOMC-Termine über den MT5-Wirtschaftskalender, Zinsvergleich über die Swap-Sätze (wie Nr. 6), Orders um 16:50 New York. Es werden keine externen Daten benötigt.

## 6. Trial-Log (Fortsetzung des globalen Logs)

| # | Test |
|---|---|
| T84 | F-USD, In-Sample |
| T85 | F-CARRY, In-Sample |
| T86 | Hold-out der gewählten Variante (nur falls T84 oder T85 besteht) |
| T87 | FTMO-Bootstrap (nur falls T86 besteht) |
