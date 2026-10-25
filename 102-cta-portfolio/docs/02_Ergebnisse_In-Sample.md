# Ergebnisse In-Sample: Modell C (Strategie Nr. 102)

Lauf vom 25.10.2026, vollständige Tabellen in `research/results/c_in_sample.md`.

| | C-FIX (Standard-CTA) | C-WF (Walk-Forward) |
|---|---|---|
| Netto je Tag | +0,35 bp | +1,46 bp |
| Sharpe p. a. | 0,09 | 0,26 |
| t (kleinster) | 0,25 | 0,77 |
| Jahre positiv | 6 von 9 | 2 von 9 |
| Klassen positiv | 2 von 4 | 1 von 4 |
| doppelte Kosten | −0,84 bp | −0,50 bp |
| Kosten + Swaps p. a. | 4,4 % | 7,1 % |

**Beide nicht bestanden.** Der Hold-out bleibt unberührt.

**Klassen (C-FIX, netto p. a.):**

| Klasse | netto p. a. |
|---|---|
| FX | −0,9 % |
| Indizes | +2,1 % |
| Rohstoffe | −1,0 % |
| Krypto | +1,1 % |

## Einordnung

- **Die klassische CTA-Trendfolge verdient 2015–2023 auf FTMO-Konditionen fast nichts.**
  - Vor Kosten bringt sie etwa 5 % p. a. bei 15 % Vola (Sharpe ~0,35); Kosten und Swaps nehmen davon 4,4 Prozentpunkte.
  - Das passt zur Branche: Der SG Trend Index lag 2015–2019 nahe null bzw. negativ und hatte nur 2020 und 2022 gute Jahre.
- **Walk-Forward hilft nicht.**
  - Die jährliche Neuwahl jagt der Vergangenheit hinterher: 2016 FX und Indizes hoch gewichtet, die 2016 verloren; ab 2020 fast alles auf Krypto, das 2022/23 verlor.
  - Das ist das typische Ergebnis von Parameter- und Gewichtsoptimierung bei schwachen Signalen: Die gestern beste Einstellung ist morgen nicht besser als die Standardeinstellung.
- **Gegen Nr. 101:** Die schnelle Krypto-Trendfolge (7–56 Tage) war dort deutlich stärker als die CTA-Rückblicke (1–12 Monate). Hier steuert Krypto nur 25 % des Risikos bei, und die übrigen Klassen verwässern das Ergebnis.
