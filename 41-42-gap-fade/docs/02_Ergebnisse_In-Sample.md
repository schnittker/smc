# Ergebnisse Strategien Nr. 41 und 42 – Modell Q „Gap-Fade“

Stand: 24.10.2026

Grundlagen:
- Regeln: unverändert aus der Vorregistrierung `docs/01_Vorregistrierung.md` (Commit `1e86b7d`)
- Code: `research/gap/`, Lauf `research/scripts/run_q.py`; 5 Tests grün
- Robustheitsprüfung: `research/scripts/check_q_fxw.py`
- In-Sample: 2015–2023, 0,25 % Risiko je Trade
- Tabellen: `research/results/q_in_sample.md`, `research/results/q_fxw_robustheit.md`

## 1. Ergebnis

- **Q-IDX (Nr. 41) ist gescheitert:** −3,15 bp je Tag, t −3,61, 0 von 9 Jahren positiv.
- **Q-FXW (Nr. 42) erfüllt formal alle vorregistrierten In-Sample-Kriterien.** Es ist der erste solche Fall in der Reihe.
- Die Robustheitsprüfung zeigt aber, dass der gesamte Ertrag aus einem **Artefakt des HistData-Feeds** stammt (Abschnitt 2). **Q-FXW wird deshalb verworfen.** Der Hold-out bleibt unberührt, weil er auf derselben Datenquelle mit demselben Artefakt nichts entscheiden könnte. T140–T143 entfallen.

| Kennzahl | Q-IDX (41) | Q-FXW (42) |
|---|---|---|
| Netto je Tag bzw. Montag (bp des Kapitals) | **−3,15** | **+11,88** |
| vor Kosten | +1,13 | +17,92 |
| Kosten | 4,28 | 6,04 |
| t-Wert (kleinster) | −3,61 | 5,08 |
| Jahre positiv | 0 von 9 | 9 von 9 |
| Instrumente positiv | 1 von 4 | 7 von 7 |
| bei doppelten Kosten | −7,43 | +5,84 |
| Trades (9 Jahre) | 6.069 | 1.042 |
| Ø R je Trade vor Kosten / netto | +0,017 / −0,047 | +0,312 / +0,207 |
| Ausstiege Ziel / Stop / Zeit | 43 % / 43 % / 14 % | 64 % / 31 % / 4 % |

## 2. Warum Q-FXW verworfen wird

**Befund 1: Der Ertrag hängt an genau einer Uhrzeit.** Mit derselben Regel und anderen Einstiegszeiten am Server-Montag ergibt sich:

| Einstieg | 00:05 | 00:30 | **01:00** | 02:00 | 04:00 | 09:00 |
|---|---|---|---|---|---|---|
| Netto bp je Montag | +2,0 | −2,5 | **+11,9** | −0,9 | −8,2 | −10,1 |

Ein echter Wochenend-Effekt würde sich nicht innerhalb einer Stunde auf null abbauen und eine halbe Stunde vorher nicht fehlen.

**Befund 2: Ursache ist die Zeitzone des Feeds.** HistData stempelt in fester EST (UTC−5, ohne Sommerzeit). Im Sommer beginnt die Woche dort erst um 17:00 EST, also 18:00 EDT bzw. 01:00 Server; die erste Handelsstunde fehlt. Im Winter beginnt der Feed um 00:00 Server. Auf dem FTMO-Server beginnt der Handel ganzjährig um 00:00 Server.

| Teilmenge | Trades | Netto bp/Montag | t | Ø R vor Kosten | Füllquote |
|---|---|---|---|---|---|
| Sommer: 01:00 = **erste Kerze der Woche im Feed** | 703 | **+20,2** | +8,9 | +0,457 | 72 % |
| Winter: 01:00 = 1 h nach Eröffnung (wie auf FTMO) | 339 | **−5,1** | −1,4 | +0,009 | 48 % |
| Sommer: Einstieg 02:00 = 1 h nach der ersten Kerze | 525 | +2,0 | +1,0 | +0,154 | 55 % |

Der Ertrag stammt also vollständig aus dem ersten Kurs der Woche im HistData-Feed. Dieser Kurs liegt ungewöhnlich weit vom Freitagsschluss entfernt und läuft danach zurück. Das ist ein Merkmal des Feeds, kein handelbarer Effekt. Auf dem FTMO-Server ist 01:00 immer eine Stunde nach der Eröffnung. Genau das entspricht dem Winterfall, und der ist negativ.

**Weitere Hinweise:**
- Die besten 5 % der Montage liefern 44 % der Summe.
- Die Long-Seite (Gap nach unten) trägt fast alles: +0,30 R gegenüber +0,02 R für Short.
- In der Einstiegskerze fehlen bei 22–44 % der Montage M1-Kurse, der Feed ist also dünn.

**Entscheidung:** Q-FXW gilt als gescheitert (Datenartefakt). Eine Prüfung wäre nur mit unabhängigen Tickdaten möglich, etwa dem MT5-Tickexport des FTMO-Servers für Sonntagabende. Mit diesen Daten wäre es allerdings ein neuer Versuch mit neuer Vorregistrierung.

## 3. Folgen für frühere Tests

Die fehlende Sommer-Eröffnungsstunde betrifft nur Regeln, die die erste Kerze der Woche verwenden. Bei Modell T (Nr. 35, Eröffnung des Servertags) sind das die Sommer-Montage. Dort ändert es nichts am Scheitern, denn alle Varianten waren auch vor Kosten nahe null. Neue Spielregel in `../STRATEGIEN.md`: Hängt ein Ergebnis an einer Uhrzeit, wird es vor dem Hold-out gegen benachbarte Zeiten und die Jahreszeiten geprüft.

## 4. Trial-Log (Fortsetzung)

| # | Datum | Test | Ergebnis |
|---|---|---|---|
| T138 | 24.10.2026 | Q-IDX, In-Sample | nicht bestanden: −3,15 bp/Tag, t −3,61 |
| T139 | 24.10.2026 | Q-FXW, In-Sample | formal bestanden (+11,9 bp/Montag, t 5,08), verworfen: Feed-Artefakt der ersten Wochenkerze |
| T140–T143 | – | Hold-out, FTMO | entfallen, Hold-out unberührt |
