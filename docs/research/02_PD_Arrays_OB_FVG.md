<!-- Kapitel 2: PD Arrays (Order Blocks, FVG, Displacement, OTE, POI-Scoring) | Deep-Research-Rohbericht (Recherche-Agent), Stand 2026-10-24, unverändert übernommen -->

# Teilbereich PD Arrays / POIs: objektive, programmierbare Regeln

**Quellenlage (vorab, für die Bewertung wichtig)**
- **ICT-Primärquellen:** Videos und Transkripte waren per Web nicht im Volltext abrufbar. Wörtlich belegt ist nur ICTs X-Post zu NWOG/NDOG/CE. ICT-Aussagen mit Video-ID und Zeitstempel stammen aus der GitHub-Wissensbasis *SrsBlack/ict-knowledge-library*. Das ist ein LLM-gepflegtes Drittprojekt, die Zeitstempel habe ich nicht gegen die Videos geprüft. Im Text markiert als **[ICT/Lib]**. Dazu kommen Mitschriften der 2022-Mentorship (TanjaTrades).
- **Code-Primärquellen:**
  - LuxAlgo-Pine: SMC v1 in der „Enhanced“-Fassung (Gist) und eine Kopie des IFVG-Codes
  - Python-Port *joshyattridge/smart-money-concepts*
  - MQL5-Artikel
- **Grenzen:** Mein Web-Search-Budget war gegen Ende aufgebraucht. Die Interna der aktuellen LuxAlgo-SMC-Version (2024) habe ich nicht verifiziert.
- **Grundbefund:** ICT nennt fast keine Zahlen. Displacement definiert er ausdrücklich nur als „energetic“ vs. „lethargic“. Alle Schwellen unten sind daher Engineering-Vorschläge: ATR-normalisiert und per Walk-Forward zu kalibrieren.

---

## 1. Order Blocks (OB)

### 1.1 Definitionen im Vergleich

| Variante | Kerzenwahl | Zone | Pflichtbedingungen | Mitigation / Invalidierung |
|---|---|---|---|---|
| **ICT 2016** [ICT/Lib, Trading-Patiently-Thread] | Bullish: tiefste Down-Close-Kerze mit dem größten Open–Close-Range nahe HTF-Support. Bearish spiegelbildlich. | – | „Validiert“, wenn eine spätere Kerze durch das Hoch handelt (bearish: durch das Tief). | keine explizite Regel |
| **ICT 2017** [ICT/Lib] | „The bodies only, not the wicks“. Eine Serie gleichfarbiger Kerzen ist **ein** Block. Steckt ein Mini-Body im Body des Nachbarn, wird die größere Kerze genommen. | Bodies. MT = 50 % der **zusammengefassten** Bodies. | HTF-Level-Bezug. HTF-Blöcke sind mehrfach handelbar. | – |
| **ICT 2022** [TanjaTrades-Notes, ICT/Lib] | „A change in the state of delivery“: konsekutive Down-Close-Kerzen direkt vor einem Preisschub mit Imbalance. Live wird die preisnächste Kerze referenziert. | Entry am **Opening Price** des OB, +3 Ticks für den Spread. | Imbalance ist Pflicht: „Without the imbalance, there is no order block“ (EP18, nicht wörtlich verifiziert). MSS ist nur ein Qualitätsmerkmal (EP03). | – |
| **SMC-Community** | letzte gegenläufige Kerze vor dem Displacement | Full Range (am häufigsten), Body oder Open→Extrem. LuxAlgo: „none is official“. | BOS/CHoCH per Close, FVG im Leg, vorheriger Sweep (teils Pflicht, teils Bonus), unmitigiert. Strengste Lesart: jeder Wick-Touch gilt schon als mitigiert. | Close durch die ganze Zone → invalid, Breaker-Kandidat. Teils schon ein Body-Close jenseits des MT. |
| **LuxAlgo SMC (Pine v1)** | Nach `crossover(close, swingHigh)`: Bar mit dem **tiefsten Low** (bullish) bzw. **höchsten High** (bearish) zwischen Pivot+1 und Break-Bar−1. Bars mit `high−low ≥ 2·ATR(200)` (alternativ 2× kumulativer Ø-Range) sind ausgeschlossen. **Kerzenfarbe egal.** | Full Range dieser Bar | Jeder OB hängt an einem Close-Break (internal `len=5`, swing `len=50`). | Enhanced-Fork: Wick-Tap von außen setzt das Flag „mitigated“. Gelöscht wird bei `close < bottom` (bull) bzw. `close > top` (bear). |
| **smart-money-concepts (Python)** | wie LuxAlgo, bei Gleichstand die letzte Bar | Full Range | Close-Break | Default: „Breaker“, sobald `low < bottom`. Mit `close_mitigation`: Body statt Wick. Reset bei `high > top`. |
| **LuxAlgo Order Block Detector** | Volumen-Pivots | Low→Median (bull) | – | wählbar: Wick oder Close |

**Widersprüche**
1. **Kerzenwahl:** „letzte gegenläufige Kerze“ (ICT/Community) vs. „Bar mit dem Extremum“ (LuxAlgo). Beides fällt oft, aber nicht immer zusammen, z. B. wenn das tiefste Low eine bullische Kerze mit langem Docht ist.
2. **Einzel- vs. Mehrkerzen:**
   - 2016: Einzelkerze mit dem größten Body
   - 2017/2022: die ganze Serie
   - 2022 live: die preisnächste Kerze
3. **Zonengrenzen:** Body vs. Full Range vs. Open→Extrem.
4. **MT:** Die Mehrheit nimmt 50 % des Bodys (Community-„ICT Gem“, ictkillzone). Andere nehmen 50 % der ganzen Kerze; laut einer Antwort unter dem LumiTraders-Tweet tat das ICT selbst in einem Video. innercircletrader.net macht es bei Propulsion Blocks ebenso.
5. **„Mitigated“:**
   - ICT: Preis kehrt in den Block zurück. Das ist positiv und der Entry-Moment.
   - LuxAlgo, Python-Port: Block gebrochen oder gelöscht.
   - **Folge für den EA:** das Wort nicht verwenden, nur explizite Zustände (Abschnitt 8).
6. **Sweep:** Pflicht bei ictkillzone und TradeZella, Qualitätsfaktor bei Velotrade und auf der LuxAlgo-Konzeptseite.

### 1.2 Empfohlene Detektion (Hybrid ICT + LuxAlgo)
Auslöser ist ein bullisches Struktur-Event `ev` aus dem Struktur-Modul: Close über den bestätigten Swing High `s` auf der Break-Bar `b`.

1. **Leg-Ursprung:** `legLow = argmin low[j]` für `j ∈ (s, b]`, bei Gleichstand die späteste Bar (wie LuxAlgo). Optional werden Bars mit `range ≥ 2·ATR(200)` übersprungen (LuxAlgo-Filter).
2. **Displacement-Start `d`:** erste bullische Bar ≥ `legLow`, ab der das Leg das Displacement-Kriterium aus Abschnitt 4 erfüllt.
3. **OB-Kerze `k`:** die letzte Down-Close-Kerze (`close < open`) im Fenster `[max(s+1, legLow−2), d−1]`.
   - Gibt es keine, gilt der LuxAlgo-Fallback `k = legLow` mit Flag `noOpposite` (Score-Abzug).
