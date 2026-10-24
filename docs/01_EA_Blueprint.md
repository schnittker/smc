# SMC-EA für MetaTrader 5 – Blueprint v0.1 (Entwurf)

Stand: 24.10.2026 · Grundlage: Deep-Research in `docs/research/01–07` · Status: **Entwurf zur Abstimmung, noch kein Code**

**Ziel (vom User festgelegt):** **FTMO 2-Step Challenge, Swing-Konto, 100.000 USD**, auf MT5. Für alle FTMO-spezifischen Regeln gilt zusätzlich `02_FTMO_Challenge_Plan.md`: FtmoGuard, Risikoleiter, Margin-Budget, Kostenmodell und Compliance.

Dieses Dokument übersetzt die Recherche in eine Spezifikation, die sich implementieren lässt. Wo die Quellen mehrdeutig sind (fast überall), trifft es eine **Default-Entscheidung [D]** und macht sie parametrierbar. Herleitung und Quellen stehen in den Research-Kapiteln; Verweise sind als `→ K1 §3` notiert (Kapitel 1, Abschnitt 3). Was du entscheiden musst, steht in Abschnitt 18.

---

## 1. Ausgangslage

- **SMC/ICT ist kein festes Regelwerk.** Es ist ein Sammelbegriff für Price-Action-Konzepte: Marktstruktur, Liquidität, Order Blocks, Fair Value Gaps und Zeitfenster. ICT selbst nennt fast keine Zahlen, und jede Implementierung definiert die Begriffe anders (→ K1, K2, K4).
- **Ein belegter Edge fehlt bisher.** Unabhängige mechanische Tests mit Kosten zeigen keinen robusten Vorteil (→ K5 §2–3). Eine Studie zu Sweep/Reclaim an PDH/PDL über 22 Instrumente und 11.990 Trades findet keinen signifikanten Effekt. **Unbestätigtes** Fading an Liquidität ist dort sogar signifikant schlechter als Zufall: 40,9 % Trefferquote gegenüber 49,4 % in der Kontrolle (→ K7 §9.1). Deshalb verlangt jedes Modell eine Bestätigung (MSS bzw. CISD). Das beste gefundene Ergebnis bringt etwa +0,1 R pro Trade **vor** Kosten (HTF-OB → LTF-CISD mit Trendfilter, → K4 §4). Ein Preprint (SSRN, Mahadzva) findet, dass Sweeps eher **Fortsetzung** als Umkehr vorhersagen (→ K4 §4).
- **Konsequenz für den Aufbau.** Der EA wird als **kausal korrekte SMC-Feature-Engine mit Research- und Validierungsschicht** gebaut. Handelsmodelle sind austauschbare Module. Mit echtem Geld laufen sie erst, wenn sie die Evidenz-Gates in Abschnitt 16 bestanden haben.

---

## 2. Leitprinzipien (verbindlich)

| # | Prinzip | Umsetzung |
|---|---|---|
| P1 | **Kausalität** | Jedes Objekt (Pivot, Pool, Zone, Event) speichert Ursprungs- *und* Bestätigungszeit. Signale nutzen nur bestätigte Information, nur geschlossene Bars (shift ≥ 1) und als HTF-Kontext die letzte geschlossene HTF-Bar. Keine zentrierten Fenster, keine Normierung über den ganzen Datensatz. |
| P2 | **Skalenneutralität** | Schwellen werden in ATR- bzw. ADR-Einheiten angegeben, nie in Pips oder Points. Ausnahmen: Spread, Stops-Level, Tick-Größe. |
| P3 | **Ein Codepfad** | Warm-up, Backtest und Live durchlaufen dieselbe inkrementelle Verarbeitung pro geschlossener Bar. |
| P4 | **Research first** | Jedes Event wird exportiert. Ein Baustein muss Placebo-Tests bestehen, bevor eine Strategie darauf aufbaut. |
| P5 | **Kosten zuerst** | Kein Trade, wenn Spread + Kommission + Slippage mehr als 10 % des Risikos ausmachen. |
| P6 | **Wenige freie Parameter** | Höchstens 5 optimierbare Parameter je Modell, alles andere per Konvention fixiert. Jeder Versuch kommt ins Trial-Log. |
| P7 | **Zentrales Portfolio-Risiko** | Ein Exposure-Vektor über 8 Währungen plus XAU. Pending-Orders zählen, als wären sie gefüllt. |
| P8 | **Fail-safe** | Kein Handel bei unsynchronisierten Daten, unbestätigtem Zeitmodell oder fehlenden Berechtigungen. |

---

## 3. Systemarchitektur

**[D] Ein Portfolio-EA auf einem Chart** (EURUSD), der alle 25 Symbole über Polling bedient. Mit `InpSymbols="EURUSD"` läuft derselbe Code als Einzelinstanz, für Debugging und Einzeltests (→ K6 §1.1).

```
  OnTimer (live 250–500 ms; im Tester an M1-Wechsel gekoppelt)     OnTick (Chart-Symbol)
                     \                                           /
                      v                                         v
              ┌──────────────────────── Dispatcher ─────────────────────────┐
              │ je Symbol: BarClock.Poll() in der Reihenfolge D1→H4→H1→M15→M5 │
              └──────────────────────────────┬──────────────────────────────┘
                                             v  neue geschlossene Bar(s)
  SessionClock ──► SymbolContext[s]: Ringpuffer MqlRates je TF, ATR (eigene RMA),
  (Server→UTC→NY)                    Spread-Profil je Stunde, Kontraktdaten
                                             v
        ┌──────── Engines: rein, ohne Terminal-Aufrufe, Daten über IMarketData ─────────┐
        │ SwingEngine → StructureEngine → LiquidityEngine → PDArrayEngine → BiasEngine   │
        └──────────────────────────────────────┬────────────────────────────────────────┘
                                               v  Events: PIVOT, BOS, CHOCH, MSS, SWEEP, BREAK,
                                               v          FVG_*, OB_*, POOL_*, BIAS_*
                   EventBus ──► EventExporter (CSV für Research)
                                               v
                   Modelle: A „Sweep→MSS→FVG“ (Presets LDN / NY / SB), C „HTF-POI→LTF-Bestätigung“
                                               v  TradeIntent {Symbol, Richtung, Entry, SL, TP, Ablauf, SetupID}
                   Filter (Kosten, Spread, News, Rollover, Wochenende, Daten)
                                               v
                   RiskManager (Lots) → ExposureManager (Währungsvektor, Tages- und Wochenlimits)
                                               v
                   TradeExecutor (Filling, Stops/Freeze, Expiry, Retry/Reconcile)
                                               v
                   PositionManager (Zeit-Exits, optional BE/Partial/Trail – nur bei Bar-Close)
```

**Event-Modell und Polling (→ K6 §1.2, §1.3):**
- `OnTick` feuert nur für das Chart-Symbol. Alle anderen Symbole werden im Timer gepollt.
- Die New-Bar-Erkennung läuft je Symbol und TF über `SERIES_LASTBAR_DATE`. Nach Wochenende oder Reconnect holt sie verpasste Bars nach (Catch-up). Signale entstehen nur aus „frischen“ Bars.
- Symbolübergreifende Logik (SMT, Exposure) rechnet erst, wenn alle beteiligten Symbole die neue Bar haben. Im Tester laufen die Symbole nicht synchron.

---

## 4. Zeitmodell

### 4.1 Serverzeit → UTC → New York (→ K6 §3, K3 §7)

- **[D] Broker-Modell `SRV_TZ_NY_CLOSE`:** GMT+2/+3 mit US-Sommerzeitumstellung. Damit gilt ganzjährig NY = Server − 7 h, und 00:00 Server entspricht 17:00 NY. Alternativen: `SRV_TZ_EU_DST` und `SRV_TZ_FIXED`.
  - **Für FTMO bestätigt:** „GMT+2 + DST“ nach US-Kalender (→ K8 §1, §6).
  - Der **FTMO-Tag** für den Daily Loss ist davon getrennt: Er folgt dem Prager Kalender, der Reset liegt um 01:00 Serverzeit bzw. 02:00 in den Lückenwochen (→ FTMO-Plan §4.1).
