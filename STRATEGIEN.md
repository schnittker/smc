# 100 Trading-Strategien – Testplan

Ziel: jeden Tag eine Strategie mit Claude testen, bis eine die FTMO-2-Step-Challenge (Swing, 100.000 USD) realistisch besteht.
Gleiche Pipeline wie in `smart-money-concept/`: Vorregistrierung → In-Sample 2015–2023 → Hold-out 2024–2026 nur einmal und nur, wenn IS besteht.

## Feste Rahmenbedingungen (für jede Strategie identisch)

| Punkt | Vorgabe |
|---|---|
| Umsetzung | Expert Advisor für **MetaTrader 5**, handelt **vollständig autonom** (kein manueller Eingriff) |
| Max. Drawdown gesamt | **10 %** vom Startkapital (harte Grenze, FtmoGuard im EA) |
| Max. Tagesverlust | **5 %** (inkl. offener Positionen, Tagesgrenze nach Serverzeit) |
| Ziel Phase 1 | **+10 %** |
| Ziel Phase 2 | **+5 %** |
| News-Trading | erlaubt |
| Weekend-Holding | erlaubt |
| Konto | FTMO 2-Step, Swing, 100.000 USD |

Folgen für die Auswahl:
- Jede Regel muss sich **in MQL5 umsetzen** lassen. ML-Modelle nur, wenn sie als ONNX in MT5 laufen.
- Externe Daten müssen **live im EA** verfügbar sein: Wirtschaftskalender (FOMC, EZB, NFP, CPI) liefert MT5 selbst (`CalendarValueHistory`); COT, FRED, VIX bräuchten `WebRequest` oder eine regelmäßig importierte Datei → ⚠.
- Bewertet wird nicht nur Sharpe, sondern die **Bestehenswahrscheinlichkeit** in der FTMO-Monte-Carlo (Ziel erreicht, bevor 5 % Tages- oder 10 % Gesamtverlust greifen).

**Reihenfolge = Priorität.** Oben stehen Strategien mit Evidenz aus der Forschung, unten Indikator-Setups mit geringem Prior und Strategien, die mit unseren Daten oder den FTMO-Regeln nicht sinnvoll testbar sind.

**Datenlage (wichtig für die Auswahl):**
- Vorhanden: HistData M1 (Bid) für 24 FX-Paare, Gold, Silber, Brent, US500, US100, FRA40, UK100, JP225, HK50, AUS200; Zinsen von FRED
- Kaputt/unvollständig: DAX, Euro Stoxx 50, WTI (siehe `docs/13`)
- **Kein echtes Volumen**, kein Orderbuch, kein Tickvolumen
- Frei nachladbar: CFTC-COT-Daten, FRED (VIX, Renditen, CPI), FOMC-/EZB-Termine, Wirtschaftskalender (mit Aufwand)

**Status:** ✗ gescheitert · ✓ bestanden · ⏳ in Arbeit · ⚠ nur eingeschränkt testbar · ⛔ nicht empfohlen / FTMO-Regeln · ⊘ durch einen früheren Test abgedeckt

---

## Bereits getestet (Tag 1)

| # | Strategie | Idee | Markt / TF | Status |
|---|---|---|---|---|
| 1 | Smart Money Concept (SMC/ICT) | Order Blocks, FVG, Liquidity Sweeps, MSS; Ereignisstudie + Modelle C/D | FX, Gold / M5–H4 | ✗ Tag 1 (P2–P4) |
| 2 | USD-Fix-Reversal | USD steigt vor den Fixings, fällt danach (Krohn et al. 2024) | EURUSD, GBPUSD, USDJPY / M5 | ✗ Tag 1 (P5) – Effekt ≈ Kosten |
| 3 | Zeitreihen-Momentum FX + Gold | Vorzeichen der 1/3/12-Monats-Rendite, vol-skaliert | 25 FX + Gold / D1 | ✗ Tag 1 (P6) |
| 4 | Zeitreihen-Momentum Indizes + Rohstoffe | wie #3 | 10 CFDs / D1 | ✗ Tag 1 (P7) |

## A – Evidenzbasiert (zuerst testen)

