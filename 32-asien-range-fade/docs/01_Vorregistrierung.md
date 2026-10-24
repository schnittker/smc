# Vorregistrierung: Modell A „Asien-Range-Fade“ (Strategie Nr. 32)

Festgelegt am 24.10.2026, **bevor** Code für dieses Modell geschrieben oder Daten dafür ausgewertet wurden. Änderungen nach diesem Commit zählen als neuer Versuch im Trial-Log (`../TRIAL_LOG.md`).

**Vorab festgehalten:** EURCHF wurde in Nr. 21 auf Tagesbasis ausgewertet (z-Score, inklusive SNB-Schock). Intraday-Daten der Asien-Session wurden nicht angesehen.

## 0. Feste Rahmenbedingungen (für alle Strategien gleich)

- Expert Advisor für MetaTrader 5, handelt vollständig autonom
- FTMO 2-Step, Swing, 100.000 USD
- Max. Verlust gesamt 10 %, max. Tagesverlust 5 %
- Ziel Phase 1 +10 %, Ziel Phase 2 +5 %
- News-Trading und Halten übers Wochenende erlaubt

## 1. Hypothese

Fades von Bollinger-Band-Ausschlägen in der Asien-Session verdienen nach Kosten mit t ≥ 3.

**Erwartung vor dem Test: Scheitern an den Kosten.**

## 2. Daten und Zeiträume

- HistData M5 (Bid); FX-Kostenmodell des SMC-Projekts (Raw-Spread + 0,3 Pip, Kommission 5 USD/Lot, Slippage 0,1 Pip je Marktausführung)
- Londoner Zeit über `mer.events.london_utc` (Nr. 5); Handelstage Mo–Fr ohne 24.12.–01.01.
- **In-Sample:** 2015–2023. **Hold-out:** ab 2024, einmalig und nur, wenn IS besteht.

## 3. Regeln (Londoner Zeit, M5)

| Variante | Instrument |
|---|---|
| **A-EURCHF** | EURCHF |
| **A-AUDCAD** | AUDCAD |

- **Bänder:** SMA20 ± 2 Standardabweichungen der letzten 20 M5-Schlusskurse (Bid), einschließlich der aktuellen Kerze
- **Handelsfenster:** Signale aus Kerzen, die zwischen 00:00 und 05:55 schließen. Spätestens um 06:00 wird alles geschlossen.
- **Einstieg** zur Eröffnung der nächsten Kerze, wenn flat:
  - Schluss > oberes Band: Short
  - Schluss < unteres Band: Long
- **Ausstieg** zur Eröffnung der nächsten Kerze, sobald der Schluss die SMA20 erreicht (Long: Schluss ≥ SMA; Short: Schluss ≤ SMA), sonst um 06:00
- **Stop:** Abstand = Bandbreite (oberes − unteres Band) beim Signal, ab Einstieg; intrabar gegen Bid bzw. Ask; bei einem Gap zur Eröffnung
- **Größe:** Nominal = min(0,25 % Kapital / (Stopabstand / Kurs), 10 × Kapital)
- Mehrere Trades pro Nacht möglich, immer nur eine Position

**Bewertungseinheit:** Netto-Ergebnis je Nacht in Kapitalanteilen. Nächte ohne Trade zählen mit 0.

## 4. Akzeptanzkriterien

Wie Nr. 16 (alle müssen erfüllt sein): t ≥ **3,0** (kleinster aus iid, Woche, Monat) bei positivem Mittel; ≥ 6 von 9 Jahren positiv; beide Teilzeiträume positiv; doppelte Kosten > 0. Variantenwahl über den t-Wert. Besteht keine, ist **Strategie Nr. 32 gescheitert**, und der Hold-out bleibt unberührt.

**Beschreibend:** Trades, Trefferquote, Ø Ergebnis in R vor und nach Kosten, Anteil Stops.

**Hold-out und FTMO:** wie Nr. 16.

## 5. Umsetzbarkeit als MT5-EA

M5-Bollinger-Bänder im EA, Orders nur im Zeitfenster, Server-Stop. Es werden keine externen Daten benötigt.

## 6. Trial-Log (Fortsetzung des globalen Logs)

| # | Test |
|---|---|
| T110 | A-EURCHF, In-Sample |
| T111 | A-AUDCAD, In-Sample |
| T112 | Hold-out der gewählten Variante (nur falls T110 oder T111 besteht) |
| T113 | FTMO-Bootstrap (nur falls T112 besteht) |
