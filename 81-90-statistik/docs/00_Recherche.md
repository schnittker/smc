# Recherche: Statistische Modelle (Nr. 81 HMM, 82 GARCH, 85 k-NN, 90 Gold-Saisonalität)

Stand: 24.10.2026

## 1. Idee

| Nr. | Modell | Einsatz |
|---|---|---|
| 81 | 2-Zustands-Gauss-HMM auf Tagesrenditen | Regime „ruhig“ → Trendfolge, „unruhig“ → flat |
| 82 | GARCH(1,1) | Volatilitätsprognose für die Positionsgröße einer Trendregel (statt EWMA) |
| 85 | k-Nächste-Nachbarn | Ähnliche 10-Tage-Renditemuster der Vergangenheit sagen den nächsten Tag voraus |
| 90 | Gold-Saisonalität | Long Gold im September und November (Baur 2013) |

## 2. Quellen

| Quelle | Inhalt |
|---|---|
| Hamilton (1989); Ang & Bekaert (2002) | Regime-Switching-Modelle; Regime vor allem in der Volatilität erkennbar |
| Bollerslev (1986); Moreira & Muir (2017) | GARCH; volatilitätsgesteuerte Portfolios |
| Fernández-Rodríguez et al. (2000); Cover & Hart (1967) | Nicht-parametrische Nearest-Neighbour-Prognosen in FX, kleine Effekte vor Kosten |
| Baur (2013), *Journal of Applied Economics* | Gold steigt saisonal im September und November |

## 3. Bezug zu früheren Tests

- Zeitreihen-Momentum (Nr. 3, 4) und Kanal-Trend (Nr. 28, 30) sind gescheitert, ebenso Vol-gesteuertes Index-Long (Nr. 14) und Hurst-Regime (Nr. 40).
- HMM und GARCH ändern nur Filter bzw. Größe einer schwachen Grundregel.

## 4. Einschätzung vor dem Test

**Erwartung: Scheitern aller vier.** Bei ST-GOLD sind 18 Monatsereignisse zu wenig für t ≥ 3.