4. **Mehrkerzen:** die Serie zusammenhängender Down-Close-Kerzen vor `k` bis maximal `maxRun` (Default 3) dazunehmen. Die Zone ist die Union.
5. **Validierung:**
   - `Displacement(k+1 … min(b, k+3)) = ok`
   - **Trade-through:** ein Close im Leg über `hiFull` (ICT 2016, robuster als nur ein Wick)
   - **FVG im Leg:** Default Pflicht, gemäß ICT 2022; als Parameter abschaltbar
6. **Features für das Scoring** (Abschnitt 7): Displacement-Stärke, FVG adjazent oder nur im Leg, Struktur-Level (internal/external), Sweep, Zeitpunkt der Entstehung.

### 1.3 Zonengeometrie (alles speichern, Entry-Modell parametrisierbar)
- **Gespeicherte Werte:** `hiFull`, `loFull`, `bodyHi = max(O,C)`, `bodyLo = min(O,C)` über die Serie, `openRef`.
- **MT:** `MT_body = (bodyHi+bodyLo)/2`, zusätzlich `MT_full = (hiFull+loFull)/2`.
- **Default „Hybrid“** (beschrieben auf der LuxAlgo-Anatomy-Seite):
  - Entry-Zone = Body, proximal = `bodyHi` (= ICT-„Opening Price“)
  - MT = `MT_body`
  - Stop-Referenz = `min(loFull, low[legLow])` minus Puffer
- **Zu große Zone:** Ist `hiFull−loFull > maxH·ATR`, auf den Body verkleinern. Reicht das nicht, LTF-Refinement (1.5).

### 1.4 Mitigation, Invalidierung, Alterung
- **TOUCHED:** Wick erreicht proximal. **MT_REACHED:** Wick erreicht MT.
- **WEAKENED:** ein Body-Close jenseits des MT. Danach keine neuen Entries. ICT: „MT should not give way“ gilt explizit für Propulsion und wird von vielen auf OBs übertragen.
- **INVALIDATED:** Close jenseits von distal (Full Range). Das deckt sich mit LuxAlgo v1 und dem Konsens „decisive close through“.
- **Alterung:** ICT gibt keine Regel vor; HTF-Blöcke sind mehrfach handelbar (2017). Vorschlag:
  - `maxAge` je Timeframe
  - `maxTouches`: LTF 1, H1/H4 2, D1 3
  - Pruning nach Distanz, wenn die Zone weiter als 15·ATR vom Kurs entfernt ist

### 1.5 Refined OB (LTF)
- **(a) Nested:** Auf dem LTF die Bars mit `time ∈ [htfOB.time, htfOB.time + PeriodSeconds(HTF))` durchsuchen. Darin per Regel 1.2 den LTF-OB bzw. das LTF-FVG suchen, die den HTF-Leg einleiten. Das Ergebnis ersetzt die HTF-Entry-Zone; die Stop-Referenz bleibt HTF-distal.
- **(b) Confirmation:** Erst nachdem der Preis die HTF-Zone berührt hat, auf einen LTF-CHoCH warten und dessen OB/FVG handeln. Die Quellen nennen typisch H4/D1 → M15/M5 bzw. M15 → M1.

**Quellen Abschnitt 1:**
- https://gist.github.com/niquedegraaff/8c2f45dc73519458afeae14b0096d719
- https://www.tradingview.com/script/CnB3fSph-Smart-Money-Concepts-SMC-LuxAlgo/
- https://raw.githubusercontent.com/joshyattridge/smart-money-concepts/master/smartmoneyconcepts/smc.py
- https://www.luxalgo.com/library/concept/bullish-bearish-order-block/
- https://www.luxalgo.com/library/concept/order-block-anatomy-and-refinement/
- https://www.tradingview.com/script/KvGhxGxY-Order-Block-Detector-LuxAlgo/
- https://docs.luxalgo.com/platform/algos/price-action-concepts/order-blocks
- https://github.com/SrsBlack/ict-knowledge-library (concepts/07-order-blocks/order-block-criteria.md)
- https://www.scribd.com/document/666181194/ICT-2022-Mentorship-Notes-TanjaTrades
- https://en.rattibha.com/thread/1758939804388012497
- https://x.com/tradngpatiently/status/1683266752468119552
- https://twitter.com/LumiTraders/status/1701255772812759160
- https://www.ictkillzone.com/ict-order-block
- https://www.tradezella.com/learning-items/key-ict-concepts
- https://dailypriceaction.com/blog/order-blocks/
- https://velotrade.com/blog/order-block
- https://algoalpha.io/blog/order-block-trading-strategy
- https://www.mql5.com/en/articles/22078

---

## 2. Abgeleitete Blöcke

### 2.1 Breaker Block
- **ICT [ICT/Lib, 2016 Breaker]:** Ein Stop-Run, gefolgt von einem Strukturbruch.
  - Bullish: altes Low L1 → Swing High H, darin Up-Close-Kerze(n) = bearischer OB → Lower Low L2 < L1 (Sweep) → Bruch über H.
  - „A bearish breaker is a … down close candle in the most recent swing low“.
  - Zone: **„we're using the entire range“**, also die Full Range.
  - „The breaker has precedence over everything“ (2017).
- **Community/LuxAlgo:** Lockerere Lesart: jeder gebrochene OB ist ein Breaker. LuxAlgo-Option „Use Candle Body“.
- **Namenskonflikt:** LuxAlgo-PAC und der Python-Port benennen Breaker nach dem **ursprünglichen** OB-Typ: Ein „bullish breaker“ wirkt dort als Widerstand. ICT benennt nach der neuen Handelsrichtung. **Der EA nutzt die ICT-Konvention.**
- **Regel:** Bei einem bärischen Close-Break des Swing Lows L:
  - `H1` = letzter bestätigter Swing High vor L
  - `H2` = höchstes Hoch zwischen L und Break
  - `H2 > H1` → **BREAKER**, Zone = Full Range der Down-Close-Kerze(n) an L (Kerzenwahl wie 1.2)
  - `H2 ≤ H1` → **Mitigation Block** (2.2)
  - Zusätzlich: Displacement auf dem Bruch-Leg nötig
  - Invalidierung: Close jenseits der Gegenseite (LuxAlgo: „trade back through the whole zone“)

### 2.2 Mitigation Block
- **ICT [ICT/Lib, 2016]:** Failure Swing: das vorherige Extrem wird nicht erreicht (M/W-Muster), danach bricht die Struktur. Zone = **nur der Body** der gegenläufigen Kerze am gebrochenen Swing („classic support broken turns resistance“). Mitigation Blocks liegen meist näher am Preis als Breaker.
- **Widersprüche:**
  - LuxAlgo nimmt die letzte Up-Close-Kerze vor dem **gescheiterten Lower High**.
  - tradingstrategyguides nimmt den Bereich zwischen gebrochenem Low und Lower High.
  - innercircletrader.net definiert ganz anders („unmitigated swing point“).
- **Empfehlung:** die ICT-Variante, also dieselbe Routine wie 2.1 mit `sweep=false` und Body-Zone. Die LuxAlgo-Variante als Option.

