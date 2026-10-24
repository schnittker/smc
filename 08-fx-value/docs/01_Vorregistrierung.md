# Vorregistrierung: Modell V „FX Value“ (Strategie Nr. 8)

Festgelegt am 24.10.2026, **bevor** Code für dieses Modell geschrieben oder Daten dafür ausgewertet wurden. Die FRED-Dateien wurden nur auf Länge, ersten und letzten Wert geprüft. Änderungen nach diesem Commit zählen als neuer Versuch im Trial-Log (`../TRIAL_LOG.md`).

**Vorab festgehalten:** Die Portfolio-Engine und die 24 FX-Paare wurden in Nr. 6 (Carry), Nr. 7 (Momentum inkl. 12-Monats-Umkehr) und Nr. 20 (Zins-Momentum) ausgewertet. Reale Wechselkurse wurden nicht angesehen.

## 0. Feste Rahmenbedingungen (für alle Strategien gleich)

- Expert Advisor für MetaTrader 5, handelt vollständig autonom
- FTMO 2-Step, Swing, 100.000 USD
- Max. Verlust gesamt 10 %, max. Tagesverlust 5 %
- Ziel Phase 1 +10 %, Ziel Phase 2 +5 %
- News-Trading und Halten übers Wochenende erlaubt

## 1. Hypothese

Ein monatliches G8-Value-Portfolio verdient nach Kosten mit t ≥ 3. **Erwartung vor dem Test: Scheitern.**

## 2. Daten

- **Monats-CPI** P_c (AUD und NZD quartalsweise, für die Monate des Quartals gleich; Japan ab 07/2021 fortgeschrieben, siehe Recherche)
- **Monatsend-Wechselkurse** S_c = USD je Einheit c (FRED DEX, letzter Wert des Monats)
- **Realer Wechselkurs** q_c(m) = ln S_c(m) + ln P_c(m − 2) − ln P_US(m − 2), mit 2 Monaten Veröffentlichungsverzug für die CPI; q_USD = 0
- **Handel und Buchhaltung** wie Nr. 6/20 (`carry.model`, HistData 16:50 New York, Kosten, Swaps mit 1 % Aufschlag, Gebühr)

## 3. Regeln

**Ranking** am ersten Handelstag des Monats m aus den Daten bis Ende m−1. Die Währung mit dem höchsten Signal gilt als am billigsten.

| Variante | Signal je Währung c |
|---|---|
| **V-5Y** | −[q_c(m−1) − q_c(m−61)], also die 5-Jahres-Änderung des realen Kurses mit umgekehrtem Vorzeichen (AMP 2013) |
| **V-PPP** | −[q_c(m−1) − Mittel von q_c über alle Monate ab 01/1999 bis m−1] (Abweichung vom Langfristmittel) |

**Positionen** wie K-3 (Nr. 6): Long/Short-Paare (1/8), (2/7), (3/6) aus der Rangfolge, je 10 % / σ. Gleichstände werden alphabetisch aufgelöst. Gewichte bleiben bis zum nächsten Monat konstant.

## 4. Akzeptanzkriterien

Wie Nr. 6/20 (alle müssen erfüllt sein): t ≥ **3,0** (kleinster aus iid, Woche, Monat); ≥ 6 von 9 Jahren positiv; ≥ 60 % der gehandelten Instrumente (≥ 250 Positionstage) positiv; doppelte Kosten > 0. Variantenwahl über den höheren t-Wert. Vor einem Hold-out gilt die Artefakt-Prüfung (Spielregel 6).

**Beschreibend:** Ranking-Häufigkeit je Währung; Korrelation der Tagesrenditen mit Nr. 7 X-12.

**Hold-out:** ab 2024, einmalig für die gewählte Variante. Der UK-, CA- und CH-CPI endet 2025; danach wird mit dem letzten Wert fortgeschrieben.

## 5. Umsetzbarkeit als MT5-EA

Das Ranking ist monatlich und kann offline erstellt und als Tabelle in den EA eingetragen werden (oder per WebRequest auf FRED). Gehandelt wird mit Marktorders zur Monatswende.

## 6. Trial-Log (Fortsetzung des globalen Logs)

| # | Test |
|---|---|
| T299 | V-5Y (Nr. 8), In-Sample |
| T300 | V-PPP (Nr. 8), In-Sample |
| T301, T302 | Hold-out, FTMO (nur bei Bestehen) |
