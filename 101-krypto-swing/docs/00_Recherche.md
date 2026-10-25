# Recherche: Krypto-Swing-Trendfolge (Strategie Nr. 101)

Stand 25.10.2026. Wunsch des Nutzers: nur Swing-Trades, autonomer EA, alle FTMO-Instrumente. Krypto ist die einzige FTMO-Marktklasse, die in der Reihe noch nicht getestet wurde; HistData hat dafür keine Kurse.

## FTMO-Bedingungen für Krypto-CFDs (laut Recherche, im EA zu verifizieren)

- **Angebot:** rund 30 Krypto-CFDs, darunter BTC, ETH, SOL, XRP, DOGE
- **Hebel:** im **Swing-Konto 1:1** (Standard 1:3,33). Die Summe der Krypto-Nominale darf also höchstens etwa dem Kapital entsprechen.
- **Handel:** auch am Wochenende, mit wöchentlichen Wartungsfenstern je Plattform
- **Kommission:** etwa 0,065 % je Trade, also 0,0325 % je Seite
- **Spreads:** variabel. 2020 nannte FTMO für BTC etwa 0,25 %, heute sind sie deutlich enger.
- **Swaps:** öffentlich nicht gelistet. Bei anderen Brokern liegen sie für BTC bei etwa 20 % p. a. in beide Richtungen (FxPro) bzw. −23 % long / +1,7 % short (OW Markets). Für Trendfolge ist das der **größte Kostenblock**.

Quellen: FTMO Symbols-Seite, FTMO-FAQ Swing-Konto, LuxAlgo, HyroTrader, Propvator, Broker-Swapseiten (Stand Okt. 2026).

## Literatur zur Krypto-Trendfolge

- **Liu & Tsyvinski (2021), „Risks and Returns of Cryptocurrency“, RFS:** starkes Zeitreihen-Momentum bei BTC auf 1–4 Wochen
- **Liu, Tsyvinski & Wu (2022), „Common Risk Factors in Cryptocurrency“, JF:** Querschnitts-Momentum
- **Hudson & Urquhart (2021):** technische Handelsregeln in Krypto profitabel, aber abnehmend
- **Grobys, Ahmed & Sapkota (2020):** Gleitende-Durchschnitte-Regeln funktionieren in Krypto vor allem in frühen, illiquiden Phasen

Der Konsens: Der Effekt war bis etwa 2019 stark und ist seitdem kleiner. Kosten und Finanzierung (Swaps) zehren viel davon auf.

## Daten

Binance-Spot (USDT) Tageskerzen 00:00 UTC über die öffentliche API bzw. data.binance.vision. Der USDT-Kurs weicht vom FTMO-USD-CFD nur wenig ab. FTMO-Kurse selbst sind nicht verfügbar.

**Listungsdaten bei Binance:**
- BTC und ETH: 08/2017
- LTC: 12/2017
- ADA: 04/2018
- XRP: 05/2018

Neuere Coins wie SOL (2020), DOGE (2019) oder DOT (2020) hätten keinen vollständigen IS-Zeitraum.

## Bekannte Probleme

- Der Effekt ist laut Literatur gealtert. Ein IS ab 2018 enthält noch die Spätphase der Blase.
- Die Swap-Höhe bei FTMO ist unbekannt, deshalb wird mit pessimistischen 20 % p. a. gerechnet.
- Der FTMO-Tagesbeginn liegt bei 00:00 Prag (22/23 Uhr UTC), die Binance-Tagesgrenze bei 00:00 UTC. Das sind 1–2 Stunden Versatz.
