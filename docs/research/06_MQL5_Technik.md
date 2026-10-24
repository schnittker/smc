<!-- Kapitel 6: Technische MQL5-Umsetzung (Multi-Symbol/Multi-TF) | Deep-Research-Rohbericht (Recherche-Agent), Stand 2026-10-24, unverändert übernommen -->

# Technische MQL5-Umsetzung: Multi-Symbol-/Multi-Timeframe-SMC-EA (25 Instrumente)

## 1. Architektur

### 1.1 Ein Portfolio-EA oder 25 Chart-Instanzen

| Kriterium | 1 EA für alle 25 Symbole | 1 Instanz pro Chart |
|---|---|---|
| Ticks | `OnTick` feuert nur für das Chart-Symbol, die übrigen Symbole müssen gepollt werden | natives `OnTick` je Symbol |
| Threads | ein Thread („each Expert Advisor runs in its own separate thread“), alle Symbole laufen seriell | 25 parallele Threads |
| Risiko/Exposure | zentral und konsistent, ohne Interprozess-Kommunikation | Koordination über `GlobalVariableSetOnCondition` oder Dateien nötig, Race Conditions bei gleichzeitigen Entries |
| Backtest | ein Multi-Currency-Lauf liefert Portfolio-Equity samt Korrelations-Drawdowns | der Tester führt nur einen EA aus, das Portfolio entsteht erst durch Zusammenführen der Reports |
| Fehlerisolation | ein Critical Error (array out of range, Division durch 0, ungültiger Pointer) beendet den EA sofort und damit den Handel auf allen 25 Symbolen | nur ein Symbol fällt aus |
| Parameter je Symbol | Datei plus `#property tester_file`, weil Input-Strings begrenzt sind (laut MQL5-Book in der Optimierung auf 63 Zeichen gekürzt) | normale Inputs je Chart |

**Empfehlung:** ein Portfolio-EA mit gekapselten `SymbolContext`-Modulen und einer einzigen Risk-/Exposure-Schicht. Über einen Input wie `InpSymbols="EURUSD"` muss derselbe Code auch als Einzelinstanz laufen, für Debugging und Einzeloptimierung. Defensive Bounds- und Pointer-Checks sind Pflicht, denn ein einziger Laufzeitfehler stoppt das ganze Portfolio.

### 1.2 Ereignismodell und Ticks fremder Symbole

- **OnTick:** „tick events are generated only for one symbol, which is the symbol of the current chart.“ Ein NewTick wird nicht eingereiht, solange bereits einer in der Queue liegt oder verarbeitet wird. Ticks gehen dabei verloren, `OnTick` ist also kein Handler für jeden Tick.
- **OnTimer:** `EventSetTimer` oder `EventSetMillisecondTimer`, nur ein Timer pro Programm, Auflösung 10–16 ms. Liegt schon ein Timer-Event in der Queue, wird kein neues angehängt. Im Tester läuft `OnTimer` unabhängig vom Modus in Simulationszeit. Beispiel aus der Doku: H4, Open prices, 1-s-Timer ergibt 14 400 `OnTimer`-Aufrufe pro Bar.
- **OnBookEvent** (`MarketBookAdd`): BookEvents werden nie verworfen, sie werden immer eingereiht (Flutgefahr) und an alle Programme des Charts gebroadcastet. Viele FX-Broker liefern kein echtes DOM, und das Tester-Verhalten ist nicht dokumentiert. Als Tick-Ersatz ungeeignet.
- **Spy-Indikator** (`iCustom` je Symbol, `EventChartCustom` → `OnChartEvent`): live mit geringer Latenz, im Tester aber widersprüchlich dokumentiert. Laut Doku verarbeitet ein EA im Tester Custom Events. Das MQL5-Book sagt dagegen, `OnChartEvent` werde im Tester nicht aufgerufen, auch nicht im visuellen Modus. Forum-Nutzer berichten, dass es im Backtest nicht funktioniert. Höchstens als Live-Optimierung einsetzen.
- **Empfehlung:** ein zentraler `Dispatch()`, aufgerufen aus `OnTimer` (live 250–500 ms) und aus `OnTick`. Als Chart- und Tester-Symbol ein liquides Paar wie EURUSD wählen.
  - Pro Symbol `SymbolInfoTick()` abfragen; Positionsmanagement nur, wenn sich `tick.time_msc` geändert hat.
  - Strukturberechnung über New-Bar-Polling.
  - SL/TP liegen serverseitig, Polling genügt daher.
  - Für Tick-genaue Sweep-Analysen `CopyTicks` ab dem letzten `time_msc`. Der Cache hält 4096 Ticks; der erste Aufruf synchronisiert und kann in EAs bis zu 45 s warten, gehört also nicht in den Startpfad.

### 1.3 New-Bar-Erkennung pro Symbol/TF (Codeskizze)

```mql5
struct SBarKey { string sym; ENUM_TIMEFRAMES tf; datetime lastOpen; datetime lastProcessed; };

class CBarClock
{
   SBarKey m_k[];
public:
   int Register(const string sym, const ENUM_TIMEFRAMES tf)
   {
      int n = ArraySize(m_k); ArrayResize(m_k, n + 1, 64);
      m_k[n].sym = sym; m_k[n].tf = tf; m_k[n].lastOpen = 0; m_k[n].lastProcessed = 0;
      return n;
   }
   // true = seit letztem Poll neue Bar eröffnet; danach geschlossene Bars ab shift 1 lesen
   bool Poll(const int i, datetime &newOpen)
   {
      long t = 0;
      if(!SeriesInfoInteger(m_k[i].sym, m_k[i].tf, SERIES_LASTBAR_DATE, t) || t == 0)
         return false;                              // Daten noch nicht bereit
      if((datetime)t == m_k[i].lastOpen) return false;
      const bool first = (m_k[i].lastOpen == 0);
      m_k[i].lastOpen = (datetime)t; newOpen = (datetime)t;
      return !first;                                // erste Beobachtung = nur Initialisierung
   }
   // alle seit letzter Verarbeitung geschlossenen Bars (Catch-up nach Wochenende/Reconnect)
   int ClosedSince(const int i, MqlRates &out[])
   {
      datetime from = (m_k[i].lastProcessed > 0) ? m_k[i].lastProcessed + 1 : m_k[i].lastOpen - 1;
      int n = CopyRates(m_k[i].sym, m_k[i].tf, from, m_k[i].lastOpen - 1, out);
      if(n > 0) m_k[i].lastProcessed = out[n - 1].time;
      return n;                                     // -1/0 => nächster Zyklus
   }
};
```

Regeln dazu:

- Jedes Symbol-TF-Paar braucht eigenen Zustand. Eine einzige `static`-Variable für alle ist der klassische Fehler.
- `SERIES_LASTBAR_DATE` ist billig. `iTime` hat laut Doku keinen Cache.
- Eine neue Bar entsteht erst mit dem ersten Tick nach der Zeitgrenze, in ruhigen Phasen oder Gold-Pausen also verspätet. Bars ohne Ticks existieren nicht.
- Schließen mehrere TFs gleichzeitig, von oben nach unten verarbeiten (D1 → H4 → H1 → M15 → M5), damit der LTF-Entry den aktualisierten HTF-Kontext sieht.
- Catch-up-Bars nur für die Struktur nutzen. Signale nur für „frische“ Bars erzeugen, also solche, die innerhalb der letzten TF-Periode geschlossen haben.
- Symbolübergreifende Logik (SMT-Divergenz EURUSD/GBPUSD, USD-Basket) erst rechnen, wenn alle beteiligten Symbole die neue Bar haben. Im Tester sind die Bars verschiedener Symbole ausdrücklich nicht synchron.

### 1.4 Daten-Synchronisierung

- **OnInit:**
  - Für alle 25 Symbole plus Umrechnungspaare `SymbolExist` und `SymbolSelect(sym,true)` aufrufen. Suffix/Prefix auflösen („EURUSD.r“, „GOLD“).
  - Im Tester lädt `SymbolSelect` in `OnInit` die History vorab; sonst pausiert der Test beim ersten Zugriff.
  - `OnInit` nicht blockieren, weil das Terminal beim Start eventuell noch nicht verbunden ist.
