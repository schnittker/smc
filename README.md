# ea – Strategietests für einen autonomen MT5-EA (FTMO 2-Step)

Jeden Tag wird eine Strategie aus [STRATEGIEN.md](STRATEGIEN.md) getestet, bis eine die FTMO-Challenge realistisch besteht. Alle Versuche stehen im globalen [TRIAL_LOG.md](TRIAL_LOG.md).

**Feste Rahmenbedingungen:** MT5-EA, vollständig autonom; FTMO 2-Step Swing, 100.000 USD; max. Verlust 10 %, max. Tagesverlust 5 %; Ziele +10 % / +5 %; News und Wochenende erlaubt.

**Vorgehen je Strategie:** Recherche → Vorregistrierung (Commit vor Code und Daten) → Code und Tests (Commit vor dem ersten Lauf) → In-Sample 2015–2023 → Hold-out 2024–2026 einmalig und nur, wenn In-Sample besteht → FTMO-Bootstrap.

| Ordner | Strategie (Nr.) | Status |
|---|---|---|
| [smart-money-concept/](smart-money-concept/) | SMC (1), Fix-Reversal (2), Trendfolge FX/Gold (3), Trendfolge Indizes/Rohstoffe (4); enthält die gemeinsame Pipeline (Daten, Zeitmodell, Kosten, Statistik) | gescheitert |
| [05-monatsend-rebalancing/](05-monatsend-rebalancing/) | Monatsend-Rebalancing am London-Fix (5) | gescheitert |
| [06-fx-carry/](06-fx-carry/) | FX Carry G8 (6) | gescheitert |

Kursdaten (≈ 4 GB) liegen unter `smart-money-concept/data/` und sind nicht im Repo; Neuaufbau siehe `smart-money-concept/README.md`.
