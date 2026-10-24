# Recherche: Hurst-Regime-Switch

Stand: 24.10.2026

## 1. Idee

Der Hurst-Exponent H misst die Persistenz einer Zeitreihe: H > 0,5 bedeutet trendend, H < 0,5 mean-reverting, H = 0,5 Random Walk. Ein Regime-Switch handelt im Trendregime eine Trendfolgeregel und im Umkehrregime eine Mean-Reversion-Regel. So sollen die Verluste vermieden werden, die jede Regel allein im falschen Regime erleidet.

## 2. Quellen

| Quelle | Inhalt |
|---|---|
| Hurst (1951); Mandelbrot & Wallis (1969) | R/S-Analyse, Langzeitgedächtnis |
| Lo (1991), *Econometrica* | Modifizierte R/S-Statistik: Viele „Hurst-Befunde“ in Finanzdaten verschwinden nach Korrektur für Kurzzeit-Abhängigkeit. |
| Taqqu, Teverovsky & Willinger (1995) | Schätzer im Vergleich, z. B. aggregierte Varianz; große Stichprobenfehler bei kurzen Fenstern |
| Praxis (Chan 2013, Kap. 2) | Hurst und Variance Ratio als Regime-Filter |

## 3. Einschätzung vor dem Test

- Beide Bausteine sind einzeln gescheitert: Keltner-Ausbruch (Nr. 38) vor Kosten +0,03 R, Bollinger-Fade (Nr. 37) +0,01 R vor Kosten bei hohen Kosten.
- Ein Regime-Filter kann helfen, wenn H Regimes vorhersagt. Laut Lo (1991) ist H aus kurzen Fenstern aber kaum von 0,5 unterscheidbar.
- **Erwartung: Scheitern.**
