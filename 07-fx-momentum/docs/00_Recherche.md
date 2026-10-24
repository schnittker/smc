# Recherche: FX Querschnitts-Momentum

Stand: 24.10.2026

## 1. Mechanismus

Währungen, die im letzten Monat (bzw. im letzten Jahr) gegenüber den anderen am stärksten gestiegen sind, steigen im Folgemonat im Mittel weiter, die schwächsten fallen weiter. Anders als bei Zeitreihen-Momentum (Nr. 3) zählt die **relative** Stärke: Das Portfolio ist immer Long die Gewinner und Short die Verlierer, unabhängig von der allgemeinen Richtung.

Erklärung laut Literatur: Unter- und Überreaktion der Investoren sowie Grenzen der Arbitrage. Ein Risikofaktor erklärt die Renditen nicht.

## 2. Evidenz

| Studie | Ergebnis |
|---|---|
| Menkhoff, Sarno, Schmeling & Schrimpf (2012, *Journal of Financial Economics* 106, 660–684), „Currency momentum strategies“ | Spread der Überschussrenditen zwischen Gewinner- und Verliererwährungen **bis 10 % p. a.**; kaum korreliert mit Carry und mit technischen Handelsregeln; Kosten erklären ihn nicht vollständig; „effective limits to arbitrage“ |
| Asness, Moskowitz & Pedersen (2013, *Journal of Finance*), „Value and Momentum Everywhere“ | 12-1-Monats-Momentum in G10-Währungen mit positiver, aber kleiner Sharpe Ratio (Größenordnung 0,2–0,4) |

**Aus dem Gedächtnis, nicht am Volltext geprüft** (Volltext: https://openaccess.city.ac.uk/id/eprint/3296/1/Currency%20Momentum%20Strategies.pdf):
- Stichprobe etwa 48 Währungen 1976–2010.
- Am stärksten bei kurzer Formations- und Haltedauer (1 Monat / 1 Monat).
- Bei Industrieländern schwächer, konzentriert auf kleine Währungen mit hoher idiosynkratischer Volatilität und Länderrisiko, die hohe Spreads haben.

## 3. Was dagegen spricht

1. **Nur 8 Hauptwährungen:** Genau dort ist der Effekt laut Literatur am schwächsten. Die kleinen, illiquiden Währungen, die ihn tragen, gibt es bei FTMO nicht.
2. **Verwandt mit Nr. 3:** Zeitreihen-Momentum auf denselben Paaren war 2015–2023 schon vor Kosten negativ (Sharpe −0,18). Querschnitts-Momentum ist ein anderer Effekt, profitiert aber von denselben anhaltenden Trends.
3. **Alter des Effekts:** Die Studien reichen bis 2010. Danach gelten Momentum-Renditen in Währungen allgemein als schwach.

## 4. Einschätzung vor dem Test

- Kosten sind bei monatlicher Umschichtung gering.
- **Erwartung: Scheitern** (Sharpe Ratio um 0), wegen des kleinen Universums und des Ergebnisses von Nr. 3.
- Getestet wird trotzdem, weil die Strategie die nächste auf der Liste ist und die Engine von Nr. 6 fast unverändert passt.
