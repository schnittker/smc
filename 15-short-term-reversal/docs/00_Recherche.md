# Recherche: Kurzfrist-Reversal bei US-Indizes (Connors)

Stand: 24.10.2026

## 1. Idee

Im langfristigen Aufwärtstrend (Kurs über dem 200-Tage-Durchschnitt) erholen sich Indizes nach kurzen, scharfen Rücksetzern überdurchschnittlich. Gekauft wird der Rücksetzer, verkauft nach der Erholung, meist nach wenigen Tagen.

## 2. Evidenz

| Quelle | Ergebnis |
|---|---|
| Connors & Alvarez (2008), *Short Term Trading Strategies That Work* | **RSI(2)-Regel:** Kauf bei RSI(2) < 10 über SMA200, Ausstieg bei Schluss über SMA5. **Double 7s:** Kauf am 7-Tage-Schlusstief über SMA200, Ausstieg am 7-Tage-Schlusshoch. S&P 500 / SPY bis 2007: hohe Trefferquoten (70–80 %), positive Erwartung je Trade |
| Literatur zur Autokorrelation von Indexrenditen (z. B. Baltussen, van Bekkum & Da 2019, *JFE*, „Indexing and stock market serial dependence around the world“) | Seit den 2000ern sind tägliche Indexrenditen **negativ autokorreliert** (Mean Reversion). Erklärt wird das mit dem Wachstum von Indexfonds und ETFs. |
| Praxistests (Blogs, keine Peer-Review) | RSI(2) auf SPY bis in die 2020er positiv, aber mit kleineren Gewinnen und langen Seitwärtsphasen |

## 3. Was dagegen spricht

1. **Bekanntheit** seit 2008, sehr weit verbreitet.
2. **Wenig Zeit im Markt** (etwa 20–30 % der Tage). Die Strategie verdient nur einen Teil der Aktienprämie, und die Schwelle t ≥ 3 ist schwer zu erreichen.
3. **Kosten:** Je Trade fallen Spread und Slippage (etwa 1,6 bp) sowie einige Nächte Swap an. Das ist klein gegen typische Ziele von 50–100 bp je Trade.

## 4. Einschätzung vor dem Test

- **Erwartung:** positiv, Sharpe Ratio um 0,5–0,8, **eher Scheitern am t-Kriterium**.
- Wegen der negativen Autokorrelation ist das einer der wenigen Kandidaten, bei denen die Literatur einen *stärker gewordenen* Effekt nahelegt.
