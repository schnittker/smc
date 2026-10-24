# Ergebnisse Strategie Nr. 10 – Modell T „Turn-of-the-Month US500“

Stand: 24.10.2026

Grundlagen:
- Regeln: unverändert aus der Vorregistrierung `docs/01_Vorregistrierung.md` (Commit `eb70847`)
- Code: `research/tom/`, Lauf `research/scripts/run_t.py` (Commit `ee0a13a`); 25 Tests grün
- In-Sample: Monatswechsel 2015–2023, US500, NYSE-Handelstage
- Vollständige Tabellen: `research/results/t_in_sample.md`

## 1. Ergebnis

**Beide Varianten verfehlen das Hauptkriterium deutlich. Strategie Nr. 10 ist damit gescheitert.** Der Hold-out 2024–2026 bleibt unberührt, T37 und T38 entfallen.

| Kriterium | Schwelle | T-KLASSIK (Tag −1 bis +3) | T-FRÜH (Tag −4 bis +2) |
|---|---|---|---|
| Netto je Ereignis | > 0 | +22,0 bp | +36,4 bp |
| t-Wert (kleinster aus iid, Quartal) | ≥ 3,0 | **1,17** | **1,68** |
| Jahre positiv | ≥ 6 von 9 | **5 von 9** | 6 von 9 |
| Teilzeiträume 2015–2019 / 2020–2023 | beide > 0 | +6,1 / +44,1 bp | +13,0 / +66,6 bp |
| bei doppelten Kosten | > 0 | +17,9 bp | +30,7 bp |
| Sharpe Ratio p. a. (12 Ereignisse) | – | 0,39 | 0,56 |
| Kosten je Ereignis (davon Swap) | – | 4,2 bp (3,0) | 5,7 bp (4,5) |
| Notfall-Stops | – | 6 | 13 |

## 2. Einordnung

1. **Die Fenster verdienen mehr als ein durchschnittlicher Tag, aber die Schwankung überdeckt es.**
   - Gegenüber den übrigen Tagen (+2,3 bp je Tag bei US500) bringen die Fenster etwa 5 bis 7 bp mehr pro Tag.
   - Ein 4- bis 6-Tage-Fenster schwankt aber um rund 190–210 bp. Bei 100 Ereignissen reicht das nur für t 1,2 bzw. 1,7.
   - Für t ≥ 3 hätte es etwa 60–65 bp netto je Ereignis gebraucht.
2. **Der Effekt hat sich verlagert** (beschreibend, Tabelle der relativen Tage):
   - Der letzte Handelstag (Tag −1), der Kern des klassischen Fensters, ist bei US500 negativ (−7,5 bp).
   - Positiv sind vor allem Tag −2 (+19,2 bp), Tag +1 (+14,6 bp) und Tag +4 (+13,9 bp). Kein einzelner Tag ist signifikant (alle t < 2).
   - Das passt zur Literatur, nach der der Effekt wandert und verwischt.
3. **2015–2019 schwach, 2020–2023 stark**, wie bei Nr. 9. Getragen wird das vor allem von 2020 (+1.255 bp bzw. +1.270 bp), dem Jahr der starken Erholung nach dem Corona-Crash. Hohe Gewinne in wenigen Jahren mit starkem Aufwärtstrend sprechen eher für Markt-Exposure als für einen stabilen Kalendereffekt.
4. **US100 zeigt dasselbe Bild:** +28 bzw. +50 bp je Ereignis, t 1,15 bzw. 1,56, je 5 von 9 Jahren positiv.

**Datenhinweis:** 8 Ereignisse (T-KLASSIK) bzw. 12 (T-FRÜH) entfielen nach der vorregistrierten Regel, weil die 15:55-Kerze fehlte.
- **Verkürzte NYSE-Handelstage** (Tag nach Thanksgiving, 24.12., um den 3.7.) schließen um 13:00. Dann gibt es keinen Kurs um 15:55.
- Dazu kommt die bekannte HistData-Lücke März bis Juli 2023.
- Ein EA bräuchte eine Regel für verkürzte Handelstage. Das Urteil ändert sich bei t-Werten von 1,2 bzw. 1,7 nicht.

## 3. Bezug zu den festen Rahmenbedingungen

Allein für FTMO ungeeignet (12 Ereignisse pro Jahr, σ ≈ 2 % je Ereignis). Als Ensemble-Baustein ist die Strategie schwächer als Nr. 9 (t 1,7 gegenüber 2,4). Sie ist zudem eng mit dem Markt-Exposure verbunden, das Nr. 9 und ein späteres Index-Long ohnehin abdecken.

## 4. Trial-Log (Fortsetzung)

| # | Datum | Test | Ergebnis |
|---|---|---|---|
| T35 | 24.10.2026 | T-KLASSIK, In-Sample | nicht bestanden: +22,0 bp/Ereignis, t 1,17, 5 von 9 Jahren |
| T36 | 24.10.2026 | T-FRÜH, In-Sample | nicht bestanden: +36,4 bp/Ereignis, t 1,68 |
| T37 | – | Hold-out | entfällt, Hold-out unberührt |
| T38 | – | FTMO-Bootstrap | entfällt |

US100, die Tabelle der relativen Tage und die Prüfung der fehlenden Ereignisse sind beschreibende Diagnosen, keine neuen Trials.
