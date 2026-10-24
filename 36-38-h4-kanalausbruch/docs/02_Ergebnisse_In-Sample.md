# Ergebnisse Strategien Nr. 36 und 38 – Modell K „H4-Kanal-Ausbruch“

Stand: 24.10.2026

Grundlagen:
- Regeln: unverändert aus der Vorregistrierung `docs/01_Vorregistrierung.md` (Commit `3ce765d`)
- Code: `research/hkb/`, Lauf `research/scripts/run_k.py`; 7 Tests grün
- In-Sample: Einstiege 2015–2023, 17 Instrumente, 0,25 % Risiko je Trade
- Vollständige Tabellen: `research/results/k_in_sample.md`

## 1. Ergebnis

**Beide Regeln sind nach Kosten leicht negativ. Die Strategien Nr. 36 und 38 sind damit gescheitert.** Der Hold-out bleibt unberührt, T125–T128 entfallen.

| Kennzahl | K-BBSQ (36) | K-KELT (38) |
|---|---|---|
| Netto je Tag (bp des Kapitals, Portfolio) | **−0,25** | **−0,76** |
| vor Kosten je Tag | +0,51 | +1,60 |
| Handelskosten und Swap-Belastung je Tag | 0,81 | 2,53 |
| Rendite p. a. netto | −0,6 % | −2,0 % |
| t-Wert (kleinster) | −0,39 | −0,51 |
| Jahre positiv | 4 von 9 | 3 von 9 |
| Instrumente positiv | 7 von 17 | 7 von 17 |
| Trades (9 Jahre) | 1.535 | 4.950 |
| Ø R je Trade vor Kosten / netto | +0,031 / −0,015 | +0,030 / −0,014 |
| Trefferquote / Stops | 32 % / 23 % | 34 % / 33 % |
| Ø Haltedauer | 13,7 H4-Kerzen (≈ 2,3 Tage) | 16,8 H4-Kerzen (≈ 2,8 Tage) |

## 2. Einordnung

- **Gleiches Bild wie bei den Tages-Ausbrüchen (Nr. 33–35):** Vor Kosten bringen beide Regeln etwa +0,03 R je Trade. Kosten und Swaps nehmen etwa 0,045 R je Trade weg.
- **Instabil:** Die Jahresergebnisse springen von +21,5 % (K-KELT 2020, Corona-Trends) bis −15,4 % (2021). Keine Anlageklasse ist über beide Varianten klar positiv. Metalle liegen bei +0,7 bzw. +1,5 % p. a., das sind aber nur 2 Instrumente.
- **Fazit für die Liste:** Preis-Ausbrüche auf H4 und D1 sind in fünf Projekten mit 10 Regeln gescheitert (Nr. 3, 4, 16, 28, 30, 31, 33–36, 38). Weitere reine Ausbruchsregeln (Nr. 51 Trendlinien, Nr. 50 S/R-Ausbruch) haben eine niedrige Vorab-Wahrscheinlichkeit.

## 3. Trial-Log (Fortsetzung)

| # | Datum | Test | Ergebnis |
|---|---|---|---|
| T123 | 24.10.2026 | K-BBSQ, In-Sample | nicht bestanden: −0,25 bp/Tag, t −0,39 |
| T124 | 24.10.2026 | K-KELT, In-Sample | nicht bestanden: −0,76 bp/Tag, t −0,51 |
| T125–T128 | – | Hold-out, FTMO | entfallen, Hold-out unberührt |
