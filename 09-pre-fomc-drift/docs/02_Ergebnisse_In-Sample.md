# Ergebnisse Strategie Nr. 9 – Modell P „Pre-FOMC-Drift“

Stand: 24.10.2026

Grundlagen:
- Regeln: unverändert aus der Vorregistrierung `docs/01_Vorregistrierung.md` (Commit `c139be4`)
- Code: `research/fomc/`, Lauf `research/scripts/run_p.py` (Commit `b58225e`); 7 Tests grün
- In-Sample: 71 planmäßige FOMC-Entscheide 2015–2023, HistData M5
- Vollständige Tabellen: `research/results/p_in_sample.md`

## 1. Ergebnis

**Beide Varianten verfehlen das Hauptkriterium (t ≥ 3,0) und sind damit nach den Regeln gescheitert.** Die übrigen drei Kriterien erfüllen beide. Der Hold-out 2024–2026 bleibt unberührt, T33 und T34 entfallen.

| Kriterium | Schwelle | P-SPX (US500) | P-NDX (US100) |
|---|---|---|---|
| Netto je Termin | > 0 | +19,2 bp | +28,3 bp |
| t-Wert (kleinster aus iid, Quartal) | ≥ 3,0 | **2,38** | **2,26** (iid 2,68) |
| Jahre positiv | ≥ 6 von 9 | 7 von 9 | 6 von 9 |
| Teilzeiträume 2015–2019 / 2020–2023 | beide > 0 | +7,3 / +37,0 bp | +9,1 / +55,8 bp |
| bei doppelten Kosten | > 0 | +17,5 bp | +26,5 bp |
| Sharpe Ratio p. a. (8 Termine) | – | 0,77 | 0,89 |
| Kosten je Termin (davon Swap) | – | 1,7 bp (0,9) | 1,8 bp (0,9) |

**Zum ersten Mal in der Testreihe ist ein Effekt deutlich größer als die Kosten.** Er ist aber nicht stark genug für die vorab festgelegte Schwelle.

## 2. Einordnung

1. **Der FOMC-Effekt ist sichtbar.** Im selben Uhrzeitfenster (14:00 Vortag bis 13:55) bringen alle übrigen Handelstage +3,9 bp (US500) bzw. +5,9 bp (US100). Die FOMC-Termine liegen um **+17,1 bp bzw. +24,2 bp** darüber (t je 2,21). Der Effekt ist also nicht nur die allgemeine Aufwärtsdrift der Indizes.
2. **2015–2019 schwach, 2020–2023 stark.**
   - 2015–2019 brachten nur +7 bis +9 bp je Termin. Das passt zu Kurov, Wolfe & Gilbert (2021): Bis 2019 war die Drift „verschwunden“.
   - 2020–2023 brachten +37 bis +56 bp, getragen von 2020 und 2022 (Summe 2022: +576 bzw. +884 bp). Das waren Jahre hoher Unsicherheit. Kurov et al. bringen die Drift mit dem VIX-Niveau vor dem Termin in Verbindung.
   - Mit nur 8 Terminen pro Jahr bleibt das ein dünnes Fundament.
3. **Die Drift entsteht über Nacht** (beschreibend): 16:00 am Vortag bis 09:30 am Entscheidungstag +19 bp (US500, t 3,8) bzw. +29 bp (US100, t 4,1). Die Fenster 14:00–16:00 am Vortag und 09:30–13:55 liegen bei null.
   - **Vorsicht:** Das Teilfenster wurde nach Ansicht der Daten ausgewählt. Wer nur noch das Overnight-Fenster handelt, testet eine aus dem In-Sample abgeleitete Hypothese. Der t-Wert von ~4 ist dafür kein gültiger Nachweis.
4. **Datenlücke 2023:** Von März bis Juli 2023 fehlen bei HistData häufig Kerzen zur vollen Stunde (dieselbe Lücke wie bei Nr. 6). Deshalb entfielen nach der vorregistrierten Regel 4 Termine (US500) bzw. 3 Termine (US100). Gegenprobe mit der nächstgelegenen Kerze: Mit allen 71 Terminen läge t (iid) bei 2,50 bzw. 2,58. Das Urteil ändert sich nicht.
5. **Mehrfachtesten:** Nach 32 Versuchen ist ein t-Wert um 2,4 auch als Zufallstreffer plausibel. Genau deshalb liegt die Schwelle bei 3,0.

## 3. Bezug zu den festen Rahmenbedingungen

- **Allein für FTMO ungeeignet, wie vorab festgehalten.** Mit 8 Trades pro Jahr und rund +20–28 bp je Trade bei einfachem Nominal kommt man selbst mit Hebel 3 nur auf etwa 5–7 % p. a. Die Schwankung je Termin (σ 70–87 bp) belastet dabei die 5-%-Tagesgrenze.
- **Als Baustein für ein Ensemble (Nr. 100) interessant:** Der Ertrag kommt an wenigen festen Tagen, die Kosten sind klein, und die Ertragsquelle unterscheidet sich von allen bisherigen Strategien.
- Für eine echte Bestätigung reicht der Hold-out nicht. 2024–2026 enthalten nur rund 22 Termine; selbst bei einem echten Effekt dieser Größe wäre dort ein t-Wert um 1,4 zu erwarten.

## 4. Gesamtbild nach Strategie 1–9 (ohne 8)

| Nr. | Strategie | Ergebnis |
|---|---|---|
| 1 | SMC | kein Baustein nach Kosten profitabel |
| 2 | Fix-Reversal | Effekt nur so groß wie die Kosten (Sharpe 0,31) |
| 3 | Trendfolge FX/Gold | Sharpe −0,53 |
| 4 | Trendfolge Indizes/Rohstoffe | Sharpe −0,37 |
| 5 | Monatsend-Rebalancing | Effekt seit 2015 auf ein Zehntel geschrumpft |
| 6 | FX Carry G8 | Sharpe −0,16 / −0,02 |
| 7 | FX Querschnitts-Momentum G8 | Sharpe −0,28 / −0,81 |
| 9 | Pre-FOMC-Drift | **+19 bzw. +28 bp je Termin, t 2,4 / 2,3: knapp gescheitert, Ensemble-Kandidat** |

## 5. Trial-Log (Fortsetzung)

| # | Datum | Test | Ergebnis |
|---|---|---|---|
| T31 | 24.10.2026 | P-SPX, In-Sample | nicht bestanden: +19,2 bp/Termin, t 2,38 (3 von 4 Kriterien erfüllt) |
| T32 | 24.10.2026 | P-NDX, In-Sample | nicht bestanden: +28,3 bp/Termin, t 2,26 (3 von 4 Kriterien erfüllt) |
| T33 | – | Hold-out | entfällt, Hold-out unberührt |
| T34 | – | FTMO-Bootstrap | entfällt |

Kontrollvergleich, Teilfenster und die Gegenprobe zur Datenlücke 2023 sind beschreibende Diagnosen, keine neuen Trials.
