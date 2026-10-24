# Recherche: Monatsend-Rebalancing-Flows am London-Fix

Stand: 24.10.2026

## 1. Mechanismus

Internationale Aktienfonds sichern ihr Währungsrisiko meist mit Forwards ab. Die Absicherung wird einmal im Monat angepasst, zum WM/Reuters-Fix um 16:00 London am letzten Geschäftstag. Grund: Die Benchmark-Indizes (MSCI, FTSE) bewerten mit diesem Fix.

- Ist ein Aktienmarkt im Monat gestiegen, ist das Fremdwährungsexposure der ausländischen Halter größer geworden. Sie verkaufen am Monatsende zusätzlich dessen Währung auf Termin.
- **Folge:** Die Währung des Marktes, der im Monat besser lief, wertet in der Zeit vor dem Monatsend-Fix ab. Das gilt auch für den USD, wenn US-Aktien besser liefen.
- Der Druck ist vorübergehend. Nach dem Fix kehrt sich ein Teil der Bewegung um.

## 2. Evidenz

**Melvin, M. & Prins, J. (2015): „Equity hedging and exchange rates at the London 4 p.m. fix“**, *Journal of Financial Markets* 22, 50–72, doi:10.1016/j.finmar.2014.11.001. Working Paper 2012: https://ssrn.com/abstract=2019274

- **Daten:** 10 Hauptwährungen, 2004–2012
- **Regression:** Wechselkursrendite von 15:00 bis 16:00 London am letzten Tag des Monats auf die relative Aktienrendite des Monats (erster bis vorletzter Tag)
- **Ergebnis:** Steigung −0,0142 (Panel, R² 0,03, p < 0,01). 10 % relative Outperformance bringen also etwa 14 bp Abwertung in der Stunde vor dem Fix, also etwa 1,4 bp je Prozentpunkt.
- **Umkehr:** Ein Teil der Bewegung kehrt bis zum Mittag des Folgetags um.
- **Volatilität:** Am Monatsend-Fix ist die Wechselkursvolatilität erhöht.
- Eine Handelsstrategie mit Kosten rechnet das Paper nicht.

Hinweis: Die Details zur Regression stammen aus einer Zusammenfassung der ECB-Workshop-Fassung (2013), siehe https://github.com/DougOscar/DataScienceAndTrading/issues/27. Den Volltext haben wir nicht geprüft.

**Weitere Belege und Einordnung**
- Krohn, Mueller & Whelan (2024, *Journal of Finance*): USD-Muster um die täglichen Fixings. Dieses Muster hat Modell F (P5 im SMC-Projekt) reproduziert, allerdings nur in Höhe der Kosten.
- Chinn, Ito & McCauley (2022, *JIMF*) und Evans (2018) zum WMR-Fix: Seit Februar 2015 ist das Fix-Fenster 5 statt 1 Minute lang (15:57:30–16:02:30). Außerdem gibt es seit 2014/15 Strafverfahren gegen Fix-Manipulation.

## 3. Was dagegen spricht

1. **Bekanntheit:** Banken veröffentlichen seit Jahren Tage vorher Schätzungen der Monatsend-Flows. Wer sie handelt, positioniert sich früher, und der Effekt in der letzten Stunde kann kleiner werden.
2. **Fix-Reform 2015:** Das breitere Fenster verteilt die Fix-Orders und dämpft den Preisdruck.
3. **Größe:** Eine typische relative Monatsrendite von 3 % ergibt laut Paper etwa 4 bp Bewegung. Die FTMO-Kosten liegen bei etwa 1–1,5 bp je Position, am Fix wegen breiterer Spreads eher mehr.
4. **Wenige Beobachtungen:** Es gibt ein Ereignis pro Monat, also 108 im In-Sample 2015–2023. Für einen t-Wert ≥ 3 braucht es eine Sharpe Ratio von etwa 1,0 p. a.

## 4. Einschätzung vor dem Test

- **Vorteil gegenüber Modell F:** Der erwartete Effekt je Ereignis ist ein Mehrfaches der Kosten. Bei F lag er nur auf Höhe der Kosten.
- **Nachteil:** sehr wenige Ereignisse, Reformen des Fixes und eine starke Verbreitung der Idee.
- **Für FTMO allein ungeeignet,** selbst wenn der Effekt trägt:
  - Ein Trade-Fenster pro Monat reicht kaum, um +10 % und +5 % in 6 Monaten zu erreichen, ohne die 5-%-Tagesgrenze zu reißen.
  - Die Strategie ist eher ein Baustein für ein Ensemble (Nr. 100 der Strategieliste).
- **Erwartung: eher Scheitern** (t < 3), Effekt vor Kosten vermutlich sichtbar, aber kleiner als im Paper.
