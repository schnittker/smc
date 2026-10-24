# Recherche: H1-Mean-Reversion auf FX-Crosses (Bollinger, z-Score/OU)

Stand: 24.10.2026

## 1. Idee

Crosses ohne USD, z. B. EURCHF, AUDNZD oder AUDCAD, bewegen sich oft in Spannen, weil die beiden Volkswirtschaften ähnlich laufen. Kurzfristige Ausschläge vom gleitenden Mittel sollten zurücklaufen.

- **Nr. 37 Bollinger Mean Reversion:** Schluss außerhalb der Bänder in einer Seitwärtsphase (ADX niedrig) → Gegenposition bis zur Mittellinie.
- **Nr. 39 z-Score / Ornstein-Uhlenbeck:** Abstand zum Mittel in Standardabweichungen. Gehandelt wird nur, wenn die geschätzte Halbwertszeit der Rückkehr kurz ist.

## 2. Quellen

| Quelle | Inhalt |
|---|---|
| Bollinger (2001) | Bandberührungen in Seitwärtsmärkten als Umkehrsignal, nicht in Trends |
| Wilder (1978) | ADX als Trendstärke; < 20 = kein Trend |
| Chan (2013), *Algorithmic Trading*, Kap. 2 | OU-Halbwertszeit −ln 2 / λ aus der Regression Δx auf x(t−1); Lookback ≈ Halbwertszeit |

## 3. Bezug zu früheren Tests

- **Nr. 32 (Asien-Range-Fade, M5):** Die Mean Reversion war vor Kosten deutlich (+0,05 bis +0,12 R), die Kosten waren aber zwei- bis siebenmal größer. Auf H1 sind die Ausschläge größer (typisch 20–60 Pips gegenüber 5–10 Pips), die Kosten relativ also kleiner.
- **Nr. 21 (Pairs Mean Reversion, D1):** Sharpe 0,13 / −0,20.

## 4. Einschätzung vor dem Test

Möglich, aber unsicher: Die Crosses haben 0,6–2 Pip Spread, und das Umfeld ab 2022 (Zinsdivergenz, Trends) war ungünstig. **Erwartung: Scheitern, mit etwas Restchance bei R-BB.**
