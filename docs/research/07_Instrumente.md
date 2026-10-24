<!-- Kapitel 7: Instrument-Spezifika der 25 Symbole | Deep-Research-Rohbericht (Recherche-Agent), Stand 2026-10-24, unverändert übernommen -->

# Teilbericht: Instrument-Spezifika der 25 Symbole (SMC-EA, MQL5)

Stand der Daten ist der 24.10.2026. Legende: „gem.“ heißt gemessen und zitiert. „abgel.“ heißt eigene Rechnung oder Einordnung aus zitierten Daten. „Größenordnung“ heißt, es gibt keine harte Messung. Das Websuche-Budget war zwischenzeitlich erschöpft. Punkte ohne Beleg sind markiert, vor allem Hurst-Werte pro Paar und BIS-Anteile einzelner Crosses.

## 0. Kernaussagen für das EA-Design

- **Das Risiko muss pro Währung gesteuert werden, nicht pro Symbol.** Die 25 Symbole bestehen aus 8 Währungen plus Gold. Daraus ergeben sich realistisch 4–6 unabhängige gleichzeitige Positionen.
- **Liquidität sitzt in sechs USD-Majors.** Jeder davon hatte 2025 mindestens 4,9 % des Weltumsatzes. Die 18 Crosses sind dünne Märkte, deren Preis weitgehend synthetisch über die USD-Legs entsteht. Alle CAD-Crosses zusammen kommen auf höchstens ≈0,5 % des Weltumsatzes (abgel.).
- **Nur sechs Symbole sind für M5-Entries günstig genug.** EURUSD, GBPUSD, USDJPY, EURJPY, GBPJPY und XAUUSD bleiben bei M5-Entries unter ≈15 % eines Stops von 1×ATR(M5).
  - AUDNZD, AUDCAD, CADCHF, EURCHF, GBPCHF und GBPNZD liegen bei 26–47 %. Für sie kommt nur M15 oder H1 in Frage.
- **Volatilitäts-Regime wechseln schnell, daher müssen alle Distanzen ATR-basiert sein.**
  - Gold: Tagesrange Ø 2025 ≈60 USD, 2026 YTD ≈132 USD.
  - USDJPY: 0,89 % des Kurses 2025, 0,60 % im Jahr 2026.
- **Öffentliche Backtests zeigen pro Instrument keine robuste Kante.** Getestet wurden Sweep/Reclaim an PDH/PDL, Asia-Range-Breaks und London-ORB auf Dukascopy-Daten 2022–2026. Nach Mehrfachtest-Korrektur ist kein Effekt signifikant.
  - Ungebestätigtes Fading an Liquidität ist signifikant **schlechter** als Zufall: 40,9 % gegenüber 49,4 % im Kontrollarm.
  - Der EA braucht daher Bestätigung (Displacement oder CHoCH) und einen Kostenfilter.
- **Tail-Risiken bei JPY, CHF und Gold:**
  - JPY: 2026 Interventionen über ¥27,1 Bio., am 31.07.2026 die erste gemeinsame US-JP-Intervention.
  - CHF: Beim SNB-Schock 2015 stieg der Franken intraday um bis zu ≈30 %.
  - Gold: Größte Tagesrange 771 USD. Allzeithoch 5.595 USD am 29.01.2026.
- **Rollover um 17:00 ET ist eine Sperrzone.** Die Spreads sind dann 5–7× breiter, und Short-Stops werden auf dem Ask ausgelöst. Daraus folgt eine Sperrzeit von 16:45 bis 18:15 ET.

---

## 1. Instrumententabelle (25 Symbole)

Spalten:
- **Spread:** Raw-Durchschnitt von IC Markets („current or very recent“, Abruf Oktober 2026). In Klammern steht bei den Majors der Razor-Durchschnitt von Pepperstone vom 01.–31.08.2026 inklusive Rollover.
- **ADR:** OffbeatForex, ATR auf Tageskerzen, Werte 2025 mit 2024 in Klammern, in Pips.
- **Aktivste Phase:** in UTC. „50 %“ ist die Stunde, bis zu der im Mittel 50 % der Tagesrange erreicht sind (fxbacktest, Dukascopy 2010–2026, gem.).

| # | Symbol | Basis/Quote | Digits → Pip | 1 Lot | Raw-Spread Ø (Pips) | ADR 2025 (2024) | Aktivste Phase | Besonderheiten |
|---|---|---|---|---|---|---|---|---|
| 1 | EURUSD | EUR/USD | 5 → 0,0001 | 100k EUR | 0,01 (0,1) | 75 (65) | Overlap 12–16 UTC; 50 % bis 08, 80 % bis 13 UTC | #1 im BIS-Survey (21,2 %); ECB-Fix 14:15 CET; geringste Kosten/ADR |
| 2 | GBPUSD | GBP/USD | 5 → 0,0001 | 100k GBP | 0,04 (0,2) | 90 (81,5) | London + Overlap; 50 % bis 08 UTC | UK-Daten 07:00 London; stärkster Monatsend-Fix-Effekt (2,25×); Flash-Crash 2016 |
| 3 | USDJPY | USD/JPY | 3 → 0,01 | 100k USD | 0,03 (0,2) | 133 (157,5) | Tokio (33 % des Volumens) + NY; 50 % bis 06 UTC | MoF-Interventionen; Tokio-Fix 9:55 JST/Gotobi; BoJ ohne feste Uhrzeit |
| 4 | AUDUSD | AUD/USD | 5 | 100k AUD | 0,02 (0,1) | 57 (55) | Asia (32 % des Volumens); 50 % bis 05 UTC | China/Rohstoffe; RBA 14:30 Sydney; höchster Leitzins (4,60 %) |
| 5 | NZDUSD | NZD/USD | 5 | 100k NZD | 0,38 | 54 (52) | Asia (32 % des Volumens) | dünn (NZD 1,5 % Weltanteil); RBNZ 14:00 NZ; v. a. als SMT-Referenz zu AUDUSD |
| 6 | USDCAD | USD/CAD | 5 | 100k USD | 0,04 (0,2) | 71 (63) | NY (45 % des Volumens im Overlap); 50 % bis 09 UTC | Öl; BoC 09:45 ET; London-ORB-Fortsetzung 47,6 % (niedrigster FX-Wert) |
| 7 | USDCHF | USD/CHF | 5 | 100k USD | 0,09 (0,2) | 62 (59,5) | London/Overlap (abgel.) | Safe Haven; SNB 0 %; ≈ Spiegelbild von EURUSD (ρ ≈ −0,9) |
| 8 | EURJPY | EUR/JPY | 3 | 100k EUR | 0,30 | 128,5 (158) | Tokio-Ende/London; 50 % bis 07 UTC | volumenstärkster JPY-Cross; Asia-Break-Fortsetzung 54,2 % |
| 9 | GBPJPY | GBP/JPY | 3 | 100k GBP | 0,82 | 160 (200) | London; 50 % bis 07 UTC | höchste FX-ADR der Liste; Spread um 21 UTC = 69 % der Stundenrange |
| 10 | AUDJPY | AUD/JPY | 3 | 100k AUD | 0,50 | 97 (115,5) | Asia; 50 % bis 04 UTC, 65 % der Range bis 07 UTC | Risk-on/off und Carry; Flash-Crash-Risiko an Asia-Feiertagen |
| 11 | NZDJPY | NZD/JPY | 3 | 100k NZD | 0,60 | 84 (99) | Asia (abgel.) | wie AUDJPY, aber dünner |
| 12 | CADJPY | CAD/JPY | 3 | 100k CAD | 0,48 | 96 (115) | Tokio + NY (abgel.) | Öl × JPY; CAD-Crosses zusammen ≤0,5 % Weltumsatz |
| 13 | CHFJPY | CHF/JPY | 3 | 100k CHF | 0,86 | 125,5 (139) | London (abgel.) | zwei Safe Havens; SNB- und MoF-Risiko gleichzeitig |
| 14 | EURCAD | EUR/CAD | 5 | 100k EUR | 0,74 | 88,5 (76,5) | London + NY-Vormittag (abgel.) | Öl; ECB und BoC |
| 15 | EURCHF | EUR/CHF | 5 | 100k EUR | 0,61 | 48,5 (55,5) | London; 50 % bis 08 UTC | langfristige Tagesrange nur 0,53 % des Kurses; SNB 2015; ORB-Fortsetzung 49,4 % |
| 16 | EURNZD | EUR/NZD | 5 | 100k EUR | 1,32 | 129 (116,5) | London + NZ-Datenfenster (abgel.) | hoher Spread, dünn |
| 17 | EURAUD | EUR/AUD | 5 | 100k EUR | 0,80 | 120 (104,5) | London + AU-Daten (abgel.) | ρ zu AUDNZD −0,90 (21 Tage) |
| 18 | GBPCHF | GBP/CHF | 5 | 100k GBP | 1,10 | 74 (81) | London (abgel.) | Safe-Haven-Leg; Kosten im Verhältnis zur ADR hoch |
| 19 | GBPNZD | GBP/NZD | 5 | 100k GBP | 1,98 | 147 (136) | London (abgel.) | breitester Raw-Spread der Liste |
| 20 | GBPCAD | GBP/CAD | 5 | 100k GBP | 1,12 | 108 (95,5) | London + NY (abgel.) | ORB-Fortsetzung 48,8 %; Trefferquote bei 1:1 nur 47,4 % |
| 21 | GBPAUD | GBP/AUD | 5 | 100k GBP | 1,06 | 136 (124) | London (abgel.) | hohe ADR bei moderaten Kosten |
| 22 | AUDNZD | AUD/NZD | 5 | 100k AUD | 0,77 | 51 (51,5) | Asia (abgel.) | höchste Kosten/ADR (≈3,9 %); Range-Charakter |
| 23 | AUDCAD | AUD/CAD | 5 | 100k AUD | 0,68 | 57 (55,5) | Asia; 50 % bis 06 UTC | Spread im Dukascopy-Feed = 3,28 % der Tagesrange |
| 24 | CADCHF | CAD/CHF | 5 | 100k CAD | 0,58 | 44 (45) | London/NY; 50 % bis 09 UTC | niedrigste ADR der Liste |
| 25 | XAUUSD | XAU/USD | meist 2 (teils 3); „Pip“ uneinheitlich (0,01, 0,10 oder 1,00 USD) | meist 100 oz (Mini 10, Mikro 1) | 0,07–0,10 USD (IC, Pepperstone-Test); Dukascopy Ø 0,61 USD | 2025 ≈53–60 USD; 2026 YTD ≈132 USD | London-Open + 13–15 UTC; Asia-Spitze um 01 UTC | tägliche Pause ≈17–18 ET; Allzeithoch 5.595 USD (29.01.2026) |

