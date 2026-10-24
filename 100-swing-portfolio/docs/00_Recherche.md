# Recherche: Swing-Portfolio (Strategie Nr. 100, Ensemble)

Stand 24.10.2026, nach 131 Versuchen (Nr. 1–99, 0 bestanden).

## Ausgangslage

Keine Einzelstrategie hat t ≥ 3 erreicht. Über 9 Jahre entspricht das Kriterium einer Sharpe Ratio von mindestens etwa 1. Einige Swing-Modelle lagen mit einer Sharpe von 0,5–0,9 in einem Bereich, der für FTMO schon brauchbar wäre: Nach dem Brownschen Modell (±10 %, 10 % Vola) liegt die Bestehenschance bei Sharpe 0,5 bei etwa 73 %.

Der Nutzer will ausschließlich Swing-Trades: autonomer EA, Haltedauer über Nacht bis mehrere Tage, alle FTMO-Instrumente. Naheliegend ist deshalb, die nicht korrelierten Beinahe-Kandidaten zu bündeln. Unabhängige Ertragsquellen mit je Sharpe s ergeben zusammen etwa s·√n.

## Bausteine (Regeln unverändert aus der jeweiligen Vorregistrierung)

| Baustein | Nr. | Regel | IS 2015–2023 netto | Sharpe | t |
|---|---|---|---|---|---|
| P-SPX | 9 | Long US500 von 14:00 NY am Vortag bis 13:55 am FOMC-Entscheidungstag, Stop 3 ATR(D1), 1× Nominal | +19,2 bp/Termin (σ 60) | 0,87 | 2,38 |
| T-FRÜH | 10 | Long US500 vom Schluss (15:55 NY) des Handelstags −5 bis +2 um den Monatswechsel, Stop 3 ATR, 1× Nominal | +36,4 bp/Ereignis (σ 213) | 0,56 | 1,68 |
| V-VOL | 14 | US500 täglich long mit Gewicht min(0,15/σ21, 3), Umschichtung 16:50 NY | – | 0,56 | 1,68 |
| F-CARRY | 24 | An FOMC-Tagen Short USD gegen die 3 höchstverzinsten G10-Währungen, 16:50 Vortag bis 16:50, je Paar 10 %/σ | +54,6 bp/Termin (σ 197) | 0,70 | 2,11 |

Alle vier sind Swing-Positionen (über Nacht bzw. mehrere Tage) und brauchen nur Kurse und einen Kalender (FOMC-Termine, NYSE-Handelstage). Keiner der vier nutzt die erste Feed-Kerze einer Sitzung. Damit greift das Artefakt aus Spielregel 6 hier nicht.

**Nicht aufgenommen:**
- Die Zwillingsvarianten P-NDX und F-USD: dieselbe Quelle, also keine Diversifikation
- Modelle mit negativer Netto-Sharpe
- Krypto: keine Daten vorhanden (HistData führt kein BTC). Krypto-Swing ist ein eigener Folgekandidat.

## Warnung: Auswahlverzerrung

Die vier Bausteine sind die Besten aus rund 130 Versuchen. Ihre IS-Werte sind deshalb nach oben verzerrt. Das IS-Ergebnis des Portfolios ist nur **beschreibend**. Entscheidend ist der noch nie angefasste Hold-out 2024–2026, und er wird **für alle vier Bausteine gemeinsam verbraucht**. Ein späterer Einzel-Hold-out von Nr. 9, 10, 14 oder 24 ist danach nicht mehr möglich.

## Literatur

- Lucca/Moench (2015): Pre-FOMC-Drift
- Ariel (1987) und McConnell/Xu (2008): Turn-of-the-Month
- Moreira/Muir (2017): Volatility-Managed Portfolios
- Mueller/Tahbaz-Salehi/Vedolin (2017): Exchange Rates and Monetary Policy Uncertainty (FX an FOMC-Tagen)
- Risk Parity: Maillard/Roncalli/Teïletche (2010), hier vereinfacht als inverse Volatilität
