<!-- Kapitel 3: ICT Zeit-Konzepte, Bias & Entry-Modelle | Deep-Research-Rohbericht (Recherche-Agent), Stand 2026-10-24, unverändert übernommen -->

# Teilbericht: Zeit-Konzepte, Bias & Entry-Modelle (ICT/SMC) als programmierbare Regeln

**Legende:** [W] = Quellen widersprechen sich · [V] = eigener Vorschlag/Default, nicht aus einer Quelle · [U] = unklar oder nicht verifiziert.

**Quellenlage (wichtig für die Gewichtung):**
- Kein ICT-Primärdokument (Video oder Transkript) war direkt prüfbar.
- innercircletrader.net, ictkillzone.com, michaeljhuddleston.org usw. sind Dritt- bzw. Fanseiten. Ob michaeljhuddleston.org eine offizielle ICT-Seite ist, ließ sich nicht verifizieren.
- Fast alle Zahlenschwellen (ATR-Multiplikatoren, Pip-Grenzen) stammen von diesen Autoren, nicht von ICT.
- Unabhängige mechanische Tests zeigen bisher keinen belegten Edge (Abschnitt 4.9).
- Das Websuche-Kontingent der Session war gegen Ende erschöpft. Einige Punkte blieben deshalb unverifiziert und sind mit [U] markiert: IPDA-Datenbereiche, Korrelationen einzelner Crosses, Verfügbarkeit des MQL5-Kalenders im Tester.

---

## 1 Zeit-Konzepte

### 1.1 Zeit-Tabelle

Alle Zeiten sind New-York-Lokalzeit (folgt der US-DST). „Server" meint einen NY-Close-Broker mit GMT+2/+3 und US-Umstellung. Dort gilt ganzjährig **Server = NY + 7 h**.

