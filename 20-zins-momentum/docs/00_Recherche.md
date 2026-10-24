# Recherche: Zins-Momentum (Änderung der Zinsdifferenz)

Stand: 24.10.2026

## 1. Idee

Währungen, deren Notenbank in den letzten Monaten stärker gestrafft hat als die anderen, werten im Folgemonat tendenziell weiter auf. Grund: Geldpolitische Zyklen laufen über viele Monate, Märkte unterschätzen ihre Dauer, und die Zinswende zieht Kapital an. Dieser Ansatz unterscheidet sich von Carry (Nr. 6), das auf das **Niveau** des Zinses setzt, und von Momentum (Nr. 7), das auf **Kurse** setzt. Hier zählt die **Änderung** des Zinses.

## 2. Evidenz

| Studie | Ergebnis |
|---|---|
| **Dahlquist & Hasseltoft (2020, *Journal of Financial Economics* 136(1), 152–167)**, „Economic momentum and currency returns“ | Trends in Konjunktur und Inflation (21 Industrieländer, 1976–2017) sagen Währungsrenditen voraus: Long starke, Short schwache „Economic Momentum“, **Sharpe Ratio 0,70**, Alpha gegenüber Carry, Momentum und Value. Erklärung der Autoren: Starke Konjunktur führt zu **geldpolitischer Straffung**, und relative Trends in den Fundamentaldaten bilden Carry ab. |

Quelle: https://econpapers.repec.org/article/eeejfinec/v_3a136_3ay_3a2020_3ai_3a1_3ap_3a152-167.htm

**Hinweis:** Das Paper nutzt Trends in makroökonomischen Größen, nicht Zinsänderungen direkt. Unser Test nimmt die Zinsänderung als messbares Ergebnis dieser Trends (Proxy). Daten zu Konjunktur und Inflation für 8 Länder mit Veröffentlichungsdatum haben wir nicht.

## 3. Was dagegen spricht

1. **Nur 8 Währungen** und davon 2015–2021 fast alle mit Zinsen nahe null, also kaum Bewegung im Signal. Erst 2022–2023 gab es große, unterschiedliche Zinserhöhungen.
2. **Überschneidung** mit Nr. 6 (Carry: Zinsniveau) und Nr. 7 (Kursmomentum). Beide scheiterten auf diesen Währungen.
3. Monatliche FRED-Mittelwerte reagieren mit Verzögerung auf Zinsentscheide.

## 4. Einschätzung vor dem Test

**Erwartung: Scheitern** (Sharpe Ratio unter 0,5). Interessant ist vor allem 2022–2023.
