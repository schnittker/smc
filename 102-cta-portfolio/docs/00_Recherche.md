# Recherche: Multi-Asset-Trendportfolio im CTA-Stil (Strategie Nr. 102)

Stand 25.10.2026. Der Nutzer will einen autonomen Swing-EA, Dauer 6–12 Monate ist ihm egal. Vorschlag nach der Frage „Was wäre eine institutionelle Strategie?“: die Trendfolge der Managed-Futures-Fonds (CTAs), übertragen auf alle FTMO-Klassen mit Daten.

## Prinzip (Hurst/Ooi/Pedersen 2017, „A Century of Evidence on Trend-Following Investing“; Moskowitz/Ooi/Pedersen 2012)

- **Signal:** Vorzeichen der Rendite über 1, 3 und 12 Monate, je Markt
- **Größe:** umgekehrt proportional zur Volatilität. Jeder Markt hat gleiches Risiko, jede Anlageklasse ein Risikobudget.
- **Streuung:** Je Markt Sharpe 0,2–0,4, im Portfolio über viele unkorrelierte Märkte 0,6–1,0
- **Schwächephasen:** Branchenindex (SG Trend) 2011–2013 und 2016–2019 schwach, 2014, 2020 und 2022 stark

## Was in der Reihe schon bekannt ist (offen gelegt, weil es die Erwartung prägt)

| Nr. | Teil | IS 2015–2023 |
|---|---|---|
| 3 | Trend FX (25 Paare) + Gold, 21/63/252 Tage | Sharpe −0,53 |
| 4 | Trend Indizes + Rohstoffe (10 CFDs) | Sharpe −0,37 |
| 101 | Krypto-Trend 7–56 Tage, IS 2018–2023 | K-TSM 0,80, K-LONG 1,18 |
| 14 | US500 Long vola-gesteuert | 0,56; Hold-out 0,59 (in Nr. 100) |

**Folgerung:**
- Ein gleichgewichtetes CTA-Portfolio auf unseren Daten dürfte in-sample scheitern, weil zwei bis drei von vier Klassen negativ waren.
- Eine Walk-Forward-Gewichtung würde mit hoher Wahrscheinlichkeit zu Krypto kippen. Das ist legitim, solange nur Vorjahresdaten in die Entscheidung eingehen. Der Erfolg hinge dann aber an Krypto.

## Datenstand für den Hold-out

- Die Hold-outs von Nr. 3, 4 und 101 sind unberührt.
- US500 und die 7 USD-Majors wurden ab 2024 aber schon in Nr. 100 gesehen (FOMC-Tage, V-VOL). Der Hold-out ist für diese Instrumente daher nicht mehr völlig frisch. Das wird im Ergebnis vermerkt.

## FTMO-Hebel im Swing-Konto (Recherche, im EA zu verifizieren)

| Klasse | Hebel |
|---|---|
| FX | 1:30 |
| Indizes | 1:15 |
| Metalle | 1:9 |
| Energie | angenommen 1:9 |
| Krypto | 1:1 |
