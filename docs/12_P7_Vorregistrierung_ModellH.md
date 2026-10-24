# P7 – Vorregistrierung: Modell H „Trendfolge Indizes und Rohstoffe“

Festgelegt am 24.10.2026, **bevor** Code für dieses Modell geschrieben oder Kursdaten der neuen Instrumente ausgewertet wurden. Geprüft werden darf vorher nur die Datenvollständigkeit (Abdeckung, Lücken, Roll-Sprünge), nicht das Ergebnis einer Strategie. Änderungen nach diesem Commit zählen als neuer Versuch im Trial-Log.

## 1. Hypothese und Herkunft

Dieselbe Trendregel wie Modell G (`docs/10`) trägt auf Aktienindizes und Rohstoffen. Dort ist Zeitreihen-Momentum in der Literatur am besten belegt (Moskowitz, Ooi & Pedersen 2012; Hurst, Ooi & Pedersen 2017).

**Herkunft:** Empfehlung aus `docs/11`, §4, nachdem Modell G auf FX und Gold gescheitert ist. Die Regeln von Modell G werden unverändert übernommen; neu sind nur Instrumente, Handelszeiten und das Kostenmodell für CFDs.

**Vorab festgehalten:**
- Anleihen fehlen. FTMO bietet sie nicht an, HistData hat keine Daten dafür. Gerade Anleihen trugen in der Literatur viel zur Trendrendite bei.
- **Erwartung vor dem Test: Sharpe Ratio deutlich unter 1.**

## 2. Daten und Zeiträume

- HistData M1 (Bid), umgerechnet in UTC und Serverzeit, mit Warm-up 2014
- **In-Sample (IS):** 01.01.2015–31.12.2023
- **Hold-out (HO):** 01.01.2024 bis Datenende (16.10.2026), einmalig und nur, wenn IS besteht
- Zinsen für Swaps: FRED wie in P4 und P6

## 3. Instrumente, Handelszeiten und Kosten

| HistData | FTMO | Währung | Ausführung (New York) | Ø FTMO-Spread | Dividendenrendite (Annahme) |
|---|---|---|---|---|---|
| SPXUSD | US500.cash | USD | 15:50 | 0,55 | 1,8 % |
| NSXUSD | US100.cash | USD | 15:50 | 1,66 | 0,8 % |
| GRXEUR | GER40.cash | EUR | 10:50 | 1,58 | 0 (Performance-Index) |
| FRXEUR | FRA40.cash | EUR | 10:50 | 2,25 | 2,8 % |
| UKXGBP | UK100.cash | GBP | 10:50 | 1,34 | 3,8 % |
| ETXEUR | EU50.cash | EUR | 10:50 | 2,0 (nicht gelistet, Annahme) | 3,2 % |
| JPXJPY | JP225.cash | JPY | 00:50 | 10 | 1,9 % |
| HKXHKD | HK50.cash | HKD (USD-Zins, Peg) | 02:50 | 6,99 | 3,5 % |
| AUXAUD | AUS200.cash | AUD | 23:50 des Vortags | 1,61 | 4,2 % |
| WTIUSD | USOIL.cash | USD | 15:50 | 0,08 | – |
| BCOUSD | UKOIL.cash | USD | 15:50 | 0,08 | – |
| XAGUSD | XAGUSD | USD | 15:50 | 0,071 | – |
| XAUUSD | XAUUSD | USD | 15:50 | 0,52 | – |

- **Spreads:** FTMO-Durchschnittswerte für das Raw-Spread-Konto laut FXVerify (2026).
  - Sie werden relativ angesetzt: Spread geteilt durch den mittleren Kurs 01.01.–16.10.2026 in unseren Daten.
  - In Basispunkten werden sie dann auf alle Jahre übertragen.
- **Ausführungszeiten:** Sie liegen in der liquiden Kassasitzung und mindestens 2 Stunden vor jeder Handelspause von 2 Stunden oder mehr (FTMO-Regel zum Gap Trading).
  - USA 15:50 New York
  - Europa 10:50 New York (15:50 London, 16:50 Frankfurt)
  - Tokio 00:50, Hongkong 02:50, Sydney 23:50 New York
