# Vorregistrierung: Modell LV „Intraday-Level“ (Strategien Nr. 48 und 49)

Festgelegt am 24.10.2026, **bevor** Code für dieses Modell geschrieben oder Daten dafür ausgewertet wurden. Änderungen nach diesem Commit zählen als neuer Versuch im Trial-Log (`../TRIAL_LOG.md`).

**Vorab festgehalten:** Die Kassasitzungen von US500, US100, FRA40 und UK100 wurden in Nr. 41 ausgewertet (Gap-Fade), Servertage der Majors und Indizes in Nr. 33–35 und 43/44. Value Areas und Pivot-Level wurden nicht angesehen.

## 0. Feste Rahmenbedingungen (für alle Strategien gleich)

- Expert Advisor für MetaTrader 5, handelt vollständig autonom
- FTMO 2-Step, Swing, 100.000 USD
- Max. Verlust gesamt 10 %, max. Tagesverlust 5 %
- Ziel Phase 1 +10 %, Ziel Phase 2 +5 %
- News-Trading und Halten übers Wochenende erlaubt

## 1. Hypothesen

- **Nr. 48 (LV-VA80):** Die 80-%-Regel verdient auf den Index-CFDs nach Kosten mit t ≥ 3.
- **Nr. 49:** Fades an S1/R1 zum Pivot (LV-PFADE) bzw. Ausbrüche über R3/S3 (LV-PBRK) verdienen nach Kosten mit t ≥ 3.

**Erwartung vor dem Test: Scheitern aller drei.**

## 2. Daten, Kosten, Zeiträume

- HistData M5, Bid-Kurse
- **LV-VA80:** US500, US100, FRA40, UK100. Kassasitzungen und Handelstage wie Nr. 41 (`gap.model.session`, `index_days`).
- **LV-PFADE, LV-PBRK:** EURUSD, GBPUSD, USDJPY, AUDUSD, NZDUSD, USDCAD, USDCHF, US500, US100, FRA40, UK100, JP225, HK50, AUS200. Servertage Mo–Fr wie Nr. 33–35 (`dbo.model.server_days`).
- **Kosten:** Kostenmodell wie Nr. 33–35. Marktorders zahlen Spread und Slippage, Limit-Einstiege und Limit-Ziele werden zum Level ohne Slippage ausgeführt. Kauf zum Ask, Verkauf zum Bid. Keine Swaps, weil alle Positionen vor dem Rollover bzw. Sitzungsende geschlossen werden.
- Kein Handel an Tagen 24.12.–01.01.
- **In-Sample:** 2015–2023. **Hold-out:** ab 2024, einmalig je bestandener Variante.

## 3. Regeln

**LV-VA80 (Nr. 48, je Index und Handelstag)**
1. **Profil der vorigen Kassasitzung:** 30-Minuten-Blöcke ab Sitzungsbeginn (Hoch/Tief aus M5). Jeder Block erhält ein TPO in jeder Preisstufe zwischen seinem Tief und Hoch. Stufe = 0,02 % des Schlusskurses der Vorsitzung.
2. **POC** = Stufe mit den meisten TPOs; bei Gleichstand die Stufe, die der Mitte der Spanne am nächsten liegt.
3. **Value Area:** Ausgehend vom POC wird schrittweise die benachbarte Stufe (oben oder unten) mit mehr TPOs hinzugenommen, bei Gleichstand die obere, bis ≥ 70 % aller TPOs erfasst sind. VAH und VAL sind die Grenzen.
4. **Bedingung:** Die heutige Kassa-Eröffnung O liegt über VAH oder unter VAL.
5. **Signal:** Zwei aufeinanderfolgende 30-Minuten-Blöcke der heutigen Sitzung schließen innerhalb [VAL, VAH], und der zweite endet spätestens 2 Stunden vor Sitzungsschluss.
6. **Einstieg** (Marktorder) zur Eröffnung des nächsten Blocks, in Richtung der Gegenseite. Eröffnung über VAH → Short mit Ziel VAL; Eröffnung unter VAL → Long mit Ziel VAH.
7. **Stop:** Short am höchsten Bid-Hoch, Long am tiefsten Bid-Tief seit Sitzungsbeginn; Abstand mindestens 0,1 % des Kurses.
8. **Ziel:** Limit an der Gegenseite der VA
9. **Zeitausstieg:** Marktorder zum Sitzungsschluss
10. Höchstens ein Trade je Index und Tag

**LV-PFADE / LV-PBRK (Nr. 49, je Instrument und Servertag i; Level aus Hoch H, Tief L und Schluss C des Servertags i−1)**
- P = (H + L + C) / 3; R1 = 2P − L; S1 = 2P − H; R2 = P + (H − L); S2 = P − (H − L); R3 = H + 2(P − L); S3 = L − 2(H − P)

| | LV-PFADE | LV-PBRK |
|---|---|---|
| Long-Order | Buy-Limit bei S1 (Ask ≤ S1; Gap darunter: Ausführung zur Eröffnung) | Buy-Stop bei R3 (Ask ≥ R3; Gap: Eröffnung) |
| Short-Order | Sell-Limit bei R1 (Bid ≥ R1) | Sell-Stop bei S3 (Bid ≤ S3) |
| Stop | S2 bzw. R2 | R2 bzw. S2 |
| Ziel (Limit) | P | keins |
| aktiv | vom Tagesbeginn bis 1 h vor Tagesende, One-Cancels-Other | wie links |
| Ausstieg | spätestens Schluss der letzten M5-Kerze des Servertags | wie links |

**Gemeinsam:**
- Einstieg und Stop in derselben M5-Kerze zählen als gestoppt, ebenso Stop und Ziel in derselben Kerze.
- **Größe:** Nominal = min(0,25 % Kapital / (R / Einstieg), 10 × Kapital), R = Abstand Einstieg–Stop
- **Portfolio:** Summe aller Instrumente je Tag; Tage ohne Trade zählen als 0

## 4. Akzeptanzkriterien

Wie Nr. 33–47 (alle müssen erfüllt sein): t ≥ **3,0** (kleinster aus iid, Woche, Monat) bei positivem Mittel; ≥ 6 von 9 Jahren positiv; ≥ 60 % der Instrumente positiv; doppelte Kosten > 0. Jede Variante wird für sich bewertet. Vor einem Hold-out gilt die Artefakt-Prüfung (Spielregel 6).

**Beschreibend:** Signale, Ausführungsquote, Ziel-, Stop- und Zeitausstiege, Ø R vor und nach Kosten, Ergebnis je Instrument.

**Hold-out und FTMO:** wie Nr. 16.

## 5. Umsetzbarkeit als MT5-EA

TPO-Profil bzw. Pivots aus den Kursen des Vortags; Pending- bzw. Marktorders mit festem Stop und Limit-Ziel; Schließen zur festen Uhrzeit. Es werden keine externen Daten benötigt.

## 6. Trial-Log (Fortsetzung des globalen Logs)

| # | Test |
|---|---|
| T165 | LV-VA80 (Nr. 48), In-Sample |
| T166 | LV-PFADE (Nr. 49), In-Sample |
| T167 | LV-PBRK (Nr. 49), In-Sample |
| T168–T173 | Hold-out und FTMO je bestandener Variante |