- **Im Tester ist `TimeGMT()` wertlos**, weil es dort gleich der Serverzeit ist. Das Modell kommt deshalb aus einem Input und wird an der History **validiert**: Die letzte H1-Bar vor dem Wochenende muss um 16:00 NY öffnen. Das wird mit Mehrheitsentscheid über die letzten 26 Wochen geprüft, einschließlich der Abweichungswochen. Scheitert die Prüfung, ist der Handel gesperrt.
- **Live** wird zusätzlich gegen `TimeTradeServer() − TimeGMT()` geprüft. Voraussetzung ist eine NTP-synchrone Uhr.
- **DST-Regeln:**
  - US: zweiter Sonntag im März bis erster Sonntag im November.
  - EU: letzter Sonntag im März bis letzter Sonntag im Oktober.
- **Abweichungswochen** (geprüft):

  | Jahr | Frühjahr | Herbst |
  |---|---|---|
  | 2026 | 08.03.–29.03. | **25.10.–01.11. (ab morgen)** |
  | 2027 | 14.03.–28.03. | 31.10.–07.11. |

  **[D]** Killzones bleiben in NY-Zeit fix (ICT-Konvention). Ein Parameter `KZ_LONDON_REF = NY | LONDON` erlaubt den Vergleichstest.
- **Tagesgrenzen:**
  - **[D]** Der Handelstag läuft von 17:00 bis 17:00 NY („FX-Tag“).
  - PDH/PDL, ADR und die Tageskerzen-Regel nutzen NY-Close-Tage. Wenn der Server kein NY-Close-Broker ist, werden diese Tage aus H1 aggregiert.
  - Midnight Open (00:00 NY) wird aus der M5-Bar gelesen.

### 4.2 Zeitfenster (alle NY-Zeit)

| Fenster | Zeit (NY) | Rolle im EA [D] | Quelle |
|---|---|---|---|
| Asian Range | 20:00–00:00 | Referenz-Range und Liquiditätspool (Hoch/Tief) | → K3 §1.1 |
| Asian KZ | 20:00–23:00 | Preset A-ASIA (optional, v1 aus; JPY-, AUD-, NZD-Gruppen) | → K3 §1.2, K7 §3.1 |
| Pre-London | 00:00–02:00 | Pool (Judas-Fenster) | → K3 §1.7 |
| **London KZ** | **02:00–05:00** | Entry-Fenster Modell A-LDN, C | Konsens |
| Silver Bullet LDN | 03:00–04:00 | Preset A-SB (Variante) | → K3 §1.3 |
| London-Range (für NY) | 02:00–07:00 | Pool für NY-Sweeps | [D] |
| **NY AM KZ (FX)** | **07:00–10:00** | Entry-Fenster Modell A-NY, C | Konsens |
| Silver Bullet AM | 10:00–11:00 | Preset A-SB (Variante; USD-Paare, XAUUSD) | → K3 §1.3 |
| London Close | 10:00–12:00 | nur Management, keine Entries | → K3 §1.2 |
| NY Lunch | 12:00–13:00 | keine Entries | → K3 §1.1 |
| NY PM KZ / SB PM | 13:30–16:00 / 14:00–15:00 | default **aus**, nur nach eigenem Backtest | → K3 §8 |
| Rollover-Sperre | 16:45–18:15 | keine neuen Orders und keine SL-Änderungen; XAUUSD-Pause 17:00–18:00 | → K6 §6 |

---

## 5. Timeframe-Stack

| TF | Rolle | Pivots L_int / L_ext [D] | Bemerkung |
|---|---|---|---|
| **D1** (NY-Close) | Bias (Tageskerzen-Regel), PDH/PDL, ADR20, DOL-Kandidaten | 3 / 10 | L_ext = 50 wäre auf D1 rund 2,5 Monate Lag (→ K1 §7.3) |
| **H4** | Swing-Struktur, Dealing Range, HTF-PD-Arrays | 5 / 20 | |
| **H1** | POI für Modell C, externe Pools | 5 / 30 | |
| **M15** | interne Struktur, Pools (EQH/EQL, Swings), Session-Ranges | 5 / 40 | EQ-Pivots: L_eq = 3 |
| **M5** | Trigger: STH/STL (Fraktal n = 1), Sweep, MSS, FVG-Entry | 5 / 50 | |
| M1 | optional, **nicht Default** | – | Kostendrift: −1,6 R Ø-Verlust bei M1-Entries (→ K3 §4.9) |

Für HTF-Logik wird immer die letzte geschlossene HTF-Bar gelesen. Schließen mehrere TFs gleichzeitig, wird von oben nach unten verarbeitet.

Der **Trigger-TF ist pro Symbol konfigurierbar** (Abschnitt 11.2). Tier 1 und 2 nutzen M5. Tier 3 nutzt M15, mit H1 als POI- bzw. interne Ebene. Grund sind die Kosten: Bei M5 lägen sie dort bei über 25 % eines 1×ATR-Stops.

---

## 6. Engines

### 6.1 SwingEngine (→ K1 §1, K4 §1.1)

- **Leg-Pivots (LuxAlgo-kompatibel):**
  - Kandidat c = k − L (k ist die zuletzt geschlossene Bar).
  - `newHi = High[c] > max(High[c+1..k])`, `newLo = Low[c] < min(Low[c+1..k])`.
  - Ein Pivot entsteht nur beim Wechsel des Leg-Zustands; Startzustand BEAR. Highs und Lows alternieren dadurch automatisch.
  - Lag = L Bars. `tPivot = Time[c]`, `tConfirm = Time[k]`.
- **ICT-Short-Term-Pivots (Fraktal n = 1)** für den Trigger-TF:
  - Hoch: `High[c] > High[c+1] && High[c] ≥ High[c−1]`. Das ist die Tie-Regel von MT5: rechts strikt, links ≥.
  - Lag = 1 Bar.
- **Optionaler Amplitudenfilter** (default aus): |P − letzter Gegenpivot| ≥ k·ATR14, mit k_int = 0,5 und k_ext = 1,5.
- **Outside Bar** (Hoch- und Tief-Pivot zugleich): Die Reihenfolge wird aus M1 bestimmt, sonst gilt die Close-Richtung.
- **Pivots werden nie zurückgezogen.** Dedup durch Zurückziehen ist der Hauptfehler der Python-Library (→ K4 §2).

### 6.2 StructureEngine (je TF, Layer INT und EXT) (→ K1 §2–3)

- **Zustand je Layer:**
  - `bias ∈ {UNKNOWN, BULL, BEAR}`
  - Levels H/L mit `crossed`-Flag
  - `trailTop`/`trailBot` (nur EXT)
  - `protH`/`protL`
  - Flag `TRANSITION`
- **Bruch nur per Close:** `Close[k] > H.px + brkBuf` und `!H.crossed`, mit `brkBuf` [D] = 0, optional 0,05–0,1·ATR14.
  - **BOS**, wenn der Bias nicht BEAR ist; ein UNKNOWN-Bias wird damit beim ersten Bruch BULL.
  - Sonst **CHOCH**.
  - Bei bullischem Bruch: `protL = min(Low)` zwischen Pivot-Bar und Bruch-Bar.
