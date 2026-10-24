# Vorregistrierung: Modell K „FX Carry G8“ (Strategie Nr. 6)

Festgelegt am 24.10.2026, **bevor** Code für dieses Modell geschrieben oder Daten dafür ausgewertet wurden. Geprüft wurde vorher nur die Abdeckung der Zinsreihen (alle bis 09/2026, EUR bis 01/2026). Änderungen nach diesem Commit zählen als neuer Versuch im Trial-Log (`../TRIAL_LOG.md`).

## 0. Feste Rahmenbedingungen (für alle Strategien gleich)

- Expert Advisor für MetaTrader 5, handelt vollständig autonom
- FTMO 2-Step, Swing, 100.000 USD
- Max. Verlust gesamt 10 %, max. Tagesverlust 5 %
- Ziel Phase 1 +10 %, Ziel Phase 2 +5 %
- News-Trading und Halten übers Wochenende erlaubt

## 1. Hypothese

Ein dollar-neutrales Portfolio, das die höchstverzinsten G8-Währungen gegen die niedrigstverzinsten hält, erzielt nach Spreads, Swap-Aufschlägen und Gebühren eine positive Rendite (Lustig, Roussanov & Verdelhan 2011; Details in `docs/00_Recherche.md`).

**Erwartung vor dem Test: eher Scheitern** (Sharpe Ratio unter 0,5).

## 2. Daten und Zeiträume

- HistData M5 (Bid) der 24 FX-Paare aus `../smart-money-concept/data/bars`
- Zinsen: die Monatsreihen von FRED aus dem SMC-Swap-Modell (`smc/swaps.py`). Tagesgeld bzw. 3-Monats-Interbank für CHF und NZD.
- Engine, Zeit- und Kostenmodell aus dem SMC-Projekt (Stand Commit `0c41b29`)
- **Warm-up:** 2014 (Volatilitätsschätzung)
- **In-Sample (IS):** Handelstage 01.01.2015–31.12.2023
- **Hold-out (HO):** 01.01.2024 bis Datenende (16.10.2026), einmalig und nur, wenn IS besteht. Fehlende Zinsmonate am Ende (EUR ab 02/2026) werden mit dem letzten Wert fortgeschrieben, wie im Swap-Modell.

## 3. Regeln

**Währungen:** USD, EUR, GBP, JPY, AUD, CAD, NZD, CHF

**Signal**
- `r_c` = Zinssatz der Währung c im **Vormonat** des Umschichtungstags (Monatsmittel). Damit ist der Wert zum Handelszeitpunkt bekannt.
- Rangfolge absteigend nach `r_c`, bei Gleichstand alphabetisch.

**Varianten (je ein Trial)**

| Variante | Carry-Positionen (Rang hoch / Rang niedrig) |
|---|---|
| **K-3** | (1 / 8), (2 / 7), (3 / 6) |
| **K-1** | (1 / 8) |

**Umsetzung einer Carry-Position H/L** (long H, short L)
- Gibt es das Paar H/L oder L/H unter den 24 FX-Paaren, wird es direkt gehandelt.
- Sonst wird die Position über zwei USD-Paare gebaut: Long H gegen USD, Short L gegen USD.
  - Betroffen sind die fehlenden Crosses EURGBP, AUDCHF, NZDCHF und NZDCAD.
  - Der Swap-Aufschlag fällt dann auf beide Beine an.
- Ist H oder L der USD, ist es ein direktes USD-Paar.

**Größe einer Carry-Position**
- Nominalwert `N = 10 % / σ` in Vielfachen des Kapitals.
- `σ` = EWMA-Volatilität der Tagesrenditen des Kurses H/L.
  - Schwerpunkt 60 Tage (α = 1/61), annualisiert mit √261, Untergrenze 4 % p. a.
  - Berechnet aus den 16:50-New-York-Kursen der USD-Paare, auch wenn das Cross direkt handelbar ist.
  - Startwert: Varianz der ersten 60 Tagesrenditen.
- **Gewichte je Instrument** (Vielfache des Kapitals), Summe über alle Carry-Positionen:
  - Direktes Paar: `+N`, wenn H die Basiswährung ist, sonst `−N`.
  - Bein „Long H gegen USD“: `+N` bei HUSD, `−N` bei USDH. Bein „Short L“ entsprechend umgekehrt.

**Umschichten**
- Am **ersten Handelstag jedes Monats** um 16:50 New York auf die neuen Zielgewichte.
  - Handelstag = Server-Tag Mo–Fr, an dem alle 7 USD-Paare eine M5-Kerze haben, die um 16:50 New York endet.
  - Keine Umschichtung an FX-Tagen vom 24.12. bis 01.01. (dann der nächste Handelstag).
- Fehlt einem Instrument am Umschichtungstag der Kurs, wird es am nächsten Tag mit Kurs umgeschichtet.
- Dazwischen bleiben die Gewichte konstant. Halten über Nacht und Wochenende ist erlaubt.