### 2.3 Rejection Block
- **ICT [ICT/Lib, 2017]:** An alten Hochs/Tiefs mit langen Dochten. Das Level liegt **an der Body-Kante**, nicht an der Docht-Spitze: „it doesn't need to go through the wicks“. Eine Cluster-Form über mehrere gleich hohe Bodies ist möglich.
- **LuxAlgo-Indikator (Defaults):**
  - Swing mit 10 Bars je Seite
  - Docht ≥ 50 % des Kerzen-Range und ≥ 0,5·ATR(14)
  - Zone bearish: Body-Top → High (bullish spiegelbildlich)
  - wird erst „armed“, wenn der Preis die Zone verlässt
  - invalid bei Body-Close jenseits des Extrems
- **Regel:** wie LuxAlgo, dazu ein Cluster: Bars ±1 um den Pivot, deren High ≥ Pivot-High − 0,1·ATR.
  - `level = max Body-Top` des Clusters, `extreme = max High`
  - Signal: Preis handelt über `level` und schließt wieder darunter
  - Option `requireSweep`: der Pivot hat ein älteres Hoch genommen

### 2.4 Propulsion Block
- **ICT [ICT/Lib, 2016]:** Eine Down-Close-Kerze, die in einen bestehenden bullischen OB **hineinhandelt** und von dort „sudden and violent“ wegschiebt.
  - Entry-Referenz: das High der PB-Kerze
  - MT = 50 % des **Bodys**: „it should never see the mean threshold break“
- **Widerspruch:** innercircletrader.net nimmt den MT über die Full Range.
- **Regel:**
  - für einen ACTIVE/TOUCHED bullischen OB: Down-Close-Bar `j` mit `low[j] ≤ OB.proximal` und `close[j] ≥ OB.distal`
  - bestätigt, wenn innerhalb von 3 Bars ein Close über `high[j]` folgt
  - Zone = Body/High von `j`
  - invalid bei Close < `MT_body(j)`

### 2.5 Vacuum Block
- **ICT [ICT/Lib, 2016 Vacuum Block]:** „A vacuum block is nothing more than a breakaway gap“. Es ist eine Lücke durch ein Volatilitätsereignis (Opening, News).
  - Grenzen: Open der Gap-Kerze und Close der Kerze davor
  - nicht jede Lücke wird gefüllt
- **Widersprüche:** LuxAlgo führt „Vacuum Block“ als **Alias für Rejection Block**. ictkillzone setzt ihn einer großen Liquidity Void gleich.
- **Empfehlung:** ICT-konform als Close→Open-Gap mit Größenfilter ≥ `kVac·ATR`. Ursache taggen: Wochenende, Tagesbreak oder News.

### 2.6 Reclaimed OB
- **ICT [ICT/Lib, 2016, Teaching 3.4]:** Im Market-Maker-Buy-Model entstehen bullische OBs auf der Sell-Side-Kurve (Down-Close-Kerzen vor kleinen Rallies). Kehrt der Preis auf der Buy-Side zurück, werden sie „reclaimed“: „these old blocks or down candles will be reclaimed for new longs“.
- **Community/LuxAlgo:** ein OB, der verletzt und danach wieder respektiert wird.
- **Regel (Approximation, deckt beide ab):**
  - ein INVALIDATED-OB, bei dem innerhalb von `maxReclaimBars` ein Close zurück über proximal folgt
  - zusätzlich ein MSS in die Original-Richtung
  - → `RECLAIMED_OB` mit gleichen Grenzen und Original-Richtung
  - Eine echte MMBM-Kontextprüfung braucht das Modell-Modul.