- **EXT-Layer [D]:** Der Trend kippt nur bei einem Close jenseits `protL`/`protH` (**CHOCH_STRICT**). Der Bruch des jüngsten Swing-Pivots gegen den Trend erzeugt nur `CHOCH_WARN`.
- **INT-Layer:** LuxAlgo-Semantik; jeder Gegenbruch kippt den Bias. Ein INT-Bruch wird unterdrückt, wenn das INT-Level gleich dem EXT-Level ist.
- **`TRANSITION`** wird gesetzt bei INT-CHoCH gegen den EXT-Trend. Gelöscht wird es bei einem INT-BOS in Trendrichtung oder bei EXT-CHOCH_STRICT.
- **Warm-up:** Bias bleibt UNKNOWN bis zum ersten EXT-Bruch. In UNKNOWN wird nicht gehandelt.
- **MSS (Trigger-TF M5)** = interner CHoCH + vorheriger Sweep + Displacement. Ausgelöst wird er durch ein SWEEP-Event der LiquidityEngine:
  1. **Referenz:** `ref` = jüngstes STH (n = 1) mit `tPivot` < Sweep-Bar.
  2. **Fenster:** `W_mss` Bars [D 20, Bereich 10–30].
  3. **Bruch:** `Close > ref.px + brkBuf`. Disarm, wenn `Close < sweepExtreme`.
  4. **Displacement** im Leg von Sweep-Extrem bis Bruch-Bar (6.5).
  5. **[D] RequireFVG = true:** Im Leg muss ein FVG ≥ minFVG liegen.

### 6.3 LiquidityEngine (→ K1 §4, K3 §1)

**Pool-Typen und Startgewichte für das DOL-Ranking:**

| Typ | Quelle / Definition [D] | Gewicht |
|---|---|---|
| PMH/PML | Vormonat (NY) | 5 |
| PWH/PWL | Vorwoche (NY) | 4 |
| IPDA20 | 20-Handelstage-Hoch/-Tief (rollierend) | 3,5 |
| PDH/PDL | Vortag (NY-Close-Tag) | 3 |
| EQ_EXT / EQ | ≥ 2 bestätigte Pivots (M15, L_eq = 3) innerhalb `tolEQ` = 0,1·ATR200(M15), mit Pullback ≥ 0,5·ATR14 dazwischen und Abstand ≥ 2·L_eq Bars | 3 / 2,5 |
| SWING_EXT | H1/H4 EXT-Pivots | 2 |
| SESSION | Asia 20–00, Pre-London 00–02, London 02–07 (Hoch/Tief) | 1,5 |
| SWING_INT | M15 INT-Pivots | 1 |

Die Gewichte sind ein Vorschlag aus einer qualitativen Rangfolge (→ K1 §4.4) und müssen validiert werden. Pools innerhalb `tolEQ` werden zusammengeführt; der Pool-Preis ist das extremste Mitglied.

**Lebenszyklus**, ausgewertet auf jeder geschlossenen M5-Bar, auch für HTF-Pools:
- **ACTIVE → SWEPT:** Wick jenseits des Levels, Close zurück im Range (Sweep auf derselben Bar).
- **ACTIVE → PENDING:** Close jenseits.
  - PENDING → SWEPT (`FAILED_BREAK`) bei Reclaim innerhalb `nReclaim` = 3 Bars.
  - PENDING → BROKEN nach `nAccept` = 2 Closes jenseits.
- **ACTIVE → EXPIRED:** Alter > maxAge(TF). Richtwerte: M15 5 Tage, H1 20 Tage, H4 40 Tage.
- SWEPT und BROKEN **verbrauchen** den Pool als Ziel (ICT: „Liquidität ist genommen“).

**Bid/Ask-Korrektur:** Buy-Stops über Hochs triggern auf dem Ask. Für BSL gilt deshalb ein Pool als durchstochen bei `High + spreadEst > px`; für SSL reicht `Low < px` (Bid-Chart, → K1 §7.4).

**Mindest-Penetration:** [D] 1 Tick, Parameter `minPenATR` von 0 bis 0,2·ATR14(M5).

**Sweep-Event** enthält: gesweepte Pool-Typen, Extrempreis, Tiefe in ATR, Reclaim-Bars, Session, Zeit.

### 6.4 PDArrayEngine (→ K2, K4 §1.3–1.4)

**FVG**
- Drei Kerzen c1, c2, c3. Bullisch: `Low[c3] > High[c1]`, Zone `[High[c1], Low[c3]]`, CE = Mitte.
- **Filter:** Gap ≥ max(`kFVG`·ATR14, 3·Median-Spread) [D `kFVG` = 0,2]; `Close[c2] > High[c1]`; Body/Range(c2) ≥ 0,5.
- **Zustände:** CREATED → ACTIVE → TOUCHED → CE_REACHED → FILLED (Wick an der fernen Kante) → INVALIDATED (Body-Close jenseits der fernen Kante, dann entsteht eine IFVG). Daneben EXPIRED.
- **Kappung:** 20–30 Zonen je TF und Richtung.

**Order Block, Hybrid aus ICT und LuxAlgo**, ausgelöst durch einen bullischen Strukturbruch (Pivot s, Bruch-Bar b):
1. `legLow = argmin Low (s, b]`, bei Gleichstand die späteste Bar.
2. Displacement-Start d (6.5).
3. **OB-Kerze:** letzte Down-Close-Kerze in `[max(s+1, legLow−2), d−1]`. Gibt es keine, gilt `legLow` mit Flag `noOpposite`.
4. **Serie:** maximal 3 zusammenhängende Gegenkerzen.
5. **Zone:**
   - Entry-Zone = Body (proximal = `bodyHi`)
   - MT = Body-Mitte
   - `stopRef = min(loFull, Low[legLow])`
   - Ist die Zone breiter als `maxH`·ATR, wird auf den Body reduziert.
6. **Gültig nur, wenn:** Displacement ok, Close im Leg über `hiFull` (Trade-through) und [D] FVG im Leg.

**OB-Zustände:**
- TOUCHED
- MT_REACHED
- WEAKENED: Close jenseits MT, keine neuen Entries
- INVALIDATED: Close jenseits distal, Breaker-Kandidat
- CONSUMED: maxTouches LTF 1, H1/H4 2
- EXPIRED

**Breaker / Mitigation Block:** bei CHoCH. Hat das Hoch vor dem Bruch ein älteres Hoch gesweept (`H2 > H1`), entsteht ein Breaker mit Full Range, sonst ein Mitigation Block mit Body. Im v1 nur als Qualitäts-Flag (Unicorn = Breaker ∩ FVG).

**Nur für Research erfasst:** IFVG, BPR, Volume Imbalance, Liquidity Void, NWOG/NDOG (NDOG nur bei echter Tagespause laut `SymbolInfoSessionTrade`), Rejection Block, Propulsion Block.

**Speicherung:**
- Struct-Arrays mit festen Obergrenzen je Symbol, TF und Typ; kein `new` pro Zone.
- **Lifecycle-Update vor der Neuerkennung**, damit eine Zone sich nicht selbst berührt.

### 6.5 Displacement – eine Definition für alle Module

`Displacement(a..b)` umfasst 1–3 aufeinanderfolgende Bars in einer Richtung und ist erfüllt, wenn gilt:

| Bedingung | Regel |
|---|---|
| D1 | Σ Body ≥ `kD`·ATR14 (1 Bar) bzw. ≥ 1,5·`kD`·ATR14 (2–3 Bars). **ATR gemessen an Bar a−1**, also vor dem Impuls; sonst hebt der Impuls seine eigene Schwelle an (→ K4 §6). |
| D2 | jede Kerze Body/Range ≥ 0,5, Mittelwert ≥ 0,6 |
| D3 | Close[b] jenseits des Referenzlevels (gebrochener Swing bzw. OB-Extrem) |
| D4 (Flag „strong“) | mindestens ein FVG im Leg |

- **[D] `kD` = 1,2**, optimierbar im Bereich 0,8–1,6.
- Vergleichswerte aus den Quellen:
  - K1: 1,0·ATR, Body ≥ 0,6
  - K2: TF-gestaffelt 1,0–1,5
  - MrOwl1011: 2,0·ATR hat das Ergebnis verbessert (→ K4 §4)

### 6.6 BiasEngine (→ K1 §6, K3 §2)

**Votes:**

