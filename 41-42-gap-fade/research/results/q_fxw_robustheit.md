# Q-FXW: Robustheitsprüfungen (beschreibend, In-Sample 2015–2023)

Lauf vom 24.10.2026. Ändert weder Regeln noch Entscheidung (`docs/01_Vorregistrierung.md`); Zweck: Datenartefakte und Kostenempfindlichkeit vor dem einmaligen Hold-out erkennen.

## 1. Spread zur Montagseröffnung (Vielfaches des effektiven Spreads)

| Vielfaches | Trades | Netto bp/Montag | t | Ø R vor Kosten | Ø R netto | Füllquote |
|---|---|---|---|---|---|---|
| 1×  | 1,042 | +14.97 | +6.48 | +0.331 | +0.260 | 64% |
| 3× (vorregistriert) | 1,042 | +11.88 | +5.48 | +0.312 | +0.207 | 64% |
| 5×  | 1,042 | +9.20 | +4.49 | +0.295 | +0.160 | 64% |
| 8×  | 1,042 | +5.77 | +3.03 | +0.274 | +0.100 | 64% |
| 12×  | 1,042 | +2.01 | +1.14 | +0.251 | +0.035 | 64% |
| 20×  | 1,042 | -3.66 | -2.32 | +0.217 | -0.064 | 64% |

## 2. Einstiegszeit (Server-Montag; 01:00 = vorregistriert)

| Einstieg | Trades | Netto bp/Montag | t | Ø R vor Kosten | Ø R netto | Füllquote |
|---|---|---|---|---|---|---|
| 00:05 | 391 | +1.96 | +0.55 | +0.130 | +0.033 | 54% |
| 00:30 | 361 | -2.46 | -0.76 | +0.049 | -0.045 | 49% |
| 01:00 | 1,042 | +11.88 | +5.48 | +0.312 | +0.207 | 64% |
| 02:00 | 995 | -0.86 | -0.42 | +0.083 | -0.016 | 51% |
| 04:00 | 1,374 | -8.22 | -2.96 | -0.018 | -0.109 | 45% |
| 09:00 (London 07:00/08:00) | 1,885 | -10.09 | -3.79 | -0.018 | -0.097 | 40% |

## 3. Verteilung

| Kennzahl | Wert |
|---|---|
| Anteil der Summe aus den besten 5 % der Montage | 44% |
| Summe ohne die besten 5 % der Montage | +30.4 % (gesamt +53.8 %) |
| Median je Montag / Anteil positiver Montage | +13.68 bp / 54% |
| Long (Gap nach unten) Ø R netto / Trades | +0.301 / 689 |
| Short (Gap nach oben) Ø R netto / Trades | +0.022 / 353 |
| Ø \|Gap\| / Ø Stop-Abstand | 23.5 bp / 24.8 bp |

## 4. Datenqualität der Einstiegskerze (Server-Montag 01:00)

| Paar | Montage | Ø M1-Kerzen in der M5-Kerze | Anteil < 5 | Ø Spannweite der Kerze (bp) |
|---|---|---|---|---|
| EURUSD | 452 | 4.52 | 22% | 4.5 |
| GBPUSD | 414 | 4.37 | 28% | 4.7 |
| USDJPY | 430 | 4.51 | 27% | 4.9 |
| AUDUSD | 437 | 4.37 | 31% | 6.5 |
| NZDUSD | 415 | 4.03 | 44% | 6.7 |
| USDCAD | 411 | 4.07 | 41% | 4.0 |
| USDCHF | 391 | 4.26 | 34% | 5.9 |

## 5. Zerlegung nach Jahreszeit (erste Kerze der Woche im HistData-Feed)

Im Sommer (US-Sommerzeit) beginnt der HistData-Feed die Woche erst um 01:00 Server (17:00 EST fest = 18:00 EDT); im Winter um 00:00. Auf dem FTMO-Server beginnt der Handel ganzjährig um 00:00 Server.

| Teilmenge | Trades | Netto bp/Montag | t | Ø R vor Kosten | Ø R netto | Füllquote |
|---|---|---|---|---|---|---|
| Sommer, 01:00 = erste Kerze der Woche | 703 | +20.19 | +8.94 | +0.457 | +0.349 | 72% |
| Winter, 01:00 = 1 h nach Eröffnung | 339 | -5.08 | -1.37 | +0.009 | -0.089 | 48% |
| Sommer, Einstieg 02:00 = 1 h nach erster Kerze | 525 | +1.95 | +0.98 | +0.154 | +0.045 | 55% |