| # | Strategie | Idee | Markt / TF | Daten | Status |
|---|---|---|---|---|---|
| 5 | Monatsend-Rebalancing-Flows | Fonds sichern Währungsrisiko zum Monatsende ab: USD-Richtung aus Aktienperformance des Monats ableiten (Melvin & Prins 2015) | USD-Majors / H1 | vorhanden | ✗ Tag 2 (T19/T20): Effekt seit 2015 weg |
| 6 | FX Carry | Long hochverzinste, Short niedrigverzinste Währungen (Lustig & Verdelhan) – FTMO-Swap-Aufschläge prüfen | G10-FX / D1–W1 | FRED vorhanden ⚠ live per WebRequest | ✗ Tag 3 (T23/T24): Sharpe −0,16 / −0,02 |
| 7 | FX Querschnitts-Momentum | Monatlich Long die 3 stärksten, Short die 3 schwächsten Währungen (Menkhoff et al. 2012) | G10-FX / D1 | vorhanden | ✗ Tag 4 (T27/T28): Sharpe −0,28 / −0,81 |
| 8 | FX Value (Kaufkraftparität) | Long unterbewertete, Short überbewertete Währungen nach realem Wechselkurs. Achtung: nicht mehr unabhängig von der 12-Monats-Umkehr aus Nr. 7 | G10-FX / W1–MN | CPI von FRED ⚠ live per WebRequest | |
| 9 | Pre-FOMC-Drift | Long US500 in den 24 h vor FOMC-Entscheidungen (Lucca & Moench 2015) | US500 / H1 | MT5-Kalender | ✗ knapp, Tag 5 (T31/T32): +19 / +28 bp je Termin, t 2,4 / 2,3 – Ensemble-Kandidat |
| 10 | Turn-of-the-Month | Long Indizes vom letzten bis zum 3. Handelstag des Monats | Indizes / D1 | vorhanden | ✗ Tag 6 (T35/T36): +22 / +36 bp je Ereignis, t 1,2 / 1,7 |
| 11 | Intraday-Momentum | Rendite der ersten 30 min sagt die letzte 30 min voraus (Gao et al. 2018) | US500, US100 / M5 | vorhanden | ✗ Tag 7 (T39/T40): +0,4 / +1,0 bp/Tag, t 0,5 / 1,3; Effekt vor Kosten ≈ 2 bp |
| 12 | Overnight- vs. Intraday-Rendite | Indexrendite entsteht überwiegend über Nacht – nur Overnight halten | Indizes / H1 | vorhanden | ✗ Tag 8 (T43–T45): vor Kosten +0,6 bis +2,1 bp/Nacht ≈ Kosten |
| 13 | Tageszeit-Effekt FX | Währungen werten während der eigenen Handelszeit ab (Breedon & Ranaldo 2013) | Majors / H1 | vorhanden | ⊘ abgedeckt durch Nr. 2 (Fix-Fenster W1–W4 = Heim-/Auslandsstunden), kein eigener Trial |
| 14 | Volatilitätsgesteuertes Index-Long | Long Index, Größe ∝ 1/Volatilität (Moreira & Muir 2017) | US500, US100 / D1 | vorhanden | ✗ Tag 9 (T48/T49): Sharpe 0,56 / 0,32 (Halten 0,51) |
| 15 | Kurzfrist-Reversal / RSI(2) | Kaufen nach kurzen Rücksetzern im Aufwärtstrend (Connors) | US500, US100 / D1 | vorhanden | ✗ Tag 10 (T52/T53): Sharpe 0,31 / 0,28 (Halten 0,51) |
| 16 | Opening Range Breakout | Ausbruch aus der ersten 5–30-min-Range nach Kassaeröffnung (Zarattini & Aziz 2023) | US100, US500 / M5 | vorhanden | ✗ Tag 11 (T56/T57): −1,6 / −0,4 bp/Tag; 85 % Stops |
| 17 | Lead-Lag US → Asien | US-Schlussrendite sagt Eröffnung JP225/AUS200/HK50 voraus | Asien-Indizes / H1 | vorhanden | ⊘ strukturell nicht handelbar: FTMO-Asien-Indizes sind Futures-CFDs mit ≈ 19 h Handel, die US-Bewegung ist eingepreist; kein eigener Trial |
| 18 | COT-Positionierung | Contrarian bei extremer Netto-Position der Spekulanten | Majors, Gold / W1 | CFTC nachladen ⚠ live per WebRequest | ✗ Tag 12 (T60/T61): konträr Sharpe 0,22, folgend −0,50 |
| 19 | VIX-Regime | Bei Risk-off (VIX-Sprung) Long JPY, CHF, Gold | FX, Gold / D1 | VIX von FRED ⚠ live per WebRequest | ✗ Tag 13 (T64/T65): Sharpe −0,14 / 0,04 |
| 20 | Zinsdifferenz-Momentum | FX folgt Änderungen der 2-jährigen Renditedifferenz | USD-Majors / D1 | FRED (teils lückenhaft) ⚠ live per WebRequest | ✗ Tag 14 (T68/T69): Sharpe −0,22 / −0,29 |
| 21 | Pairs Trading / Kointegration | Spread AUDUSD–NZDUSD (bzw. AUDNZD) handeln bei z-Score-Extremen | AUD/NZD, EUR/CHF / H4 | vorhanden | ✗ Tag 15 (T72/T73): Sharpe 0,13 / −0,20 (SNB-Schock) |
| 22 | Gold/Silber-Ratio | Mean Reversion des Verhältnisses | XAUUSD, XAGUSD / D1 | vorhanden | ✗ Tag 16 (T76/T77): Sharpe −0,07 / 0,09 |
| 23 | Rohstoff-Währungen Lead-Lag | Öl → CAD, Gold → AUD, Dairy/Risk → NZD | USDCAD, AUDUSD / H1–D1 | vorhanden (WTI lückenhaft) | ✗ Tag 17 (T80/T81): Sharpe −0,41 / 0,21; nur gleichzeitiger Zusammenhang |
| 24 | Zentralbank-Tage FX | Drift vor/nach EZB-, BoJ-, BoE-Entscheidungen | Majors / H1 | MT5-Kalender | ✗ knapp, Tag 18 (T84/T85): FOMC-Tage +108 / +55 bp, t 2,1; Ensemble-Kandidat |
| 25 | Makro-News-Drift | Drift nach NFP/CPI-Überraschung | USD-Majors, Gold / M5 | MT5-Kalender (inkl. Prognose) | ⚠ zurückgestellt: Konsensprognosen-Historie fehlt (FRED nur Ist-Werte); testbar nach Export aus dem MT5-Kalender (CalendarValueHistory) |
| 26 | Pre-Holiday-Effekt | Long Indizes am Handelstag vor Feiertagen | Indizes / D1 | vorhanden | ✗ Tag 19 (T88/T89): +14 / +11 bp je Ereignis, t 1,7 / 0,9 |
| 27 | Halloween / Sell in May | Nur November–April long | Indizes / D1 | vorhanden (wenige Datenpunkte) | ✗ Tag 20 (T92/T93): Sharpe 0,37 / 0,47 (unter Halten) |
| 28 | 52-Wochen-Hoch | Nähe zum 52-Wochen-Hoch → Fortsetzung (George & Hwang) – ähnlich #3/#4, Prior gering | alle / D1 | vorhanden | ✗ Tag 21 (T96): Sharpe −0,54 |
| 29 | Dual Momentum | Relativ + absolut: bestes Asset aus Indizes/Gold, sonst Cash (Antonacci) | Indizes, Gold / MN | vorhanden | ✗ Tag 22 (T102/T103): Sharpe 0,17 / 0,14 |
| 30 | Donchian / Turtle | Ausbruch über 20/55-Tage-Hoch – ähnlich #3/#4, Prior gering | alle / D1 | vorhanden | ✗ Tag 21 (T97): Sharpe −0,54 |