**Hinweise zur Tabelle**

- **Pip und Point.** Bei 5- bzw. 3-stelligen Quotes gilt Pip = 10 × Point. Bei Gold ist „Pip“ nicht standardisiert:
  - Exness und RoboForex nennen 0,01 einen Pip, andere 0,10.
  - Ein 2-Digit-Broker zeigt dieselben 0,25 USD als 25 Punkte, ein 3-Digit-Broker als 250.
  - Folge für den EA: intern nur in Preis- und ATR-Einheiten rechnen. Benötigt werden `SYMBOL_DIGITS`, `SYMBOL_POINT`, `SYMBOL_TRADE_TICK_SIZE`, `SYMBOL_TRADE_TICK_VALUE_LOSS` und `SYMBOL_TRADE_CONTRACT_SIZE`.
- **Pip-Werte in USD pro Lot (abgel. aus EZB-Referenzkursen vom 23.10.2026).** Zugrunde liegen EURUSD 1,1193, USDJPY ≈156,80, USDCAD ≈1,3995, USDCHF ≈0,8244, AUDUSD ≈0,7022 und NZDUSD ≈0,5687.
  - Quote USD: 10,00
  - Quote JPY: ≈6,38
  - Quote CAD: ≈7,15
  - Quote CHF: ≈12,13
  - Quote NZD: ≈5,69
  - Quote AUD: ≈7,02
  - XAUUSD bei 100 oz: 1 USD je 0,01 USD Kursbewegung
- **Spreads.** Die IC-Werte für Majors (0,01–0,09) sind optimistisch.
  - Ein 30-Tage-Test bei Pepperstone Razor (≈März 2026) maß EURUSD 0,4 in Asia, 0,2 in London und im Overlap, 0,3 zum NY-Close und **1,4 (max. 3,5) zum Rollover**. Dazu GBPUSD 0,4, USDJPY 0,2, AUDUSD 0,3 und Gold 0,10 USD.
  - IC verlangt 3,50 USD pro Lot und Seite (beim EUR-Konto 5,50 EUR Round-Turn).
- **ADR im aktuellen Regime.** Laut fxbacktest (Dukascopy, bis September 2026) lag die Tagesrange 2026 YTD bei EURUSD bei 0,57 % des Kurses (≈64 Pips, abgel.), bei GBPUSD bei 0,66 % (≈88) und bei USDJPY bei 0,60 % (≈94). Der EURUSD-Durchschnitt der letzten 10 Wochen betrug nur ≈50 Pips (Trade That Swing, September 2026). Die ADR-Spalte ist deshalb nur ein Startwert; die Normalisierung muss rollierend erfolgen.

