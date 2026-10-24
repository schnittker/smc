# Ergebnisse Kontrollen Nr. 98 und 99 – Modell PL „Placebo“

Stand: 24.10.2026

Grundlagen:
- Regeln: unverändert aus der Vorregistrierung `docs/01_Vorregistrierung.md` (Commit `7ccabbc`)
- Code: `research/plc/`, Lauf `research/scripts/run_pl.py`; 2 Tests grün
- Vollständige Tabellen: `research/results/pl_in_sample.md`

## 1. Ergebnis

**Beide Kontrollen scheitern wie erwartet. Die Pipeline erzeugt keine falschen Treffer.**

| Kennzahl | PL-RANDOM (98) | PL-MOON (99) |
|---|---|---|
| Netto | −1,46 bp/Tag, t −1,54 | Sharpe −0,50, t −1,49 |
| vor Kosten | +0,017 R je Trade, 95 %: [−0,019; +0,053] | Kurs +0,2 % p. a. bei 10 % Vol. |
| Ø R netto | −0,027 je Trade | – |
| Jahre positiv / Instrumente positiv | 2 von 9 / 7 von 17 | 4 von 9 / 5 von 34 |

## 2. Was die Kontrollen über die Reihe aussagen

- **Die Engine ist unverzerrt.** Zufällige Einstiege liefern vor Kosten ≈ 0, das 95-%-Intervall enthält 0. Nach Kosten verlieren sie genau die Kosten (≈ 0,044 R je Trade). Die Kostenrechnung ist also nicht systematisch zu pessimistisch.
- **Die meisten „Vor-Kosten-Edges“ der Reihe sind nicht von Zufall unterscheidbar.** Viele H4-Regeln (Nr. 36–38, 50–55, 61–76) lagen vor Kosten bei +0,00 bis +0,03 R je Trade. Das liegt im Zufallsintervall von PL-RANDOM ([−0,019; +0,053]) und ist mit null Edge vereinbar.
- **Mondphasen** bringen 2015–2023 vor Kosten ≈ 0 (+0,2 % p. a.). Ein Lunar-Effekt ist nicht erkennbar.

## 3. Trial-Log (Fortsetzung)

| # | Datum | Test | Ergebnis |
|---|---|---|---|
| T297 | 24.10.2026 | PL-RANDOM (98), In-Sample | nicht bestanden (Kontrolle ok): −1,46 bp/Tag, vor Kosten +0,017 R [−0,019; +0,053] |
| T298 | 24.10.2026 | PL-MOON (99), In-Sample | nicht bestanden (Kontrolle ok): Sharpe −0,50 |