| Konzept | Default NY [V] | Varianten (Quelle) | Server | UTC EST / EDT |
|---|---|---|---|---|
| Asian Killzone (Entry-Fenster) | 20:00–22:00 | 19:00–22:00 (innercircletrader.net, ictkillzone); 20:00–22:00 (TradingFinder, michaeljhuddleston.org); 20:00–00:00 (TFO-Skript, FibAlgo) [W] | 03–05 | 01–03 / 00–02 |
| Asian Range (Referenz) | 20:00–00:00 | 18:00–00:00 (Leserkommentar); 20:00–02:00 (eine Quelle) [W] | 03–07 | 01–05 / 00–04 |
| CBDR | 14:00–20:00, Bodies | – | 21–03 | 19–01 / 18–00 |
| Flout | 14:00–00:00 | 15:00–00:00 („CBDF"-Skript); LiquidityScan definiert anders [W] | 21–07 | – |
| Midnight Open (MO) | 00:00 | – | 07:00 | 05 / 04 |
| True Day Open | 00:00 | 18:00 (FibAlgo, CME-Sessionstart) [W] | 07:00 | – |
| Judas/Protraction | 00:00–02:00 (normal), ab 02:00 (delayed) | 02:00–03:00 (fxnx); 03:00–05:30 (FXReplay) [W] | 07–09 | – |
| London Open KZ | 02:00–05:00 | Kernfenster 02:00–04:00 (ictkillzone) | 09–12 | 07–10 / 06–09 |
| Silver Bullet London | 03:00–04:00 | – | 10–11 | 08–09 / 07–08 |
| NY AM KZ (FX) | 07:00–10:00 | 07:00–09:00 (innercircletrader.net-Tabelle, ictkillzone); 08:00–11:00 (EBC) [W] | 14–17 | 12–15 / 11–14 |
| NY AM (Indizes, 2022er Mentorship) | 08:30–11:00 | 09:30–11:00 (TFO) | 15:30–18 | 13:30–16 / 12:30–15 |
| Opening Range / 1st Presented FVG | 09:30–10:00 | – | 16:30–17 | – |
| Silver Bullet AM | 10:00–11:00 | – | 17–18 | 15–16 / 14–15 |
| London Close KZ | 10:00–12:00 | 11:00–13:00 (EBC, älter) [W] | 17–19 | 15–17 / 14–16 |
| NY Lunch (keine Entries) | 12:00–13:00 | 11:30–13:30 (ictkillzone); 12:00–14:00 (TFlab) [W] | 19–20 | – |
| NY PM KZ | 13:30–16:00 | 13:30–15:00 (2022er Notizen); 13:30–15:30 (TSG) [W] | 20:30–23 | 18:30–21 / 17:30–20 |
| Silver Bullet PM | 14:00–15:00 | 15:00–16:00 (vereinzelt) [W] | 21–22 | 19–20 / 18–19 |
| FX-Tagesschluss/Rollover | 17:00 | – | 00:00 | 22 / 21 |
| Macros | 02:33–03:00, 04:03–04:30, 08:50–09:10, 09:50–10:10, 10:50–11:10, 11:50–12:10, 13:10–13:40, 15:15–15:45 | FibAlgo: 11 Fenster (u. a. 09:30–09:50, 13:50–14:10, 14:50–15:10). „Jede Stundenwende xx:50–xx:10" (angeblich 2024er Lehre) [W][U] | NY + 7 h | – |

### 1.2 Killzones

**Funktion.** Entries sind nur innerhalb der Killzones erlaubt. Außerhalb gelten Setups als „generally lower quality" (innercircletrader.net, 2022-Seite).

**Instrument-Zuordnung** laut innercircletrader.net:
- Asian: AUDJPY, NZDJPY, AUDUSD und Crosses.
- London: GBPUSD, EURUSD.
- New York: USD-Majors (inkl. USDCAD, USDJPY) und XAUUSD.
- London Close: USD-Majors.
- [V] Für die übrigen Paare: EUR-/GBP-/CHF-Crosses → London; CAD-Crosses → London und NY; AUD-/NZD-Crosses → Asia und London. Umsetzung als Bitmaske pro Symbol.

**London Close** (ictkillzone): Um 10:00 NY wird geprüft, ob die Tages-DOL schon erreicht wurde.
- Wenn ja: Fade/Reversal mit Ziel Tages-Equilibrium (50 % der Tagesrange).
- Wenn nein: Continuation-Pullback.
- Unterfenster: 10:00–10:30 finaler Push, 10:30–11:15 Reversal um den 11:00-Fix, 11:15–12:00 Follow-through. Entries vor 11:15, Exit bis etwa 12:30.
- Audacity und Trinity Trading stufen das Fenster als geringer wahrscheinlich ein; ein Reversal sei nicht automatisch [W].
- [V] London Close nur als Management-Fenster für Exits und Partials nutzen.

### 1.3 Silver Bullet (SB)

**Konsens:** Ein Setup pro Einstundenfenster. Es braucht ein FVG in Bias-Richtung mit Ziel DOL. Kein Chasing; ohne FVG kein Trade.

**Widersprüche [W]:**
- **Muss das FVG im Fenster entstehen?** LuxAlgo: ja. ictkillzone: in sich widersprüchlich. innercircletrader.net: nicht spezifiziert. [V] Kerze 3 schließt im Fenster, Fill ebenfalls im Fenster, sonst Cancel.
- **Ist ein Sweep Pflicht?** ictkillzone: ja, gegen den Bias, im Fenster bzw. bis 10:00. LuxAlgo: Sweep *oder* Strukturbruch. [V] Zwei Modi: STRICT (Sweep + MSS) und BASIC (nur Displacement-FVG).
- **Entry:** CE/50 % (ictkillzone, michaeljhuddleston.org), erste Rejection-Kerze (chartwhisperer) oder Retest der Kante.
- **SL:**
  - jenseits des Sweep-Wicks (ictkillzone)
  - jenseits der FVG-erzeugenden Kerze plus Puffer (innercircletrader.net)
  - jenseits des FVG-Extrems (michaeljhuddleston.org)
- **Mindestdistanz:**
  - michaeljhuddleston.org: Entry→Pool >10 Pips FX bzw. >5 Handles Index; Ziel mindestens 15 Pips bzw. 10 Punkte, maximal etwa 40.
  - innercircletrader.net: „20–30 pip move".
  - ictkillzone: keine Pip-Grenze, aber RR ≥ 1:2 bis T1.

**Weitere Regeln (ictkillzone):**
- Bias steht bis 02:30 (London) bzw. 09:45 (NY) fest.
- High-Impact-News im Fenster → kein Trade.
- Nach einem AM-Gewinn kein PM-Trade.

**Erwartete Frequenz:** 1–2 Trades pro Tag (innercircletrader.net).

### 1.4 Macros

**Erwartetes Verhalten** (LuxAlgo): ein Liquiditäts-Run, dann Rebalancing eines FVG innerhalb von etwa 20 Minuten.

**Einschränkungen:**
- Es gibt keine Statistik.
- Die genauen Minuten variieren je nach Quelle und Kursjahr.
- Die NY-Macros überlappen mit 10:00-Datenreleases.

[V] Nur als Feature bzw. Filter nutzen („Sweep/MSS fällt in ein Macro"), nicht als eigenständiges Signal.

### 1.5 Referenzpreise

- **Midnight Open (00:00):** Preis über MO spricht für bullisches Intraday-Bias, darunter für bärisches (FibAlgo). PO3: Bullische Tage manipulieren unter MO, also „buy below open, sell above open".
- **True Day Open [W]:** Mehrheit und Quarterly Theory setzen ihn auf 00:00 NY. Das GitHub-ICT-Knowledge-Library leitet das aus der 2017er Lektion „Defining Daily Range" ab. FibAlgo setzt 18:00 (CME-Sessionstart).
  - [V] 00:00 für Entry-Filter verwenden; 18:00 als Beginn des Handelstags für die Segmentierung.
- **Session-True-Opens** (Quarterly Theory von Daye, *nicht* ICT): London 01:30, NY 07:30, PM 13:30; Woche Montag 18:00.
- **Index-Opens 08:30/09:30** und das 1st Presented FVG (09:30–10:00): für FX höchstens bei XAUUSD und USD-Paaren relevant [V].
- **Implementierung:** Das Broker-D1 öffnet um 17:00 NY und ist ≠ MO. MO aus dem M1/M5-Bar um 00:00 NY lesen.

### 1.6 CBDR, Asian Range, Flout, Standard-Deviation-Projektionen

**CBDR** (innercircletrader.net):
- Fenster 14:00–20:00 NY, gemessen auf Kerzen-Bodies.
- Größe < 40 Pips, bevorzugt 20–30. Ist die Range breiter, wird der Tag ausgelassen (außer Scalps).
- Messung auf M15, Präzision auf M5. Dienstag und Mittwoch gelten als ergiebigste Tage (Behauptung).
- Entwickelt auf NQ/ES; angeblich auch auf GBPUSD, EURUSD und XAUUSD anwendbar.

**Projektion:** 1 SD = Höhe der Range.
- Sell-Day: Das Tageshoch liegt typisch bei +1 bis +3 SD (ideal ≤ +2), das Tief bei −2 bis −3 SD. Buy-Day gespiegelt.
- Das Gegenextrem entsteht „most probably" in der London-Close-KZ (Behauptung, ohne Daten).

**Asian Range:** 20:00–00:00.
- Filter laut Intraday-Profil: ≤ 20–30 Pips; über 30 Pips ist das Profil ungültig.
- fxnx: < 40 Pips [W].

**Flout:** Fallback, wenn die CBDR zu breit ist.
- 14:00–00:00 (joshuuu) oder 15:00–24:00 (CBDF-Skript) [W].
- Ein Skript halbiert die kombinierte Range und projiziert halbe SD-Schritte.

**Manipulation-Leg-SD** (TTrades, LuxAlgo):
- Fib wird über das Manipulationsbein gelegt (letztes Hoch vor bärischem CISD bzw. letztes Tief vor bullischem CISD).
- −2 bis −2,5 SD: Reaktions-/Retracement-Zone. Schließt der Preis jenseits, ist −4 das Maximalziel (Runner dort schließen).

**Caveat:** LuxAlgo betont, die Multiplikatoren seien „convention, not measured probabilities".

[V] Normierung für 25 Instrumente: `CBDR_max = min(40 Pips, 0.5·ADR20)`, `AR_max = min(30 Pips, 0.4·ADR20)`. Für XAUUSD nur die ADR-Variante.

### 1.7 Judas Swing, Power of 3 / AMD

**Judas Swing** (Intraday-Profil, innercircletrader.net):
- Normale Protraction 00:00–02:00. Sell-Day: Rally über die CBDR, dann Umkehr. Buy-Day gespiegelt.
- Die Protraction soll höchstens 2–3 SD der CBDR betragen.
- Entries ab 01:00 oder nach 02:00. „Delayed Protraction": Umkehr erst ab oder kurz nach 02:00.
- Alternative Definition: Bruch der Asian Range zur London-Eröffnung [W bei den Zeiten].

**PO3/AMD:**
- Akkumulation um MO, Manipulation als Wick gegen den Bias über/unter MO (oft auch über/unter ein Asia-Extrem), Distribution als Expansion.
- Bullischer Tag: Open → Low → High → Close.
- Das Muster ist nur ex post sicher erkennbar (proea, quantum-algo).
- [V] Programmierbar als:
  1. MO-Filter
  2. „Manipulation erkannt" = Preis ≥ 0,25·ATR(M15) jenseits MO gegen den Bias **und** Sweep eines Pools
  3. MSS-Trigger

### 1.8 Weekly Profiles

**ICT Month 7** (via innercircletrader.net und ictsharks): 12 Profile.

**Objektiv prüfbare Kerne:**
- Montag, Dienstag oder Mittwoch erreicht ein HTF-Discount- oder Premium-Array → Classic Tuesday, Wednesday Low/High bzw. Wednesday Reversal.
- Mo–Mi Konsolidierung und Donnerstag gegen 14:00 NY ein Run des Intra-Week-Extrems mit Rejection → Consolidation Thursday Reversal.
- Seek & Destroy Friday → auslassen.

**Evidenz:**
- Keine belastbaren Trefferquoten (LuxAlgo).
- Informelle ForexFactory-Auswertung für EURUSD: 2010 lag das Wochenextrem am häufigsten am Freitag, 2017 YTD am Montag; Dienstag war am *seltensten*. Das widerspricht der Idee „Classic Tuesday" [W].
- [V] Nur als Wochen-Statusfilter verwenden, z. B. Risiko halbieren, wenn bis Mittwochsschluss kein Extrem im HTF-Array liegt.

**Quellen:**
- Killzones/Zeiten: [ictkillzone Kill Zones](https://www.ictkillzone.com/ict-kill-zones), [innercircletrader.net Kill Zones](https://innercircletrader.net/tutorials/master-ict-kill-zones/), [FibAlgo Killzones](https://fibalgo.com/library/ict-killzones-sessions), [TFO-Republikation](https://www.tradingview.com/script/F6U0aVqL-ICT-Killzones-Pivots/), [TradingFinder KZ](https://tradingfinder.com/education/forex/ict-kill-zones/), [EBC](https://www.ebc.com/forex/what-are-ict-killzone-times-simple-trading-hours-guide), [2022-Notizen (Scribd)](https://www.scribd.com/document/666181194/ICT-2022-Mentorship-Notes-TanjaTrades), [London Close](https://www.ictkillzone.com/ict-london-close)
- Silver Bullet: [ictkillzone SB](https://www.ictkillzone.com/ict-silver-bullet), [innercircletrader.net SB](https://innercircletrader.net/tutorials/ict-silver-bullet-strategy/), [LuxAlgo SB](https://www.luxalgo.com/library/concept/silver-bullet/), [michaeljhuddleston.org SB](https://michaeljhuddleston.org/notes/ict-silver-bullet-strategy-capture-10-40-pips-in-just-60-minutes/)
- Macros: [LuxAlgo Macros](https://www.luxalgo.com/library/concept/ict-macros/), [LuxAlgo-Skript](https://www.tradingview.com/script/aLTywnJ0-ICT-Macros-LuxAlgo/), [FibAlgo Macros](https://www.tradingview.com/script/dcAxHlVJ-FibAlgo-ICT-Macro-Times/)
- Opens: [FibAlgo MO/TDO](https://fibalgo.com/library/ict-midnight-open), [Quarter Sequence True Opens](https://quartersequence.com/the-study/true-opens/), [Quantum Algo QT](https://www.quantum-algo.com/blog/guides/ict-quarterly-theory/)
- CBDR/Asia/Flout/SD: [CBDR](https://innercircletrader.net/tutorials/ict-central-bank-dealers-range/), [Intraday Profiles](https://innercircletrader.net/tutorials/ict-intraday-profiles/), [joshuuu Range Deviations](https://www.tradingview.com/script/bo56LlEd-Range-Deviations-joshuuu/), [CBDR-Skripte](https://in.tradingview.com/scripts/cbdr/), [LiquidityScan](https://liquidityscan.io/blog/cbdr-standard-deviations-ict-range-projection), [LuxAlgo SD](https://www.luxalgo.com/library/concept/standard-deviation-projections/), [TTrades SD](https://ttrades.com/standard-deviation-projections/)
- PO3: [innercircletrader.net PO3](https://innercircletrader.net/tutorials/ict-power-of-3/), [MQL5-Blog PO3](https://www.mql5.com/en/blogs/post/771729)
- Weekly Profiles: [innercircletrader.net](https://innercircletrader.net/tutorials/ict-weekly-range-profiles/), [ICT Sharks Month 7](https://forum.ictsharks.com/t/ict-mentorship-core-content-month-7-short-term-trading-defining-weekly-range-profiles/94), [LuxAlgo Profiles](https://www.luxalgo.com/library/concept/session-and-weekly-profiles/), [ForexFactory-Statistik](https://www.forexfactory.com/thread/710352-anticipating-weekly-highslows-on-eurusd)

---

## 2 Daily/Weekly Bias als Regelwerk und Score

### 2.1 Objektive Komponenten

**(1) Previous-Day-Close-Regel** (TTrades; ScalperIntel/joshuuu formulieren sie vollständig). D−1 ist der zuletzt geschlossene NY-Close-Tag, D−2 der Tag davor.

| Bedingung | Bias für D | Ziel |
|---|---|---|
| Close(D−1) > High(D−2) | bullish | High(D−1) |
| Close(D−1) < Low(D−2) | bearish | Low(D−1) |
| High(D−1) > High(D−2), Close zurück ≤ High(D−2) (Sweep) | bearish | Low(D−1) |
| Low(D−1) < Low(D−2), Close zurück ≥ Low(D−2) | bullish | High(D−1) |
| Outside Day (beide Seiten genommen), Close innen | kein Bias | – |
| Inside Day | Farbe von D−1 (ScalperIntel) **oder** neutral (WillyAlgoTrader) [W] | – |

- Der Bias gilt, bis das Ziel erreicht ist; danach ist er neutral (joshuuu).
- „ICT Daily Bias Pro" verlangt einen Body ≥ 50 % der Range für Überzeugung.

**(2) Weekly-Regel:** dieselbe Logik mit PWH/PWL (TTrades, ScalperIntel).

**(3) Struktur D1/H4:** Richtung des letzten Body-Close-Bruchs eines bestätigten Swings. ICT-Swing = 3-Candle-Pivot. [V] Auf D1/H4 ein 5-Bar-Fraktal (N=2) gegen Rauschen.

**(4) HTF Draw on Liquidity** (LuxAlgo-Ranking):
- Kandidaten: PDH/PDL, PWH/PWL, Session-Hochs/-Tiefs, EQH/EQL, unmitigierte HTF-FVGs.
- Rangfolge: höherer TF vor niedrigerem; „engineered" Equal Highs/Lows vor einzelnen Swings; frisch vor angetestet; intern und extern wechseln sich ab.
- [U] IPDA-Lookbacks (20/40/60 Handelstage) werden häufig genannt, waren hier aber nicht verifizierbar. [V] 20-Tage-Hoch/-Tief als zusätzlicher externer Kandidat.

**(5) Premium/Discount:**
- Formel: `pos = (P − R_low)/(R_high − R_low)`. Discount bei < 0,5, Premium bei > 0,5 (LuxAlgo).
- [V] R = Vorwochen-Range und zusätzlich die aktuelle H4-Dealing-Range.

**(6) HTF-PD-Array-Reaktion:** Preis in bzw. Reaktion aus einem unmitigierten D1/H4-Bull-FVG oder -OB ergibt +1; Bear ergibt −1.

**(7) HTF-SMT** auf H4/H1 (Abschnitt 5).

### 2.2 Score [V]

```text
V1 = DailyRuleVote()      ∈{-1,0,+1}   // Gewicht 2
V2 = WeeklyRuleVote()     ∈{-1,0,+1}
V3 = StructureVote(D1); V4 = StructureVote(H4)
V5 = (pos_Vorwoche < 0.5 ? +1 : -1)       // Discount zieht nach oben, Premium nach unten
V6 = HTF_PDArrayVote(D1,H4); V7 = SMTVote(H4/H1)
S  = 2*V1 + V2 + V3 + V4 + V5 + V6 + V7          // Bereich -8..+8
Bias = LONG  wenn S >= +3 und V1 >= 0
       SHORT wenn S <= -3 und V1 <= 0
       sonst NONE (keine Trend-Entries; höchstens Reversal-Modelle nach beidseitigem Sweep)
DOL  = höchstrangiger ungetesteter Pool in Bias-Richtung mit Abstand >= 1.0*ATR(H1)
Neuberechnung: 17:00 NY (neuer D1); Check um 00:00 und 07:00/09:45 NY
Ist DOL getroffen: keine neuen Entries in Bias-Richtung (Bias "verbraucht")
```

**Gewichte nicht optimieren** (Overfitting über 25 Instrumente).

**Evidenz:** Keine der Bias-Regeln veröffentlicht belastbare Trefferquoten. ScalperIntel und joshuuu bieten Statistiktabellen, deren Zahlen sind aber nur Beispiele. Der EA muss die Trefferquote pro Symbol selbst loggen.

**Quellen:** [TTrades Daily Bias](https://ttrades.com/ict-daily-bias-most-simple-mechanical-framework/), [ScalperIntel](https://scalperintel.com/blogs/hub/ict-bias-the-higher-timeframe-directional-edge-that-ties-everything-together), [joshuuu/TTrades-Skript](https://es.tradingview.com/script/ezS0ydMQ-daily-bias-ttrades-x-joshuuu), [ICT Daily Bias Pro](https://www.tradingview.com/script/7DrG46w8-ICT-DAILY-BIAS-PRO/), [WillyAlgoTrader](https://www.tradingview.com/script/4Y1T9TrB-ICT-Structure-Engine-WillyAlgoTrader/), [LuxAlgo DOL](https://www.luxalgo.com/library/concept/draw-on-liquidity/), [LuxAlgo Premium/Discount](https://www.luxalgo.com/library/concept/premium-and-discount/)

---

## 3 Gemeinsame Code-Bausteine

```text
// Bars chronologisch, k = letzter GESCHLOSSENER Bar; Zeit via NY(t) (Abschn. 7)
// ATR = ATR(14) des jeweiligen TF; ADR20 = Mittel(High-Low) der letzten 20 NY-Close-D1
SwingHigh(i)    := H[i]>H[i-1] && H[i]>H[i+1]            // ICT 3-Candle, bestätigt nach Close i+1
SwingLow(i)     := L[i]<L[i-1] && L[i]<L[i+1]
EQH(a,b)        := |H[a]-H[b]| <= 0.1*ATR, dazwischen kein höheres High          [V]
BullFVG(k)      := L[k] > H[k-2]; Zone [H[k-2], L[k]]; CE = Mitte                // Bear: H[k] < L[k-2]
FVG_min         := max(0.15*ATR, 2*Spread)                                       [V]
Displacement(i) := Body(i) >= 1.3*ATR && Body/Range >= 0.6 && FVG mit Bar i+1    // Quellen 1.2–1.5×ATR / ≥2× Ø-Body(10)
SweepSSL(lvl,j) := L[j] < lvl - pen  &&  Reclaim: C[j] > lvl oder C[j'] > lvl, j'≤j+3; pen=max(1 Pt, 0.05*ATR) [V]
RunSSL(lvl,j)   := C[j] < lvl - 0.25*ATR und kein Reclaim in 3 Bars → Ausbruch, kein Sweep  [V]
BullMSS(s)      := erster m∈(s, s+12] mit C[m] > High(letzter SwingHigh vor s), Body-Close, Leg s..m enthält Displacement
BullCISD(s)     := C[m] > Open der ersten Kerze der letzten ununterbrochenen Down-Close-Serie ins Tief s
BullOB          := letzte Down-Close-Kerze vor dem Displacement-Leg; Zone [L,H] oder Body [W]; MeanThreshold=(O+C)/2
BullBreaker     := L1 → SwingHigh H → L2<L1 (Sweep) → C>H; Breaker = letzte Up-Close-Kerze(n) an H; Zone Body
PD(P)           := (P-R_low)/(R_high-R_low); OTE = 0.62–0.79 Retracement
buf             := max(2*Spread, 0.1*ATR(M15))                                   [V]
```

**Zu den Definitionen:**
- **MSS:** Ein Wick-Poke zählt nicht; es braucht einen Body-Close jenseits des Swings (innercircletrader.net).
- **CISD:** feuert früher als ein MSS und erzeugt mehr Fehlsignale (LuxAlgo).
- **Breaker:** Die Mehrheit („up-close candle in the swing high prior to an old low being violated", WritoFinance, Audacity) widerspricht ForexMT4Systems und QuantVPS, die „down-close" schreiben [W]. Die Mehrheitsdefinition ist hier verwendet.
- **FVG wird zur IFVG** bei einem Body-Close durch das gesamte Gap (Wicks zählen nicht).

**Quellen:** [Market Structure](https://innercircletrader.net/tutorials/ict-market-structure/), [ICT Core (1,2×ATR)](https://www.tradingview.com/script/cVV7Z0rI-ICT-Core-MSS-Liquidity-Raids-FPFVG-Gap-Quarters/), [ForexMT4Systems 2022](https://forexmt4systems.com/education/smart-money-concepts/ict-2022-model/), [Backtrex Displacement](https://backtrex.com/en/blog/ict-displacement-candle-market-concept), [LuxAlgo CISD](https://www.luxalgo.com/library/concept/change-in-state-of-delivery/), [IFVG](https://innercircletrader.net/tutorials/ict-inversion-fair-value-gap/), [Order Block](https://www.ictkillzone.com/ict-order-block), [WritoFinance Breaker](https://www.writofinance.com/breaker-block-smc-and-ict-in-forex/), [Audacity Breaker](https://audacity.capital/trading-guides/what-is-a-breaker-block-in-trading/)

---

## 4 Entry-Modelle

Alle Modelle sind für Long beschrieben; Short ist jeweils gespiegelt.

### 4a ICT 2022 Mentorship Model

**Kernsequenz:** Sweep → Displacement/MSS → FVG-Retracement.

**TF:** D1/H4 Bias, M15 Liquidität, M5 Ausführung. M1 erst nach etwa 100 geloggten M5-Setups (innercircletrader.net).

**Fenster:** London 02:00–05:00; NY 08:30–11:00 (Index) bzw. 07:00–10:00 (FX) [W].

**Entry:**
- ForexMT4Systems bevorzugt CE; ein Limit an der Nahkante oder CE ist üblich.
- Stop jenseits des gesweepten Extrems. „Ein Pip dahinter ist zu eng" (innercircletrader.net).

**Ziel:** gegenüberliegender Pool. Mindest-CRV 1:3 (innercircletrader.net) bzw. 2:1 (ForexMT4Systems) [W].

**Invalidierung:** Body-Close zurück jenseits des Sweep-Extrems.

```text
ON closed M5 bar, NY in KZ, Bias==LONG:
  pools = {AsiaLow, Low(00:00-03:00 NY), LondonLow (nur NY-KZ), PDL, EQL(M15)}
  s = erster SweepSSL(pool) seit KZ-Start               ; sonst return
  m = BullMSS(s)                                         ; sonst return
  g = jüngstes BullFVG im Leg s..m, Größe >= FVG_min     ; sonst return
  if CE(g) > s.low + 0.5*(High(s..m)-s.low): return      // Entry nur im Discount des Legs
  entry = CE(g)    // aggressiv: g.top
  sl    = s.low - buf                                    // Variante eng: g.candle1.low - buf
  dol   = nächster ungetesteter BSL-Pool über entry (Leg-High, AsiaHigh, LondonHigh, PDH, EQH)
  if RR(entry,sl,dol) < 2: return
  BuyLimit(entry, sl, dol, expiry = KZ.end)
  CANCEL vor Fill: C[M5] < s.low | dol berührt | KZ.end
```

**Statistik:** „No reliable success rate" (ForexMT4Systems). Die übrigen Angaben sind unbelegt.

**Quellen:** [innercircletrader.net 2022](https://innercircletrader.net/tutorials/complete-ict-trading-strategy-2022/), [ForexMT4Systems 2022](https://forexmt4systems.com/education/smart-money-concepts/ict-2022-model/), [FundingPips 2022 (1,5×ATR)](https://fundingpips.com/blog/ict-2022-model), [AlgoKings](https://www.algokings.net/learn/ict-2022-model/)

### 4b Silver Bullet

**TF:** M15 Kontext, M5 (oder M1/M3) Ausführung.

```text
PARAM W ∈ {03:00-04:00, 10:00-11:00, 14:00-15:00}; MODE ∈ {STRICT, BASIC}
AT W.start-15min: Bias != NONE; dol = DOL(Bias)
   require Dist(price, dol) >= max(15 Pips, 0.2*ADR20)          // [V] Normierung der 15-Pip-Regel
ON closed M5 bar in W:
  if MODE==STRICT:
     s = SweepSSL(pools={Range(W.start-60min..W.start), Asia/London H/L, EQL}, Fenster [W.start-30min, now])
     require s und BullMSS(s)
  g = ERSTES BullFVG, dessen 3. Kerze in W schließt (und nach s bei STRICT), Displacement-erzeugt
  entry = CE(g)
  sl = (STRICT ? s.low : g.candle1.low) - buf
  require RR(entry, sl, dol) >= 2
  BuyLimit(entry, sl, dol, expiry = W.end)            // kein Fill im Fenster → Cancel, kein Chasing
  max 1 Trade/Fenster; nach AM-Gewinn kein PM-Trade; Red-News in W → skip
```

**Management** (ictkillzone): 50 % am ersten IRL, 25 % am zweiten IRL, 25 % am ERL; nach T1 auf Breakeven.

**Zeit-Exit [W]:**
- innercircletrader.net: nicht wegen des Fensterendes schließen.
- GitHub-Test: 2-Stunden-Zeit-Exit.
- LuxAlgo: manche schließen an Session-Marken.

### 4c OTE (Optimal Trade Entry)

**Bezug:** ein Impuls-Leg, das auf Sweep oder MSS folgt (Strefa Tradingu).
- Zone 62–79 %, Sweet Spot 70,5 %.
- Flacher als 62 %: zu schwach, warten. Tiefer als 79 %: Impuls fraglich.

**Stop:** jenseits 1,0 plus Puffer. Strefa Tradingu nennt 10–20 Pips FX, 50–100 Cent Gold. [V] ATR-basierter Puffer.

**Ziele** (Strefa Tradingu): −0,27 erstes Ziel; −0,62 Breakeven plus Partial; −1,0 Hauptziel; −2/−2,5 Trend-Tag; −4 Maximum. Eine andere Strefa-Variante nimmt das Leg-Extrem (0) als TP1 [W].

**TF:** H1/M15 für das Leg, M5 zur Bestätigung.

```text
INPUT: s.low (=1.0), legHigh (=0.0, bestätigter SwingHigh nach MSS), R = legHigh - s.low
zone  = [legHigh-0.79R, legHigh-0.62R]; sweet = legHigh-0.705R
require NY in KZ und Overlap(zone, FVG oder OB des Legs)        // Konfluenz [V] Pflicht
entry = sweet  (Variante: 3 Tranchen 0.62/0.705/0.79)
sl    = s.low - buf
TP: legHigh+0.27R (Partial) | +0.62R (BE + Partial) | +1.0R (Haupt) | Runner +2.0R/+2.5R
CANCEL: Preis erreicht legHigh+0.27R vor Fill | Close < s.low | KZ-Ende
```

**Statistik:** Im StatOasis-Tagesbar-Test auf SPY: t = −0,17, 0 % der Varianten schlagen Zufall. Einziges signifikantes Ergebnis: DIA, 10 Tage, t = +2,07. Gilt nur für Tagesbars.

**Quellen:** [Strefa Tradingu Fib-Levels](https://strefatradingu.pl/en/blog/ict-fibonacci-levels/), [GrandAlgo OTE](https://grandalgo.com/blog/ict-optimal-trade-entry-ote), [Backtrex OTE](https://backtrex.com/en/blog/ict-optimal-trade-entry-ote-fibonacci-guide)

### 4d Unicorn (Breaker + FVG)

**Definition:** Sweep, Shift, Overlap. Nur die Schnittmenge aus Breaker und FVG ist die Entry-Zone; ohne Overlap kein Unicorn (LuxAlgo, innercircletrader.net).

**SL-Varianten [W]:**
- jenseits der Breaker-Fernseite bzw. des gesweepten Swings (LuxAlgo, Equiti)
- 10–20 Pips unter dem Tief der FVG-erzeugenden Kerze (innercircletrader.net)
- 10–20 Pips jenseits FVG/Breaker (QuantVPS)

**Ziele [W]:** fix 1:2 (FluxCharts, QuantVPS) oder nächste Liquidität (Equiti, innercircletrader.net).

**TF:** Setup auf M15/M5, Entry auf M5/M3.

```text
on M15/M5: L1=SwingLow; H=SwingHigh nach L1; L2 = Low < L1.low nach H (Sweep)
m = erster Close > H.high nach L2 mit Displacement
B = Up-Close-Kerze(n) am Swing H (letzte vor Abfall zu L2); zoneB = [min(O_B), max(C_B)]   // Variante Wicks
g = BullFVG im Leg L2..m;  U = zoneB ∩ g; require Größe(U) >= FVG_min
entry = CE(U)  (aggressiv: U.top); sl = L2.low - buf
tp = DOL(Bias) mit RR >= 2  (Fallback fix 2R)
CANCEL: Close < zoneB.bottom (LuxAlgo-Invalidierung) | KZ-Ende | Gegen-Bias
```

**Statistik:** keine Zahlen („meaningfully higher", ohne Beleg).

**Quellen:** [innercircletrader.net Unicorn](https://innercircletrader.net/tutorials/ict-unicorn-model/), [LuxAlgo Unicorn](https://www.luxalgo.com/library/concept/unicorn/), [FluxCharts](https://www.fluxcharts.com/articles/trading-strategies/ict-strategies/ict-unicorn), [QuantVPS](https://www.quantvps.com/blog/the-ict-unicorn-model-strategy), [Equiti](https://www.equiti.com/sc-en/news/trading-ideas/what-is-the-ict-unicorn-model/)

### 4e Turtle Soup

**Zwei klar verschiedene Varianten:**
- **Original** nach Raschke/Connors, *Street Smarts*: neues 20-Tage-Tief; das vorige 20-Tage-Tief liegt mindestens 4 Sessions zurück; Buy-Stop 5–10 Ticks über dem alten Tief, nur für den Tag gültig; Stop 1 Tick unter dem Tagestief; Trailing.
  - „Plus One"-Variante: 3 Sessions Abstand; Close am oder unter dem alten Tief; Buy-Stop am Folgetag.
  - RoboForex nennt für das Original „3 Tage" (Verwechslung mit Plus One) [W].
- **ICT-Variante:** beliebiger offensichtlicher Pool, Wick über/unter dem Level, Body schließt zurück innen. Schließt der Preis jenseits, ist es ein echter Breakout und das Setup ist ungültig. Danach LTF-MSS und Entry in FVG/OB; Stop jenseits des Wicks plus kleiner Puffer.
  - Nicht in Trendmärkten und nicht in Asia-/NY-Lunch handeln (innercircletrader.net).
  - Level „respected ≥ 2 sessions" (FXOpen).

```text
(e1) Raschke D1:  if Low[0] < min(Low[1..20]) und Index(min(Low[1..20])) >= 4:
       BuyStop = prevLow20 + 5..10 Ticks (nur heute); SL = Low[0]-1 Tick; Trailing (kein fixes TP belegt)
(e2) ICT intraday: levels = {PDH/PDL, Session-H/L >= 2 Sessions alt, EQH/EQL M15}
       in KZ: SweepSSL(level) mit Reclaim; RunSSL → verwerfen
       BullMSS auf M5 → entry CE(FVG)/OB; sl = Sweep-Wick - buf
       tp = Gegenseite der Range / DOL, RR >= 2; skip wenn D1-Bias SHORT (Trendfilter)
```

**Statistik:**
- innercircletrader.net behauptet 60–70 % Trefferquote bei CRV 1:2 bis 1:3, ohne Daten.
- Eine proea-Simulation auf zufälligen Kerzen ist nicht aussagekräftig.

**Quellen:** [proea Turtle Soup](https://proea.app/en/blog/turtle-soup), [Street Smarts (Auszug)](https://pdfcoffee.com/street-smarts-laurence-a-connors-and-linda-bradford-raschke-1995-file-goc-5-pdf-free.html), [innercircletrader.net Turtle Soup](https://innercircletrader.net/tutorials/ict-turtle-soup-pattern/), [Captain Trading](https://captain-trading.com/en/free-trading-course/turtle-soup), [FXOpen](https://fxopen.com/blog/en/what-is-ict-turtle-soup-and-how-can-you-use-it-in-trading/)

### 4f Market Maker Buy/Sell Model (MMBM/MMSM)

**Voraussetzungen** (innercircletrader.net, MMBM):
- HTF-Struktur bullisch.
- DOL oberhalb.
- LTF-Sell-Programm vor Erreichen des HTF-PD-Arrays.

**Phasen:** Original Consolidation → Engineering Liquidity (Lower Highs) → Smart Money Reversal am HTF-Array → Liquidity Hunt. Andere Quellen zählen 5 Phasen [W].

**Entry:** nach LTF-MSS (plus SMT) im FVG.

**Stop:** 10–20 Pips unter dem letzten Swing-Low vor dem MSS.

**Ziele:**
- Fib vom SMR-Low (1) zum MSS-High (0): −1 (1. Partial), −1,5 (2. Partial), −2 (1. Ziel), −2,5 (Final).
- Zwischenziele: die Lower Highs der Engineering-Phase.
- Endziel: High der Original Consolidation oder HTF-DOL, je nachdem, was näher liegt.

**TF:** D1/H4 (Swing) bzw. H1 (Intraday) für die Struktur; M15/M5 für MSS.

```text
OC   = jüngstes H1-Fenster >= 8 Bars mit Range <= 1.0*ATR(H1)                       [V]
EL   = nach OC-Bruch nach unten >= 2 M15 Lower Highs (als BSL-Ziele speichern)
SMR  = Preis in HTF-Discount-Array (D1/H4 Bull-FVG/OB oder altes Tief) + SweepSSL; optional SMT bull
MSS  = M15/M5 Close > letzter LH mit Displacement → BullFVG
entry= CE(FVG); sl = lastSwingLow(vor MSS) - max(10 Pips, 0.15*ADR20)              [V-Normierung]
TP   = Fib(1=SMR.low, 0=MSS.high): -1 (25%), -1.5 (25%), -2 (25%), -2.5 (Rest); Deckel min(OC.high, HTF-DOL)
```

**Statistik:** keine gefunden.

**Quellen:** [MMBM](https://innercircletrader.net/tutorials/ict-market-maker-buy-model/), [MMSM](https://innercircletrader.net/tutorials/ict-market-maker-sell-model/), [TradingFinder MMSM](https://tradingfinder.com/education/forex/ict-market-maker-sell-model-2023/)

### 4g Klassisches SMC: HTF POI + LTF CHoCH + Inducement

**Ablauf** (TradingStrategyGuides, fxnx):
1. HTF-Trend bestimmen.
2. POI = OB/FVG in Discount bzw. Premium.
3. Preis muss im POI sein.
4. LTF-Sweep (Inducement), dann CHoCH.
5. Entry am LTF-OB oder -FVG.

**Inducement** = kleiner, früher Swing vor dem echten POI.

**Zielregel** (TradingView-Modell): TP am nächsten „weak high" bei 1:3. Kein Trade, wenn ein unmitigiertes HTF-FVG/OB vor dem Ziel das CRV unter 2–3 drückt.

**Entry-Varianten:**
- „Risk Entry": Limit direkt am HTF-POI.
- „Confirmation Entry": Entry erst nach LTF-Sweep und CHoCH. Diese ist der Default.

**TF:** H4/H1 für den POI; M5/M1 für den CHoCH.

```text
H4 Trend bull (letzter BOS up); DR = H4-Dealing-Range
POI = unmitigiertes H4/H1 Bull-OB/FVG mit PD(POI.mid) < 0.5, durch Displacement entstanden
on Touch(POI): M5: LH = letzter LTF Lower High; IDM = jüngstes LTF-SwingLow oberhalb/im POI
   require SweepSSL(IDM)                     // Inducement genommen
   require Close > LH mit Displacement binnen 24 Bars  (CHoCH)
   entry = MeanThreshold(LTF-OB) oder CE(LTF-FVG)
   sl = min(POI.low, Sweep.low) - buf
   tp = nächstes H1/H4 SwingHigh/BSL; require RR >= 2 (Quelle: 3)
VOID: H1 Close < POI.low (POI mitigiert/ungültig) | gegenläufiges HTF-Array vor tp
```

**Statistik:** IndicatorEdge (mechanisch, 738 Assets):
- Order Block: 40,0 % Trefferquote, Alpha −6,5 %
- Fair Value Gap: 42,8 %, Alpha −7,7 %
- Change of Character: 50,6 %, Alpha −5,7 %

**Quellen:** [TradingStrategyGuides SMC Entry Models](https://tradingstrategyguides.com/the-ultimate-guide-to-smc-entry-models-trading-like-the-smart-money/), [fxnx HTF Bias + LTF Entry](https://fxnx.com/en/blog/smc-htf-bias-ltf-entry-precision-guide), [SmartMoneyTrader Inducement](https://www.smartmoneytrader.co/blog/ict-inducement-trading), [TradingView SMC-Modell](https://www.tradingview.com/chart/EURUSD/PBhizQcH-SMC-Mechanical-Entry-Models/)

### 4h Judas Swing / London-Open-Reversal nach Asia-Range-Sweep

**fxnx:**
- Asian Range 20:00–00:00 (Wicks), unter 40 Pips; Judas um 02:00–03:00.
- Der Sweep muss auf der Bias-Seite liegen. Wird die falsche Seite gebrochen und Preis läuft weiter: kein Gegentrade.
- M5-MSS, Entry FVG/OB, Stop unter dem Judas-Tief.
- TP1 = gegenüberliegendes Asia-Extrem, TP2 = doppelte Range.

**FXReplay:** Sweep 03:00–05:30, M5-MSS, TP Gegenseite, kein Management.

**Intraday-Profil:** zusätzlich CBDR < 40 Pips, Protraction ≤ 2–3 SD; Stop jenseits des London-Session-Extrems; Ziel HTF-DOL oder 50–70 Pips.

**Entry-Varianten** (Suchergebnis-Zusammenfassung):
- Market am CHoCH-Close: höhere Mitnahme, weiterer Stop.
- Limit am FVG (Default).

```text
AT 00:00 NY: AR = [High,Low] von 20:00–00:00 (Wicks); CB = Body-High/Low 14:00–20:00
  require AR.size <= AR_max; optional CB.size <= CBDR_max (sonst Flout 14:00–00:00 als Anker)
  SD(k) = CB.low - k*CB.size  (k = 1..3)
WINDOW 00:00–05:00 NY, Bias==LONG:
  s = SweepSSL(AR.low); require s.low >= SD(3)        // Protraction <= 3 SD
  if zuerst AR.high per RunBSL gebrochen: kein Trade heute
  m = BullMSS(s) auf M5 (Body-Close)
  entry = CE(BullFVG im Leg) | OB-MeanThreshold; bevorzugt entry < MidnightOpen
  sl = s.low - buf
  tp1 = AR.high (50 %); tp2 = AR.high + AR.size (= 2× Range) oder CB.high + 2..3 SD oder DOL
  Zeit-Exit 12:00 NY [V]; Red-News 02:00–05:00 → skip
```

**Statistik:** keine (fxnx rechnet mit hypothetischen 40 %).

**Quellen:** [fxnx Asian Range](https://fxnx.com/en/blog/master-the-ict-asian-range-forex-strategy), [FXReplay Judas](https://fxreplay.com/strategies/judas-swing-model), [Intraday Profiles](https://innercircletrader.net/tutorials/ict-intraday-profiles/)

### 4.9 Berichtete Trefferquoten (kritisch)

| Quelle | Ergebnis | Bewertung |
|---|---|---|
| innercircletrader.net (Silver Bullet) | 55–65 % bei 1:3 | Selbstauskunft |
| FundingPips | unabhängige Backtester berichten 50–65 % statt 70–80 % | ohne Daten |
| michaeljhuddleston.org | über 77 % | ohne Daten |
| EA-Verkaufsseiten | über 80 % | unverifiziert |
| GitHub, mechanischer SB-Test auf NQ (06–10/2026) | 39 Trades, 28,2 % Trefferquote bei 2R, PF ≈ 0,58, −0,25R pro Trade | Stichprobe klein |
| skoolboykenny-PR | Ø-Verlust −1,61R statt −1R durch Spread und Slippage bei M1-Entries | Detektoren noch nicht validiert |
| HowToTrade | nur „selektiv profitabel", stark regimeabhängig | – |
| StatOasis (648 Tagesbar-Tests, Indizes) | kein signifikanter Edge, 0 schlagen Buy & Hold | Killzones/Intraday nicht getestet |
| IndicatorEdge | alle SMC-Konzepte mit negativem Alpha; Liquidity Sweep 71,9 % Trefferquote, aber Alpha −7,4 % | „Win-Rate-Falle" |

**Quellen:** [GitHub SB-Backtest](https://github.com/cjosh4toyotas-stack/silver-bullet-backtest), [skoolboykenny PR](https://github.com/skoolboykenny/skoolboykenny/pull/4), [HowToTrade PDF](https://howtotrade.com/wp-content/uploads/2024/04/ICT-Silver-Bullet-Trading-Strategy.pdf), [FundingPips SB](https://fundingpips.com/blog/ict-silver-bullet-strategy-explained), [StatOasis](https://statoasis.com/overfit/research/ict-backtest-what-survives), [IndicatorEdge](https://indicatoredge.io/smart-money)

---

## 5 SMT Divergence

**Definition:** Zwei korrelierte Instrumente bestätigen ein Extrem nicht gemeinsam. Das nicht bestätigende Instrument ist das Signal.
- Positiv korreliert: A macht ein Lower Low, B ein Higher Low → bullisch.
- Invers korreliert (z. B. DXY): Logik spiegeln.

**Einsatz:** als Bestätigung am HTF-PD-Array, gefiltert nach Daily Bias; Ausführung auf M15 oder darunter (innercircletrader.net). Wegen vieler Fehlsignale Filter, nicht Trigger (comelearnforex).

**Algorithmus [V]:**

```text
Gate: Pearson(LogReturns M15, 20 Handelstage) |rho| >= 0.8, sonst Paar deaktivieren
inv:  B'.high = 1/B.low, B'.low = 1/B.high          // für inverse Paare (MT4-Indikator: "InvertCorrelation")
// (1) Level-SMT (robust, kein Pivot-Matching):
BullSMT_Level(lvl) := A.low[t] < A.lvl  &&  B.low über dasselbe Zeitfenster >= B.lvl
                      // lvl = gleich definierter Pool beider Symbole: Asia-Low, London-Low, PDL
// (2) Pivot-SMT:
p1,p2 = letzte zwei bestätigte SwingLows von A (Fraktal N=1..3; MT4-Default 3), p2.low < p1.low
b1 = min(B.low[t1-w..t1+w]); b2 = min(B.low[t2-w..t2+w]); w = 2 Bars
BullSMT_Pivot := b2 > b1
Bars synchron über identische Zeitstempel (CopyRates); fehlende Bars → kein Signal
```

**Paare aus der Liste.** Die Korrelationswerte sind undatierte Snapshots und vom Timeframe abhängig:

| Paar | Korrelation (Quelle) | Eignung |
|---|---|---|
| EURUSD–GBPUSD | +0,85 (FXAbsolute), 91,3 % (TradingFinder) | Standard |
| AUDUSD–NZDUSD | +0,92 (FXAbsolute), 96,5 % (TradingFinder) | sehr gut |
| EURJPY–GBPJPY | 85,4 % (Myfxbook) | gut |
| AUDJPY–NZDJPY | 88,2 % (TradingFinder) | gut |
| AUDJPY–EURJPY | 95,4 % (Myfxbook) | gut |
| EURUSD/GBPUSD–DXY (synth., invers) | Triple-SMT als „A+" (fxnx) | gut |
| XAUUSD–DXY (synth., invers) | XAGUSD als Standardpartner fehlt in der Liste | mittel |
| EURUSD–USDCHF (invers); EURAUD–EURNZD; GBPAUD–GBPNZD; EURCAD–GBPCAD; EURCHF–GBPCHF | nicht verifiziert [U] | per Gate prüfen |
| AUDNZD, CADCHF, AUDCAD, CADJPY, USDCAD, USDJPY | kein klarer Partner (USDJPY/USDCAD allenfalls gegen DXY) | eher nein |

**Synthetischer DXY:** `50.14348112 · EURUSD^−0.576 · USDJPY^0.136 · GBPUSD^−0.119 · USDCAD^0.091 · USDSEK^0.042 · USDCHF^0.036`.
- USDSEK steht nicht in der Instrumentenliste. [V] Entweder zusätzlich beziehen oder die übrigen fünf Gewichte renormieren; die Konstante ist für SMT irrelevant.
- High/Low eines synthetischen Bars sind nicht simultan. [V] Den DXY auf M1-Closes berechnen und zu M5/M15-OHLC aggregieren.

**Quellen:** [innercircletrader.net SMT](https://innercircletrader.net/tutorials/ict-smt-divergence-smart-money-technique/), [TacticalJay SMT](https://www.tradingview.com/script/8FyXyvXM-SMT-Divergence-ICT/), [MT4 SMT-Indikator](https://forexmt4systems.com/indicators/smt-divergence-ict-01-indicator/), [fxnx Triple SMT](https://fxnx.com/en/blog/ict-triple-smt-divergence-spot-smart-money), [comelearnforex](https://www.comelearnforex.com/strategies/smt-divergence/), [EarnForex DXY](https://www.earnforex.com/guides/dxy-us-dollar-index/), [MQL5 DXY Custom Symbol](https://www.mql5.com/en/forum/481824), [TradingFinder Korrelation](https://tradingfinder.com/products/tools/fx-correlation/), [Myfxbook](https://www.myfxbook.com/forex-market/correlation), [FXAbsolute](https://fxabsolute.com/forex-correlation-table)

---

## 6 Trade-Management

**Quellenbefund:**
- **Partials am IRL, Rest zum ERL:**
  - LiquidityScan: erst Partial am internen Ziel, danach Breakeven, Rest zur externen DOL; maximal 1 % Risiko; mindestens 2:1 bis T1.
  - Aron Groups: Breakeven eine Stufe später [W].
- **Silver Bullet:** 50/25/25 mit Breakeven nach T1 (ictkillzone); Partial bei 10 Pips (michaeljhuddleston.org).
- **OTE:** Breakeven an −0,62.
- **MMBM:** −1 / −1,5 / −2 / −2,5.
- **OSOK (wöchentlich):** 80 % bei 50 Pips, 20 % bis über 75 trailen.
- **ICT-Archivist (2022er Twitter Spaces):**
  - „Take partials, leave a small runner"; Stops nachziehen.
  - Zwei-Trade-Regel: nach zwei verlorenen Trades Schluss für den Tag; der zweite Trade mit höchstens 50 % Größe.
  - Nach einem Verlusttag kleiner handeln; Gegen-Bias-Trades mit höchstens 50 % Größe.
- **Scribd-Notizen „Day 13":** Risiko nach Verlusten von 2 % auf 1 % auf 0,5 % senken; erst wieder hoch, wenn 50 % des Drawdowns aufgeholt sind. Nicht als ICT-Originalwortlaut verifiziert.
- **Explizite Trailing-Regeln:** keine Quelle nennt welche [U].

**Defaults [V]:**

```text
risk = 0.5 % (max 1 %); Gegen-Bias-Trades verboten (bzw. 50 %)
TP1 = erstes IRL im Weg (Leg-Extrem, gegenläufiges FVG-CE, Session-H/L) falls >= 1R, sonst 1.5R → 50 % schließen
nach TP1: SL = Entry ± (Spread + 0.1*ATR(M5))
TP2 = DOL/ERL → 25 %; Runner 25 %: Trailing unter letztem bestätigten M15-SwingLow - buf, Deckel -4 SD
Kein DOL innerhalb 4R → Fixed-Target 2R
Zeit-Exits: London-Trades 12:00 NY, NY-Trades 16:00 NY; Freitag alles bis 16:00 NY
            keine neuen Entries 16:00–19:00 NY (Rollover-Spreads)
Limits: 1 Trade/Fenster/Symbol, max 2/Symbol/Tag; global Stopp nach 2 Verlusten oder -2R pro Tag
Exposure: max 1 Position je Währung+Richtung (EURUSD-Long + GBPUSD-Long = doppelter USD-Short)
Spread-Filter: Spread <= 0.1 * SL-Distanz; M5 statt M1 bei breiten Crosses (AUDNZD, CADCHF, EURNZD ...)
```

**Quellen:** [LiquidityScan](https://liquidityscan.io/blog/how-to-build-a-complete-ict-trading-model-step-by-step), [Aron Groups DOL](https://arongroups.co/technical-analyze/draw-on-liquidity-in-ict/), [Liquidity-Provider](https://liquidity-provider.com/articles/internal-vs-external-range-liquidity-in-ict-trading/), [ICT Archivist 2022](https://ictarchivist.com/2022/), [Scribd ICT Material](https://www.scribd.com/document/348443220/i-Ct-Material-Reference), [innercircletrader.net OSOK](https://innercircletrader.net/tutorials/ict-one-shot-one-kill/)

---

## 7 Umsetzung: NY-Zeit, Serverzeit, DST

**Umstellungsdaten:**
- **USA:** zweiter Sonntag im März bis erster Sonntag im November.
- **EU:** letzter Sonntag im März bis letzter Sonntag im Oktober.
- **Mismatch 2026:** 8.–28. März und 25.–31. Oktober. Die Oktober-Woche beginnt morgen.
- **Mismatch 2027:** 14.–28. März.

**Broker-Typen:**
- **NY-Close-Broker (GMT+2/+3 nach US-Daten):** NY = Server − 7 h ganzjährig, 5 D1-Bars pro Woche. In Mismatch-Wochen verschieben sich nur Londoner Zeiten um +1 h Serverzeit.
- **Broker mit EU-Umstellung** (Drittseite über Tickmill): In Mismatch-Wochen liegen NY-Fenster eine Stunde verschoben, der D1 schließt um 18:00 NY.

**Konzeptfrage [V]:** In Mismatch-Wochen entspricht die London-KZ 02:00–05:00 NY nur 06:00–09:00 London statt 07:00–10:00.
- Parameter `KZ_LONDON_REF = NY|LONDON`, Default NY (ICT-Konvention).
- Beide Varianten backtesten oder die Wochen auslassen; das kostet laut MQL5-Forum 2–3 Wochen pro Jahr.

**Tester-Falle:** Im Strategy Tester liefert `TimeGMT()` die simulierte Serverzeit. Den Offset daher aus Datumsregeln berechnen, nicht aus der Terminaluhr (MQL5-Forum).
- Alternativen: Offset aus dem Wochenschluss schätzen (Freitag 17:00 NY, Mehrheitsvotum über die letzten 45 Tage; hinkt bei Umstellungen nach); amrali-Bibliothek.

```text
bool IsUSDST(utc){ s = NthSunday(Y,3,2)+07:00 UTC; e = NthSunday(Y,11,1)+06:00 UTC; return s<=utc<e; }
bool IsEUDST(utc){ s = LastSunday(Y,3)+01:00 UTC; e = LastSunday(Y,10)+01:00 UTC; return s<=utc<e; }
int  SrvOffset(utc){ NYCLOSE: IsUSDST(utc)?3:2 | EUDST: IsEUDST(utc)?3:2 | FIXED: input | AUTO: Wochenschluss-Votum }
datetime ToNY(srv){ if(mode==NYCLOSE) return srv - 7h;
                    utc = srv - SrvOffset(srv-2h)*3600;  // Näherung, an Umstellungsstunden prüfen
                    return utc - (IsUSDST(utc)?4:5)*3600; }
```

**Validierung pro Broker:**
- 5 D1-Bars pro Woche und keine Sonntags-Bars.
- Wochenschluss um 00:00 Serverzeit.
- Volumenspitze zur London-Eröffnung um die Umstellungsdaten herum dort, wo erwartet (MQL5-Forum).

**Bar-basierte Logik:**
- CBDR, Asia Range und Flout liegen über der Broker-Tagesgrenze. Immer mit NY-Zeitstempeln arbeiten, nie mit Server-D1-Grenzen.
- Den MO aus Intraday-Bars lesen.
- „Every tick based on real ticks" verwenden, damit Limit-Fills, Spreads und SL/TP-Reihenfolge stimmen.

**News-Filter [U]:** Nach meinem Kenntnisstand ist der MQL5-Wirtschaftskalender im Tester nicht verfügbar; das ist zu verifizieren. Gegebenenfalls einen CSV-Import der Termine nutzen.

**Quellen:** [MQL5 Forum DST-Gap](https://www.mql5.com/en/forum/517402), [MQL5 Forum Offset im Tester](https://www.mql5.com/en/forum/518277), [MQL5 Blog Serverzeit](https://www.mql5.com/en/blogs/post/774934), [amrali TimeGMT-Lib](https://www.mql5.com/en/code/48291), [Dealing with Time](https://www.mql5.com/en/articles/9926), [Tickmill-Serverzeit](https://www.chiefidea.com/forex-brokers/latest/tickmill-trading-hours-and-server-time/)

---

## 8 Empfehlung für vollautomatisches Trading

**1. Kern-Engine „Sweep → Displacement/MSS → FVG-Limit" (2022-Modell) mit Silver Bullet als NY-Fenster.**
- Jeder Baustein ist geometrisch oder zeitlich exakt definierbar: Zeitfenster, Pool-Sweep mit Reclaim, Body-Close-MSS, ATR-Displacement, 3-Kerzen-FVG.
- Entry per Limit mit festem Stop am Sweep-Extrem, Ziel am vorab definierten Pool mit RR-Untergrenze und klarer Cancel-Logik.
- Silver Bullet ist dieselbe Engine mit härterem Zeitfilter (FVG und Fill im Fenster, DOL-Mindestabstand). Das ergibt eine Codebasis und pro Fenster separat auswertbare Statistik.
- Priorität: London-SB und NY-AM für USD-Majors und XAUUSD. SB-PM nur nach eigenem Backtest.

**2. Judas Swing / Asia-Range-Sweep (London).**
- Fixe, quellenübereinstimmende Referenzrange 20:00–00:00 NY und genau ein Ereignis pro Tag.
- Objektive Größenfilter (Asia Range, CBDR) und natürliche Ziele (gegenüberliegendes Range-Extrem, doppelte Range, SD-Projektionen).
- Deckt EUR-, GBP- und CHF-Majors und -Crosses in London ab und ergänzt damit Modell 1 zeitlich.

**3. Optional: ICT-Turtle-Soup an PDH/PDL bzw. Session-Extremen** als dritter, unkorrelierter Trigger. Klare Wick/Close-Regel, Level ohne Diskretion. Alternativ das mechanische Raschke-Original auf D1/H4.

**Nicht als eigenständige Modelle priorisieren:**
- **MMXM:** „Original Consolidation" und die Kurvenphasen sind kaum robust detektierbar.
- **Unicorn:** selten, Breaker-Definition widersprüchlich. Besser als Qualitäts-Flag in Modell 1.
- **Klassisches SMC POI + CHoCH:** viele Freiheitsgrade (welcher OB gilt, was ist Inducement), daher Overfitting-Risiko.
- **OTE:** Entry-Ort, kein Setup. Als optionale Limit-Platzierung in Modell 1 nutzen.
- **Weekly Profiles:** nur ex post klassifizierbar. Höchstens als Risikofilter.

**Pflicht vor dem Live-Betrieb:** Kein Modell hat unabhängig belegte Profitabilität; die einzigen mechanischen Tests sind negativ oder nicht signifikant.
- Walk-Forward- und Out-of-Sample-Tests pro Instrument mit echten Spreads und Kommission.
- ATR-normierte, gemeinsame Parameter statt Symbol-Feintuning.
- Logging pro Fenster, Modell und Symbol.
- Instrumente mit ungünstigem Spread/ADR-Verhältnis ausschließen.
- Bevorzugt M5 statt M1 ausführen (Kosten-Drift auf −1,6R pro Verlust bei M1).
