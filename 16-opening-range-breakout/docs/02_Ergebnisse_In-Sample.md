# Ergebnisse Strategie Nr. 16 – Modell O „Opening Range Breakout 5 Minuten“

Stand: 24.10.2026

Grundlagen:
- Regeln: unverändert aus der Vorregistrierung `docs/01_Vorregistrierung.md` (Commit `d39df6a`)
- Code: `research/orb/`, Lauf `research/scripts/run_o.py` (Commit `65a8b16`); 4 Tests grün
- In-Sample: volle NYSE-Handelstage 2015–2023
- Vollständige Tabellen: `research/results/o_in_sample.md`

## 1. Ergebnis

**Beide Varianten verfehlen alle Kriterien. Strategie Nr. 16 ist damit gescheitert.** Der Hold-out 2024–2026 bleibt unberührt, T58 und T59 entfallen.

| Kriterium | Schwelle | O-NDX (US100) | O-SPX (US500) |
|---|---|---|---|
| Netto je Tag (bp des Kapitals) | > 0 | **−1,60** | **−0,41** |
| t-Wert (kleinster aus iid, Woche, Monat) | ≥ 3,0 | **−0,54** | **−0,16** |
| Jahre positiv | ≥ 6 von 9 | **4 von 9** | **3 von 9** |
| Teilzeiträume | beide > 0 | **nein** (2020–2023 negativ) | **nein** (2020–2023 negativ) |
| bei doppelten Kosten | > 0 | **nein** | **nein** |
| Ø R je Trade netto / vor Kosten | – | −0,105 / +0,033 | −0,151 / +0,092 |
| Stop / Ziel / Tagesende | – | 85 % / 4 % / 11 % | 85 % / 4 % / 11 % |
| Median-Risiko R | – | 11,1 bp | 8,8 bp |
| Tage an der Hebel-Obergrenze 4 | – | 79 % | 89 % |

## 2. Einordnung

1. **Die erste 5-Minuten-Kerze ist im CFD zu klein.**
   - Das Risiko R liegt im Median bei 9–11 bp des Kurses.
   - Spread und Slippage (etwa 1,5 bp) sind dadurch 0,14–0,24 R je Trade. Vor Kosten bliebe nur ein kleiner Vorteil (+0,03 bzw. +0,09 R).
   - 85 % der Trades enden am Stop, nur 4 % erreichen das Ziel von 10 R.
2. **CFD-Kurse sind nicht die ETF-Eröffnung.**
   - Das Paper nutzt QQQ mit Eröffnungsauktion. Der HistData-CFD handelt fortlaufend, die Kerze 09:30–09:35 enthält keine Auktion.
   - Diese Abweichung war vorab als Risiko benannt. Der EA würde aber genau auf solchen CFD-Kursen handeln, für FTMO ist also dieser Test der relevante.
3. **Die Hebel-Obergrenze ist meist bindend.** Für 1 % Risiko wären bei R ≈ 10 bp etwa 10-facher Hebel nötig, gedeckelt bei 4. Das tatsächliche Risiko liegt damit meist bei etwa 0,4 % je Trade.
4. **2020–2023 negativ, also nach Ende des Paper-Zeitraums kein Halt.** Das Paper reicht bis 2023, unsere Auswertung zeigt für beide Indizes in diesen Jahren Verluste.

## 3. Bezug zu den festen Rahmenbedingungen

Für FTMO wäre ein Tages-Breakout mit festem Risiko gut geeignet. Mit den Kosten der Index-CFDs und der kleinen Opening Range fehlt aber der Vorteil.

## 4. Trial-Log (Fortsetzung)

| # | Datum | Test | Ergebnis |
|---|---|---|---|
| T56 | 24.10.2026 | O-NDX, In-Sample | nicht bestanden: −1,60 bp/Tag, t −0,54 |
| T57 | 24.10.2026 | O-SPX, In-Sample | nicht bestanden: −0,41 bp/Tag, t −0,16 |
| T58 | – | Hold-out | entfällt, Hold-out unberührt |
| T59 | – | FTMO-Bootstrap | entfällt |

Die Trade-Statistiken sind beschreibende Diagnosen, keine neuen Trials.
