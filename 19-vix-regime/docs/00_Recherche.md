# Recherche: VIX-Regime

Stand: 24.10.2026

## 1. Idee

In Stressphasen (hoher VIX) fliehen Anleger in sichere Häfen: JPY, CHF, Gold. Gleichzeitig sind Aktien nach starken Rückgängen oft „überverkauft“ und erholen sich.

## 2. Evidenz

| Studie | Ergebnis |
|---|---|
| Ranaldo & Söderlind (2010, *Review of Finance* 14, 385–407), „Safe Haven Currencies“ | CHF und JPY werten gegen USD auf, **während** US-Aktien fallen und die Volatilität steigt (1993–2008), über Stunden bis wenige Tage, verstärkt in Krisen. Das ist ein gleichzeitiger Zusammenhang, **keine Prognose**. |
| **Giot (2005, *Journal of Portfolio Management* 31(3), 92–100)**, „Relationships between implied volatility indexes and stock index returns“ | Sehr hohe VIX-Perzentile (VXO/VXN) gingen positiven künftigen Indexrenditen über bis zu 60 Tage voraus: „hoher VIX = Kaufgelegenheit“ |
| Banerjee, Doran & Peterson (2007, *Journal of Banking & Finance*), „Implied volatility and future portfolio returns“ (Autorenschaft nicht geprüft) | positiver Zusammenhang zwischen VIX und künftigen Renditen, passend zu einer negativen Volatilitätsrisikoprämie |

Quellen: https://doi.org/10.2139/ssrn.999382, https://www.sciencedirect.com/science/article/abs/pii/S0378426607000490

## 3. Daten

VIX-Tagesschlusskurse von Cboe (`VIX_History.csv`, https://cdn.cboe.com/api/global/us_indices/daily_prices/VIX_History.csv), Abruf 24.10.2026, 1990–23.10.2026. Der VIX-Schluss liegt um 16:15 New York vor.

## 4. Einschätzung vor dem Test

- **X-HAVEN** (sichere Häfen im Risk-off): schwach begründet, weil die Literatur nur gleichzeitige Bewegungen zeigt. **Erwartung: Scheitern.**
- **X-FEAR** (US500 im Risk-off): von Giot gestützt. Verwandt mit Nr. 15 (Rücksetzer kaufen), dort Sharpe 0,3. Das Regime ist hier aber über den VIX definiert, nicht über Kursmuster. Selten im Markt, daher geringe statistische Kraft. **Erwartung: Scheitern am t-Kriterium.**
- **Für den EA:** Der VIX ist bei FTMO nicht handelbar und nicht als Kurs verfügbar. Er müsste per `WebRequest` geladen werden (⚠).