| Vote | Werte | Definition |
|---|---|---|
| V_D1 | +1 / −1 / 0 | EXT-Trend auf D1 |
| V_H4 | +1 / −1 / 0 | EXT-Trend auf H4 |
| V_DC | +1 / −1 / 0 | Tageskerzen-Regel (Tabelle unten). Gilt, bis ihr Ziel erreicht ist, danach 0 |

**Tageskerzen-Regel** (D−1 = letzter geschlossener NY-Close-Tag, D−2 = davor):

| Bedingung | V_DC |
|---|---|
| Close(D−1) > High(D−2) | +1, Ziel High(D−1) |
| Close(D−1) < Low(D−2) | −1, Ziel Low(D−1) |
| High-Sweep (Hoch über High(D−2), Close zurück) | −1 |
| Low-Sweep (Tief unter Low(D−2), Close zurück) | +1 |
| Outside Day mit Close innen, Inside Day | 0 |

**Bias-Bestimmung:**
- **[D] `BiasMode = SIMPLE`:** LONG, wenn V_H4 = +1 ∧ V_D1 ≥ 0 ∧ V_DC ≥ 0. SHORT gespiegelt. Sonst NEUTRAL, dann keine Trades.
  - Begründung: Der Trendfilter war in der besten gefundenen Evidenz der dominante Faktor (→ K4 §4). Wenige Freiheitsgrade.
- **Variante `BiasMode = SCORE`:** Score aus 7 Votes, Gewichte fix (→ K3 §2.2).

**Filter:**
- **Dealing Range H4** = `[trailBot, trailTop]` des EXT-Layers. Long-Entries nur bei Position < 0,5 (Discount), Short-Entries nur > 0,5 (Premium).
- **DOL-Gate:** Ein ACTIVE-Pool in Bias-Richtung mit Abstand ≥ 1·ATR(H1) muss existieren.

**Neuberechnung:** um 17:00 NY und bei jedem H4-Close.

### 6.7 Kontext-Features (für Logging und Analyse)

- ADR20 (NY-Tage), ATR14 je TF, Spread-Median je Stunde (rollierend 20 Tage)
- Session- und Killzone-Flag, Macro-Flag, Lage zum Midnight Open
- Wochentag, Abstand zur nächsten News
- DST-Abweichungswoche ja/nein, `TRANSITION`-Flag, Dealing-Range-Position

---

## 7. Handelsmodelle (v1-Umfang)

Alle Regeln sind für Long beschrieben; Short ist gespiegelt.

### 7.1 Modell A – „Sweep → MSS → FVG“ (ICT-2022-Kern)

> **Ergebnis der Ereignisstudie P2 (24.10.2026):** Der Trigger Sweep → MSS zeigt gegenüber Placebo keinen Effekt (Δ −0,01 R, n = 23.855). Sweeps in den Killzones sind nicht besser als außerhalb. **Modell A ist deshalb zurückgestellt** (→ `03_Ergebnisse_P2_Ereignisstudie.md`).

Eine Codebasis mit Presets (→ K3 §4a, §4b, §4h, §8):

| Preset | Entry-Fenster (NY) | Sweep-Pools für Long (SSL) | Besonderheit |
|---|---|---|---|
| **A-LDN** | 02:00–05:00 | Asia-Low (20–00), Pre-London-Low (00–02), PDL, M15-EQL, M15-Swing-Low | **Judas-Regel:** Wurde das Asia-High vorher per BROKEN akzeptiert, kein Long. Asia-Range ≤ 0,4·ADR20. |
| **A-NY** | 07:00–10:00 | London-Low (02–07), Asia-Low, PDL, M15-EQL | |
| **A-SB** | 03–04 / 10–11 | wie oben | Sweep ab 30 min vor Fensterbeginn; das FVG (c3) muss im Fenster schließen; Fill nur im Fenster |
| A-ASIA (optional, **v1 aus**) | 20:00–23:00 | NY-Session-Low (07–17), PDL, M15-EQL, M15-Swing-Low | nur JPY-, AUD- und NZD-Gruppen (Abschnitt 11.2); erst nach eigener Ereignisstudie |

**Ablauf:**

1. **Gates:**
   - Bias = LONG, Fenster aktiv
   - Tageslimits ok; keine aktive News-Sperre (nur relevant bei `NewsMode = AVOID`)
   - keine offene Position oder Pending-Order auf dem Symbol
   - Symbol für das Preset freigeschaltet (Session-Maske, Abschnitt 11)
2. **Sweep:** Ein SSL-Pool aus der Preset-Liste ist auf dem Trigger-TF des Symbols SWEPT; das ist M5, bei Tier 3 M15 (Abschnitt 11.2). Die Sweep-Bar liegt in `[Fensterstart − 30 min, jetzt]`. Ist die Sweep-Tiefe größer als 0,5·ATR(D1), gilt das als Trendtag und es gibt kein Setup (fix, → K7 §10.1).
3. **MSS:** gemäß 6.2 (Body-Close über das Referenz-STH innerhalb `W_mss`, Displacement, FVG im Leg).
4. **FVG-Wahl:** das jüngste bullische FVG im Leg (Sweep-Bar bis MSS-Bar) mit Größe ≥ minFVG, dessen CE ≤ Leg-Mitte liegt (Discount des Legs). Gibt es keins, das jüngste FVG mit Flag `notDiscount`.
5. **Entry:** Buy Limit bei `CE + spreadEst` [D `EntryMode = CE`, alternativ `NEAR_EDGE`]. Der Spread-Aufschlag ist nötig, weil Kerzen Bid zeigen, das Limit aber auf dem Ask füllt.
6. **SL:** `sweepExtreme − buf` mit `buf = max(2·spreadEst, 0,1·ATR14(M15))`. Bei Short zusätzlich `+ spreadEst`, weil der SL auf dem Ask triggert.
7. **TP:**
   - erster ACTIVE BSL-Pool oberhalb des Entry mit RR ≥ `RRmin` [D 2,0]
   - liegt dieser jenseits `RRcap` = 4, gilt TP = 4 R
   - gibt es keinen Pool, gilt TP = `RRmin`
8. **Kosten-Gate:** `costR ≤ 0,10` (Abschnitt 10), sonst Setup verwerfen und mit Grund loggen.
9. **Order:** Buy Limit mit Ablauf zum Fensterende.
   - **Cancel vor Fill:** Close auf dem Trigger-TF < Sweep-Extrem, TP vor Fill erreicht, Fensterende, Bias-Wechsel, bei `NewsMode = AVOID` auch der Beginn einer News-Sperre.
10. **Limits:** 1 Trade pro Fenster und Symbol, höchstens 2 pro Symbol und NY-Tag.

### 7.2 Modell C – „HTF-POI → LTF-Bestätigung“ (Trend-Fortsetzung)

Angelehnt an MrOwl1011 (H1-OB → M5-CISD mit Trend-Gate), die beste gefundene Evidenz (→ K4 §4), und an das klassische SMC-Modell (→ K3 §4g). **Im FTMO-Modus ist C das Primärmodell:** weitere Stops, weniger Margin- und Kostendruck (→ FTMO-Plan §5).

1. **Gates:** Bias = LONG, Fenster London KZ ∪ NY AM KZ [D].
2. **POI:**
   - ACTIVE bullischer H1-Order-Block (6.4)
   - Displacement mit `kD_POI` [D 1,5] und FVG im Leg
   - im Discount der H4-Dealing-Range
   - Touches ≤ 1
3. **Touch:** M5-Low ≤ POI proximal.
4. **Bestätigung** innerhalb `W_conf` = 24 M5-Bars, solange kein Close unter POI distal fällt:
   - **CISD** = Close über dem Open der ersten Kerze der letzten ununterbrochenen Down-Close-Serie ins Touch-Tief
   - Variante: M5-CHoCH (Close über das letzte STH)
5. **Entry:** [D] Market zum Open der Folgebar. Variante: Limit am CE des LTF-FVG.
6. **SL:** `min(POI.stopRef, Touch-Tief) − buf`.
7. **TP:** erster ACTIVE BSL-Pool (H1-Swing-High, PDH, EQH) mit RR ≥ `RRmin`, Deckel 4 R.
8. **Invalidierung:** H1-Close < POI distal macht den POI INVALIDATED.

