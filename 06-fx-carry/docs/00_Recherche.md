# Recherche: FX Carry

Stand: 24.10.2026

## 1. Mechanismus

Die ungedeckte Zinsparität sagt: Hochzinswährungen sollten im Mittel so stark abwerten, wie ihr Zinsvorteil beträgt. Empirisch tun sie das nicht (Forward-Premium-Puzzle).

- **Carry Trade:** Long in Hochzinswährungen, Short in Niedrigzinswährungen. Der Zinsvorteil wird kassiert, der Wechselkurs schwankt um null oder läuft sogar mit.
- **Risiko:** seltene, heftige Crashs, wenn sich Carry-Positionen in Krisen auflösen (Oktober 2008, August 2015, März 2020, August 2024).
- **Bei FTMO** fließt der Zinsvorteil über die täglichen Swaps, abzüglich eines Broker-Aufschlags.

## 2. Evidenz

| Studie | Ergebnis |
|---|---|
| Lustig, Roussanov & Verdelhan (2011, *Review of Financial Studies*), „Common Risk Factors in Currency Markets“ | Carry-Portfolios (Long hohe, Short niedrige Zinsen), 1983–2009: Sharpe Ratio etwa 0,5–0,9 vor Kosten; ein gemeinsamer Risikofaktor (HML_FX) erklärt die Renditen |
| Menkhoff, Sarno, Schmeling & Schrimpf (2012, *Journal of Finance*), „Carry Trades and Global Foreign Exchange Volatility“ | Carry-Renditen sind Prämie für globales FX-Volatilitätsrisiko; Verluste in Phasen steigender Volatilität |
| Brunnermeier, Nagel & Pedersen (2008, *NBER Macroeconomics Annual*), „Carry Trades and Currency Crashes“ | negative Schiefe; Crashs bei Liquiditätsengpässen |
| Daniel, Hodrick & Lu (2017, *Critical Finance Review*), „The Carry Trade: Risks and Drawdowns“ | Dollar-neutrale G10-Carry-Portfolios haben deutlich geringere Sharpe Ratios als gleichgewichtete; lange Drawdowns |

## 3. Was dagegen spricht

1. **Zinsniveau 2015–2021:** Fast alle G10-Zinsen lagen nahe null oder darunter. Die Zinsdifferenzen waren klein, oft 1–2 % p. a. zwischen AUD/NZD und JPY/CHF/EUR. Erst 2022–2023 wurden sie groß (USD ≈ 5 %, JPY ≈ 0 %).
2. **Swap-Aufschlag:** Bei FTMO zahlt jede Position einen Aufschlag (Annahme wie im SMC-Projekt: 1 % p. a. je Position). Bei einer Differenz von 1,5 % bleibt davon wenig. Wird ein Cross über zwei USD-Paare gebaut, fällt der Aufschlag doppelt an.
3. **Eigene Einschätzung, nicht getestet:** G10-Carry-Indizes der Banken lagen 2008–2020 netto etwa bei null. Die guten Jahre waren 2021–2023.
4. **G8 statt G10:** SEK und NOK fehlen bei FTMO, wir haben nur 8 Währungen.

## 4. Einschätzung vor dem Test

- **Vorteil gegenüber den bisherigen Tests:** Carry ist der am besten belegte FX-Faktor, und die Handelskosten sind bei monatlicher Umschichtung gering.
- **Nachteil:** schwache Zinsdifferenzen im größten Teil des In-Sample, Swap-Aufschläge und Crashrisiko gegenüber der 5-%-Tagesgrenze.
- **Erwartung: eher Scheitern** (Sharpe Ratio unter 0,5), gute Ergebnisse vor allem 2022–2023.
