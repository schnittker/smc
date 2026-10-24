# Ergebnisse Strategien Nr. 43 und 44 – Modell E „Tagesmuster“

Stand: 24.10.2026

Grundlagen:
- Regeln: unverändert aus der Vorregistrierung `docs/01_Vorregistrierung.md` (Commit `878c55f`)
- Code: `research/dpat/`, Lauf `research/scripts/run_e.py`; 3 Tests grün
- In-Sample: Servertage 2015–2023, 17 Instrumente, Nominal 0,5 % je ATR
- Vollständige Tabellen: `research/results/e_in_sample.md`

## 1. Ergebnis

**Alle drei Varianten liegen nach Kosten bei null. Die Strategien Nr. 43 und 44 sind damit gescheitert.** Der Hold-out bleibt unberührt, T147–T152 entfallen.

| Kennzahl | E-REV (43) | E-CONT (43) | E-WD (44) |
|---|---|---|---|
| Netto je Tag (bp des Kapitals, Portfolio) | **−0,30** | **−0,06** | **+0,52** |
| vor Kosten je Tag | −0,12 | +0,12 | +1,68 |
| t-Wert (kleinster) | −0,54 | −0,11 | 0,50 |
| Jahre positiv | 2 von 9 | 6 von 9 | 6 von 9 |
| Instrumente positiv | 5 von 17 | 10 von 17 | 7 von 17 |
| Trades (9 Jahre) | 402 | 402 | 3.100 |
| Ø Ergebnis je Trade in ATR vor Kosten / netto | −0,014 / −0,034 | +0,014 / −0,007 | +0,025 / +0,008 |

## 2. Einordnung

- **Nr. 43:** Auf einen Tag mit mehr als 2 ATR folgt im Mittel weder Umkehr noch Fortsetzung, nur ±0,01 ATR. Solche Tage sind selten (≈ 2,6 je Instrument und Jahr), und ihre Folgetage sind reines Rauschen.
- **Nr. 44:** Die rollierende Wahl erkennt teils stabile Muster, etwa US500/US100 Mittwoch Long seit 2018, Brent Montag Short 2016–2020 und USDCHF Montag Long seit 2018. Netto bleibt aber fast nichts: t 0,5, 2017 −19,9 %, 2016 +14,8 %.
- **Datenhinweis:** Mehrere FX-Paare wählen „Montag Long“. Die Montagsrendite (Eröffnung → Schluss) enthält im Sommer die erste Wochenkerze des HistData-Feeds, die in Nr. 42 als Artefakt erkannt wurde. Am Scheitern ändert das nichts.

## 3. Trial-Log (Fortsetzung)

| # | Datum | Test | Ergebnis |
|---|---|---|---|
| T144 | 24.10.2026 | E-REV, In-Sample | nicht bestanden: −0,30 bp/Tag, t −0,54 |
| T145 | 24.10.2026 | E-CONT, In-Sample | nicht bestanden: −0,06 bp/Tag, t −0,11 |
| T146 | 24.10.2026 | E-WD, In-Sample | nicht bestanden: +0,52 bp/Tag, t 0,50 |
| T147–T152 | – | Hold-out, FTMO | entfallen, Hold-out unberührt |
