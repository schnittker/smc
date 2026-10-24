# Recherche: Intraday-Momentum am Aktienindex

Stand: 24.10.2026

## 1. Effekt

Die Rendite des Index vom Vortagsschluss bis 10:00 New York (Overnight plus erste halbe Stunde) sagt die Richtung der letzten halben Stunde (15:30–16:00) voraus. Dasselbe gilt für die Rendite des übrigen Tages bis 15:30.

## 2. Evidenz

| Studie | Ergebnis |
|---|---|
| Gao, Han, Li & Zhou (2018, *Journal of Financial Economics*), „Market intraday momentum“ | SPY 1993–2013: erste halbe Stunde (inkl. Overnight) sagt die letzte halbe Stunde voraus; Timing-Strategie mit positiver Rendite und Sharpe Ratio um 1 vor Kosten; stärker an volatilen Tagen und bei Nachrichten |
| **Baltussen, Da, Lammers & Martens (2021, *Journal of Financial Economics*)**, „Hedging demand and market intraday momentum“ | Über 60 Futures (Aktien, Anleihen, Rohstoffe, Währungen), 1974–2020: Intraday-Momentum **„strong … everywhere“**. Sowohl Overnight plus erste halbe Stunde als auch die Tagesmitte sagen voraus. Ursache: Gamma-Hedging von Händlern mit Short-Gamma-Position und Rebalancing gehebelter ETFs, gebündelt in der liquiden letzten halben Stunde. |
| Baltussen, Da & Soebhag, „End-of-Day Reversal“ | Bei Einzelaktien im Querschnitt dagegen Umkehr in den letzten 30 Minuten (Gegenbefund, betrifft nicht den Index) |

Quellen: https://www.sciencedirect.com/science/article/abs/pii/S0304405X21001598, https://www.researchgate.net/publication/351315710_Hedging_demand_and_market_intraday_momentum

## 3. Was dagegen spricht

1. **Kosten gegen Effekt:** Die letzte halbe Stunde bewegt US500 typisch um 15–25 bp. Bei einer Vorhersagegüte von R² ≈ 1–2 % ergibt das einen erwarteten Vorteil von etwa 2–3 bp je Trade. Die FTMO-Kosten liegen bei etwa 1,6 bp (Spread plus Slippage).
2. **CFD statt Future:** HistData-Kurse sind Bid-Kurse eines CFD. Zu den Zeitpunkten 10:00, 15:30 und 16:00 können sie leicht vom Kassaindex abweichen.
3. **Bekanntheit seit 2018:** Rebalancing-Flows am Schluss sind heute gut prognostiziert. Der Effekt hängt außerdem davon ab, wie die Händler bei Gamma positioniert sind, und das schwankt über die Zeit.

## 4. Einschätzung vor dem Test

- **Vorteil:** tägliche Signale, also rund 2.200 Beobachtungen im In-Sample. Ein echter Effekt kann t ≥ 3 erreichen.
- **Erwartung:** Effekt vor Kosten positiv, nach Kosten knapp. **Eher Scheitern.**
- **Für FTMO** wäre eine tägliche Strategie im Erfolgsfall deutlich besser geeignet als Nr. 5, 9 und 10.