### 7.3 Richtungs-Hypothese offen halten

ICT lehrt **Umkehr** nach einem Sweep. Osler (Stop-Kaskaden) und das SSRN-Preprint sprechen eher für **Fortsetzung** (→ K5 §1.1, K4 §4).

Die Ereignisstudie (16, Phase P2) testet deshalb beide Richtungen:
- Umkehr nach SWEPT, das ist die Grundlage von Modell A
- Fortsetzung nach BROKEN mit FVG-Retest, das ist die Familie von Modell C
- dazu Spiegeltests

Kein Modell geht live, dessen Richtungs-Hypothese die Ereignisstudie nicht stützt.

### 7.4 Bewusst nicht im v1-Umfang (Research-Backlog)

| Konzept | Grund | Möglicher Einsatz |
|---|---|---|
| Unicorn (Breaker ∩ FVG) | selten, Breaker-Definition widersprüchlich | Qualitäts-Flag in A |
| OTE 62–79 % | Entry-Ort, kein eigenes Setup | Entry-Variante |
| Turtle Soup (Raschke D1) | klassisch definiert | **Vergleichsbaseline** |
| MMXM | Phasen kaum robust erkennbar | – |
| Weekly Profiles | nur ex post klassifizierbar | Risiko-Filter |
| SMT-Divergenz | viele Fehlsignale | Filter/Feature; Paare in Abschnitt 11 |
| CBDR / SD-Projektionen | Konvention, keine Messung | Zielvariante |
| Macros | keine Statistik | Feature |
| Fix-Effekte (WM/R 16:00 London, Tokio-Fix) | **evidenzbasiert** (Krohn et al. 2024, → K5 §1.4) | eigener Research-Strang |

---

## 8. Trade-Management

- **Baseline** (für saubere Auswertung):
  - feste SL und TP, keine Partials, kein Trailing
  - Zeit-Exits: A-LDN um 12:00 NY, A-NY um 16:00 NY. Modell C im FTMO-Modus: Zeit-Stopp nach 3 FTMO-Tagen (Swing-Halten, → FTMO-Plan §5); sonst 16:00 NY.
  - Kein Zwangs-Close vor dem Wochenende (Swing-Konto, Parameter `CloseBeforeWeekend` [D false]). Das Wochenend-Risiko steuert die Gap-Reserve im FtmoGuard.
- **Varianten**, einzeln getestet; jede zählt als Trial im Log:
  - Breakeven bei +1 R (SL auf Entry ± Kostenpuffer)
  - 50 % Partial am ersten IRL ≥ 1 R
  - Trailing hinter M15-Swing-Lows nach TP1
  - Ziel an Session-Extremen
- **Ausführung des Managements:** nur bei Bar-Close (M5), nicht pro Tick. SL und TP liegen serverseitig.

---

## 9. Risiko & Exposure (→ K5 §6, K6 §4, §10)

**Positionsgröße**
- **Risiko pro Trade:** [D] 0,5 % Equity; 0,25 % für den Live-Start.
  - **FTMO-Modus:** Risikoleiter vom Anfangskapital: 1,0 % (Challenge), 0,75 % (Verification), 0,5 % (FTMO Account). Ab 3 % Drawdown halbiert, ab 6 % geviertelt; hergeleitet per Monte-Carlo (→ FTMO-Plan §2–3).
  - Zusätzlich gilt ein **Margin-Budget** von ≤ 80 % der Equity. FTMO-Swing-Hebel: FX 1:30, XAUUSD 1:15.
- **Lots:**
  - `OrderCalcProfit` mit Referenzvolumen `VOLUME_MAX`
  - Gegenprobe über `TICK_VALUE_LOSS`; Warnung bei mehr als 5 % Abweichung
  - **abrunden**; unter `VOLUME_MIN` den Trade auslassen
  - Margin-Prüfung per `OrderCheck`
  - Kommission über `SymbolInfoCommissions` (ab Build 6060), sonst per Input
- **Nach dem Fill:** Ist das reale Risiko größer als 110 % des geplanten, wird der Überschuss teilweise geschlossen.

**Exposure-Vektor** über USD, EUR, GBP, JPY, AUD, NZD, CAD, CHF und XAU:
- Long auf Base/Quote mit Risiko r → `+r` auf Base, `−r` auf Quote.
- Pending-Orders zählen wie gefüllt.
- XAU wird explizit gemappt (CFD-Gold hat teils USD als Base-Währung).

| Limit | Default [D] |
|---|---|
| \|Netto-Risiko je Währung\| | ≤ 1,5 × Risiko pro Trade |
| Trades je Währung | ≤ 2 |
| Offenes Gesamtrisiko | ≤ 4 × Risiko pro Trade |
| Positionen + Pendings | ≤ 6 |
| JPY-Cluster (alle xxxJPY) | ≤ 2 |
| Cluster A und B (\|ρ\| ≥ 0,8, Abschnitt 11.3) | höchstens 1 Position je Richtung |
| Positionen je Symbol | 1 (keine Gegenpositionen) |
| Tagesstopp (NY-Tag) | −2 R realisiert oder 2 Verluste (ICT-Zwei-Trade-Regel) |
| Wochenstopp | −5 R |
| Equity-Guard | DD vom Hoch > 10 % → Pause und Alarm |
| FTMO-Modus (FtmoGuard) | Grenze = max(Balance 00:00 Prag − 5.000; 90.000). Keine neuen Entries ab Grenze + 2.000, alles schließen ab Grenze + 1.000, Prüfung vor jedem Trade inkl. offener Positionen, Zielsicherung, Handelstage-Zähler (→ FTMO-Plan §4) |

**Kill-Switch** (Betrieb): Live-DD > 99. Perzentil des Monte-Carlo-DD, **oder** Live-Expectancy nach mindestens 100 Trades unter der unteren Konfidenzgrenze.

---

## 10. Filter

| Filter | Regel [D] |
|---|---|
| **Kosten-Gate** | `costR = (spreadEst + slipEst) / abs(Entry − SL) + KommissionRT / VerlustProLot ≤ 0,10` |
| Spread | aktueller Spread ≤ 2 × Median der Stunde **und** ≤ Symbol-Cap (Abschnitt 11) |
| Rollover | 16:45–18:15 NY keine neuen Orders und keine SL-Änderungen; XAUUSD: Pendings vor 16:45 löschen |
| Wochenende | Positionen dürfen übers Wochenende offen bleiben (Swing, `CloseBeforeWeekend = false`). Freitag Neueröffnungen bis 15:00 NY (danach dünne Liquidität), Pendings um 16:00 NY löschen. Wochenend-Risikoprüfung mit Gap-Reserve im FtmoGuard (→ FTMO-Plan §4.12) |
| News | [D] `NewsMode = ALLOW`: keine Sperre (Swing-2-Step erlaubt News-Trading), aber 50 % Slippage-Reserve für Positionen über Tier-1-Events (→ FTMO-Plan §4.13). Testvariante `AVOID`: keine neuen Entries von −30 bis +30 min (Notenbanken −30 bis +60 min), Pendings −15 min löschen, Tier-1-USD-Events sperren den USD-Cluster. Kalender im Tester per CSV-Export, DST-korrigiert (→ K6 §6) |
| Monatsende-Fix | letzter Geschäftstag des Monats 10:45–11:15 NY keine Entries (WM/R-Fix 16:00 London, → K7 §3.3) |
| Wochenstart | erste Stunde nach der Wiedereröffnung keine Entries; keine Levels aus dieser Stunde |
| ADR-Erschöpfung | kein neuer Trade, wenn die Tagesrange ≥ 1,0·ADR20 ist **und** das Ziel außerhalb der bisherigen Tagesrange liegt (fix vorregistriert, nicht optimiert) |
| JPY-Intervention | siehe 11.4 |
| Request-Budget | ≤ 500 Trade-Requests pro Tag (FTMO: > 2.000 = hyperaktiv) |
| Daten | `SERIES_SYNCHRONIZED`, genug Bars, Tick ≤ 60 s alt, Zeitmodell validiert |
| Rechte | `TERMINAL_TRADE_ALLOWED`, `MQL_TRADE_ALLOWED`, `ACCOUNT_TRADE_EXPERT`, `SYMBOL_TRADE_MODE` |

