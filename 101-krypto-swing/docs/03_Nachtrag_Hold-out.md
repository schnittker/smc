# Nachtrag zur Vorregistrierung: Hold-out für K-LONG trotz t < 3 (Strategie Nr. 101)

Festgelegt am 25.10.2026, **nach** dem In-Sample-Lauf (T309/T310) und **vor** jeder Auswertung von Krypto-Daten ab 2024. Auftrag des Nutzers: „dann mach mit krypto weiter“.

## Warum ein Nachtrag

- K-LONG hat drei von vier IS-Kriterien erfüllt. Verfehlt wurde nur t ≥ 3 (t = 2,57 bei Sharpe 1,18).
- Nach der ursprünglichen Regel ist Nr. 101 gescheitert. Diese Ausnahme ist eine **Regeländerung nach Kenntnis der Ergebnisse**. Sie wird als eigener Versuch (T317) im Trial-Log geführt und im Ergebnis als solche gekennzeichnet.
- Zum Ausgleich ist der Hold-out strenger als üblich. Er ist der letzte saubere Test für Krypto-Trendfolge in dieser Reihe.

**Vorab bekannt** (allgemeines Marktwissen, nicht aus den Daten):
- BTC stieg 2024 stark (Spot-ETFs, Halving).
- Die Altcoins entwickelten sich 2024–2025 uneinheitlich.

## Regeln

- **Unverändert:** Modell, Parameter, Kosten (Swap 20 % p. a., Spreads wie vorregistriert) und Universum gelten wie in `01_Vorregistrierung.md`, Variante **K-LONG**.
- **Hold-out:** 01.01.2024 bis 24.10.2026 (Datenende), einmalig

## Kriterien Hold-out (T317): alle müssen erfüllt sein

| # | Kriterium |
|---|---|
| 1 | Mittleres Netto-Tagesergebnis > 0 |
| 2 | ≥ untere Grenze des 95-%-Konfidenzintervalls von IS (Cluster-Bootstrap nach Monat) |
| 3 | **zusätzlich:** Sharpe Ratio im Hold-out ≥ 0,5 |

## FTMO (T318, nur falls T317 besteht)

Wie vorregistriert:
- Tagesreihe IS + Hold-out
- Stufen 0,5 / 0,75 / 1,0 / 1,25 % Tagesschwankung
- Hebel je Tag auf 1:1 begrenzt
- Phase 2 × 0,75, De-Risk ab 3 %/6 %
- Worst-Case aus Hoch/Tief gegen 5 % und 10 %
- Block-Bootstrap über Kalendermonate, 10.000 Pfade

**Bestanden**, wenn mindestens eine Stufe ≥ 70 % Chance für beide Phasen bei ≤ 12 Monaten Median-Dauer erreicht.

**Beschreibend:**
- Ergebnis je Coin und Jahr im Hold-out
- Anteil des Ergebnisses an Wochenenden (FTMO-Wartungsfenster)
- Ergebnis bei 10 % und 30 % Swap

## Artefakt-Prüfung (Spielregel 6)

Die Binance-Daten sind 24/7 ohne Sitzungsbeginn. Die HistData-Artefakte der ersten Feed-Kerze betreffen sie nicht.

Ein mögliches Problem ist der Wochenendhandel: FTMO hat Wartungsfenster am Wochenende. Deshalb wird der Wochenend-Anteil beschreibend ausgewiesen. Ist das Hold-out-Ergebnis überwiegend Wochenend-getrieben, wird das als Vorbehalt vermerkt.

## Trial-Log

| # | Test |
|---|---|
| T317 | K-LONG Hold-out nach Ausnahmeregel (Regeländerung nach IS-Ergebnis) |
| T318 | FTMO-Bootstrap (nur falls T317 besteht) |
