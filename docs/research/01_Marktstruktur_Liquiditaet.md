<!-- Kapitel 1: Marktstruktur & Liquidität | Deep-Research-Rohbericht (Recherche-Agent), Stand 2026-10-24, unverändert übernommen -->

# Teilbereich: Marktstruktur & Liquidität – objektive Regeln für einen SMC/ICT-EA (MQL5)

**Hinweis zur Quellenlage:** ICT (Huddleston) hat selbst kein schriftliches Regelwerk veröffentlicht. Seine Aussagen unten stammen aus automatisch erzeugten Transkripten der 2022 Mentorship (Transkriptionsfehler möglich). Alle Glossare, „ICT“-Websites und Indikatoren sind Drittquellen. Bei Code (LuxAlgo, smartmoneyconcepts, MQL5-Artikel) habe ich die tatsächliche Logik gelesen. Wo ich selbst ableite oder etwas vorschlage, ist das als **eigene Ableitung** oder **Vorschlag** markiert. Das WebSearch-Budget der Session war gegen Ende aufgebraucht. Danach habe ich nur noch bekannte URLs per WebFetch gelesen. Zwei Punkte konnte ich deshalb nicht weiter absichern: weitere Quellen für Displacement-Schwellen und ICTs eigene Zahlen zu „relative equal highs“.

---

## 0. Kernentscheidungen (Kurzfassung)

1. **Pivots nur mit Bestätigungszeitpunkt speichern** (`tPivot` und `tConfirm`). Signale, Backtests und Strukturbrüche dürfen nur `tConfirm` verwenden.
2. **Zwei Swing-Erkennungen parallel laufen lassen:**
   - LuxAlgo-kompatible „Leg“-Pivots mit Länge 5 (internal) und 50 (swing/external).
   - ICT-Short-Term-Pivots (3-Candle, n=1) für den MSS-Trigger auf dem LTF.
3. **Brüche nur per Candle-Close** (BOS, CHoCH, MSS). **Liquidität gilt per Wick als genommen.** Ein Wick durch das Level mit Close zurück im Range ist ein **Sweep**, kein Break.
4. **MSS = CHoCH auf LTF + vorheriger Sweep (≤ 20 Bars) + Displacement.** Ein FVG im Leg ist optional als Pflicht einstellbar.
5. **Alle Toleranzen ATR-normiert**, nie in Pips. Grund: die 25 Instrumente mit JPY-Paaren und XAUUSD haben sehr unterschiedliche Preisskalen.
6. **Alle Session- und Tagesgrenzen in New-York-Zeit** mit eigener DST-Logik. Server-Zeit und `TimeGMT()` reichen im Tester nicht.

---

## 1. Swing-Punkte

### 1.1 Varianten im Vergleich

| Methode | Definition | Bestätigungs-Lag | Quelle |
|---|---|---|---|
| ICT STH/STL („3-Candle“) | High der mittleren Kerze > Highs beider Nachbarn | 1 Bar | ICT Ep. 3 (Transkript), Drittquellen |
| Bill-Williams-Fractal (MT5 `iFractals`) | 2 Bars je Seite. Code: `high[i]>high[i+1] && high[i]>high[i+2] && high[i]>=high[i-1] && high[i]>=high[i-2]` | 2 Bars | MT5-Code |
| Symmetrisches n-Bar-Fractal | n Bars links und rechts. MQL5-Artikel nutzen n=3…5. Part 39 hat eine Auto-Länge: ≤H1 5, ≤H4 7, ≤D1 9, sonst 11 | n Bars | MQL5-Artikel |
| Zentriertes Fenster (smartmoneyconcepts) | High = Maximum über `swing_length` Bars **vor und nach** der Kerze (Default 50, also Fenster 101). Danach werden aufeinanderfolgende gleichartige Swings entfernt; das extremere Pivot bleibt | 50 Bars, Lookahead im Code | GitHub |
| LuxAlgo „Leg“ (SMC v2) | `newLegHigh = high[size] > ta.highest(size)`. Eine Leg-Wechsel-Flanke erzeugt das Pivot. Swing 50 (Input, min 10), internal **fest 5** | `size` Bars | Pine-Quelle |
| MT5-ZigZag | Depth 12, Deviation 5 (**in Points**, `InpDeviation*_Point`), Backstep 3, `ExtRecalc=3` | variabel, **letzter Leg repaintet** | MQL5-Forum (Code) |
| ATR-, Prozent- oder Tick-Pullback | Neuer Swing erst nach Rücklauf ≥ 2.0×ATR(14), ≥ 30 % des Vor-Swings oder ≥ 80 Ticks (TradeDevils „PriceAction“-Modus) | variabel | TradeDevils-Doku |
| ICT-Hierarchie STH → ITH → LTH | Ein ITH ist ein STH mit niedrigeren STHs auf beiden Seiten. Ein LTH ist ein ITH mit niedrigeren ITHs auf beiden Seiten. Rekursiv, ohne Parameter | ITH: bis zum nächsten STH | Drittquellen (ictkillzone u. a.) |
| Validierungsfilter (MQL5 „Swing Extremes“ Teil 3) | Ein Swing ist gültig, wenn mindestens eins gilt: Range der Swing-Kerze > 1.5× mittlere Range(50); Sweep eines älteren Swings mit Close zurück; der Level hält 3 Bars | – | MQL5-Artikel |

### 1.2 LuxAlgo-Leg-Logik genau (eigene Ableitung aus dem Code)

Der Code prüft den Kandidaten `size` Bars zurück **nur gegen die nachfolgenden `size` Bars**. Ein Pivot entsteht nur beim Wechsel des `leg`-Zustands. Startzustand ist `BEARISH_LEG = 0`, bei einer Outside-Bar hat das Hoch Vorrang.

Daraus folgt:
- **H und L alternieren immer.**
- Das gemeldete Pivot-High ist das **höchste Hoch seit dem letzten Pivot-Low**.
- Der Algorithmus ist damit ein **zeitbasierter ZigZag**: Ein Extrem gilt als bestätigt, sobald es `size` Bars lang nicht überboten wurde.
- Es gibt **keine Mindest-Amplitude**. Eine flache Seitwärtsphase kann deshalb Pivots erzeugen.

Weitere Details aus dem Code:
- Brüche: `ta.crossover(close, level) and not crossed`. Es gibt also genau **einen Bruch pro Pivot**.
- Ohne neues Pivot „friert“ die Struktur ein, auch wenn der Kurs weiterläuft.
- Das Script nutzt kein `barstate.isconfirmed`. Auf der Realtime-Bar können Brüche intrabar erscheinen und wieder verschwinden. Die MQL5-Portierung von GeneralTradingSarl übernimmt deshalb nur geschlossene Bars.

### 1.3 Lag, Repainting, Lookahead

- **Ein Pivot ist erst `n` Bars nach der Pivot-Bar bekannt.** Ein negativer Plot-Offset verschiebt nur die Zeichnung, nicht den Wissenszeitpunkt (PineConnector, Pineify).
- **Messbarer Effekt des Lookaheads:** Issue #101 bei smartmoneyconcepts zeigt das zentrierte Fenster bei XAUUSD M15 über 10 Jahre:

  | Variante | Trades | Winrate | Profit Factor |
  |---|---|---|---|
  | Zentriertes Fenster | 177 | 81.4 % | 7.32 |
  | Kausale Bestätigung | 106 | 52.8 % | 1.82 |

