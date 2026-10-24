# Vorregistrierung: Modell Y „Währungsstärke“ (Strategien Nr. 46 und 47)

Festgelegt am 24.10.2026, **bevor** Code für dieses Modell geschrieben oder Daten dafür ausgewertet wurden. Änderungen nach diesem Commit zählen als neuer Versuch im Trial-Log (`../TRIAL_LOG.md`).

**Vorab festgehalten:** H1-Daten der Majors und Crosses wurden ausgewertet: Querschnitts-Momentum D1 (Nr. 7), London Breakout (Nr. 31), Asien-Range (Nr. 32), H1-Mean-Reversion Crosses (Nr. 37, 39). Sitzungsstärke-Rankings und währungsspezifische Abweichungen wurden nicht angesehen.

## 0. Feste Rahmenbedingungen (für alle Strategien gleich)

- Expert Advisor für MetaTrader 5, handelt vollständig autonom
- FTMO 2-Step, Swing, 100.000 USD
- Max. Verlust gesamt 10 %, max. Tagesverlust 5 %
- Ziel Phase 1 +10 %, Ziel Phase 2 +5 %
- News-Trading und Halten übers Wochenende erlaubt

## 1. Hypothesen

- **Nr. 46:** Das Paar aus der stärksten und der schwächsten Währung einer Sitzung setzt die Bewegung in der Folgesitzung nach Kosten mit t ≥ 3 fort (Y-ASIA, Y-LDN).
- **Nr. 47:** Währungsspezifische Abweichungen eines USD-Paares vom Korb kehren nach Kosten mit t ≥ 3 zurück (Y-USDB).

**Erwartung vor dem Test: Scheitern aller drei.**

## 2. Daten, Kosten, Zeiträume

- **Daten:** H1-Serverkerzen (HistData). Gehandelt wird über die 24 verfügbaren Paare (7 USD-Majors, 17 Crosses); EURGBP, AUDCHF, NZDCAD und NZDCHF fehlen.
- **Währungsstärke:** aus den 7 USD-Paaren. Für Währung c ist p_c = ln(Kurs von c in USD), also ln EURUSD bzw. −ln USDJPY; für USD gilt p_USD = 0. Die Stärke über ein Fenster ist die Änderung von p_c minus das Mittel der Änderungen aller 8 Währungen.
- **Kosten und Swaps:** FX-Kostenmodell (effektiver Spread, Kommission, 0,1 Pip Slippage, Kauf und Short-Schluss zum Ask); Swaps je Rollover
- **In-Sample:** Einstiege 2015–2023, Kurse bis 31.12.2023. **Hold-out:** ab 2024, einmalig je bestandener Variante.

## 3. Regeln

**Nr. 46 (Londoner Zeit, Werktage, keine Einstiege 24.12.–01.01.)**

| Variante | Stärke-Fenster | Einstieg (Eröffnung der H1-Kerze) | Zeitausstieg (Eröffnung) |
|---|---|---|---|
| **Y-ASIA** | 00:00 → 07:00 London (Eröffnungen der H1-Kerzen) | 07:00 | 16:00 |
| **Y-LDN** | 07:00 → 12:00 London | 12:00 | 16:00 |

- Stärkste Währung S und schwächste W nach Fensterstärke. Gehandelt wird das verfügbare Paar aus S und W in Richtung „S kaufen, W verkaufen“. Ist das Paar nicht verfügbar, gibt es keinen Trade.
- Fehlt eine benötigte H1-Kerze (USD-Paare zu Fensterbeginn/-ende, Handelspaar zu Einstieg und Ausstieg), gibt es keinen Trade.
- **Stop:** fest bei Einstieg ∓ 2 × ATR14_H1 des Handelspaares (aus den Kerzen vor dem Einstieg), intrabar
- **Größe:** Nominal = min(0,25 % Kapital / (2 × ATR14 / Kurs), 10 × Kapital)

**Nr. 47 Y-USDB (je USD-Major, Signal am Schluss der H1-Kerze i, Einstieg zur Eröffnung von i+1)**
- **Abweichung:** dev_c(i) = [p_c(i) − p_c(i−24)] − Mittel über die 6 anderen Nicht-USD-Währungen k von [p_k(i) − p_k(i−24)], mit Schlusskursen
- z(i) = dev_c(i) / Standardabweichung von dev_c über die Kerzen i−499 … i
- z > 2 → Short c gegen USD (Short EURUSD bzw. Long USDJPY); z < −2 → Long c
- **Ausstieg:** zur nächsten Eröffnung, sobald z das Vorzeichen wechselt oder 0 erreicht, spätestens nach 24 gehaltenen Kerzen
- **Stop:** fest 2 × ATR14_H1(i), intrabar mit Vorrang
- Je Paar höchstens eine Position; ein neues Signal frühestens am Schluss der Kerze nach dem Ausstieg; keine neuen Einstiege 24.12.–01.01.
- **Größe:** wie Nr. 46

**Gemeinsam:**
- Ein Gap über den Stop wird zur Eröffnung gefüllt.
- **Portfolio:** Summe aller Trades; Ergebnis am Servertag des Ausstiegs; alle Werktage zählen, Tage ohne Ausstieg als 0.

## 4. Akzeptanzkriterien

Wie Nr. 33–45 (alle müssen erfüllt sein): t ≥ **3,0** (kleinster aus iid, Woche, Monat) bei positivem Mittel; ≥ 6 von 9 Jahren positiv; doppelte Kosten > 0. Statt der Instrumente-Regel gilt: ≥ 60 % der 8 Währungen positiv, gemessen am Ergebnis der Trades, in denen die Währung gekauft bzw. verkauft wurde. Jede Variante wird für sich bewertet. Vor einem Hold-out gilt die Artefakt-Prüfung (Spielregel 6).

**Beschreibend:**
- Trades, Ø R vor und nach Kosten, Stops
- gehandelte Paare; Häufigkeit von S und W
- Ergebnis je Währung

**Hold-out und FTMO:** wie Nr. 16.

## 5. Umsetzbarkeit als MT5-EA

Der EA liest die H1-Kurse der 7 USD-Paare und berechnet daraus die Stärke. Er braucht Marktorders auf bis zu 24 Paaren, einen festen Stop und einen Zeitausstieg. Es werden keine externen Daten benötigt.

## 6. Trial-Log (Fortsetzung des globalen Logs)

| # | Test |
|---|---|
| T156 | Y-ASIA (Nr. 46), In-Sample |
| T157 | Y-LDN (Nr. 46), In-Sample |
| T158 | Y-USDB (Nr. 47), In-Sample |
| T159–T164 | Hold-out und FTMO je bestandener Variante |
