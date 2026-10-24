<!-- Kapitel 4: Bestehende Implementierungen (LuxAlgo, smartmoneyconcepts, MQL5, GitHub, Market) | Deep-Research-Rohbericht (Recherche-Agent), Stand 2026-10-24, unverändert übernommen -->

# Teilbericht: Bestehende algorithmische SMC/ICT-Implementierungen

**Wie gelesen wurde:** Den Quellcode habe ich per WebFetch gelesen. Das Tool liefert Paraphrasen und kurze wörtliche Zitate, keine vollständigen Dateien. Der Pseudocode ist aus diesen Zitaten rekonstruiert, wörtliche Fragmente stehen in `code`. Backtest-Reports, die in MQL5-Artikeln nur als Bild vorliegen, konnte ich nicht auswerten. Gegen Ende war das gemeinsame WebSearch-Budget aufgebraucht. Der MQL5-Market-Teil beruht deshalb auf einer direkt abgerufenen Listing-Seite und Stichproben. Weitere Suchen, etwa zu „ICT Concepts [LuxAlgo]“, waren nicht mehr möglich.

---

## 1. LuxAlgo „Smart Money Concepts (SMC) [LuxAlgo]“

**Status und Quellen**
- Open Source auf TradingView, veröffentlicht 11.10.2022.
- Refactoring-Update 05.09.2024 („improved performance and detection for structures, order blocks, FVGs and EQH/EQL“), letztes Update 23.09.2025.
- Lizenz CC BY-NC-SA 4.0: keine kommerzielle Nutzung, Share-Alike.
- Gelesen habe ich die Original-Pine-Datei (v5), die im Parity-Ordner des MQL5-Ports liegt: `parity/luxalgo_smc_original.pine`.

**Weitere Mirrors und Ports**
- Gist von niquedegraaff („[Enhanced]“): ältere Codebasis mit `swings()`/`ob_coord()`. Sie schließt Hochvolatilitätskerzen per `(high-low) < 2*threshold` aus, statt die Werte zu tauschen.
- Python-Port makeitcount89: nur Struktur und OB.
- MQL5-Port GeneralTradingSarl (identisch: isaias-muniz): rund 2.300 Zeilen. Gegen TradingView getestet: 327/327 Labels und Linien, 5.044/5.044 Kerzenfarben.
- LuxAlgo/PineTS: Pine-Runtime für JS, AGPL. Nützlich, um Referenzdaten für Tests zu erzeugen.

**Defaults im Code**

| Bereich | Default |
|---|---|
| Swing-Struktur | `swingsLengthInput` = 50 (min. 10) |
| Internal-Struktur | fest 5 (`getCurrentStructure(5,false,true)`) |
| Confluence Filter | aus |
| Internal OB | an, 5 werden angezeigt |
| Swing OB | aus |
| OB-Filter | „Atr“ (alternativ „Cumulative Mean Range“) |
| OB-Mitigation | „High/Low“ (alternativ „Close“) |
| EQH/EQL | an, Bars Confirmation 3, Threshold 0,1 (Bereich 0–0,5) |
| FVG | aus, Auto Threshold an, Timeframe "" (= Chart-TF), Extend 1 |
| Volatilitätsmaß | ATR fest `ta.atr(200)` |
| MTF-Levels D/W/M, Premium/Discount | aus |

### 1.1 Leg- und Pivot-Erkennung

Kausal, Bestätigung nur auf der rechten Seite:

```
var legState = 0                                // 0=BEARISH_LEG, 1=BULLISH_LEG
leg(size):
  if high[size] > ta.highest(size)  -> legState = BEARISH_LEG   // Kerze vor size Bars > alle size Folgebars
  elif low[size] < ta.lowest(size)  -> legState = BULLISH_LEG
getCurrentStructure(size, equal, internal):
  l = leg(size)
  if ta.change(l) == +1:                         // Swing-LOW bestätigt, Ursprung = Bar t-size
     p = equal?equalLow : internal?internalLow : swingLow
     if equal and |p.currentLevel - low[size]| < eqThr*ATR200 -> EQL
     p.lastLevel=p.currentLevel; p.currentLevel=low[size]; p.crossed=false
     p.barTime=time[size]; p.barIndex=bar_index[size]
     if swing: trailing.bottom=p.currentLevel; Label = currentLevel<lastLevel ? "LL":"HL"
  if ta.change(l) == -1: spiegelbildlich (EQH, trailing.top, "HH"/"LH")
```

- Swings alternieren automatisch (High, Low, High …), ein Dedup-Schritt ist nicht nötig.
- Lag = `size` Bars: bei Swing 50, bei Internal 5.
- Ereigniszeit (Bestätigung) und Ursprung (`barIndex` = t−size) werden getrennt geführt. Das ist das richtige Muster für einen EA.

### 1.2 BOS/CHoCH und Confluence Filter

```
displayStructure(internal):
  if internal and confluenceFilter:                         // var bool, Start true
     bullishBar := high - max(close,open) > min(close, open - low)   // wörtlich so
     bearishBar := high - max(close,open) < min(close, open - low)
  p = internal?internalHigh:swingHigh ; T = internal?internalTrend:swingTrend
  extra = internal ? (internalHigh.currentLevel != swingHigh.currentLevel and bullishBar) : true
  if ta.crossover(close, p.currentLevel) and not p.crossed and extra:
     tag = T.bias==BEARISH ? CHOCH : BOS                    // Start-Bias 0 -> erster Bruch = BOS
     p.crossed=true ; T.bias=BULLISH                        // auch wenn nicht angezeigt
     Linie (p.barTime -> time) auf p.currentLevel
     if OB-Layer aktiv: storeOrderBlock(p, internal, BULLISH)
  bärisch: ta.crossunder(close, low-Pivot), tag = T.bias==BULLISH ? CHOCH : BOS
```