- **Zwei weitere Lookahead-Stellen in derselben Library (eigene Code-Analyse):**
  - `liquidity()` berechnet die Bandbreite aus Gesamt-High und Gesamt-Low des **ganzen** Datensatzes.
  - `bos_choch()` klassifiziert über ein 4-Swing-Muster, dessen letzter Swing erst nach dem Bruch bestätigt ist.
- **ZigZag:** Nur der letzte Leg repaintet. Abgeschlossene Legs sind fix.
- **MT5-Fractals:** Bars ab `rates_total-3` sind final.
- **MQL5-spezifisch:**
  - Bar 0 nie für Signale verwenden. Auf HTF immer Index 1 lesen.
  - Logik nur bei neuer Bar ausführen.
  - Im Artikel MQL5 #19365 liegt das Fractal-Fenster bei Zentrum `p` auf der offenen Bar 0. Das ist ein Bug; das Zentrum muss bei `p+1` liegen.

### 1.4 Empfehlung

| Rolle | Methode | Lag |
|---|---|---|
| Internal | LuxAlgo-Leg mit L=5 | 5 Bars |
| External/Swing | LuxAlgo-Leg mit L=50 (Parität zu TradingView) | 50 Bars |
| MSS-Trigger auf LTF | ICT-STH (Fractal n=1, Tie-Regel wie MT5: rechts strikt, links ≥) | 1 Bar |

- **Optional:** ein Amplitudenfilter. Ein Pivot zählt nur als „strukturell“, wenn `|P − letzter Gegenpivot| ≥ k·ATR(14)`, mit **Vorschlag** k_int 0.5 und k_ext 1.5.
- **ZigZag mit Deviation in Points:** nicht verwenden. Er ist nicht skalenneutral über die 25 Symbole.

**Quellen:**
- LuxAlgo SMC v2 (Pine-Quelle): https://c.mql5.com/21/592/text.txt?d=1
- LuxAlgo SMC v1 (Gist): https://gist.github.com/niquedegraaff/8c2f45dc73519458afeae14b0096d719
- LuxAlgo Market-Structure-Doku: https://docs.luxalgo.com/docs/algos/price-action-concepts/market-structures
- MQL5-Portierung von LuxAlgo: https://github.com/GeneralTradingSarl/Smart-Money-Concepts
- smartmoneyconcepts (`smc.py`): https://raw.githubusercontent.com/joshyattridge/smart-money-concepts/master/smartmoneyconcepts/smc.py
- smartmoneyconcepts Issue #101: https://github.com/joshyattridge/smart-money-concepts/issues/101
- MT5-Fractals (Hilfe): https://www.metatrader5.com/en/terminal/help/indicators/bw_indicators/fractals
- MT5-Fractals (Code-Zitat im Forum): https://www.mql5.com/en/forum/191698
- MT5-ZigZag (Forum, Code): https://www.mql5.com/en/forum/372849 und https://www.mql5.com/en/forum/442175
- ICT-Hierarchie STH/ITH/LTH: https://www.ictkillzone.com/ict-swing-point-hierarchy
- TradeDevils-Doku: https://tradedevils-indicators.com/pages/tdu-market-structure-smart-money-concepts-docs
- MQL5-Artikel: https://www.mql5.com/en/articles/19365, https://www.mql5.com/en/articles/21888, https://www.mql5.com/en/articles/22363
- Pivot-Timing in Pine: https://www.pineconnector.com/blogs/pico-blog/pine-script-pivothigh-pivotlow-repainting

---

## 2. Struktur-Klassifikation, Trend-Zustandsautomat, Strong/Weak/Protected

### 2.1 HH/HL/LH/LL

- Ein neues Pivot wird mit dem **vorherigen Pivot gleichen Typs** verglichen (LuxAlgo-Labels).
- Liegt der Unterschied innerhalb der EQ-Toleranz (Abschnitt 4.2), labelt der EA es als **EQH/EQL statt HH/LH** (**Vorschlag**). Das vermeidet Flackern zwischen HH und LH.

### 2.2 Wie der Trend bestimmt wird – widersprüchliche Modelle

| Modell | Trendlogik | Quelle |
|---|---|---|
| **Event-basiert** | Trend = Richtung des letzten Close-Bruchs. Unbekannter Trend wird beim ersten Bruch BOS | LuxAlgo, MQL5 „Sentinel“ |
| **Muster-basiert** | 4-Swing-Muster | smartmoneyconcepts |
| **Muster-basiert** | Letztes Swing-Paar | MQL5 „Sentinel“ |
| **Muster-basiert** | Regressionssteigung über 5 Highs und 5 Lows, mit Hysterese | MQL5 „Hierarchical“ |

**Empfehlung:** event-basiert. Das ist kausal und ohne Lookahead. Die Labels dienen nur zur Information.

### 2.3 Internal vs. External

Auch hier gibt es drei Lesarten:
- **LuxAlgo:** Zwei Pivot-Sätze auf **demselben** Timeframe (5 vs. 50).
  - Ein interner Bruch wird ignoriert, wenn der interne Level gleich dem Swing-Level ist.
  - Der optionale Confluence-Filter vergleicht Dochtgrößen und ist per Default aus. Die Klammerung `math.min(close, open - low)` wirkt wie ein Präzedenzfehler (**eigene Beobachtung**) und sollte nicht übernommen werden.
- **MQL5 „Hierarchical Framework“:** internal = Chart-TF, external = HTF (Default H4). Swing-Stärke internal 5, external 8.
- **TradeDevils und writofinance:** internal = Highs und Lows zwischen dem jüngsten Swing-High und Swing-Low („minor“ vs. „major“).

### 2.4 Strong/Weak und Protected – drei inkompatible Definitionen

1. **LuxAlgo (trendbasiert):**
   - Code: `swingTrend.bias == BEARISH ? 'Strong High' : 'Weak High'`.
   - Das Label gilt für die *trailing extremes*. Diese werden bei jedem neuen Swing-Pivot auf dessen Level zurückgesetzt und danach mit `max(high)` bzw. `min(low)` erweitert.
2. **Strukturell (TradeDevils, Altrady, TradingView-Ideen):**
   - **Strong Low:** Danach entstand ein neues Hoch. Es ist der Low, der den BOS „verursacht“ hat.
   - **Weak Low:** der jüngste Low ohne neues Hoch danach. Weak-Levels gelten als Ziele, Strong-Levels als geschützt.
3. **Protected Low:**
   - writofinance: „most recent higher low“, unabhängig davon, ob ein BOS folgte.
   - Alternativ im CISD-Kontext: das Extrem der Sweep-Kerze.
   - Abweichend davon: LuxAlgo Price Action Concepts (kostenpflichtig) nutzt **Volumen**, Trader-Dale die **Rejection-Stärke**.

**Empfehlung (objektiv):** `protectedLow` wird beim bullischen Swing-BOS gesetzt, gespiegelt für bärisch:

