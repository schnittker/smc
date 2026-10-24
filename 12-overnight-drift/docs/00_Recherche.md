# Recherche: Overnight-Rendite bei US-Aktienindizes

Stand: 24.10.2026

## 1. Effekt

Ein großer Teil der US-Aktienrendite entsteht außerhalb der Handelszeit, zwischen Schluss (16:00 New York) und Eröffnung (09:30). Neuere Arbeiten verorten ihn noch enger: in der Stunde, in der Europa öffnet (02:00–03:00 New York).

## 2. Evidenz

| Studie | Ergebnis |
|---|---|
| Cliff, Cooper & Gulen (2008), „Return differences between trading and non-trading hours: like night and day“ | US-Aktien/ETFs 1993–2006: die Prämie entsteht über Nacht, intraday nahe null oder negativ |
| Lou, Polk & Skouras (2019, *Journal of Financial Economics*), „A tug of war: overnight versus intraday expected returns“ | systematische Unterschiede zwischen Overnight- und Intraday-Renditen über viele Anomalien |
| **Boyarchenko, Larsen & Whelan (2023, *Review of Financial Studies* 36(9), 3502–3547)**, „The Overnight Drift“ | S&P-500-E-mini 1998–2022: fast die gesamte Prämie entfällt auf **02:00–03:00 New York** (Eröffnung Europa), etwa 3,7 % p. a.; Ursache: Händler bauen ihr Inventarrisiko ab; **asymmetrisch: nach Kursverlusten am Vortag starke positive Overnight-Umkehr**, nach Gewinnen kaum |
| Bondarenko & Muravyev (2023) | alternative Erklärung: Auflösung von Unsicherheit bei Eröffnung in Europa |
| **Boyarchenko, Larsen & Whelan (2026, Liberty Street Economics)**, „The Disappearing Overnight Drift“ | **das 02:00–03:00-Fenster liegt seit 2021 im Mittel nahe null** |

Quellen: https://academic.oup.com/rfs/article-abstract/36/9/3502/7076616, https://libertystreeteconomics.newyorkfed.org/2026/07/the-disappearing-overnight-drift/

## 3. Was dagegen spricht

1. **Größe gegen Kosten:**
   - 3,7 % p. a. entsprechen etwa 1,5 bp pro Nacht. Ein Round Trip kostet bei FTMO etwa 1,6 bp.
   - Die ganze Nacht bringt mehr (die ganze Aktienprämie, etwa 3–4 bp pro Nacht). Dafür fällt jede Nacht der Index-Swap an (Dividende − USD-Zins − 2,5 %, also etwa −0,7 bis −1,6 bp pro Nacht) und montags der Wochenend-Swap.
2. **Verschwinden seit 2021**, laut den Autoren selbst. Das betrifft die letzten 3 Jahre unseres In-Sample.
3. **Schwankung:** Eine Nacht schwankt um etwa 50–70 bp. Selbst bei 2.200 Nächten reicht ein Effekt von 2 bp netto nur für t ≈ 1,5–2.

## 4. Einschätzung vor dem Test

- **Erwartung: Scheitern** aller drei Varianten am t-Kriterium.
- Am ehesten trägt die Variante „nur nach Verlusttagen“. Der Effekt je Trade ist dort größer, und die Bedingung stammt aus dem Paper, nicht aus unseren Daten.