## B – Praktiker-Setups: Sessions, Ausbrüche, Mean Reversion

| # | Strategie | Idee | Markt / TF | Daten | Status |
|---|---|---|---|---|---|
| 31 | London Breakout | Ausbruch aus der Asien-Range zur London-Eröffnung | GBPUSD, EURUSD / M15 | vorhanden | ✗ Tag 23 (T106/T107): t 0,47 / −1,01 |
| 32 | Asien-Range-Fade (Nachtscalper) | Range-Extreme in der ruhigen Asien-Session faden | EURCHF, AUDCAD, EURGBP-Ersatz / M5 | vorhanden – Rollover-Spreads beachten | ✗ Tag 24 (T110/T111): vor Kosten +, netto −12 bis −14 bp/Nacht |
| 33 | NR4 / NR7 (Crabel) | Ausbruch nach der engsten Range der letzten 4/7 Tage | alle / D1 | vorhanden | ✗ Tag 25 (T114): −0,5 bp/Tag, t −0,50 |
| 34 | Inside Bar Breakout | Ausbruch aus Inside Bar in Trendrichtung | alle / D1, H4 | vorhanden | ✗ Tag 25 (T115): +0,1 bp/Tag, t 0,15 (beide Richtungen, D1) |
| 35 | Volatility Breakout (L. Williams) | Einstieg bei Open ± k · Vortagesrange | Indizes, Gold / D1 | vorhanden | ✗ Tag 25 (T116): −4,2 bp/Tag, t −2,07; vor Kosten + |
| 36 | Bollinger Squeeze | Ausbruch nach Bandbreiten-Tief | alle / H4 | vorhanden | ✗ Tag 26 (T123): −0,25 bp/Tag, t −0,39 |
| 37 | Bollinger Mean Reversion | Rückkehr zur Mitte nach Bandberührung in Seitwärtsphasen | FX-Crosses / H1 | vorhanden | ✗ Tag 27 (T129): −11,1 bp/Tag, t −6,19; Kosten 6× Vorteil |
| 38 | Keltner-Channel-Ausbruch | ATR-Kanal-Ausbruch mit Trendfilter | alle / H4 | vorhanden | ✗ Tag 26 (T124): −0,76 bp/Tag, t −0,51 |
| 39 | z-Score Mean Reversion (OU) | Abstand zum gleitenden Mittel in Std.-Abw., Halbwertszeit schätzen | FX-Crosses / H1 | vorhanden | ✗ Tag 27 (T130): −1,8 bp/Tag, t −2,84; vor Kosten negativ |
| 40 | Hurst-Regime-Switch | Hurst > 0,5 → Trendmodell, < 0,5 → Mean Reversion | alle / H4 | vorhanden | ✗ Tag 28 (T135): −2,3 bp/Tag, t −4,70; Filter verschlechtert |
| 41 | Gap-Fill Indizes | Eröffnungslücke zum Vortagesschluss faden | Indizes / M5 | vorhanden | ✗ Tag 29 (T138): −3,2 bp/Tag, t −3,61 |
| 42 | Wochenend-Gap FX | Montags-Gap faden | Majors / H1 | vorhanden | ✗ Tag 29 (T139): formal bestanden, aber Feed-Artefakt (erste Wochenkerze HistData); auf FTMO-Zeit −5 bp |
| 43 | Große Tagesbewegung | Nach Tag > 2 ATR: Reversal oder Fortsetzung | alle / D1 | vorhanden | ✗ Tag 30 (T144/T145): −0,30 / −0,06 bp/Tag, t −0,5 / −0,1 |
| 44 | Wochentags-Effekt | Wochentags-Saisonalität | alle / D1 | vorhanden | ✗ Tag 30 (T146): +0,5 bp/Tag, t 0,50 (rollierende Wahl) |
| 45 | Multi-Timeframe-Pullback | Trend auf D1/H4, Einstieg auf H1-Rücksetzer | alle / H1 | vorhanden | ✗ Tag 31 (T153): −14,7 bp/Tag, t −6,53; vor Kosten negativ |
| 46 | Währungsstärke-Ranking intraday | Stärkste vs. schwächste Währung der Session handeln | 28 Paare / H1 | vorhanden | ✗ Tag 32 (T156/T157): −0,56 / +0,07 bp/Tag, t −1,2 / 0,2 |
| 47 | USD-Basket Mean Reversion | Einzelpaar weicht vom USD-Index (synthetisch) ab → Rückkehr | USD-Majors / H1 | vorhanden | ✗ Tag 32 (T158): −1,05 bp/Tag, t −1,17 |
| 48 | Market Profile / TPO | Rückkehr in die Value Area (80-%-Regel), zeitbasiert, ohne Volumen | Indizes / M30 | vorhanden | ✗ Tag 33 (T165): −0,8 bp/Tag, t −2,10; Durchquerung nur 45 % |
| 49 | Pivot Points (Classic/Camarilla) | Abpraller an S1/R1, Ausbruch über S3/R3 | Indizes, Majors / M15 | vorhanden | ✗ Tag 33 (T166/T167): −12,6 / −4,3 bp/Tag; vor Kosten ≤ 0 |
| 50 | Horizontale S/R-Zonen | Algorithmisch ermittelte Swing-Level, Abpraller oder Ausbruch | alle / H1–H4 | vorhanden | ✗ Tag 34 (T174/T175): −8,5 / −7,0 bp/Tag; vor Kosten ≤ 0 |
| 51 | Trendlinien-Ausbruch | Algorithmische Trendlinien aus Swing-Punkten | alle / H4 | vorhanden | ✗ Tag 34 (T176): −3,5 bp/Tag, t −2,81; vor Kosten 0 |
| 52 | Fibonacci-Pullback | Einstieg am 50–61,8-%-Retracement im Trend | alle / H4 | vorhanden | ✗ Tag 35 (T183): −1,8 bp/Tag, t −2,69 |
| 53 | ATR-Trailing-Trend (Chandelier) | Trend halten bis ATR-Trailing-Stop | alle / D1 | vorhanden | ✗ Tag 35 (T184): −0,1 bp/Tag, t −0,38 (55-Tage-Ausbruch) |
| 54 | Candlestick an Levels | Pin Bar / Engulfing an S/R | alle / H4–D1 | vorhanden | ✗ Tag 36 (T189/T190): −0,45 / −5,80 bp/Tag |
| 55 | Chartformationen | SKS, Doppeltop/-boden, Dreiecke algorithmisch | alle / H4–D1 | vorhanden ⚠ (Erkennung subjektiv) | ✗ Tag 36 (T191): Doppeltop/-boden −0,55 bp/Tag, t −1,73; SKS/Dreiecke nicht formalisiert |
| 56 | Verfallstage (OPEX / Triple Witching) | Index-Verhalten rund um Optionsverfall | US500, US100 / H1 | Termine berechenbar | ✗ Tag 37 (T201/T202): −6,7 / −30,3 bp je Ereignis |
| 57 | Jahresende / Santa Rally | Long Indizes letzte Dezemberwoche | Indizes / D1 | vorhanden (wenige Datenpunkte) | ✗ Tag 37 (T203): +0,1 bp je Ereignis (9 Ereignisse) |
| 58 | Aktien → AUDJPY | AUDJPY folgt US500 mit Verzögerung (Risk-Proxy) | AUDJPY / H1 | vorhanden | ✗ Tag 38 (T210): −1,45 bp/Tag, t −4,33; kein Nachlauf |
| 59 | US-Renditen → USDJPY | USDJPY folgt 10-jähriger US-Rendite | USDJPY / D1 | FRED vorhanden ⚠ live per WebRequest | ✗ Tag 38 (T211/T212): −0,99 / −0,13 bp/Tag; nur gleichzeitig korreliert |
| 60 | Supply/Demand-Zonen (Seiden) | Basis-Zonen vor starkem Impuls – nah an SMC, Prior gering | alle / H4 | vorhanden | ✗ Tag 36 (T192): +0,15 bp/Tag, t 0,40 (473 Trades) |