```
protectedLow = min(Low) zwischen Pivot-Bar des gebrochenen Hochs und Bruch-Bar
```

Dieser Wert ist ab dem Bruch bekannt, also kausal. Den Swing-Trend kippt nur ein Close jenseits von protectedLow/High („strict CHoCH“). Den LuxAlgo-CHoCH (Bruch des jüngsten Swing-Pivots) führt der EA zusätzlich als Frühwarnung.

### 2.5 Zustandsautomat (Vorschlag)

- Zustände je Ebene: `UNKNOWN → BULL | BEAR`, plus Flag `TRANSITION`.
- Das Flag wird gesetzt, wenn ein interner CHoCH gegen den Swing-Trend läuft.
- Es wird gelöscht bei einem internen BOS in Trendrichtung oder bei einem Swing-CHoCH.
- `UNKNOWN` bleibt bis zum ersten Swing-Bruch nach der Warm-up-Phase bestehen. In `UNKNOWN` handelt der EA nicht.
- **CHoCH+ (LuxAlgo, „supported“):** Vor dem CHoCH gab es ein gescheitertes HH bzw. ein LH im Aufwärtstrend. Das ist trivial aus den Labels ableitbar.

**Quellen:**
- LuxAlgo Pine-Quelle: https://c.mql5.com/21/592/text.txt?d=1
- LuxAlgo PAC-Settings: https://docs.luxalgo.com/platform/algos/price-action-concepts/settings
- TradeDevils-Doku: https://tradedevils-indicators.com/pages/tdu-market-structure-smart-money-concepts-docs
- writofinance (Module 2): https://www.writofinance.com/module-2-reading-ict-market-structure/
- Protected High/Low (CISD): https://www.smartmoneytrader.co/blog/what-is-protected-high-low-ict
- Altrady: https://www.altrady.com/crypto-trading/smart-money-concept/market-structure-in-smart-money-trading
- TradingView (Strong/Weak): https://www.tradingview.com/chart/BTCUSD/qjZOwOYy-STRONG-WEAK-HIGHS-LOWS/
- Trader-Dale: https://www.trader-dale.com/price-action-strong-or-weak-highs-and-lows/
- MQL5 „Hierarchical Framework“: https://www.mql5.com/en/articles/23049
- MQL5 „Market Structure Sentinel“: https://www.mql5.com/en/articles/22249

---

## 3. BOS vs. CHoCH vs. MSS, Sweep vs. Break, Inducement

### 3.1 Definitionsvergleich

| Quelle | BOS | CHoCH | MSS |
|---|---|---|---|
| LuxAlgo (Code und Doku) | Close-Crossover in Trendrichtung | Close-Crossover gegen den bisherigen Bias. Doku nennt CHoCH auch „market structure shift“ | = CHoCH |
| theinnercircletraders.com (Glossar, Drittquelle) | Close jenseits des jüngsten Swings | „close back through a recently swept structural extreme … Wicks do not count“ | „daily-level“, Swing-Bruch auf **D1/H4** |
| ICT 2022 Ep. 2/3/6 (Transkript) | – („break in market structure“ ist bei ihm die längerfristig relevantere **Umkehr**) | – | Nach Raid über alte Hochs „quickly shift lower“. Kurzfristiges Tief wird mit Displacement gebrochen. „this is all time frames“; intraday auf 15m/5m/1m |
| innercircletrader.net | mit Trend | jüngster Gegenswing, „softer warning“ | Gegenswing **mit Displacement**, „wait for the body close“, „a wick poke is not an MSS“. Ein FVG nur „ideally“ |
| backtrex | ohne Displacement möglich | moderates Displacement | starkes Displacement **plus** klares FVG |
| algostorm | – | CHoCH und MSS sind synonym | – |
| writofinance | Close **und** vorheriger Liquidity Grab | Bruch des jüngsten Swing-Lows bzw. -Highs | – |

**Widersprüche:**
- MSS als LTF-Event (ICT selbst) gegenüber MSS als D1/H4-Event (Glossar).
- ICTs „break in market structure“ meint eine Umkehr, SMCs „BOS“ meint Fortsetzung.

**Empfehlung:**
- BOS und CHoCH nach LuxAlgo-Semantik.
- **MSS = (interner oder STH-) CHoCH + Sweep davor + Displacement.**
- Ein HTF-CHoCH heißt im EA „Swing-CHoCH“, nicht MSS.

### 3.2 Close vs. Wick

- **Close für Brüche:** Mehrheitlich so umgesetzt bei LuxAlgo, im MQL5-„Sentinel“ und in Part 39, bei WillyAlgo (Default close) und TradeDevils (`Candle_Close`). In smartmoneyconcepts ist es der Default `close_break=True`.
- **Ausnahme:** Das MQL5-„Hierarchical Framework“ bricht per Wick und listet das selbst als Schwäche.
- **ICT macht dieselbe Trennung, wie der EA sie braucht:**
  - Liquidität nehmen braucht keinen Close: „it does not need to close above that“ (Ep. 3).
  - Für den MSS will er einen Close: „a wick and come back up … not all that convincing“ und „it has absolutely displaced and then the candle closed“ (Ep. 6).
- **Bruch-Puffer:**
  - LuxAlgo: 0 (`close > level`).
  - **Vorschlag:** optional `brkBuf = 0.05–0.1·ATR(14)` gegen 1-Tick-Brüche.

### 3.3 Displacement messbar machen

Bausteine aus den Quellen:

| Quelle | Kriterium |
|---|---|
| backtrex | Body/Range ≥ 0.6, Dochte < 20 % der Range |
| LuxAlgo Trendline Liquidity | Displacement-Multiplikator 1.0·ATR |
| MQL5 „Swing Extremes“ | Range > 1.5× mittlere Range(50) |
| WillyAlgo | „Require Displacement“ = FVG im Leg von Sweep bis CHoCH, Mindestgröße 0.2·ATR(50) |
| ICT (Ep. 6) | „quick“ = Displacement. Für die Schnelligkeit gibt es **keine Zahl** |

**Vorschlag (Komposit):** Im Leg vom Sweep-Extrem bis zur Bruch-Bar gibt es mindestens eine Kerze in Bruchrichtung mit `body ≥ 0.6·range` **und** `range ≥ 1.0·ATR(14)`. Zusätzlich optional ein FVG ≥ 0.2·ATR(50) im Leg.

### 3.4 Sweep vs. echter Break

- **Wick-Sweep:** Wick über bzw. unter den Level, Close zurück im Range. WillyAlgo verlangt das auf derselben Bar; ein Close jenseits zählt dort als „taken without sweep“.
- **Outbreak & Retest** (LuxAlgo Liquidity Sweeps): Close durch den Level, Retest, Wick in Gegenrichtung.
- **LuxAlgo Trendline Liquidity:** Reclaim innerhalb von 8 Bars gilt als Sweep. Drei „Acceptance Closes“ gelten als Break.
- **Achtung smartmoneyconcepts:** `Swept` heißt dort schon „High erreicht die Band-Oberkante“. Das ist eine Berührung, kein Reclaim.
- **Terminologie:** Raid, Stop Hunt, Run und Sweep werden in der Literatur praktisch synonym benutzt.