**`spreadEst`** = max(aktueller Spread, Median des Stundenprofils). Der Bar-Spread aus `MqlRates` ist der **Minimal**-Spread und unterschätzt die Kosten (→ K6 §2.1).

---

## 11. Instrument-Konfiguration (→ K7)

### 11.1 Grundregeln

- **Einheiten:** Intern wird nur in Preis- und ATR-Einheiten gerechnet. „Pip“ dient nur dem Logging; bei Gold ist er nicht einmal standardisiert (0,01, 0,10 oder 1,00 USD).
- **Symbol-Mapping in `OnInit`:**
  - Suffixe auflösen (z. B. `EURUSD.r`), ebenso `GOLD` ↔ `XAUUSD`.
  - Kontraktdaten aus `SymbolInfo` lesen. Gold hat je nach Broker 1, 10 oder 100 oz.
- **Kosten selbst messen:** Der EA protokolliert ab Tag 1 pro Symbol und Wochenstunde Spread, Slippage und ATR. Das Tiering wird quartalsweise per Walk-Forward überprüft.
- **Spread-Caps:**
  - dynamisch: ≤ 2 × Median derselben Wochenstunde über 20 Handelstage
  - statischer Not-Cap: ≈ 3 × typischer Raw-Spread, z. B. EURUSD 0,6 Pips, GBPJPY 2,5 Pips, XAUUSD 0,30 USD (→ K7 §10.2)
- **Liquidität:** Sie liegt in den sechs USD-Majors (BIS 2025: jeder ≥ 4,9 % des Weltumsatzes). Die 18 Crosses sind dünne, weitgehend synthetische Märkte. Struktur und SMT liest man deshalb bevorzugt auf den USD-Legs.

### 11.2 Tiering, Trigger-TF und Fenster [D]

Die Kostenklasse bezieht sich auf die All-in-Kosten in Prozent eines Stops von 1×ATR(M5) (→ K7 §9.3).

| Symbol | Tier | Kostenklasse | Trigger-TF | Fenster (Presets) | Cluster | SMT-Partner | Hinweise |
|---|---|---|---|---|---|---|---|
| EURUSD | 1 | A (13 %) | M5 | LDN, NY | A | GBPUSD, USDCHF⁻¹, DXY′ | ECB-Fix 14:15 CET |
| GBPUSD | 1 | A (12 %) | M5 | LDN, NY | A | EURUSD | UK-Daten 02:00 NY (in der London-KZ) |
| USDJPY | 1 | A (12 %) | M5 | LDN, NY, (ASIA) | D | DXY′ | Interventionsmodus (11.4); Gotobi/Tokio-Fix |
| EURJPY | 1 | A (13 %) | M5 | LDN, NY, (ASIA) | D | GBPJPY | volumenstärkster JPY-Cross |
| GBPJPY | 1 | A (14 %) | M5 | LDN, NY, (ASIA) | D | EURJPY | höchste FX-ADR; extremer Rollover-Spread |
| XAUUSD | 1 | A (≈ 2–12 %) | M5 | LDN, NY, SB | G (USD) | DXY′ (schwach) | Regime-, Pause- und Gap-Regeln (11.4) |
| AUDUSD | 2 | B (17 %) | M5 | LDN, NY, (ASIA) | B | NZDUSD | |
| USDCAD | 2 | B (20 %) | M5 | NY, LDN | F | – | BoC 09:45 NY, Öl |
| USDCHF | 2 | B (15 %) | M5 | LDN, NY | A, E | EURUSD⁻¹ | |
| AUDJPY | 2 | B (20 %) | M5 | LDN, (ASIA) | B, D | NZDJPY | |
| CADJPY | 2 | B (20 %) | M5 | LDN, NY | D, F | – | |
| CHFJPY | 2 | B (19 %) | M5 | LDN | D, E | – | |
| EURAUD | 2 | B (18 %) | M5 | LDN | B | EURNZD | |
| GBPAUD | 2 | B (18 %) | M5 | LDN | B | GBPNZD | |
| EURCAD | 2 | B (23 %) | M5 | LDN, NY | F | – | |
| NZDUSD | 2 | B (24 %) | M5 | LDN, NY, (ASIA) | B | AUDUSD | vor allem SMT-Referenz |
| GBPCAD | 3 | B (23 %), Mean-Reversion-Tendenz | M15 | NY, LDN | F | – | |
| EURNZD | 3 | B (24 %) | M15 | LDN | B | EURAUD | dünn |
| NZDJPY | 3 | B (24 %) | M15 | LDN, (ASIA) | B, D | AUDJPY | dünn |
| GBPNZD | 3 | C (26 %) | M15 | LDN | B | GBPAUD | breitester Raw-Spread |
| GBPCHF | 3 | C (27 %) | M15 | LDN | E | – | |
| EURCHF | 3 | C (30 %) | M15 | LDN | E | – | SNB-Risiko, niedrige ADR |
| CADCHF | 3 | C (32 %) | M15 | NY, LDN | E, F | – | niedrigste ADR |
| AUDCAD | 3 | C (35 %) | M15 | LDN, (ASIA) | B, F | – | |
| AUDNZD | **aus** | C (47 %) | (H1) | – | B | – | Kosten bei M15 noch ≈ 27 % → **Default deaktiviert** |

**Legende**
- **Fenster:** LDN = A-LDN 02:00–05:00, NY = A-NY 07:00–10:00, SB = Silver Bullet. **(ASIA)** = optionales Preset A-ASIA 20:00–23:00 NY: im v1 aus und erst nach eigener Ereignisstudie freischalten. JPY-, AUD- und NZD-Paare machen 55–65 % ihrer Tagesrange in Asia (→ K7 §3.1).
- **Trigger-TF M15** heißt: Modell A läuft für dieses Symbol mit M15 als Trigger- und H1 als POI-TF. Die Engines sind TF-agnostisch.
- **Unabhängig vom Tier gilt das Kosten-Gate** (≤ 0,10 R) für jeden einzelnen Trade.

### 11.3 Cluster (für Exposure-Regeln und Event-Sperren)

| Cluster | Mitglieder | Kopplung (→ K7 §4) | Regel [D] |
|---|---|---|---|
| A „EUR/GBP vs USD“ | EURUSD, GBPUSD, USDCHF (invers) | ρ ≈ +0,9 bzw. −0,9 | höchstens 1 Position je Richtung |
| B „Antipoden“ | AUDUSD, NZDUSD, AUDJPY, NZDJPY, EURAUD, EURNZD, GBPAUD, GBPNZD, AUDCAD | ρ(AUDUSD, NZDUSD) ≈ +0,92 | höchstens 1 Position je Richtung |
| C „USD gesamt“ | 7 Majors + XAUUSD | USD-Event trifft 8 Symbole | über den Währungsvektor (9); bei Tier-1-USD-News höhere Slippage-Reserve für alle Positionen des Clusters (Sperre nur bei `NewsMode = AVOID`) |
| D „JPY-Block“ | USDJPY + 6 JPY-Crosses | ρ(EURJPY, GBPJPY) ≈ +0,95 | höchstens 2 Positionen; Interventionsmodus |
| E „CHF-Block“ | USDCHF, EURCHF, GBPCHF, CADCHF, CHFJPY | SNB-Risiko gebündelt | SNB-Termine: höhere Slippage-Reserve (Sperre nur bei `AVOID`) |
| F „CAD/Öl“ | USDCAD, EURCAD, GBPCAD, AUDCAD, CADJPY, CADCHF | BoC, Öl | BoC-Termine: höhere Slippage-Reserve (Sperre nur bei `AVOID`) |
| G „Gold“ | XAUUSD | eigener Faktor, zählt aber zum USD-Bein | – |