**Quellen Abschnitt 2:**
- ict-knowledge-library: concepts/08-breaker-blocks/*, 19-rejection-blocks/rejection-block.md, 07-order-blocks/{propulsion,vacuum,reclaimed}-*.md
- https://www.luxalgo.com/library/concept/breaker-block/
- https://www.luxalgo.com/library/concept/mitigation-block/
- https://www.luxalgo.com/library/concept/rejection-block/
- https://www.luxalgo.com/library/indicator/rejection-block/
- https://www.luxalgo.com/library/concept/propulsion-block/
- https://www.luxalgo.com/library/concept/reclaimed-order-block/
- https://www.tradingview.com/script/piIbWMpY-Order-Blocks-Breaker-Blocks-LuxAlgo/
- https://innercircletrader.net/tutorials/ict-propulsion-block/
- https://www.ictkillzone.com/ict-propulsion-block
- https://www.ictkillzone.com/ict-vacuum-block
- https://tradingfinder.com/education/forex/ict-vacuum-block/
- https://innercircletrader.net/tutorials/ict-reclaimed-order-block/

---

## 3. Fair-Value-Gap-Familie

### 3.1 FVG: Definition und Mindestgröße
- **ICT Core Content (Monat 4):** „a range in Price Delivery where one side of the Market Liquidity is offered“, typischerweise durch eine Liquidity Void auf dem LTF bestätigt.
- **Bezeichnungen:** BISI = bullish, SIBI = bearish.
- **Kerzen:** `c1` (älteste), `c2` (mittlere, Displacement), `c3` (jüngste):
  - **bullish:** `low[c3] > high[c1]`, Zone `[high[c1], low[c3]]`
  - **bearish:** `high[c3] < low[c1]`, Zone `[high[c3], low[c1]]`
- **ICT-Entry:** „just above candle number three's high“ (bearish), also an der Kante. Der CE ist optional: „I don't need that“ (EP18) [ICT/Lib].

**Zusatzfilter im Code verschiedener Quellen:**

| Quelle | Bedingung |
|---|---|
| LuxAlgo (FVG, SMC, IFVG) | zusätzlich `close[c2] > high[c1]` (bull) |
| Python-Port | `c2` bullisch (`close > open`) |
| LuxAlgo FVG (veröffentlichte Kopie) | `(low[c3]−high[c1])/high[c1] > thr`; Auto: `ta.cum((high−low)/low)/bar_index`. Laut Changelog später gelockert. |
| LuxAlgo SMC | Body-% von `c2` > 2·Ø\|Body-%\| (Auto), nur auf neuen Bars des FVG-Timeframes |
| LuxAlgo IFVG | Gap > 0,25·ATR(200) |
| MQL5 #23539 | Gap ≥ 0,5·SMA(TR,14), nur geschlossene Bars |
| MQL5 #22078 | Gap > 10 Points (absolut, nicht portierbar) |

**Empfehlung:**
- `gap ≥ max(kFVG[tf]·ATR14, 3·Median-Spread)`
- `close[c2]` jenseits des Extrems von `c1` (bull: `close[c2] > high[c1]`, bear: `close[c2] < low[c1]`)
- Body/Range von `c2` ≥ 0,5
- Flag `strong`, wenn `c2` das volle Displacement-Kriterium (Abschnitt 4) erfüllt

### 3.2 CE, Fill und Mitigation
- **CE** = (top+bot)/2. Laut ICTs X-Post der „middle point of any gap or inefficiency“.
- **ICT [ICT/Lib]:**
  - Begriffe: „rebalance“, „closed in“, „fill“; Teilfüllungen sind normal
  - Wicks durch die Zone invalidieren nicht zwingend (EP09: „does this invalidate the fair value gap? no it does not“)
  - keine Zeitgrenze
- **Code-Konventionen widersprechen sich:**

| Quelle | Wann gilt die FVG als erledigt? |
|---|---|
| LuxAlgo SMC | Löschung beim Wick-Fill der Gegenkante |
| LuxAlgo-Konzept | „violated“ erst bei einem **Close** jenseits der Gegenkante → IFVG-Kandidat |
| Python-Port | „mitigated“ schon bei der ersten Berührung |
| MQL5 #23539 | wählbar: Wick-Touch (nahe Kante) oder Close-Through (ferne Kante) |

- **Empfehlung (vier getrennte Zustände):**
  - TOUCHED: Wick an der nahen Kante
  - CE_REACHED: Wick am CE
  - FILLED: Wick an der fernen Kante → kein Entry mehr, bleibt für die IFVG-Erkennung
  - INVALIDATED: Body-Close jenseits der fernen Kante → IFVG
  - Zusätzlich `maxPen` (tiefste Penetration) speichern.

### 3.3 Inverse FVG (IFVG)
- **LuxAlgo-Code:**
  - Inversion einer bullischen FVG, wenn `min(O,C) < bot`
  - IFVG gelöscht, wenn `max(O,C) > top`
  - Retest-Signal: (Close-Modus `close[1]`, Wick-Modus `high`) in der Zone und `close < bot`
  - Defaults: Close-Modus, ATR-Multiplikator 0,25, Show Last 5
- **Community:** Body-Close durch die ferne Kante; ein Wick allein ist eine „Probe“. „A gap that has flipped twice is noise.“
- **ICT-Korpus:** dünn belegt, das Konzept ist im Wesentlichen Community- und Code-Standard.
- **Regel:** wie LuxAlgo. Keine IFVG aus einer IFVG.

### 3.4 Balanced Price Range (BPR)
- **LuxAlgo:** Überlappung einer aktuellen bullischen und einer bärischen FVG innerhalb von „Bars to Look Back“, mit einem Mindestwert „BPR Threshold“. Bullish BPR = bärische FVG, danach eine überlappende bullische.
- **ICT-Herkunft:** im Korpus nicht belegt; 2017 gibt es nur „price balanced range“ im Sinn einer Konsolidierung. Also eine Mehrdeutigkeit.
- **Regel:**
  - beim Entstehen einer FVG `f`: Gegen-FVG `g` mit `|c2(f)−c2(g)| ≤ bprLB` und nicht invalidiert
  - Zone = Schnittmenge, Breite ≥ 0,1·ATR
  - Richtung = die der jüngeren FVG

### 3.5 Volume Imbalance (VI)
- **Definition:** Body-Gap bei überlappenden Wicks.
  - bull: `min(O,C)[n] > max(O,C)[n−1]` und `low[n] ≤ high[n−1]`
  - Zone `[max(O,C)[n−1], min(O,C)[n]]`
- **Herkunft:** Den Begriff fand die Lib nicht im 2016/2022-Korpus. 2016 heißt das „common gap“ („where the bodies don't close in“); ICT handelte damit einen 2-Pip-Body-Gap.
- **FX-Hinweis:** Im kontinuierlichen Spot-FX gilt meist `open[n] ≈ close[n−1]`. VIs entstehen dort fast nur an Session-Übergängen oder bei News, und der Bid-Feed verzerrt sie.
- **Empfehlung:** Mindestgröße `max(2·Tick, 0,05·ATR)`. Vor allem als Konfluenz nutzen (FVG-Verkettung, FPFVG), nicht als eigenständiger Entry.

### 3.6 Liquidity Void (LV)
- **Herkunft:** ICT 2016 „Liquidity Voids“. Mehrkerzige einseitige Bewegung, die mehrere FVGs enthält. Keine ICT-Zahlen; die 80 %/30 %-Werte der Lib sind deren eigene Setzung.
- **Vorschlag:**
  - ≥ 3 gleichgerichtete Kerzen, Body/Range ≥ 0,6
  - jede Kerze mit `low > Mitte der Vorkerze` (bull)
  - Netto ≥ 2·ATR, mindestens eine FVG darin
  - Zone `[low erste, high letzte]`, CE = Mitte
  - primär als Draw/Target nutzen

### 3.7 Opening Gaps (NWOG / NDOG)
- **ICT, primär (X-Post):**
  - „NWOG: Difference between Friday's Close Price & Sunday's Open Price“
  - „NDOG: … between 5pm Close Price & 6pm Open Price“
  - CE = Mittelpunkt
  - Lib (EP34): Liegt der Preis über der NWOG → Support, darunter → Resistance.
- **Spot-FX:** handelt über 17:00 NY durch. Ein NDOG existiert nur, wo der Broker eine Tagespause hat. Das per `SymbolInfoSessionTrade()` auslesen, nicht hart codieren; bei XAUUSD typischerweise vorhanden.
- **Anzahl:** die letzten 5 NDOG (Community/2024-Lecture-Notes) und die letzten 4 NWOG halten.

### 3.8 First Presented FVG (FPFVG)
- **Belege:** nur sekundär, Ära 2023–25.
- **Definition:** die erste FVG nach 09:30 NY im Fenster 09:30–10:00, M1 als Referenz.
  - ictkillzone: alle drei Kerzen im Fenster
  - PoorTomTrading: eine erste Kerze um 09:29 zählt nicht; FVGs, die durch VIs getrennt sind, werden verkettet; weitere Fenster 00:00–00:30 und 01:30–02:00
- **Regel:** pro konfiguriertem Anker die erste qualifizierte M1-FVG → Flag `FPFVG` mit Score-Bonus, gültig bis Session-Ende.

### 3.9 Zusammenfassen benachbarter FVGs
- **Python-Port** `join_consecutive`: Union bei aufeinanderfolgenden FVGs gleicher Richtung.
- **PoorTomTrading:** verkettet FVGs mit VIs dazwischen.
- **ICT 2022 (Notes):** Bei zwei FVGs kann der Preis in die tiefere tauchen und danach die flachere respektieren. Also beide einzeln handelbar halten.
- **Empfehlung:**
  - ein `Cluster`-Objekt als Union, genutzt für Invalidierung, LV und Target
  - Kinder mit eigenem CE und Zustand, genutzt für Entries
  - zusammengefasst wird, wenn die `c2`-Indizes höchstens 1 Bar auseinanderliegen und die Lücke ≤ 0,05·ATR ist oder per VI überbrückt wird

**Quellen Abschnitt 3:**
- https://x.com/I_Am_The_ICT/status/1623531900366118912
- https://medium.com/@badrdata37/ict-fvg-fair-value-gap-d0a2949fd11c
- https://www.luxalgo.com/library/concept/fair-value-gap/
- https://www.luxalgo.com/library/concept/fvg-behavior-rules/
- https://www.tradingview.com/script/OCiww9Rz-Fair-Value-Gap-LuxAlgo-With-ANY-alert/
- https://www.tradingview.com/script/8FHucjY6-Inversion-Fair-Value-Gaps-IFVG-LuxAlgo/
- https://www.prorealcode.com/topic/traduction-code-ifvg-de-luxalgo/
- https://www.luxalgo.com/library/concept/inversion-fvg/
- https://www.luxalgo.com/library/indicator/856oabwc-balanced-price-range-bpr/
- https://www.mql5.com/en/articles/23539
- https://github.com/joshyattridge/smart-money-concepts
- ict-knowledge-library: 06-fair-value-gaps/*, 09-displacement/gap-classification.md, 31-models/{nwog,ndog}.md
- https://liquidityscan.io/blog/what-is-a-volume-imbalance-body-gaps-vs-fair-value-gaps
- https://innercircletrader.net/tutorials/master-ict-liquidity-void/
- https://fibalgo.com/library/ict-opening-gaps
- https://innercircletrader.net/tutorials/ict-2024/ict-2024-mentorship-lecture-3/
- https://www.ictkillzone.com/ict-1st-presented-fvg
- https://www.tradingview.com/script/IK86l33L-ICT-s-First-Presented-Fair-Value-Gaps/

---

## 4. Displacement

**ICT [ICT/Lib]:** keine numerische Definition.
- „it's got to be energetic, it can't be a little lethargic little move“ (EP06)
- „toe in the water … that's not enough“ (EP40)
- „a big beefy bearish candle that closes … below this level“ (EP06)
- Die FVG wird **innerhalb** des Displacements als Entry-Gate gesucht (EP06). Displacement ohne FVG bleibt trotzdem gültig (EP10).

**Code- und Educator-Varianten:**

| Quelle | Regel |
|---|---|
| TFO „Visualizing Displacement“ | Range (Default O–C) > 4·stdev(Range,100); optional „Require FVG“ |
| Qvintrix | Body ≥ 1,5·ATR (bewusst Body, damit Pin-Bars bzw. Sweeps rausfallen) |
| FibAlgo OB | Body > k·ATR; bei 2–3 gleichgerichteten Kerzen die kumulierte Body-Summe |
| FibAlgo MM-Model | Body/Range ≥ 0,65 und Range ≥ 0,8·ATR |
| ictkillzone | Range ≥ 2× (oft 3–5×) der Ø-Kerze; Body/Range > ~0,75 |
| Backtrex | Body/Range > 0,60 plus messbare FVG |
| LuxAlgo v1 | umgekehrt: Bars mit Range ≥ 2·ATR(200) sind als OB-Kandidat ausgeschlossen |

**Vorschlag `Displacement(a..b)`** (1–3 Bars, gleiche Richtung). Erfüllt, wenn D1–D3 gelten:
- **D1:** Σ|C−O| ≥ `k1·ATR14` (eine Bar) bzw. ≥ `k3·ATR14` (2–3 Bars)
- **D2:** jede Kerze Body/Range ≥ 0,5, Mittelwert ≥ 0,6
- **D3:** `close[b]` jenseits der Referenz (gebrochener Swing oder OB-Extrem)
- **D4 (optional, Flag „strong“):** mindestens eine FVG im Leg
- **Alternative zu D1:** Z-Score `range > μ + 2,5σ` über 100 Bars
- **Stärke für das Scoring:** `dispATR = Σbody/ATR`

**Quellen Abschnitt 4:**
- ict-knowledge-library: 09-displacement/{displacement-definition,displacement-strength-criteria}.md
- https://easycators.com/porting-visualizing-displacement-pinescript-thinkscript/
- https://www.tradingview.com/script/mekKJPQl-ICT-Order-Blocks-Qvintrix/
- https://www.tradingview.com/script/TTeQ7rTf-FibAlgo-ICT-Order-Blocks/
- https://fibalgo.com/library/ict-market-maker-model
- https://www.ictkillzone.com/ict-displacement
- https://backtrex.com/en/blog/ict-displacement-candle-market-concept
- https://tiomarkets.com/en/article/displacement-forex-trading-guide

---

## 5. Premium/Discount, Equilibrium, OTE

**ICT [ICT/Lib]:**
- **Dealing Range:** „the most energetic most recent low and high“ (EP19), also ein Impuls-Leg in Handelsrichtung (EP34). Bei neuem Struktur-Swing wird neu verankert (EP38). EQ = 50 % (EP11).
- **OTE:** „62, 70.5, and 79%“ (2016). Der Stop liegt am Leg-Ursprung, also Fib 1,0.
- **Anker-Widerspruch:**
  - ICT 2017/2020: Bodies [ICT/Lib], aber in einem Review auch einmal der Wick
  - ictkillzone, Backtrex: Wick-Extrem (Sweep-Docht)
  - tradingstrategyguides: Body zu Body
  - Gemeinsam ist allen: nur bestätigte Swings, und das Leg, das die Struktur gebrochen hat

**LuxAlgo:**
- **Code:** Premium-Box = oberste 5 % der Trailing-Range, EQ-Band 47,5–52,5 %, Discount = unterste 5 %. Das ist nur Visualisierung und **nicht** der 50/50-Split.
- **Konzeptseite:** Die Range wird bei einem Close jenseits eines Extrems verworfen. `Position = (P−Low)/(High−Low)`.

**Vorschlag:**
- **Externe DR** (HTF, Swings des Struktur-Moduls): nur als Bias-Filter. Longs nur bei `pos < 0,5`.
- **Interne DR** (Setup-Timeframe):
  - `lo` = Ursprung des BOS/MSS-Legs (bevorzugt das Sweep-Tief)
  - `hi` = laufendes Maximum seit dem Break
  - OTE-Entries erst, wenn `hi` als Pivot bestätigt ist (kein Look-ahead)
- **Zonen** (für Longs, Shorts gespiegelt):
  - Discount: `pos < 0,5`
  - OTE: `pos ∈ [0,21; 0,38]`, entspricht Retracement 0,62–0,79
  - Sweet Spot: 0,295
  - EQ-Band 0,475–0,525: kein Entry
- **Parameter:** `fibAnchor = WICK | BODY` (Default WICK; der robustere Community-Standard, ICT-nähere Variante BODY im Backtest prüfen). Exakte ICT-Werte 0,62/0,705/0,79 verwenden.
- **Reset:** ein Close jenseits eines Ankers, oder ein neuer BOS in Richtung → neues Leg.

**Quellen Abschnitt 5:**
- ict-knowledge-library: 05-pd-arrays/dealing-range.md, 17-optimal-trade-entry/ote-rules.md
- https://www.luxalgo.com/library/concept/premium-and-discount/
- Gist (Zonenformeln, siehe Abschnitt 1)
- https://liquidityscan.io/blog/how-to-draw-a-dealing-range-in-ict-correctly
- https://www.ictkillzone.com/ict-ote
- https://tradingstrategyguides.com/understanding-ict-optimal-trade-entry-ote/
- https://proea.app/en/blog/ict-optimal-trade-entry
- https://thesimpleict.com/premium-vs-discount-ict-smart-money/

---

## 6. Beziehung zu klassischen Supply/Demand-Zonen

**Seiden/OTA-Logik:**
- **Aufbau:** Leg-in, Base, Leg-out.
  - Base-Kerze: Body ≤ 50 % des Range (streng ≤ 25 %)
  - Leg-out: Body > 50 % (streng 70–75 %)
  - höchstens 5 Base-Kerzen
- **Zeichnung:** eine Base-Kerze wick-to-wick; 2–5 Base-Kerzen body-to-wick.
- **Odds Enhancer (Punkte/10):**
  - Strength of Departure: 2
  - Time at Level: 1, weniger Kerzen sind besser
  - Freshness: 2/1/0 für den 1./2./3. Test
  - Profit Margin: ≥ 3:1
  - Big Picture, Ankunftsweise
  - Bewertung: ≥ 8 = handelbar, 9–10 = Limit-Order

**Verhältnis zum OB:**
- Der ICT-OB ist meist die präzise Teilzone, also die letzte Gegenkerze innerhalb bzw. am Ende der Base.
- Zusätzlich verlangt der OB Displacement plus Imbalance bzw. Strukturbruch. S/D verlangt keinen BOS.
- Algostorm sieht OBs als umbenannte S/D-Zonen.

**Empfehlung:**
- eine gemeinsame Zonen-Engine: S/D = Base-Cluster ohne BOS-Pflicht; OB = Teilzone mit BOS und Imbalance
- Seidens Enhancer direkt als Scoring-Features übernehmen: Departure ≈ Displacement, Time at Level ≈ `runLen`, Freshness ≈ `touches`, Profit Margin ≈ Raum zum Ziel

**Quellen Abschnitt 6:**
- https://forums.babypips.com/t/odd-enhancers-sam-seiden/39321
- https://www.moneyshow.com/articles/daytraders-24494/
- https://twpstudentportal.com/wp-content/uploads/2023/07/Supply-and-Demand-Step.docx.pdf
- https://vn.tradingview.com/script/KDXMpXnB-Supply-and-Demand-Dashboard-tambangEA
- https://forexbee.co/supply-and-demand-forex/
- https://www.luxalgo.com/library/concept/zone-scoring-and-refinement/
- https://algostorm.com/ict-smc-key-concepts/
- ict-knowledge-library: 07-order-blocks/order-block-vs-supply-demand.md

---

## 7. POI-Qualitätsbewertung (Scoring-Vorschlag)

**Belege für Konfluenzen:**
- Sweep davor, FVG im Leg, richtige Range-Seite, HTF-Alignment: LuxAlgo-Konzept, Quantum-Algo
- Nesting LTF-Array in HTF-Array: ICT 2017 [ICT/Lib]
- Breaker-Vorrang: ICT 2017
- Seiden-Enhancer (Abschnitt 6)
- Bestehende Code-Modelle:
  - FvgGold-EA: Gap 30, Displacement 30, HTF 20, Freshness 10, P/D 10, OB-Konfluenz +20
  - LuxAlgo-Library-Text (nur Suchauszug, nicht verifiziert): Grade A/B/C aus ATR-normierter Displacement und relativem Volumen gegenüber dem 20-Bar-Ø. In FX gibt es nur Tick-Volumen, daher allenfalls niedrig gewichten.

**Harte Gates** (alle müssen erfüllt sein):
1. Zustand ∈ {ACTIVE, TOUCHED, MT_REACHED} und nicht WEAKENED
2. Richtung nicht gegen den HTF-Bias
3. Zonenhöhe nach Refinement ≤ `maxH·ATR`
4. R:R ≥ 2 bis zum nächsten gegenüberliegenden Liquiditätsziel (Entry proximal oder MT, Stop distal + Puffer + Spread)

**Score 0–100** (alle Features `f ∈ [0,1]`):

| Feature | Gewicht | Bewertung f |
|---|---|---|
| Displacement-Stärke | 20 | `clamp((dispATR − k)/k)` |
| FVG | 15 | adjazent 1 · im Leg 0,6 · keine 0 |
| Strukturbruch | 15 | external BOS/MSS 1 · internal 0,6 |
| Sweep vor Entstehung | 15 | externer Swing/EQH/EQL/PDH/PDL 1 · interner Swing 0,5 |
| Premium/Discount | 10 | OTE 1 · Discount 0,7 · EQ-Band 0,2 · falsche Seite 0 |
| HTF-Konfluenz | 10 | in gleichgerichtetem HTF-Array „nested“ 1 · nur Bias 0,5 |
| Freshness | 5 | unberührt 1 · berührt < MT 0,5 · MT erreicht 0 |
| Überlappung | 5 | OB∩FVG oder Breaker∩FVG 1 |
| Zeit | 5 | in Killzone entstanden 1 (London 02–05, NY 07–10 NY-Zeit) |

**Modifikatoren:**
- Alterung ×`(1 − 0,5·age/maxAge)`
- `noOpposite` −5
- FPFVG +5
- Typ-Prior (subjektiv, optional): Breaker 1,0 · OB 0,95 · FVG 0,9 · MB/RB/IFVG 0,85 · VI 0,6

**Grades:** A ≥ 75, B 60–74, kein Trade < 60 (LTF strenger, siehe Tabelle). Die Gewichte sind Startwerte. Kalibrieren per logistischer Regression auf das Label „+2R vor −1R nach Touch“, pro Timeframe und Instrumentengruppe (Majors, Crosses, JPY, XAU).

**Quellen Abschnitt 7:**
- https://github.com/foeed/FvgGold-EA
- https://www.luxalgo.com/library/indicator/SRsr9SLs-smart-money-concepts/
- https://www.quantum-algo.com/blog/guides/order-blocks-complete-trading-guide/
- ict-knowledge-library: 05-pd-arrays/pd-array-matrix.md, 06-fair-value-gaps/nested-fvg.md

---

## 8. Pseudocode: Erkennung, Lebenszyklus, Speicherung

### 8.1 Zustände (bullish beschrieben, bearish gespiegelt)

| Zustand | Eintritt | Wirkung |
|---|---|---|
| CREATED | Detektion auf geschlossener Bar | nicht handelbar |
| ACTIVE | erste Bar mit `low > proximal` (Zone verlassen, „armed“) | Entries erlaubt |
| TOUCHED | `low ≤ proximal`, beim Eintritt von außen `touches++` | Entry-Trigger |
| MT_REACHED | `low ≤ mid` (MT bzw. CE) | fresh = false |
| WEAKENED | `close < mid` (OB, PB, MB) | keine neuen Entries |
| FILLED | `low ≤ distal` (nur Gaps) | keine Entries |
| INVALIDATED | `close < distal` (Gaps: Body) | Konversion |
| CONSUMED | `touches > maxTouches` und Zone wieder verlassen | archivieren |
| EXPIRED | `age > maxAge` | löschen |

### 8.2 Code

```cpp
enum ZType  { OB, BREAKER, MITBLK, REJECT, PROPUL, RECLAIM, FVG, IFVG, BPR, VI, LVOID, NWOG, NDOG, VACUUM };
enum ZState { CREATED, ACTIVE, TOUCHED, MT_REACHED, WEAKENED, FILLED, INVALIDATED, CONSUMED, EXPIRED };

struct Zone {
  long id; int sym, tf; ZType type; int dir;          // dir +1 = Support/Long, -1 = Resistance/Short
  datetime tOrigin, tCreated, tInvalid;
  double top, bot, mid;                               // Handelszone + MT/CE
  double hiFull, loFull, bodyHi, bodyLo, stopRef;
  ZState state; int touches; bool inside; double maxPen;
  long parent;                                        // OB->Breaker, FVG->IFVG, Cluster->Kind
  double dispATR; bool hasFVG, fvgAdj, sweep, noOpp, fpfvg, inKZ; int bosLvl; double score;
  double proximal() { return dir>0 ? top : bot; }
  double distal()   { return dir>0 ? bot : top; }
};

class ZoneStore {                                     // eine Instanz je (Symbol, TF)
  Zone z[]; int cap[ZTYPES];                          // Kappung je Typ und Richtung (Tabelle)
  void Add(Zone &n){ if(!OverlapsSameTypeDir(n)) Push(n); else KeepNewer(n); PruneByCapAndDistance(); }
};
ZoneStore Store[NSYM][NTF];

void OnTimer() {                                      // z. B. jede Sekunde; Arbeit nur bei neuer geschlossener Bar
  for(s in Symbols) for(tf in TFs) if(NewClosedBar(s,tf)) {
     MqlRates r[]; CopyRates(s, tf, 1, NBARS, r);     // nur geschlossene Bars (Shift >= 1)
     double atr = ATR14(s,tf,1), spr = MedianSpread(s,tf);
     ZoneStore &S = Store[s][tf];
     UpdateLifecycle(S, r[last], atr);                // ZUERST bestehende Zonen fortschreiben (kein Self-Touch)
     DetectGaps(S, r, atr, spr);                      // FVG/VI/Vacuum/NWOG/NDOG, danach BPR, Merge
     for(ev in Structure.NewEvents(s,tf)) {           // BOS/CHoCH/MSS per Close (fremdes Modul)
        DetectOB(S, r, ev, atr);
        DetectBreakerOrMB(S, r, ev, atr);
     }
     DetectRejection(S, r, atr); DetectPropulsion(S, r, atr);
     ScoreAll(S, Context(s));                          // DR-Position, HTF-Nesting, Killzone usw.
  }
}

void DetectGaps(ZoneStore &S, MqlRates &r[], double atr, double spr) {
  int c3 = last, c2 = last-1, c1 = last-2;
  double minG = MathMax(P.kFVG[tf]*atr, 3*spr);
  if(r[c3].low > r[c1].high && r[c2].close > r[c1].high && BodyRatio(r[c2]) >= 0.5 &&
     r[c3].low - r[c1].high >= minG)
     S.Add(MakeGap(FVG, +1, r[c1].high, r[c3].low, r[c2]));       // mid = CE
  /* bearish gespiegelt; VI: min(O,C)[n] > max(O,C)[n-1] && low[n] <= high[n-1];
     Vacuum/NWOG/NDOG: close[vor Pause] vs. open[nach Pause] (Pausen via SymbolInfoSessionTrade);
     BPR: Schnittmenge mit Gegen-FVG innerhalb bprLB Bars;
     Merge: Cluster-Union plus Kinder; FPFVG-Flag, wenn erste FVG nach Anker */
}

