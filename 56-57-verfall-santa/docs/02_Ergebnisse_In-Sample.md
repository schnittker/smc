# Ergebnisse Strategien Nr. 56 und 57 – Modell KA „Verfall und Santa Rally“

Stand: 24.10.2026

Grundlagen:
- Regeln: unverändert aus der Vorregistrierung `docs/01_Vorregistrierung.md` (Commit `93ff616`)
- Code: `research/cal/`, Lauf `research/scripts/run_ka.py`; 3 Tests grün
- In-Sample: Ereignisse mit Ausstieg 2015–2023, US500, Position 1 × Kapital
- Vollständige Tabellen: `research/results/ka_in_sample.md`

## 1. Ergebnis

**Keine Variante besteht. Die Strategien Nr. 56 und 57 sind damit gescheitert.** Der Hold-out bleibt unberührt, T204–T209 entfallen.

| Kennzahl | K-OPEX (56) | K-POST (56, Short) | K-SANTA (57) |
|---|---|---|---|
| Ereignisse | 105 | 102 | 9 |
| Netto je Ereignis (bp) | **−6,7** | **−30,3** | **+0,1** |
| vor Kosten je Ereignis | −1,7 | −23,0 | +7,3 |
| t-Wert (kleinster) | −0,28 | −1,61 | 0,00 |
| Jahre positiv | 5 von 9 | 4 von 9 | 7 von 9 |
| Teilzeiträume 2015–2019 / 2020–2023 | +41,6 / −71,1 | −18,8 / −46,8 | −55,5 / +69,6 |

## 2. Einordnung

- **OPEX-Woche:** Im Mittel ist sie 2015–2023 nicht besser als jede andere Woche. Bis 2019 war sie noch positiv, danach negativ. Quartalsverfälle waren schlecht (−48 bp), die übrigen Monate leicht positiv (+13 bp, t 0,6).
- **Woche nach OPEX:** Sie ist **positiv** für Long. Der Short verliert −23 bp vor Kosten, also das Gegenteil von Stivers & Sun (2013). Das passt zu einem Effekt, der nach seiner Veröffentlichung verschwunden ist, und zur allgemeinen Aufwärtsdrift.
- **Santa Rally:** 7 von 9 Jahren sind positiv, im Mittel nach Kosten aber null. Mit 9 Ereignissen lässt sich das nicht testen.
- Kalendereffekte sind damit in fünf Projekten gescheitert (Nr. 10, 26, 27, 56, 57). Nur die FOMC-Fenster (Nr. 9, 24) kamen in die Nähe der Schwelle.

## 3. Trial-Log (Fortsetzung)

| # | Datum | Test | Ergebnis |
|---|---|---|---|
| T201 | 24.10.2026 | K-OPEX, In-Sample | nicht bestanden: −6,7 bp/Ereignis, t −0,28 |
| T202 | 24.10.2026 | K-POST, In-Sample | nicht bestanden: −30,3 bp/Ereignis, t −1,61 |
| T203 | 24.10.2026 | K-SANTA, In-Sample | nicht bestanden: +0,1 bp/Ereignis, t 0,00 (9 Ereignisse) |
| T204–T209 | – | Hold-out, FTMO | entfallen, Hold-out unberührt |