- **Warm-up-State je SymbolContext im Timer:**
  - `SeriesInfoInteger(...,SERIES_SYNCHRONIZED)` prüfen.
  - Liefert `CopyRates(...)` weniger Bars als benötigt, `GetLastError()` auswerten (z. B. 4401 `ERR_HISTORY_NOT_FOUND`, 4403 `ERR_HISTORY_TIMEOUT`, 4404 `ERR_HISTORY_BARS_LIMIT`) und im nächsten Zyklus erneut versuchen.
  - Niemals mit Nullen weiterrechnen.
  - Trading erst freigeben, wenn alle TFs und die Kontraktdaten plausibel sind.
- **CopyRates-Verhalten:**
  - In EAs wartet der Aufruf bis zu einem Timeout und liefert, was bis dahin bereit ist, danach lädt er weiter. Deshalb immer die Anzahl prüfen.
  - Anfragen jenseits von `TERMINAL_MAXBARS` liefern -1. „Max bars in chart“ ausreichend setzen; die Änderung wirkt erst nach Terminal-Neustart.
- **Erste Aufrufe liefern 0:** `SYMBOL_TRADE_TICK_VALUE` und `OrderCalcProfit` liefern bei unsynchronisierten Symbolen beim ersten Aufruf teils 0, ohne Fehler zu setzen.
- **Nachträgliche History-Änderung:** History kann sich nach einem Reconnect oder nach dem Füllen von Lücken ändern. Die letzten Bars periodisch gegen `CopyRates` vergleichen und bei Abweichung neu laden und die Engines neu aufbauen.

**Quellen 1:** https://www.mql5.com/en/book/automation/experts/experts_ontick · https://www.mql5.com/en/book/automation/experts/experts_multisymbol · https://www.mql5.com/en/docs/runtime/running · https://www.mql5.com/en/docs/event_handlers/ontimer · https://www.mql5.com/en/docs/event_handlers/onbookevent · https://www.mql5.com/en/docs/runtime/event_fire · https://www.mql5.com/en/forum/235928 · https://www.mql5.com/en/articles/234 · https://www.mql5.com/en/code/280 · https://www.mql5.com/en/book/automation/tester/tester_chart_limits · https://www.mql5.com/en/articles/159 · https://www.mql5.com/en/articles/14574 · https://www.mql5.com/en/docs/series/timeseries_access · https://www.mql5.com/en/docs/series/copyrates · https://www.mql5.com/en/docs/series/copyticks · https://www.mql5.com/en/docs/constants/errorswarnings/errorcodes · https://www.mql5.com/en/docs/runtime/errors

## 2. Strategy Tester

### 2.1 Mechanik im Multi-Currency-Modus

- **Tick-Sequenzen:** „An individual tick sequence is generated for each symbol“. Neue Bars öffnen je Symbol unabhängig.
- **OnTick:** feuert nur für das im Tester gewählte Symbol. Andere Symbole über `OnTimer` bzw. Polling abfragen.
- **Herkunft der History:**
  - Sie kommt aus dem Terminal, nicht vom Server; nur Fehlendes wird nachgeladen.
  - Für ≤ D1 mindestens 1 Jahr, W1 100 Bars, MN1 96 Monate.
  - Nur Symbole in der Market Watch stehen zur Verfügung.
  - Als Cross-Rates taugen nur Symbole mit Calc-Mode Forex oder Forex No Leverage.
  - Alle Daten vorab herunterladen.
- **Tick-Reihenfolge:** Seit Build 1375 arbeitet der Tester mit Millisekunden. Vorher kamen erst alle Ticks einer Sekunde für Symbol A, dann für B.
- **Every tick based on real ticks:**
  - Echte Ticks werden gegen die M1-Bars validiert. Bei Widerspruch und in Minuten ohne Ticks werden Ticks generiert, es entsteht also ein Mischmodell. Datenqualität pro Symbol prüfen.
  - Der Download für 25 Symbole ist groß.
- **Spread:**
  - Er kommt aus der History.
  - Bei generierten Ticks ist er pro M1-Bar konstant = Bar-Spread. Nach Forum-Aussagen (Alain Verleyen, Fernando Carreiro) ist das der **Minimal-Spread** der Bar, Backtests werden dadurch optimistisch.
  - Spread- und Rollover-Filter nur mit Real Ticks validieren.
  - `SYMBOL_SPREAD_FLOAT` ist im Tester immer true.
- **Weitere Einstellungen:**
  - Delays: Random Delay (laut Doku in 90 % der Fälle 0–8 s) oder Fixed bzw. gemessener Ping.
  - Commission: unter Advanced Settings konfigurierbar.
  - Test-Zeitraum: Start und Ende um 00:00, Startdatum inklusive, Enddatum exklusive; davor werden mindestens 100 Bars geladen.

### 2.2 Eigenheiten, die der Code abfangen muss

- **Zeit:**
  - Im Tester gilt `TimeLocal()` = `TimeTradeServer()` = `TimeGMT()`, und `TimeTradeServer()` = `TimeCurrent()`.
  - Ein Broker-Offset über `TimeTradeServer()-TimeGMT()` ergibt im Tester 0 und verschiebt die Killzones um 2–3 h (siehe §3).
- **Wirtschaftskalender:** Alle `Calendar*`-Funktionen liefern `ERR_FUNCTION_NOT_ALLOWED` (4014).
- **Nicht oder eingeschränkt ausgeführt:**
  - `Print`/`Comment` in der Optimierung nicht (außer in `OnInit`).
  - `Alert`, `SendNotification`, `WebRequest` nie.
  - Grafische Objekte nur im visuellen Modus.
  - `IndicatorRelease()` wird im Tester nicht ausgeführt.
- **GlobalVariables:** pro Agent emuliert, getrennt von den Terminal-GVs.
- **Dateien:**
  - Jeder Agent hat eine eigene Sandbox.
  - `FILE_COMMON` funktioniert nur für lokale Agents.
  - Für Remote- und Cloud-Agents `#property tester_file "x.csv"` oder `#resource` verwenden.
- **Sleep:** verschiebt die Simulationszeit, `TimeCurrent()` bleibt bis zum nächsten Tick stehen. Nach `Sleep` daher `TimeTradeServer()` nutzen.
- **Tick Value:** Bei manchen Brokern liefert er im Tester falsche Werte, z. B. 100.0 für JPY-Crosses statt live ~0.88. Mit `OrderCalcProfit` gegenrechnen (§4).
- **DLLs:** auf Remote-Agents verboten.

### 2.3 Performance-Hebel

- Logik nur bei Bar-Close ausführen. Bykov misst bei 256 Instanzen auf Real Ticks 4:15 min mit Tick-Logik gegenüber 0:25 min mit „only new bars“.
- Every tick ist etwa 10× langsamer als 1-Minute-OHLC. Real Ticks kosten gegenüber Every tick etwa +30 % Zeit und +20 % RAM.
- Logging per Makro abschalten; laut Bykov bringt das 5–10 %.
- Timer-Periode als Input. Im Tester gröber takten oder das Polling an M1-Bar-Wechsel koppeln.
- Workflow:
  1. 1-Minute-OHLC nur zur Grobsuche. Bei Limit-Entry plus engem SL innerhalb derselben Minute ist dieser Modus mehrdeutig.
  2. Bestätigen mit Every tick.
  3. Final validieren mit Real Ticks plus Delay.
- MQL5 Cloud: maximal 4 GB RAM und 4 GB Disk pro Pass.

### 2.4 Optimierung und Forward-Test

- **Genetischer Algorithmus:** Population 64–256, 15–31 Generationen, Abbruch bei Konvergenz.
- **Kriterien:** u. a. Balance, Profit Factor, Drawdown min, Recovery, Sharpe, **Custom max** (Rückgabewert von `OnTester()`, sortiert absteigend), Complex Criterion.
- **Forward:**
  - Anteil 1/2, 1/3, 1/4 oder Custom-Datum; der späte Teil des Zeitraums wird Forward.
  - Getestet werden die besten 25 % (genetisch) bzw. 10 % (vollständige Suche), mindestens 256 Passes.
  - Ein natives Walk-Forward gibt es nicht. Entweder manuell oder als Pipeline nach Bykovs Serie (Python-Stufen).
- **Frames:**
  - `FrameAdd()` in `OnTester` löst im Terminal `OnTesterPass` aus; dort `FrameNext()`.
  - Die Frames landen in einer *.MQD-Datei unter `MQL5\Files\Tester`.
  - Mit `OnTesterInit` lädt der EA auf einem separaten Chart.
  - So lassen sich Kennzahlen je Symbol aus jedem Pass einsammeln.