## C – Klassische Indikatoren (geringer Prior, meist an Kosten gescheitert)

| # | Strategie | Idee | Markt / TF | Status |
|---|---|---|---|---|
| 61 | MA-Crossover 50/200 | Golden/Death Cross | alle / D1 | ✗ Tag 39 (T219): −0,5 bp/Tag, t −1,39 |
| 62 | EMA 9/21 | schneller Crossover | alle / H1 | ✗ Tag 39 (T220): −13,4 bp/Tag, t −3,49 |
| 63 | Triple MA | 3 MAs in Reihenfolge als Trendfilter | alle / H4 | ✗ Tag 39 (T221): −2,3 bp/Tag, t −1,55 |
| 64 | MACD | Signal-Crossover / Nulllinie | alle / H4 | ✗ Tag 39 (T222): −3,8 bp/Tag, t −1,89 |
| 65 | RSI 14 Überkauft/Überverkauft | Fade bei 30/70 | alle / H1 | ✗ Tag 40 (T249): −15,8 bp/Tag, t −7,78 |
| 66 | Stochastik | %K/%D-Kreuzung in Extremzonen | alle / H1 | ✗ Tag 40 (T250): −29,8 bp/Tag, t −10,6 |
| 67 | Williams %R | Extremzonen-Fade | alle / H1 | ✗ Tag 40 (T251): −50,3 bp/Tag, t −16,8 |
| 68 | CCI | ±100-Durchbruch | alle / H4 | ✗ Tag 40 (T252): −2,9 bp/Tag, t −1,34 |
| 69 | ADX / DMI | DI-Kreuzung bei ADX > 25 | alle / H4 | ✗ Tag 39 (T223): −1,8 bp/Tag, t −1,55 |
| 70 | Parabolic SAR | Stop-and-Reverse | alle / H4 | ✗ Tag 39 (T224): −5,2 bp/Tag, t −2,78 |
| 71 | Supertrend | ATR-basierter Trendwechsel | alle / H4 | ✗ Tag 39 (T225): −1,5 bp/Tag, t −1,04 |
| 72 | Ichimoku | Kumo-Ausbruch, Tenkan/Kijun | alle / H4–D1 | ✗ Tag 39 (T226): −2,7 bp/Tag, t −2,01 |
| 73 | Heikin-Ashi | Farbwechsel als Trendsignal | alle / H4 | ✗ Tag 39 (T227): −6,7 bp/Tag, t −3,23 |
| 74 | Renko | Box-Wechsel als Signal (Backtest-Fallen beachten) | alle / M1-basiert | ✗ Tag 40 (T253): −4,7 bp/Tag, t −1,94 (H1-Schlusskurse) |
| 75 | RSI/MACD-Divergenzen | Reversal bei Divergenz | alle / H4 | ✗ Tag 40 (T254): −1,6 bp/Tag, t −2,59 |
| 76 | Kalman-Filter-Trend | Adaptive Trendschätzung statt MA | alle / H4 | ✗ Tag 39 (T228): −3,1 bp/Tag, t −1,72 |
| 77 | Harmonische Muster | Gartley, Bat, Butterfly | alle / H4 | ✗ Tag 41 (T267): Gartley/Bat −0,1 bp/Tag, 107 Trades |
| 78 | Elliott-Wellen | Wellenzählung | alle / D1 | ⊘ nicht vorab formalisierbar, kein Test (Tag 41) |
| 79 | Wyckoff | Akkumulation/Distribution | alle / H4 | ✗ Tag 41 (T268): Spring/Upthrust ohne Volumen −1,3 bp/Tag, t −0,99 |
| 80 | Scalping M1/M5 | EMA-/Momentum-Scalps | Majors / M1 | ✗ Tag 41 (T269): M5 EMA 9/21 −165 bp/Tag; vor Kosten 0 |

