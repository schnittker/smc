# Ergebnisse Strategien Nr. 81, 82, 85, 90 – Modell ST „Statistische Modelle“

Stand: 24.10.2026

Grundlagen:
- Regeln: unverändert aus der Vorregistrierung `docs/01_Vorregistrierung.md` (Commit `913861c`)
- Code: `research/stm/`, Lauf `research/scripts/run_st.py`; 3 Tests grün (HMM, GARCH, Gold-Kalender)
- In-Sample: 2015–2023, Tagesbuchhaltung wie Nr. 28/30, Modelle jährlich nur mit Vorjahresdaten geschätzt
- Vollständige Tabellen: `research/results/st_in_sample.md`

## 1. Ergebnis

**Alle vier Modelle sind nach Kosten negativ. Die Strategien Nr. 81, 82, 85 und 90 sind damit gescheitert.** Der Hold-out bleibt unberührt, T280–T287 entfallen.

| Variante | Nr. | Sharpe | t | Rendite p. a. bei 10 % Vol. | Kurs / Swaps / Handel p. a. | Jahre + | Instr. + |
|---|---|---|---|---|---|---|---|
| ST-HMM | 81 | −0,55 | −1,69 | −5,5 % | +0,8 / −3,5 / −2,3 % | 1 | 9 von 34 |
| ST-GARCH | 82 | −0,50 | −1,74 | −5,1 % | −0,7 / −2,8 / −1,3 % | 3 | 12 von 34 |
| ST-KNN | 85 | −2,02 | −6,27 | −20,2 % | −0,5 / −5,9 / −11,8 % | 0 | 8 von 34 |
| ST-GOLD | 90 | −0,10 | −0,31 | −1,1 % | −0,2 / −0,8 / −0,0 % | 2 | – |

## 2. Einordnung

- **HMM:** Der Regimefilter macht die 20-Tage-Trendregel vor Kosten leicht positiv (+0,8 % p. a. bei 10 % Vol.). Swaps und Handel kosten aber −5,7 %.
- **GARCH:** Eine bessere Vol-Prognose rettet die Trendregel nicht. Schon vor Kosten bleibt sie negativ (−0,7 %).
- **k-NN:** Die Muster der letzten 10 Tage sagen den nächsten Tag nicht voraus (Kurs −0,5 %). Die häufigen Wechsel kosten 12 % p. a.
- **Gold im September/November:** Kein Saisoneffekt 2015–2023, nur 2 von 9 Jahren positiv.
- Damit bestätigt sich der Befund aus Abschnitt A–C: Selbst flexible statistische Modelle finden auf Tagesbasis keine Vorhersagekraft, die die Kosten trägt.

## 3. Trial-Log (Fortsetzung)

| # | Datum | Test | Ergebnis |
|---|---|---|---|
| T276 | 24.10.2026 | ST-HMM (81), In-Sample | nicht bestanden: Sharpe −0,55, t −1,69 |
| T277 | 24.10.2026 | ST-GARCH (82), In-Sample | nicht bestanden: Sharpe −0,50, t −1,74 |
| T278 | 24.10.2026 | ST-KNN (85), In-Sample | nicht bestanden: Sharpe −2,02, t −6,27 |
| T279 | 24.10.2026 | ST-GOLD (90), In-Sample | nicht bestanden: Sharpe −0,10, t −0,31 |
| T280–T287 | – | Hold-out, FTMO | entfallen, Hold-out unberührt |
