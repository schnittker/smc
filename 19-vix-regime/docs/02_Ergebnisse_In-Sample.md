# Ergebnisse Strategie Nr. 19 – Modell X „VIX-Regime“

Stand: 24.10.2026

Grundlagen:
- Regeln: unverändert aus der Vorregistrierung `docs/01_Vorregistrierung.md` (Commit `ca55ef9`)
- Code: `research/vixr/`, Lauf `research/scripts/run_x.py` (Commit `175a7bc`); 4 Tests grün
- In-Sample: Handelstage 2015–2023
- Vollständige Tabellen: `research/results/x_in_sample.md`
- **Korrektur nach dem ersten Lauf:** Die aus Nr. 14 übernommene Statistik fasste bei X-HAVEN die drei Instrumente nicht je Tag zusammen (7.010 statt 2.340 Tage). Die Aggregation wurde korrigiert und der Lauf wiederholt. Regeln und Positionen sind unverändert. Das Urteil (nicht bestanden) war vor und nach der Korrektur dasselbe.

## 1. Ergebnis

**Beide Varianten verfehlen das Hauptkriterium deutlich. Strategie Nr. 19 ist damit gescheitert.** Der Hold-out 2024–2026 bleibt unberührt, T66 und T67 entfallen.

| Kriterium | Schwelle | X-HAVEN (JPY, CHF, Gold long im Risk-off) | X-FEAR (US500 long im Risk-off) |
|---|---|---|---|
| Sharpe Ratio p. a. netto | (≈ 1,0) | **−0,14** | **0,04** |
| t-Wert (kleinster aus iid, Woche, Monat) | ≥ 3,0 | **−0,65** | **0,13** |
| Jahre positiv | ≥ 6 von 9 | **3 von 9** | 6 von 9 |
| Teilzeiträume | beide > 0 | **nein** | **nein** (2020–2023 negativ) |
| bei doppelten Kosten | > 0 | **nein** | ja |

Risk-off herrschte an 11 % der Handelstage, verteilt auf 48 Episoden.

## 2. Einordnung

1. **Sichere Häfen verdienen nach dem Signal nichts.** JPY und CHF verloren im Risk-off-Regime (je etwa −10 % Summe bei 10-%-Volatilitätssizing), Gold gewann leicht (+3 %). Das passt zu Ranaldo & Söderlind (2010): Die Aufwertung passiert *gleichzeitig* mit dem Stress, also bevor ein Tagesschluss-Signal handeln kann. 2022 war die Umkehrung (USD stark, JPY schwach) besonders teuer (−23 %).
2. **„Fear kaufen“ ist 2015–2023 nur knapp positiv.** US500 brachte im Risk-off insgesamt +3 % (Summe), bei einer Sharpe Ratio von 0,04 für die Strategie. Die von Giot (2005) beschriebene Erholung nach VIX-Spitzen reicht hier nicht. 2020 (Corona-Crash, −3,7 %) zeigt, dass ein hoher VIX auch der Anfang eines größeren Einbruchs sein kann.
3. **Externe Datenquelle:** Selbst bei Erfolg bräuchte der EA den VIX per `WebRequest`.

## 3. Trial-Log (Fortsetzung)

| # | Datum | Test | Ergebnis |
|---|---|---|---|
| T64 | 24.10.2026 | X-HAVEN, In-Sample | nicht bestanden: Sharpe −0,14, t −0,65 |
| T65 | 24.10.2026 | X-FEAR, In-Sample | nicht bestanden: Sharpe 0,04, t 0,13 |
| T66 | – | Hold-out | entfällt, Hold-out unberührt |
| T67 | – | FTMO-Bootstrap | entfällt |
