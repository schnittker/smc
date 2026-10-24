<!-- Kapitel 5: Evidenz, Kritik, Robustheit, Risiko | Deep-Research-Rohbericht (Recherche-Agent), Stand 2026-10-24, unverändert übernommen -->

# Teilbericht: Evidenz, Kritik und Robustheit für einen SMC/ICT-EA (MT5, 25 Instrumente)

Stand: 24.10.2026. Wo ich eine Quelle nur über Abstract oder Suchsnippet lesen konnte, steht das dabei. Zahlen ohne Quellenangabe sind meine eigenen Rechnungen und so gekennzeichnet.

## 0. Kernaussagen

1. **Für SMC/ICT als Gesamtsystem gibt es keine peer-reviewte Evidenz.**
   - Die methodisch sauberste öffentliche Prüfung umfasst 648 Backtests auf Tagesdaten von US-Index-ETFs, ohne Kosten. In 31 von 32 Ereignistests fand sie keinen signifikanten Edge.
   - Alle auffindbaren mechanischen Intraday-Tests liegen bei einem Profit Factor (PF) unter 1. Das betrifft Silver Bullet auf NQ/ES, einen ICT-Bot auf EURUSD und den London-Range-Breakout auf EURUSD.
2. **Einzelne Mechanismen sind dagegen gut belegt:**
   - Stop- und Take-Profit-Cluster an runden Zahlen
   - Stop-Kaskaden
   - Support/Resistance fällt mit Orderbuch-Tiefe zusammen
   - starke Intraday-Saisonalität von Volatilität und Volumen
   - Fixing-Effekte

   Diese Befunde erklären, **wo und wann** sich Preise schnell bewegen. Sie stützen **nicht** die SMC-typische Richtungsprognose nach einem Sweep.
3. **Technische Analyse im G10-FX:** Die Profite einfacher Regeln sind seit Anfang der 1990er weitgehend verschwunden. Intraday-Regeln scheitern an realistischen Kosten. Euer Universum (G10-Paare plus Gold) ist das liquideste und effizienteste Segment.
4. **Der Verfall vom Backtest zum Live-Handel ist der Normalfall.** Bei 215 Bank-Strategien fiel die Sharpe Ratio im Median um 73 %. Die Backtest-Sharpe erklärt weniger als 2,5 % der Out-of-Sample-Varianz.
5. **MT5-Fallen:**
   - Die echte Tick-Historie beim Broker reicht teils nur Monate zurück.
   - Die Anzeige „100 % real ticks“ kann falsch sein.
   - Der Tester rechnet Swaps mit den heutigen Sätzen.
   - Kommissionen müssen manuell gepflegt werden.
6. **Korrelation:** Die 25 Instrumente bestehen praktisch aus 8 Währungen plus Gold. USD steckt in 8 Instrumenten, JPY in 7. Die Trades sind daher nicht unabhängig.
7. **Realistisches Ziel nach Kosten:** PF etwa 1,1–1,4 bzw. +0,05 bis +0,2 R pro Trade. Für einen statistisch belastbaren Nachweis braucht es mehrere hundert bis knapp 2.000 Out-of-Sample-Trades (eigene Rechnung, Abschnitt 5.4).

---

## 1. Theoretische und empirische Grundlagen

### 1.1 Order-Clustering und Stop-Kaskaden (der Kern der „Liquidity“-Idee)

- **Osler (2003, Journal of Finance)** wertete erstmals Daten zu rund 9.700 Stop-Loss- und Take-Profit-Orders einer großen FX-Bank aus.
  - Take-Profit-Orders clustern stark auf runden Zahlen (xx00/xx50). Dort drehen Trends häufiger, was den klassischen Support/Resistance-Effekt erklärt.
  - Stop-Orders clustern **knapp jenseits** runder Zahlen. 14,3 % der ausgeführten Stop-Buys lagen bei xx01–10, nur 6,9 % bei xx90–99. Das erklärt Beschleunigung nach einem Durchbruch.
  - Wertgewichtet lagen 9,9 % der Take-Profit-Orders exakt auf xx00, gegenüber 3,8 % der Stops.
- **Osler (2005, JIMF):** Auf Minutendaten für DEM, JPY und GBP gegen USD laufen Trends ungewöhnlich schnell, sobald der Kurs Stop-Cluster erreicht.
  - Der Markt reagiert stärker und länger auf Stops als auf Take-Profits.
  - Signifikant ist das über **Stunden, nicht über Tage**.
  - Der Effekt trägt zu Fat Tails bei.
- **Osler & Savaser (2011):** Laut kalibrierten Simulationen kann preisabhängig ausgelöstes Trading mehr als die Hälfte der Exzess-Kurtosis von FX-Renditen erklären.
- **Savaser (2011):** Solche Orders erhöhen die Erklärungskraft für Renditen nach Nachrichten um die Hälfte, und zwar unabhängig von der Nachrichten-Überraschung.
- **BIS (2017) zum GBP-Flash-Event vom 7.10.2016:** Das Pfund fiel in den frühen asiatischen Handelsstunden um rund 9 %. Als Ursachen nennt der Bericht Tageszeit bzw. dünne Liquidität, Options-Hedging und ausgelöste Stop-Losses. Laut Bank of England fiel GBPUSD um 9,66 % in 40 Sekunden.
- **Kavajecz & Odders-White (2004, RFS):** Support/Resistance-Niveaus fallen mit Tiefenspitzen im Limit-Orderbuch zusammen.
  - Die Autoren definieren S/R als ein Hoch oder Tief, das in der Vorwoche mindestens zweimal erreicht wurde. Das entspricht faktisch den „Equal Highs/Lows“ von SMC.
  - Die Kausalität läuft eher vom Orderbuch zur Technischen Analyse. Techniker finden also vorhandene Tiefe, sie erzeugen sie nicht.
  - Datengrundlage sind NYSE-Aktien.

**Einordnung für SMC:** Die Prämisse „über offensichtlichen Hochs und Tiefs liegt Liquidität“ hat einen empirischen Kern. Drei Einschränkungen sind entscheidend:
- **Fortsetzung statt Umkehr.** Osler belegt nach dem Auslösen von Stops eine Fortsetzung (Kaskade). Das SMC-Narrativ „Sweep, dann Reversal“ ist damit nicht belegt. Eine Umkehr ist nur dort plausibel, wo Take-Profit- oder Limit-Cluster die Bewegung absorbieren.
- **Alte Daten.** Die Belege stammen aus der Interbank-Ära vor 2002 bzw. aus NYSE-Orderbüchern.
- **Fehlende Sicht.** Ein Retail-EA sieht weder Orderbuch noch Order-Flow. Cluster lassen sich nur über Proxies annähern: runde Zahlen, Swing-Extreme, Session-Hochs und -Tiefs.

