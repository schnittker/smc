# Recherche: Placebo-Kontrollen (Nr. 98 Zufalls-Einstiege, Nr. 99 Mondphasen)

Stand: 24.10.2026

## 1. Zweck

Die Pipeline (Daten, Kosten, Statistik, Akzeptanzkriterien) wird mit Regeln ohne ökonomische Begründung kalibriert. Sie sollen mit hoher Wahrscheinlichkeit scheitern:
- **Nr. 98 Zufalls-Einstiege:** Gleiche Engine und Kosten wie Nr. 50/51, aber Einstiege per Zufallsgenerator. Vor Kosten muss ≈ 0 herauskommen, nach Kosten ≈ −Kosten. Wäre das Ergebnis vor Kosten deutlich positiv, hätte die Engine einen Fehler oder eine Datenverzerrung, z. B. Zukunftsinformation oder ein Ziel-/Stop-Bias.
- **Nr. 99 Mondphasen:** Long zwischen Neumond und Vollmond, Short zwischen Vollmond und Neumond. Yuan, Zheng & Zhu (2006, *J. Empirical Finance*) finden niedrigere Aktienrenditen um den Vollmond. Das ist ökonomisch unbegründet und dient als zweite Kontrolle.

## 2. Bedeutung für die Reihe

Mit 0 bestandenen von ≈ 130 Versuchen ist bereits sichtbar, dass die Kriterien streng sind. Die Placebos zeigen zusätzlich, ob die Pipeline nach Kosten systematisch zu negativ rechnet:
- Zufall vor Kosten ≈ 0 (nicht deutlich negativ)
- nach Kosten genau um die Kosten negativ

## 3. Erwartung

Beide scheitern. PL-RANDOM: Ø R vor Kosten im Bereich ±0,01, nach Kosten ≈ −Kosten je Trade.
