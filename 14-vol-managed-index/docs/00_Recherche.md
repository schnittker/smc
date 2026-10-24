# Recherche: Volatilitätsgesteuertes Index-Long

Stand: 24.10.2026

## 1. Idee

Hohe Volatilität ist kurzfristig gut vorhersagbar, die erwartete Rendite steigt aber nicht im selben Maß mit. Ein Index-Long, dessen Größe umgekehrt zur jüngsten Volatilität skaliert wird, erreicht dadurch eine höhere Sharpe Ratio als ein konstantes Long. Die Position ist klein in Krisen und groß in ruhigen Phasen.

## 2. Evidenz

| Studie | Ergebnis |
|---|---|
| **Moreira & Muir (2017, *Journal of Finance*)**, „Volatility-Managed Portfolios“ | Gewicht ∝ 1 / Varianz des Vormonats, monatlich umgeschichtet: höheres Alpha und höhere Sharpe Ratio für den US-Markt und viele Faktoren (1926–2015) |
| Cederburg, O'Doherty, Wang & Yan (2020, *Journal of Financial Economics*), „On the performance of volatility-managed portfolios“ | Out-of-Sample und mit realistischen Kosten bringt die Steuerung über viele Faktoren **keinen systematischen Vorteil** gegenüber dem ungesteuerten Portfolio |
| Harvey et al. (2018), „The impact of volatility targeting“ | Volatilitäts-Targeting bei Aktien verbessert die Sharpe Ratio leicht und vermindert vor allem extreme Verluste |

## 3. Bezug zu FTMO

- Kern der Rendite ist die Aktienprämie. Die Steuerung soll vor allem die Verluste in Krisen begrenzen (2020, 2022), und genau die bedrohen die 5-%- und 10-%-Grenzen.
- **Kosten:** Der Index-CFD-Swap (Dividende − USD-Zins − 2,5 % Aufschlag) kostet 2022–2023 etwa 6 % p. a. auf den gehaltenen Nominalwert. Bei großem Hebel in ruhigen Phasen wiegt das schwer.
- **Schwelle t ≥ 3 über 9 Jahre** entspricht einer Sharpe Ratio von etwa 1,0. Der S&P 500 hatte 2015–2023 eine Sharpe Ratio um 0,6–0,7 vor Finanzierungskosten.

## 4. Einschätzung vor dem Test

- **Erwartung: Scheitern am t-Kriterium** (Sharpe Ratio netto um 0,4–0,6).
- Der Test liefert zugleich die Referenz „Index halten“ für alle folgenden Index-Strategien.
