# Ergebnisse Strategien Nr. 77, 79, 80 – Modell HP „Harmonische Muster, Wyckoff-Spring, M5-Scalping“ (Nr. 78 ⊘)

Stand: 24.10.2026

Grundlagen:
- Regeln: unverändert aus der Vorregistrierung `docs/01_Vorregistrierung.md` (Commit `7a4df75`)
- Code: `research/hps/`, Lauf `research/scripts/run_hp.py`; 3 Tests grün
- In-Sample: Einstiege 2015–2023, 0,25 % Risiko je Trade
- Vollständige Tabellen: `research/results/hp_in_sample.md`

## 1. Ergebnis

**Keine Variante besteht. Die Strategien Nr. 77, 79 und 80 sind damit gescheitert. Nr. 78 (Elliott-Wellen) ist nicht formalisierbar und wird nicht getestet.** Der Hold-out bleibt unberührt, T270–T275 entfallen.

| Variante | Nr. | TF | Trades | Netto bp/Tag | vor Kosten bp/Tag | Ø R vor / nach Kosten | t | Jahre + | Instr. + |
|---|---|---|---|---|---|---|---|---|---|
| HP-HARM | 77 | H4 | 107 | −0,12 | −0,09 | −0,076 / −0,106 | −1,27 | 5 | 5 |
| HP-SPRING | 79 | H4 | 3.791 | −1,27 | +1,49 | +0,037 / −0,031 | −0,99 | 2 | 7 |
| HP-SCALP | 80 | M5 | 69.905 | −164,71 | −0,24 | −0,000 / −0,224 | −28,27 | 0 | 0 (von 7) |

## 2. Einordnung

- **Harmonische Muster:** Mit Standard-Toleranzen sind sie sehr selten, nur 107 Trades in 9 Jahren über 17 Instrumente, und schon vor Kosten negativ.
- **Spring/Upthrust:** Mit +0,037 R vor Kosten die beste Umkehrregel des Projekts. Die Kosten (0,07 R) sind aber doppelt so hoch, und nur 2 von 9 Jahren sind positiv.
- **M5-Scalping:** Vor Kosten exakt null. Die Kosten liegen bei 0,22 R je Trade, das ergibt −1,6 % je Tag bei 0,25 % Risiko. Damit ist die Listennotiz „Kosten fressen den Edge“ bestätigt; auf M5 gibt es nicht einmal einen Edge.
- **Abschnitt C ist abgeschlossen:** 19 getestete Regeln aus 20 Listenplätzen, keine besteht.

## 3. Trial-Log (Fortsetzung)

| # | Datum | Test | Ergebnis |
|---|---|---|---|
| T267 | 24.10.2026 | HP-HARM (77), In-Sample | nicht bestanden: −0,12 bp/Tag, t −1,27 (107 Trades) |
| T268 | 24.10.2026 | HP-SPRING (79), In-Sample | nicht bestanden: −1,27 bp/Tag, t −0,99 |
| T269 | 24.10.2026 | HP-SCALP (80), In-Sample | nicht bestanden: −164,7 bp/Tag, t −28,3 |
| T270–T275 | – | Hold-out, FTMO | entfallen, Hold-out unberührt |
