# Recherche: Währungsstärke intraday und USD-Basket Mean Reversion

Stand: 24.10.2026

## 1. Idee

Aus den USD-Paaren lässt sich für jede der 8 Hauptwährungen eine Stärke gegenüber dem Durchschnitt ableiten (synthetische Währungsindizes).

- **Nr. 46 Währungsstärke-Ranking:** Die in einer Sitzung stärkste Währung bleibt in der nächsten Sitzung stark, die schwächste schwach (Intraday-Momentum über Sitzungen). Gehandelt wird das Paar stärkste gegen schwächste Währung.
- **Nr. 47 USD-Basket Mean Reversion:** Läuft ein einzelnes USD-Paar stark vom Gleichlauf der übrigen Währungen weg, also mit einer währungsspezifischen Bewegung, kehrt diese Abweichung zurück.

## 2. Quellen

| Quelle | Inhalt |
|---|---|
| Praxis (Currency-Strength-Meter, „Strongest vs. Weakest“) | weit verbreitet, keine geprüften Netto-Belege |
| Ranaldo (2009), *J. Int. Money and Finance* | Saisonale Intraday-Muster von FX-Renditen je Sitzung (Heimatwährung schwächer in der Heimsitzung) |
| Breedon & Ranaldo (2013) | Systematische Sitzungseffekte bei Majors |
| Menkhoff et al. (2012) | Querschnitts-Momentum über Monate, kurzfristige Umkehr |

## 3. Bezug zu früheren Tests

Querschnitts-Momentum über Monate (Nr. 7) ist gescheitert, ebenso Mean Reversion auf H1 (Nr. 37, 39) und das Asien-Range-Fading (Nr. 32). Die Kosten der Crosses sind hoch (0,6–2 Pip).

## 4. Einschätzung vor dem Test

**Erwartung: Scheitern aller drei Varianten.**
