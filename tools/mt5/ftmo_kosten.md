# Echte FTMO-Handelskosten (Export vom 25.10.2026, FTMO-Demo, Swing-relevant)

Quelle: `tools/mt5/ExportFtmoData.mq5`, ausgewertet mit `tools/mt5/analyse_export.py`. Spread relativ zum Kurs; Swap in % des Nominals pro Jahr (365 Belastungen: Mo–Do einfach, ein Tag dreifach). Negativ = Belastung.

## Spreads aus Ticks (letzte 30 Tage, Bid/Ask)

| Symbol | Ticks | Median | zeitgewichtet Ø | 90 %-Quantil |
|---|---|---|---|---|
| BTCUSD | 8,508,525 | 0.0012% | 0.0014% | 0.0025% |
| ETHUSD | 1,682,343 | 0.0245% | 0.0237% | 0.0268% |
| EURUSD | 1,404,334 | 0.0009% | 0.0023% | 0.0027% |
| US500.cash | 1,767,731 | 0.0078% | 0.0078% | 0.0078% |
| XAUUSD | 5,016,486 | 0.0099% | 0.0100% | 0.0111% |

## Spreads aus der Bar-Historie und Swaps

Bar-Spread = Median des Spread-Felds der H1-Bars im letzten Jahr (MT5 speichert je Bar den kleinsten Spread, daher eher eine Untergrenze; Vergleich mit den Ticks oben).

| Symbol | Gruppe | Historie ab | Spread H1 (Median, 12 M.) | Swap long p. a. | Swap short p. a. | Swap-Art | 3-fach |
|---|---|---|---|---|---|---|---|
| EURUSD | Forex | 2014-01 | 0.0009% | -2.79% | +0.07% | Punkte | Mi |
| GBPUSD | Forex | 2014-01 | 0.0023% | -1.47% | -1.30% | Punkte | Mi |
| USDJPY | Forex | 2014-01 | 0.0025% | +0.40% | -4.42% | Punkte | Mi |
| AUDUSD | Forex | 2014-01 | 0.0029% | -1.41% | -3.62% | Punkte | Mi |
| NZDUSD | Forex | 2014-01 | 0.0085% | -2.98% | +0.03% | Punkte | Mi |
| USDCAD | Forex | 2014-01 | 0.0022% | +0.17% | -3.05% | Punkte | Mi |
| USDCHF | Forex | 2014-01 | 0.0038% | +0.58% | -5.97% | Punkte | Mi |
| EURJPY | Forex | 2014-01 | 0.0060% | +0.43% | -2.50% | Punkte | Mi |
| GBPJPY | Forex | 2014-01 | 0.0074% | +0.91% | -4.12% | Punkte | Mi |
| EURCHF | Forex | 2014-01 | 0.0066% | +0.56% | -5.21% | Punkte | Mi |
| US500.cash | Cash CFD | 2017-12 | 0.0077% | -8.71% | -0.02% | Punkte | Fr |
| US100.cash | Cash CFD | 2017-12 | 0.0052% | -8.72% | +0.04% | Punkte | Fr |
| US30.cash | Cash CFD | 2019-02 | 0.0041% | -6.82% | -1.98% | Punkte | Fr |
| GER40.cash | Cash CFD | 2017-12 | 0.0058% | -7.26% | -0.73% | Punkte | Fr |
| FRA40.cash | Cash II CFD | 2017-12 | 0.0197% | -7.24% | -0.73% | Punkte | Fr |
| UK100.cash | Cash CFD | 2017-12 | 0.0126% | -8.94% | +0.23% | Punkte | Fr |
| JP225.cash | Cash II CFD | 2017-12 | 0.0147% | -5.58% | -2.30% | Punkte | Fr |
| HK50.cash | Cash II CFD | 2018-12 | 0.0238% | -7.48% | -0.33% | Punkte | Fr |
| AUS200.cash | Cash II CFD | 2019-02 | 0.0114% | -10.09% | +0.48% | Punkte | Fr |
| XAUUSD | Metals CFD | 2014-01 | 0.0086% | -5.29% | -0.38% | Punkte | Mi |
| XAGUSD | Metals CFD | 2014-01 | 0.0660% | -8.98% | -0.09% | Punkte | Mi |
| USOIL.cash | Cash II CFD | 2020-12 | 0.0736% | +3.12% | -18.54% | Punkte | Fr |
| UKOIL.cash | Cash II CFD | 2016-04 | 0.0620% | +18.78% | -86.44% | Punkte | Fr |
| NATGAS.cash | Commodities | 2024-10 | 1.8962% | -234.04% | +52.72% | Punkte | Fr |
| BTCUSD | Crypto I CFD | 2014-01 | 0.0013% | -30.00% | -30.00% | Zins | Fr |
| ETHUSD | Crypto I CFD | 2016-05 | 0.0259% | -30.00% | -30.00% | Zins | Fr |
| LTCUSD | Crypto I CFD | 2014-01 | 0.2718% | -30.00% | -30.00% | Zins | Fr |
| XRPUSD | Crypto I CFD | 2016-05 | 0.1068% | -30.00% | -30.00% | Zins | Fr |
| ADAUSD | Crypto I CFD | 2021-09 | 0.1193% | -30.00% | -30.00% | Zins | Fr |
| SOLUSD | Crypto I CFD | 2025-04 | 0.0320% | -30.00% | -30.00% | Zins | Fr |
| DOGEUSD | Crypto II CFD | 2021-09 | 0.0950% | -30.00% | -30.00% | Zins | Fr |
| AAPL | Equities I CFD | 2014-01 | 0.0358% | -8.28% | -6.55% | Punkte | Fr |
| MSFT | Equities I CFD | 2014-01 | 0.0235% | -8.52% | -6.74% | Punkte | Fr |
| NVDA | Equities I CFD | 2020-11 | 0.0507% | -8.79% | -6.96% | Punkte | Fr |
| TSLA | Equities I CFD | 2019-03 | 0.0257% | -8.68% | -6.86% | Punkte | Fr |

