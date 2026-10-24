# Ergebnisse Gate P2 – Ereignisstudie der SMC-Bausteine

Stand: 24.10.2026

Grundlagen:
- Daten: HistData M1 (Bid), 25 Instrumente, umgerechnet in FTMO-Serverzeit (NY + 7 h)
- Auswertungszeitraum: **2015–2023 (In-Sample)**. Der Hold-out 2024–2026 bleibt unangetastet.
- Code: `research/smc/` (Engine), `research/scripts/run_event_study.py` (Studie)
- Vollständige Tabelle: `research/results/event_study_p2.md`; Datenqualität: `research/results/data_quality.md`

## 1. Methode in Kürze

**Bausteine**
- Alle Bausteine laufen mit den vorab festgelegten Parametern aus Blueprint und Kapitel 2. Nichts wurde optimiert.
- Jeder Baustein ist kausal implementiert: Jedes Ereignis zählt erst ab seinem Bestätigungszeitpunkt. 31 Tests sind grün, darunter History-Invarianz-Tests.

**Messung je Ereignis**
- **Einstieg:** Markteinstieg zur Eröffnung der ersten M5-Kerze nach dem Ereignis, in Richtung der Hypothese.
- **Ergebnis in R:** Ziel +2 Einheiten, Stop −1 Einheit. Erreicht eine Kerze beides, zählt sie als Verlust. Ohne Treffer gilt der Marktwert bei Zeitablauf.
- **Zwei Einheiten:**
  - ATR14(M15) mit 24 h Horizont
  - **ATR14(H1) mit 3 Handelstagen Horizont.** Diese weitere Variante passt zum FTMO-Plan und wird in diesem Dokument berichtet.

**Placebo**
- Je Ereignis 3 zufällige M5-Kerzen desselben Instruments, mit gleicher New-York-Stunde, gleichem Volatilitätsdezil und gleicher Richtung.

**Statistik**
- Bootstrap mit Handelstagen als Clustern über alle Instrumente.
- Holm-Korrektur über alle 55 Zeilen je Einheit.

**Kosten**
- FTMO-All-in-Kosten je Trade: Spread, Volume-Band-Zuschlag, 5 USD Kommission pro Lot und Slippage, geteilt durch die Einheit.
- Der 0,7-%-Umrechnungsabschlag ist nicht enthalten, er kostet zusätzlich etwa 0,01 R.

## 2. Ergebnisse (Einheit ATR(H1), alle Instrumente, 2015–2023)

| Baustein | Ereignisse | Δ R gg. Placebo [95-%-KI] | p (Holm) | R brutto | Kosten (R) | **R netto** |
|---|---|---|---|---|---|---|
| FVG-Touch H1 | 140.484 | **+0,043** [+0,034; +0,052] | 1e-16 | +0,034 | 0,090 | −0,056 |
| FVG-Touch M15 | 489.692 | +0,015 [+0,010; +0,021] | 1e-06 | +0,004 | 0,086 | −0,082 |
| FVG-Touch M5 | 1.241.422 | +0,008 [+0,004; +0,011] | 0,002 | −0,003 | 0,082 | −0,085 |
| OB-Touch H1 | 33.357 | +0,017 [−0,004; +0,037] | 1 | +0,007 | 0,091 | −0,084 |
| OB-Touch M15 | 113.089 | +0,012 [−0,001; +0,023] | 1 | +0,004 | 0,091 | −0,087 |
| Sweep → Umkehr | 509.362 | +0,011 [+0,004; +0,019] | 0,09 | +0,005 | 0,098 | −0,092 |
| Sweep → Umkehr, nur London-Killzone | 116.566 | −0,009 [−0,023; +0,004] | 1 | −0,001 | 0,104 | −0,105 |
| Sweep → Umkehr, nur NY-Killzone | 76.781 | −0,017 [−0,036; +0,000] | 1 | −0,022 | 0,097 | −0,119 |
| Break → Fortsetzung | 201.679 | **−0,019** [−0,029; −0,009] | 0,02 | −0,026 | 0,093 | −0,119 |
| **MSS nach Sweep (ICT-2022-Trigger)** | 23.855 | −0,008 [−0,030; +0,013] | 1 | −0,012 | 0,089 | −0,101 |
| BOS/CHoCH H1 (Swing) | 13.842 | +0,015 [−0,018; +0,045] | 1 | −0,009 | 0,088 | −0,098 |
| BOS/CHoCH H4 (Swing) | 5.179 | +0,040 [−0,005; +0,088] | 1 | +0,023 | 0,085 | −0,063 |
| **H1-Trendwechsel in H4-Trendrichtung** | 1.595 | **+0,138** [+0,059; +0,226] | 0,07 | **+0,140** | 0,086 | **+0,053** |
| H1-Trendwechsel gegen H4-Trend | 2.799 | −0,043 [−0,109; +0,025] | 1 | −0,066 | 0,083 | −0,150 |

