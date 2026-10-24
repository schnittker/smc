from datetime import date

import numpy as np
import pytest

from smc.swaps import RateTable
from ffx.model import currencies, per_event, run_model_f, short_usd_sign

EPOCH = date(1970, 1, 1)
RATES = RateTable.constant({"USD": 0.05, "EUR": 0.02, "GBP": 0.055, "JPY": 0.0, "AUD": 0.045, "CAD": 0.051,
                            "NZD": 0.06, "CHF": 0.01})


def dn(y, m, d):
    return (date(y, m, d) - EPOCH).days


def test_signs_and_carry_selection():
    assert short_usd_sign("EURUSD") == 1 and short_usd_sign("USDJPY") == -1
    assert currencies("F-CARRY", RATES, dn(2023, 6, 14)) == ["NZD", "GBP", "CAD"]
    assert len(currencies("F-USD", RATES, dn(2023, 6, 14))) == 7


def _pxs(days):
    out = {}
    rng = np.random.default_rng(0)
    for k, sym in enumerate(("EURUSD", "GBPUSD", "AUDUSD", "NZDUSD", "USDJPY", "USDCAD", "USDCHF")):
        p = (1 + k) * np.exp(np.cumsum(rng.normal(0, 0.005, len(days))))
        out[sym] = {"day": days, "p_sig": p, "p_mark": p, "exact": np.ones(len(days), bool),
                    "lo": p * 0.999, "hi": p * 1.001}
    return out


def test_one_event_round_trip():
    days = np.array([d for d in range(dn(2023, 1, 2), dn(2023, 7, 1)) if (d + 3) % 7 < 5])
    pxs = _pxs(days)
    t = dn(2023, 6, 14)                                       # Wednesday
    rows, log = run_model_f("F-USD", pxs, np.array([t]), RATES)
    assert log[0][0] == dn(2023, 6, 13) and len(log[0][2]) == 7
    held = rows[rows["w"] != 0]
    assert set(held["day"].tolist()) == {dn(2023, 6, 13)}
    assert (held["w"][held["symbol"] == "EURUSD"] > 0).all() and (held["w"][held["symbol"] == "USDJPY"] < 0).all()
    d, net, cost = per_event(rows, log)
    assert d.tolist() == [t] and cost[0] > 0
    sel = np.isin(rows["day"], [dn(2023, 6, 13), t])
    assert net[0] == pytest.approx(rows["net"][sel].sum())