## D – Statistik und Machine Learning (hohes Overfitting-Risiko)

| # | Strategie | Idee | Markt / TF | Status |
|---|---|---|---|---|
| 81 | Hidden-Markov-Regime | Regime erkennen, je Regime eigenes Modell | alle / D1 | |
| 82 | GARCH-Volatilitätsprognose | Ausbruch/Positionsgröße aus Vol-Prognose | alle / D1 | |
| 83 | Gradient Boosting Richtung | Features → Richtung nächste n Bars | alle / H1 | |
| 84 | Meta-Labeling (López de Prado) | ML filtert Signale einer Basisstrategie, Triple Barrier | Basis aus A/B | |
| 85 | k-NN-Analogien | Ähnliche historische Muster suchen | alle / D1 | |
| 86 | LSTM / Transformer | Sequenzmodell auf Renditen, als ONNX in MT5 | alle / H1 | |
| 87 | Reinforcement Learning | Agent lernt Positionierung, als ONNX in MT5 | alle / H1 | |
| 88 | Genetic Programming | Automatische Regelsuche – extremes Data Mining | alle | ⚠ |
| 89 | Retail-Sentiment contrarian | Gegen Mehrheit der Retail-Positionen (IG/Myfxbook) | Majors / D1 | ⚠ Historie knapp |
| 90 | Gold-Saisonalität | Monats-/Jahreszeiteffekte bei Gold | XAUUSD / D1 | |