```mql5
double OnTester()
{
   const double trades = TesterStatistics(STAT_TRADES);
   const double net    = TesterStatistics(STAT_PROFIT);
   const double ddPct  = TesterStatistics(STAT_EQUITY_DDREL_PERCENT);
   if(trades < 150 || net <= 0) return -1.0;                 // zu wenig Evidenz
   double score = net / MathMax(ddPct, 1.0) * MathSqrt(trades / 150.0);
   if(TesterStatistics(STAT_PROFIT_FACTOR) > 5.0) score *= 0.5; // Overfit-Verdacht
   double perSym[]; /* je Symbol in OnTradeTransaction gesammelt */
   FrameAdd("persym", 1, score, perSym);
   return score;
}
```

### 2.5 Custom Symbols

Einsatzzwecke: externe oder längere Tickdaten importieren (`CustomTicksAdd`, `CustomRatesUpdate`), Stresstests mit verbreitertem Spread. Fallstricke:

- `SYMBOL_TRADE_CALC_MODE` **vor** den Währungen setzen. Sonst werden Base- und Profit-Währung aus den Buchstaben 1–3 und 4–6 des Namens abgeleitet.
- Tick Value und Kontraktdaten per Clone aus dem Originalsymbol übernehmen.
- Für `CustomTicksAdd` muss das Symbol in der Market Watch stehen.
- Live sind Custom Symbols nicht handelbar.

**Quellen 2:** https://www.mql5.com/en/docs/runtime/testing · https://www.mql5.com/en/articles/239 · https://www.metatrader5.com/en/terminal/help/algotrading/testing · https://www.metatrader5.com/en/terminal/help/algotrading/tick_generation · https://www.metatrader5.com/en/releasenotes/terminal/1357 · https://www.metatrader5.com/en/terminal/help/algotrading/optimization_types · https://www.metatrader5.com/en/terminal/help/algotrading/strategy_optimization · https://www.mql5.com/en/docs/event_handlers/ontester · https://www.mql5.com/en/docs/optimization_frames · https://www.mql5.com/en/docs/constants/environment_state/statistics · https://www.mql5.com/en/docs/series/indicatorrelease · https://www.mql5.com/en/forum/446070 · https://www.mql5.com/en/forum/390874 · https://www.mql5.com/en/forum/381280 · https://www.mql5.com/en/docs/customsymbols · https://www.mql5.com/en/book/advanced/custom_symbols/custom_symbols_properties · https://www.mql5.com/en/articles/7166

## 3. Zeit: Serverzeit → UTC → New York

### 3.1 Zeitfunktionen

- **`datetime`:** trägt keine Zone. Bar-, Deal- und Kalenderzeiten sind **Serverzeit**.
- **`TimeCurrent()`:** in `OnTick` die Zeit des behandelten Ticks, sonst die letzte Quote irgendeines Market-Watch-Symbols. Friert am Wochenende ein.
- **`TimeTradeServer()`:** wird im Terminal berechnet und hängt von der PC-Uhr ab; läuft am Wochenende weiter.
- **`TimeGMT()`:** aus der lokalen PC-Zeit inklusive DST abgeleitet. Live ist das brauchbar, solange die PC-Uhr per NTP synchron läuft; im Tester ist es wertlos.

### 3.2 Broker-Modelle

- **„NY-Close“ (GMT+2/+3 nach US-DST, sehr verbreitet):**
  - Server = NY + 7 h, ganzjährig.
  - 00:00 Server = 17:00 NY; fünf D1-Kerzen pro Woche.
  - H4-Bars öffnen um 17/21/01/05/09/13 Uhr NY.
- **GMT+2/+3 nach EU-DST:** In den Abweichungswochen gilt NY = Server − 6 h, und die D1-Grenze liegt eine Stunde verschoben.
- **GMT+0 oder fester Offset:** Es gibt Sonntagskerzen; der D1 entspricht nicht dem NY-Tag.
- **DST-Regeln:**
  - US: 2. Sonntag im März bis 1. Sonntag im November, jeweils 02:00 lokal.
  - EU: letzter Sonntag im März bis letzter Sonntag im Oktober, jeweils 01:00 UTC.
- **Abweichungswochen:**
  - 2026: 08.03.–29.03. und **25.10.–01.11.2026, also ab morgen**.
  - 2027: 14.03.–28.03.
- **London-Open in diesen Wochen:** 08:00 London entspricht 04:00 NY statt 03:00. ICT-Killzones sind in NY-Zeit definiert; bewusst entscheiden, ob London-Fenster NY-fix oder London-lokal geführt werden.
- **Eigene Tageskerzen:** PDH/PDL, Midnight Open (00:00 NY) und Wochen-Open selbst aus H1/M15 in NY-Zeit aggregieren. Nicht dem Broker-D1 vertrauen, außer bei einem verifizierten NY-Close-Server.

### 3.3 SessionClock (Codeskizze)

```mql5
enum ENUM_SERVER_TZ { SRV_TZ_NY_CLOSE, SRV_TZ_EU_DST, SRV_TZ_FIXED };

class CSessionClock
{
   ENUM_SERVER_TZ m_model; int m_std;                 // Winter-Offset Server-UTC in Sekunden
   static datetime D(int y,int m,int d){ MqlDateTime s; ZeroMemory(s); s.year=y; s.mon=m; s.day=d; return StructToTime(s); }
   static datetime NthSunday(int y,int m,int n)
   { datetime d1=D(y,m,1); MqlDateTime s; TimeToStruct(d1,s); return d1+(((7-s.day_of_week)%7)+7*(n-1))*86400; }
   static datetime LastSunday(int y,int m)
   { datetime d=(m==12?D(y+1,1,1):D(y,m+1,1))-86400; MqlDateTime s; TimeToStruct(d,s); return d-s.day_of_week*86400; }
public:
   CSessionClock(ENUM_SERVER_TZ model,int stdOffsetH):m_model(model),m_std(stdOffsetH*3600){}
   static bool UsDst(datetime utc){ MqlDateTime s; TimeToStruct(utc,s);
      return utc>=NthSunday(s.year,3,2)+7*3600 && utc<NthSunday(s.year,11,1)+6*3600; }
   static bool EuDst(datetime utc){ MqlDateTime s; TimeToStruct(utc,s);
      return utc>=LastSunday(s.year,3)+3600 && utc<LastSunday(s.year,10)+3600; }
   static datetime UtcToNy(datetime utc){ return utc-(UsDst(utc)?4:5)*3600; }
   static datetime NyToUtc(datetime ny){ datetime u=ny+5*3600; return UsDst(u-3600)? u-3600 : u; } // Grenzfälle = Wochenende
   datetime ServerToUtc(datetime srv) const
   {  switch(m_model){
         case SRV_TZ_NY_CLOSE: return NyToUtc(srv-7*3600);
         case SRV_TZ_EU_DST: { datetime w=srv-m_std; return EuDst(w-3600)? w-3600 : w; }
         default:            return srv-m_std; } }
   datetime UtcToServer(datetime utc) const
   {  switch(m_model){
         case SRV_TZ_NY_CLOSE: return UtcToNy(utc)+7*3600;
         case SRV_TZ_EU_DST:   return utc+m_std+(EuDst(utc)?3600:0);
         default:              return utc+m_std; } }
   datetime ServerToNy(datetime srv) const { return m_model==SRV_TZ_NY_CLOSE? srv-7*3600 : UtcToNy(ServerToUtc(srv)); }
   datetime NyToServer(datetime ny)  const { return m_model==SRV_TZ_NY_CLOSE? ny+7*3600  : UtcToServer(NyToUtc(ny)); }
   int  OffsetSec(datetime srv) const { return (int)(srv-ServerToUtc(srv)); }
   bool CheckLive(string &msg) const                    // nur live sinnvoll
   {  if(MQLInfoInteger(MQL_TESTER)) return true;
      datetime srv=TimeTradeServer();
      int live=(int)MathRound((double)(srv-TimeGMT())/900.0)*900;
      if(live==OffsetSec(srv)) return true;
      msg=StringFormat("TZ-Modell %ds != live %ds",OffsetSec(srv),live); return false; }
   static int MinOfDay(datetime t){ MqlDateTime s; TimeToStruct(t,s); return s.hour*60+s.min; }
};
// Beispiel: London-KZ 02:00–05:00 NY
// int m=CSessionClock::MinOfDay(clk.ServerToNy(TimeTradeServer())); bool lkz=(m>=120 && m<300);
```