**Vorschlag:** Der EA unterscheidet nur nach dem **Ergebnis**:
- `SWEPT` = Reclaim innerhalb von `nReclaim` Bars. Default 1, bzw. ≤ 3 als „failed break“.
- `BROKEN` = `nAccept` Closes jenseits. Default 2.
- In **beiden** Fällen ist der Pool als Ziel verbraucht. Das folgt ICTs „Liquidität ist genommen“.

### 3.5 Inducement (IDM)

Drei Varianten in den Quellen:
- **(A) writofinance:** der **erste Pullback nach** BOS/CHoCH. Sein Orderblock gilt als ungültig. Erst der Sweep des IDM macht den POI gültig.
- **(B) AlgoKings und innercircletrader.net:** der erste **gültige** Pullback **innerhalb des Legs**, der den BOS erzeugt hat.
  - Validierung bei innercircletrader.net, bullischer Leg: Man markiert die höchste bullische Kerze vor dem Pullback. Deren Low muss per Wick genommen werden. Danach muss ein **Close** über ihr High folgen.
- **(C) LuxAlgo-Konzeptseite, „strict“:** der jüngste interne Pullback **vor dem Swing-Extrem bzw. vor dem POI**. Dieselbe Seite nennt im Identifikationsschritt aber den „first minor pullback“. Sie ist also selbst uneindeutig.

Weitere Punkte:
- Ob „Swing erst nach IDM-Sweep bestätigt“ gilt, ist stilabhängig (writofinance-Seite zur Dealing Range).
- PocketOption warnt, dass die meisten Pullbacks einfach Pullbacks sind.

**Empfehlung:** Variante (A) als Default, (B) als Option. Der IDM ist das erste interne Pivot-Low nach dem bullischen Swing-BOS. Ein POI gilt erst nach einem Wick unter den IDM als „armed“.

**Quellen:**
- LuxAlgo Pine-Quelle: https://c.mql5.com/21/592/text.txt?d=1
- ICT Ep. 2: https://sozai.app/transcript/2022-ict-mentorship-episode-2/
- ICT Ep. 3: https://sozai.app/transcript/2022-ict-mentorship-episode-3/
- ICT Ep. 6: https://sozai.app/transcript/2022-ict-mentorship-episode-6/
- ICT Sharks Forum (Ep. 6): https://forum.ictsharks.com/t/2022-ict-mentorship-episode-6-market-efficiency-paradigm-institutional-order-flow/151
- theinnercircletraders.com Glossar: https://www.theinnercircletraders.com/wp-content/uploads/2026/08/ICT-Trading-Glossary.pdf
- innercircletrader.net MSS: https://innercircletrader.net/tutorials/ict-market-structure-shift/
- backtrex Displacement: https://backtrex.com/en/blog/ict-displacement-candle-market-concept
- algostorm: https://algostorm.com/ict-smc-key-concepts/
- WillyAlgoTrader (ICT Structure Engine): https://www.tradingview.com/script/4Y1T9TrB-ICT-Structure-Engine-WillyAlgoTrader/
- LuxAlgo Liquidity Sweeps: https://www.luxalgo.com/library/indicator/liquidity-sweeps/
- LuxAlgo Trendline Liquidity: https://www.luxalgo.com/library/indicator/trendline-liquidity/
- writofinance Structure Mapping: https://www.writofinance.com/structure-mapping-in-trading/
- writofinance Inducement: https://www.writofinance.com/inducement-in-forex-trading/
- LuxAlgo Inducement: https://www.luxalgo.com/library/concept/inducement/
- AlgoKings Inducement: https://www.algokings.net/learn/inducement-explained/
- innercircletrader.net Valid Pullback: https://innercircletrader.net/tutorials/3-step-guide-to-master-valid-pullback/

---

## 4. Liquidität

### 4.1 Pool-Typen – objektive Definition

| Typ | Seite | Definition für den EA | Quelle |
|---|---|---|---|
| Swing-Pool (internal/external) | BSL über Hoch, SSL unter Tief | Bestätigtes Pivot, Preis = Wick | ICT: „Above old highs, buy stops. Below old lows, sell stops.“ (Ep. 2) |
| EQH/EQL | BSL/SSL | ≥ 2 bestätigte Pivots innerhalb der Toleranz, mit echtem Pullback dazwischen | LuxAlgo, Glossar |
| Trendline-Liquidity | diagonal | Pivot-Länge 10, ≥ 3 Touches, Touch-Toleranz 0.25·ATR(200), Reclaim-Fenster 8 Bars, 3 Acceptance-Closes, Linie muss geneigt sein | LuxAlgo-Defaults |
| Session-H/L | beide | Siehe 4.3 | |
| PDH/PDL, PWH/PWL, PMH/PML | beide | Vorperiode (LuxAlgo: `request.security(..., [high[1], low[1]], lookahead_on)`) | LuxAlgo-Code |
| IPDA 20/40/60 | beide | Hoch und Tief der letzten 20/40/60 Handelstage | FibAlgo, itradesize |
| „Old highs/lows“ | beide | Bei ICT nur qualitativ: „large fund traders … looking at these old lows and old highs“ (Ep. 2). **Vorschlag:** External-Pivot auf D1/H4, seit ≥ 20 Bars unberührt | |

**IPDA-Widerspruch:** Rollierende, überlappende Fenster gegenüber drei getrennten 20-Tage-Blöcken (Aron Groups).

### 4.2 Toleranz für EQH/EQL – sehr unterschiedliche Werte

| Quelle | Toleranz | Bemerkung |
|---|---|---|
| LuxAlgo | `abs(Δ) < 0.1·ATR(200)` | Eigene Pivots mit Länge 3; nur mit dem **vorherigen** EQ-Pivot verglichen |
| WillyAlgo | 0.1·ATR | |
| homirana (MQL5 Code Base) | 0.5·ATR(14) | Pivot-Länge 5 |
| TradeDevils | 2 Ticks | |
| smartmoneyconcepts | 1 % der Gesamt-Range | mit Lookahead |
| Educators | 2–5 Pips (x10hop), 5–10 Pips (ictkillzone), 10–20 Pips (quantum-algo) | |
| ICT („relative equal highs“, Ep. 2/3) | **keine Zahl** | |

Zusätzliche Kriterien aus der LuxAlgo-Konzeptseite: ein „meaningful pullback“ zwischen den Touches, und eine Toleranz als Band statt Punkt.

**Vorschlag:**
- `tolEQ = 0.1·ATR(200)` des Pivot-Timeframes, Optimierungsbereich 0.05–0.25.
- „Relative EQ“ = 0.25·ATR(200), separat gekennzeichnet.
- Mindestabstand zwischen den Touches ≥ 2·L_eq Bars.
- Pullback zwischen den Touches ≥ 0.5·ATR(14).
- Pool-Preis = das extremste Member (für BSL das höchste).

### 4.3 Sessions und Tagesgrenzen (immer New-York-Zeit)

**Killzones (Mehrheitsmeinung):**

| Fenster | Zeit (NY) |
|---|---|
| Asia | 20:00–00:00 |
| London | 02:00–05:00 |
| NY AM | 07:00–10:00 |
| London Close | 10:00–12:00 |
| NY PM (WillyAlgo) | 13:30–16:00 |