## E – Datenlücken, FTMO-Regeln, Kontrollen

| # | Strategie | Problem | Status |
|---|---|---|---|
| 91 | VWAP-Reversion | kein echtes Volumen in HistData | ⚠ |
| 92 | Volume Profile | kein echtes Volumen | ⚠ |
| 93 | Order Flow / Footprint / DOM | keine Orderbuchdaten | ⛔ |
| 94 | News-Straddle | erlaubt, aber Slippage und Spread-Ausweitung im Backtest kaum abbildbar | ⚠ |
| 95 | Grid Trading | Ruinrisiko vs. 5 %/10 %-Verlustgrenze | ⛔ |
| 96 | Martingale | Ruinrisiko vs. Verlustgrenze | ⛔ |
| 97 | Latenz- / Tick-Arbitrage | bei FTMO verboten | ⛔ |
| 98 | Zufalls-Einstiege (Placebo) | Kalibriert die Pipeline: wie oft „besteht“ reiner Zufall? Am besten früh nebenbei laufen lassen | Kontrolle |
| 99 | Mondphasen (Placebo) | Zweite Kontrolle ohne ökonomische Begründung | Kontrolle |
| 100 | Ensemble der besten Kandidaten | Mehrere schwache, unkorrelierte Edges kombinieren – erst am Ende, mit Trial-Korrektur | |