### 3.4 Validierung im Tester

Weil `TimeGMT()` im Tester unbrauchbar ist, kommt das Modell aus einem Input und wird an der History geprüft. Der FX-Schluss liegt Freitag um 17:00 NY, die letzte H1-Bar vor dem Wochenende muss also in NY-Zeit um **16:00** öffnen. Diese Prüfung funktioniert auch im Tester; die Wochen sollten die Abweichungswochen enthalten.

```mql5
int TzMismatches(const CSessionClock &clk,const string sym,int weeks)
{  int bad=0; datetime now=TimeTradeServer();
   for(int w=1; w<=weeks; w++){
      datetime p=now-w*7*86400; MqlDateTime s; TimeToStruct(p,s);
      datetime sat=p-(s.hour*3600+s.min*60+s.sec)+((6-s.day_of_week+7)%7)*86400; // Sa 00:00 Server
      MqlRates r[]; if(CopyRates(sym,PERIOD_H1,sat-1,1,r)!=1) continue;
      if(CSessionClock::MinOfDay(clk.ServerToNy(r[0].time))!=16*60) bad++; }   // Feiertage = Ausreißer
   return bad;  // Mehrheitsentscheid; viele Abweichungen => falsches Modell, Trading sperren
}
```

Fertige Alternativen:

- Carl Schreiber „DealingWithTime“ (Code Base 45287). v2 war nötig, weil MetaQuotes das Verhalten von `CopyTime` geändert hat.
- amralis „TimeGMT library for the strategy tester“ (48291). Sie leitet den Offset aus der ersten Wochenbar von XAUUSD gegen Sonntag 18:00 NY ab. Hinweis des Autors: im Tester liegen die DST-Wechsel dadurch eine Stunde später.

**Quellen 3:** https://www.mql5.com/en/docs/dateandtime/timegmt · https://www.mql5.com/en/docs/dateandtime/timetradeserver · https://www.mql5.com/en/docs/dateandtime/timecurrent · https://www.mql5.com/en/articles/9929 · https://www.mql5.com/en/code/45287 · https://www.mql5.com/en/code/48291

## 4. Positionsgröße (Risiko-% → Lots)

### 4.1 Grundsätze

- **Primärmethode `OrderCalcProfit(type,sym,vol,entry,sl,pl)`:**
  - Berücksichtigt `SYMBOL_TRADE_CALC_MODE`, die Kontraktgröße (XAUUSD je nach Broker 1, 10 oder 100 oz) und die Umrechnung in die Kontowährung.
  - Nur in EAs und Scripts verfügbar, nicht in Indikatoren.
  - Das Ergebnis ist auf die Nachkommastellen der Kontowährung gerundet. Deshalb ein großes Referenzvolumen verwenden; Carreiro nimmt `SYMBOL_VOLUME_MAX`.
- **Tick-Value-Methode als Gegenprobe:** `SYMBOL_TRADE_TICK_VALUE` ist identisch mit `..._PROFIT`. Für Risiko `SYMBOL_TRADE_TICK_VALUE_LOSS × Distanz / SYMBOL_TRADE_TICK_SIZE` rechnen. Bekannte Fehlerbilder:
  - Broker melden XAUUSD in USD statt in der Kontowährung.
  - Bei CFDs ist der Wert teils um Faktor 10 falsch.
  - Beim ersten Aufruf kommt 0.
  - Im Tester liefern JPY-Crosses 100.0. Auf MetaQuotes-Demo waren die Werte korrekt, das Problem ist also brokerabhängig.
- **Kleine Abweichungen sind normal:** `OrderCalcProfit` wählt den Tick-Value nach Ordertyp, nicht nach Ergebnis (Forum 439319). Abweichungen über 5 % deuten auf ein Datenproblem hin.
- **Keine Pip- oder Point-Annahmen:** `TICK_SIZE` kann von `POINT` abweichen. Ein „Pip“ ist pro Symbol explizit zu definieren, bei XAUUSD in Preiseinheiten.
- **Umrechnungspaare:** Alle Quote-Währungen der Liste (USD, JPY, CAD, CHF, AUD, NZD) lassen sich für USD-, EUR- und GBP-Konten über Paare aus der Liste umrechnen; damit ist eine manuelle Gegenrechnung möglich. Diese Paare müssen selektiert und synchron sein.

### 4.2 Codeskizze

```mql5
int VolDigits(double step){ return (int)MathMax(0,MathCeil(-MathLog10(step)-1e-9)); }

bool LotsForRisk(const string sym,const bool buy,const double entry,const double sl,
                 const double riskMoney,const double commPerLotRT,double &lots,string &why)
{
   lots=0;
   const double vMin=SymbolInfoDouble(sym,SYMBOL_VOLUME_MIN), vMax=SymbolInfoDouble(sym,SYMBOL_VOLUME_MAX),
                vStp=SymbolInfoDouble(sym,SYMBOL_VOLUME_STEP);
   if(vMin<=0||vMax<=0||vStp<=0||entry<=0||sl<=0||(buy? sl>=entry : sl<=entry)){ why="Daten/SL ungültig"; return false; }

   double pl=0, ref=vMax, lossLot=0;                                   // 1) OrderCalcProfit
   if(OrderCalcProfit(buy?ORDER_TYPE_BUY:ORDER_TYPE_SELL,sym,ref,entry,sl,pl) && pl<0) lossLot=-pl/ref;

   const double tv=SymbolInfoDouble(sym,SYMBOL_TRADE_TICK_VALUE_LOSS),   // 2) Gegenprobe
                ts=SymbolInfoDouble(sym,SYMBOL_TRADE_TICK_SIZE);
   const double lossTV=(tv>0&&ts>0)? MathAbs(entry-sl)/ts*tv : 0;
   if(lossLot<=0) lossLot=lossTV;
   else if(lossTV>0 && MathAbs(lossTV/lossLot-1.0)>0.05)
      PrintFormat("WARN %s Verlust/Lot: OCP=%.4f TV=%.4f",sym,lossLot,lossTV);
   if(lossLot<=0){ why="Verlust/Lot unbestimmt (nicht synchron?)"; return false; }

   const double raw=riskMoney/(lossLot+commPerLotRT);
   double v=MathFloor(raw/vStp+1e-9)*vStp;                            // ABrunden
   if(v<vMin){ why=StringFormat("%.3f Lot < VOLUME_MIN -> auslassen",raw); return false; }
   v=MathMin(v,vMax);
   const double vLim=SymbolInfoDouble(sym,SYMBOL_VOLUME_LIMIT);        // 0 = kein Limit
   if(vLim>0) v=MathMin(v,vLim-OwnVolumeSameDirection(sym,buy));       // inkl. Pending-Orders
   lots=NormalizeDouble(v,VolDigits(vStp));
   if(lots<vMin){ why="VOLUME_LIMIT"; return false; }

   MqlTick t; double margin=0;                                         // 3) Margin
   if(!SymbolInfoTick(sym,t) ||
      !OrderCalcMargin(buy?ORDER_TYPE_BUY:ORDER_TYPE_SELL,sym,lots,buy?t.ask:t.bid,margin) ||
      margin>0.5*AccountInfoDouble(ACCOUNT_MARGIN_FREE)){ why="Margin-Puffer"; return false; }
   return true;
}
```

Ergänzende Regeln:

- **Nicht auf `VOLUME_MIN` aufrunden.** Bei kleinen Konten, XAUUSD oder 0,25 % Risiko würde das Risiko sonst überschritten.
- **Margin:** `OrderCalcMargin` ignoriert offene Positionen und Orders. Zusätzlich `OrderCheck()` aufrufen; `MqlTradeCheckResult.margin_free` und `margin_level` berücksichtigen den Kontostand.
- **Kommission:**
  - Neu ist `SymbolInfoCommissions(sym, MqlCommission &arr[])` (Build 6060, 23.07.2026).
  - Die Regeln kommen mit `tiers`, Modi in Geld, Pips oder Prozent, Bemessung nach Volumen oder Turnover und `SYMBOL_COMMISSION_ENTRY_IN/OUT/INOUT`.
  - Daraus Geld pro Lot Round-Turn berechnen.
  - Rückgabe 0 bedeutet, dass keine Regeln hinterlegt sind. Dann einen Input oder historische Werte nutzen (`DEAL_COMMISSION` geteilt durch `DEAL_VOLUME`).
  - Im Tester die Kommission in den Advanced Settings setzen.