- Brüche sind close-basiert.
- Pro Pivot gibt es genau einen Bruch (`crossed`).
- Ein Internal-Bruch wird unterdrückt, wenn sein Level gleich dem Swing-Level ist.
- Der Confluence Filter ist fragwürdig: `min(close, open - low)` vergleicht einen Preis mit einer Spanne. Gemeint war vermutlich `min(close,open) - low`. Außerdem verlangt der Filter für bullische Brüche einen oberen Docht, der größer ist als der untere Teil. Nicht 1:1 übernehmen.

### 1.3 Order Blocks: Volatilitätsfilter und „parsed highs/lows“

```
jede Bar:
  vol        = filter=="Atr" ? ta.atr(200) : ta.cum(ta.tr)/bar_index
  highVol    = (high-low) >= 2*vol
  parsedHigh = highVol ? low : high ; parsedLow = highVol ? high : low     // Swap
  push(parsedHighs, parsedLows, highs, lows, times)
storeOrderBlock(p, internal, bias):            // aufgerufen auf der Bruchkerze
  if bias==BEARISH: idx = p.barIndex + indexOf(max(parsedHighs[p.barIndex .. bar_index-1]))
  else:             idx = p.barIndex + indexOf(min(parsedLows [p.barIndex .. bar_index-1]))
  ob = {barHigh=parsedHighs[idx], barLow=parsedLows[idx], barTime=times[idx], bias}
  if size(list)>=100: pop()  ;  unshift(list, ob)          // neuester vorn, max. 100 je Liste
deleteOrderBlocks(internal):                   // jede Bar, nach displayStructure
  bearSrc = mit=="Close"?close:high ; bullSrc = mit=="Close"?close:low
  remove ob if (BEARISH and bearSrc > ob.barHigh) or (BULLISH and bullSrc < ob.barLow)
drawOrderBlocks: nur list[0..N-1] (N=5), nur auf der letzten Bar
```

- **Bullischer OB:** die Kerze mit dem tiefsten (geparsten) Low zwischen dem gebrochenen Swing-High-Pivot und der Bruchkerze, die Bruchkerze selbst ausgeschlossen. Das ist der Tiefpunkt des Pullbacks.
- **Volatilitätsfilter:** Durch den Swap scheiden Kerzen mit Range ≥ 2×ATR(200) praktisch aus. Wird trotzdem eine solche Kerze gewählt, entsteht eine invertierte Box (Randfall).
- **„Mitigation“ heißt hier Invalidierung:** Der OB wird gelöscht, wenn der Preis ihn durchbricht. Eine Erstberührung oder ein Retest wird nicht verfolgt.

### 1.4 FVG mit Auto-Threshold

```
[lastClose,lastOpen,lastTime, currentHigh,currentLow,currentTime, last2High,last2Low] =
  request.security(tickerid, fvgTF, [close[1],open[1],time[1], high[0],low[0],time[0], high[2],low[2]],
                   lookahead = barmerge.lookahead_on)
barDeltaPercent = (lastClose - lastOpen) / (lastOpen * 100)
newTF     = timeframe.change(fvgTF)                     // auf Chart-TF jede Bar
threshold = auto ? ta.cum(|newTF ? barDeltaPercent : 0|) / bar_index * 2 : 0
bullFVG = currentLow  > last2High and lastClose > last2High and  barDeltaPercent > threshold and newTF
bearFVG = currentHigh < last2Low  and lastClose < last2Low  and -barDeltaPercent > threshold and newTF
bull: top=currentLow, bottom=last2High ;  bear: top=currentHigh (!), bottom=last2Low
deleteFairValueGaps (jede Bar): remove if (bull and low < bottom) or (bear and high > top)
```

- Die Mittelkerze muss jenseits des Extrems von Kerze 1 schließen. Ihr Body muss größer sein als das Doppelte des **kumulativen** historischen Durchschnitts-Body in Prozent. Das wirkt als Displacement-Filter.
- **Asymmetrie (vermutlich ein Bug):** Ein bullisches FVG wird erst bei vollständiger Füllung gelöscht, ein bärisches schon beim ersten Eintritt, weil `top` beim bärischen FVG die untere Kante ist.
- **HTF-Einstellung:** `high[0]/low[0]` mit `lookahead_on` liest auf historischen Bars die finale HTF-Kerze, also Zukunftsdaten. Nur mit Chart-TF ist die Erkennung sauber.
- **Threshold-Verdünnung (meine Ableitung aus dem Code):** Der Threshold summiert nur über HTF-Wechsel, teilt aber durch die Zahl aller Chart-Bars. Bei HTF wird er dadurch um den TF-Faktor verwässert.
- Die FVG-Liste hat **kein Größenlimit**.

### 1.5 EQH/EQL, Trailing Extremes, Strong/Weak, Premium/Discount

- **EQH/EQL:** 3er-Pivots. Verglichen wird nur mit dem unmittelbar vorherigen Pivot gleichen Typs, Toleranz 0,1 × ATR(200).
- **Trailing Extremes:** `trailing.top = max(high, trailing.top)` und `trailing.bottom` analog. Bei jedem neuen 50er-Swing-Pivot werden sie überschrieben.
- **Strong/Weak:** Ist `swingTrend` bärisch, heißt der Hochpunkt „Strong High“, sonst „Weak High“. Ist `swingTrend` bullisch, heißt der Tiefpunkt „Strong Low“, sonst „Weak Low“.
- **Zonen:**
  - Premium: `[0.95T+0.05B, T]`
  - Equilibrium: `[0.525B+0.475T, 0.525T+0.475B]`
  - Discount: `[B, 0.95B+0.05T]`
  - Das sind dünne 5-%-Bänder für die Anzeige. Als Handelslogik taugt nur die Schwelle bei 50 %.

### 1.6 MTF-Levels, Ausführungsreihenfolge, Realtime

**MTF-Levels:** `request.security(tf, [high[1], low[1], time[1], time], lookahead_on)` liefert die letzte abgeschlossene D/W/M-Kerze. Das ist das korrekte Idiom ohne Repaint.