Quellen: [IC Spreads](https://ic.com/global/en/trading-pricing/spreads) · [IC Forex](https://ic.com/global/en/trading-markets/forex) · [Pepperstone Pairs & Spreads](https://pepperstone.com/en/markets/forex/pairs-and-spreads) · [LowSpreadBroker Pepperstone-Test](https://lowspreadbroker.com/artigos/pepperstone-spreads-review) · [OffbeatForex ADR 2014–2025](https://offbeatforex.com/forex-average-daily-range-table/) · [fxbacktest ADR](https://fxbacktest.app/research/average-daily-range/) · [fxbacktest Range-Fortschritt](https://fxbacktest.app/research/when-daily-high-low-forms/) · [OANDA Session-Volumen 2024](https://www.oanda.com/us-en/trade-tap-blog/asset-classes/forex/best-time-to-trade-forex-volume-insights/) · [EZB-Referenzkurse](https://www.ecb.europa.eu/stats/policy_and_exchange_rates/euro_reference_exchange_rates/html/index.en.html) · [Trade That Swing EURUSD](https://tradethatswing.com/analyzing-eur-usd-volatility-for-day-trading-purposes/) · [IC Commodity-Spec](https://cdn.icmarkets.eu/uploads/Commodity-Specification-Sheet.pdf) · [Exness Commodities](https://get.exness.help/hc/en-us/articles/17854173039388-Commodities) · [RoboForex XAUUSD](https://roboforex.com/forex-trading/trading/specifications/card/pro-stan/XAUUSD/) · [FXNX Points vs Pips](https://fxnx.com/en/blog/points-vs-pips-xauusd-what-mt5-s-digits-field-changes) · [FXNX Symbol-Varianten](https://fxnx.com/en/blog/xauusd-symbol-variants-mt5-gold-xauusd-m-suffixes) · [MQL5 SymbolInfo](https://www.mql5.com/en/docs/constants/environment_state/marketinfoconstants)

---

## 2. Liquiditäts-Ranking (BIS Triennial Survey)

Der Gesamtumsatz lag im April 2025 bei 9,6 Bio. USD pro Tag, 28 % über den 7,5 Bio. USD von 2022.

| Paar | Anteil 2022 | Anteil 2025 | Veränderung |
|---|---|---|---|
| EUR/USD | 22,7 % | 21,2 % | −1,5 |
| USD/JPY | 13,5 % | 14,3 % | +0,8 |
| USD/CNY | 6,6 % | 8,1 % | +1,5 |
| GBP/USD | 9,5 % | 7,6 % | −1,9 |
| USD/CAD | 5,5 % | 5,3 % | −0,2 |
| AUD/USD | 5,1 % | 4,9 % | −0,2 |
| USD/CHF | 3,9 % | 4,9 % | +1,0 |

**Anteile der einzelnen Währungen 2025 (2022 in Klammern; die Summe über alle Währungen ist 200 %):**

| Währung | 2025 | 2022 |
|---|---|---|
| USD | 89,2 % | 88,4 % |
| EUR | 28,9 % | 30,6 % |
| JPY | 16,8 % | 16,7 % |
| GBP | 10,2 % | 12,9 % |
| CHF | 6,4 % | 5,2 % |
| AUD | 6,1 % | 6,4 % |
| CAD | 5,8 % | 6,2 % |
| NZD | 1,5 % | 1,7 % |

London hatte im April 2025 einen EUR/USD-Umsatz von 1.010 Mrd. USD pro Tag, das sind 25 % des Londoner Umsatzes.

**Restanteile der Crosses (abgel.: Währungsanteil minus Anteil des USD-Paares, 2025).** Die Werte sind Obergrenzen und enthalten auch Crosses außerhalb der Liste, zum Beispiel EUR/GBP oder EUR/SEK.

| Währung | Rest für alle Crosses |
|---|---|
| EUR | ≤7,7 % |
| GBP | ≤2,6 % |
| JPY | ≤2,5 % |
| CHF | ≤1,5 % |
| AUD | ≤1,2 % |
| CAD | ≤0,5 % |
| NZD | Gesamtanteil nur 1,5 % |

Die Anteile einzelner Crosses wie EUR/JPY oder EUR/CHF waren nicht belegbar. EUR/JPY gilt laut Babypips/BIS als volumenstärkster JPY-Cross.

**Implikationen für den EA:**
- **Liquiditäts-Tiers:**
  - L1: EURUSD, USDJPY, GBPUSD, USDCAD, AUDUSD, USDCHF.
  - L2 (Größenordnung): EUR- und JPY-Crosses.
  - L3: NZD-Paare, CAD- und CHF-Crosses.
  - Gold ist nicht Teil der BIS-Paartabelle.
- **Struktur in Crosses ist abgeleitet.** Ein Cross-Swing entsteht meist aus dem Zusammenspiel zweier USD-Legs. Liquidity Pools und Order Blocks sind dort weniger „originär“. Das ist ein Argument, SMT und Struktur primär auf den USD-Legs zu lesen.
- **Die Bedeutung von USD/JPY steigt, die von GBP/USD sinkt.** Liquidität ist ein Faktor beim Tiering, aber kein Kantenbeweis.

Quellen: [BIS 2025 FX-Turnover](https://www.bis.org/statistics/rpfx25_fx.htm) · [BIS 2022](https://www.bis.org/statistics/rpfx22_fx.htm) · [Wikipedia FX Market (Währungsanteile 2022/2025)](https://en.wikipedia.org/wiki/Foreign_exchange_market) · [CompareForexBrokers/BusinessWire (Paar-Anteile)](https://www.businesswire.com/news/home/20251001844788/en) · [The Full FX](https://thefullfx.com/10-observations-on-the-bis-fx-turnover-survey/) · [BoE London-Survey April 2025](https://www.bankofengland.co.uk/markets/london-foreign-exchange-joint-standing-committee/results-of-the-semi-annual-fx-turnover-survey-april-2025) · [RBA 2025](https://www.rba.gov.au/media-releases/2025/mr-25-28-tables.html) · [Babypips Yen-Crosses](https://www.babypips.com/learn/forex/euro-and-yen-crosses)

---

## 3. Session-Verhalten, Tageshoch und -tief, Fixings

### 3.1 Stundenprofil

Die Werte sind durchschnittliche Stunden-Ranges in Pips nach Session (UTC), gemessen von fxbacktest auf Dukascopy H1, 2010–2026. Bei Gold sind es Punkte, langfristig seit 2009.

| Instrument | 00–07 Asia | 07–12 London | 12–16 Overlap | 16–21 NY | 21–24 spät | Spitze/Ruhe |
|---|---|---|---|---|---|---|
| EURUSD | 13,3 | 20,3 | 26,1 | 15,1 | 8,6 | 3,4× |
| GBPUSD | 15,8 | 27,2 | 31,0 | 17,9 | 11,3 | 3,1× |
| USDJPY | 17,2 | 17,4 | 24,0 | 14,6 | 12,2 | 2,4× |
| AUDUSD | 15,0 | 15,4 | 19,9 | 12,6 | 10,2 | 2,2× |
| USDCAD | 11,7 | 16,3 | 26,6 | 16,6 | 9,7 | 3,6× |
| EURJPY | 21,4 | 26,4 | 29,9 | 18,1 | 15,2 | 2,2× |
| GBPJPY | 26,7 | 35,8 | 38,8 | 23,8 | 20,4 | 2,1× |
| Gold (Pkt) | 445 | 491 | 814 | 482 | 318 | 3,4× |

Alle Instrumente haben ihre Spitze um 14 UTC, Gold um 13 UTC, also im NY-AM-Fenster. Asia-lastige Paare (JPY, AUD) haben ein flaches Profil mit einem Verhältnis von Spitze zu Ruhe von 2,1–2,4×.

**Range-Fortschritt und Asia-Range (00–07 UTC), fxbacktest 2010–2026:**

| Instrument | 50 % / 80 % der Range erreicht (UTC) | Anteil Asia-Range an der Tagesrange | Beide Asia-Extreme gebrochen |
|---|---|---|---|
| AUDJPY | 04 / 12 | 65,2 % | 18,4 % |
| AUDUSD | 05 / 12 | 61,6 % | 21,7 % |
| USDJPY | 06 / 13 | 59,4 % | 22,6 % |
| EURJPY | 07 / 12 | 57,9 % | 24,1 % |
| GBPJPY | 07 / 12 | 55,9 % | 28,4 % |
| AUDCAD | 06 / 13 | 59,3 % | 26,5 % |
| EURUSD | 08 / 13 | 47,9 % | 37,7 % |
| GBPUSD | 08 / 13 | 46,9 % | 38,4 % |
| EURCHF | 08 / 13 | 50,3 % | 37,4 % |
| Gold | 08 / 13 | 50,3 % | 34,7 % |
| USDCAD | 09 / 14 | 44,0 % | 46,6 % |
| CADCHF | 09 / 14 | 43,1 % | 46,2 % |

Die Volumenanteile nach Session (OANDA, 2024) passen dazu:

| Paar | Tokio-Session | London-NY-Overlap |
|---|---|---|
| USDJPY | 33 % | 30 % |
| AUDUSD | 32 % | 34 % |
| NZDUSD | 32 % | 32 % |
| USDCAD | 21 % | 45 % |
| EURUSD | 17 % | 41 % |
| GBPUSD | 16 % | 38 % |

Der Volumen-Peak liegt bei 08:30–09:00 ET: 7 % des Tagesvolumens fallen in 2 % der Zeit.

**Folge für die Killzones in NY-Zeit:**
- JPY-, AUD- und NZD-Paare machen den Großteil ihrer Range in der Asia-Killzone (20:00–00:00 ET) und der London-Killzone.
- CAD- und CHF-Paare machen ihn in London und NY AM (07:00–10:00 ET).
- Nach 13–14 UTC (≈09–10 ET) sind im Mittel 80 % der Range erledigt. Ein ADR-Erschöpfungsfilter ist deshalb sinnvoll.

### 3.2 Wann entstehen Tageshoch und -tief?

- **EURUSD** (UTC-Tag, 2010–2026):
  - Häufigste Stunden für das Hoch: 00 UTC (8,8 %, teils ein Artefakt der Tagesgrenze), 14 UTC (7,9 %), 12 und 15 UTC (je 6,6 %), 13 UTC (6,4 %). Bei Gleichverteilung wären es 4,2 %.
  - Häufigste Stunde für das Tief: 00 UTC (10,6 %).
  - Hoch **und** Tief zusammen in 12–16 UTC: nur 6,2 % der Tage.
- **Gold** (UTC-Tag, Juli 2024 bis Juli 2026):
  - Anteile an den Tagesextremen: 00 UTC 15,1 %, 01 UTC 9,3 %, 13 UTC 6,2 %, 14 UTC 7,8 %, 15 UTC 7,1 %, 23 UTC 5,8 %. Das Fenster 12–15 UTC kommt zusammen auf 24,2 %.
  - London durchbrach an 80,6 % der Tage die Asia-Range. NY setzte diesen Bruch in 69,0 % der Fälle fort.
- **Fixing-Muster** (Krohn, Mueller & Whelan, Bank of Canada WP 2021-48; G9-Paare 1999–2019):
  - Der USD steigt systematisch **vor** dem Tokio-Fix (9:55 JST), dem EZB-Fix (14:15 CET) und dem London-Fix (16:00) und dreht danach. Der Effekt liegt bei ≈2,5 bp hin und zurück.
- **Wichtig für SMC-Statistiken:** Die Tagesgrenze verändert die Stundenverteilung der Extreme. Für PDH/PDL eignet sich ein Server mit NY-Close (GMT+2/+3, D1-Kerze schließt 17:00 ET). Server mit GMT+0 erzeugen Sonntagskerzen.

### 3.3 Fixings und Rollover

- **WM/R 16:00 London.** Das Berechnungsfenster umfasst seit 2015 fünf Minuten (15:57:30–16:02:30).
  - Die Bewegung im Fix-Fenster ist an allen 11 getesteten Instrumenten größer als um 13:00. Bei GBPUSD ist sie 2,17×, bei EURUSD 1,34× so groß.
  - Am letzten Geschäftstag des Monats beträgt sie 10,1 bp statt ≈5,5 bp. Im Verhältnis zur 16:00-Ankerzeit ist sie 2,31× größer (Permutationstest p = 0,0007).
  - Spitzenreiter am Monatsende ist GBPUSD mit 13,67 bp gegenüber 6,09 bp an normalen Tagen.
  - Nach 60 Minuten werden am Monatsende im Mittel 2,71 bp zurückgegeben (t = 2,14, n = 17). An normalen Tagen gibt es keine Umkehr.
  - Hintergrund ist der Fixing-Skandal: 2014 Bußgelder von über 1,4 Mrd. USD (CFTC) und 1,7 Mrd. USD (FCA).
- **Tokio-Fix 9:55 JST (00:55 UTC) und Gotobi-Tage** (5., 10., 15., 20., 25., 30. des Monats). Japanische Importeure erzeugen USD-Nachfrage.
  - USDJPY steigt an Gotobi-Tagen in den Fix und fällt danach (Ito & Yamada, 1999–2013; Bessho et al. 2023).
  - In Praxis-Backtests ist der Effekt real, aber klein und out-of-sample instabil.
- **ECB-Fix 14:15 CET** und **LBMA-Gold-Auktion 15:00 London**.
  - Um 15:00 London bewegt sich Gold im Mittel um 18,38 bp, um 13:00 um 10,16 bp.
  - Das überlappt mit US-Daten um 10:00 ET.
- **Rollover 17:00 ET:** siehe Abschnitt 8.

### 3.4 Zeitumrechnung für den EA (ET)

„Normal“ heißt, USA und Europa haben dieselbe Sommerzeit-Phase. In den Versatzwochen ist der Abstand London–NY nur 4 Stunden. Das betrifft den 08.–28.03.2026, den **25.–31.10.2026 (nächste Woche)**, den 14.–27.03.2027 und den 31.10.–06.11.2027 (abgel.).

| Ereignis | Lokalzeit | ET normal | ET in Versatzwochen |
|---|---|---|---|
| Tokio-Open / Tokio-Fix | 09:00 / 09:55 JST | 20:00 / 20:55 (EDT); 19:00 / 19:55 (EST) | unverändert (Japan hat keine Sommerzeit) |
| UK-Daten / London-Open | 07:00 / 08:00 London | 02:00 / 03:00 | 03:00 / 04:00 |
| ECB-Entscheid und ECB-Fix | 14:15 CET | 08:15 | 09:15 |
| US-Daten (NFP, CPI) | 08:30 ET | 08:30 | 08:30 |
| BoC | 09:45 ET | 09:45 | 09:45 |
| LBMA Gold PM / WM/R | 15:00 / 16:00 London | 10:00 / 11:00 | 11:00 / 12:00 |
| FOMC-Statement | 14:00 ET | 14:00 | 14:00 |
| Rollover / Gold-Pause | 17:00 ET | 17:00–18:00 | 17:00–18:00 |

Weitere Zeiten:
- **RBNZ** entscheidet um 14:00 NZ. Ende Oktober entspricht das 21:00 ET am Vortag.
- **RBA** entscheidet um 14:30 Sydney, je nach Sommerzeit ≈22:30–00:30 ET.
- **BoJ** hat keine feste Uhrzeit, meist gegen Mittag JST (≈22–23 ET am Vortag).

In MQL5 gilt im Strategy Tester `TimeGMT()` = `TimeTradeServer()`. Die NY-Zeit muss deshalb aus der Serverzeit mit eigenen Sommerzeit-Regeln berechnet werden.

Quellen: [fxbacktest Volatilität/Stunde](https://fxbacktest.app/research/forex-volatility-by-hour/) · [fxbacktest Tageshoch/-tief](https://fxbacktest.app/research/when-daily-high-low-forms/) · [GoldSniper Stunden-Statistik](https://goldsnipersignals.com/xauusd-trading-hours/) · [Krohn/Mueller/Whelan](https://www.bankofcanada.ca/2021/10/staff-working-paper-2021-48/) · [fxbacktest London-Fix](https://fxbacktest.app/research/london-fix-month-end/) · [Wikipedia Forex-Skandal](https://en.wikipedia.org/wiki/Forex_scandal) · [Ito & Yamada (NBER)](https://www.nber.org/system/files/working_papers/w22820/w22820.pdf) · [Bessho et al. (arXiv)](https://arxiv.org/abs/2301.13204) · [Gotobi-Bot-Backtest (GitHub)](https://github.com/prathamesh-git9/gotobi-fx-bot) · [Admirals: Notenbank-Woche Oktober 2026](https://admiralmarkets.com/analytics/traders-blog/central-bank-super-week-october-2026) · [MQL5 TimeGMT](https://www.mql5.com/en/docs/dateandtime/timegmt)

---

## 4. Korrelations-Cluster und Exposure

Die Datenlage ist heterogen. Werte aus Kursniveaus überschätzen die Korrelation. Belastbar ist nur der 21-Tage-Renditen-Snapshot von FX Terminal (Stand 23.10.2026). Der EA sollte die Korrelationen selbst rollierend auf Renditen rechnen.

| Cluster | Mitglieder | Typische Korrelation (Quelle, Zeitraum) | Implikation |
|---|---|---|---|
| A „EUR/GBP gegen USD“ | EURUSD, GBPUSD, USDCHF (invers) | EURUSD–GBPUSD +0,93 (FX Terminal, 21 Tage); +0,85 (FXAbsolute, „Ø 2023–26“, Methode unklar); Spanne +0,75…+0,90 (TradingFinder). EURUSD–USDCHF −0,90 (FXAbsolute); −0,80…−0,95 (TradingFinder) | gleichgerichtet ≈ eine Position |
| B Antipoden | AUDUSD, NZDUSD, AUDJPY/NZDJPY, EURAUD/EURNZD, GBPAUD/GBPNZD | AUDUSD–NZDUSD +0,92 (FXAbsolute); +0,94 (TradingFinder, Februar 2025). AUDNZD–EURAUD −0,90; AUDCAD–EURAUD −0,80 (FX Terminal, 21 Tage). Für EURAUD/EURNZD keine Messung gefunden (Größenordnung hoch) | AUD und NZD als ein Block behandeln |
| C USD gesamt | 7 Majors + XAUUSD | EURUSD–AUDUSD +0,72 (FXAbsolute) gegenüber +0,30…+0,55 (TradingFinder) – widersprüchlich. EURUSD–USDJPY −0,80 (FXAbsolute) bzw. −0,64 (Dukascopy) | USD-Event trifft 8 Symbole |
| D JPY-Block | USDJPY + 6 JPY-Crosses | EURJPY–GBPJPY +0,95 (FX Terminal, 21 Tage); ≈+0,90 (Dukascopy). AUDJPY–EURJPY 0,954 und EURJPY–GBPJPY 0,854 (Myfxbook-Snapshot, Zeitrahmen unklar). AUDJPY–USDJPY +0,69 (21 Tage) | Risk-off oder Intervention bewegen alle gleichzeitig |
| E CHF-Block | USDCHF, EURCHF, GBPCHF, CADCHF, CHFJPY | USDCHF–GBPCHF ≈+0,90 (Dukascopy, ohne Zeitraum) | SNB-Risiko gebündelt |
| F CAD/Öl | USDCAD, EURCAD, GBPCAD, AUDCAD, CADJPY, CADCHF | USDCAD–AUDUSD −0,80 (FXAbsolute); ≈−0,85 (Dukascopy) | BoC, CAD-Daten und Öl gemeinsam |
| G Gold | XAUUSD | gegen EURUSD +0,55, AUDUSD +0,60, USDJPY −0,45 (FXAbsolute, Näherung). Laut WGC erklärte der FX-Faktor im ersten Halbjahr 2026 nur 14 % der Goldvarianz | teils eigenständiger Faktor |

### Vorschlag für Exposure-Limits (eigener Designvorschlag)

r bezeichnet das Risiko pro Trade, empfohlen sind 0,25–0,5 % des Equity.

1. **Leg-Zerlegung:** Jede Position bucht +r auf die gekaufte und −r auf die verkaufte Währung. Long XAUUSD bucht +r XAU und −r USD.
2. **Netto-Limit pro Währung:** |Σ| ≤ 2r. Das gilt ausdrücklich auch für USD und JPY.
3. **Brutto-Limit pro Währung:** ≤ 3r.
4. **Cluster mit |ρ| ≥ 0,8 (A, B, D):** höchstens eine Position je Richtung. Das Paar mit SMT-Bestätigung wird gehandelt, nicht beide.
5. **Portfolio-Heat:** Summe des offenen Risikos ≤ 4r. Das korrelationsbereinigte Risiko √(wᵀΣw) soll ≤ 2,5r sein, mit Σ aus 60 Tagen Renditen und täglichem Update.
6. **Event-Sperren gelten für den ganzen Cluster.** Bei Tier-1-USD-Events wird Cluster C komplett gesperrt, nicht nur das Ereignispaar.

Quellen: [FX Terminal (21 Tage Renditen, 23.10.2026)](https://fxterminal.app/correlation-matrix) · [FXAbsolute](https://fxabsolute.com/forex-correlation-table) · [TradingFinder](https://tradingfinder.com/education/forex/what-is-correlation-in-forex/) · [Dukascopy](https://www.dukascopy.com/swiss/english/marketwatch/articles/forex-correlation-pairs/) · [Myfxbook Korrelation](https://www.myfxbook.com/forex-market/correlation) · [WGC Mid-Year Outlook 2026](https://www.gold.org/goldhub/research/gold-mid-year-outlook-2026)

---

## 5. SMT-Divergenz-Paare und synthetischer DXY

**SMT-Paare innerhalb der Liste**, sortiert nach Kopplung:

1. **EURUSD / GBPUSD.** Klassiker. Mathematisch ist eine SMT-Divergenz hier gleichbedeutend mit einer Bewegung in EURGBP (EURGBP = EURUSD / GBPUSD).
2. **AUDUSD / NZDUSD.** Gleichbedeutend mit einer Bewegung in AUDNZD.
3. **EURJPY / GBPJPY** sowie **AUDJPY / NZDJPY.**
4. **EURUSD / USDCHF** (invertieren) und **EURUSD / DXY**.
5. **EURAUD / EURNZD** und **GBPAUD / GBPNZD.**
6. Schwächer gekoppelt: **USDCAD / AUDUSD** (invers, Öl-Treiber) und **XAUUSD / DXY**.

Bei SMT nur Swings auf zeitlich synchronisierten Bars vergleichen, mit einer Toleranz von ±k Bars. Inverse Paare werden über −ln(Preis) gespiegelt.

**ICE-DXY-Formel** (laut ICE FAQ seit der Euro-Einführung unverändert):
`USDX = 50,14348112 × EURUSD^−0,576 × USDJPY^0,136 × GBPUSD^−0,119 × USDCAD^0,091 × USDSEK^0,042 × USDCHF^0,036`

**Problem: USDSEK fehlt in der Liste.** Es gilt exakt USDSEK = EURSEK / EURUSD. Damit ist USDSEK^0,042 = EURSEK^0,042 × EURUSD^−0,042.

- **Variante A (empfohlen, abgel.).** EURSEK wird als konstant behandelt. Daraus folgt `DXY' = c × EURUSD^−0,618 × USDJPY^0,136 × GBPUSD^−0,119 × USDCAD^0,091 × USDCHF^0,036`.
  - Der Restfehler ist nur EURSEK^0,042. Eine Bewegung von 1 % in EURSEK verschiebt den Index um ≈0,04 %.
  - Myfxbook zeigt EURUSD–USDSEK bei −92,6 % bzw. −94,3 % (Snapshot, Zeitrahmen unklar).
  - Für SMT ist c beliebig. Man kann c = 1 setzen oder den Index auf 100 normieren.
- **Variante B.** SEK wird gestrichen und die Restgewichte durch 0,958 geteilt: EUR −0,601, JPY 0,142, GBP −0,124, CAD 0,095, CHF 0,038. Das ist schlechter, weil das SEK-Gewicht auf Währungen verteilt wird, die SEK weniger eng folgen.
- **Umsetzung.** Hochs und Tiefs eines Produkts sind nicht das Produkt der Hochs. Synthetische OHLC-Bars daher aus synchronisierten M1-Closes oder Ticks bilden; fehlende Bars mit dem letzten Wert auffüllen.
  - Bietet der Broker einen USDX/DXY-CFD, kann er als Referenz dienen. Zu beachten sind dann Futures-Rolls und die Pause von 17:00 bis 18:00 ET.

Quellen: [ICE Dollar Index FAQ](https://www.ice.com/publicdocs/futures_us/ICE_Dollar_Index_FAQ.pdf) · [Myfxbook USDSEK-Korrelation](https://www.myfxbook.com/forex-market/correlation/USDSEK)

---

## 6. Event-Risiken pro Währung

Die Leitzinsen stammen von Investing.com (Oktober 2026). Die Uhrzeiten sind Standardzeiten. Live liefert der MQL5-Kalender die Termine in Serverzeit. Dass die Kalenderfunktionen im Strategy Tester fehlen, ist verbreitete Praxis, wird in der Doku aber nicht explizit bestätigt. Für Backtests die Kalenderdaten daher exportieren.

| Währung | Wichtigste Events (ET) | Besondere Risiken |
|---|---|---|
| USD (4,00 %) | NFP und CPI 08:30; FOMC 14:00, Pressekonferenz 14:30; nächstes FOMC 27.–28.10.2026 | betrifft 8 Symbole inklusive Gold |
| EUR (2,65 %) | ECB 14:15 CET, Pressekonferenz 14:45; HICP-Flash; PMIs. ECB am 29.10. um 09:15 ET (Versatzwoche) | ECB-Fix |
| GBP (3,75 %) | BoE 12:00 London; UK-Daten 07:00 London (02:00 ET, also in der London-Killzone); nächster BoE-Termin widersprüchlich angegeben (29.10. bzw. 05.11.) | Flash-Crash 07.10.2016: GBPUSD −6 % in 2 Minuten |
| JPY (1,25 %) | BoJ ohne feste Uhrzeit (30.10.); Tokyo-CPI | Interventionen (Tabelle unten); Flash-Crash 2./3.01.2019: USDJPY und AUDUSD je über −4 % in Minuten, USDJPY-Tief ≈104,9 |
| CHF (0,00 %) | SNB quartalsweise 09:30 CET (nächste am 10.12.2026) | 2015: Franken intraday ≈+30 % gegen EUR, Schluss +23 %; Broker-Insolvenzen (Alpari UK; FXCM musste gestützt werden). 2025: CHF +12,7 % gegen USD |
| AUD (4,60 %) | RBA 14:30 Sydney (03.11.2026); AU-CPI und Arbeitsmarkt 11:30 Sydney; China-Daten | Asia-Feiertags-Liquidität |
| NZD (2,75 %) | RBNZ 14:00 NZ (28.10.2026, = 21:00 ET am 27.10.); NZ-CPI 10:45 NZ | dünner Markt |
| CAD (2,25 %) | BoC 09:45 ET, Pressekonferenz 10:30 (28.10.2026); CPI und LFS 08:30; EIA-Rohöl mittwochs 10:30 | Öl-Schocks |
| XAU | US-CPI, NFP, FOMC; Realzinsen und USD; Geopolitik (2026 US-Iran-Konflikt); Notenbankkäufe; LBMA 10:30 und 15:00 London | siehe Abschnitt 7 |

### Interventions-Historie

| Datum | Akteur | Volumen | Kontext |
|---|---|---|---|
| 06.09.2011 | SNB | „unbegrenzt“ | Mindestkurs EURCHF 1,20 eingeführt (EURCHF von 1,11 auf 1,20) |
| 15.01.2015 | SNB | – | Mindestkurs aufgehoben, Zins auf −0,75 % |
| 22.09.2022 | MoF (USD verkauft, JPY gekauft) | ¥2,84 Bio. | erste Intervention dieser Art seit 1998 |
| 21. und 24.10.2022 | MoF | ¥6,35 Bio. | USDJPY ≈152 |
| 29.04. und 01.05.2024 | MoF | ¥5,92 + ¥3,87 Bio. | nach Hoch bei 160,245 |
| 11.–12.07.2024 | MoF | ¥5,53 Bio. | USDJPY 161,76 → 157,30 |
| 30.04., 04.05., 06.05.2026 | MoF | ¥6,28 + ¥0,78 + ¥4,68 Bio. (Σ ¥11,73 Bio.) | nach Anstieg über 160 |
| 30.07.–26.08.2026 | MoF, am 31.07. gemeinsam mit dem US-Treasury | ¥15,40 Bio. (Monatsrekord) | erste gemeinsame Aktion seit 1998; USDJPY ≈164 → 155,20, bis 10.08. wieder ≈159 |

### Ausmaß von News-Bewegungen

fxbacktest misst die Range der Release-Stunde (H1, 2007–2026) als Vielfaches einer normalen Stunde:

| Event | EURUSD | USDJPY | Gold |
|---|---|---|---|
| Fed-Entscheid | 5,21× (Ø 73,2 Pips) | – | 3,27× |
| NFP | 2,69× (Ø 63,6 Pips) | 3,33× | 2,25× |
| CPI | 2,08× | 2,66× | – |

Bei NFP hält die Richtung der ersten 15 Minuten nach 4 Stunden in 72 % der Fälle (n = 36, M15 ab 2022).

### Wochenend-Gaps

fxbacktest, 835 Wochenenden 2010–2026, in Pips:

| Instrument | Median | 90. Perzentil | Maximum |
|---|---|---|---|
| EURUSD | 6,5 | 31,8 | 192,7 |
| USDJPY | 8,2 | 30,9 | 209,2 |
| EURJPY | 12,0 | 42,9 | 366,5 |
| GBPJPY | 15,6 | 51,0 | 332,4 |
| EURCHF | 5,9 | 21,8 | 128,7 |
| Gold | 0,96 USD | 5,61 USD | 112 USD |

Für Gold allein im Zeitraum 2024–2026: Median 8,36 USD, Mittel 19,16 USD, Maximum 153 USD (GoldSniper).

FX-Gaps schließen sich zu 86–91 % innerhalb von 24 Stunden. Die Kurse direkt nach der Wiedereröffnung sind verzerrt: Der Median-Gap ist negativ, die erste Stunde schließt zu 60–71 % höher. Die erste Stunde nach der Wiedereröffnung daher nicht für Levels und Stops verwenden.

Quellen: [Investing Leitzinsen](https://www.investing.com/central-banks/) · [FOMC-Kalender](https://www.federalreserve.gov/monetarypolicy/fomccalendars.htm) · [RBA-Termine](https://www.rba.gov.au/schedules-events/board-meeting-schedules.html) · [BoC 28.10.2026](https://www.bankofcanada.ca/2026/10/fad-announcement-release-mpr-2026-10-28/) · [MoF Juli/Aug. 2026](https://www.mof.go.jp/english/policy/international_policy/reference/feio/monthly/20260828e.html) · [MoF Q2 2026](https://www.mof.go.jp/english/policy/international_policy/reference/feio/quarter/2026_2Qe.html) · [MoF Q2 2024](https://www.mof.go.jp/english/policy/international_policy/reference/feio/quarter/2024_2Qe.html) · [MoF Q3 2024](https://www.mof.go.jp/english/policy/international_policy/reference/feio/quarter/2024_3Qe.html) · [CNBC 2024](https://www.cnbc.com/2024/05/31/japan-confirms-first-currency-intervention-since-2022.html) · [Japan Times August 2026](https://www.japantimes.co.jp/business/2026/08/29/markets/japan-record-forex-interventions/) · [Wikipedia: Intervention 2026](https://en.wikipedia.org/wiki/2026_U.S.%E2%80%93Japan_yen_intervention) · [Wikipedia Schweizer Franken](https://en.wikipedia.org/wiki/Swiss_franc) · [Wikipedia Flash Crash](https://en.wikipedia.org/wiki/Flash_crash) · [fxbacktest Wirtschaftsdaten](https://fxbacktest.app/research/economic-release-volatility/) · [fxbacktest Wochenend-Gaps](https://fxbacktest.app/research/weekend-gap-statistics/) · [MQL5 Kalender](https://www.mql5.com/en/docs/calendar)

---

## 7. XAUUSD im Detail

**Spezifikation**
- **Kontrakt:** Standard sind 100 oz pro Lot (IC, Exness, RoboForex). Es gibt Mini- und Mikro-Varianten mit 10 bzw. 1 oz (etwa XAUUSD.m oder .c), also bis zu Faktor 100 Unterschied bei der Größe.
- **Quote:** meist 2 Digits, manche Broker 3.
- **Symbolnamen:** GOLD, XAUUSD, mit Suffixen.
- **Hebel:** für EU- und AU-Retailkunden maximal 1:20.

**Spreads**
- IC Raw: 0,07 USD (Spec-Sheet) bzw. 0,09 USD (Spread-Seite), dazu 7 USD Round-Turn pro Lot (= 0,07 USD/oz).
- Pepperstone Razor: 0,10 USD im 30-Tage-Test.
- Dukascopy-Bankfeed (ohne Kommission): Ø 0,61 USD, je nach Stunde 0,55–0,74 USD. Am breitesten um 22–23 UTC.

**Volatilität** (Dukascopy M1, Juli 2024 bis Juli 2026)

| Zeitraum | Ø Tagesrange | Median |
|---|---|---|
| 2024 (ab Juli) | 34,8 USD | – |
| 2025 | 60,4 USD | – |
| 2026 YTD | 132,2 USD (2,83 % des Kurses) | 104,3 USD |

- Monatswerte 2026: Januar 160, Februar 168, März 182, April 114, Mai 98, Juni 112, Juli 87 USD.
- An 21,6 % der Tage lag die Range über 100 USD, an 4,3 % über 200 USD. Die größte Session-Range betrug 771 USD.
- Laut WGC: Allzeithoch intraday 5.595,47 USD am 29.01.2026, Tief 3.959,33 USD am 24.06.2026. Die realisierte Volatilität lag zeitweise über 50 %, danach unter 30 %; der 20-Jahres-Schnitt ist 17 %.
- Am 22.10.2026 betrug die Range ≈124 USD (Investing.com).

**Sessions**
- Spitzenstunden sind 13–14 UTC (Ø 21,8–22,2 USD) und 01 UTC (19,7 USD). Die Spitze um 01 UTC fällt plausibel mit der Eröffnung in Shanghai zusammen; diese Zuordnung ist eigene Einordnung.
- Die Asia-Range liegt im Median bei 27,42 USD.
- London durchbricht sie an 80,6 % der Tage, NY setzt in 69 % der Fälle fort.
- 50 % der Tagesrange sind bis 08 UTC erreicht, 80 % bis 13 UTC.

**Tagespause**
- IC: Handel 01:02–23:59 Serverzeit (freitags bis 23:57), Server GMT+2/+3. Die Pause liegt damit bei ≈17:00–18:00 ET.
- Pepperstone: Metalle 01:01–23:59.

**Warum SMC-Trader Gold bevorzugen** (datengestützt, soweit vorhanden)
- Große absolute Ranges bei kleinen relativen Kosten: Der Spread macht 0,3–1 % der ADR aus.
- Klare Abfolge von Asia-Range, London-Sweep und NY-Expansion: 80,6 % bzw. 69 %, siehe oben.
- Leichter Fortsetzungs-Bias: London-ORB 52,5 % (höchster Wert der Studie), Fortsetzung nach Asia-Break 53,7 % (p < 0,05, unkorrigiert).
- Starke und schnelle Reaktion auf US-Daten.
- Aber: Im Sweep/Reclaim-Test liegt Gold nur 2,8 Punkte über der Kontrolle, und das ist nicht signifikant.

**Risiken speziell für einen EA**
1. **Regime-Sprünge:** Die ADR hat sich binnen Monaten mehr als verdoppelt. Feste Punkt-Parameter fallen dabei aus.
2. **Positionsgröße:** Sie muss über `TICK_VALUE` und `TICK_SIZE` berechnet werden, nicht über eine angenommene Kontraktgröße.
3. **Kursnähe zu Stops:** Bei Kursen von 4.000–5.600 USD verfehlen Stop-Level- und Freeze-Level-Prüfungen in Punkten leicht ihr Ziel.
4. **Slippage bei Events:** Bei FOMC ist die Stundenrange 3,27× so groß wie normal.
5. **Gaps:** Wochenend-Gap bis 153 USD. Hinzu kommen Gap und Spread nach der täglichen Pause.
6. **Swaps:** Triple-Swap am Mittwoch, Swaps häufig negativ (beim Broker prüfen).
7. **USD-Kopplung:** Gold zählt bei Exposure-Limits zum USD-Cluster.

Quellen: [GoldSniper Volatilität](https://goldsnipersignals.com/xauusd-volatility/) · [GoldSniper Spreads](https://goldsnipersignals.com/xauusd-spread/) · [GoldSniper Handelszeiten](https://goldsnipersignals.com/xauusd-trading-hours/) · [WGC Mid-Year Outlook 2026](https://www.gold.org/goldhub/research/gold-mid-year-outlook-2026) · [Investing XAU/USD historisch](https://www.investing.com/currencies/xau-usd-historical-data) · [IC Handelszeiten](https://www.ic.com/en/trading-pricing/trading-hours) · [IC Gold (AU)](https://www.icmarkets.com.au/en/trade-gold) · [Pepperstone Commodities](https://pepperstone.com/en/markets/commodities/) · [fxbacktest London-ORB](https://fxbacktest.app/research/london-opening-range-break/)

---

## 8. Swap, Rollover und Spread-Ausweitung

**Swap**
- Der Swap entspricht der Zinsdifferenz zuzüglich Broker-Aufschlag. Er wird zum NY-Close (17:00 ET) belastet.
- Den Triple-Swap belastet IC für FX **und Metalle** in der Nacht zu Donnerstag (Mittwoch), wegen T+2-Valuta. Energie, Indizes und Krypto haben ihn am Freitag.
- Im EA nicht annehmen, sondern `SYMBOL_SWAP_ROLLOVER3DAYS` und `SYMBOL_SWAP_MODE` auslesen.
- Carry nach Leitzinsen (Investing.com, Oktober 2026): Positive Long-Carry haben vor allem AUDJPY, NZDJPY, GBPJPY, USDJPY, CADCHF und AUDNZD. Viele Paare sind wegen des Broker-Aufschlags auf beiden Seiten negativ.

**Spread-Ausweitung**
- EURUSD im Dukascopy-Feed: 0,31 Pips in aktiven Stunden, 2,24 Pips um 21 UTC.
  - Um 21 UTC frisst der Spread 27 % der Stundenrange, zwischen 12 und 15 UTC nur 1 %. Ein Entry um 21 UTC ist damit relativ ≈22-mal so teuer wie einer um 13 UTC.
- Andere Paare um 21 UTC (Spread als Anteil der Stundenrange): GBPJPY 69 %, EURJPY 49 %, USDJPY 45 %, GBPUSD 42 %, USDCAD 40 %, AUDUSD 31 %, Gold 25 %.
- Pepperstone Razor, EURUSD: 0,2 Pips in London, 1,4 Pips (max. 3,5) zum Rollover.
- 21 UTC entspricht 17:00 ET nur im US-Sommer. Im Winter liegt der Rollover bei 22 UTC.

**EA-Regeln**
- Zwischen 16:45 und 18:15 ET keine Entries.
- Pending Orders vor dem Rollover deaktivieren.
- Short-Stops werden auf dem Ask ausgelöst. Spread-Spitzen können sie auslösen, deshalb einen Puffer von mindestens 3× dem normalen Spread einplanen oder Stops spread-bewusst setzen.

Quellen: [IC Swap-Sätze](https://ic.com/global/en/trading-pricing/swap-rates) · [fxbacktest Spread-Kosten](https://fxbacktest.app/research/forex-spread-cost/) · [LowSpreadBroker](https://lowspreadbroker.com/artigos/pepperstone-spreads-review) · [Investing Leitzinsen](https://www.investing.com/central-banks/)

---

## 9. Eignung für SMC und Kosten

### 9.1 Was die Daten zeigen

Alle Studien stammen von fxbacktest und beruhen auf Dukascopy-Bid-Daten.

- **Sweep und Reclaim an PDH/PDL** (M15, 22 Instrumente, August 2022 bis August 2026, 11.990 Trades):
  - Trefferquote bei 1R: 48,67 % gegenüber 49,42 % in der Kontrolle (p = 0,11).
  - Kein Instrument übersteht die Bonferroni-Korrektur. Nominal am besten: AUDCAD +5,7 Punkte, EURUSD +3,5, Gold +2,8. Nominal am schlechtesten: USDCAD −4,5, GBPJPY −3,3.
  - Ungebestätigtes Fading bei Berührung: 40,9 % (z = −22,3).
  - Bei 2R: 30,8 % gegenüber einem fairen Wert von 33,3 %.
- **Asia-Range-Break** (Bruch als „Judas Swing“ oder Fortsetzung): Die 13 FX-Paare zusammen kommen auf 49,4 % Umkehr (p = 0,21).
  - Leichte Fortsetzungstendenz: EURJPY 54,2 %, Gold 53,7 %, GBPJPY 52,8 %.
  - Leichte Umkehrtendenz: EURCHF 51,5 %, USDCAD 50,9 % (nicht signifikant).
  - Beide Seiten der Asia-Range gebrochen (Studienzeitraum 2022–2026): CADCHF 57,8 %, EURCHF 55,3 %, EURUSD 48,5 %; bei AUDJPY nur 25,3 %.
- **London-ORB-Fortsetzung** (2010–2026, n ≈ 4.000 je Paar, Konfidenzintervall ≈±1,5 Punkte):
  - Oben: XAUUSD 52,5 %, USDJPY 52,5 %, GBPJPY 52,4 %, AUDJPY 52,1 %.
  - Unten: USDCAD 47,6 %, GBPCAD 48,8 %, AUDCAD 48,9 %, EURCHF 49,4 %.
- **Stop/Target auf H1:** Die Trefferquoten entsprechen dem Break-even S/(S+T) mit Abweichungen von höchstens 0,38 Punkten. Die Wahl des Chance-Risiko-Verhältnisses erzeugt also keine Kante.

**Einordnung als Proxy für „strukturtreu“ gegenüber „choppy“** (alle Effekte klein, ±2–3 Punkte):
- Eher strukturtreu: XAUUSD, USDJPY, GBPJPY, EURJPY, AUDJPY.
- Eher mean-reverting oder choppy: EURCHF, CADCHF, USDCAD, GBPCAD, AUDCAD. Bei AUDNZD stützt sich die Einordnung nur auf die niedrige ADR und die hohen Kosten, eine Studie dazu wurde nicht gefunden.

### 9.2 Hurst-Exponent

Hurst-Werte pro Paar habe ich nicht gefunden. Belegt sind nur:
- EURUSD: H ≈ 0,5 auf 10-Sekunden-Renditen über rollierende 30-Tage-Fenster (arXiv 1906.07834).
- EURGBP: H = 0,44 als illustrativer Wert (quantt, nicht als Messung ausgewiesen).

Empfehlung für den EA pro Symbol:
- DFA-Hurst auf H1-Log-Renditen (500 Bars)
- Variance Ratio VR(12) auf M5
- Kaufman Efficiency Ratio ER(20)

Diese Kennzahlen dienen als Regime-Filter und nicht als Kantenbehauptung.

### 9.3 Kostenkennzahl pro Paar (abgel.)

**Berechnung**
- All-in-Kosten = Raw-Spread + Kommission von 7 USD Round-Turn, umgerechnet in Pips mit den Pip-Werten aus Abschnitt 1. Das ergibt 0,70 Pips bei Quote USD, 1,10 bei JPY, 0,98 bei CAD, 0,58 bei CHF, 1,23 bei NZD und 1,00 bei AUD.
- Für die Majors ist der Pepperstone-Durchschnitt angesetzt, weil er konservativer ist.
- Die Umrechnung der ADR auf ATR(M5) und ATR(M1) in aktiven Stunden ist eine eigene Näherung. Grundlage ist das EURUSD-Overlap-Profil (26,1 Pips pro Stunde bei 90,7 Pips ADR), skaliert mit √t. So ist ATR(M5) ≈ 0,083 × ADR und ATR(M1) ≈ 0,037 × ADR.
- Für Asia-lastige Paare in der Asia-Session ist der Faktor kleiner. Die Werte dort sind also eher zu günstig angesetzt.

| Symbol | All-in (Pips) | Kosten/ADR 2025 | ≈ % ATR(M5) | ≈ % ATR(M1) | Kontrolle Dukascopy: Spread/Tagesrange | Klasse |
|---|---|---|---|---|---|---|
| USDJPY | 1,30 | 0,98 % | 12 | 26 | 0,74 % | A |
| GBPUSD | 0,90 | 1,00 % | 12 | 27 | 0,84 % | A |
| EURUSD | 0,80 | 1,07 % | 13 | 29 | 0,50 % | A |
| EURJPY | 1,40 | 1,09 % | 13 | 29 | 1,07 % | A |
| GBPJPY | 1,92 | 1,20 % | 14 | 32 | 1,52 % | A |
| XAUUSD | ≈0,17 USD | 0,28 % (2025) / 0,13 % (2026) | 3 / 2 | 8 / 3 | 2,44 %* | A |
| USDCHF | 0,78 | 1,26 % | 15 | 34 | – | B |
| AUDUSD | 0,80 | 1,40 % | 17 | 38 | 1,32 % | B |
| EURAUD | 1,80 | 1,50 % | 18 | 41 | – | B |
| GBPAUD | 2,06 | 1,51 % | 18 | 41 | – | B |
| CHFJPY | 1,96 | 1,56 % | 19 | 42 | – | B |
| AUDJPY | 1,60 | 1,65 % | 20 | 45 | 1,05 % | B |
| CADJPY | 1,58 | 1,65 % | 20 | 45 | – | B |
| USDCAD | 1,18 | 1,66 % | 20 | 45 | 1,67 % | B |
| EURCAD | 1,72 | 1,94 % | 23 | 52 | – | B |
| GBPCAD | 2,10 | 1,94 % | 23 | 52 | – | B |
| EURNZD | 2,55 | 1,98 % | 24 | 53 | – | B |
| NZDUSD | 1,08 | 2,00 % | 24 | 54 | – | B |
| NZDJPY | 1,70 | 2,02 % | 24 | 55 | – | B |
| GBPNZD | 3,21 | 2,18 % | 26 | 59 | – | C |
| GBPCHF | 1,68 | 2,27 % | 27 | 61 | – | C |
| EURCHF | 1,19 | 2,45 % | 30 | 66 | 2,08 % | C |
| CADCHF | 1,16 | 2,64 % | 32 | 71 | 2,97 % | C |
| AUDCAD | 1,66 | 2,91 % | 35 | 79 | 3,28 % | C |
| AUDNZD | 2,00 | 3,92 % | 47 | 106 | – | C (aus) |

\* Der Dukascopy-Wert für Gold ist auf die langfristige Range (≈27 USD seit 2009) bezogen. Mit der aktuellen ADR und dem Dukascopy-Spread von 0,61 USD ergeben sich ≈12 % von ATR(M5) im Jahr 2025 und ≈6 % im Jahr 2026.

**Klassen:**
- **A:** unter 15 % eines Stops von 1×ATR(M5). M1- und M5-Entries sind möglich.
- **B:** 15–25 %. Entries auf M5 mit Stop ≥ 1,5×ATR(M5) oder auf M15. Für M1 zu teuer.
- **C:** über 25 %. Nur M15 oder H1. Bei AUDNZD sind auch auf M15 noch ≈27 % fällig, daher nur H1-Swing oder deaktivieren.

Quellen: [fxbacktest Liquidity Grab](https://fxbacktest.app/research/liquidity-grab-win-rate/) · [fxbacktest Asia-Range](https://fxbacktest.app/research/asian-range-break/) · [fxbacktest London-ORB](https://fxbacktest.app/research/london-opening-range-break/) · [fxbacktest Stop/Target](https://fxbacktest.app/research/stop-target-hit-rates/) · [fxbacktest Spread-Kosten](https://fxbacktest.app/research/forex-spread-cost/) · [arXiv 1906.07834](https://arxiv.org/pdf/1906.07834) · [quantt Hurst](https://www.quantt.co.uk/resources/hurst-exponent-explained)

---

## 10. Empfehlungen

### 10.1 Parameter-Normalisierung

- **Einheiten:** Alles in Preis- bzw. ATR-Einheiten führen. ADR = ATR(D1, 20) mit NY-Close-Kerzen; dazu ATR(14) auf dem Entry-Timeframe. Pips nur für Logging.
- **Startwerte** (zu kalibrieren):

| Parameter | Startwert |
|---|---|
| Mindestgröße FVG | ≥ 0,3–0,5 × ATR(TF) und ≥ 3 × Spread |
| Displacement | Körper ≥ 1,2–1,5 × ATR(TF) |
| Sweep-Tiefe | ≤ 0,5 × ATR(D1); tiefere Sweeps gelten als Trendtag (Grenzwert wie in der fxbacktest-Studie) |
| SL-Puffer hinter dem Sweep-Docht | max(0,1 × ATR(M5); 2 × Spread) |
| ADR-Erschöpfung | kein neuer Trade, wenn die Tagesrange ≥ 90–100 % von ADR(20) ist und das Ziel außerhalb liegt |

- **Lot-Berechnung:**
  `lots = floor( Risiko_Geld / ((SL_Distanz / TICK_SIZE) × TICK_VALUE_LOSS) / VOLUME_STEP ) × VOLUME_STEP`
  Anschließend `VOLUME_MIN`, `STOPS_LEVEL` und `FREEZE_LEVEL` prüfen. Das deckt auch unterschiedliche Gold-Kontraktgrößen ab.
- **Kosten in Preis:** Spread + Kommission / (TICK_VALUE / TICK_SIZE) pro Lot.

### 10.2 Spread-Caps

- **Dynamischer Cap:** aktueller Spread ≤ 1,5–2 × Median des Spreads dieses Symbols zur selben Wochenstunde über die letzten 20 Handelstage. Der EA führt diese Statistik selbst.
- **Kosten-Cap:**
  - Tier 1: (Spread + Kommission) ≤ 15 % von ATR(M5) bei M5-Entries.
  - Tier 2: ≤ 20 %.
  - Tier 3: ≤ 15 % von ATR(M15).
- **Statischer Not-Cap:** ≈3 × typischer Raw-Spread aus Tabelle 1. Beispiele: EURUSD 0,6 Pips, GBPJPY 2,5 Pips, Gold 0,30 USD.

### 10.3 Handelsfenster in NY-Zeit

ICT-Killzones nach Konvention: Asia 20:00–00:00, London 02:00–05:00, NY AM 07:00–10:00.

| Gruppe | Primärfenster | Sekundärfenster |
|---|---|---|
| EURUSD, GBPUSD, USDCHF | London 02:00–05:00 | NY AM 08:30–11:00 |
| USDCAD, EURCAD, GBPCAD, CADCHF | NY AM 08:30–11:00 | London 03:00–05:00 |
| USDJPY und JPY-Crosses | Asia 19:00–22:00 (inklusive Tokio-Fix) | London 02:00–05:00, NY AM 08:30–10:30 |
| AUDUSD, NZDUSD, AUDJPY, NZDJPY, AUDCAD, AUDNZD | Asia 19:00–23:00 | London-Open 02:00–04:00 |
| EURAUD, EURNZD, GBPAUD, GBPNZD, EURCHF, GBPCHF | London 02:00–05:00 | – |
| XAUUSD | London 02:00–04:00, NY AM 08:20–11:00 | Asia 20:00–22:00 |

In den DST-Versatzwochen verschieben sich die europäischen Termine um +1 Stunde in ET.

**Globale Sperren**
- Rollover 16:45–18:15 ET.
- Am Monatsende 10:45–11:15 ET (WM/R-Fix).
- Tier-1-Events: −15 bis +30 Minuten. Bei Notenbanken der jeweiligen Währung −30 bis +60 Minuten.
- Freitags ab 12:00 ET keine neuen Trades.
- Montags die erste Stunde nach der Wiedereröffnung meiden.
- JPY-Interventionsmodus: Ab USDJPY ≥ 158 oder bei verbalen Warnungen des MoF keine neuen JPY-Shorts und halbe Positionsgröße. Grundlage sind die Interventionsniveaus 152, 160 und 164 der Jahre 2022–2026.

### 10.4 Tiering

| Tier | Symbole | Entry-Timeframe | Begründung |
|---|---|---|---|
| 1 Kern | EURUSD, GBPUSD, USDJPY*, EURJPY, GBPJPY, XAUUSD* | M1–M5 | Kostenklasse A, hohe Liquidität, leichter Fortsetzungs-Bias (JPY-Paare, Gold) |
| 2 selektiv | AUDUSD, USDCAD, USDCHF, AUDJPY, CADJPY, CHFJPY, EURAUD, GBPAUD, EURCAD, NZDUSD | M5–M15, maximal eine Position pro Cluster | Kostenklasse B; NZDUSD und USDCHF vor allem als SMT-Referenz |
| 3 Swing oder aus | GBPCAD, EURNZD, NZDJPY, GBPNZD, GBPCHF, EURCHF, CADCHF, AUDCAD, AUDNZD | M15/H1 oder deaktiviert | Kostenklasse C oder B mit Mean-Reversion-Tendenz; dünne Märkte (CAD- und CHF-Crosses) |

\* Mit Sonderregeln: Interventionsmodus für USDJPY, Regime- und Gap-Regeln für Gold.

### 10.5 Offene Punkte

- Die BIS-Anteile einzelner Crosses waren nicht belegbar.
- Hurst- und Trendpersistenz-Werte pro Paar waren nicht belegbar.
- Statistiken zur Uhrzeit von Tageshoch und -tief liegen nur für EURUSD und Gold vor.
- Die Spreads sind Brokerangaben, mit einer Ausnahme ohne Angabe des Zeitraums.
- Der EA sollte deshalb ab dem ersten Tag pro Symbol und Stunde Spread, Slippage, ATR und Korrelation protokollieren. Das Tiering sollte quartalsweise per Walk-Forward überprüft werden.