Quellen:
- [Osler 2003, JF](https://onlinelibrary.wiley.com/doi/abs/10.1111/1540-6261.00588) / [NY Fed SR125](https://www.newyorkfed.org/research/staff_reports/sr125.html)
- [Osler 2005, NY Fed SR150](https://www.newyorkfed.org/research/staff_reports/sr150.html)
- [Osler & Savaser 2011](https://www.brandeis.edu/economics/RePEc/brd/doc/Brandeis_WP04.pdf)
- [Savaser 2011 (SSRN, nur Abstract)](https://www.ssrn.com/abstract=2202942)
- [BIS Markets Committee 2017](https://www.bis.org/publ/mktc09.htm)
- [BoE Staff WP 687](https://www.bankofengland.co.uk/-/media/boe/files/working-paper/2017/the-october-2016-sterling-flash-episode)
- [Kavajecz & Odders-White 2004](https://ideas.repec.org/a/oup/rfinst/v17y2004i4p1043-1071.html)

### 1.2 Support/Resistance und Chartmuster im FX

- **Osler (2000):** Die S/R-Niveaus, die sechs Marktteilnehmer an ihre Kunden ausgaben, sagen intraday Trendunterbrechungen voraus. Die Stärke schwankt deutlich je Währung und Anbieter.
- **Curcio, Goodhart, Guillaume & Payne (1997):** Intraday-Filterregeln von Praktikern bringen in Trendphasen teils Gewinne, im Durchschnitt aber nicht.
- **Chang & Osler (1999):** Head-and-Shoulders ist im Zeitraum 1973–1994 nur bei DEM und JPY signifikant profitabel. Selbst dort schneiden einfache Moving-Average- und Filterregeln besser ab.

S/R enthält also Information über Trendunterbrechungen. Wirtschaftlich nutzbar ist sie nach Kosten nur schwach.

Quellen:
- [Osler 2000](https://www.newyorkfed.org/research/epr/00v06n2/0007osle.html)
- [Curcio et al. 1997](http://technicalanalysis.org.uk/support-and-resistance/Curcio-etal1997.pdf)
- [Chang & Osler 1999](https://onlinelibrary.wiley.com/doi/abs/10.1111/1468-0297.00466)

### 1.3 Order Flow und „Smart Money“

- **Evans & Lyons (2002, JPE):** Der Interdealer-Order-Flow erklärt mehr als 60 % der täglichen Veränderungen von DM/$ (R²). 1 Mrd. $ Netto-Käufe heben den Kurs um etwa 0,5 %.
- **Menkhoff, Sarno, Schmeling & Schrimpf (2016, JF):** Die Kunden-Order-Flows einer großen Dealer-Bank sind hoch informativ für künftige Kurse. Die Kundengruppen unterscheiden sich deutlich in Prognosekraft, Handelsstil und Risiko.

**Einordnung:** „Smart Money“ im Sinne informierter Order-Flows existiert. Im dezentralen Spotmarkt gibt es aber kein konsolidiertes Volumen. Das MT5-„Tick-Volumen“ misst nur die Quote-Aktivität des Brokers. SMC leitet institutionelle Absicht aus OHLC-Formen ab, und dafür fehlt jede Evidenz.

Quellen:
- [Evans & Lyons 2002](https://www.journals.uchicago.edu/doi/10.1086/324391)
- [Menkhoff et al. 2016 (BIS WP 405)](https://www.bis.org/publ/work405.pdf)

### 1.4 Intraday-Saisonalität, Sessions, Fixings

- **Andersen & Bollerslev (1998, JF):** Die Intraday-Volatilität folgt ausgeprägten Mustern. Die Spitzen kommen von US-Makrodaten um 8:30 ET. Für den bedingten Mittelwert von 5-Minuten-Renditen gibt es **kaum Vorhersagbarkeit**: Volatilität ist prognostizierbar, die Richtung nicht.
- **Ito & Hashimoto (2006, EBS-Daten):** Die Handelsaktivität ist U-förmig für Teilnehmer in Tokio und London, nicht aber für New York.
- **BIS-Triennial-Survey:** Das FX-Volumen lag 2022 bei 7,5 Bio. $/Tag und 2025 bei 9,6 Bio. $/Tag. Großbritannien hat einen Anteil von 38 %. Der USD war 2025 an 89 % aller Trades beteiligt.
- **Breedon & Ranaldo (2013, JMCB):** Währungen werten während ihrer lokalen Handelszeiten tendenziell ab, und der Order-Flow zeigt dasselbe Muster. Laut CXO-Zusammenfassung ist das nach Spreads nur bei EURUSD profitabel.
- **Evans (2018, JBF):** Über 21 Währungen und 10 Jahre zeigt sich extreme Volatilität kurz vor dem 16:00-WMR-Fix. Vor und nach dem Fix sind die Kursänderungen negativ autokorreliert, besonders am Monatsende.
- **Krohn, Mueller & Whelan (2024, JF):** Der USD wertet vor dem Tokio-, EZB- und London-Fix auf und danach wieder ab („W-Muster“).
  - Datengrundlage: 21 Jahre, 9 Währungen, hochsignifikant.
  - Die Autoren erklären das mit dem Inventarrisiko der Dealer.
  - Eine Long-USD-vor-Fix-Strategie ist **ohne Kosten** stark positiv.

**Einordnung:**
- Als Volatilitäts- und Liquiditätsfenster sind „Killzones“ gut belegt. Das spricht für Session-**Filter**: Kosten fallen dort relativ zur Bewegung kleiner aus.
- Belegte Richtungsmuster hängen an Fixings und Flows, nicht an „Manipulation“, und sie reagieren empfindlich auf Kosten.
- Die ICT-spezifischen Zeitfenster, etwa Silver Bullet 10–11 NY, sind nirgends untersucht.
- Testbar wäre der Fix-Reversal-Effekt als evidenzbasierte Zeitkomponente.

Quellen:
- [Andersen & Bollerslev 1998](https://public.econ.duke.edu/~boller/Published_Papers/jf_98.pdf)
- [Ito & Hashimoto (NBER)](https://www.nber.org/papers/w12413)
- [BIS 2022](https://www.bis.org/press/p221027.htm) / [BIS 2025](https://www.bis.org/press/p250930.htm)
- [Breedon & Ranaldo (SNB WP)](https://www.snb.ch/en/publications/research/working-papers/2011/working_paper_2011_04) / [CXO-Zusammenfassung](https://www.cxoadvisory.com/currency-trading/daily-currency-exchange-pattern/)
- [Evans 2018](https://mpra.ub.uni-muenchen.de/81583/)
- [Krohn et al. 2024](https://onlinelibrary.wiley.com/doi/10.1111/jofi.13306)

### 1.5 Gaps und „Imbalances“

- **Caporale & Plastun (2017):** Auf Tagesdaten 2000–2015 für Aktien, FX und Rohstoffe verhalten sich Gaps meist so, wie es mit Markteffizienz vereinbar ist. **Ausnahme ist FOREX**: Dort erzielte eine Gap-Strategie abnormale Gewinne. Den Volltext konnte ich nicht lesen. Eine Sekundärquelle nennt über 60 % Trefferquote für Shorts nach Up-Gaps in EURUSD/GBPUSD.
- **MDPI JRFM (2025):** Bei Weekend-Gaps in Aktienindizes entsprechen die Treffer- und Stop-Raten normaler Marktdynamik, nicht einem gezielten „Gap-Filling“.
- **Edgeful-Daten via TradeThatSwing:** EURUSD-Weekend-Gaps wurden von Januar bis Juli 2026 zu 85 % gefüllt. Sie sind aber meist kleiner als 10 Pips und damit selten handelbar.

**Methodische Konsequenz für FVGs:** Hohe Fill-Raten kleiner Lücken treten auch bei einem Random Walk auf. Eine FVG-Statistik ist nur aussagekräftig gegen ein Nullmodell, also gegen gleich große, zufällig gewählte Preisintervalle mit gleicher Volatilität und in der gleichen Session.

Quellen:
- [Caporale & Plastun (SSRN)](https://papers.ssrn.com/abstract=2850057) / [Sekundärquelle](https://stocksoftresearch.com/trading-gaps-in-the-forex/)
- [MDPI 2025](https://www.mdpi.com/1911-8074/18/3/132)
- [TradeThatSwing](https://tradethatswing.com/eurusd-monday-gap-fill-strategy-and-statistics/)

### 1.6 Profitabilität Technischer Analyse im FX

- **Park & Irwin (2007):** Von 95 „modernen“ Studien fallen 56 positiv, 20 negativ und 19 gemischt aus. Die Gewinne reichen etwa bis Anfang der 1990er. Viele Studien leiden unter Data Snooping, nachträglicher Regelwahl und unzureichend berücksichtigten Kosten.
- **Menkhoff & Taylor (2007, JEL):** Technische Analyse ist unter FX-Profis weit verbreitet. Einzelne Regeln erzielten über längere Zeiträume signifikante Überrenditen. Weder Irrationalität noch Zentralbank-Interventionen reichen als Erklärung.
- **Neely, Weller & Ulrich (2009, JFQA):** In echten Out-of-Sample-Tests waren die Gewinne von Filter- und Moving-Average-Regeln bis Anfang der 1990er verschwunden. Weniger untersuchte Regeln haben nachgelassen, aber womöglich nicht vollständig (Adaptive Markets Hypothesis).
- **Neely & Weller (2003, JIMF):** Intraday-Regeln für DEM, JPY, CHF und GBP, gefunden per Genetic Programming und linearen Modellen, bringen **keine Überrenditen** bei realistischen Kosten (2,5 bp) und Handelszeiten. Ohne Kosten waren die Renditen teils hoch.
- **Neely & Weller (2013):** Die Renditen adaptiver Regelportfolios sind zu einem erheblichen Teil zu Schwellenländer-Währungen gewandert.
- **Hsu, Taylor & Wang (2016, JIE):** Auf Basis von 21.000 Regeln, 30 Währungen, 45 Jahren und mit Korrektur für Data Snooping finden sie Vorhersagbarkeit. Sie schwankt aber über die Zeit und zwischen Ländergruppen und wächst mit der Volatilität. Die Studie arbeitet mit Tagesdaten.
- **Aronson (2006):** Keine der 6.402 getesteten Regeln auf den S&P 500 ist nach Korrektur für Data Mining signifikant.
- **Bajgrowicz & Scaillet (2012, Dow Jones):** Schon niedrige Kosten heben die Performance auf, sogar in-sample.
- **Menkhoff et al. (2012, JFE):** Bei Währungsmomentum liegt der Renditeunterschied zwischen Gewinner- und Verliererwährungen bei bis zu 10 % p.a. Er wird teils durch Kosten erklärt, und die Grenzen der Arbitrage sind deutlich.

**Implikation:** Ein Intraday-System auf G10 plus Gold konkurriert im effizientesten Segment. Kosten sind der Hauptgrund, warum es scheitert.

Quellen:
- [Park & Irwin](https://onlinelibrary.wiley.com/doi/10.1111/j.1467-6419.2007.00519.x)
- [Menkhoff & Taylor](https://www.aeaweb.org/articles?id=10.1257%2Fjel.45.4.936)
- [Neely/Weller/Ulrich (WP)](https://files.stlouisfed.org/files/htdocs/wp/2006/2006-046.pdf)
- [Neely & Weller 2003](https://www.sciencedirect.com/science/article/abs/pii/S0261560602001018)
- [Neely & Weller 2013 (WP)](https://s3.amazonaws.com/real.stlouisfed.org/wp/2011/2011-021.pdf)
- [Hsu/Taylor/Wang](https://profiles.wustl.edu/en/publications/technical-trading-is-it-still-beating-the-foreign-exchange-market/)
- [Aronson-Review (CXO)](https://www.cxoadvisory.com/technical-trading/evidence-based-technical-analysis-applying-the-scientific-method-and-statistical-inference-to-trading-signals-chapter-by-chapter-review/)
- [Bajgrowicz & Scaillet](https://ideas.repec.org/a/eee/jfinec/v106y2012i3p473-491.html)
- [Menkhoff et al. 2012](https://ideas.repec.org/a/eee/jfinec/v106y2012i3p660-684.html)

### 1.7 Evidenz-Matrix (SMC-Begriff, nächstliegende Evidenz, Bewertung)

| SMC/ICT-Konzept | Nächstliegende Evidenz | Status |
|---|---|---|
| Liquidity Pools (Equal Highs/Lows, runde Zahlen) | Osler 2003; Kavajecz & Odders-White 2004 | Existenz von Order-Clustern belegt (ältere Daten) |
| Sweep / Stop Hunt mit anschließendem Reversal | Osler 2005 zeigt Kaskade bzw. **Fortsetzung**; Turtle Soup (1995) | Mechanismus belegt, Reversal-Prognose **nicht** belegt |
| Order Block | keine direkte Evidenz; StatOasis: t ≤ 1,22 | unbelegt |
| FVG „wird gefüllt“ | keine peer-reviewte Studie; Fill-Raten ohne Nullmodell | unbelegt |
| Killzones / Sessions | Volatilitäts- und Volumensaisonalität | **als Volatilitätsfilter belegt**, Richtung nicht |
| Judas Swing / Power of 3 | verwandt: Breedon & Ranaldo, Krohn et al. (flow- und fixbedingt) | in ICT-Form unbelegt |
| BOS/CHoCH (Marktstruktur) | entspricht Dow-Theorie bzw. Trendfolge; im G10 seit ca. 1990 weitgehend arbitriert | schwach |
| „Smart Money“-Absicht | informative Flows (Evans & Lyons; Menkhoff 2016), aber aus OHLC nicht beobachtbar | Konzept real, Ableitung unbelegt |
| OTE / Premium-Discount (Fibonacci) | StatOasis: 1 von 8 OTE-Tests mit t > 2 | unbelegt |

---

## 2. Akademische und systematische Untersuchungen speziell zu SMC/ICT

Über Scholar-, SSRN- und arXiv-nahe Websuche habe ich **keine peer-reviewte Publikation** gefunden. Vorhanden sind:

- **Maskey (2021), Bachelorarbeit an der Centria UAS (Finnland):** Strategie aus Online-SMC-Material plus eigener Erfahrung zusammengestellt. Laut Abstract kein systematischer Test. Das PDF war gesperrt (403). [Theseus](https://www.theseus.fi/bitstream/handle/10024/505690/Maskey_Bikesh.pdf)
- **Kondapally (2025), SSRN-Preprint, nicht begutachtet:** Führt einen „Degree of FVG“ ein, gemessen über die Steigung aus Tickdaten. Ausgewertet sind 32.202 FVG-Ereignisse in 4 Asset-Klassen. Flache FVGs zeigen eine 3,2-fach stärkere Preisreaktion (p < 0,001). Netto-Handelsergebnisse sind nicht ersichtlich; ich konnte nur das Snippet lesen. [SSRN](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=6032676)
- **Rehan (2026), SSRN, Protokoll für BTC-Sweeps ohne Ergebnisse:**
  - Es definiert Levels, Sweep, Akzeptanz und Ablehnung ohne Lookahead.
  - Es sieht Placebo-Kontrollen, einen gesperrten Hold-out und Kontrolle für Multiple Testing vor.
  - Die Hypothese lautet: Der Sweep allein trägt wenig Information, erst der Zustand danach (Akzeptanz oder Ablehnung) trägt zusätzliche.
  - Als **Vorlage für das eigene Testdesign** ist das sehr brauchbar. [SSRN](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=7557779)
- **StatOasis (Sept. 2026), unabhängiger Blog, methodisch am saubersten:**
  - Order Blocks, FVG, Sweep und OTE mechanisch kodiert.
  - 648 Backtests auf SPY, QQQ, DIA und IWM, Tagesdaten seit 1993–2000, nur Long, ohne Kosten.
  - Ereignisstudie: 31 von 32 t-Werten liegen unter 2. Bestwert ist Order Block auf SPY mit t = +1,22 (+0,121 % über 5 Tage, 736 Ereignisse). Ausnahme ist OTE auf DIA über 10 Tage mit t = 2,07, was bei 32 Tests zufällig zu erwarten ist.
  - Keiner der 648 Backtests schlug Buy-and-Hold, und kein Konzept bestand in allen 4 Märkten gegen beide Baselines.
  - Einschränkung: Tagesdaten auf Aktienindizes, keine Session-Logik.
  - [StatOasis](https://statoasis.com/overfit/research/ict-backtest-what-survives)

**Fazit:** Hier besteht eine echte Forschungslücke. Die Beweislast liegt vollständig beim EA-Projekt.

---

## 3. Dokumentierte Backtests: Befunde und Testqualität

| Quelle (Typ) | Setup / Markt | Stichprobe | Ergebnis | Kosten | OOS | Urteil |
|---|---|---|---|---|---|---|
| [GitHub Silver Bullet](https://github.com/cjosh4toyotas-stack/silver-bullet-backtest) (Hobby, laufend aktualisiert, Stand 24.10.2026) | Sweep des 2h-Extrems, dann FVG-Limit, 2R, Fenster 3–4 / 10–11 / 14–15 NY; NQ, ES, CL | NQ 39, ES 49, CL 9 Trades (Juni–Okt. 2026) | NQ: PF 0,58, Trefferquote 28,2 %, −6.465 $; ES: PF 0,69 | 10 $ pro Round-Turn | **ja**: Variante v3 in-sample +0,253 R, out-of-sample −0,337 R | kleine Stichprobe, aber ehrlich |
| [OffbeatForex](https://offbeatforex.com/is-ict-strategy-profitable/) (Anbieter) | ICT-Bot (Sweep, MSS, FVG, Killzones), EURUSD M15 | 125 Trades, 07/2025–07/2026 | Trefferquote 29,6 %, PF 0,81, −15,1 R | **keine** | nein | Regeln vom Autor selbst als „naive Untergrenze“ bezeichnet |
| [GitHub London-ORB](https://github.com/ryousuke5/Gold-AI-Trader/pull/25) | EURUSD, Range 07–08 London, Breakout 08:15–12:00 | 2017–2022, 5 Parameterprofile | PF 0,64–0,80 in allen Profilen | unklar | – | verworfen |
| [Substack QTD](https://quanttradingdiscoveries.substack.com/p/fair-value-gap-backtest-results-eurusd) (Paywall) | FVG EURUSD, 2022–2025 | 1.247 Setups, davon 341 gefiltert | gefiltert: Trefferquote 66,5 %, +1,14 R; ungefiltert 41–55 % | „Spread“ erwähnt, nicht spezifiziert | nicht ersichtlich | Filterkriterien geheim, nicht verwertbar |
| [PuraVidaEdge](https://puravidaedge.com/blog/fair-value-gaps-backtested-honestly) (Anbieter) | FVG M5 auf MNQ, MGC, NAS, XAU | 163–218 Trades je Markt, 12 Monate | PF 1,18 (XAU) bis 1,45 (MNQ) | ja; 1 Tick Slippage kostet 0,10–0,15 PF | nein | dünner Edge, keine OOS-Prüfung |
| [Quantum Algo](https://medium.com/@QuantumAlgo/i-backtested-2-600-trades-using-smart-money-concepts-heres-what-actually-works-bb3c671098c6) (Indikator-Verkäufer) | SMC-Indikator, 10 Assets | 2.600 Trades | Trefferquote 61,2 %, PF 2,17 | unklar | unklar | Interessenkonflikt |
| [FXNX](https://fxnx.com/en/blog/smart-money-concepts-work-backtest-evidence) (Broker-Blog) | regelbasiertes SMC auf Majors | 1.000 Trades | Trefferquote 38–48 %; Verlustserien von 10 und mehr; Blind-Limits an Order Blocks scheitern zu 56,9 % | – | – | Methodik unklar |

Weitere Hinweise:
- Eine 14-jährige Studie zum Overnight-Range-Breakout im DAX kommt netto auf PF 1,25, positiv in 9 von 14 Jahren. Der Autor nennt das einen dünnen Edge, den wenige Punkte Slippage aufzehren ([fxvps](https://fxvps.biz/blog/dax-opening-range-breakout-14-year-study/), nur Snippet gelesen).
- Für den Judas Swing gibt es laut [TMGM](https://www.tmgm.com/en/academy/trading-academy/ict-trading) bzw. dessen Judas-Swing-Seite **keine allgemein verifizierte Trefferquote**.
- Die Seite von QuantifiedStrategies zum London-Breakout war per Bot-Schutz gesperrt. Laut Snippet verlor das Kaufen eines Ausbruchs über das Asia-Hoch in EURUSD häufig oder lag nahe null.

**Bewertung der Testqualität:**
- **Das Muster ist eindeutig.** Mechanisch, mit Kosten und Out-of-Sample geprüft, landet der PF unter 1. Positive Zahlen stammen aus diskretionären Kurzproben, geheimen Filtern, Anbietern mit kommerziellem Interesse und Tests ohne Out-of-Sample-Prüfung.
- **Ein Lehrbuchbeispiel für Selektionsbias** liefert das Silver-Bullet-Repo: Variante v2 brachte bei der Auswahl +0,49 R pro Trade und verlor danach in 7 Trades −5,4 R.
- **Die Filterexplosion von 1.247 auf 341 Setups** bei 66,5 % Trefferquote ist ein klassisches Overfitting-Signal, solange die Filter erst nach Sichtung der Daten gewählt wurden.
- **Der Liquidity-Sweep-Reversal ist keine neue Idee.** Er entspricht der „Turtle Soup“ von Connors und Raschke (1995). Trotz 30 Jahren Bekanntheit fand ich keine robusten, quantifizierten FX-Ergebnisse ([MQL5-Test](https://www.mql5.com/en/articles/2717); im gelesenen Auszug keine Kennzahlen).

---

## 4. Kritik an SMC/ICT

### 4.1 Rebranding klassischer Technischer Analyse

| SMC/ICT-Begriff | Klassisches Vorbild |
|---|---|
| Order Block | Supply/Demand-Zone |
| Liquidity Sweep | Wyckoff Spring/Upthrust bzw. Turtle Soup (Connors/Raschke) |
| BOS/CHoCH | Dow-Theorie der Swing-Struktur |
| Power of 3 (Accumulation–Manipulation–Distribution) | Wyckoff-Zyklus |
| OTE, Premium/Discount | Fibonacci-Retracements |
| „Smart Money“ | Wyckoffs „Composite Operator“, bei Wyckoff ausdrücklich nur ein Denkmodell |

Quellen: [TradingWyckoff](https://tradingwyckoff.com/en/smart-money-concepts/), [XS.com](https://www.xs.com/en/test-blog/smc-smart-money-concepts-explained/), [EarnForex](https://www.earnforex.com/guides/smart-money-concepts-flaws/), [Wyckoff vs. SMC](https://bharathshiksha.com/wyckoff-vs-smc-trading.html)

### 4.2 Bias, Subjektivität, Unfalsifizierbarkeit

- **Rückschaufehler.** Auf historischen Charts sieht man die Zonen, die funktioniert haben. Live konkurrieren viele Kandidaten.
- **Erklärungen lassen sich nicht widerlegen.** Ein Verlust wird umgedeutet: „Du warst die Liquidität“. Ein Framework, das alles erklärt, prognostiziert nichts.
- **Analysten beurteilen gleiche Charts unterschiedlich.** Dieselben Kerzen werden verschieden gelabelt, ein System „SMC“ gibt es daher streng genommen nicht.
- **Viele Freiheitsgrade.** Welcher Swing, welcher Timeframe, welcher Order Block, welches FVG? Jede Wahl ist ein weiterer Versuch und vergrößert das Multiple-Testing-Problem.
- **Repainting und Lookahead.** Ein Swing ist erst nach k Bars bestätigt. Indikatoren, die auf der noch offenen Kerze bestätigen, schönen den Backtest.

Quellen: [ForexMT4Indicators](https://forexmt4indicators.com/smart-money-concepts-guide/), [Backtrex](https://backtrex.com/en/blog/fair-value-gap-trading-strategy)

### 4.3 ICT-Kontroversen

- Es gibt **keine verifizierbare Performance-Historie** von Michael J. Huddleston.
- Berichte über Scheitern bei öffentlichen Challenges stammen aus Foren und Anbieterseiten und sind **nicht verifiziert**. Genannt werden der Robbins Cup 2024 und eine 10k-auf-1-Mio.-Challenge mit widersprüchlichen Jahreszahlen. Die offizielle Rangliste habe ich nicht geprüft.
- Das zugrundeliegende IPDA-Narrativ (ein „Interbank Price Delivery Algorithm“) ist nirgends belegt.

Quellen: [Backtrex Bio](https://backtrex.com/en/blog/michael-j-huddleston-biography-ict-trader), [BabyPips-Thread](https://forums.babypips.com/t/unexpected-the-biggest-forex-fraud-ict-has-claimed-to-enter-the-robbins-cup/1230675), [FundingPips](https://fundingpips.com/blog/ict-silver-bullet-strategy-explained)

### 4.4 „Smart Money“ im Retail-FX/CFD-Kontext

- **Verlustquoten.** Laut ESMA (2018) verlieren 74–89 % der Retail-CFD-Konten Geld, mit Durchschnittsverlusten von 1.600 bis 29.000 € je Kunde.
- **Interessenkonflikte im Market-Maker- bzw. B-Book-Modell sind dokumentiert:**
  - **CFTC gegen FXCM (2017):** Strafe von 7 Mio. $. FXCM hatte seine Beziehung zum wichtigsten Market Maker verschwiegen, der Gegenpositionen zu den Kunden einnahm.
  - **FCA gegen FXCM UK (2014):** Strafe von 4 Mio. £ für asymmetrische Slippage von 2006 bis 2010. Gewinne aus Kursbewegungen behielt der Broker, Verluste gab er an die Kunden weiter.
  - **ESMA-Entscheidung 2018:** Sie nennt asymmetrische Slippage und absichtlich verzögerte Ausführung ausdrücklich als Risiken.
- **Hayley & Marsh (2016):** Bei über 95.000 Retail-FX-Tradern fanden sie keine Lerneffekte. Die Performance sinkt mit zunehmender Erfahrung sogar leicht.
- **Konsequenz für den EA:** Ein „Stop Hunt“ im Retail-Chart kann broker-spezifisch sein, etwa durch Spread-Ausweitung zum Rollover oder bei News oder durch Abweichungen im Datenfeed. Dann ist er kein Marktsignal, sondern ein Kostenfaktor. Mit fremden Daten lässt er sich im Backtest nicht reproduzieren.

Quellen:
- [ESMA Pressemitteilung](https://www.esma.europa.eu/press-news/esma-news/esma-agrees-prohibit-binary-options-and-restrict-cfds-protect-retail-investors) / [ESMA-Entscheidung](https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:32018X0601(02))
- [CFTC-Order](https://www.cftc.gov/idc/groups/public/@lrenforcementactions/documents/legalpleading/enfforexcapitalorder020617.pdf)
- [FCA](https://www.fca.org.uk/news/press-releases/financial-conduct-authority-fines-fxcm-uk-%C2%A34-million-making-%E2%80%98unfair-profits%E2%80%99-and)
- [Hayley & Marsh](https://openaccess.city.ac.uk/id/eprint/15691/)

---

## 5. Methodik für robuste Strategieentwicklung

### 5.1 Overfitting und Multiple Testing: harte Zahlen

- **Bailey, Borwein, López de Prado & Zhu (2014):** Bei 5 Jahren Daten sollte man **höchstens 45 unabhängige Konfigurationen** testen. Sonst erreicht die beste Variante in-sample erwartbar eine Sharpe von 1, obwohl die Out-of-Sample-Sharpe 0 ist. Bei 2 Jahren Daten liegt die Grenze bei 7 Konfigurationen. Ein bloßer Hold-out reicht nicht, weil er die Zahl der Versuche ignoriert.
- **PBO und CSCV (Bailey et al. 2017):** Ein Verfahren, das die Wahrscheinlichkeit schätzt, dass ein Backtest überangepasst ist („Probability of Backtest Overfitting“).
- **Deflated Sharpe Ratio (Bailey & López de Prado 2014):** Korrigiert die Sharpe für die Zahl der Versuche und für nicht-normalverteilte Renditen.
- **Harvey & Liu (2015):** Ein pauschaler Abschlag von 50 % auf die Sharpe ist falsch. Bei marginalen Strategien muss der Abschlag deutlich größer sein. **Harvey, Liu & Zhu (2016):** Ein neuer Faktor braucht **t > 3,0**.
- **White (2000), Reality Check** und **Hansen (2005), SPA-Test:** Hansens Test ist mächtiger und weniger anfällig für schlechte, irrelevante Alternativen. Hsu, Hsu & Kuan (2010) erweitern ihn zu einer schrittweisen Variante.
- **Wiecki et al. (2016, 888 Quantopian-Algorithmen):** Die Backtest-Sharpe erklärt die Out-of-Sample-Performance kaum (R² < 0,025). Je mehr ein Entwickler backtestet, desto größer die Lücke. Volatilität und maximaler Drawdown sind bessere Prädiktoren.
- **Suhonen, Lennkh & Perez (2017):** 215 Strategien von 15 Banken. Die Sharpe fiel im Median von 1,20 im Backtest auf 0,31 live, ein Verlust von 73 %. Komplexe Strategien verfallen um mehr als 30 Prozentpunkte stärker.
- **McLean & Pontiff (2016):** Die Renditen sind out-of-sample 26 % niedriger und nach der Publikation 58 % niedriger.

Quellen:
- [Notices AMS 2014](https://www.ams.org/notices/201405/rnoti-p458.pdf)
- [PBO](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2326253)
- [Deflated Sharpe Ratio](https://www.davidhbailey.com/dhbpapers/deflated-sharpe.pdf)
- [Harvey & Liu](https://www.cmegroup.com/education/files/backtesting.pdf)
- [Harvey, Liu & Zhu](https://www.nber.org/papers/w20592)
- [White 2000 (DOI)](https://doi.org/10.1111/1468-0262.00152)
- [Hansen 2005](https://www.researchgate.net/publication/4724332_A_Test_for_Superior_Predictive_Ability)
- [Stepwise-SPA](https://www.sciencedirect.com/science/article/abs/pii/S0927539810000022)
- [Wiecki et al. (CXO)](https://www.cxoadvisory.com/big-ideas/in-sample-vs-out-of-sample-performance-of-888-trading-strategies/)
- [Suhonen et al.](https://research.aalto.fi/en/publications/quantifying-backtest-overfitting-in-alternative-beta-strategies/)
- [McLean & Pontiff](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2156623)

### 5.2 Validierungsdesign für 25 Instrumente

- **Vorregistrierung.**
  - Alle Definitionen schriftlich fixieren, bevor getestet wird: Swing-Fraktal, BOS auf Close oder Docht, Sweep, FVG-Mindestgröße in ATR, Order Block, Session-Zeiten in UTC mit Sommerzeit-Logik.
  - Jeden Versuch in einem **Trial-Log** festhalten. Daraus ergibt sich die ehrliche Versuchsanzahl für die Deflated Sharpe Ratio.
- **Dreifacher Split.**
  - **Zeit:** zum Beispiel in-sample 2015–2020, Walk-Forward 2021–2023 und ein finaler Hold-out 2024–2026, der genau einmal angefasst wird.
  - **Instrumente:** auf einem Entwicklungsset von 6–8 Paaren entwickeln, das jede Währung mindestens einmal enthält. Danach unverändert auf den übrigen 17–19 Instrumenten validieren.
  - **Gold:** XAUUSD separat behandeln.
- **Walk-Forward**, rollierend (etwa 24 Monate in-sample, 6 Monate out-of-sample). Die Walk-Forward-Effizienz wird üblicherweise, nach Pardo, als Verhältnis von annualisierter Out-of-Sample- zu In-sample-Rendite definiert. Diese Definition konnte ich nicht mehr verifizieren.
- **Combinatorial Cross-Validation** (CSCV bzw. CPCV nach López de Prado) zur Schätzung der PBO.
- **Ereignisstudie vor jeder Strategie.**
  - Jeden Baustein (Sweep, FVG, Order Block, BOS) einzeln gegen **Placebo-Ereignisse** testen. Diese werden zufällig gezogen, aber in derselben Session, demselben Volatilitätsdezil und mit derselben Stop/Target-Geometrie.
  - Gemessen werden Forward-Returns in ATR-Einheiten mit Block-Bootstrap und Holm- oder Benjamini-Hochberg-Korrektur, wie bei StatOasis und im Rehan-Protokoll.

### 5.3 Monte-Carlo- und Stresstests

- **Trade-Bootstrap**, als Block-Bootstrap, weil Trades nach Tagen und Währungen geclustert sind. Daraus die Verteilungen von maximalem Drawdown, längster Verlustserie und Zeit unter Wasser ablesen. Entscheidungsgrundlage sind das 95. bzw. 99. Perzentil, nicht der historische Pfad.
- **Parameter-Perturbation** um ±10–20 %. Gesucht ist ein Plateau, keine einzelne Spitze.
- **Robustheitschecks:**
  - Entry um 1 Bar verzögern
  - Preisrauschen hinzufügen
  - Spread mit 1,5 bzw. 2 multiplizieren
  - Slippage auf Stop-Orders ansetzen
  - die besten 1–5 % der Trades entfernen
- **Random Entry mit identischen Exits** als Benchmark.
- **Zeitverschiebungs-Test als Falsifikation des Killzone-Arguments.** Die Fenster werden um ±1–2 Stunden verschoben. Wenn der Edge dabei nicht schrumpft, ist er nicht zeitgebunden.

### 5.4 Mindest-Trade-Anzahl (eigene Rechnung)

Benötigte Tradezahl N für einen t-Wert von 2 bzw. 3 auf den mittleren R-Wert: N = (t·SD/E)².

| System (Trefferquote, Gewinn in R / Verlust −1R) | Erwartungswert E | Standardabweichung SD | PF | N für t = 2 | N für t = 3 |
|---|---|---|---|---|---|
| 50 %, 1,5R | +0,25 R | 1,25 | 1,50 | 100 | 225 |
| 40 %, 2R | +0,20 R | 1,47 | 1,33 | 216 | 486 |
| 35 %, 2,5R | +0,225 R | 1,67 | 1,35 | 220 | 496 |
| 36,7 %, 2R | +0,10 R | 1,45 | 1,16 | 836 | 1.881 |

Faustregeln wie „30 Trades“ oder „mehr als 50 Trades“, die in der Praxis kursieren, sind viel zu wenig. Bei echten Mehrfachtests ist t ≥ 3 der realistische Maßstab.

### 5.5 Kosten

- **Kosten pro Trade in R** = (Spread + Kommission + Slippage) / Stop-Distanz.
- **Hypothetisches Beispiel:** Bei 1 Pip All-in-Kosten und 10 Pips Stop kostet jeder Trade 0,1 R. Das frisst bei einem Brutto-Edge von 0,2 R die Hälfte auf.
- **Enge Stops.** SMC-Einstiege mit engen Stops (3–5 Pips auf M1) brechen unter realen Kosten zusammen ([FXNX](https://fxnx.com/en/blog/smart-money-concepts-work-backtest-evidence)).
- **Teure Paare.** Crosses wie GBPNZD, EURNZD und GBPAUD sowie Gold haben deutlich höhere Kosten. Dafür eine Mindest-Stop-Distanz verlangen, sodass die Kosten 0,05–0,1 R nicht übersteigen.
- **Konservative Füllannahmen:**
  - Treffen Stop und Target in derselben Kerze, gilt der Trade als Verlust. So machen es das Silver-Bullet-Repo und OffbeatForex.
  - Limit-Orders gelten erst als gefüllt, wenn der Preis um mindestens einen Tick durchläuft.
  - Rollover-Phasen und News-Fenster werden gemieden.

### 5.6 MT5-Datenqualität

- **Modi.** Im Modus „Every tick“ (generiert) sind nur OHLC exakt, die Zwischenticks werden synthetisch erzeugt, und der Spread bleibt pro Minute fest. „Real ticks“ verwenden die Ticks des Brokers. Fehlt für eine Minute die Tickhistorie, **generiert der Tester die Ticks stillschweigend** ([MT5-Hilfe](https://www.metatrader5.com/en/terminal/help/algotrading/tick_generation)).
- **Die Modi liefern sehr unterschiedliche Ergebnisse.** In einem Test von MetaQuotes (2016) ergab dieselbe Strategie 96, 158 bzw. 156 Trades und einen Nettogewinn von +169, −467 bzw. −97 ([MQL5 2612](https://www.mql5.com/en/articles/2612)).
- **Ein MQL5-Artikel vom Oktober 2026** zeigt, wie dünn die Datenbasis sein kann ([MQL5 24562](https://www.mql5.com/en/articles/24562)):
  - Auf zwei Demo-Servern begann die echte Tickhistorie erst **2026**.
  - Der Report meldete „100 % real ticks“, laut Journal liefen aber 72,7 % der Minuten auf generierten Ticks.
  - Die Lehre: Den Anteil echter Ticks über die Journalzeilen prüfen. Out-of-Sample-Fenster dürfen nicht auf eine andere Datenart fallen.
- **Konsequenz für einen Test über 2015–2026:** Externe Tickdaten (zum Beispiel Dukascopy) als Custom Symbols importieren. Zusätzlich die letzten Monate mit den echten Ticks des eigenen Brokers kalibrieren, weil Spreads und Feeds abweichen ([Import](https://www.mql5.com/en/blogs/post/746240), [Custom Symbols](https://www.mql5.com/en/articles/3540)).
- **Kommissionen** im Tester manuell konfigurieren ([MQL5 746300](https://www.mql5.com/en/blogs/post/746300)).
- **Swaps:** Der Tester verwendet die **heutigen** Swap-Sätze für die gesamte Historie ([Forum](https://www.mql5.com/en/forum/513455/page1), [Blog](https://www.mql5.com/en/blogs/post/775419)).
- **Slippage** lässt sich nur über den Modus „Random delay“ emulieren ([Forum](https://www.mql5.com/en/forum/393589/page11)).
- **Multi-Symbol-Tests** ([Blog](https://www.mql5.com/en/blogs/post/769442)):
  - In der Marktübersicht alle Symbole einblenden („Show all“) und die Historie für jedes Symbol vorladen.
  - Die Zeitzone des Broker-Servers verifizieren.

### 5.7 Regimewechsel

Pro Jahr und Volatilitätsregime getrennt auswerten. Extremereignisse prüfen: die Aufhebung des EUR/CHF-Mindestkurses durch die SNB (2015), den GBP-Flash-Crash (2016), Covid (2020) und die JPY-Interventionen (2022/2024). Kein Jahr und kein Instrument sollte einen dominanten Anteil am Gewinn haben.

---

## 6. Risiko und Positionsgrößen

### 6.1 Fixed Fractional und Verlustserien (eigene Rechnung)

Die erwartete längste Verlustserie über 500 Trades habe ich mit der Näherung von Schilling (1990, *The Longest Run of Heads*) berechnet:
- bei 50 % Trefferquote etwa 8
- bei 40 % Trefferquote etwa 11
- bei 35 % Trefferquote etwa 13

Drawdown allein aus diesen Serien:

| Serie | 0,5 % Risiko | 1 % Risiko | 2 % Risiko |
|---|---|---|---|
| 8 Verluste | −3,9 % | −7,7 % | −14,9 % |
| 11 Verluste | −5,4 % | −10,5 % | −19,9 % |
| 13 Verluste | −6,3 % | −12,2 % | −23,1 % |

Der reale maximale Drawdown liegt meist höher, weil sich auch gemischte Sequenzen aufaddieren. Deshalb gehört er per Monte-Carlo bestimmt.

### 6.2 Kelly

- **Formel (Thorp 2006, kontinuierliche Näherung):** Bei einem Einsatz von c-mal Kelly ist die Wahrscheinlichkeit, jemals auf den Anteil x des Startkapitals zu fallen, gleich x^(2/c−1).
- **Folgen:**
  - Bei vollem Kelly halbiert sich das Kapital mit Wahrscheinlichkeit 1/2, bei halbem Kelly mit 1/8.
  - Halbes Kelly erreicht 75 % der Wachstumsrate des vollen Kelly ([Thorp](https://gwern.net/doc/statistics/decision/2006-thorp.pdf)).
  - Kelly ist kurzfristig sehr riskant ([MacLean/Thorp/Ziemba](https://www.researchgate.net/publication/300558392_Good_and_Bad_Properties_of_the_Kelly_Criterion)).
- **Beispiel (eigene Rechnung):** Ein System mit 40 % Trefferquote und 2R Gewinn hat f* = 10 % Risiko pro Trade. 1 % Risiko entspricht also 1/10 Kelly. Dann gilt:
  - P(jemals −50 %) ≈ 2·10⁻⁶
  - P(jemals −10 %) ≈ 13,5 %
- **Entscheidend ist der Schätzfehler.** Ist der wahre Edge nur halb so groß wie im Backtest, verdoppelt sich c. Aus „halbem Kelly“ wird dann faktisch volles Kelly. Nach Suhonen (−73 % Sharpe) ist das kein Randfall.
- **Edge null (eigene Rechnung, Random-Walk-Näherung):** Die Wahrscheinlichkeit, innerhalb von 200 Trades −10 % zu berühren, liegt bei etwa 60 % mit 1 % Risiko und bei etwa 30 % mit 0,5 % Risiko. Kleines Risiko kauft Zeit, aber keinen Edge.

### 6.3 Korrelationsrisiko: die Währungsbeine der 25 Instrumente (eigene Zählung)

| Währung | Anzahl Instrumente | Instrumente |
|---|---|---|
| USD | 8 | 7 Majors + XAUUSD |
| JPY | 7 | USDJPY, EURJPY, GBPJPY, AUDJPY, NZDJPY, CADJPY, CHFJPY |
| EUR | 6 | |
| GBP | 6 | |
| AUD | 6 | |
| CAD | 6 | |
| NZD | 5 | |
| CHF | 5 | |

- **Verflochtene Positionen.** Die Instrumente sind über Dreiecksbeziehungen verbunden: EURJPY ≈ EURUSD × USDJPY. Ein Long auf EURUSD plus ein Long auf USDJPY ist faktisch ein synthetischer Long auf EURJPY.
- **Ein Event trifft viele Positionen.** Eine einzige US-Veröffentlichung wie NFP, CPI oder FOMC trifft bis zu 8 Positionen gleichzeitig.
- **Empfehlung:**
  - Ein Netting-Vektor pro Währung. Jede Position zählt +r für die Basiswährung und −r für die Quote-Währung.
  - Cap von höchstens 1,5–2 R netto pro Währung und höchstens 3–4 R offenem Gesamtrisiko.
  - Vor High-Impact-News keine neuen Trades in betroffenen Währungen.
  - Die rollierende Korrelationsmatrix als Zusatzbremse, mit einem Stresstest, bei dem die Korrelation innerhalb einer Währungsgruppe auf 1 gesetzt wird.

### 6.4 Prop-Firm-Regeln (falls angestrebt)

- **FTMO, offizielle Seite:**
  - **2-Step:** Profitziel 10 % in der Challenge und 5 % in der Verification. Maximaler Tagesverlust 5 %, maximaler Gesamtverlust 10 % statisch, mindestens 4 Handelstage.
  - **1-Step:** Profitziel 10 %, maximaler Tagesverlust 3 %, maximaler Gesamtverlust 10 % als End-of-Day-Trailing. Der beste Tag darf höchstens 50 % des Gesamtgewinns ausmachen.
  - **Instant:** maximaler Tagesverlust 3 %, maximaler Gesamtverlust 10 % intraday trailing.
  - Ob der Tagesverlust auf Equity oder Balance gemessen wird, stellen Drittquellen widersprüchlich dar. Maßgeblich sind die AGB. Regeln zu EAs nennt die Seite nicht. ([FTMO](https://ftmo.com/en/trading-objectives/))
- **Branchenstatistiken, meist sekundär:**
  - Der CEO von The Funded Trader nennt 5–10 % bestandene Challenges und 1–2 % der Kunden mit Auszahlung ([Finance Magnates](https://www.financemagnates.com/forex/only-1-in-20-traders-pass-prop-firm-challenges-reports-the-funded-trader/)).
  - FPFX-Daten (laut Aggregatoren): 14 % bestehen, 7 % bekommen jemals eine Auszahlung ([Aggregator](https://thepropfirmguide.com/prop-firm-statistics/)).
- **Plausibilitätscheck (eigene Rechnung):** Ein kostenloser Random Walk mit Edge null bestünde Phase 1 (+10 % vor −10 %) in 50 % der Fälle und beide Phasen in etwa 33 %. Die real beobachteten 5–14 % deuten auf einen deutlich negativen Netto-Edge bzw. auf Verstöße gegen das Tageslimit hin.
- **Empfehlung für einen Prop-EA:**
  - 0,25–0,5 % Risiko pro Trade.
  - Ein internes Tageslimit bei 40–60 % des Firmenlimits.
  - Alle Positionen vor News schließen.
  - Das 99. Perzentil des Monte-Carlo-Drawdowns muss deutlich unter 10 % liegen.

---

## 7. Realistische Erwartungen und Bewertungsmetriken

**Erwartungen.** Das ist meine Einschätzung, abgeleitet aus Abschnitt 1, 3 und 5, keine Studie.
- Ein robustes, regelbasiertes SMC-artiges Intraday-System auf G10 erreicht nach Kosten bestenfalls einen PF von etwa 1,1–1,4, also +0,05 bis +0,2 R pro Trade.
- **Illustration (eigene Rechnung):** Ein Backtest mit PF 1,33 und +0,2 R schrumpft beim Median-Verfall von −73 % auf etwa +0,054 R, also PF ≈ 1,08.
- Trefferquoten über 60 % bei RR über 2 sind ein Warnsignal für Overfitting oder Lookahead.

**Metriken:**
- **Erwartungswert in R** netto, mit Konfidenzintervall und t-Wert. Van Tharps SQN = √N·E/SD entspricht genau diesem t-Wert.
- **PF** immer zusammen mit Trefferquote und Payoff-Ratio betrachten, nie isoliert.
- **Sharpe, Probabilistic Sharpe und Deflated Sharpe** auf täglichen Equity-Renditen, nicht pro Trade.
- **Rendite im Verhältnis zum Drawdown:** MAR bzw. Calmar (CAGR / maximaler Drawdown), außerdem Ulcer-Index und Zeit unter Wasser.
- **Monte-Carlo-Drawdown** im 95. und 99. Perzentil.
- **Stabilität:**
  - Anteil der Instrumente und Kalenderjahre mit PF > 1
  - Gewinnkonzentration (Anteil der besten 10 % der Trades)
  - Parameter-Plateau
  - Walk-Forward-Effizienz
- **Ausführung:**
  - Kostenanteil am Bruttogewinn
  - Break-even-Kostenmultiplikator
  - Abweichung der Live-Slippage vom Backtest

---

## 8. Empfehlungen: Prozess, Checkliste und Akzeptanzkriterien

Die folgenden Schwellen sind Heuristiken, keine wissenschaftlich fixierten Grenzwerte.

**A. Design**
1. Hypothesen pro Baustein vorab festlegen. Höchstens 4–6 freie Parameter, der Rest per Konvention fixieren.
2. Swings nur bestätigt verwenden und Timeframes ohne Lookahead synchronisieren. Gegen Repainting testen, indem Live-Logik und Backtest-Logik auf identischen Ticks verglichen werden.
3. Sessions in UTC mit Sommerzeit-Logik definieren und den Rollover meiden.
4. Kosten-Gate: Kosten höchstens 0,1 R pro Trade, sonst kein Trade.

**B. Daten**

5. Tickdaten für 2015–2026 für alle 25 Instrumente beschaffen, extern plus Broker-Ticks zur Kalibrierung. Den Anteil echter Ticks per Journal belegen.
6. Kommission, Slippage und „Random delay“ aktivieren. Historische Swaps separat modellieren oder Positionen vor dem Rollover schließen.

**C. Evidenzstufen (Go/No-Go)**

7. **Ereignisstudie:** Mindestens ein Baustein schlägt Placebo-Ereignisse nach Multiple-Testing-Korrektur. Sonst Projekt stoppen oder neu fassen, zum Beispiel mit Volatilitäts- und Fixing-Logik statt SMC-Narrativ.
8. **Walk-Forward und Cross-Instrument-Prüfung**, jeweils out-of-sample:

| Kriterium | Schwelle |
|---|---|
| Trades | mindestens 500 insgesamt, mindestens 30 pro Instrument |
| t-Wert des mittleren R | mindestens 3 |
| Deflated Sharpe Ratio | mindestens 0,95 bei ehrlicher Versuchsanzahl |
| PBO | höchstens 0,2 |
| Netto-PF | mindestens 1,2 |
| Erwartungswert | mindestens +0,1 R |
| PF bei doppelten Kosten | mindestens 1,05 |
| Walk-Forward-Effizienz | mindestens 0,5 |
| Instrumente mit PF > 1 | mindestens 70 % |
| Kalenderjahre mit PF > 1 | mindestens 70 % |
| Gewinnanteil eines einzelnen Instruments oder Jahres | höchstens 25–30 % |
| Parameter ±20 % | PF bleibt mindestens 1,1 |
| Monte-Carlo-Drawdown, 95. Perzentil | höchstens das definierte Risikobudget (privat zum Beispiel 20 %, Prop höchstens 6 %) |
| Zeitverschiebung der Session-Fenster | Edge muss messbar schrumpfen, falls Sessions Teil der These sind |

9. **Finaler Hold-out (2024–2026)** genau einmal anfassen. Bei klarem Verfehlen wird nicht nachoptimiert, sondern verworfen.

**D. Inkubation und Live-Betrieb**

10. Demo oder Mikro-Live über 3–6 Monate bzw. mindestens 100 Trades. Der Live-Erwartungswert muss im 95-%-Konfidenzintervall der Out-of-Sample-Ergebnisse liegen. Die mittlere Slippage darf die Annahme nicht überschreiten.
11. Live mit 0,25–0,5 % Risiko pro Trade, Währungs-Caps aus Abschnitt 6.3 und einem internen Tageslimit starten.
12. **Kill-Switch:** abschalten, wenn der Drawdown größer ist als das 99. Perzentil des Monte-Carlo-Drawdowns, oder wenn der Live-Erwartungswert nach mindestens 100 Trades unter der unteren Konfidenzgrenze liegt. Ein Re-Fit erfolgt nur per Walk-Forward-Protokoll und zählt als neuer Versuch.

---

## 9. Quellenlage und Unsicherheiten

- Bei mehreren Quellen konnte ich nur Abstract oder Suchsnippet lesen, weil SSRN, Theseus und Tandfonline 403 lieferten und PDF-Streams nicht lesbar waren. Betroffen sind Kondapally, Maskey, die Details von Caporale & Plastun und die genauen Quoten aus Osler (2000).
- Die Anbieter-Backtests (Substack, PuraVida, Quantum Algo, FXNX, OffbeatForex, Botsfolio) sind nicht verifiziert und haben zum Teil kommerzielle Interessen.
- Das Silver-Bullet-Repo wird laufend aktualisiert. Die Zahlen gelten für den 24.10.2026.
- Das Websuch-Budget der Session war gegen Ende erschöpft. Deshalb konnte ich nicht mehr prüfen:
  - die WFE-Definition nach Pardo
  - empirische Korrelationswerte der Paare
  - Faktoranteile bilateraler Wechselkurse
  - die FTMO-Regeln zu Expert Advisors

  Die entsprechenden Stellen sind ohne Zahlen bzw. als eigene Rechnung formuliert.
