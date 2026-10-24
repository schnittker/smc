# Ergebnisse Strategie Nr. 24 – Modell F „USD an FOMC-Tagen“

Stand: 24.10.2026

Grundlagen:
- Regeln: unverändert aus der Vorregistrierung `docs/01_Vorregistrierung.md` (Commit `d933305`)
- Code: `research/ffx/`, Lauf `research/scripts/run_f.py` (Commit `1bff5ad`); 2 Tests grün
- In-Sample: 71 FOMC-Termine 2015–2023
- Vollständige Tabellen: `research/results/f_in_sample.md`

## 1. Ergebnis

**Beide Varianten verfehlen nur das Hauptkriterium (t ≥ 3,0), die übrigen drei erfüllen sie. Strategie Nr. 24 ist damit nach den Regeln gescheitert.** Der Hold-out 2024–2026 bleibt unberührt, T86 und T87 entfallen.

| Kriterium | Schwelle | F-USD (Short USD gegen 7) | F-CARRY (Short USD gegen die 3 Hochzinsen) |
|---|---|---|---|
| Netto je Termin (bp des Kapitals) | > 0 | +107,7 | +54,6 |
| t-Wert (kleinster aus iid, Quartal) | ≥ 3,0 | **2,10** | **2,11** (Quartal 2,58) |
| Jahre positiv | ≥ 6 von 9 | 7 von 9 | **9 von 9** |
| Teilzeiträume 2015–2019 / 2020–2023 | beide > 0 | +81,6 / +141,4 | +42,3 / +67,8 |
| bei doppelten Kosten | > 0 | +92,0 | +50,0 |
| Termine gehandelt | – | 71 | 58 |
| Kosten je Termin | – | 15,7 bp | 4,6 bp |
| Sharpe Ratio p. a. (8 Termine) | – | 0,70 | 0,70 |

F-CARRY handelte 2018–2019 kaum (5 bzw. 1 Termin), weil der USD damals den höchsten Zins der 8 Währungen hatte.

## 2. Einordnung

1. **Der Effekt des Papers ist 2015–2023 klar sichtbar.**

   | Short-USD-Korb über den FX-Tag, vor Kosten (beschreibend) | Ø bp | t |
   |---|---|---|
   | FOMC-Tage (71) | +136,8 | +2,66 |
   | übrige Tage (2.269) | −9,3 | −1,36 |
   | Differenz | **+146,1** | **+2,81** |

   Der USD wertet an FOMC-Tagen deutlich stärker ab als sonst, wie bei Mueller, Tahbaz-Salehi & Vedolin (2017). Das gilt in 7 bzw. 9 von 9 Jahren und auch nach den Straffungsphasen der Fed.
2. **Statistisch knapp unter der Schwelle.** t-Werte um 2,1 (iid) bzw. 2,3–2,6 (Quartal) bei nur 71 bzw. 58 Ereignissen. Nach 51 Versuchen ist ein solcher t-Wert für sich kein Beleg. Gleichzeitig ist er von unseren Daten unabhängig vorhergesagt worden.
3. **Zweiter FOMC-Kandidat nach Nr. 9.** Beide Effekte liegen an denselben Tagen und passen zusammen: Vor dem Entscheid sind Aktien stärker und der USD schwächer. Ob sie zusammen mehr Aussagekraft haben, wäre eine **neue, vorab festzulegende** Hypothese („FOMC-Risk-on“), keine Nachauswertung dieser Daten.

## 3. Bezug zu den festen Rahmenbedingungen

- Allein ungeeignet: 8 Termine pro Jahr, die Schwankung je Termin ist groß (σ 433 bp bei F-USD mit 7 Paaren zu je 10 % / σ).
- **Ensemble-Kandidat** (Nr. 100) neben Nr. 9: Kosten klein (F-CARRY 4,6 bp je Termin), feste Termine aus dem MT5-Kalender.

## 4. Trial-Log (Fortsetzung)

| # | Datum | Test | Ergebnis |
|---|---|---|---|
| T84 | 24.10.2026 | F-USD, In-Sample | nicht bestanden: +107,7 bp/Termin, t 2,10 (3 von 4 Kriterien) |
| T85 | 24.10.2026 | F-CARRY, In-Sample | nicht bestanden: +54,6 bp/Termin, t 2,11 (3 von 4 Kriterien, 9/9 Jahre) |
| T86 | – | Hold-out | entfällt, Hold-out unberührt |
| T87 | – | FTMO-Bootstrap | entfällt |