- **Nach dem Fill:** mit `ResultPrice()` das tatsächliche Risiko neu berechnen und bei Überschreitung teilweise schließen. Wochenend- und News-Gaps (SL-Slippage) deckt keine Lot-Formel ab.

**Quellen 4:** https://www.mql5.com/en/docs/trading/ordercalcprofit · https://www.mql5.com/en/book/automation/experts/experts_ordercalcprofit · https://www.mql5.com/en/docs/trading/ordercalcmargin · https://www.mql5.com/en/book/automation/experts/experts_ordercalcmargin · https://www.mql5.com/en/docs/constants/environment_state/marketinfoconstants · https://www.mql5.com/en/forum/430265/page2 · https://www.mql5.com/en/forum/444637 · https://www.mql5.com/en/forum/453450 · https://www.mql5.com/en/forum/439319 · https://www.mql5.com/en/forum/468983 · https://www.mql5.com/en/docs/marketinformation/symbolinfocommissions · https://www.metatrader5.com/en/releasenotes/terminal · https://www.mql5.com/en/articles/22

## 5. Order-Ausführung

### 5.1 Filling Modes

| Execution (`SYMBOL_TRADE_EXEMODE`) | FOK | IOC | RETURN |
|---|---|---|---|
| Instant/Request | immer | immer | immer |
| **Market** | laut Symbol-Flags | laut Symbol-Flags | **nicht erlaubt** |
| Exchange | laut Symbol-Flags | laut Symbol-Flags | immer |

- **Unterschiedliche Konstanten:** `SYMBOL_FILLING_MODE` ist eine Bitmaske mit `SYMBOL_FILLING_FOK=1`, `IOC=2`, `BOC=4`. `ORDER_FILLING_*` hat **andere Werte**: FOK=0, IOC=1, RETURN=2, BOC=3. Die Maske direkt einzusetzen ist der häufigste Grund für 10030 `TRADE_RETCODE_INVALID_FILL`.
- **Pending-Orders:** laut Doku `ORDER_FILLING_RETURN`, unabhängig vom Execution-Modus.
- **`CTrade::SetTypeFillingBySymbol()`:** wählt FOK, wenn FOK und IOC beide erlaubt sind. Nach im Forum gepostetem Quelltext setzt die Methode nur FOK oder IOC und liefert false, wenn keines der beiden Flags gesetzt ist. Dann RETURN explizit setzen; lokal in `MQL5\Include\Trade\Trade.mqh` prüfen.

```mql5
ENUM_ORDER_TYPE_FILLING FillingFor(const string sym,const ENUM_ORDER_TYPE type)
{
   if(type!=ORDER_TYPE_BUY && type!=ORDER_TYPE_SELL) return ORDER_FILLING_RETURN;
   const long m=SymbolInfoInteger(sym,SYMBOL_FILLING_MODE);
   if((m&SYMBOL_FILLING_FOK)==SYMBOL_FILLING_FOK) return ORDER_FILLING_FOK;  // kein Teil-Fill
   if((m&SYMBOL_FILLING_IOC)==SYMBOL_FILLING_IOC) return ORDER_FILLING_IOC;  // DONE_PARTIAL möglich
   return ORDER_FILLING_RETURN;   // bei SYMBOL_TRADE_EXECUTION_MARKET unzulässig -> 10030-Fallback
}

enum ESend { S_OK, S_RETRY, S_RECONCILE, S_FATAL };
ESend Classify(uint rc)
{  switch(rc){
   case TRADE_RETCODE_DONE: case TRADE_RETCODE_PLACED: case TRADE_RETCODE_DONE_PARTIAL: return S_OK;
   case TRADE_RETCODE_REQUOTE: case TRADE_RETCODE_PRICE_CHANGED: case TRADE_RETCODE_PRICE_OFF:
   case TRADE_RETCODE_TOO_MANY_REQUESTS: case TRADE_RETCODE_LOCKED: return S_RETRY;
   case TRADE_RETCODE_TIMEOUT: case TRADE_RETCODE_CONNECTION: case TRADE_RETCODE_ERROR: return S_RECONCILE;
   default: return S_FATAL; } } // INVALID_*, NO_MONEY, MARKET_CLOSED, *_DISABLES_AT, LIMIT_*, FROZEN ...

bool SendMarket(CTrade &tr,const string sym,const bool buy,const double lots,
                const double sl,const double tp,const string tag,const ulong magic)
{
   tr.SetExpertMagicNumber(magic);
   tr.SetDeviationInPoints(10);                    // wirkt nur bei Instant/Request Execution
   tr.SetTypeFilling(FillingFor(sym,buy?ORDER_TYPE_BUY:ORDER_TYPE_SELL));
   for(int a=0;a<3;a++)
   {
      MqlTick t; if(!SymbolInfoTick(sym,t)) return false;
      const double px=buy?t.ask:t.bid;
      if(!StopsOk(sym,buy,px,sl,tp)) return false;  // STOPS_LEVEL ab Bid(Buy)/Ask(Sell) + Puffer
      bool sent=buy? tr.Buy(lots,sym,px,sl,tp,tag) : tr.Sell(lots,sym,px,sl,tp,tag);
      const uint rc=tr.ResultRetcode();
      if(sent && Classify(rc)==S_OK) return true;
      if(rc==TRADE_RETCODE_INVALID_FILL){ tr.SetTypeFilling(NextAllowedFilling(sym)); continue; }
      if(Classify(rc)==S_RETRY){ Sleep(300*(a+1)); continue; }       // Tester: Sleep = Simulationszeit
      if(Classify(rc)==S_RECONCILE) return ReconcileByTag(sym,magic,tag); // erst prüfen, ob ausgeführt!
      PrintFormat("%s fatal %u %s",sym,rc,tr.ResultRetcodeDescription()); return false;
   }
   return false;
}
```

- **Rückgabewert von OrderSend:** `true` heißt nur, dass die Grundprüfung bestanden ist. Immer `retcode` auswerten und vorher `OrderCheck()` aufrufen.
- **Timeout und Verbindungsabbruch:** Bei Timeout oder Connection niemals blind erneut senden. Erst Positionen, Orders und die History der letzten Minuten auf Magic plus Tag prüfen; sonst entstehen doppelte Positionen.
- **Kommentar-Tag:** kurz halten (≤ 25 Zeichen, das Limit liegt bei 31). Der Broker kann Kommentare ändern, sie taugen also nur für den Abgleich direkt nach dem Senden.

### 5.2 Stops-Level, Freeze-Level und Preise

- **Preise normalisieren:** `MathRound(p/tickSize)*tickSize`, danach `NormalizeDouble(…, SYMBOL_DIGITS)`.
- **`SYMBOL_TRADE_STOPS_LEVEL`:** Mindestabstand in Points für SL, TP und Pending-Orders. Bei Positionen wird er vom Schließpreis aus gemessen (Buy: Bid, Sell: Ask), bei Pending-Orders vom Eröffnungspreis. Der Wert 0 heißt nur „kein Mindestabstand gesetzt“, deshalb immer einen Puffer von etwa max(Stops, Spread) einplanen.
- **`SYMBOL_TRADE_FREEZE_LEVEL`:** Innerhalb dieser Distanz sind Änderungen und Löschungen gesperrt, Retcode 10029 `FROZEN`. Distanzen:
  - Buy Limit: Ask − Open
  - Sell Stop: Bid − Open
  - Buy-Position: TP − Bid bzw. Bid − SL
  - analog für die übrigen Fälle
- **Unveränderte Modifikationen nicht senden** (10025 `NO_CHANGES`). Modifikationen drosseln (10024 `TOO_MANY_REQUESTS`).
- **SL/TP bei Market Execution:** Sie gehören laut Doku nicht zu den Pflichtfeldern. Lehnt ein Broker sie ab (`INVALID_STOPS`), ohne SL/TP öffnen und sofort `TRADE_ACTION_SLTP` senden; schlägt das fehl, Position notfalls schließen.

