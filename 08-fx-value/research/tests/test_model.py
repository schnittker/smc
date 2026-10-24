import numpy as np
import pytest

from fval import RAW_DIR
from fval.model import CPI, LAG, cpi_table, fx_month_end, ranking, real_rates, value_signal

LAST = 2023 * 12 + 11


def test_cpi_table_quarterly_and_japan_extension():
    cpi = cpi_table(RAW_DIR, LAST)
    assert set(cpi) == set(CPI) and all(np.isfinite(v[2014 * 12:]).all() for v in cpi.values())
    aud = cpi["AUD"]
    assert aud[2018 * 12 + 3] == aud[2018 * 12 + 5] and aud[2018 * 12 + 3] != aud[2018 * 12 + 2]   # Q1 from April
    jp = cpi["JPY"]
    assert jp[2022 * 12 + 1] / jp[2022 * 12] == pytest.approx((1 - 0.0023335) ** (1 / 12), rel=1e-6)   # 2021 rate


def test_fx_orientation_and_real_rate():
    fx = fx_month_end(RAW_DIR, LAST)
    assert 0.005 < fx["JPY"][2020 * 12] < 0.012 and 1.0 < fx["EUR"][2020 * 12] < 1.3        # USD per unit
    q = real_rates(RAW_DIR, LAST)
    assert np.isfinite(q["EUR"][2014 * 12:]).all() and (q["USD"] == 0).all()


def test_ranking_orders_cheap_first():
    q = {c: np.zeros(LAST + 1) for c in ("USD", "EUR", "GBP", "JPY", "AUD", "CAD", "NZD", "CHF")}
    q["JPY"][LAST - 1] = -0.3                                             # yen fell 30 % in real terms -> cheapest
    q["CHF"][LAST - 1] = 0.2                                              # franc rose -> most expensive
    r = ranking("V-5Y", q, LAST - 1)
    assert r[0] == "JPY" and r[-1] == "CHF"
