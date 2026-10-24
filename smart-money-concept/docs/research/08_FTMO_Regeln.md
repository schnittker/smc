<!-- Kapitel 8: FTMO 2-Step Swing 100k – Regeln & Handelsbedingungen | Deep-Research-Rohbericht (Recherche-Agent), Stand 2026-10-24, unverändert übernommen -->

# FTMO 2-Step mit Swing-Konto, 100.000 USD: Regeln und Handelsbedingungen für den EA

**Stand der Recherche:** 24.10.2026. Die Quellen sind überwiegend von ftmo.com: Trading Objectives (zuletzt geändert 20.10.2026), FAQ-Seiten aus September und Oktober 2026 und die Trading Updates bis 22.10.2026. Mit „[eigene Rechnung]“ oder „[Inferenz]“ markierte Stellen habe ich selbst abgeleitet, sie sind kein FTMO-Wortlaut.

**Einschränkung bei den AGB:** Die aktuellen AGB liegen als PDF vor („FTMO Challenge Terms and Conditions, last updated on 12 October 2026“, https://cdn.ftmo.com/docs/terms-and-conditions/b1d80f4da76c4bd4bcd42a5807727e34). WebFetch konnte den Inhalt nicht lesen, weil er komprimiert ist. Einen Parser habe ich wegen der Vorgabe „nur lesen“ nicht ausgeführt. Alle AGB-Klauseln unten stammen deshalb aus Suchauszügen oder Drittquellen und sind entsprechend gekennzeichnet.

---

## 0. Änderungen 2023–2026 (alt → neu)

| Datum (Wirksamkeit) | Was | Alt → neu |
|---|---|---|
| 13.07.2023 | Zeitlimit Challenge/Verification | 30 bzw. 60 Tage → unbegrenzt; Free Repeat und 14-Tage-Verlängerung entfallen |
| 24./25.08.2024 | Stop-Out; Margin bei Hedge-Positionen | 30 % → 50 %; statt nur der größeren Seite wird die Summe beider Seiten als Margin gesperrt |
| 29.09.2025 | Kommission | FX: 1,50 → 2,50 USD/Lot/Seite; Metalle: 0,0005 % → 0,0007 % vom Volumen je Seite |
| 15.09.2025 (Free Trials), 20.04.2026 (alle Konten) | Ausführung | Einführung von „Volume Bands“: der Preis hängt von der Ordergröße ab, Spreads niedriger |
| 01.02.2026 | Hebel XAU-Paare | Swing 1:9 → 1:15; Standard 1:30 → 1:50 |
| 11.05.2026 | Hebel NZD-Paare (u. a. NZDUSD, NZDJPY, EURNZD, GBPNZD, AUDNZD) | Swing 1:20 → 1:30; Standard 1:67 → 1:100 |
| 28.07.2026 (Inkrafttreten je nach Produktphase, steht im jeweiligen Vertrag) | AGB und Account Agreement | neu: 0,7 % Abschlag bei Währungsumrechnung |
| 12.10.2026 | nur 1-Step: Consistency-Regel ersetzt die Best Day Rule | betrifft 2-Step nicht |
| – | Bezeichnung der Kontoart | „Normal“ heißt jetzt „Standard“ |

---

## 1. Max Daily Loss (MDL)

Gilt im 2-Step in Challenge, Verification **und** im späteren FTMO Account.

| Punkt | Regel |
|---|---|
| Betrag | 5 % des Initial Simulated Capital, also **fix 5.000 USD** (nicht 5 % vom Tagesstand) |
| Basis | **Balance** um 00:00 CE(S)T (Prager Zeit) des laufenden Tages; am ersten Handelstag das Anfangskapital |
| Formel | Limit = Balance(00:00 Prag) − 5.000 |
| Prüfgröße | Equity = „Balance + Open Positions P/L ± Swaps – Commissions“. Floating-P/L, Swaps und Kommissionen zählen also mit |
| Wann geprüft | „at any time“, also laufend und intraday auf Equity inklusive offener Positionen |
| Reset | täglich 00:00 CE(S)T; das Limit gilt bis zur nächsten Neuberechnung |
| Bei Verletzung | „the platform automatically closes all your open positions, and the account is considered failed“ |

**Rechenbeispiele von FTMO:**
- 100k, Tag 1: Limit 95.000.
- 200k (Academy): Mitternachtsbalance 204.000 → Limit 194.000; danach 202.000 → Limit 192.000.

**Reset in MT5-Serverzeit.** Die MT5-Server laufen laut FTMO auf „GMT+2 +DST“. Die Sommerzeitumstellung folgt nachweislich dem US-Kalender (Umstellungen am 09.03.2025, 02.11.2025 und 01.11.2026). FTMO schreibt dazu: „Max Daily Loss is measured on Prague time … resets at Prague midnight“.

| Zeitraum | Server | Prag | Reset in Serverzeit |
|---|---|---|---|
| Normal (beide Winterzeit bzw. beide Sommerzeit) | GMT+2 / GMT+3 | GMT+1 / GMT+2 | **01:00** |
| 26.10.–01.11.2026 (EU schon Winterzeit, US noch Sommerzeit) | GMT+3 | GMT+1 | **02:00** |
| 08.03.–29.03.2026 (von FTMO bestätigt); 14.–28.03.2027 und 31.10.–07.11.2027 [eigene Rechnung nach den DST-Regeln] | GMT+3 | GMT+1 | **02:00** |

Die Lückenwoche beginnt am Montag, 26.10.2026. FTMO empfiehlt, den Reset über den Tooltip „Today's permitted loss“ in Account MetriX zu prüfen.

**Folgen für den EA [Inferenz/eigene Rechnung]:**
- **Server-Tag ≠ FTMO-Tag.** Die ersten ein bis zwei Serverstunden gehören noch zum vorherigen Prager Tag.
- **Swaps und Daily Reports** werden um 00:00 Serverzeit gebucht (Updates 30.10.2025 und 22.10.2026). Das liegt vor dem MDL-Reset, ebenso die Spread-Ausweitung zum Rollover.
- **Über Nacht gehaltene Positionen.** Die Basis ist die Balance, nicht die Equity. Beispiel: Balance um 00:00 = 102.000 bei −1.500 Floating ergibt ein Limit von 97.000. Der Restspielraum beträgt dann nur 3.500 statt 5.000.
- **Wochenend-Gap.** Die Woche öffnet um 00:00 Serverzeit am Montag, das ist 23:00 Prager Zeit am Sonntag (in Lückenwochen 22:00). Ein Gap fällt damit auf den „Sonntag“, dessen Basis die Balance vom Freitag ist.

**Widerspruch:** jptradingcapital.com nennt als Basis „5 % of starting equity or balance (whichever is higher)“. Das widerspricht den FTMO-Quellen und ist zu verwerfen.

**Quellen:**
- https://ftmo.com/en/trading-objectives/ (geändert 20.10.2026)
- https://academy.ftmo.com/lesson/maximum-daily-loss/ (07.03.2026)
- https://ftmo.com/en/drawdowns/ (28.04.2026)
- https://ftmo.com/en/faq/what-are-the-trading-objectives/ (06.10.2026)
- https://ftmo.com/en/faq/what-are-the-account-specifications/ (05.10.2026)
- https://ftmo.com/en/blog/trading-updates/trading-update-22-oct-2026/
- https://ftmo.com/en/blog/trading-updates/trading-update-15-oct-2026/
- https://ftmo.com/en/blog/trading-updates/trading-update-12-mar-2026/
- https://ftmo.com/en/blog/trading-updates/trading-update-30-oct-2025/
- Abweichende Drittquelle: https://www.jptradingcapital.com/blog/en/ftmo-rules

## 2. Max Loss (10 %)

- **Statisch, nicht trailing.** Die Equity (gleiche Definition wie oben) darf nie unter **90.000** fallen.
- Gilt in allen Phasen, auch im FTMO Account.
- Trailing gibt es nur beim 1-Step (End-of-Day) und beim Instant Account (intraday).
- **Wirksame Untergrenze [eigene Rechnung]:** Floor = max(Balance um 00:00 Prag − 5.000; 90.000).

**Quellen:** https://ftmo.com/en/trading-objectives/ · https://ftmo.com/en/comparison-table/

## 3. Profit Target

- **Ziele:** Challenge 10 % (Balance ≥ 110.000), Verification 5 % (Balance ≥ 105.000). Der FTMO Account hat kein Profitziel.
- **Balance zählt, nicht Equity.** Wortlaut: „once your account balance exceeds the Initial Simulated Capital by the required Profit Target **with all positions closed**“. Die Academy ergänzt: „To secure the Profit Target, all of your positions must be closed.“
- Berührt die Equity das Ziel bei offenen Positionen, gilt das nicht als bestanden. Dass FTMO dann automatisch schließt, habe ich nirgends gefunden.
- **Alle Ziele gleichzeitig:** „You must satisfy all applicable Trading Objectives concurrently.“ Das Profitziel und die 4 Handelstage müssen also gemeinsam erfüllt sein.
- **Nach dem Bestehen:** „no longer need to trade on the account“. Die Prüfung dauert etwa 1–2 Werktage (Challenge) bzw. 1–4 Werktage (Verification). Danach kommt ein neues Konto; nach der Verification sind KYC („FTMO Identity“) und das Account Agreement nötig.

**Quellen:**
- https://ftmo.com/en/trading-objectives/
- https://academy.ftmo.com/lesson/profit-target/ (06.06.2024)
- https://ftmo.com/en/faq/i-have-successfully-passed-what-to-do-now/ (09.10.2026)

## 4. Handelstage, Zeitlimit, Inaktivität

**Mindesthandelstage**
- Mindestens **4 Trading Days je Phase**. Im FTMO Account gilt keine Mindestzahl.
- Ein Trading Day ist jeder Tag „from 00:00:00 to 23:59:59 CE(S)T“, an dem mindestens eine Position **eröffnet** wird.
- Das Schließen einer Position zählt nicht. Mehrere Eröffnungen am selben Tag zählen als ein Tag.
- FTMO-Beispiel: Eröffnungen am 12., 18. und 24. Januar ergeben 3 Tage, das reicht nicht.
- Die Regel „kann nicht verletzt werden“: Man handelt einfach weiter, bis die Tage erreicht sind.
- Eine Mindestgröße pro Trade nennt FTMO nicht. Laut FTMO-US-FAQ ist das Volumen „not further specified“.

**Zeitlimit:** keines („Trading Period: Unlimited“, seit 13.07.2023). Vorher galten 30 Tage für die Challenge und 60 Tage für die Verification.

**Aktivierung:** AGB 5.8.4 (laut Suchauszug der Fassung vom 12.10.2026): Jede Phase wird durch den ersten Trade aktiviert. Geschieht das nicht innerhalb von 30 Kalendertagen nach Bereitstellung, wird der Zugang gesperrt. Innerhalb von 6 Monaten kann man die Reaktivierung beantragen, sonst wird der Vertrag ohne Erstattung beendet.

**Inaktivität:** AGB 13.2.3 (laut pipster.io, Fassung vom 04.08.2026):
- „you do not open at least one simulated trade … for a period of thirty (30) consecutive calendar days“ führt zur Kündigung nach FTMO-Ermessen.
- Laut Suchauszug und Drittquellen zusätzlich: ein Verlust zwischen 8 % und 10 % (inklusive) des Anfangskapitals, der länger als 30 Tage besteht. Diesen Wortlaut konnte ich nicht selbst prüfen.
- FTMO-Blog: Man wird nach „a few weeks“ Inaktivität kontaktiert; ein „freeze“ des Kontos ist auf Antrag möglich.

**Quellen:**
- https://ftmo.com/en/trading-objectives/
- https://academy.ftmo.com/lesson/minimum-trading-days/
- https://ftmo.com/en/2-step-challenge/ (22.10.2026)
- https://ftmo.com/en/blog/trade-without-any-time-limit-and-take-as-long-as-you-want-to-pass/ (13.07.2023)
- https://ftmo.oanda.com/how-to-pass-ftmo-challenge/
- https://www.pipster.io/research/firms/ftmo (28.09.2026)
- https://www.xsrtrade.com/en/prop-firm/ftmo
- AGB-PDF wie oben

## 5. Swing vs. Standard

| | Swing | Standard |
|---|---|---|
| Hebel FX | bis 1:30 (alle 24 Paare; NZD-Paare erst seit 11.05.2026) | bis 1:100 |
| Hebel XAUUSD | 1:15 (seit 01.02.2026, vorher 1:9) | 1:50 (vorher 1:30) |
| News in Challenge/Verification | frei | frei |
| News im FTMO Account | frei | gesperrt 2 Minuten vor bis 2 Minuten nach markierten Events, für betroffene Instrumente, inklusive Auslösung von SL/TP/Pending |
| Halten über Marktpausen > 2 h (Wochenende) in Challenge/Verification | erlaubt | erlaubt |
| Halten über Marktpausen > 2 h im FTMO Account | erlaubt | Schließpflicht |
| Verfügbarkeit | **nur 2-Step** | 2-Step, 1-Step, Instant |
| Wechsel | Swing → Standard möglich, nur auf neuem Konto ohne Trades | Standard → Swing nicht möglich |

- Beide Freiheiten gelten nur „provided that the Forbidden Trading Practices are avoided“ (siehe Abschnitt 7, „Gap Trading“).
- Margin-Beispiel von FTMO: 1 Lot EURUSD braucht EUR 3.333,33 (Swing) bzw. EUR 1.000 (Standard).
- **Widerspruch:** FTMO US (ftmo.oanda.com, Update vom 23.03.2026) bietet Swing auch für den 1-Step an. Das gilt nur für die US-Struktur; die globale FAQ (06.10.2026) sagt ausdrücklich „exclusively within the 2-Step“.
- **Veraltete Werte:** Die Asset-Tabelle im Blog von 2022 nennt für Metalle 1:9 (Swing). Für XAU und XAG ist das durch die Updates 2026 überholt.

**Quellen:**
- https://ftmo.com/en/faq/ftmo-swing-account-type/ (06.10.2026)
- https://ftmo.com/en/faq/can-i-trade-news/ (11.10.2026)
- https://ftmo.com/en/faq/do-i-have-to-close-my-positions-overnight-or-before-the-weekend/ (11.10.2026)
- https://ftmo.com/en/faq/can-i-modify-my-platform-or-account-type/
- https://ftmo.com/en/comparison-table/
- https://ftmo.com/en/blog/trading-updates/trading-update-2-feb-2026/
- https://ftmo.com/en/blog/trading-updates/trading-update-7-may-2026/
- https://ftmo.com/en/blog/a-few-answers-to-your-questions/
- https://ftmo.oanda.com/?p=3728

## 6. Handelsbedingungen auf den FTMO-MT5-Servern

| Punkt | Befund |
|---|---|
| Kommission FX | 2,50 USD je Lot und Seite, also **5 USD Round Turn** |
| Kommission Metalle | 0,0007 % vom Volumen je Seite. XAUUSD-Beispiel bei 4.000 USD: Nominal 400.000 USD, also etwa 2,80 USD pro Seite [eigene Rechnung] |
| Spreads | Kein offizieller Wert. FXEmpire-Test (MT5, London-Session, März 2026): EURUSD 0,1 Pips. Volume Bands: ein Preis je Größenstufe; FTMO-Beispiel EURUSD (0,1] / (1,15] / (15,30] / (30,50] Lots mit Spread 0 / 0,4 / 0,8 / 1,2 Pips [aus den Beispielkursen abgeleitet]. Die AU-Fassung nennt die Grenzen [0,1), dadurch ist die Zuordnung an den Bandgrenzen widersprüchlich |
| Kontraktgrößen | XAUUSD 100 oz (Update 26.09.2024); FX 100.000 Einheiten [abgeleitet aus dem Margin-Beispiel] |
| Symbole | Auf ftmo.com heißen FX- und Metall-Symbole ohne Suffix (EURUSD, XAUUSD); Index-CFDs tragen „.cash“. Alle 25 Instrumente des EA kommen in FTMO-Dokumenten oder Drittlisten vor; alle 24 FX-Paare stehen in der 28er-Majors/Minors-Liste. Im Market Watch prüfen |
| Hedging | Gegenpositionen innerhalb eines Kontos sind ausdrücklich erlaubt. Den MT5-Kontomodus (Hedging oder Netting) dokumentiert ftmo.com nicht; FTMO US hat im Januar/Februar 2026 von Netting auf Hedging umgestellt |
| Stop-Out | 50 % (seit August 2024). Margin bei Hedge-Positionen = Summe beider Seiten |
| Limits | höchstens 200 Orders gleichzeitig, 2.000 Positionen pro Tag; mehr als 2.000 Server-Requests pro Tag gelten als Hyperaktivität |
| Serverzeit | GMT+2 +DST nach US-Kalender. Die D1-Kerze schließt um 00:00 Serverzeit, das entspricht 17:00 New York [Inferenz] |
| Swap | gebucht um 00:00 Serverzeit. Den Tag mit dreifachem Swap nennt FTMO nicht offiziell (Drittquelle: Mittwoch). FTMO: Swaps ändern sich, Verantwortung liegt beim Trader |
| Gold-Handelszeiten | Quote-Session XAUUSD real 01:00–23:50 Serverzeit; seit 28.07.2024 beginnt sie formal um 00:00 (für einheitliche Kerzen). Die tatsächlichen Handelszeiten stehen separat in der Symbol-Spezifikation. An Feiertagen schließen Metalle früher (z. B. 21:30 am US Labor Day 2026; 20:45 am 24.12.2025; geschlossen 25.12. und 01.01.) |
| Währungsumrechnung | **0,7 % Abschlag** auf realisierte Gewinne und Verluste, wenn die Profit-Währung des Symbols ≠ Kontowährung. Er mindert Gewinne und erhöht Verluste und wird beim Schließen fällig. Beim USD-Konto betrifft das 20 der 25 Instrumente; nicht betroffen sind EURUSD, GBPUSD, AUDUSD, NZDUSD, XAUUSD |

**Quellen:**
- https://ftmo.com/en/blog/trading-updates/trading-update-25-sep-2025/
- https://ftmo.com/en/blog/trading-updates/trading-update-11-sep-2025/
- https://ftmo.com/en/blog/trading-updates/trading-update-16-apr-2026/
- https://ftmo.com/en/blog/trading-updates/trading-update-26-sep-2024/
- https://ftmo.com/en/blog/trading-updates/trading-update-22-aug-2024/
- https://ftmo.com/en/blog/trading-updates/trading-update-18-jul-2024/
- https://ftmo.com/en/blog/trading-updates/trading-update-28-jul-2026/
- https://ftmo.com/au/blog/trading-updates/trading-update-3-sep-2026/
- https://ftmo.com/en/blog/trading-updates/trading-update-18-dec-2025/
- https://ftmo.com/en/faq/which-instruments-can-i-trade-and-what-strategies-am-i-allowed-to-use/ (30.09.2026)
- https://ftmo.com/en/forbidden-trading-practices/
- https://ftmo.com/en/trading-platforms/ (Server: FTMO-Demo/-Demo2/-Server…-Server5)
- https://www.fxempire.com/prop-firms/ftmo
- https://propvator.com/blog/ftmo-instruments/
- https://fxverify.com/tools/prop-firm-spreads/ftmo-2509
- https://ftmo.oanda.com/blog/trading-updates/trading-update-jan-28-2026/

## 7. Expert Advisors und verbotene Praktiken

**Grundsatz:** EAs und algorithmischer Handel sind erlaubt, wenn der Handel legitim ist, mit Risikomanagement arbeitet und am echten Markt replizierbar wäre. Ein Stop-Loss ist nicht Pflicht („We do not require you to use a Stop-loss“).

**Verboten laut Forbidden Trading Practices (geändert 12.10.2026):**
1. **Ausnutzen von Fehlern:** Preisanzeigefehler, verzögerte Kursupdates, langsame oder externe Feeds, und zwar „knowingly or unknowingly“. Darunter fällt Latenzarbitrage.
2. **Manipulative Trades** allein oder mit anderen, auch über verbundene Konten oder andere Anbieter. Gleichzeitige Gegenpositionen sind nur innerhalb eines einzelnen Kontos erlaubt; Hedging über mehrere Konten ist verboten.
3. **Software, KI, „ultra-high-speed tools“ oder Masseneingaben**, die einen unfairen Vorteil verschaffen. Das deckt HFT und Tick-Scalping ab; diese Begriffe werden nicht mehr wörtlich genannt.
4. **Gap Trading:** Eröffnen von Trades, (a) wenn große News, Makro-Events oder Earnings geplant sind und den Markt beeinflussen könnten, oder (b) „two hours or less before a relevant financial market is closed for at least two hours“. Eine Ausnahme für Swing wird nicht genannt.
5. **Overleveraging, Overexposure, One-sided Bets, Account Rolling.** Laut Blog fällt das Vergrößern der Position nach einer Verlustserie unter Overleveraging; mehrere USD-Paare gleichzeitig sind „one big dollar bet“.
6. **Hyperaktive EAs:** mehr als 2.000 Server-Requests pro Tag, gezählt über Eröffnen, Ändern und Schließen von Trades und Pending Orders.
7. **Gewinnverteilung über mehrere Tage ohne proportionale Risikoverteilung**, um Best Day oder Consistency zu umgehen (praktisch nur für 1-Step relevant).
8. **Risikomanagement-Regeln, jeweils relativ zu den eigenen Trades:**
   - keine deutlich größeren Positionen als sonst,
   - keine deutlich kleinere oder größere Positionsanzahl als sonst,
   - kein wiederholtes Aufstocken, das das „Risk per Trade Idea“ erhöht und kumulierte Exposure in einem oder korrelierten Symbolen aufbaut. Grid und Martingale werden nicht namentlich genannt, sind aber faktisch erfasst.
9. **Kein Fremdzugriff** und kein Handel durch Dritte auf dem Konto.

**Folgen:** Trades werden entfernt, der Plattformzugang gesperrt, man wird disqualifiziert oder verliert Rewards bis hin zur Vertragskündigung. In der Regel warnt FTMO zuerst, in schweren Fällen wird sofort gekündigt.

**Keine festen Grenzen:**
- Kein Maximalrisiko pro Trade und keine Lot-Obergrenze. FTMO: „does not set universal limits“ für Positionsgröße, Margin-Nutzung und Chance-Risiko-Verhältnis. Die Empfehlung von 1–1,5 % pro Trade ist „only a best practice“.
- **2-Step hat keine Consistency- und keine Best-Day-Regel** (FAQ vom 12.10.2026).

**Drittanbieter-EAs und Copy-Trading:** Identische oder sehr ähnliche Trades über mehrere Konten (auch aus Signalgruppen oder Copy-Diensten) werden zusammengerechnet. Die Obergrenze ist **400.000 USD pro Trader oder Strategie** vor Scaling. Bei Überschreitung droht die Sperre oder die Verweigerung des FTMO Accounts.

**Quellen:**
- https://ftmo.com/en/forbidden-trading-practices/
- https://ftmo.com/en/faq/which-instruments-can-i-trade-and-what-strategies-am-i-allowed-to-use/
- https://ftmo.com/en/faq/how-many-accounts-can-i-have/ (30.09.2026)
- https://ftmo.com/en/blog/why-ftmo-monitors-certain-patterns-in-trading-behaviour/ (12.10.2026)
- https://ftmo.com/en/blog/gambling-is-not-the-right-way-to-make-money/
- https://ftmo.com/en/faq/do-you-have-any-consistency-rules
- https://ftmo.com/en/blog/trading-updates/trading-update-8-oct-2026/

## 8. Nach dem Bestehen: FTMO Account (2-Step)

- **Regeln:** MDL 5 % und Max Loss 10 % statisch gelten weiter. Kein Profitziel, keine Mindesthandelstage.
- **Swing vs. Standard:** Im Standard-Konto gelten jetzt die News-Sperre und die Schließpflicht vor dem Wochenende; Verstöße können zur Kündigung führen. Swing ist frei.
- **Erster Reward:** am 14. Tag nach dem ersten Trade auf dem Konto oder später.
  - Vorher müssen alle Positionen **und Pending Orders** geschlossen sein.
  - FTMO prüft 1–2 Werktage; ausgezahlt wird 1–2 Werktage nach Freigabe der Rechnung.
  - Mindestbetrag 20 USD (Bank, Visa/Mastercard) bzw. 50 USD (Krypto).
- **Gewinnanteil:** standardmäßig 80 %; 90 % über den Scaling Plan oder das Premium Programme (Prime Status).
- **Auszahlungsrhythmus nach dem ersten Reward:** nicht explizit dokumentiert. Vermutlich startet die 14-Tage-Frist mit jedem neuen Konto neu [Inferenz].
- **Gebühr:** wird mit dem ersten Reward über die ursprüngliche Zahlungsart erstattet (nur 2-Step).
- **Scaling Plan:** alle 4 Monate +25 % Kontogröße, wenn in diesen 4 Monaten mindestens 10 % Nettogewinn, mindestens 2 ausgezahlte Rewards und eine positive Balance vorliegen. Bis maximal 2 Mio. USD.

**Quellen:**
- https://ftmo.com/en/faq/how-do-i-withdraw-my-profits/ (13.10.2026)
- https://ftmo.com/en/faq/is-the-entry-fee-refunded/ (06.10.2026)
- https://ftmo.com/en/scaling-plan/ (14.10.2026)
- https://ftmo.com/en/faq/what-are-the-benefits-of-prime-status/

## 9. Kosten

- **100k 2-Step:** Listenpreis **540 EUR**; die Gebühren werden in EUR berechnet.
- **Aktionspreis 439 EUR:** „Special Deal“ seit September 2025, nur ohne aktive gleichartige Challenge. Das ist laut Drittquellen mit Stand September/Oktober 2026 noch aktiv.
- **Swing-Preis:** Mehrere Drittquellen sagen „identisch mit Standard“. Laut PropTradingVibes gilt die öffentliche Preistabelle aber nur für Standard-Konten. **Den Swing-Preis vor dem Kauf im Konfigurator prüfen.**
- **Wiederholung:** Kein Free Retake mehr. Den Free Trial gibt es kostenlos und unbegrenzt oft: 14 Tage, halbiertes Ziel, 2 Mindesttage, endet nach 7 Tagen ohne Trade. Er eignet sich zum Test des EA auf FTMO-Servern.
- **Widerrufsrecht:** nur bis zum ersten Trade (AGB).

**Quellen:**
- https://ftmo.com/en/comparison-table/
- https://cryptoslate.com/prop-firms/ftmo-review/
- https://traderssecondbrain.com/guides/ftmo-review
- https://www.passproptradingfirms.com/best-prop-firms/ftmo-review/ftmo-account-prices/
- https://proptradingvibes.com/blog/ftmo-account-sizes-pricing
- https://ftmo.com/en/ftmo-free-trial/ (16.10.2026)

## 10. Statistiken

**FTMO veröffentlicht keine offizielle Bestehensquote je Phase.** Es gibt nur Aussagen und Gesamtzahlen:
- **CEO-Aussagen:** Im Forbes-CZ-Interview, das FTMO am 13.03.2026 veröffentlicht hat, antwortet Otakar Šuffner auf die Frage nach dem Anteil, der die Challenge besteht: „Eight to ten percent.“ Bei TradeInformer (13.03.2024) sagte er „only about 10%“.
- **Auszahlungen, von FTMO selbst gemeldet und nicht geprüft:**
  - September 2026: über 14,4 Mio. USD bei etwa 7.100 Rewards.
  - August 2026: über 15,2 Mio. USD bei mehr als 7.500 Rewards.
  - Über 200 Mio. USD in 12 Monaten; insgesamt über 650 Mio. USD.
  - Widerspruch: Im Forbes-Interview ist von 500 Mio. USD die Rede.
- **2021 (FTMO-Blog):** über 960.000 Konten und 29 Mio. USD Auszahlungen.
- **Verification-Quote:** Es gibt nur unbelegte Schätzungen von Drittseiten (40–70 %).

**Quellen:**
- https://ftmo.com/en/blog/forbes-the-ftmo-cover-story/
- https://tradeinformer.com/interviews/ftmo-ceo-we-can-bring-something-new-to-the-broker-space
- https://coinspectator.com/mainstream/2026/10/08/ftmo-adds-200-million-to-lifetime-payouts-in-one-year-as-monthly-rewards-near-15-million/
- https://ftmo.com/en/blog/year-2021-in-numbers/
- https://coinlaw.io/ftmo-statistics/

## 11. Sonstiges, das der EA beachten muss

- **Bei Erreichen eines Limits** schließt die Plattform sofort alle Positionen; es gibt keine Karenz. Geprüft wird in Echtzeit auf Equity.
- **Rundung:** nicht dokumentiert, ebenso ob Equity = Limit schon als Verstoß gilt.
- **Spreadspitzen:** Ob FTMO Verstöße durch Spreadspitzen oder Fehlticks zurücknimmt, ist nicht dokumentiert. FTMO US warnt, dass sich Spreads und Liquidität um den Rollover stark ändern.
- **Wochenend-Gaps** (FTMO-Daten, ca. 2021, 55 Wochen, Durchschnitt/Maximum in Pips): EURUSD 8,3/37,6; GBPUSD 16,9/113,1; GBPJPY 21,6/104,8; EURCHF 8,7/36,3; XAUUSD 27,2/153,9 (Einheit unklar). Die größten Gaps lagen beim 4- bis 6-Fachen des Durchschnitts. Stop-Losses greifen bei einem Gap nicht zum gesetzten Kurs.
- **Samstags-Wartung:** Trading ist dann deaktiviert. Der EA muss Neustarts und Verbindungsabbrüche robust überstehen.
- **Neues Konto pro Phase:** Jede Phase und jeder Reward bringt ein neues MT5-Konto mit eigenem Login. Der EA muss seinen Zustand dann zurücksetzen.

**Quelle zu den Gaps:** https://ftmo.com/en/blog/holding-trades-over-the-weekend/

---

## (a) Checkliste: Was der EA technisch einhalten bzw. implementieren muss

**Zeit**
1. **Zeitbasis:** UTC ermitteln. Server-Offset = +2 h, plus 1 h während der US-Sommerzeit (2. Sonntag im März 07:00 UTC bis 1. Sonntag im November 06:00 UTC). Prag-Offset = +1 h, plus 1 h während der EU-Sommerzeit (letzter Sonntag im März bis letzter Sonntag im Oktober, jeweils 01:00 UTC).
2. **FTMO-Tag = Prager Kalendertag.** Der Reset liegt um 01:00 Serverzeit, in den Lückenwochen um 02:00. Gegen den Tooltip in Account MetriX validieren, besonders vom 26.10. bis 01.11.2026.

**Verlustgrenzen**

3. **Referenzbalance B_ref** aus der Deal-Historie rekonstruieren: Summe aus Profit, Commission, Swap und Fee aller Deals vor dem Reset-Zeitpunkt. Das ist robust gegen Neustarts. Am ersten Tag gilt B_ref = 100.000.
4. **Floor** = max(B_ref − 5.000; 90.000).
5. **Konservative Equity** E* = ACCOUNT_EQUITY − geschätzte Schließkommission − 0,7 % × Floating-Verluste bei Symbolen mit Profit-Währung ≠ USD − Puffer für Spread und Slippage.
6. **Kill-Switch** bei E* ≤ Floor + Puffer: alles schließen und bis zum nächsten Prager Tag sperren. Weiche Stufen davor einbauen.
7. **Prüfung vor jedem Trade:** Das Risiko bis zum SL aller offenen Positionen plus der neuen Position, plus Kommission, plus 0,7 %-Zuschlag, plus Gap- und Slippage-Reserve muss kleiner sein als E* − Floor − Sicherheitsmarge. Positionen über Nacht und Wochenende einrechnen.
8. **Wochenende:** Kumuliertes Risiko inklusive Gap-Reserve gegen den Sonntagsspielraum begrenzen. Keine neuen Einstiege in den letzten 2 h vor dem Freitagsschluss und vor Feiertagspausen von mindestens 2 h (konservative Auslegung des Gap-Trading-Verbots).
9. **Rollover-Fenster** um 00:00 Serverzeit meiden: keine Einstiege, enge Stops vermeiden. Bei Gold liegt die Pause etwa zwischen 23:50 und 01:00 Serverzeit.

**Ziele und Fristen**

10. **Handelstage:** die Prager Daten aller Eröffnungs-Deals (DEAL_ENTRY_IN) zählen; mindestens 4 je Phase.
11. **Profitziel:** Wenn E* ≥ Ziel + Puffer und 4 Tage erreicht sind: alles schließen, Pending Orders löschen, Balance prüfen (≥ 110.000 bzw. ≥ 105.000), danach nicht mehr handeln.
12. **Inaktivität:** spätestens alle 25 Tage einen Trade eröffnen [Empfehlung]. Neue Phasen innerhalb von 30 Tagen aktivieren.

**Server- und Kontogrenzen**

13. **Request-Budget:** alle OrderSend-Aufrufe zählen (Eröffnen, Ändern, Schließen, Pendings) und hart unter 2.000 pro Tag deckeln. Kein Trailing pro Tick. Höchstens 200 Orders und Positionen gleichzeitig.
14. **Margin** per OrderCalcMargin berechnen (FX 1:30, XAU 1:15). Stop-Out liegt bei 50 %; Hedge-Margin zählt doppelt.
15. **Kontomodus** zur Laufzeit prüfen: ACCOUNT_MARGIN_MODE (Hedging oder Netting).
16. **Symbole zur Laufzeit auflösen**, inklusive Suffix. Aus der Spezifikation lesen: CONTRACT_SIZE, VOLUME_MIN/MAX/STEP, TICK_VALUE, CURRENCY_PROFIT (für die 0,7 %-Logik), SWAP_LONG/SHORT, SWAP_ROLLOVER3DAYS, Stops- und Freeze-Level, Handelssessions.

**Kosten und Risiko**

17. **Kostenmodell:** FX 5 USD Round Turn pro Lot; Metalle 0,0014 % Round Turn vom Nominal; Volume Bands; 0,7 % auf realisierte Ergebnisse.
18. **Risikoregeln:** kein Martingale, kein Grid und kein Nachkaufen ins Minus. Netto-Exposure pro Währung, etwa USD, über korrelierte Paare begrenzen. Positionsgrößen konsistent halten.
19. **Phasenwechsel** über ACCOUNT_LOGIN erkennen und den Zustand zurücksetzen. Vor einer Reward-Anfrage das Konto komplett flach stellen.
20. **Ausführung:** keine Ausnutzung veralteter Kurse, kein Hedging über mehrere Konten, insgesamt höchstens 400.000 USD Kapital pro Strategie.

## (b) Offene Punkte, die im Client-Bereich oder beim Support zu klären sind

1. **Swing-Preis** für 100k im Konfigurator: 540 EUR oder 439 EUR, oder ein Aufschlag?
2. **AGB-Wortlaut** (12.10.2026): Klausel 13.2.3 (30 Tage ohne Trade; Verlust 8–10 % länger als 30 Tage) und ab wann der 0,7 %-Abschlag für eine jetzt gekaufte Challenge gilt.
3. **Gap Trading vs. Swing:** Ist das Eröffnen von Trades vor High-Impact-News oder in den letzten 2 h vor dem Wochenende auf einem Swing-Konto bzw. in der Challenge erlaubt? Die News-FAQ sagt „frei“, die Forbidden Trading Practices sagen wörtlich „verboten“.
4. **MT5-Kontomodus** (Hedging oder Netting); ob Kommissionen beim Eröffnen und beim Schließen belastet werden; ob die FTMO-Equity die künftige Schließkommission schon einrechnet.
5. **Reale Handelszeiten** (FX und XAUUSD), Tag des dreifachen Swaps, Swap-Sätze, Symbolnamen und Maximalvolumen pro Order. Am besten im Free Trial auslesen.
6. **Handelstage:** Zählt das Auslösen einer Pending Order als Eröffnung? Werden Micro-Trades, die nur der Tageszählung dienen, toleriert?
7. **Grenzfälle am Limit:** Ist Equity = Limit schon ein Verstoß? Wie wird gerundet? Wie geht FTMO mit Verstößen durch Spreadspitzen beim Rollover um? Wie aktuell ist Account MetriX im Vergleich zur serverseitigen Prüfung?
8. **Volume Bands auf ftmo.com:** Bandgrenzen pro Symbol, Fill-or-Kill bzw. Teilausführungen, und ob das Aufteilen von Orders in kleinere Stücke zulässig ist.
9. **Auszahlungsrhythmus** nach dem ersten Reward.
10. **Autonomer EA:** Bestätigung, dass die Klausel zu „AI/ultra-high-speed tools“ einen selbst entwickelten, autonomen EA nicht erfasst.
11. **Reset in der Lückenwoche** (26.10.–01.11.2026): per Tooltip prüfen, ob er tatsächlich um 02:00 Serverzeit liegt.