Mit der engeren Einheit ATR(M15) sind einige Effekte stärker signifikant, die Kosten liegen dort aber bei 0,13–0,25 R. Dazu gehören OB-Touch H1 (+0,050 R, p = 6e-05) und Sweep → Umkehr (+0,024 R, p = 3e-11). Alle Zeilen stehen in `research/results/event_study_p2.md`.

**Stabilitätsprüfung**

| Baustein | Jahre mit positivem Δ | Instrumente mit positivem Δ | Instrumente netto im Plus |
|---|---|---|---|
| FVG-Touch H1 | 9 von 9 (Spanne +0,025 bis +0,060) | 25 von 25 | 1 von 25 |
| H1-Trendwechsel in H4-Trendrichtung | 7 von 9 (2021 und 2023 negativ) | 16 von 25 | 13 von 25 |

Beim H1-Trendwechsel liegen nur etwa 170 Ereignisse pro Jahr vor, entsprechend groß ist die Streuung.

## 3. Was das bedeutet

1. **Kein Baustein ist allein und mit Markteinstieg nach Kosten profitabel.** Die Brutto-Effekte liegen bei höchstens +0,04 R. Die FTMO-Kosten betragen auch bei weiteren Stops (ATR H1) etwa 0,09 R.
2. **Ein FVG ist ein echter, aber sehr kleiner Effekt.** Der Kurs reagiert an FVGs messbar stärker als zufällig, und zwar über alle Jahre und alle 25 Instrumente. Ein FVG taugt damit als **Ort für den Einstieg** (Limit-Order statt Markt) oder als Filter, nicht als eigenständiges Signal.
3. **Das ICT-Kernmodell trägt nicht.** Sweep → MSS hat in dieser Definition keinen Effekt. Sweeps in den Killzones sind nicht besser als außerhalb, in New York sogar tendenziell schlechter. Damit ist **Modell A (Sweep → MSS → FVG) als Primärmodell nicht gestützt.** Es wird zurückgestellt.
4. **Auf M5-Ebene laufen Level-Brüche eher zurück:** Break → Fortsetzung ist signifikant negativ. Das widerspricht der Fortsetzungs-These des SSRN-Preprints, ist aber ebenfalls klein.
5. **Der einzige ökonomisch interessante Kandidat** ist das Ende eines Gegen-Swings im übergeordneten Trend. Gemeint ist ein strikter H1-Trendwechsel in Richtung des H4-Trends. Er liegt bei +0,14 R brutto bzw. +0,05 R netto. Er passt zur besten externen Evidenz (Trendfilter als dominanter Faktor, → K4 §4) und zum Konzept von Modell C. **Aber:** Nach Holm-Korrektur ist er nicht signifikant (p = 0,07), die Streuung ist groß, und er wurde nach Sichtung der In-Sample-Daten hervorgehoben. Er ist daher eine **Hypothese**, kein Befund.

**Gate P2:** Statistisch erfüllt, denn mehrere Bausteine sind nach Korrektur signifikant. **Ökonomisch nicht erfüllt**, denn alle sind netto negativ. Ein EA, der diese Bausteine einzeln und per Markteinstieg handelt, würde die Challenge sehr wahrscheinlich nicht bestehen.

## 4. Vorschlag für Phase P3 (vorregistriert, vor jedem weiteren Blick in die Daten)

1. **Ein einziges Modell** wird geprüft: **Modell C „Trend-Fortsetzung“**.
   - **Signal:**
     - H4-Trend (strikt) bestimmt die Richtung.
     - Ein strikter H1-Trendwechsel in dieselbe Richtung ist das Signal.
   - **Einstieg:** als Limit am jüngsten H1- oder M15-FVG bzw. -Order-Block des Bestätigungs-Legs. So wird der kleine, robuste FVG-Effekt genutzt.
   - **Stop und Ziel:**
     - Stop am Protected Level des H1.
     - Ziel ist der erste Liquiditätspool mit RR ≥ 2.
   - **Varianten (je ein Trial im Trial-Log):** Markteinstieg vs. Limit-Einstieg.
2. **Validierung:**
   - Walk-Forward 2015–2023 mit fest vorgegebenen Parametern.
   - Danach **einmalig** der Hold-out 2024–2026.
   - Akzeptanz nach Blueprint §16, mit Netto-Erwartung ≥ +0,1 R.
3. **Bootstrap der Challenge:** Die echten Trades werden durch die FTMO-Simulation geschickt. Gefordert ist eine Bestehenschance von mindestens 70 %.
4. **Scheitert C,** wird zuerst eine Swing-Variante auf H4/D1-Ebene geprüft, wo die Kosten nur 0,03–0,05 R betragen. Sonst wird das SMC-Narrativ verlassen, zugunsten evidenzbasierter Zeitkomponenten wie der Fixing-Effekte (→ K5 §1.4).

## 5. Trial-Log

| # | Datum | Test | Anzahl Hypothesen | Ergebnis |
|---|---|---|---|---|
| T1 | 24.10.2026 | Ereignisstudie P2 v0, 13 Bausteine × 5 Gruppen, Einheiten M15 und H1, In-Sample 2015–2023, Parameter vorab festgelegt | 55 je Einheit (110) | siehe oben; keine Parameter angepasst |