## Einordnung

- **Spreads:** Sie sind bei FTMO deutlich niedriger als in meinen Annahmen.
  - BTC 0,0013 % statt 0,05 %, ETH 0,025 % statt 0,08 %
  - FX-Majors etwa 0,1 Pip Rohspread, plus Kommission
  - US500 0,5 Punkte, wie im Kostenmodell H
  - Nur LTC (0,27 %), Silber und Öl sind teurer.
  - Die Spreads sind über den Tag sehr stabil. Nur bei EURUSD ist er zum Rollover (00 Uhr UTC) etwa 30-fach.
- **Swaps:** Sie sind höher als angenommen.
  - Krypto: −30 % p. a. long und short (angenommen 20 %)
  - Index-Longs: −7 bis −10 % p. a. (Modell H rechnete ca. −5 bis −7 %)
  - Aktien-CFDs: −8 % long und −7 % short
  - Öl: Swap stark richtungsabhängig (UKOIL short −86 % p. a.)
- **Kommission:** Sie ist nicht im Export enthalten, weil auf dem Demo-Konto keine Deals lagen. Für eine Klärung genügt je ein 0,01-Lot-Trade in EURUSD, BTCUSD, US500.cash und AAPL, danach Export erneut starten.
- **Für Swing-Strategien ist der Swap der entscheidende Kostenblock**, nicht der Spread.

## Nachrechnung Krypto-Trendfolge Nr. 101 mit echten Kosten (beschreibend, kein neuer Test)

Spreads aus den Ticks bzw. der H1-Historie, Swap 30 % p. a., Kommission weiter angenommen 0,0325 % je Seite.

| Variante | Zeitraum | vorregistrierte Kosten | echte FTMO-Kosten (Handel / Swap je Tag) | echte, ohne Kommission |
|---|---|---|---|---|
| K-LONG | IS 2018–23 | +7,93 bp, Sharpe 1,18 | +7,54 bp, Sharpe 1,12 (0,68 / 1,75 bp) | +7,75 bp, 1,16 |
| K-LONG | HO 2024–26 | +2,93 bp, Sharpe 0,48 | +2,50 bp, Sharpe 0,41 (0,93 / 2,04 bp) | +2,78 bp, 0,46 |
| K-TSM | IS 2018–23 | +7,31 bp, Sharpe 0,80 | +6,58 bp, Sharpe 0,72 | +7,02 bp, 0,77 |
| K-TSM | HO 2024–26 | +0,14 bp, Sharpe 0,02 | −0,76 bp, Sharpe −0,08 | −0,15 bp, −0,02 |

**Ergebnis:** Mit den echten FTMO-Kosten fällt Krypto-Trendfolge leicht schlechter aus. Der höhere Swap wiegt die niedrigeren Spreads mehr als auf. Die Entscheidung „gescheitert“ wird bestätigt.

**Daten:** Der vollständige Export (166 Symbole D1/H1 ab 2014 bzw. Listung, Spread je Bar, 30 Tage Ticks für 5 Symbole) liegt unter `ftmo-data/export_2026-10-25/` (nicht im Repo).
