# Ergebnisse Strategie Nr. 12 – Modell N „Overnight-Drift US500“

Stand: 24.10.2026

Grundlagen:
- Regeln: unverändert aus der Vorregistrierung `docs/01_Vorregistrierung.md` (Commit `9eca529`)
- Code: `research/ovn/`, Lauf `research/scripts/run_n.py` (Commit `7636eba`); 4 Tests grün
- In-Sample: NYSE-Handelstage 2015–2023, US500
- Vollständige Tabellen: `research/results/n_in_sample.md`
  - Nach dem Lauf wurde nur die Darstellung des Swap-Anteils korrigiert: Er erschien mit negativem Vorzeichen, gemeint sind Kosten. Die Zahlen sind unverändert.

## 1. Ergebnis

**Alle drei Varianten verfehlen das Hauptkriterium deutlich. Strategie Nr. 12 ist damit gescheitert.** Der Hold-out 2024–2026 bleibt unberührt, T46 und T47 entfallen.

| Kriterium | Schwelle | N-NACHT (16:00–09:30) | N-EU (02:00–03:00) | N-EU-DOWN (nach Verlusttag) |
|---|---|---|---|---|
| Netto je Trade | > 0 | +0,22 bp | **−0,51 bp** | **−0,10 bp** |
| t-Wert (kleinster aus iid, Woche, Monat) | ≥ 3,0 | **0,14** | **−1,54** | **−0,18** |
| Jahre positiv | ≥ 6 von 9 | **5 von 9** | **2 von 9** | **3 von 9** |
| Teilzeiträume | beide > 0 | +0,11 / +0,36 | **−0,47 / −0,56** | **−0,19** / +0,02 |
| bei doppelten Kosten | > 0 | **−1,70 bp** | **−1,64 bp** | **−1,23 bp** |
| vor Kosten je Trade | – | +2,14 bp | +0,63 bp | +1,04 bp |
| Kosten je Trade (davon Swap) | – | 1,92 bp (0,79) | 1,13 bp (0) | 1,13 bp (0) |

## 2. Einordnung

1. **Die Nacht verdient die Prämie, aber kaum mehr als die Kosten.**
   - N-NACHT bringt vor Kosten +2,1 bp je Nacht, also etwa 5 % p. a. Spread, Slippage und Index-Swap kosten zusammen 1,9 bp.
   - Intraday (09:30–16:00) wäre vor Kosten mit +2,6 bp sogar etwas besser (beschreibend). Die Aufteilung „die Prämie entsteht nur nachts“ aus Cliff et al. (1993–2006) gilt 2015–2023 für US500 also nicht.
2. **Das Fenster zur Eröffnung in Europa ist schon 2015–2023 schwach und seit 2021 null.**
   - N-EU bringt vor Kosten +0,6 bp je Nacht (Paper: etwa 1,5 bp für 1998–2022).
   - 2021–2023: vor Kosten −0,1 bp. Das bestätigt den Befund der Autoren („The Disappearing Overnight Drift“, 2026).
   - Nach Verlusttagen (+1,0 bp vor Kosten) ist der Effekt etwas größer als nach Gewinntagen (+0,4 bp), wie im Paper. Er liegt aber unter den Kosten von 1,1 bp.
3. **US100 ist etwas stärker** (N-NACHT +3,5 bp vor Kosten, N-EU-DOWN +1,6 bp), netto aber ebenfalls weit von t ≥ 3 entfernt (t 0,8 bzw. 1,1).
4. **Datenhinweis:** 2023 enthält bei N-NACHT nur 164 Nächte (HistData-Lücke März bis Juli 2023). Das Urteil hängt daran nicht.

## 3. Folgerung

Dieselbe Hürde wie bei Nr. 2, 5, 9, 10 und 11: Der Effekt ist vor Kosten vorhanden, aber in der Größenordnung der FTMO-Kosten. Bei einer Haltedauer von einer Stunde bis einer Nacht und einem Index-CFD mit etwa 1,1 bp Round-Trip-Kosten plus Swap fehlt die Marge.

## 4. Trial-Log (Fortsetzung)

| # | Datum | Test | Ergebnis |
|---|---|---|---|
| T43 | 24.10.2026 | N-NACHT, In-Sample | nicht bestanden: +0,22 bp/Nacht, t 0,14 |
| T44 | 24.10.2026 | N-EU, In-Sample | nicht bestanden: −0,51 bp, t −1,54 |
| T45 | 24.10.2026 | N-EU-DOWN, In-Sample | nicht bestanden: −0,10 bp, t −0,18 |
| T46 | – | Hold-out | entfällt, Hold-out unberührt |
| T47 | – | FTMO-Bootstrap | entfällt |

Teilzeitraum ab 2021, Gewinntage, Intraday-Vergleich und US100 sind beschreibende Diagnosen, keine neuen Trials.