void DetectOB(ZoneStore &S, MqlRates &r[], StructEvent ev, double atr) {
  if(ev.dir != +1) { MirrorBear(...); return; }
  int legLow = ArgMinLowLatest(r, ev.pivotIdx+1, ev.breakIdx, P.skipHighVol ? 2*ATR200 : INF);
  int d = FirstDisplacementStart(r, legLow, ev.breakIdx, atr);   // Abschnitt 4
  if(d < 0) return;                                              // kein Displacement -> kein OB
  int k = -1;
  for(int j=d-1; j>=MathMax(ev.pivotIdx+1, legLow-2); j--) if(r[j].close < r[j].open) { k=j; break; }
  bool noOpp = (k < 0); if(noOpp) k = legLow;
  int k0 = k; while(k-k0 < P.maxRun-1 && k0-1 > ev.pivotIdx && r[k0-1].close < r[k0-1].open) k0--;
  Zone z; Fill(z, OB, +1, r, k0, k);                             // Union aus hiFull/loFull/bodyHi/bodyLo
  z.stopRef = MathMin(z.loFull, r[legLow].low);
  if(z.hiFull - z.loFull > P.maxH[tf]*atr) { z.top = z.bodyHi; z.bot = z.bodyLo; }
  else                                     { z.top = z.bodyHi; z.bot = z.loFull; } // Hybrid
  z.mid = (z.bodyHi + z.bodyLo)/2;                               // MT_body
  bool tt  = AnyCloseAbove(r, k+1, ev.breakIdx, z.hiFull);       // Trade-through
  Disp ds  = Displacement(r, k+1, MathMin(ev.breakIdx, k+3), atr);
  z.hasFVG = FvgInRange(S, +1, k, ev.breakIdx, z.fvgAdj);
  if(!(ds.ok && tt && (z.hasFVG || !P.requireFVG))) return;
  z.dispATR = ds.atrMult; z.bosLvl = ev.level; z.noOpp = noOpp;
  z.sweep = Liquidity.SweptBelow(r[legLow].low, legLow, P.sweepLB[tf]);
  z.state = CREATED; S.Add(z);
}

