# ea – Strategietests für einen autonomen MT5-EA (FTMO 2-Step)

Jeden Tag wird eine Strategie aus [STRATEGIEN.md](STRATEGIEN.md) getestet, bis eine die FTMO-Challenge realistisch besteht. Alle Versuche stehen im globalen [TRIAL_LOG.md](TRIAL_LOG.md).

**Feste Rahmenbedingungen:** MT5-EA, vollständig autonom; FTMO 2-Step Swing, 100.000 USD; max. Verlust 10 %, max. Tagesverlust 5 %; Ziele +10 % / +5 %; News und Wochenende erlaubt.

**Vorgehen je Strategie:** Recherche → Vorregistrierung (Commit vor Code und Daten) → Code und Tests (Commit vor dem ersten Lauf) → In-Sample 2015–2023 → Hold-out 2024–2026 einmalig und nur, wenn In-Sample besteht → FTMO-Bootstrap.

| Ordner | Strategie (Nr.) | Status |
|---|---|---|
| [smart-money-concept/](smart-money-concept/) | SMC (1), Fix-Reversal (2), Trendfolge FX/Gold (3), Trendfolge Indizes/Rohstoffe (4); enthält die gemeinsame Pipeline (Daten, Zeitmodell, Kosten, Statistik) | gescheitert |
| [05-monatsend-rebalancing/](05-monatsend-rebalancing/) | Monatsend-Rebalancing am London-Fix (5) | gescheitert |
| [06-fx-carry/](06-fx-carry/) | FX Carry G8 (6) | gescheitert |
| [07-fx-momentum/](07-fx-momentum/) | FX Querschnitts-Momentum G8 (7) | gescheitert |
| [09-pre-fomc-drift/](09-pre-fomc-drift/) | Pre-FOMC-Drift (9) | knapp gescheitert (t 2,4), Ensemble-Kandidat |
| [10-turn-of-the-month/](10-turn-of-the-month/) | Turn-of-the-Month US500 (10) | gescheitert |
| [11-intraday-momentum/](11-intraday-momentum/) | Intraday-Momentum US500 (11) | gescheitert |
| [12-overnight-drift/](12-overnight-drift/) | Overnight-Drift US500 (12) | gescheitert |
| — | Tageszeit-Effekt FX (13) | durch Nr. 2 abgedeckt, kein eigener Test |
| [14-vol-managed-index/](14-vol-managed-index/) | Vol-gesteuertes US500-Long (14) | gescheitert |
| [15-short-term-reversal/](15-short-term-reversal/) | Kurzfrist-Reversal US500, Connors (15) | gescheitert |
| [16-opening-range-breakout/](16-opening-range-breakout/) | Opening Range Breakout 5 min (16) | gescheitert |
| — | Lead-Lag US → Asien (17) | strukturell nicht handelbar (CFDs handeln während der US-Sitzung), kein eigener Test |
| [18-cot-positionierung/](18-cot-positionierung/) | COT-Extreme (18) | gescheitert |
| [19-vix-regime/](19-vix-regime/) | VIX-Regime (19) | gescheitert |
| [20-zins-momentum/](20-zins-momentum/) | Zins-Momentum G8 (20) | gescheitert |
| [21-pairs-mean-reversion/](21-pairs-mean-reversion/) | z-Score Mean Reversion AUDNZD / EURCHF (21) | gescheitert |

Kursdaten (≈ 4 GB) liegen unter `smart-money-concept/data/` und sind nicht im Repo; Neuaufbau siehe `smart-money-concept/README.md`.