**Abweichungen:**
- Asian Range 20:00–02:00 (theinnercircletraders-Glossar).
- Asia 19:00–22:00 (ictkillzone).
- NY 08:00–11:00 (EBC).
- ICT selbst handelt Indizes „8:30 … to 11:00“ (Ep. 2).
- smartmoneyconcepts nutzt **feste UTC-Fenster ohne DST**, nämlich London 07–16 und NY 13–22. Für Forex ist das falsch.

**Tagesgrenze:**
- ICT „Midnight Open“ = 00:00 NY.
- „True Day Open“ ist widersprüchlich: 00:00 laut ictkillzone, 18:00 laut GrandAlgo und FibAlgo.
- Der Forex-D1 beim Broker endet üblicherweise um 17:00 NY. Das ist bei GMT+2/+3-Servern verbreitet, aber **broker-abhängig und zu verifizieren**.
- GrandAlgo fand im Test über 3 Jahre **keinen** Vorteil des Midnight Open gegenüber einem Kontroll-Level.

**MQL5-Fallstrick:** Laut Doku gilt: „During testing in the strategy tester, TimeGMT() is always equal to TimeTradeServer()“. Der EA braucht deshalb einen eingebauten Server-Offset und DST-Regeln:
- US: zweiter Sonntag im März bis erster Sonntag im November.
- EU: letzter Sonntag im März bis letzter Sonntag im Oktober.
- Daraus entstehen Mismatch-Wochen, z. B. **25.10.–01.11.2026**.

### 4.4 IRL vs. ERL, Draw on Liquidity

- **ERL:** Liquidität jenseits der Extreme der Dealing Range. Darüber besteht Einigkeit.
- **IRL – Widerspruch:**
  - Nur FVGs (innercircletrader.net).
  - FVG plus OB plus minor EQH/EQL (LuxAlgo).
  - ICT selbst (Ep. 3): „internal range liquidity is looking for short-term lows or short-term highs“.
- **Rotation (Heuristik, keine Regel):** ERL genommen, dann IRL als Ziel. IRL gefüllt, dann die gegenüberliegende ERL. Ausnahme ist ein echter Breakout.
- **Draw on Liquidity:** ICT: „It's drawing to stops, which is liquidity, or it's running to an imbalance“ (Ep. 2).
- **LuxAlgo-Rangfolge** (qualitativ):
  - HTF-Pools vor LTF-Pools.
  - Engineered EQH/EQL vor einzelnen Swings.
  - Unberührte Pools vor angetesteten.
  - Richtung muss zur HTF-Struktur passen.
  - Genau **ein** aktives Ziel; Setups dagegen werden übersprungen.
- **Daily-Bias-Regeln** (WillyAlgo, TTrades, ScalperIntel; vorheriger Tag):

  | Vorheriger Tag | Bias |
  |---|---|
  | Close > PDH | bullisch |
  | Close < PDL | bärisch |
  | Nur PDH genommen, Close innen | bärisch |
  | Nur PDL genommen, Close innen | bullisch |
  | Beide Seiten genommen oder Inside Day | neutral |

  Alternative bei innercircletrader.net: Close relativ zum Mittelpunkt des Vortags.

**Quellen:**
- theinnercircletraders.com Glossar: https://www.theinnercircletraders.com/wp-content/uploads/2026/08/ICT-Trading-Glossary.pdf
- LuxAlgo EQH/EQL als Liquidität: https://www.luxalgo.com/library/concept/equal-highs-lows-as-liquidity/
- homirana SMC (MQL5 Code Base): https://www.mql5.com/en/code/71497
- x10hop: https://x10hop.com/concepts/relative-equal-highs-lows/
- ictkillzone EQH/EQL: https://www.ictkillzone.com/ict-equal-highs-lows
- LuxAlgo Trendline Liquidity: https://www.luxalgo.com/library/indicator/trendline-liquidity/
- ChartingLens Kill Zones: https://chartinglens.com/blog/ict-kill-zones-guide
- ictkillzone Kill Zones: https://www.ictkillzone.com/ict-kill-zones
- ictkillzone Midnight Open: https://www.ictkillzone.com/ict-midnight-open
- GrandAlgo Midnight Open: https://grandalgo.com/blog/ict-midnight-open-true-day
- MQL5 `TimeGMT`: https://www.mql5.com/en/docs/dateandtime/timegmt
- FibAlgo IPDA: https://fibalgo.com/library/ict-ipda-data-range
- Aron Groups IPDA: https://arongroups.co/technical-analyze/understanding-how-ipda-frames-liquidity-imbalance-and-institutional-price-delivery/
- LuxAlgo IRL/ERL: https://www.luxalgo.com/library/concept/internal-vs-external-range-liquidity/
- innercircletrader.net IRL/ERL: https://innercircletrader.net/tutorials/ict-internal-external-liquidity/
- LuxAlgo Draw on Liquidity: https://www.luxalgo.com/library/concept/draw-on-liquidity/
- TTrades Daily Bias: https://ttrades.com/ict-daily-bias-most-simple-mechanical-framework/
- ScalperIntel: https://scalperintel.com/blogs/hub/ict-bias-the-higher-timeframe-directional-edge-that-ties-everything-together

---

## 5. Dealing Range, Equilibrium, Premium/Discount

**Varianten für die Ankerpunkte:**
- **(a) LuxAlgo (Code):** `[trailing.bottom, trailing.top]`. Die Werte werden bei jedem neuen Swing-Pivot auf dessen Level gesetzt und danach mit neuen Extremen erweitert. Das ist praktisch der **jüngste externe Leg plus Erweiterung**.
- **(b) Strikt (innercircletrader.net):** Beide Extreme müssen vorher alte Hochs bzw. Tiefs gesweept haben. Sonst sind es „just two random pivots“.
- **(c) r2f:** „most recent significant swing high and low“ auf D1/H4. Die Range bleibt, bis ein BOS mit Displacement und neuem FVG oder OB eine neue Range bestätigt.
- **(d) Glossar:** Vortages-H/L, Wochen-H/L oder die Extreme der Asian Range.
- **(e) IPDA:** 20/40/60 Tage.

**Zonen:**
- Equilibrium = 50 %. ICT: „50 that's your equilibrium“ (Ep. 6).
- Premium oberhalb, Discount unterhalb von 50 %.
- **Achtung:** Die LuxAlgo-Boxen sind **nicht** die Hälften. Premium = oberste 5 % (`0.95·top + 0.05·bottom`), Discount = unterste 5 %, Equilibrium-Band 47.5–52.5 %.
- Einzelne Quellen sprechen von Vierteln.
- **OTE:** 61.8–78.6 % Retracement, Ideal 70.5 %.

**Empfehlung:**
- DR_ext nach Variante (a), also LuxAlgo-kompatibel und ohne Lookahead, auf dem Struktur-Timeframe H4.
- Variante (b) als optionaler Qualitätsfilter: Ein Anker zählt nur, wenn an ihm ein Pool gesweept wurde.
- Entry-Filter: Long nur bei `price < EQ`, Short nur bei `price > EQ`.
- OTE für Long: `[bot + 0.214·R, bot + 0.382·R]` mit `R = top − bot`.