**SMT (Research und Filter, nicht im v1):**
- EURUSD/GBPUSD ist mathematisch eine Bewegung in EURGBP; AUDUSD/NZDUSD analog eine Bewegung in AUDNZD.
- Synthetischer Dollar-Index: `DXY′ = EURUSD^−0,618 · USDJPY^0,136 · GBPUSD^−0,119 · USDCAD^0,091 · USDCHF^0,036`. Das ist die ICE-Formel, USDSEK wird über ein konstantes EURSEK absorbiert (→ K7 §5).
- DXY′ wird aus synchronisierten M1-Closes gebildet, nicht aus Produkten von Highs und Lows.

### 11.4 Sonderregeln

- **JPY-Interventionsmodus:** Er greift ab USDJPY ≥ 158 [Parameter] oder bei manuellem Flag. Dann sind keine neuen Longs in USDJPY/xxxJPY erlaubt (also keine JPY-Shorts), und die Positionsgröße der JPY-Paare wird halbiert. Hintergrund: MoF-Interventionen bei ≈ 152 / 160 / 164 in den Jahren 2022–2026, im Juli 2026 erstmals gemeinsam mit dem US-Treasury.
- **XAUUSD:**
  - **Volatilität:** Die ADR hat sich binnen eines Jahres mehr als verdoppelt (2025 ≈ 60 USD, 2026 YTD ≈ 132 USD). Deshalb strikt ATR-basiert rechnen.
  - **Tagespause** 17:00–18:00 NY: Pendings vor 16:45 löschen; in der ersten Stunde nach der Wiedereröffnung keine Levels und keine Entries.
  - **Wochenend-Gaps** bis 153 USD (2024–2026): Halten übers Wochenende ist erlaubt (Swing). Die Gap-Reserve im FtmoGuard begrenzt das Risiko; bei Gold ist sie wegen der großen Gaps entsprechend hoch (→ FTMO-Plan §4.12).
  - **Triple-Swap** aus `SYMBOL_SWAP_ROLLOVER3DAYS` lesen.
- **CHF:** Tail-Risiko, siehe den SNB-Schock 2015 mit ≈ +30 % intraday. Der Cluster ist deshalb auf 1 Position je Richtung begrenzt, SNB-Termine bekommen eine erhöhte Slippage-Reserve.
- **GBP:** Flash-Crash-Historie (2016, frühe Asia-Stunden). Die Asia-Preset-Freigabe für GBP-Paare nur mit kleinem Risiko.

---

## 12. Ausführung (→ K6 §5)

**Pending-Orders**
- `ORDER_FILLING_RETURN`; Preis auf die Tick-Größe normalisiert.
- Stops-Level ab Open-Preis prüfen, mit Puffer max(Stops-Level, Spread).
- Ablauf mit `ORDER_TIME_SPECIFIED`, wenn das Symbol es erlaubt, sonst Löschen durch den EA.
- Bei `SYMBOL_ORDERS_DAILY` SL/TP nach dem Rollover prüfen.

**Market-Orders**
- Filling FOK → IOC → RETURN entsprechend der Symbol-Maske; Fallback bei `INVALID_FILL`.
- Bis zu 3 Retries bei REQUOTE, PRICE_CHANGED, PRICE_OFF, TOO_MANY_REQUESTS und LOCKED.
- Bei TIMEOUT oder CONNECTION **erst abgleichen** (Magic + Tag), dann gegebenenfalls neu senden.

**Zuordnung**
- Magic = `770000 + Modell·1000 + Preset·100 + SymbolIndex`.
- Kommentar ≤ 25 Zeichen; Positionen über Magic und `POSITION_IDENTIFIER` zuordnen.

**Abgleich**
- `OnTradeTransaction` für schnelle Reaktion.
- Maßgeblich ist der periodische Server-Abgleich (Positionen, Orders, History).

**Netting-Konten:** unterstützt, weil ohnehin nur eine Position pro Symbol erlaubt ist. FIFO beachten.

**FTMO-Spezifika** (→ FTMO-Plan §4.10, 4.15, 4.16):
- **Volume Bands:** Der Spread steigt mit der Ordergröße. Deshalb `maxLotsPerOrder` je Symbol [D: FX 15] und ein bandabhängiger Spread im Kosten-Gate.
- **Kommission:** 5 USD Round Turn pro FX-Lot; Metalle 0,0014 % vom Nominal.
- **0,7 %-Abschlag** auf realisierte Ergebnisse von Symbolen mit Nicht-USD-Profit-Währung.
- **Request-Zähler** mit harter Obergrenze.

---

## 13. Zustand & Robustheit (→ K6 §7)

- **Start:**
  - Zonen und Pools werden deterministisch aus der History rekonstruiert (Replay von maxAge + 300 Bars je TF).
  - Eigene Positionen und Orders einlesen.
  - Trade-Pläne aus einer Datei laden, Schlüssel `POSITION_IDENTIFIER`, atomar geschrieben (`.tmp` → `FileMove`).
- **Tagesergebnis** aus der Deal-History des NY-Tages.
- **Absturzsicherheit:** Bounds- und Pointer-Checks überall. Ein Critical Error beendet den EA für alle 25 Symbole.
- **Laufzeit:** Zyklusbudget < 50 ms, gemessen mit `GetMicrosecondCount`.
- **History-Änderung:** Hash der letzten N Bars periodisch vergleichen; bei Abweichung den SymbolContext neu aufbauen.

---

## 14. Logging & Research-Export

| Datei | Inhalt |
|---|---|
| `events_<sym>.csv` | Serverzeit, NY-Zeit, TF, Typ, Richtung, Preise, Referenz-ID, ATR, Spread, Session, Bias, Feature-Flags |
| `setups.csv` | **jeder** Setup-Kandidat, auch abgelehnte, mit Ablehnungsgrund. So lässt sich die Wirkung jedes Filters messen |
| `trades.csv` | Setup-ID, Entry/SL/TP geplant vs. Fill, Lots, Risiko, Kosten, Ergebnis in R, MFE/MAE in R, Dauer, Exit-Grund |

- In der Optimierung ist das Logging per Makro aus.
- Statistiken je Symbol laufen über Frames (`FrameAdd`/`OnTesterPass`).

---

## 15. Parameterpolitik

**Optimierbar (höchstens 5 je Modell):**

| Parameter | Bereich | Default |
|---|---|---|
| `kD` (Displacement) | 0,8–1,6 | 1,2 |
| `RRmin` | 1,5–3,0 | 2,0 |
| `kFVG` | 0,10–0,40 | 0,20 |
| `W_mss` | 10–30 Bars | 20 |
| `EntryMode` | CE / NEAR_EDGE | CE |

**Per Konvention fixiert:**
- L_int = 5, L_ext gemäß TF-Tabelle (5)
- ATR 14/200, `tolEQ` = 0,1·ATR200
- `nReclaim` = 3, `nAccept` = 2
- Fensterzeiten, Puffer, Risikolimits

**Trial-Log ist Pflicht.** Jeder getestete Parameter- oder Variantensatz zählt als Versuch und geht in die Deflated Sharpe Ratio ein (→ K5 §5.1). Bei 5 Jahren Daten sind höchstens etwa 45 unabhängige Konfigurationen vertretbar.

---

## 16. Validierungsplan mit Gates (→ K5 §5, §8)