**Reihenfolge pro Bar:**
1. Arrays pushen
2. Trailing Extremes, Premium/Discount
3. FVGs löschen
4. Pivots: swing, dann internal, dann EQH/EQL
5. `displayStructure`: internal, dann swing
6. `deleteOrderBlocks`
7. neue FVGs erkennen
8. Zeichnen auf der letzten Bar

**Realtime:** Es gibt kein `barstate.isconfirmed`. Die Realtime-Bar wird pro Tick mit Rollback neu berechnet. BOS und Alerts können daher intrabar erscheinen und wieder verschwinden. Der MQL5-Port bildet das mit zwei Instanzen nach: `committed` (Stand der geschlossenen Bars) und `working` (Wegwerfkopie pro Tick). Zusätzlich nutzt er `PINE_EPS = 1e-10` für Vergleiche und eine RMA-ATR, die mit dem Mittel der ersten 200 True Ranges geseedet wird.

### 1.7 Folgen für eine Portierung
- Die Ergebnisse hängen von der Länge der geladenen Historie ab: `ta.cum(...)/bar_index` beim Range-Filter und beim FVG-Threshold, plus die ATR-Seed-Phase.
- Pine-Objektlimits von 500 Labels, Linien und Boxen.
- Löschen per Index während der Iteration kann Elemente überspringen.
- Die Lizenz verbietet einen kommerziellen 1:1-Port.