- **Signalpreis:** Kurs 5 Minuten vor der Ausführung.
- **Kommission:** keine auf Indizes und Öl; Gold und Silber 0,0007 % je Seite.
- **Slippage:** 25 % des Spreads je Ausführung.
- **Swaps** (je Rollover um 00:00 Serverzeit, Mittwoch dreifach, 7 Nächte je Woche):

  | Instrument | Long | Short |
  |---|---|---|
  | Indizes | Dividendenrendite − Zins − 2,5 % | Zins − 2,5 % − Dividendenrendite |
  | Öl | −(USD-Zins + 2,5 %) | USD-Zins − 2,5 % |
  | Gold und Silber | −(USD-Zins + 1 %) | USD-Zins − 1 % |

  - Die 2,5 % p. a. sind ein angenommener CFD-Aufschlag.
  - Bei Öl fehlt die Rendite aus dem Rollen der Futures (Contango/Backwardation), dafür gibt es keine Daten. In großen Trends lag sie oft auf der Seite der Position. Die Annahme ist damit eher vorsichtig, aber ungeprüft.
- **0,7-%-Gebühr:** auf Episoden-Ergebnisse bei Profit-Währung ≠ USD (EUR, GBP, JPY, HKD, AUD), wie in P6.

## 4. Regeln

Wie Modell G (`docs/10`, §3), je Instrument zu seiner Ausführungszeit:
- **Signal:** `s = (sign(R21) + sign(R63) + sign(R252)) / 3` auf Signalpreisen
- **Positionsgröße:** `w = s × 10 % / σ`; σ = EWMA-Volatilität mit Schwerpunkt 60 Tage, Untergrenze 4 % p. a.
- **Umschichten:** Montag bis Donnerstag
  - nie freitags, nicht vom 24.12. bis 01.01., nicht ohne M5-Kerze bis zur Ausführungszeit
  - tägliche Bewertung zur Ausführungszeit
- **Einstieg ins Portfolio:** sobald 253 Tageskurse vorliegen.
- **Portfolio:** Tagesergebnis = Summe über die 13 Instrumente.

## 5. Akzeptanzkriterien

**In-Sample** (alle müssen erfüllt sein)

| # | Kriterium |
|---|---|
| 1 | Mittleres Netto-Tagesergebnis > 0 mit t-Wert ≥ **3,0** (kleinster aus iid, Woche, Monat), etwa Sharpe Ratio ≥ 1,0 |
| 2 | ≥ 6 von 9 Jahren positiv |
| 3 | ≥ 60 % der Instrumente mit positivem Netto-Beitrag (≥ 8 von 13) |
| 4 | Mittleres Tagesergebnis bei doppelten Kosten > 0 (Handelskosten, Gebühr, belastende Swaps verdoppelt) |

Besteht Modell H nicht, ist **P7 gescheitert**, und der Hold-out bleibt unberührt.

**Hold-out und FTMO:** wie P6 (`docs/10`, §4).
- **Hold-out:** Mittel > 0 und ≥ untere 95-%-Grenze von IS.
- **FTMO:**
  - Ziel-Volatilität 10, 15 und 20 % p. a.
  - Leiter, Daily Loss mit Balance-Bezug, Max Loss, Block-Bootstrap über Monate
  - Bestanden: P(beide Phasen) ≥ 70 % und Median ≤ 6 Monate
- **Margin-Prüfung (zusätzlich):**
  - Swing-Hebel: Indizes 1:15 (HK50 1:9), Öl 1:9, Silber 1:9, Gold 1:15.
  - Margin ≤ 80 % der Equity, sonst werden alle Positionen anteilig verkleinert.

## 6. Trial-Log (Fortsetzung)

| # | Test |
|---|---|
| T16 | Modell H, In-Sample |
| T17 | Hold-out (nur falls T16 besteht) |
| T18 | FTMO-Bootstrap (nur falls T17 besteht) |