| Phase | Inhalt | Gate (Go/No-Go) |
|---|---|---|
| **P0 Daten** | Tickdaten 2015–2026 aller 25 Symbole (z. B. Dukascopy als Custom Symbols) plus Broker-Real-Ticks der letzten Monate zur Kalibrierung. Kommission im Tester. Zeitmodell validieren | Anteil echter Ticks per Journal belegt; Zeitmodell-Test bestanden |
| **P1 Korrektheit** | Unit-Tests (Script-Fixtures); History-Invarianz (Historie an mehreren Stellen abschneiden); Replay-Rewrite-Zähler = 0; Batch = bar-by-bar; Parität der Strukturereignisse mit dem LuxAlgo-MQL5-Port bzw. PineTS (→ K4 §1); Python-Golden-Master | 0 Lookahead-Befunde |
| **P2 Ereignisstudien** | Jeder Baustein (Sweep, MSS, FVG-Touch, OB-Touch, BOS) gegen **Placebo-Events**: gleiche Session, gleiches Volatilitätsdezil, gleiche SL/TP-Geometrie. Forward-Returns in ATR, Block-Bootstrap, Holm- oder BH-Korrektur, Umkehr **und** Fortsetzung | ≥ 1 Baustein signifikant nach Korrektur, sonst neu fassen |
| **P3 Entwicklung** | Modelle auf einem Entwicklungsset von 6–8 Paaren, das jede Währung enthält; In-Sample 2015–2020; Walk-Forward 2021–2023 (24 Monate IS / 6 Monate OOS, rollierend) | Walk-Forward-Effizienz ≥ 0,5 |
| **P4 Robustheit** | unverändert auf die übrigen Paare anwenden (XAUUSD separat); Monte-Carlo-Block-Bootstrap; Kosten ×1,5 und ×2; Parameter ±20 %; Entry +1 Bar; Top-5-%-Trades entfernen; Session-Fenster ±1–2 h verschieben | Akzeptanztabelle unten |
| **P5 Hold-out** | 2024–2026, genau **einmal** anfassen | Kriterien erfüllt, sonst verwerfen statt nachoptimieren |
| **P6 Inkubation** | **FTMO Free Trial** (kostenlos, 14 Tage, beliebig oft) auf den FTMO-Servern, 2–4 Durchläufe, ergänzt um Demo. Dazu Bootstrap-Bestehenschance mit den echten OOS-Trades (→ FTMO-Plan §6) | Live-Expectancy im 95-%-Konfidenzintervall der OOS-Ergebnisse; FTMO-Kostenannahmen bestätigt; P(beide Phasen) ≥ 70 % |

**Akzeptanzkriterien** (Out-of-Sample, Heuristiken aus → K5 §8):

| Kriterium | Schwelle |
|---|---|
| Trades | ≥ 500 gesamt, ≥ 30 je Instrument |
| t-Wert der R-Expectancy | ≥ 3 |
| Deflated Sharpe Ratio | ≥ 0,95 bei ehrlicher Versuchszahl |
| Probability of Backtest Overfitting (PBO) | ≤ 0,2 |
| Netto-Profit-Factor | ≥ 1,2 |
| Erwartungswert | ≥ +0,1 R |
| Profit-Factor bei doppelten Kosten | ≥ 1,05 |
| Anteil Instrumente mit PF > 1 | ≥ 70 % |
| Anteil Jahre mit PF > 1 | ≥ 70 % |
| Gewinnanteil eines einzelnen Instruments oder Jahres | ≤ 25–30 % |
| Parameter ±20 % | PF bleibt ≥ 1,1 |
| Monte-Carlo-DD, 95. Perzentil | ≤ Risikobudget (privat z. B. 20 %, Prop ≤ 6 %) |
| Session-Fenster verschoben | Edge schrumpft messbar, sofern Zeit Teil der These ist |

**Realistische Erwartung** (→ K5 §7): Nach Kosten bestenfalls PF 1,1–1,4 bzw. +0,05 bis +0,2 R pro Trade. Trefferquoten über 60 % bei RR über 2 deuten auf einen Fehler hin (Lookahead oder Overfitting).

---

## 17. Projektstruktur & Roadmap

```
smcea/
  docs/                      Research, Zusammenfassung, Blueprint
  mql5/
    Experts/SMC_Portfolio.mq5
    Include/SMC/
      Core/     Types.mqh, SymbolContext.mqh, BarClock.mqh, SessionClock.mqh, Ring.mqh,
                Logger.mqh, EventExporter.mqh, StateStore.mqh, IMarketData.mqh
      Engines/  ATR.mqh, SwingEngine.mqh, StructureEngine.mqh, LiquidityEngine.mqh,
                PDArrayEngine.mqh, Displacement.mqh, BiasEngine.mqh
      Models/   IModel.mqh, ModelA_SweepMSSFVG.mqh, ModelC_HTFPOI.mqh
      Risk/     RiskManager.mqh, ExposureManager.mqh, CostGate.mqh, FtmoGuard.mqh, MarginBudget.mqh
      Exec/     TradeExecutor.mqh, PositionManager.mqh
      Filters/  SpreadFilter.mqh, NewsFilter.mqh, SessionFilter.mqh
      Viz/      Draw.mqh (nur visueller Modus)
    Scripts/   ExportBars.mq5, ExportCalendar.mq5, Tests/*.mq5
  research/                  Python: Referenz-Engine, Ereignisstudien, WFA, Monte Carlo, Reports
  data/                      (nicht versioniert) Tick- und Bar-Daten, Kalender-CSV
```

| Meilenstein | Inhalt | Ergebnis |
|---|---|---|
| M0 | Entscheidungen (Abschnitt 18), Broker-Check, Datenbeschaffung | Rahmen fixiert |
| M1 | Core: SymbolContext, BarClock, SessionClock inkl. Validierung, ATR, Logger, EventExporter | lauffähiger Daten- und Zeit-Unterbau |
| M2 | Engines Swing, Structure, Liquidity, PD-Arrays, Bias plus Tests und Golden Master | kausale Feature-Engine (P1) |
| M3 | Ereignisstudien in Python | **Go/No-Go (P2)** |
| M4 | Modelle A und C, Risk, Exposure, Executor, PositionManager | handelsfähiger EA |
| M5 | Walk-Forward, Robustheit, Hold-out | **Go/No-Go (P3–P5)** |
| M6 | Inkubation | Live-Entscheidung (P6) |

---

## 18. Offene Entscheidungen

**Entschieden (24.10.2026):** FTMO 2-Step, Swing-Konto, 100.000 USD, MT5. Max Loss 10 %, Max Daily Loss 5 %, Ziele 10 % und 5 %. **News- und Wochenendhandel sind erlaubt** (vom User bestätigt): Der EA sperrt deshalb nichts, er rechnet nur Gap- und Slippage-Reserven in den Tagesverlust-Schutz ein. Daraus folgen:
- **Zeitmodell:** NY-Close GMT+2/+3 (bestätigt).
- **Kosten:** FTMO-Kommission und 0,7 %-Abschlag.
- **Risikoleiter:** 1 % / 0,75 % / 0,5 % als Vorschlag.
- **Modell C** wird Primärmodell (→ `02_FTMO_Challenge_Plan.md`).

**Noch offen:**
1. **Am FTMO-Konto (Free Trial) prüfen:** Hedging oder Netting, Symbolnamen, Volume Bands, Swap-Tage, Daily-Loss-Reset; Support-Fragen in FTMO-Plan §7.
2. **Risikoleiter bestätigen:** 1 % / 0,75 % (≈ 80 % Bestehenschance in ≈ 5 Monaten bei E = +0,1 R) oder vorsichtiger 1 % / 0,5 % bzw. 0,75 % / 0,5 % (höhere Chance, längere Dauer)?
3. **Stil:** Durch FTMO-Kosten und -Margin verschiebt sich der Default zu weiteren Stops (Modell C mit H1-POI, M15-Trigger für Tier 2/3). Einverstanden?
4. **Backtest-Daten:** externe Tickdaten (Dukascopy o. ä.) beschaffen und als Custom Symbols importieren?
5. **Research-Pipeline in Python** (Ereignisstudien, Walk-Forward, Monte Carlo): gewünscht? Empfehlung: ja.
6. **Umfang v1:** Modell C + Modell A (Tier 1), oder erst nur C?
7. **Organisation:** Repository/Git, Sprache der Code-Kommentare.
