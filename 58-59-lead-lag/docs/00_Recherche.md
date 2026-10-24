# Recherche: Lead-Lag (US500 → AUDJPY, US-Renditen → USDJPY)

Stand: 24.10.2026

## 1. Idee

- **Nr. 58:** AUDJPY ist das klassische Risk-on/Risk-off-Paar. Bewegt sich US500 stark, zieht AUDJPY mit Verzögerung nach, weil FX-Händler langsamer auf Aktienimpulse reagieren.
- **Nr. 59:** USDJPY folgt der Zinsdifferenz USA–Japan, und der japanische Zins war 2015–2023 nahe null. Steigt die 10-jährige US-Rendite, sollte USDJPY nachziehen.

## 2. Quellen

| Quelle | Inhalt |
|---|---|
| Hong, Torous & Valkanov (2007), *JFE*; Rapach, Strauss & Zhou (2013) | Lead-Lag zwischen Märkten auf Monatsbasis |
| Cespa, Gargano, Riddiough & Sarno (2022) | Kurzfristige Lead-Lag-Effekte zwischen Aktien und FX, intraday schnell arbitragiert |
| Engel & West (2005); Praxis zu USDJPY | Starker gleichzeitiger Zusammenhang Zins ↔ USDJPY, aber kaum verzögert |

## 3. Daten

- **DGS10** (10-jährige US-Staatsanleihe, konstante Laufzeit, täglich) von FRED, `data/raw/DGS10.csv`, heruntergeladen am 24.10.2026 (`curl`). Gitignored, Neuaufbau mit `scripts/download_dgs10.sh`.
- In MT5 ist der Wert nur per WebRequest live verfügbar (⚠ wie in der Liste vermerkt).

## 4. Bezug zu früheren Tests

- **Nr. 23 (Rohstoff-Lead-Lag):** Nur der gleichzeitige Zusammenhang existierte, kein verzögerter.
- **Nr. 20 (Zins-Momentum):** Kurzfristzinsen, monatlich; gescheitert.

## 5. Einschätzung vor dem Test

**Erwartung: Scheitern aller drei Varianten.**
