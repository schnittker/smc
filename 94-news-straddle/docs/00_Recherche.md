# Recherche: News-Straddle (Strategie Nr. 94) am Beispiel NFP

Stand: 24.10.2026

## 1. Idee

Vor einer Datenveröffentlichung mit großer Kursreaktion werden ein Buy-Stop über und ein Sell-Stop unter dem Kurs platziert (One-Cancels-Other). Die Richtung der Überraschung muss nicht bekannt sein, die Bewegung trägt die Position. Kandidat mit der stärksten regelmäßigen Reaktion: der US-Arbeitsmarktbericht (Nonfarm Payrolls, NFP) um 08:30 New York.

## 2. Probleme (Grund für ⚠ in der Liste)

- **Spread-Ausweitung** zur Veröffentlichung: bei FTMO typisch das 3- bis 10-fache
- **Slippage:** Stop-Orders werden in Kurslücken gefüllt, oft weit hinter dem Level
- **Whipsaw:** erster Ausschlag in die eine Richtung, dann Umkehr. Beide Seiten können ausgelöst werden.
- HistData-M1-Kurse sind Bid-Kurse ohne Spread-Historie.

Die Kosten werden deshalb bewusst pessimistisch angesetzt (5-facher Spread, 0,03 % Slippage je Ausführung in den ersten Minuten). Ein positives Ergebnis wäre trotzdem nur ein Hinweis, kein Beleg.

## 3. Termine

Es gibt keinen Kalender-Export (vgl. Nr. 25). Die Termine werden daher aus der BLS-Regel berechnet: Veröffentlichung am dritten Freitag nach dem Ende der Referenzwoche (Sonntag–Samstag mit dem 12. des Monats).
- Fällt der Freitag auf einen Bundesfeiertag, wird im Januar eine Woche später veröffentlicht (z. B. 08.01.2016, 08.01.2021).
- Im Juli wird am Donnerstag davor veröffentlicht (z. B. 02.07.2015, 02.07.2020).

## 4. Quellen

| Quelle | Inhalt |
|---|---|
| Andersen, Bollerslev, Diebold & Vega (2003), *AER* | Sprunghafte FX-Reaktion auf US-Makrodaten, vor allem NFP, binnen Minuten |
| Evans & Lyons (2008) | Orderflow nach Veröffentlichungen |
| Praxis | Straddles scheitern oft an Spread und Slippage |

## 5. Einschätzung vor dem Test

**Erwartung: Scheitern.**