### 5.3 Limit-Orders an Zonen, Market-Orders, Expiration

- **Limit-Orders an POIs:** präzise, ohne Slippage, mit RETURN. Risiko: Fills bei Spread-Spitzen, denn Buy-Limits triggern auf Ask, der SL auf Bid.
- **Market-Order nach LTF-Bestätigung:** Slippage, dafür eine bestätigte Entry-Logik.
- **Expiration:**
  - Nur wenn `SYMBOL_EXPIRATION_MODE & SYMBOL_EXPIRATION_SPECIFIED` gesetzt ist, `ORDER_TIME_SPECIFIED` mit Serverzeit verwenden, z. B. `clk.NyToServer(11:00 NY)`.
  - Sonst GTC und das Löschen per EA.
  - `SPECIFIED_DAY` gilt bis 23:59:59.
  - Bei `INVALID_EXPIRATION` auf GTC plus EA-Verwaltung zurückfallen.
- **`SYMBOL_ORDER_GTC_MODE`:** Bei `SYMBOL_ORDERS_DAILY` löscht der Broker zum Tagesende Pending-Orders **und SL/TP**. Nach dem Rollover SL/TP prüfen und neu setzen.

### 5.4 Netting/Hedging, Magic, Partial Close, Breakeven, Trailing

- **Kontomodus:**
  - `ACCOUNT_MARGIN_MODE` beim Start prüfen. Hedging ist für mehrere Setups pro Symbol vorzuziehen; Positionen dann immer per Ticket adressieren (`MqlTradeRequest.position`).
  - Im Netting-Modus gibt es nur eine Position pro Symbol. Neue Entries addieren sich, Gegensignale reduzieren oder drehen die Position.
  - `ACCOUNT_FIFO_CLOSE` und `HEDGE_PROHIBITED` (10046) beachten.
- **Magic:** Basis plus Setup-Code kodieren und nur eigene Magic-Bereiche anfassen.
- **Partial Close:** `PositionClosePartial(ticket, vol)`. In der Symbol-Variante wird die „first detected position“ mit passender Magic geschlossen, deshalb immer per Ticket. Das Restvolumen muss ≥ `VOLUME_MIN` und ein Vielfaches des Steps sein.
- **Status aus der History ableiten:** „TP1 erledigt“ ergibt sich aus Startvolumen (`DEAL_ENTRY_IN`-Deals der `POSITION_IDENTIFIER`) gegen aktuelles Volumen. „BE erledigt“ ergibt sich aus SL ≥ Entry ± Kostenpuffer.
- **Trailing:** strukturbasiert und nur bei Bar-Close, nicht pro Tick.

### 5.5 OnTradeTransaction

- Die Reihenfolge der Transaktionen ist nicht garantiert. Die Queue fasst 1024 Elemente, ältere können verdrängt werden.
- Ein Request erzeugt eine ganze Kette von Events, ein `OnTrade` entspricht einem oder mehreren `OnTradeTransaction`.
- Nutzung: schnell auf Fills, SL/TP-Treffer und Order-Löschungen reagieren und R-Statistik führen.
- Wahrheit bleibt der periodische Abgleich im Timer über `PositionsTotal`, `OrdersTotal` und `HistorySelect`.

**Quellen 5:** https://www.mql5.com/en/docs/constants/tradingconstants/orderproperties · https://www.mql5.com/en/docs/constants/environment_state/marketinfoconstants · https://www.mql5.com/en/forum/508038 · https://www.mql5.com/en/forum/222725 · https://www.mql5.com/en/docs/standardlibrary/tradeclasses/ctrade · https://www.mql5.com/en/docs/standardlibrary/tradeclasses/ctrade/ctradesettypefillingbysymbol · https://www.mql5.com/en/docs/standardlibrary/tradeclasses/ctrade/ctradepositionclosepartial · https://www.mql5.com/en/docs/constants/structures/mqltraderequest · https://www.mql5.com/en/docs/trading/ordersend · https://www.mql5.com/en/docs/constants/errorswarnings/enum_trade_return_codes · https://www.mql5.com/en/articles/2555 · https://www.mql5.com/en/book/automation/symbols/symbols_spreads_levels · https://www.mql5.com/en/book/automation/symbols/symbols_expiration · https://www.mql5.com/en/docs/event_handlers/ontradetransaction · https://www.mql5.com/en/docs/constants/environment_state/accountinformation · https://www.metatrader5.com/en/terminal/help/trading/performing_deals

## 6. Filter

- **Spread:**
  - Live aus `SymbolInfoTick` berechnen: `(ask-bid)/point` mit `MathRound`.
  - `SYMBOL_SPREAD` (int) enthält bei floatendem Spread zwar den aktuellen Wert, ist aber gerundet. Bar-Spreads (`CopySpread`, Data Window) sind Minimalwerte.
  - Schwellen pro Symbol relativ setzen, z. B. Spread/ATR(M15) ≤ x % oder ≤ k × Median des Stunden-Spreadprofils. EURUSD und GBPNZD sind nicht vergleichbar.
  - Tick-Frische prüfen: `tick.time` gegen `TimeTradeServer()`.
- **Rollover (17:00 NY, bei NY-Close-Servern 00:00 Server):**
  - Etwa 16:45–17:30 NY keine Entries und keine SL-Modifikationen.
  - Bei XAUUSD bis zur Wiedereröffnung.
  - Shorts mit engem SL werden durch Spread-Spitzen ausgestoppt, weil der SL auf Ask triggert. Solche Shorts nicht über den Rollover halten oder den SL um den erwarteten Rollover-Spread vergrößern.
- **XAUUSD:**
  - Tägliche Pause 17:00–18:00 NY (bei NY-Close-Servern 00:00–01:00 Server), Wochenstart Sonntag 18:00 NY, also eine Stunde nach FX.
  - Die tatsächlichen Sessions per `SymbolInfoSessionTrade(sym, day, idx, from, to)` lesen: Sekunden ab 00:00 Serverzeit, Index iterieren bis false.
  - Feiertage stehen nicht in der Wochenvorlage. `TRADE_RETCODE_MARKET_CLOSED` sauber behandeln.
- **Wochenende:**
  - Freitags ab etwa 12–14 Uhr NY keine neuen Entries.
  - Pending-Orders vor Handelsschluss löschen.
  - Optional bis 16:00 NY flat gehen, wegen Gap-Risiko über den SL hinaus.
  - Dreifach-Swap laut `SYMBOL_SWAP_ROLLOVER3DAYS`.
- **News live:**
  - `CalendarValueHistory(values, from, to, NULL, "USD")` je Währung, Bedeutung über `CalendarEventById(...).importance == CALENDAR_IMPORTANCE_HIGH`.
  - Inkrementell mit `CalendarValueLast(change_id, values)`: Der erste Aufruf mit `change_id = 0` initialisiert nur. Abfragen etwa einmal pro Minute.
  - Werte sind ×10^6 skaliert, LONG_MIN bedeutet „kein Wert“.
  - Zeiten sind Serverzeit.
  - Voraussetzung ist der Kalender-Schalter im Community-Tab.
  - Gesperrt werden die Währungen des Symbols über `SYMBOL_CURRENCY_BASE/PROFIT`, bei XAUUSD USD.
- **News im Tester (4014):**
  - Live per Script als CSV oder Binärdatei exportieren.
  - Lokale Agents: `FILE_COMMON`. Remote/Cloud: `#property tester_file` oder `#resource`.
  - **DST-Falle:** Das Terminal rechnet historische Kalenderzeiten mit dem **aktuellen** Server-Offset um. Beim Export daher korrigieren: `utc = ev.time - offsetJetzt; srv = clk.UtcToServer(utc)`. Code Base 77617 und das MQL5-Book (CalendarCache) beschreiben genau das.
  - Die Kalender-History reicht laut Code Base 77617 nur bis etwa 2020 zurück.

**Quellen 6:** https://www.mql5.com/en/book/automation/symbols/symbols_spreads_levels · https://www.mql5.com/en/forum/362960 · https://www.mql5.com/en/forum/466104 · https://www.mql5.com/en/docs/marketinformation/symbolinfosessiontrade · https://www.tmgm.com/en/academy/trading-academy/gold-trading-hours · https://afterprime.com/trading-hours/xauusd · https://www.mql5.com/en/docs/calendar · https://www.mql5.com/en/docs/calendar/calendarvaluehistory · https://www.mql5.com/en/docs/calendar/calendarvaluelast · https://www.mql5.com/en/docs/constants/structures/mqlcalendar · https://www.mql5.com/en/book/advanced/calendar · https://www.mql5.com/en/book/advanced/calendar/calendar_cache_tester · https://www.mql5.com/en/code/53393 · https://www.mql5.com/en/code/77617 · https://www.mql5.com/en/articles/22231 · https://www.mql5.com/en/forum/485295

