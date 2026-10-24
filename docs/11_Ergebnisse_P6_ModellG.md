# Ergebnisse P6 – Modell G „Trendfolge D1“

Stand: 24.10.2026

Grundlagen:
- Regeln: unverändert aus der Vorregistrierung `docs/10_P6_Vorregistrierung_ModellG.md`
- Code: `research/smc/strategy_g.py`, Lauf `research/scripts/run_p6.py`; 63 Tests grün, darunter der History-Invarianz-Test von Modell G
- In-Sample: Handelstage 01.01.2015–31.12.2023, 25 Instrumente, Warm-up 2014
- Vollständige Tabellen: `research/results/p6_modell_g_in_sample.md`

## 1. Ergebnis

**Modell G verfehlt alle vier Kriterien. P6 ist damit gescheitert.** Der Hold-out 2024–2026 bleibt unberührt, T14 und T15 entfallen.

| Kriterium | Schwelle | Modell G |
|---|---|---|
| t-Wert (kleinster aus iid, Woche, Monat) | ≥ 3,0 | **−1,77** |
| Sharpe Ratio p. a. netto | (≈ 1,0) | **−0,53** |
| Jahre positiv | ≥ 6 von 9 | **1 von 9** (nur 2022) |
| Instrumente positiv | ≥ 15 von 25 | **6 von 25** |
| bei doppelten Kosten | > 0 | **−9,3 % p. a.** |

Auf 10 % Portfolio-Volatilität skaliert: −5,3 % p. a., maximaler Drawdown 53 %.

## 2. Einordnung

1. **Schon vor Kosten kein Trend-Ertrag.**
   - Allein die Kursergebnisse ergeben eine Sharpe Ratio von −0,18.
   - Bei G10-FX und Gold folgten 2015–2023 auf Trends im Mittel keine Fortsetzungen, die ein 1/3/12-Monats-Signal hätte nutzen können.
2. **Swaps machen es deutlich schlechter.**
   - Kosten p. a. bei 10 % Portfolio-Volatilität:

     | Posten | Kosten p. a. |
     |---|---|
     | Handelskosten | 0,84 % |
     | Swaps netto | 2,43 % |
     | 0,7-%-Gebühr | 0,21 % |

   - Das Portfolio hält im Mittel etwa das 2,4-Fache des Kapitals als Nominalwert. Der angenommene Swap-Aufschlag von 1 % p. a. je Position kostet damit allein rund 2,4 % p. a.; die Zinsdifferenzen gleichen sich im Mittel fast aus.
   - Das Urteil hängt aber nicht an dieser Annahme: Schon ohne Kosten ist das Ergebnis negativ.
3. **Kein Fehler im Code.**
   - Eine unabhängige Nachrechnung der Kursergebnisse aus Positionen und Kursen stimmt überein.
   - Eine einfache 12-Monats-Regel auf EURUSD ergibt ebenfalls eine negative Sharpe Ratio (−0,12).
4. **Wo es lief:**
   - Positiv waren nur USDJPY, GBPJPY, CADJPY (Yen-Schwäche 2021–2023), EURCHF und GBPUSD.
   - Am schlechtesten liefen die CHF- und CAD-Crosses (CADCHF −0,76, USDCHF −0,71).
5. **Passt zur Literatur:** Die Belege für Trendfolge stammen vor allem aus breiten Futures-Portfolios mit Aktienindizes, Anleihen und Rohstoffen. Währungstrends gelten seit etwa 2010 als schwach.

## 3. Gesamtbild nach P2–P6

| Phase | Hypothese | Ergebnis |
|---|---|---|
| P2 | 13 SMC-Bausteine einzeln | kein Baustein nach Kosten profitabel |
| P3 | Modell C: SMC-Trend-Fortsetzung | +0,015 R bzw. −0,016 R pro Trade |
| P4 | Modell D: Trendfolge mit Struktur-Exit | −0,040 R pro Trade |
| P5 | Modell F: Fix-Reversal (Journal of Finance 2024) | Effekt vorhanden, aber nur so groß wie die Kosten (Sharpe 0,31) |
| P6 | Modell G: Trendfolge D1 | Sharpe −0,53, schon vor Kosten negativ |

- Fünf vorregistrierte Tests über drei Strategieklassen: SMC, Intraday-Saisonalität und Trendfolge. Keiner zeigt auf G10-FX und Gold einen Vorteil, der nach FTMO-Kosten trägt.
- Der Hold-out 2024–2026 wurde nie angefasst.
- Die Pipeline ist validiert: Sie reproduziert den publizierten Fix-Effekt in der Größenordnung des Papers.

## 4. Empfehlung

**Projekt beenden bzw. pausieren und keine Challenge kaufen.** Ohne nachgewiesenen Vorteil liegt die Bestehenschance bei etwa 35–42 %. Das ist ein Glücksspiel mit der Gebühr als Einsatz.

**Was bleibt:**
- Daten und Zeitmodell
- kausale Engine
- Kosten- und Swap-Modell
- Testkette aus Vorregistrierung, In-Sample, einmaligem Hold-out und FTMO-Bootstrap
- unberührter Hold-out

Falls später eine neue Idee kommt, kann sie in wenigen Stunden sauber geprüft werden.

**Denkbar, aber außerhalb des bisherigen Rahmens:** Trendfolge ist in breiten Portfolios mit Indizes, Rohstoffen und Anleihen am besten belegt. FTMO bietet Indizes und Rohstoffe an. Das wäre ein neues Projekt mit neuen Daten und eigener Vorregistrierung, keine Fortsetzung der FX-Liste.

## 5. Trial-Log (Fortsetzung)

| # | Datum | Test | Ergebnis |
|---|---|---|---|
| T13 | 24.10.2026 | Modell G, In-Sample | nicht bestanden: Sharpe −0,53, t −1,77, 1 von 9 Jahren positiv |
| T14 | – | Hold-out | entfällt, Hold-out unberührt |
| T15 | – | FTMO-Bootstrap | entfällt |

Bisher verbraucht: T1 (Ereignisstudie, 110 Hypothesen), T2, T3, T6, T9, T10 und T13. Der Hold-out 2024–2026 ist für keinen dieser Tests verwendet worden.