---

## Spielregeln gegen Selbsttäuschung

1. **Trial-Log über alle Strategien führen.** Bei 100 Versuchen findet man auch ohne echten Edge Gewinner. Bei t ≥ 3 erwartet man über 100 unabhängige Tests rund 0,3 Zufallstreffer – plus jede Variante, die man nachträglich ausprobiert.
2. **Hold-out 2024–2026 bleibt gemeinsam für alle.** Er wird pro Strategie höchstens einmal angefasst, und jedes Anfassen wird geloggt.
3. **Vorregistrieren vor dem ersten Lauf**, wie in `smart-money-concept/docs/`. Nachträgliche Parameteränderung = neuer Versuch.
4. **Kosten realistisch:** FTMO-Spreads, Kommission, Swaps inkl. Aufschlag; Test bei doppelten Kosten.
5. **Pipeline wiederverwenden** (Daten, Zeitmodell, Kostenmodelle, FTMO-Monte-Carlo) statt sie pro Strategie neu zu bauen.
6. **Artefakt-Prüfung vor dem Hold-out:** Hängt ein bestandenes Ergebnis an einer Uhrzeit oder an Sitzungsgrenzen, wird es vorher gegen benachbarte Zeiten und Sommer/Winter geprüft. HistData stempelt in fester EST: Im Sommer fehlt die erste Handelsstunde der Woche (Lehre aus Nr. 42).

## Tageslog