**Quellen:**
- LuxAlgo Pine-Quelle: https://c.mql5.com/21/592/text.txt?d=1
- r2f Dealing Range: https://www.r2ftrading.com/learn/what-is-a-dealing-range-in-ict
- innercircletrader.net IRL/ERL: https://innercircletrader.net/tutorials/ict-internal-external-liquidity/
- writofinance Dealing Range: https://www.writofinance.com/ict-dealing-range/
- FibAlgo Dealing Range: https://fibalgo.com/library/ict-dealing-range
- ICT Ep. 4: https://sozai.app/transcript/2022-ict-mentorship-episode-4/
- ICT Ep. 6: https://sozai.app/transcript/2022-ict-mentorship-episode-6/
- theinnercircletraders.com Glossar: https://www.theinnercircletraders.com/wp-content/uploads/2026/08/ICT-Trading-Glossary.pdf

---

## 6. Multi-Timeframe-Struktur und Bias

**Paarungen in den Quellen (alles Drittquellen, nicht einheitlich):**

| Quelle | Bias | Struktur/Zone | Entry |
|---|---|---|---|
| innercircletrader.net | D1 | H4/H1 | M15 |
| TradingStrategyGuides | D1 | H4 | M15, dann M5 |
| LiquidityScan | D1/W1 → H1/M15; H4 → M15/M5; H1 → M5/M1; M15 → M1 | | |
| TradeLikeMaster (intraday) | D1 + H4 | H1/M15 | M5/M1 |
| ICT selbst | „That sets your initial bias for the week“ (W1); Hauptanalyse auf Daily-Swings (Ep. 2) | Swings auf 15m bis 8:30 markieren | „five four three two one“ (Ep. 6) |

Konsens-Regeln:
- Nie gegen den HTF-Bias traden.
- Erst auf den LTF wechseln, wenn der HTF-POI erreicht ist.
- Bias-Timeframe fixieren und nicht driften lassen.

**Empfehlung (Default „Intraday“):**
- **D1:** Draw on Liquidity und Daily-Candle-Regel.
- **H4:** Swing-Trend und Dealing Range.
- **M15:** interne Struktur und POI.
- **M5/M1:** MSS-Trigger.
- Den HTF-Zustand liest der LTF immer zum **letzten geschlossenen HTF-Bar** (Index 1).

**Bias-Tabelle (Vorschlag):**

| D1-Trend | H4-Trend | Bias |
|---|---|---|
| Bull | Bull | LONG |
| Bear | Bear | SHORT |
| Bull | Bear | NEUTRAL, außer der Kurs liegt im D1-Discount **und** H4 zeigt einen bullischen internen CHoCH → LONG |
| Bear | Bull | Spiegelung |

Zusätzlich gilt: Widerspricht die Daily-Candle-Regel, ist der Bias NEUTRAL. Gibt es keinen aktiven DOL in Bias-Richtung, ist er ebenfalls NEUTRAL.

**Quellen:**
- innercircletrader.net Top-Down: https://innercircletrader.net/tutorials/ict-top-down-analysis/
- r2f Timeframes: https://www.r2ftrading.com/learn/best-timeframes-for-ict-trading
- TradingStrategyGuides: https://tradingstrategyguides.com/day-10-multi-timeframe-analysis-ict-smc-the-top-down-approach-explained/
- LiquidityScan: https://liquidityscan.io/blog/best-timeframe-for-order-block-trading-ict-guide
- TradeLikeMaster: https://tradelikemaster.com/blog/smart-money-concepts-order-blocks
- ICT Ep. 2: https://sozai.app/transcript/2022-ict-mentorship-episode-2/
- MQL5 Leak-Free MTF: https://www.mql5.com/en/articles/22363

---

## 7. Algorithmus

### 7.1 Ablauf je neu geschlossener Bar (pro Symbol und Timeframe)

1. ATR(14), ATR(50), ATR(200) aktualisieren.
2. Pivots erzeugen: Leg L_int, Leg L_ext, STH n=1, EQ-Pivots L_eq.
3. Struktur aktualisieren (Brüche und Trend).
4. Pools anlegen bzw. mergen.
5. Pool-Zustände aktualisieren (Sweep, Break, Expiry).
6. MSS-Watcher prüfen.
7. Dealing Range und Bias aktualisieren.

Index-Konvention: `k` ist chronologisch und meint die zuletzt **geschlossene** Bar, in MQL5 also shift 1.

### 7.2 Pseudocode