## 7. Robustheit

- **Quelle der Wahrheit ist der Server.**
  - Bei `OnInit` und periodisch Positionen und Orders mit eigener Magic einlesen.
  - Tagesergebnis per `HistorySelect` ab Beginn des NY-Tages über `DEAL_MAGIC`, `DEAL_ENTRY` und `DEAL_PROFIT+COMMISSION+SWAP+FEE` bestimmen.
  - Teilschließungen über `DEAL_POSITION_ID` zuordnen.
  - Zonen und Struktur deterministisch aus der History neu berechnen, statt sie zu persistieren.
- **Persistieren nur, was sich nicht ableiten lässt:**
  - Beispiele: Zone verbraucht, Setup-ID, geplanter TP-Plan.
  - Schlüssel ist `POSITION_IDENTIFIER`, nicht der Kommentar.
  - Atomar schreiben: in eine `.tmp`-Datei schreiben, dann `FileMove(tmp, FILE_COMMON, name, FILE_REWRITE|FILE_COMMON)`.
  - Dateiname mit Login und Magic, maximal 64 offene Dateien.
  - Kontinuierlich speichern: `OnDeinit` wird nach 2,5 s zwangsbeendet.
- **GlobalVariables:** nur `double`, Name ≤ 63 Zeichen, Lebensdauer 4 Wochen seit letztem Zugriff, `GlobalVariablesFlush()`. Eignen sich für Flags wie Tageslimit-Sperre oder als Mutex per `GlobalVariableSetOnCondition`.
- **Berechtigungen:** `TERMINAL_TRADE_ALLOWED`, `MQL_TRADE_ALLOWED`, `ACCOUNT_TRADE_EXPERT`, `ACCOUNT_TRADE_ALLOWED` (false z. B. bei Investor-Passwort) und `SYMBOL_TRADE_MODE` (CLOSEONLY usw.). Bei 10027 bzw. 10026 einmal alarmieren, nicht in Schleife senden, und Struktur weiterrechnen.
- **Verbindung:** Ohne `TERMINAL_CONNECTED` nicht handeln. Nach Reconnect neu abgleichen; `REASON_ACCOUNT` löst eine Reinitialisierung aus.
- **Logging:** Journal mit Rate-Limit plus eigenes CSV-Tradejournal mit Server- und NY-Zeit, Setup, Spread, Risiko und Retcode. In der Optimierung per Makro aus.
- **VPS:**
  - MQL5-VPS: DLLs verboten, Auto-Trading immer an, Migration nur von lokal zum VPS, nur Charts mit EAs werden übertragen. Dateien und GVs werden nicht erwähnt, der State muss also vom Server rekonstruierbar sein.
  - `TERMINAL_VPS` abfragen.
  - Eigener VPS: NTP-Zeitsync, weil `TimeGMT` und `TimeTradeServer` von der PC-Uhr abhängen.

**Quellen 7:** https://www.mql5.com/en/docs/runtime/tradepermission · https://www.mql5.com/en/docs/globals · https://www.mql5.com/en/docs/globals/globalvariableset · https://www.mql5.com/en/docs/constants/namedconstants/uninit · https://www.mql5.com/en/docs/constants/tradingconstants/dealproperties · https://www.mql5.com/en/docs/constants/environment_state/terminalstatus · https://www.mql5.com/en/docs/constants/environment_state/mql5_programm_info · https://www.metatrader5.com/en/terminal/help/virtual_hosting/virtual_hosting_migration · https://www.mql5.com/en/forum/218184

## 8. Performance

- **Daten pro Symbol und TF:**
  - Ringpuffer aus `MqlRates`, einmal per `ArrayResize` vorab allokiert, Zugriff über `At(shift)`.
  - Inkrementell nur neu geschlossene Bars nachladen; bei Inkonsistenz voll neu laden.
  - Kein `CopyRates` pro Tick über 25 Symbole × 6 TFs.
- **ATR:**
  - Selbst rechnen (Wilder-RMA über den Ringpuffer): deterministisch, ohne Warm-up-Probleme, identisch zur Python-Referenz.
  - Bei Handles (`iATR`) einmal in `OnInit` erzeugen. Vor `CopyBuffer` `BarsCalculated(h)` prüfen; `CopyBuffer` liefert anfangs -1 bzw. 4806.
  - Indikatoren eines Symbols teilen sich einen Thread.
- **Zonen (OB/FVG/Breaker):**
  - Struct-Arrays mit fester Obergrenze pro Symbol und TF, Lebenszyklus ACTIVE → MITIGATED → INVALID → recycelt.
  - Kein `new` pro Zone; wo Objekte nötig sind, einen Pool plus `CheckPointer`. Auf „leaked memory“-Meldungen achten.
- **Chart-Objekte:** nur, wenn `!MQLInfoInteger(MQL_TESTER) || MQLInfoInteger(MQL_VISUAL_MODE)`, nur für das Chart-Symbol, mit Präfix, `ChartRedraw` einmal pro Zyklus.
- **Laufzeit messen:** Zyklusdauer mit `GetMicrosecondCount()` erfassen (Budget z. B. < 50 ms). Profiler auf History-Daten nutzen.

**Quellen 8:** https://www.mql5.com/en/articles/14574 · https://www.mql5.com/en/docs/series/copybuffer · https://www.mql5.com/en/docs/series/indicatorrelease · https://www.mql5.com/en/docs/runtime/running

## 9. Code-Organisation und Tests

```
Include/SMC/
  Core/      SymbolContext.mqh (Props-Cache, Ringpuffer, BarClock, Warm-up)
             SessionClock.mqh, Logger.mqh, StateStore.mqh
  Engines/   StructureEngine.mqh (Swings, BOS/CHoCH je TF)
             LiquidityEngine.mqh (EQH/EQL, PDH/PDL, Session-H/L, Sweeps)
             POIEngine.mqh (OB, FVG, Breaker, Mitigation)
             SignalEngine.mqh (MTF-Regeln + Killzone-Gating)
  Risk/      RiskManager.mqh, ExposureManager.mqh
  Exec/      TradeExecutor.mqh (Filling, Stops/Freeze, Retry, Reconcile), PositionManager.mqh (BE/Partial/Trail)
  Filters/   SpreadFilter.mqh, NewsFilter.mqh (live Calendar | Tester-CSV)
Experts/SMC_Portfolio.mq5  (OnInit/OnTimer/OnTick/OnTradeTransaction -> Dispatcher)
```

- **Engines ohne Terminal-Aufrufe:** Die Engines arbeiten nur auf `MqlRates`-Arrays. Datenzugriff läuft über `interface IMarketData`, damit Tests Fixtures einspeisen können.
- **Unit-Tests:** Scripts (`OnStart`) mit CSV-Fixtures aus `MQL5/Files`. Frameworks: MQLUnit (Code Base 33089), der Compile-Time-Ansatz aus Artikel 22967, `CTestLite` (Artikel 19154), MTUnit auf GitHub.
- **Golden-Master gegen Python:**
  - Bars per Script als CSV exportieren, damit beide Seiten dieselben Daten haben, oder per MetaTrader5-Python-Paket (`copy_rates_range`).
  - Python-Referenz und MQL5-Engine schreiben ihre Ereignisse (Zeit, Typ, Preis) als CSV; beide werden gedifft.
  - Achtung: Laut Python-Doku sind die Zeiten „UTC“. Faktisch sind es Server-Zeitstempel ohne Zone. Mit der MQL5-Ausgabe abgleichen und dieselbe SessionClock-Logik verwenden.

**Quellen 9:** https://www.mql5.com/en/code/33089 · https://www.mql5.com/en/articles/22967 · https://www.mql5.com/en/articles/19154 · https://github.com/rodrigoshaller/MTUnit · https://www.mql5.com/en/docs/python_metatrader5 · https://www.mql5.com/en/docs/python_metatrader5/mt5copyratesfrom_py · https://www.mql5.com/en/articles/14026

