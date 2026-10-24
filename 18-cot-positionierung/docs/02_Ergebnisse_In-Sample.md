# Ergebnisse Strategie Nr. 18 – Modell C „COT-Extreme“

Stand: 24.10.2026

Grundlagen:
- Regeln: unverändert aus der Vorregistrierung `docs/01_Vorregistrierung.md` (Commit `203db86`)
- Code: `research/cot/`, Lauf `research/scripts/run_c.py` (Commit `30a070b`); 5 Tests grün
- In-Sample: Handelstage 2015–2023, 7 FX-Paare und Gold, COT-Berichte ab 2012
- Vollständige Tabellen: `research/results/c_in_sample.md`

## 1. Ergebnis

**Beide Varianten verfehlen das Hauptkriterium deutlich. Strategie Nr. 18 ist damit gescheitert.** Der Hold-out 2024–2026 bleibt unberührt, T62 und T63 entfallen.

| Kriterium | Schwelle | C-KONTRA (gegen die Spekulanten) | C-FOLGE (mit den Spekulanten) |
|---|---|---|---|
| Sharpe Ratio p. a. netto | (≈ 1,0) | **0,22** | **−0,50** |
| t-Wert (kleinster aus iid, Woche, Monat) | ≥ 3,0 | **0,62** | **−1,57** |
| Jahre positiv | ≥ 6 von 9 | 6 von 9 | **2 von 9** |
| Instrumente positiv | ≥ 60 % | 6 von 8 | **2 von 8** |
| bei doppelten Kosten | > 0 | +0,6 % p. a. | **−6,6 % p. a.** |
| Zeit im Markt | – | 17 % der Instrument-Tage | 17 % |

Die beiden Varianten sind Spiegelbilder auf demselben Signal. Ihre Summe ergibt im Wesentlichen die doppelten Kosten.

## 2. Einordnung

1. **2015–2023 eher Umkehr als Fortsetzung, aber nicht signifikant.**
   - Gegen die Spekulanten-Extreme zu handeln, brachte leicht positive Ergebnisse (Sharpe 0,22), mit ihnen negative (−0,50).
   - Tornell & Yuan (2012) fanden in ihren Daten (bis etwa 2008) das Gegenteil. Ein stabiler Zusammenhang in eine Richtung ist damit nicht belegt.
   - Das Vorzeichen passt zum Scheitern der Trendfolge (Nr. 3) und zur 12-Monats-Umkehr (Nr. 7) auf denselben Währungen.
2. **Ein Jahr trägt C-KONTRA:** 2021 brachte +14,3 % (bei 10 % Volatilität), die übrigen Jahre zusammen etwa +5 %.
   - JPY und CHF verloren konträr deutlich: Die Spekulanten lagen 2021–2023 mit dem Short in beiden Währungen richtig.
3. **Wenig Zeit im Markt:** Extreme (Index ≥ 0,9 oder ≤ 0,1) gibt es nur an 17 % der Instrument-Tage. Ein Signal pro Woche und wenige unabhängige Episoden ergeben nur geringe statistische Kraft.

## 3. Bezug zu den festen Rahmenbedingungen

Selbst bei Erfolg bräuchte der EA eine externe Datenquelle (CFTC per `WebRequest`). Bei Sharpe 0,22 stellt sich die Frage nicht.

## 4. Trial-Log (Fortsetzung)

| # | Datum | Test | Ergebnis |
|---|---|---|---|
| T60 | 24.10.2026 | C-KONTRA, In-Sample | nicht bestanden: Sharpe 0,22, t 0,62 |
| T61 | 24.10.2026 | C-FOLGE, In-Sample | nicht bestanden: Sharpe −0,50, t −1,57 |
| T62 | – | Hold-out | entfällt, Hold-out unberührt |
| T63 | – | FTMO-Bootstrap | entfällt |