Quellen:
- [TradingView-Skript](https://www.tradingview.com/script/CnB3fSph-Smart-Money-Concepts-SMC-LuxAlgo/)
- [Original-Pine im Parity-Ordner](https://raw.githubusercontent.com/GeneralTradingSarl/Smart-Money-Concepts/main/parity/luxalgo_smc_original.pine)
- [MQL5-Port GeneralTradingSarl](https://github.com/GeneralTradingSarl/Smart-Money-Concepts) / [isaias-muniz](https://github.com/isaias-muniz/Smart-Money-Concepts)
- [Gist niquedegraaff](https://gist.github.com/niquedegraaff/8c2f45dc73519458afeae14b0096d719)
- [makeitcount89](https://github.com/makeitcount89/Trading-Smart-Money)
- [LuxAlgo-Library](https://www.luxalgo.com/library/indicator/smart-money-concepts-smc/)
- [PineTS](https://github.com/LuxAlgo/PineTS)

---

## 2. joshyattridge/smart-money-concepts (PyPI `smartmoneyconcepts`)

Version 0.0.27, MIT, rund 2,1k Stars. Gelesen: `smc.py`.

**`swing_highs_lows(ohlc, swing_length=50)`**
```
swing_length *= 2                                   // Fenster = 100
hl[i]=+1 if high[i] == high.shift(-(L//2)).rolling(L).max()[i]   // = max(high[i-49 .. i+50])
hl[i]=-1 elif low[i] == low.shift(-(L//2)).rolling(L).min()[i]
repeat bis stabil: benachbarte gleichartige Swings -> extremeren behalten (Tie: späteren löschen)
hl[0] = Gegenteil des ersten Swings ; hl[n-1] = Gegenteil des letzten Swings   // erzwungen, ungeprüft
```
- Lookahead von 50 Bars (Default), obwohl der Kommentar von „5 candles“ spricht.
- Der Dedup-Schritt **zieht Swings nachträglich zurück**.
- Die Endpunkte sind künstlich gesetzt.

**`fvg(ohlc, join_consecutive=False)`**
```
bull[i]: high[i-1] < low[i+1]  & close[i] > open[i]   ->  Top=low[i+1], Bottom=high[i-1]
bear[i]: low[i-1]  > high[i+1] & close[i] < open[i]   ->  Top=low[i-1], Bottom=high[i+1]
join: gleiche Vorzeichen in Folge -> auf letzten Index mergen (max Top, min Bottom)
MitigatedIndex = erster j>=i+2 mit low<=Top (bull) bzw. high>=Bottom (bear); sonst 0
```
- Das Flag liegt auf der Mittelkerze und nutzt `shift(-1)`: 1 Bar Lookahead.
- „Mitigiert“ bedeutet hier Wick-Berührung, also eine andere Semantik als bei `ob`.

**`bos_choch(ohlc, shl, close_break=True)`**
```
bei jedem neuen Swing, letzte 4 Swings [L4,L3,L2,L1]:
  bull BOS : Typen [-1,1,-1,1] und L4<L2<L3<L1 ; bull CHoCH: L1>L3>L4>L2
  bear BOS : Typen [1,-1,1,-1] und L4>L2>L3>L1 ; bear CHoCH: L1<L3<L4<L2
  Flag auf Bar von L3 (Vergangenheit), Level=L3
BrokenIndex = erster j>=i+2 mit close (bzw. high/low) jenseits Level, gesucht bis Datenende
frühere Flags löschen, wenn deren Bruch >= aktueller Bruch ; ungebrochene löschen
```
- Rein hindsight-basierte Musterlabels.
- `BrokenIndex` bleibt nach dem Pruning teils stehen.

**`ob(ohlc, shl, close_mitigation=False)`**
```
Bar i: letzter Swing-High k<i (searchsorted), nicht crossed; close[i] > high[k] -> crossed[k]=true
  OB-Kerze o = letzte Kerze mit min(low[k+1..i-1]); sonst o=i-1 (dann Top=low, Bottom=high: VERTAUSCHT)
  OBVolume = vol[i]+vol[i-1]+vol[i-2] ; Percentage = min(vol[i]+vol[i-1], vol[i-2]) / max(..) * 100
aktive OBs: low < Bottom (bzw. min(open,close) bei close_mitigation) -> breaker, MitigatedIndex=i-1
            breaker und high > Top -> OB gelöscht
bärisch spiegelbildlich, aber MitigatedIndex=i (Asymmetrie)
```
- Das Ergebnis steht auf Zeile o, bekannt ist es aber erst bei Bar i. Index-Leak.
- Dazu kommt der Lookahead über die Swings.
- Die Volumenwerte sind bei FX nur Tick-Volumen.

**`liquidity(range_percent=0.01)`**
- `pip_range = (high.max() - low.min()) * range_percent` wird aus dem **gesamten Datensatz** berechnet.
- Gruppiert werden gleichartige Swings innerhalb ±pip_range bis zum Sweep, mindestens 2 Levels.
- `Swept` wird bis zum Datenende gesucht. Lookahead.

**Kausale Funktionen und Restbefunde**
- `previous_high_low(time_frame="1D")`: kausal, nutzt nur abgeschlossene Perioden. Kleiner Randfall an der ersten Kerze einer Periode.
- `sessions`: kausal, aber mit festen UTC-Fenstern: London 07–16, NY 13–22, London Open Kill Zone 06–09, NY Kill Zone 11–14 und weitere. Es gibt keine Sommerzeit-Logik. Nach meiner Ableitung passen die Fenster zu ICTs NY-Zeiten nur während der US-Sommerzeit. Außerdem ein Zeitzonen-Bug: „UTC+3“ wird zu „Etc/GMT+3“, also UTC−3.
- `retracements`: erbt den Lookahead der Swings. `np.roll` schiebt den letzten Wert an Index 0.

**Issues und PRs zum Lookahead**
- [#34](https://github.com/joshyattridge/smart-money-concepts/issues/34), 2024: Der Owner bestritt den Bias. freqtrade lookahead-analysis meldete 20 betroffene Signale.
- [#101](https://github.com/joshyattridge/smart-money-concepts/issues/101), 04/2026, offen: identische Logik auf XAUUSD M15, 10 Jahre.
  - Centered Window: 177 Trades, Trefferquote 81,4 %, **PF 7,32**.
  - Kausale Confirm-Bars: 106 Trades, Trefferquote 52,8 %, **PF 1,82**.
- Fix-PRs [#95](https://github.com/joshyattridge/smart-money-concepts/pull/95), [#103](https://github.com/joshyattridge/smart-money-concepts/pull/103) und #108 sind nicht gemergt.
- Replay-Test von nyambati: EURUSD M15, 60 Präfixe, swing_length 5, gezählt wurden nachträglich umgeschriebene Werte.
  - master: 92, #108: 92, #103: 61, #95: 5.
  - Die Rest-Rewrites kommen aus dem Dedup-Schritt.
  - Seine Lösung: ein einziger Vorwärtsdurchlauf, der gleichgerichtete Swings **überspringt statt zurückzuziehen**. Ergebnis 0 Rewrites.
  - Weiterer Befund: Outside Bars (gleichzeitig High und Low) werden stillschweigend überschrieben.

**Urteil:** Die Library taugt nur für Offline-Labeling und Visualisierung. Für Signale und Backtests ist sie unbrauchbar, mit Ausnahme von `previous_high_low` und `sessions`.

Quellen: [smc.py](https://raw.githubusercontent.com/joshyattridge/smart-money-concepts/master/smartmoneyconcepts/smc.py), [Repository](https://github.com/joshyattridge/smart-money-concepts)

---

## 3. MQL5-Artikel und CodeBase

**Gemeinsamer Befund:**
- Die Artikel sind didaktisch angelegt.
- Backtest-Zahlen stehen fast nie im Text, sondern nur in Bildern.
- Kosten, Out-of-Sample-Tests und Parameterbegründungen fehlen.
- Stops und Schwellen werden meist in festen **Punkten** angegeben. Auf 25 Instrumente mit XAUUSD übertragen ist das unbrauchbar.

**Serie „Automating Trading Strategies in MQL5“ (Allan Munene Mutiiria)**

- [Part 6 – OB, 17135](https://www.mql5.com/en/articles/17135)
  - Logik: Konsolidierung aus 7 Bars, benachbarte Highs und Lows ≤ 50 Punkte auseinander. Breakout per Close. Impuls innerhalb von 3 Bars mit mindestens 1× Range. Der „OB“ ist die ganze Range-Box.
  - Entry per Marktorder beim Durchbruch der Box-Kante, nicht beim Retest wie im Text beschrieben. SL und TP je 1500 Punkte. Keine Inputs.
  - Bugs: `ArrayRemove(…,0,1)` entfernt in der Schleife das falsche Element. Die Range-Erweiterung wird nur geloggt, nicht angewendet.
- [Part 12 – Mitigation OB, 17547](https://www.mql5.com/en/articles/17547)
  - Gleiche Konsolidierungslogik. Schließt der Preis durch die Gegenkante, folgt ein Gegentrade. SL und TP 1500 Punkte.
  - Das Verfallsdatum hängt an `CHART_VISIBLE_BARS`, also an der Fenstergröße des Charts.
  - Ein Leser meldet: mit Defaults keine Trades.
- [Part 35 – Breaker, 19638](https://www.mql5.com/en/articles/19638)
  - Ablauf: OB wird per Close invalidiert, optional mit Swing-Validierung. Danach Move-away von 50 Punkten, dann Retest-Close. Ergebnis ist ein Breaker-Trade.
  - SL und TP 1500 Punkte.
- [Part 45 – IFVG, 20361](https://www.mql5.com/en/articles/20361)
  - FVG ab 100 Punkten.
  - Zustände: Normal → Mitigated (Wick durch die Fernkante) → Retraced → Inverted (Close jenseits, Vorbar-Close in der Zone). Bei Inverted wird getradet.
  - Zonen-Limit `maxFVGs`=50. SL Zonenkante ± 300 Punkte.
- [Part 46 – Sweep on BoS, 20569](https://www.mql5.com/en/articles/20569)
  - Fraktal-Swings mit `SwingLength` 5. HH bzw. LL setzen den Trend.
  - Sweep: Bar 1 wickt über den letzten Swing hinaus, schließt zurück und hat die passende Kerzenfarbe.
  - SL = Sweep-Extrem ± „Pips“, die tatsächlich mit `_Point` multipliziert werden, also Punkte sind. RR 2.
- [Part 48 – OB + Inducement + BOS, 22078](https://www.mql5.com/en/articles/22078)
  - Trendfilter auf H4. Konsolidierungs-OB mit den Werten 7 / 50 / 3 / 1,0.
  - FVG ≥ 10 Punkte. Inducement mit halber Swingstärke, ≥ 20 Punkte, außerhalb des OB. BOS per Close.
  - Risiko 0,1 %, RR 4, zwei Trailing-Modi. Test AUDUSD M1, nur als Bild.
  - Lookahead: Der Trend wird über die ganze Historie berechnet und in `OnInit` auf alle historischen Zonen angewendet.
- [Part 50 – Turtle Soup, 23155](https://www.mql5.com/en/articles/23155)
  - Extremum der letzten 20 Bars, mindestens 4 Bars alt. Sweep-Tiefe > 30 Punkte und > 2 % der Range.
  - Close zurück plus Reversal-Body. SL-Puffer 3000 Punkte, TP 1R.
- [Part 51 – Judas Swing, 23523](https://www.mql5.com/en/articles/23523)
  - Killzones in NY-Zeit: London 02:00–05:00, NY 08:20–11:00.
  - Sommerzeit: US-Regeln (zweiter Sonntag im März bis erster Sonntag im November), Broker-GMT-Offset **manuell**.
  - Equilibrium aus der Session-Range. MSS über Fraktal 3 mit Close. Setup verfällt nach 24 Bars.
  - Der Text spricht vom Sweep des Session-Extrems, der Code prüft das 20-Bar-Extrem.
- [Part 52 – tCISD/SSMT, 23549](https://www.mql5.com/en/articles/23549)
  - Quarterly Theory: 90-Minuten-Zyklen ab 18:00 NY.
  - SSMT als XOR-Sweep gegen ein Korrelationssymbol (Default XAGUSDm).
  - Zweitsymbol wird über `iBarShift`/`iHigh` gelesen, mit Nearest-Bar-Matching. Das riskiert Schein-Divergenzen.

**Weitere Artikel**
- [15017](https://www.mql5.com/en/articles/15017): Fraktal 5/5. Bruch bei `Bid > swing_H && close(1) > swing_H`. SL 3500, TP 500 Punkte, also 1:7 invers.
- [15030](https://www.mql5.com/en/articles/15030): BOS plus RSI(8) mit 70/30. SL 200, TP 500. Kauf- und Verkaufslogik passen nicht zum Text. Teilweise von 15017 übernommen.
- [14261](https://www.mql5.com/en/articles/14261): FVG ab 100 Punkten. SL = 10 × Gap, TP = Gapkante. `ArrayRemove`-Bug und exakte Preisgleichheit als Ablaufkriterium.
- [16340](https://www.mql5.com/en/articles/16340): OB, FVG und BOS in einem EA. SL 3500, TP 7500 Punkte. Test 2 Monate H1. Die BOS-Richtung ist im Code gegenüber dem Text invertiert.
- [18669](https://www.mql5.com/en/articles/18669): FVG wird erkannt, aber nicht für den Entry genutzt. Ein Partial Close bei 3R ist unerreichbar, weil der TP bei 2R liegt.
- [16659 (Zhuo Kai Chen)](https://www.mql5.com/en/articles/16659): IFVG auf NQ M3, 2020–2024. „Mehr als 400 Trades“, keine Zahlen im Text, keine Kosten, kein Out-of-Sample-Test.
- [21581](https://www.mql5.com/en/articles/21581): nur Indikator, ohne SL und TP.
- [23539 – Modulare FVG-Engine](https://www.mql5.com/en/articles/23539)
  - Gutes Design: Bewertung nur geschlossener Bars, ein Filter auf das True-Range-Mittel, Mitigation wahlweise per Wick oder per Close.
  - Zahlen: EURUSD M5, 2024–2025, Real Ticks, 142 Trades, PF 1,48, Drawdown 3,12 %, Trefferquote 54,2 %, laut Artikel „fixed 20ms spread“.
  - Plausibilität: Bei festen 150/300 Punkten SL/TP und 54,2 % Trefferquote wäre vor Kosten ein PF von etwa 2,4 zu erwarten. Die Zahlen sind inkonsistent.
- [24184 – Decoding Market Intent](https://www.mql5.com/en/articles/24184)
  - Bester konzeptioneller Ansatz in diesem Teil.
  - Ein Sweep ist hier eine Sequenz, kein Touch: Penetration ≥ k × ATR, Close zurück, danach Reaktion durch Displacement oder Strukturbruch.
  - Liquidity-Pools werden mit ATR-Toleranz zusammengeführt.
  - Score 0–100 mit Gewichten: HTF-Bias 20, Sweep 20, Displacement 18, BOS/CHoCH 14, FVG 8+8, Rejection 5, Premium/Discount 7.
  - Harte Gates (Sweep, Displacement, BOS) gelten außerhalb der Arithmetik. Keine Backtests.

**CodeBase**
- [71497](https://www.mql5.com/en/code/71497): OB = letzte Gegenkerze vor dem BOS. FVG muss ≥ 15 % von ATR(14) sein.
- [70826 ExMachina](https://www.mql5.com/en/code/70826): Parameter identisch zu LuxAlgo (5/50, ATR 200, 100 OBs, EQH 0–0,5), obwohl als eigene Implementierung beworben.
- [78588](https://www.mql5.com/en/code/78588), 10/2026: kein Repaint, inkrementelle Berechnung. Mitigation-Modus wählbar: Touch, Half oder Break. Breaker-Konvertierung. **EA-Buffer 0–3** mit Ober- und Unterkante der neuesten aktiven OBs. Gutes Schnittstellenmuster.

---

## 4. GitHub, Backtests und unabhängige Studien

| Projekt | Logik | Lookahead | Kosten | OOS | Ergebnis | Urteil |
|---|---|---|---|---|---|---|
| [MrOwl1011/Smc_ZOB_CISD](https://github.com/MrOwl1011/Smc_ZOB_CISD) (MQL5, MIT) | HTF-OB (H1) → Retest → LTF-CISD (M5), Trendfilter („gate“), 1:1 | explizit verhindert ([DESIGN.md](https://raw.githubusercontent.com/MrOwl1011/Smc_ZOB_CISD/main/DESIGN.md)) | R-Ergebnisse **ohne** Kosten | IS 2/3 vs. OOS 1/3, Walk-forward, Bonferroni, Block-Bootstrap | H1→M5: 813 Trades, 55,5 %, +0,109 R, PF 1,25; ohne Trendfilter +0,005 R; Displacement 2,0 ATR: +0,143 R IS / +0,144 R OOS; FX-Majors 7/7 positiv | beste gefundene Evidenz, aber vor Kosten, 1 Broker, 20 Monate |
| [KVignesh122](https://github.com/KVignesh122/MT5-SMC-trading-bot) (90 Stars) | OB/FVG/BOS + ADX-Regime | nein: nutzt die sich noch bildende Bar 0 (FVG mit i=0, Swings) | Spreadfilter | nein | Claim „60 %+ bis 300 %+ jährlich“ ohne Daten | Marketing; BOS feuert wiederholt |
| [SiyabongaDlamini](https://github.com/SiyabongaDlamini/SmartMoney.MQ5) | MTF-Bias, OTE, Sweep, MSS (XAUUSD M1) | unbekannt | unbekannt | nein | PF 1,20, 434 Trades, +43 % – ohne Zeitraum | unvollständig |
| [foeed/FvgGold-EA](https://github.com/foeed/FvgGold-EA) | FVG-Score 0–100 + OB-Bonus | unbekannt | nicht beschrieben | „optimiert“ | +48,7 % in 6 Monaten, 64 Trades, 0,01 Lot | **unplausibel**: braucht rund 76 $ pro Trade bei 1 oz, also implizit ≈ 600 $ Risiko pro Trade |
| [frankabingale1111/smc-backtest](https://github.com/frankabingale1111/smc-backtest) (vectorbt) | H4-SMA-Bias, Sweep, FVG, Score | nicht dokumentiert | Fees ohne Werte | nein | PF 9,55, Sharpe 7,23 | Red Flag; FVG-Definition im README falsch (Low vs. Low statt Low vs. High) |
| [jmlacasa](https://github.com/jmlacasa/backtesting_finance) (backtesting.py) | LuxAlgo-OBs auf 3 TFs | ? | nein | – | Autor: „overfitted“ | ehrliches Negativbeispiel |
| [DOE SMC Pro BTC](https://www.tradingview.com/script/QMvHkvdQ-SMC-Pro-BTC-ICT-Order-Blocks-FVG-DOE/) (TradingView) | 4H/1H-BOS, OB∩FVG, Sweep, Premium/Discount | `isconfirmed`, `lookahead_off` (Selbstauskunft) | 0,075 % + 3 Ticks | nein | PF 1,95 bei 90 Trades / 1,32 bei 29 Trades, 2021–2026 | kleine Stichprobe |

**Unabhängige Studien**
- [StatOasis](https://statoasis.com/overfit/research/ict-backtest-what-survives), 09/2026
  - 648 Backtests auf Tagesbars von SPY, QQQ, DIA und IWM, ohne Kosten.
  - 31 von 32 t-Werten liegen unter 2. 0 von 648 schlagen Buy-and-Hold.
  - Nur die OB-Familie schlägt in der Mehrheit der Varianten auf allen Märkten den Zufallseinstieg.
- [SSRN, Mahadzva, „Smart Money or Costly Folklore?“](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=7430998)
  - Nur Abstract über ein Suchergebnis gesehen, die Seite lieferte 403.
  - Sechs mechanische ICT/SMC-Regeln auf EURUSD, GBPUSD, AUDUSD und USDJPY intraday, getestet mit Walk-forward, Bootstrap, Permutation und Holdout.
  - Ergebnis: „no evidence that ICT/SMC concepts work as literally taught“.
  - Sweeps sagen in 65 von 66 Fold-Selektionen **Continuation** voraus, keine Umkehr.
  - CHoCH+FVG in **umgekehrter** Richtung ist auf EURUSD H1 signifikant (p = 0,0192).

---

## 5. MQL5 Market (kritisch)

**Landschaft:** Eine [Market-Listing-Seite](https://www.mql5.com/en/market/mt5/expert?Filter=smart%20money) zeigte rund 80 EAs, davon etwa 51 mit SMC/ICT-Bezug.
- Preis von gratis bis 599 USD. „[Ict Ea](https://www.mql5.com/en/market/product/183690)“ kostet 2.000 USD und nennt keine Ergebnisse.
- Schwerpunkt XAUUSD und Indizes. Kaum Multi-Pair-FX.
- Die meisten ohne Bewertung.

**Typische Behauptungen und was dahintersteht**
- [Silver Bullet ICT](https://www.mql5.com/en/market/product/115163): „PF bis 2,8, Recovery Factor bis 5,9, +270 % in 4 Jahren“, ohne Methodik. Die Sets gibt es erst nach dem Kauf.
- [Institutional SMC Robot](https://www.mql5.com/en/market/product/187011), 599 USD, „only 2 copies left, next price 999“: seit v3.2 mit Pyramiding. Das verlinkte [XAUUSD-Signal](https://www.mql5.com/en/signals/2389159) läuft 8 Wochen: +103,8 %, 33 Trades, Trefferquote 84,8 %, PF 3,31, maximaler Drawdown 27,6 % (Balance), Hebel 1:500, 0 Abonnenten. MQL5 warnt selbst: „newly opened account … random“.
- [FVG EA Pro](https://www.mql5.com/en/market/product/105739), 4,63 Sterne bei 37 Bewertungen: keine Zahlen. Reviews berichten von Break-even nach 2 Monaten bzw. rund 18 % pro Jahr nach Optimierung.
- [ExpertSMC](https://www.mql5.com/en/market/product/112543): Martingale und „SmartRecovery“ als Features. Laut Reviews sind die Default-Sets unprofitabel.
- [MachinePRO](https://www.mql5.com/en/market/product/164802): SMC-Etikett, aber ADR-Grid, Recovery-Logik und Stealth-SL.
- [BoS SMC EA](https://www.mql5.com/en/market/product/119022), gratis, vom Artikelautor: Ein Review meldet ein invertiertes RR (SL = 7 × TP).
- [Liquidity Sweeper](https://www.mql5.com/en/market/product/161755): saubere Regelbeschreibung, aber keine Zahlen.

**Fazit:** Der Market liefert keine verwertbare Evidenz für einen Edge. Brauchbar sind nur Feature-Ideen: Spreadfilter, Daily/Total-Drawdown-Guards, News-Filter, Partial Close. „SMC“ dient oft als Etikett für Grid-, Recovery- oder Pyramiding-Systeme.

---

## 6. Lessons Learned

**Was leicht, was schwer zu automatisieren ist**

| Baustein | Schwierigkeit | Kern |
|---|---|---|
| FVG (3 Kerzen) | leicht | 1 Bar Lag; Größenfilter und Lifecycle sind die eigentliche Arbeit |
| PDH/PDL, PWH/PWL, Session-Highs/Lows | leicht | nur abgeschlossene Perioden; Serverzeit, Sommerzeit, Sonntagskerzen |
| Fraktal- und Leg-Pivots | leicht | Lag = Bestätigungsbars; keine Retraktion; Outside Bars |
| BOS (Close über unbroken Swing) | leicht–mittel | `crossed`-Flag nötig; Internal vs. Swing |
| CHoCH | mittel | braucht Trend-Zustand. LuxAlgo (zustandsbasiert) und joshyattridge (4-Swing-Muster) liefern verschiedene Labels |
| EQH/EQL, Pools | mittel | ATR-Toleranz, Merging, Relevanz |
| Order Block | mittel–schwer | mindestens 5 konkurrierende Definitionen: Extremkerze, letzte Gegenkerze, Konsolidierungsrange, Kerzenmuster, Base→Impulse |
| Mitigation-Lifecycle | mittel | Semantik je Implementierung verschieden (Touch / Durchbruch / Close); Asymmetrie-Bugs |
| Displacement | mittel | ATR zum OB-Zeitpunkt messen, sonst erhöht der Impuls seine eigene Schwelle |
| HTF→LTF-Kopplung | schwer | Zeitpunkt der HTF-Bestätigung, Synchronisation |
| Inducement, Dealing Range, „Narrative“ | schwer | diskretionär, viele Freiheitsgrade, Overfitting |
| Sweep-Interpretation | schwer | Evidenz widerspricht dem Lehrbuch (Continuation statt Umkehr) |

**Typische Bugs**
1. Zentrierte Fenster oder `shift(-n)` (joshyattridge `swing_highs_lows` und `fvg`).
2. Dedup, das Swings nachträglich zurückzieht.
3. Statistiken über den ganzen Datensatz oder kumulativ (`pip_range`; LuxAlgo `cum/bar_index`). Ergebnisse hängen dann vom Start der Historie ab.
4. Ereignisse auf der Ursprungsbar statt auf der Bestätigungsbar abgelegt (joshyattridge `ob` und `bos_choch`).
5. Die sich noch bildende Bar 0 gelesen (KVignesh122; Artikel 18669, Erkennung am ersten Tick).
6. HTF-Daten mit Lookahead (LuxAlgo HTF-FVG). In MQL5 nur Shift ≥ 1 der HTF-Reihe als „abgeschlossen“ behandeln.
7. Uneinheitliche oder asymmetrische Mitigation (LuxAlgo bärisches FVG; joshyattridge `MitigatedIndex` i−1 vs. i; Löschen während der Iteration).
8. Top und Bottom vertauscht (joshyattridge Default-OB; LuxAlgo „top“ beim bärischen FVG).
9. MQL5-Array-Bugs: parallele Arrays mit `ArrayRemove(…,0,1)`, exakte Preisgleichheit, Verfall abhängig von `CHART_VISIBLE_BARS`, Objektlimit 100.
10. Einheiten: „Pips“ × `_Point`, feste Punkte über Instrumente hinweg, Sell-SL von Ask gerechnet, unerreichbarer Partial Close.
11. Zustandslose Erkennung feuert denselben BOS wiederholt.
12. Zeitzonen: feste UTC-Fenster, manueller Broker-Offset. **Im MT5-Tester gilt `TimeGMT()` = simulierte Serverzeit** ([Doku](https://www.mql5.com/en/docs/dateandtime/timegmt)).
13. Zonen-Explosion: LuxAlgo-FVG-Liste ohne Cap; Indikatoren, die bei jeder Bar alles neu scannen (Artikel 23539).

**Bewährte Datenstrukturen und Muster**
- Pivot-Struct: `{level, lastLevel, crossed, originTime, confirmTime}`.
- Trend-Bias pro Layer.
- Zone-Struct: `{id, type, dir, top, bottom, ce, originTime, createdTime, atrAtCreation, state, touches}`.
- Gekappte Listen, neueste vorn (LuxAlgo: 100).
- Bar-Identität über die Bar-Zeit, nicht über den Shift.
- Inkrementelle Verarbeitung pro geschlossener Bar mit **demselben Codepfad** für Warmup und Live.
- Trennung von committed und working state.
- Detektion → Events → Strategie → genau ein Order-Modul (MrOwl1011: nur `SMC_OB_TradeHooks.mqh` sendet Orders).
- Zeichnen getrennt und nur im visuellen Modus.

**Testprotokoll (bewährt)**
- History-Invarianz: Historie an mehreren Stellen abschneiden. Kein Ergebnis darf rückwirkend erscheinen.
- Batch und bar-by-bar müssen identisch sein.
- Replay-Zähler für umgeschriebene Werte muss 0 sein.
- Strukturereignisse gegen den parity-getesteten LuxAlgo-Port bzw. PineTS abgleichen.
- Real Ticks mit Kosten. In-Sample/Out-of-Sample, Walk-forward, Korrektur für Mehrfachtests, Block-Bootstrap.
- **Baseline mit Zufallszonen** (fehlt bisher selbst im besten Report).
- Ergebnisse in R-Multiples; Plausibilitätsrechnung (PF aus Trefferquote und RR).

---

## 7. Empfehlung für den EA

**Übernehmen**
1. **Struktur-Engine nach LuxAlgo-Muster, kausal neu implementiert**
   - `leg(size)` mit Bestätigung nur auf der rechten Seite. Ursprung und Bestätigungszeit getrennt speichern.
   - Zwei Layer: Internal 5 und Swing. Swing 50 bedeutet auf M15 etwa 12,5 h Lag, daher je TF wählen.
   - Close-Crossover mit `crossed`-Flag. CHoCH/BOS über den Trend-Bias.
   - Internal-Bruch unterdrücken, wenn das Level gleich dem Swing-Level ist.
2. **OB = Extremkerze zwischen gebrochenem Pivot und Bruchkerze** (LuxAlgo)
   - Alternativ als Parameter: „letzte Gegenfarbenkerze ohne Gegenkerzen im Leg“ (MrOwl1011).
   - Hochvolatilitätskerzen (Range ≥ 2 × ATR) explizit ausschließen statt den Swap-Trick zu nutzen.
   - Displacement-Check mit der ATR zum OB-Zeitpunkt.
3. **Explizites, symmetrisches Zonen-Lifecycle-Modell** für OB und FVG: FRESH → TOUCHED → CE → INVALIDATED (Close oder Wick, Parameter) → optional Breaker/IFVG, plus EXPIRED nach Alter in Bars oder ATR-Distanz.
4. **FVG auf geschlossenen Bars (1–3)**
   - Mindestgröße als ATR-Anteil.
   - Optional die LuxAlgo-Displacement-Bedingung (Close der Mittelkerze jenseits Kerze 1, dazu ein Body-Filter), aber mit **rollierendem** statt kumulativem Fenster.
5. **Liquidity**
   - EQH/EQL mit 0,1 × ATR(200) auf 3er-Pivots.
   - Pools nach Artikel 24184 zusammenführen.
   - PDH/PDL, PWH/PWL und Session-Extrema nur aus abgeschlossenen Perioden (Logik wie `previous_high_low`).
   - Sweep als Sequenz mit ATR-Mindestpenetration.
6. **Premium/Discount** = 50 % der aktuellen Swing-Range (Trailing Extremes).
7. **Zeitlogik**
   - NY-Zeit nach US-Sommerzeitregeln (Muster wie Part 51/52).
   - Broker-Offset live aus `TimeGMT()`; im Tester per Parameter oder Tabelle.
8. **ATR-relative Schwellen** überall, um die 25 Instrumente vergleichbar zu machen. Risiko pro Trade in R über Tick Value normieren.
9. **Hypothesen empirisch offen halten**
   - Sweep → Umkehr oder Fortsetzung (SSRN).
   - Trendfilter als dominanter Faktor (MrOwl1011).
   - Einheitliche Parameter über Symbole statt Whitelisting.
10. **Architektur und Tests wie in Abschnitt 6.** Den LuxAlgo-MQL5-Port nur als Testreferenz nutzen.

**Nicht übernehmen**
- joshyattridge-Funktionen als Signalquelle (außer `previous_high_low` und `sessions` als Logikvorlage).
- Von LuxAlgo:
  - HTF-FVG via `lookahead_on[0]`
  - `cum/bar_index`-Schwellen
  - die Confluence-Formel
  - die asymmetrische FVG-Löschung
  - „Mitigation = Löschung“ ohne Touch-Tracking
  - unbegrenzte FVG-Liste
  - die 5-%-Premium/Discount-Bänder als Regel
- Aus den MQL5-Artikeln:
  - Konsolidierungs-OBs mit festen Punkten (7 Bars / 50 Punkte)
  - feste SL/TP in Punkten
  - parallele Arrays
  - Verfall über `CHART_VISIBLE_BARS`
  - Marktorder ohne Spread- und Stop-Level-Prüfung
- Market-Features: Grid, Recovery, Martingale, Pyramiding, Stealth-SL.
- Lizenz:
  - LuxAlgo-Code ist CC BY-NC-SA. Für Verkauf oder Weitergabe nicht portieren, sondern die Konzepte eigenständig implementieren (keine Rechtsberatung).
  - MIT-lizenziert: joshyattridge, MrOwl1011 – nutzbar mit Copyright-Hinweis.
  - Apache-2.0: KVignesh122.

**Erwartungsmanagement:** Die stärkste verfügbare Evidenz ist der MrOwl1011-Report (H1→M5, Trendfilter): etwa +0,10 bis 0,15 R pro Trade bei 1:1, **vor Kosten**.

Meine eigene Abschätzung, unter der Annahme von H1-OB-Höhen um 10–15 Pips und rund 1 Pip Round-Trip-Kosten: Die Kosten liegen dann bei etwa 0,07–0,1 R pro Trade und können einen Großteil dieses Edges aufzehren. Die akademischen und unabhängigen Tests finden für „SMC wie gelehrt“ keinen Edge.