## 10. Exposure-Management über 25 korrelierte Instrumente

- **Exposure-Vektor:** Jede Position und jede **Pending-Order** (behandelt, als wäre sie gefüllt) erzeugt einen Vektor über USD, EUR, GBP, JPY, AUD, NZD, CAD, CHF und XAU. Ein Long auf Base/Quote mit Risiko r ergibt +r auf Base und −r auf Quote.
- **Risikomaß:** das aktuelle Risiko bis zum SL in Kontowährung. Liegt der SL hinter Breakeven, ist das Risiko 0, die Position zählt aber weiter zur Trade-Anzahl (Gap-Risiko).
- **Limits:**
  - |Netto-Risiko je Währung| ≤ z. B. 1,5 %
  - offene Trades je Währung ≤ 2
  - Gesamt-Risiko ≤ 4 %, maximal 6 Trades
  - keine Gegenpositionen auf demselben Symbol
  - Cluster-Regel für die JPY-Crosses (EUR-, GBP-, AUD-, NZD-, CAD- und CHFJPY); optional eine rollierende D1-Korrelationsmatrix
  - während News die betroffene Währung komplett sperren
- **XAU-Zuordnung:** Bei CFD-Gold ist `SYMBOL_CURRENCY_BASE` mitunter USD. XAU daher explizit mappen.

```mql5
string CCY[]={"USD","EUR","GBP","JPY","AUD","NZD","CAD","CHF","XAU"};
struct SExp { double risk[9]; int cnt[9]; double total; int trades; };
int Idx(const string c){ for(int i=0;i<9;i++) if(CCY[i]==c) return i; return -1; }
void AddLeg(SExp &e,const string sym,const int dir,const double r)
{  string b=SymbolInfoString(sym,SYMBOL_CURRENCY_BASE), q=SymbolInfoString(sym,SYMBOL_CURRENCY_PROFIT);
   if(StringFind(sym,"XAU")==0 || StringFind(sym,"GOLD")==0) b="XAU";
   int ib=Idx(b), iq=Idx(q);
   if(ib>=0){ e.risk[ib]+=dir*r; e.cnt[ib]++; }
   if(iq>=0){ e.risk[iq]-=dir*r; e.cnt[iq]++; }
   e.total+=r; e.trades++; }
bool Allows(const SExp &cur,const string sym,const int dir,const double r,
            double maxCcy,int maxCnt,double maxTot,int maxTrades)
{  SExp e=cur; AddLeg(e,sym,dir,r);
   if(e.total>maxTot || e.trades>maxTrades) return false;
   for(int i=0;i<9;i++) if(MathAbs(e.risk[i])>maxCcy || e.cnt[i]>maxCnt) return false;
   return true; }
```

**Quellen 10:** https://www.mql5.com/en/docs/constants/environment_state/marketinfoconstants · https://dev.to/omaisali/why-your-multi-symbol-mql5-ea-misses-trades-on-every-symbol-except-the-chart-one-1nh9 · https://www.mql5.com/en/articles/15085

## Plattform-Fallstricke, die der EA abfangen muss

1. `OnTick` feuert nur für das Chart- bzw. Tester-Symbol, und Ticks werden verworfen, solange ein NewTick ansteht oder läuft. Ohne Timer-Polling verpasst der EA Signale auf 24 Symbolen.
2. Spy-Indikator, `OnChartEvent` und `OnBookEvent` sind im Tester unzuverlässig oder undokumentiert.
3. Im Tester sind die Bars verschiedener Symbole nicht synchron. Eine neue Bar existiert erst ab dem ersten Tick, und Bars ohne Ticks fehlen.
4. Daten sind anfangs nicht synchron: `CopyRates` liefert -1 oder zu wenige Bars, `TICK_VALUE` und `OrderCalcProfit` liefern beim ersten Aufruf 0. Warm-up-Gating ist Pflicht, `TERMINAL_MAXBARS` muss reichen.
5. Im Tester gilt `TimeGMT()` = `TimeLocal()` = `TimeTradeServer()` = `TimeCurrent()`. Ein Offset über `TimeGMT` ist dort 0; live hängt er von der PC-Uhr ab.
6. Broker-Zeitzonen (NY-Close, EU-DST, GMT+0) und die DST-Abweichungswochen (25.10.–01.11.2026, März 2027) verschieben Killzones und D1-Grenzen. Das Modell muss validiert und NY-Tageskerzen müssen selbst gebaut werden.
7. Im Tester liefern Kalenderfunktionen 4014. Historische Kalenderzeiten sind mit dem aktuellen Offset umgerechnet (DST-Fehler von einer Stunde). `FILE_COMMON` steht auf Remote- und Cloud-Agents nicht zur Verfügung.
8. `SYMBOL_TRADE_TICK_VALUE` kann falsch sein (XAUUSD, CFDs, Tester bei JPY-Crosses). Lots per `OrderCalcProfit` berechnen, mit Plausibilitätsprüfung und Abrundung; unter `VOLUME_MIN` den Trade auslassen.
9. `OrderCalcMargin` ignoriert bestehende Positionen. Kommission muss explizit eingerechnet werden (`SymbolInfoCommissions` erst ab Build 6060).
10. `SYMBOL_FILLING_*` und `ORDER_FILLING_*` haben verschiedene Werte. RETURN ist bei Market Execution verboten, Pending-Orders brauchen RETURN. `SetTypeFillingBySymbol` kann false liefern.
11. `OrderSend` = true bedeutet nicht „ausgeführt“. Bei TIMEOUT oder CONNECTION erst abgleichen, dann neu senden; sonst drohen doppelte Positionen.
12. Stops-Level wird von Bid (Buy) bzw. Ask (Sell) gemessen, Freeze-Level sperrt Modifikationen, 10025 bei unveränderten Werten.
13. `SYMBOL_ORDERS_DAILY` löscht Pending-Orders und SL/TP zum Tagesende. Expiration-Modi pro Symbol prüfen.
14. Kommentare sind auf 31 Zeichen begrenzt und vom Broker änderbar. Positionen über Magic und `POSITION_IDENTIFIER` zuordnen.
15. Bei `OnTradeTransaction` ist die Reihenfolge nicht garantiert und die Queue auf 1024 begrenzt. Periodischer Server-Abgleich ist Pflicht.
16. Im Netting-Modus werden Positionen zusammengeführt, FIFO-Konten und Hedge-Verbote gibt es auch. `ACCOUNT_MARGIN_MODE` beim Start prüfen.
17. Rollover-Spreads und die XAUUSD-Pause lösen Shorts-SL (Trigger auf Ask) und Limit-Fills aus. Wochenend-Gaps überschreiten das geplante Risiko.
18. Tester-Spread bei generierten Ticks ist der M1-Minimal-Spread, Ergebnisse werden zu optimistisch. Final mit Real Ticks plus Delay testen; Real Ticks enthalten generierte Lücken.
19. Ein Critical Runtime Error beendet den Portfolio-EA komplett. `OnDeinit` hat nur 2,5 s. GlobalVariables speichern nur `double`, Namen ≤ 63 Zeichen, 4 Wochen Lebensdauer.
20. Fehlende Berechtigungen (AutoTrading aus, Investor-Modus, `CLOSEONLY`) und Verbindungsverlust nicht mit Request-Schleifen beantworten. Auf dem VPS sind DLLs verboten und lokale State-Dateien nicht garantiert.
21. Symbolnamen mit Suffix oder abweichendem Namen (XAUUSD/GOLD) müssen aufgelöst werden. Umrechnungspaare müssen in der Market Watch stehen und sind im Tester nur mit Forex-Calc-Mode als Cross-Rate nutzbar.

*Hinweis zur Recherche:* Gegen Ende war das sitzungsweite WebSearch-Kontingent aufgebraucht. Drei Punkte sind deshalb schwächer belegt: die Ableitung der Kommission aus der Deal-History, das XAU-Base-Mapping bei CFD-Gold und die Aussage zu Python-Zeitstempeln. Sie stützen sich auf die Dokumentation und auf Praxiswissen und sollten am Zielbroker geprüft werden. Ebenfalls nur aus einem Forum-Quelltext stammt das Verhalten von `CTrade::SetTypeFillingBySymbol` (§5.1); lokal in `Trade.mqh` nachsehen.
