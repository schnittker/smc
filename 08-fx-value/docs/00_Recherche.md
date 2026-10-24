# Recherche: FX Value (Kaufkraftparität), Strategie Nr. 8

Stand: 24.10.2026 (nachgeholt; zurückgestellt an Tag 4, weil CPI-Daten fehlten)

## 1. Idee

Währungen, die real (inflationsbereinigt) stark abgewertet haben, sind „billig“ und werten langfristig wieder auf. Teure Währungen werten ab. Gehandelt wird im Querschnitt der G8: Long die billigsten, Short die teuersten.

## 2. Evidenz

| Quelle | Inhalt |
|---|---|
| Asness, Moskowitz & Pedersen (2013), *J. Finance* | FX-Value (5-Jahres-Änderung des realen Wechselkurses) mit positiver Prämie 1979–2011, negativ korreliert mit Momentum |
| Menkhoff, Sarno, Schmeling & Schrimpf (2017), *RFS* | Value in FX existiert, ist aber großteils durch Fundamentaldaten erklärt; schwankend |
| Rogoff (1996) | PPP-Halbwertszeit 3–5 Jahre |

## 3. Daten (FRED, Download 24.10.2026, `data/raw/`, Neuaufbau mit `research/scripts/download_fred.sh`)

| Reihe | Inhalt | Lücke |
|---|---|---|
| CPIAUCSL, CP0000EZ19M086NEST, GBR/CAN/CHE…MINMEI | Monats-CPI US, Euroraum (HICP), UK, Kanada, Schweiz | OECD-Reihen enden 2025 |
| AUS/NZL…QINMEI | Quartals-CPI Australien, Neuseeland | |
| JPNCPIALLMINMEI | Monats-CPI Japan | **endet 06/2021** (OECD liefert danach keine Monatswerte; auch die OECD-SDMX-API nicht) |
| FPCPITOTLZGJPN | Jahresinflation Japan (Weltbank) | zur Fortschreibung ab 07/2021 |
| DEXUSEU … DEXSZUS | Tageskurse (Mittagskurs New York) | EUR ab 1999 |

**Japan ab 07/2021:** Der CPI wird mit der Jahresinflation des Vorjahres monatlich fortgeschrieben. Der Vorjahreswert ist damit zum Zeitpunkt der Verwendung bekannt. Für eine 5-Jahres-Änderung ist der Fehler klein.

## 4. Bezug zu früheren Tests

FX Carry (Nr. 6) und FX-Momentum (Nr. 7, inkl. 12-Monats-Umkehr X-12) sind mit derselben Portfolio-Engine gescheitert. Nr. 7 X-12 hatte Sharpe −0,81. Value ist nicht unabhängig von der Langfrist-Umkehr.

## 5. Einschätzung vor dem Test

**Erwartung: Scheitern beider Varianten.**