```text
// ---------- Pivots ----------
struct Pivot { int side; double px; datetime tPiv, tConf; string label; }

Pivot? LegPivot(LegState &st, int L, int k) {          // LuxAlgo-kompatibel
  c = k - L; if (c < 1) return null;
  newHi = High[c] > Max(High, c+1..k);                  // = Pine high[size] > ta.highest(size)
  newLo = Low[c]  < Min(Low,  c+1..k);
  prev = st.leg;                                        // Init: BEAR (Pine: leg = 0)
  if (newHi) st.leg = BEAR; else if (newLo) st.leg = BULL;
  if (prev != BEAR && st.leg == BEAR) return {HIGH, High[c], Time[c], Time[k]};
  if (prev != BULL && st.leg == BULL) return {LOW,  Low[c],  Time[c], Time[k]};
  return null;
}
Pivot[] FractalPivots(int n, int k) {                   // ICT-STH: n = 1
  c = k - n;
  hi = all_j(High[c] > High[c+j]) && all_j(High[c] >= High[c-j]);   // MT5-Tie-Regel
  lo = all_j(Low[c]  < Low[c+j])  && all_j(Low[c]  <= Low[c-j]);
  // Outside-Bar (hi && lo): Reihenfolge per M1-Daten bestimmen, sonst Konvention
  // Alternierung erzwingen: 2x gleicher Typ -> extremeres Pivot behalten (smc-Regel),
  // aber nie rückwirkend Events ändern
}

// ---------- Struktur (je Ebene) ----------
struct Level { double px; datetime tPiv; bool crossed; bool valid; }
struct Structure { int bias /*0,+1,-1*/; Level H, L; double trailTop, trailBot;
                   double protH, protL; bool transition; }

void OnPivot(Structure &S, Pivot p, bool ext) {
  if (p.side == HIGH) {
    p.label = !S.H.valid ? "H" : p.px > S.H.px + tolEQ ? "HH" : p.px < S.H.px - tolEQ ? "LH" : "EQH";
    S.H = {p.px, p.tPiv, false, true}; if (ext) S.trailTop = p.px;
  } else { /* Spiegelung */ }
}

Event? CheckBreak(Structure &S, int k, Structure *EXT /* nur fuer INT */) {
  if (S.H.valid && !S.H.crossed && Close[k] > S.H.px + brkBuf) {
    S.H.crossed = true;
    if (EXT && EXT->H.valid && EXT->H.px == S.H.px) return null;    // LuxAlgo-Duplikatfilter
    type = (S.bias == -1) ? CHOCH : BOS;                             // bias 0 -> BOS
    S.protL = MinLow(BarOf(S.H.tPiv), k);                            // Low, der den Bruch erzeugt hat
    S.bias = +1;
    return {type, +1, S.H.px, k};
  }
  /* bärisch: Spiegelung, setzt S.protH = MaxHigh(BarOf(S.L.tPiv), k) */
  // strikter Swing-Trendwechsel (Empfehlung fuer EXT):
  if (ext && S.bias == +1 && Close[k] < S.protL - brkBuf) { S.bias = -1; emit CHOCH_STRICT(-1); }
}
void Trail(Structure &S, int k) { S.trailTop = max(S.trailTop, High[k]); S.trailBot = min(S.trailBot, Low[k]); }

// ---------- Liquiditaetspools ----------
struct Pool { int side /*+1 BSL, -1 SSL*/; int type; int tf; double px;
              int touches; datetime tCreate, tConf; int state; int kEvent; double ext; }

void OnPivotPool(Pivot p, int tf) {
  side = (p.side == HIGH) ? +1 : -1;
  for q in Pools(ACTIVE, tf, side, {SWING, EQ})
    if (|q.px - p.px| <= tolEQ && Bars(q.tLast, p.tPiv) >= minSep
        && PullbackBetween(q, p) >= 0.5*ATR14) {
      q.type = EQ; q.touches++; q.px = side > 0 ? max(q.px, p.px) : min(q.px, p.px); return; }
  AddPool(side, SWING, tf, p.px, p.tPiv, p.tConf);
}
void UpdatePools(int k) {
  for q in Pools(ACTIVE | PENDING) {
    pierce = q.side > 0 ? High[k] > q.px : Low[k] < q.px;          // Wick genuegt (ICT)
    beyond = q.side > 0 ? Close[k] > q.px + brkBuf : Close[k] < q.px - brkBuf;
    if (q.state == ACTIVE && pierce) {
      q.ext = WickExtreme(k);
      if (!beyond) { q.state = SWEPT; emit Sweep(q, k, WICK); }
      else { q.state = PENDING; q.kEvent = k; }
    } else if (q.state == PENDING) {
      if (!beyond && k - q.kEvent <= nReclaim) { q.state = SWEPT; emit Sweep(q, k, FAILED_BREAK); }
      else if (ConsecutiveClosesBeyond(q, k) >= nAccept) { q.state = BROKEN; emit Break(q, k); }
    }
    if (q.state == ACTIVE && AgeBars(q, k) > maxAge[q.tf]) q.state = EXPIRED;
  }
}
// Perioden-Pools: bei NY-Grenzen (17:00 oder 00:00 NY konfigurierbar) PDH/PDL, PWH/PWL, PMH/PML;
// am Session-Ende ASIA/LONDON/NY-H/L; taeglich IPDA20/40/60 (rollierend)

// ---------- MSS (LTF-Trigger) ----------
on Sweep(q, ks) where q.side == -1:                     // SSL gesweept -> bullischer MSS moeglich
  W = {sweepLow = q.ext, ks, ref = juengstes STH mit tPiv <= Time[ks], expires = ks + 20};
each k with W armed:
  if (Close[k] < W.sweepLow) disarm;                    // Sweep-Low per Close verloren
  else if (Close[k] > W.ref.px + brkBuf) {
    k0 = ArgMinLow(W.ks .. k);
    disp = exists j in k0..k: Dir(j) == +1 && Body(j) >= 0.6*Range(j) && Range(j) >= 1.0*ATR14[j];
    fvg  = exists j in k0+1..k-1: Low[j+1] - High[j-1] >= 0.2*ATR50[j];
    if (disp && (fvg || !RequireFVG)) emit MSS(+1, W.sweepLow, W.ref.px, k, FVGs(k0..k));
    disarm;
  } else if (k > W.expires) disarm;

// ---------- Inducement (Default Variante A) ----------
on Swing-BOS(+1, kb): idm = null;
on INT-Pivot LOW p with p.tPiv > Time[kb] && idm == null: idm = p.px;
POIarmed = (idm != null) && (Low seit p.tConf < idm);

// ---------- Dealing Range und Bias ----------
DR = [EXT_H4.trailBot, EXT_H4.trailTop]; EQ = (top + bot) / 2;
Bias = BiasTable(EXT_D1.bias, EXT_H4.bias, DailyCandleRule(), SelectDOL(...));
SelectDOL(dir): argmax over ACTIVE pools in Richtung dir:
  score = wTF + wType + 0.5*(touches - 1) - dist/ATR_D1        // Gewichte: Vorschlag, z. B.
  // PMH 5 > PWH 4 > IPDA60 3.5 > PDH = EQ_ext 3 > Swing_ext 2 > Session 1.5 > Swing_int 1
```

### 7.3 Parameter

**Allgemeine Parameter:**

| Parameter | Default | Bereich | Quelle / Status |
|---|---|---|---|
| L_int (Leg) | 5 | 3–8 | LuxAlgo (fest 5) |
| L_ext (Leg) | 50 | 10–100 | LuxAlgo (Input, min 10) |
| STH n | 1 | 1–2 | ICT-3-Candle |
| ATR-Perioden | 14 / 50 / 200 | – | LuxAlgo 200, WillyAlgo 50 |
| tolEQ | 0.1·ATR200 | 0.05–0.25 | LuxAlgo, WillyAlgo |
| tolEQ „relative“ | 0.25·ATR200 | – | Vorschlag |
| L_eq (EQ-Pivots) | 3 | 3–5 | LuxAlgo 3, homirana 5 |
| brkBuf | 0 | 0–0.1·ATR14 | LuxAlgo 0 / Vorschlag |
| nReclaim / nAccept | 1 / 2 | 1–8 / 1–3 | WillyAlgo, LuxAlgo TL / Vorschlag |
| Sweep→MSS-Fenster | 20 Bars | 10–30 | WillyAlgo |
| Displacement | Body ≥ 0.6·Range, Range ≥ 1.0·ATR14 | 0.5–0.7 / 0.8–1.5 | backtrex, LuxAlgo / Komposit-Vorschlag |
| FVG-Mindestgröße | 0.2·ATR50 | 0.1–0.5 | WillyAlgo |
| Trendline | Länge 10, 3 Touches, 0.25·ATR200 | – | LuxAlgo TL |
| Sessions (NY) | Asia 20–00, London 02–05, NY 07–10, London Close 10–12 | – | Konsens |
| IPDA | 20 / 40 / 60 Handelstage, rollierend | – | FibAlgo |

**Timeframe-spezifische Startwerte (alles Vorschlag, zum Optimieren):**

| Timeframe | Rolle | L_int | STH n | L_ext | Pool-maxAge |
|---|---|---|---|---|---|
| M1 | Trigger | 5 | 1 | 50 | 1 NY-Tag |
| M5 | Trigger | 5 | 1 | 50 | 2 Tage |
| M15 | POI / interne Struktur | 5 | 1 | 50 | 5 Tage |
| H1 | Struktur | 5 | 1–2 | 50 | 20 Tage |
| H4 | Swing / DR | 5 | 2 | 20–50 | 40 Tage |
| D1 | Bias / DOL | 3–5 | 1 (ITH optional) | 10–20 | 60 Handelstage (IPDA) |