**Bewertung und Kosten** (wie Modell G, `smc/strategy_g.py`)
- Tagesergebnis je Instrument = Gewicht × relative Änderung des 16:50-New-York-Kurses
- **Handel:** je gehandeltem Nominal `(Spread / 2 + Slippage + Kommission Round Turn / 2) / Kurs`
  - Spread = typischer Raw-Spread + 0,3 Pip Volume-Band-Zuschlag
  - Slippage 0,1 Pip; Kommission 5 USD pro Lot Round Turn
- **Swaps:** je Rollover `Nominal × (d × Zinsdifferenz − 1 % Aufschlag) / 365`, mittwochs dreifach
- **0,7-%-Gebühr** auf das Episodenergebnis bei Profit-Währung ≠ USD

**Portfolio:** Tagesergebnis = Summe über alle Instrumente.

## 4. Akzeptanzkriterien

**In-Sample, je Variante** (alle müssen erfüllt sein)

| # | Kriterium |
|---|---|
| 1 | Mittleres Netto-Tagesergebnis > 0 mit t-Wert ≥ **3,0**, als kleinster Wert aus iid (Tage) und Clustern nach Woche und Monat. Über 9 Jahre entspricht das einer Sharpe Ratio von etwa ≥ 1,0. |
| 2 | ≥ 6 von 9 Jahren positiv |
| 3 | ≥ 60 % der gehandelten Instrumente (mit ≥ 250 Positionstagen) mit positivem Netto-Beitrag |
| 4 | Mittleres Tagesergebnis bei doppelten Kosten > 0 (Handelskosten, Gebühr und belastende Swaps verdoppelt; Swap-Gutschriften nicht) |

**Variantenwahl:** Bestehen beide, gewinnt die mit dem höheren t-Wert. Besteht keine, ist **Strategie Nr. 6 gescheitert**, und der Hold-out bleibt unberührt.

**Beschreibend, ohne Einfluss auf die Entscheidung:**
- Zerlegung in Kursergebnis, Swaps, Handelskosten und Gebühr
- Ergebnis ohne Swap-Aufschlag (zeigt den Einfluss der Annahme von 1 %)
- Ergebnis je Jahr und je Instrument
- Häufigkeit der Währungen auf Long- und Short-Seite

**Hold-out** (einmalig, gewählte Variante)

| # | Kriterium |
|---|---|
| 1 | Mittleres Netto-Tagesergebnis > 0 |
| 2 | ≥ untere Grenze des 95-%-Konfidenzintervalls von IS (Cluster-Bootstrap nach Monat) |

**FTMO** (Tagesergebnisse IS + HO, nur falls der Hold-out besteht; Verfahren wie Modell G im SMC-Projekt, `docs/10` §4)

- **Skalierung:** Ziel-Volatilität des Portfolios 10 %, 15 % bzw. 20 % p. a., kalibriert auf IS.
  - Phase 2 mit dem 0,75-Fachen.
  - Ab 3 % Drawdown wird halbiert, ab 6 % geviertelt.
- **Daily Loss:** Bezug ist das Maximum aus Equity und Balance zu Beginn des Prager Tags, minus 5 %. Im Worst Case zählt die Summe der ungünstigsten M5-Ausschläge.
- **Max Loss:** Equity im Worst Case ≥ 90 %.
- **Ziel:** Equity ≥ Ziel + 0,3 %. Dann wird alles geschlossen.
- **Mindesthandelstage:** 4 je Phase, fehlende Tage über den Mindesttage-Modus.
- **Block-Bootstrap:** über Kalendermonate, 10.000 Pfade, höchstens 120 Monate.
- **Bestanden:** wenn für mindestens eine Ziel-Volatilität gilt:
  - Bestehenschance beider Phasen ≥ 70 %
  - Median-Dauer ≤ 6 Monate

**FTMO-Konformität:** K-3 hält bis zu 6 Positionen, darunter mehrere USD-Paare. Die Richtungen sind aber gemischt, und das Portfolio ist dollar-neutral konstruiert. Vor einem Kauf ist beim Support zu klären, ob das unter „Overexposure“ fällt.

## 5. Umsetzbarkeit als MT5-EA

- **Signal live ohne externe Daten:** Der EA liest von den 7 USD-Paaren die Swap-Sätze `SYMBOL_SWAP_LONG` und `SYMBOL_SWAP_SHORT`. Die Zinsdifferenz zum USD ergibt sich je Währung als `(Swap long − Swap short) / 2`, umgerechnet in % p. a. Ein symmetrischer Aufschlag fällt dabei heraus. Daraus folgt die Rangfolge.
- **Abweichung zum Test:** Der Backtest verwendet die FRED-Zinsen des Vormonats. Im Live-Betrieb reagiert der Swap schneller auf Zinsentscheide. Das wird im Demo-Betrieb verglichen.
- **Ausführung:** einmal im Monat Marktorders auf die Zielgewichte, Volatilität aus D1-Kursen im EA, kein Stop. Das Risiko begrenzen der FtmoGuard und die Volatilitätsskalierung.

## 6. Trial-Log (Fortsetzung des globalen Logs)

| # | Test |
|---|---|
| T23 | K-3, In-Sample |
| T24 | K-1, In-Sample |
| T25 | Hold-out der gewählten Variante (nur falls T23 oder T24 besteht) |
| T26 | FTMO-Bootstrap (nur falls T25 besteht) |
