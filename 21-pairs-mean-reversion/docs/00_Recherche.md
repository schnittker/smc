# Recherche: Pairs Trading / Mean Reversion bei verwandten Währungen

Stand: 24.10.2026

## 1. Idee

Zwei wirtschaftlich eng verbundene Währungen bewegen sich gegen den USD weitgehend gemeinsam. Ihr Verhältnis, der Cross-Kurs, schwankt deshalb in einer Spanne. Weicht der Cross stark vom gleitenden Mittel ab, wird auf die Rückkehr gesetzt.

- **AUD/NZD:** Nachbarländer, ähnliche Rohstoff- und Handelsstruktur, enge Zinsbeziehung
- **EUR/CHF:** Die Schweiz hängt am Euroraum. Bis Januar 2015 galt ein Mindestkurs von 1,20, danach Interventionen der SNB.

## 2. Evidenz

| Quelle | Ergebnis |
|---|---|
| Gatev, Goetzmann & Rouwenhorst (2006, *Review of Financial Studies*), „Pairs Trading“ | Aktienpaare mit enger gemeinsamer Bewegung: Abweichungen von 2 Standardabweichungen kehren zurück, Überrendite 1962–2002; seit den 2000ern stark gesunken |
| FX-spezifisch | keine belastbare Studie zu AUDNZD oder EURCHF gefunden; die Mean Reversion ist vor allem Praktikerwissen |

## 3. Was dagegen spricht

1. **Regimebrüche:** Am 15.01.2015 hob die SNB den Mindestkurs auf, und EURCHF fiel an einem Tag um fast 20 %. Eine Short-Position im z-Score-Signal davor wäre aufgegangen, eine Long-Position hätte das Konto zerstört. Genau solche Brüche sind das Risiko von Mean Reversion.
2. **Trends in den Crosses:** AUDNZD bewegt sich über Monate in Trends, je nach Zinsdifferenz.
3. **Kosten:** Crosses haben höhere Spreads (AUDNZD etwa 1,1 Pip, EURCHF etwa 0,9 Pip) als die Majors.
4. **Überschneidung:** Nr. 3 (Trend) war auf diesen Crosses negativ. Das spricht eher für Mean Reversion, ist aber kein Beleg.

## 4. Einschätzung vor dem Test

**Erwartung: Scheitern am t-Kriterium.** Mean Reversion auf zwei Instrumenten mit seltenen Signalen hat wenig statistische Kraft.