| Tag | Datum | # | Strategie | Ergebnis | Kernzahl |
|---|---|---|---|---|---|
| 1 | 24.10.2026 | 1–4 | SMC + Fix-Reversal + Trendfolge FX/Gold + Trendfolge Indizes/Rohstoffe | ✗ | P7: Sharpe −0,37 netto |
| 2 | 24.10.2026 | 5 | Monatsend-Rebalancing am London-Fix | ✗ | M-1H −4,4 bp/Ereignis, t −1,0; Paper-Effekt auf 1/10 geschrumpft |
| 3 | 24.10.2026 | 6 | FX Carry G8 | ✗ | K-3 Sharpe −0,16, K-1 −0,02; Swaps +1 % p. a., Kurs −1,4 bis −2,6 % p. a. |
| 4 | 24.10.2026 | 7 | FX Querschnitts-Momentum G8 | ✗ | X-1 Sharpe −0,28, X-12 −0,81 (t −2,5: eher Umkehr) |
| 5 | 24.10.2026 | 9 | Pre-FOMC-Drift | ✗ knapp | P-SPX +19 bp/Termin (t 2,38), P-NDX +28 bp (t 2,26); 3 von 4 Kriterien – Ensemble-Kandidat |
| 6 | 24.10.2026 | 10 | Turn-of-the-Month US500 | ✗ | T-KLASSIK +22 bp (t 1,17), T-FRÜH +36 bp (t 1,68) |
| 7 | 24.10.2026 | 11 | Intraday-Momentum US500 | ✗ | I-ROD +1,0 bp/Tag (t 1,31); Regression t 3,45, aber Effekt ≈ 2× Kosten |
| 8 | 24.10.2026 | 12 | Overnight-Drift US500 | ✗ | N-NACHT t 0,14, N-EU t −1,54, N-EU-DOWN t −0,18 |
| 9 | 24.10.2026 | 14 | Vol-gesteuertes US500-Long | ✗ | V-VOL Sharpe 0,56 (t 1,68), V-MM 0,32; Halten 0,51 |
| 10 | 24.10.2026 | 15 | Kurzfrist-Reversal US500 (Connors) | ✗ | R-RSI2 Sharpe 0,31, R-7S 0,28; Trefferquote 70–77 % |
| 11 | 24.10.2026 | 16 | Opening Range Breakout 5 min | ✗ | O-NDX t −0,54, O-SPX t −0,16; Range ≈ 10 bp, Kosten 0,14–0,24 R |
| 12 | 24.10.2026 | 18 | COT-Extreme | ✗ | C-KONTRA Sharpe 0,22 (t 0,62), C-FOLGE −0,50 |
| 13 | 24.10.2026 | 19 | VIX-Regime | ✗ | X-HAVEN Sharpe −0,14, X-FEAR 0,04 |
| 14 | 24.10.2026 | 20 | Zins-Momentum G8 | ✗ | Z-12 Sharpe −0,22, Z-3 −0,29 |
| 15 | 24.10.2026 | 21 | z-Score Mean Reversion AUDNZD / EURCHF | ✗ | Sharpe 0,13 / −0,20 |
| 16 | 24.10.2026 | 22 | Gold/Silber-Ratio | ✗ | G-60 Sharpe −0,07, G-250 0,09 |
| 17 | 24.10.2026 | 23 | Rohstoff-Lead-Lag | ✗ | R-OEL Sharpe −0,41, R-GOLD 0,21 |
| 18 | 24.10.2026 | 24 | USD an FOMC-Tagen | ✗ knapp | F-USD +108 bp/Termin (t 2,10), F-CARRY +55 bp (t 2,11, 9/9 Jahre) – Ensemble-Kandidat |
| 19 | 24.10.2026 | 26 | Pre-Holiday US-Indizes | ✗ | H-SPX +13,9 bp (t 1,68), H-NDX +10,6 bp |
| 20 | 24.10.2026 | 27 | Halloween US-Indizes | ✗ | S-SPX Sharpe 0,37, S-NDX 0,47 |
| 21 | 24.10.2026 | 28, 30 | Kanal-Ausbruch (52 Wochen, Turtle) | ✗ | beide Sharpe −0,54; FX −35 bis −39 % |
| 22 | 24.10.2026 | 29 | Dual Momentum | ✗ | D-TOP1 Sharpe 0,17, D-TOP2 0,14 |
| 23 | 24.10.2026 | 31 | London Breakout | ✗ | L-GBP t 0,47, L-EUR t −1,01 |
| 24 | 24.10.2026 | 32 | Asien-Range-Fade | ✗ | Kosten 2–7× der Vorteil |
| 25 | 24.10.2026 | 33–35 | NR7, Inside Bar, Volatility Breakout | ✗ | vor Kosten +0,01–0,04 R, Kosten größer |
| 26 | 24.10.2026 | 36, 38 | Bollinger Squeeze, Keltner-Ausbruch | ✗ | vor Kosten +0,03 R, Kosten 0,045 R |
| 27 | 24.10.2026 | 37, 39 | Bollinger-MR, z-Score/OU-MR | ✗ | Umkehr auf H1 nach Kosten negativ |
| 28 | 24.10.2026 | 40 | Hurst-Regime-Switch | ✗ | H ≈ 0,5, kein Regime-Signal |
| 29 | 24.10.2026 | 41, 42 | Gap-Fill Indizes, Wochenend-Gap FX | ✗ | Nr. 42 formal bestanden, als Feed-Artefakt verworfen |
| 30 | 24.10.2026 | 43, 44 | Große Tagesbewegung, Wochentags-Effekt | ✗ | Folgetage nach 2-ATR-Tagen = Rauschen |
| 31 | 24.10.2026 | 45 | Multi-Timeframe-Pullback | ✗ | Ziel 2R nur 22 % |
| 32 | 24.10.2026 | 46, 47 | Währungsstärke-Ranking, USD-Basket-MR | ✗ | vor Kosten +0,02–0,05 R |
| 33 | 24.10.2026 | 48, 49 | Market Profile 80 %, Pivot Points | ✗ | Level ohne Wirkung |
| 34 | 24.10.2026 | 50, 51 | S/R-Zonen, Trendlinien | ✗ | Swing-Level ohne Wirkung |
| 35 | 24.10.2026 | 52, 53 | Fibonacci-Pullback, Chandelier-Trend | ✗ | Fib-Zone ohne Wirkung; Trend neutral |
| 36 | 24.10.2026 | 54, 55, 60 | Candlesticks an Levels, Doppeltop/-boden, Supply/Demand | ✗ | Muster ohne Vorhersagekraft |
| 37 | 24.10.2026 | 56, 57 | Verfallstage, Santa Rally | ✗ | Kalendereffekte verschwunden |
| 38 | 24.10.2026 | 58, 59 | US500 → AUDJPY, US-Renditen → USDJPY | ✗ | kein verzögerter Zusammenhang |
| 39 | 24.10.2026 | 61–64, 69–73, 76 | 10 Trendindikatoren | ✗ | vor Kosten +0,003–0,021 R |
| 40 | 24.10.2026 | 65–68, 74, 75 | Oszillatoren, Renko, Divergenzen | ✗ | Umkehr vor Kosten ≤ 0 |
| 41 | 24.10.2026 | 77, 79, 80 (78 ⊘) | Harmonische Muster, Wyckoff-Spring, Scalping | ✗ | Abschnitt C ohne Treffer |
| 42 | | | | | |
