"""Trade-list statistics for the pre-registered acceptance checks (P4 onwards)."""
from __future__ import annotations

import numpy as np

from smc import timez
from smc.config import SYMBOLS
from smc.report import cluster_bootstrap_ci, cluster_t, profit_factor
from smc.swaps import month_index


def years_of(t: np.ndarray) -> np.ndarray:
    return np.asarray(t, dtype="datetime64[s]").astype("datetime64[Y]").astype(int) + 1970


def clusters(t_entry: np.ndarray) -> dict[str, np.ndarray]:
    """Entry day (FTMO day), entry week and entry month of every trade."""
    day = timez.ftmo_day(t_entry)
    return {"Tag": day, "Woche": (day + 3) // 7, "Monat": month_index(t_entry)}


def trade_stats(tr: dict, years) -> dict:
    """Mean, t-values (iid and clustered), profit factor, yearly and per-symbol means of net_r."""
    x, cost = tr["net_r"], tr["cost_r"]
    n = len(x)
    m = {"n": n, "E": float(x.mean()), "sd": float(x.std(ddof=1)), "cost": float(cost.mean()),
         "E_2x": float((x - cost).mean()), "pf": profit_factor(x), "win": float((x > 0).mean()),
         "t_iid": float(x.mean() / (x.std(ddof=1) / np.sqrt(n)))}
    m["t_cl"] = {name: cluster_t(x, cl) for name, cl in clusters(tr["t_fill"]).items()}
    m["t"] = min([m["t_iid"], *m["t_cl"].values()])
    yr = years_of(tr["t_sig"])
    m["by_year"] = {y: (int((yr == y).sum()), float(x[yr == y].mean()) if (yr == y).any() else np.nan) for y in years}
    m["years_pos"] = sum(1 for k, e in m["by_year"].values() if k and e > 0)
    m["by_symbol"] = {s: (int((tr["symbol"] == s).sum()), float(x[tr["symbol"] == s].mean()))
                      for s in SYMBOLS if (tr["symbol"] == s).any()}
    elig = [v for v in m["by_symbol"].values() if v[0] >= 10]
    m["sym_eligible"], m["sym_pos"] = len(elig), sum(1 for v in elig if v[1] > 0)
    m["sym_share"] = m["sym_pos"] / len(elig) if elig else np.nan
    return m


def in_sample_checks(m: dict, years, e_min=0.10, t_min=3.0, pf_min=1.2, years_min=6, sym_min=0.6) -> list:
    return [
        (f"Netto-Erwartungswert ≥ +{e_min:.2f} R".replace(".", ","), f"{m['E']:+.3f} R", m["E"] >= e_min),
        (f"t-Wert ≥ {t_min:.1f} (kleinster aus iid / Tag / Woche / Monat)".replace(".", ","), f"{m['t']:.2f}",
         m["t"] >= t_min),
        (f"Netto-Profit-Factor ≥ {pf_min:.1f}".replace(".", ","), f"{m['pf']:.2f}", m["pf"] >= pf_min),
        (f"≥ {years_min} von {len(years)} Jahren positiv", f"{m['years_pos']} von {len(years)}",
         m["years_pos"] >= years_min),
        (f"≥ {sym_min:.0%} der Instrumente (≥ 10 Trades) positiv",
         f"{m['sym_pos']} von {m['sym_eligible']} ({m['sym_share']:.0%})", m["sym_share"] >= sym_min),
        ("bei doppelten Kosten > 0", f"{m['E_2x']:+.3f} R", m["E_2x"] > 0),
    ]


def holdout_checks(m_ho: dict, is_tr: dict, m_is: dict) -> tuple[list, tuple[float, float]]:
    lo, hi = cluster_bootstrap_ci(is_tr["net_r"], month_index(is_tr["t_fill"]))
    checks = [("Netto-Erwartungswert > 0", f"{m_ho['E']:+.3f} R", m_ho["E"] > 0),
              ("Netto-Profit-Factor > 1,1", f"{m_ho['pf']:.2f}", m_ho["pf"] > 1.1),
              ("≥ untere 95-%-Grenze von In-Sample (Cluster nach Einstiegsmonat)",
               f"{m_ho['E']:+.3f} R vs. IS {m_is['E']:+.3f} R [{lo:+.3f}; {hi:+.3f}]", m_ho["E"] >= lo)]
    return checks, (lo, hi)