void DetectBreakerOrMB(ZoneStore &S, MqlRates &r[], StructEvent ev, double atr) {
  // Beispiel bärischer Bruch des Swing Lows L (ev.dir == -1):
  double H1 = Structure.LastSwingHighBefore(ev.pivotIdx);
  double H2 = HighestHigh(r, ev.pivotIdx, ev.breakIdx);
  if(!Displacement(r, LegStart(ev), ev.breakIdx, atr).ok) return;
  int k = LastOppositeRunAt(r, ev.pivotIdx);                      // Down-Close-Kerze(n) an L
  Zone z = (H2 > H1) ? MakeFromRun(BREAKER, -1, r, k, /*fullRange*/true)
                     : MakeFromRun(MITBLK , -1, r, k, /*body*/false);
  z.parent = FindOBAt(S, k); z.state = CREATED; S.Add(z);
}

void UpdateLifecycle(ZoneStore &S, MqlRates b, double atr) {
  for(Zone &z : S.z) {
    if(z.state >= INVALIDATED) { WatchReclaim(S, z, b); continue; }
    if(BarsSince(z.tCreated) > P.maxAge[tf][z.type]) { z.state = EXPIRED; continue; }
    double px  = z.dir>0 ? b.low : b.high;            // Wick
    double cl  = z.dir>0 ? (IsGap(z) ? MathMin(b.open,b.close) : b.close)
                         : (IsGap(z) ? MathMax(b.open,b.close) : b.close);
    bool beyond = z.dir>0 ? px <= z.proximal() : px >= z.proximal();
    if(z.state == CREATED) { if(!beyond) z.state = ACTIVE; continue; }
    if(beyond && !z.inside) { z.touches++; if(z.state == ACTIVE) z.state = TOUCHED; }
    z.inside = beyond;
    if(beyond) z.maxPen = MathMax(z.maxPen, Pen(z, px));          // 0 proximal, 0.5 MT, 1 distal
    if(Reached(z, px, z.mid) && z.state < MT_REACHED) z.state = MT_REACHED;
    if(IsGap(z) && Reached(z, px, z.distal())) z.state = FILLED;
    if(IsBlock(z) && Crossed(z, b.close, z.mid)) z.state = WEAKENED;
    if(Crossed(z, cl, z.distal())) {
      z.state = INVALIDATED; z.tInvalid = b.time;
      if(z.type == FVG) S.Add(Invert(z));                         // IFVG, gleiche Grenzen, dir = -dir
    }
    if(z.touches > P.maxTouches[tf][z.type] && !beyond) z.state = CONSUMED;
  }
  // Breaker/MB entstehen über Struktur-Events; RECLAIM: Close zurück über proximal plus MSS
}
```

**Betriebsregeln**
- **Neustart:** Zonen deterministisch durch Replay aus der Historie rekonstruieren (`maxAge + 300` Bars je TF). Kein Datei-Cache nötig.
- **Bid/Ask:** MT5-Kerzen sind Bid-basiert. Für Long-Touches und Long-Entries den Spread addieren (ICT: „+3 ticks for spread“).
- **HTF-Zonen:** nur aus geschlossenen HTF-Bars bilden.
- **Pivots:** Bestätigung mit `right-len` Bars Verzögerung. Das muss in Backtests identisch nachgebildet werden.
- **Killzone/NY-Zeit:** Broker-Serverzeit → NY-Zeit umrechnen, mit US-Sommerzeit.

### 8.3 Default-Parameter (Startwerte, zu kalibrieren)

| Parameter | M1 | M5 | M15 | H1 | H4 | D1 |
|---|---|---|---|---|---|---|
| ATR-Periode | 14 | 14 | 14 | 14 | 14 | 14 |
| Swing internal / external (LuxAlgo-Logik; LuxAlgo-Default 5/50) | 5/50 | 5/50 | 5/40 | 5/30 | 5/20 | 3/10 |
| FVG min (×ATR), zusätzlich ≥ 3×Spread | 0,30 | 0,25 | 0,20 | 0,15 | 0,12 | 0,10 |
| Displacement, 1 Bar Body (×ATR) | 1,5 | 1,4 | 1,3 | 1,2 | 1,1 | 1,0 |
| Displacement, 2–3 Bars Σ Body (×ATR) | 2,2 | 2,0 | 1,9 | 1,8 | 1,6 | 1,5 |
| Body/Range Ø min | 0,6 | 0,6 | 0,6 | 0,55 | 0,55 | 0,5 |
| OB maxRun (Kerzen) | 3 | 3 | 3 | 3 | 2 | 2 |
| OB maxH Full Range (×ATR), darüber Refinement | 1,5 | 1,5 | 1,5 | 2,0 | 2,0 | 2,5 |
| maxAge OB (Bars) | 240 | 288 | 192 | 240 | 180 | 120 |
| maxAge FVG (Bars); D1/H4 alternativ bis Fill | 120 | 144 | 96 | 120 | 120 | 60 |
| maxTouches OB | 1 | 1 | 1 | 2 | 2 | 3 |
| Kappung Zonen je Typ und Richtung | 20 | 20 | 25 | 30 | 30 | 30 |
| Sweep-Lookback (Bars) | 60 | 60 | 50 | 50 | 40 | 30 |
| BPR-Lookback / min. Overlap (×ATR) | 10 / 0,1 | 10 / 0,1 | 10 / 0,1 | 8 / 0,1 | 6 / 0,1 | 5 / 0,1 |
| RB-Swing / Docht min | 10 / 50 % & 0,5 ATR | 10 / dito | 8 / dito | 8 / dito | 5 / dito | 5 / dito |
| maxReclaimBars | 30 | 30 | 24 | 20 | 15 | 10 |
| Score-Schwelle | 70 | 65 | 60 | 60 | 60 | 60 |

---

## 9. Offene Mehrdeutigkeiten und Empfehlung für den EA

1. **OB-Kerze (letzte Gegenkerze vs. Extremum-Bar):** Hybrid aus 1.2. Fallback auf die Extremum-Bar mit Score-Abzug. Beide Varianten im Backtest vergleichen.
2. **Einzel- vs. Mehrkerzen-OB:** Union der Serie (max. 3). Option „last candle only“ (Refined).
3. **Body vs. Full Range, MT-Basis:** Hybrid: Entry-Zone und MT aus dem Body, Stop aus Wick bzw. Leg-Low. `MT_full` als Parameter.
4. **„Mitigated“:** den Begriff nicht verwenden. Nur explizite Zustände aus 8.1.
5. **Invalidierung OB:** hart = Close jenseits distal (Full Range). Weich = Close jenseits des MT, dann keine neuen Entries.
6. **FVG-Ende:** FILLED (Wick an der fernen Kante) und INVALIDATED (Body-Close) getrennt führen. LuxAlgo-SMC-Verhalten (Löschung schon beim Wick-Fill) als Option.
7. **Sweep als Pflicht?** Default: Score-Faktor (15 Punkte). Für Breaker ist der Sweep definitorisch Pflicht.
8. **FVG als OB-Pflicht?** Default Pflicht (ICT 2022). Abschalten, falls die Zahl der Signale bei M1/M5 zu klein wird.
9. **Breaker-Benennung und Zone:** ICT-Richtungskonvention. Full Range als Default (ICT „entire range“), Body als Option.
10. **Mitigation Block** (Swing-Low-Body vs. Lower-High-Kerze): ICT/Lib-Variante als Default. LuxAlgo-Variante nur im Test.
11. **Vacuum Block:** ICT-konform als Gap/Breakaway. Den LuxAlgo-Alias (Rejection Block) ignorieren.
12. **Reclaimed OB:** die Approximation „invalidiert → zurückerobert + MSS“. Echter MMBM-Kontext erst mit dem Modell-Modul.
13. **BPR und IFVG:** ICT-Herkunft schwach belegt. Mit niedrigerem Typ-Prior aufnehmen, Wirksamkeit per Backtest belegen.
14. **NDOG im Spot-FX:** nur, wo `SymbolInfoSessionTrade` eine echte Tagespause zeigt (meist XAUUSD). NWOG für alle Instrumente.
15. **OTE-Anker (Body vs. Wick):** Default Wick. Body (ICT 2017/2020 laut Lib) als A/B-Test.
16. **Displacement-Zahlen:** keine ICT-Vorgabe. Die ATR-Regeln aus Abschnitt 4. Alternative Z-Score. Die Schwellen je Timeframe und Instrumentengruppe optimieren, Overfitting per Walk-Forward kontrollieren.
17. **Alterung und Wiederverwendung:** keine ICT-Regel. Tabellenwerte verwenden, HTF-Zonen mehrfach nutzbar.
18. **Volumen-basierte Kriterien** (LuxAlgo-Grades, Python `OBVolume`): In FX/CFD gibt es nur Tick-Volumen. Höchstens als schwaches Zusatzfeature.
19. **Nicht verifiziert:**
    - ICT-Zitate und Zeitstempel aus der Lib
    - die LuxAlgo-SMC-v2-Interna
    - die LuxAlgo-A/B/C-Grade-Regeln

    Im EA nichts davon als „ICT-Regel“ fest verdrahten. Alles parametrisieren und Backtest-Evidenz entscheiden lassen.
