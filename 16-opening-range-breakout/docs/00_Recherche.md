# Recherche: Opening Range Breakout (ORB) bei US-Indizes

Stand: 24.10.2026

## 1. Idee

Die erste Handelsminuten nach der Kassaeröffnung (09:30 New York) zeigen die Richtung des Tages an. Gehandelt wird in Richtung der ersten Kerze mit engem Stop am Gegenende der Kerze und weitem Ziel. Am Tagesende wird geschlossen.

## 2. Evidenz

| Quelle | Ergebnis |
|---|---|
| **Zarattini & Aziz (2023, SSRN 4416622)**, „Can Day Trading Really Be Profitable? Evidence of Sustainable Long-term Profits from Opening Range Breakout (ORB) Day Trading Strategy vs. Benchmark in the US Stock Market“ | QQQ 2016–2023, 5-Minuten-ORB: Richtung der ersten 5-Minuten-Kerze, Einstieg zur Eröffnung der zweiten, Stop am Hoch/Tief der ersten, Ziel 10 R, sonst Schluss um 16:00; Risiko 1 % je Trade, Hebel ≤ 4. Laut Paper deutlich bessere Rendite als Buy-and-hold und hohe Sharpe Ratio, auch nach Kommissionen. **Arbeitspapier ohne Peer-Review.** |
| Zarattini, Barbon & Aziz (2024), „A Profitable Day Trading Strategy for the U.S. Equity Market“ | ORB auf „Stocks in Play“ (Einzelaktien mit hohem relativem Volumen); für Indizes allein schwächer |

## 3. Was dagegen spricht

1. **Kein Peer-Review, viel Medienecho.** Die Regel ist seitdem weit verbreitet.
2. **CFD statt ETF:** HistData-Kurse für US100 sind Bid-Kurse eines rund um die Uhr gehandelten Kontrakts. Die „erste 5-Minuten-Kerze“ ab 09:30 ist dort eine normale Kerze im fortlaufenden Handel, keine Eröffnungsauktion. Die Dynamik der Kassaeröffnung bildet sie nur ungefähr ab.
3. **Enger Stop:** Die erste Kerze ist oft klein. Spread (≈ 1 bp) und Slippage sind gemessen am Risiko R erheblich und an Tagen mit kleiner Kerze ein großer Anteil.
4. **Trefferquote typisch unter 25 %:** Der Ertrag hängt an wenigen großen Trendtagen. Das ist anfällig für Zufall und für die Kosten.

## 4. Einschätzung vor dem Test

- **Erwartung: Scheitern**, weil CFD-Kurse und Kosten die kleine Opening Range verwässern.
- Bei Erfolg wäre die Strategie für FTMO gut geeignet: täglicher Handel, festes Risiko je Trade, geschlossen über Nacht.
