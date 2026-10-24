# Recherche: COT-Positionierung (Commitments of Traders)

Stand: 24.10.2026

## 1. Idee

Die US-Aufsicht CFTC veröffentlicht jeden Freitag (15:30 New York) die Positionen großer Händler an den Terminbörsen, Stand Dienstag. Für Währungs- und Goldfutures gibt es die Netto-Position der „Non-Commercials“ (Spekulanten: Fonds, CTAs) und der „Commercials“ (Hedger).

- **Praktiker-Regel (konträr):** Extreme Spekulanten-Positionen zeigen einen überfüllten Trade an, also Umkehr.
- **Gegenthese (Fortsetzung):** Spekulanten sind informiert, Extreme kündigen eine weitere Bewegung in ihre Richtung an.

## 2. Evidenz

| Studie | Ergebnis |
|---|---|
| **Tornell & Yuan (2012, *Journal of Futures Markets* 32(2), 122–151)**, „Speculation and hedging in the currency futures markets: Are they informative to the spot exchange rates“ | GBP, EUR, JPY, MXN: **Hoch- und Tiefpunkte** der Netto-Positionen sagen den Kassakurs über 1–20 Wochen voraus. **Spekulanten-Positionen sagen Fortsetzung voraus, Hedger-Positionen Umkehr.** Beim GBP folgen auf Spekulanten-Hochpunkte im Mittel +0,23 % (Woche), +0,76 % (Monat), +2,31 % (Quartal). |
| Klitgaard & Weir (2004), „Exchange rate changes and net positions of speculators in the futures market“ | Wochenänderungen der Spekulanten-Positionen laufen *gleichzeitig* mit dem Wechselkurs, sagen ihn aber kaum voraus |
| Reserve Bank of New Zealand (2018), „Reassessing the information content of the Commitments of Traders positioning data“ | Positionierungsdaten helfen bei der Deutung, als Prognose für Wechselkurse aber nur begrenzt nützlich |

Quellen: https://www.researchgate.net/publication/227643703_Speculation_and_hedging_in_the_currency_futures_markets_Are_they_informative_to_the_spot_exchange_rates, https://ideas.repec.org/p/nzb/nzbans/2018-03.html

## 3. Folgerung für den Test

- Die Literatur spricht eher für **Fortsetzung**, die Praxis für **Umkehr**. Beide Richtungen werden auf demselben Signal getestet (zwei Trials, Mehrfachtest offen ausgewiesen).
- **Signal:** COT-Index über 3 Jahre (Lage der Netto-Position zwischen Minimum und Maximum der letzten 156 Wochen). Extreme bei ≥ 0,9 bzw. ≤ 0,1.

## 4. Was dagegen spricht

1. Die Daten sind bei Veröffentlichung 3 Tage alt, bei Ausführung am Montag 6 Tage.
2. Wenige unabhängige Signale: Extreme halten oft wochenlang an.
3. **Für den EA** müssen die COT-Daten live über `WebRequest` von der CFTC geladen werden (⚠ externe Datenquelle).

## 5. Einschätzung vor dem Test

**Erwartung: Scheitern beider Varianten** (t < 3). Ein Effekt wäre am ehesten bei C-FOLGE zu erwarten.