L_ext = 50 bedeutet auf H4 rund 200 Stunden Lag und auf D1 rund 2.5 Monate. Deshalb sind für H4 und D1 kleinere Werte vorgeschlagen; vergleichbare Werte nutzen auch andere Implementierungen (MQL5 Part 39: D1 → 9, Hierarchical: 8, WillyAlgo: 10).

### 7.4 Typische Fallstricke

1. **Pivot-Zeit statt Bestätigungszeit verwenden.** Das ist die Hauptursache für Lookahead (smartmoneyconcepts #101: PF 7.32 statt 1.82).
2. **Zentrierte Fenster und Normierungen über den ganzen Datensatz** (smartmoneyconcepts `range_percent`).
3. **Bar 0 oder HTF-Index 0 lesen.** Ein laufender D1-Bar liefert Mid-Bar-Werte.
4. **Tester-Modus:** Möglichst „Every tick based on real ticks“ verwenden; „Open prices only“ schränkt den Zugriff auf andere Timeframes ein.
5. **ZigZag repaintet**, und seine Deviation ist in Points angegeben, also nicht skalenneutral.
6. **Ties und Outside-Bars:** Eine Bar kann gleichzeitig STH und STL sein. Bricht eine Bar Hoch und Tief zugleich, entscheidet bei WillyAlgo der Close.
7. **„Einfrieren“ nach einem Bruch** (ein Bruch pro Pivot) und Event-Duplikate zwischen internal und swing.
8. **Bid-Charts:** MT5-Forex-Bars basieren auf Bid. Buy-Stops über Hochs lösen auf Ask aus. Ein BSL-Sweep kann also ohne Bid-Wick passieren. Stop-Loss und Sweep-Logik brauchen einen Spread-Puffer.
9. **Wochenend-Gaps:** Ein Close jenseits eines Levels ohne Handel durch den Level. Diese Fälle separat kennzeichnen.
10. **Zeitzonen:** DST-Mismatch-Wochen, `TimeGMT()` im Tester, Sonntags-Bars bei GMT+0-Brokern verfälschen PDH/PDL am Montag.
11. **Warm-up:** ATR(200) und L_ext = 50 brauchen genug Historie. Bis dahin Bias UNKNOWN, keine Trades.
12. **Pool-Wachstum:** Anzahl je Timeframe begrenzen und Expiry setzen. Gesweepte Pools nicht erneut als Ziel verwenden.
13. **Overfitting** über 25 Symbole: nur ATR-normierte Parameter verwenden, Parameter pro Asset-Klasse höchstens zweistufig (FX vs. XAUUSD).
14. **Gleicher Name, andere Bedeutung:** „swing length 50“ heißt bei LuxAlgo „50 Bars rechts plus Leg“, bei smartmoneyconcepts „50 Bars je Seite“.

**Quellen:**
- MQL5 Testing-Doku: https://www.mql5.com/en/docs/runtime/testing
- MQL5 Leak-Free MTF: https://www.mql5.com/en/articles/22363
- smartmoneyconcepts Issue #101: https://github.com/joshyattridge/smart-money-concepts/issues/101
- WillyAlgoTrader: https://www.tradingview.com/script/4Y1T9TrB-ICT-Structure-Engine-WillyAlgoTrader/
- LuxAlgo Pine-Quelle: https://c.mql5.com/21/592/text.txt?d=1
- MQL5 `TimeGMT`: https://www.mql5.com/en/docs/dateandtime/timegmt

---

## 8. Offene Mehrdeutigkeiten und wie der EA sie auflöst

1. **Close oder Wick für Brüche?** → BOS, CHoCH und MSS nur per Close. Liquidität gilt per Wick als genommen (ICT Ep. 3/6).
2. **Welcher Low definiert den CHoCH?** Der jüngste Pivot (LuxAlgo) oder der Strong/Protected Low? → Beides berechnen. Der External-Trend kippt nur bei Close jenseits von `protL`. Der interne CHoCH ist Frühwarnung und setzt das `TRANSITION`-Flag.
3. **Was ist ein MSS?** LTF-Event (ICT) oder D1/H4-Event (Glossar)? → MSS = LTF-CHoCH + Sweep ≤ 20 Bars davor + Displacement. Ein HTF-Umkehrbruch heißt „Swing-CHoCH“.
4. **Displacement hat keine Original-Zahl.** → Komposit aus Body ≥ 0.6 und Range ≥ 1.0·ATR14, FVG optional. Per Walk-Forward kalibrieren.
5. **Wo liegt das Inducement?** Erster Pullback nach dem BOS, im Leg, oder vor dem POI? → Default „erstes internes Pivot nach dem BOS“, die anderen als Option. POI ist erst nach IDM-Sweep „armed“.
6. **EQH/EQL-Toleranz und „relative“:** ICT nennt keine Zahl, Quellen streuen von 2 bis 20 Pips. → 0.1·ATR200, „relative“ 0.25·ATR200, Pullback-Pflicht zwischen den Touches.
7. **IRL:** nur FVG, FVG plus OB, oder STH/STL (ICT selbst)? → IRL = unfilled FVGs **und** interne Pivots in der Dealing Range, jeweils mit Typ-Tag.
8. **Anker der Dealing Range:** → LuxAlgo-Trailing-Leg (kausal). Ankerpunkte, an denen gesweept wurde, als Qualitäts-Flag. Neu ankern bei Swing-BOS oder Swing-CHoCH.
9. **Breite der Premium/Discount-Zonen** (Hälften, 5 %-Bänder, Viertel)? → Hälften als Filter. OTE 0.62–0.79 als Entry-Band.
10. **Tagesgrenze** (00:00 NY, 17:00 NY, 18:00 NY)? → Konfigurierbar. Default 17:00 NY, entspricht dem Forex-D1 bei NY-Close-Brokern. Midnight Open nur als Referenzlinie.
11. **Asia-Session** (20–00 oder 20–02 NY)? → 20–00 als Killzone, 20–02 als „Asian Range“-Pool, beide konfigurierbar.
12. **Strong/Weak** (Trend, Struktur, Volumen, Rejection)? → Strukturell (siehe 2.4). Volumen ist im FX-Retail-Feed nur Tick-Volumen und wird nicht verwendet.
13. **IPDA-Fenster** rollierend oder als Blöcke? → Rollierend.
14. **Sweep-Reclaim-Fenster** (gleiche Bar bis 8 Bars)? → Gleiche Bar = „Sweep“, bis 3 Bars = „Failed Break“. Beide verbrauchen den Pool.
15. **Swing-Methode und Länge:** → Leg 5/50 (LuxAlgo-Parität) plus STH n=1 für den Trigger. ICT-ITH-Promotion optional für D1/H4.
16. **„Old highs/lows“ und Trendline-Liquidity** sind bei ICT nur qualitativ beschrieben. → Old = External-Pivot ≥ 20 Bars unberührt. Trendline nach LuxAlgo-Defaults und nur als niedrig gewichteter DOL-Kandidat.
17. **Gewichte im DOL-Ranking:** Keine Quelle liefert Zahlen, nur eine Rangfolge. → Die obigen Gewichte sind ein Vorschlag und müssen im Backtest validiert werden.
