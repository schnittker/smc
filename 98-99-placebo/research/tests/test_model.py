import numpy as np
import pytest

from plc.model import SYNODIC, moon_age, random_signals


def test_random_signal_rate_and_balance():
    s = random_signals(300_000, 1)
    assert (s != 0).mean() == pytest.approx(1 / 30, rel=0.03)
    assert (s == 1).sum() == pytest.approx((s == -1).sum(), rel=0.05)


def test_moon_age_known_dates():
    t = lambda iso: (np.datetime64(iso) - np.datetime64("1970-01-01T00:00:00")).astype("timedelta64[s]").astype(np.int64)
    assert moon_age(np.array([t("2024-01-11T11:57:00")]))[0] == pytest.approx(0.0, abs=0.6) or \
        moon_age(np.array([t("2024-01-11T11:57:00")]))[0] == pytest.approx(SYNODIC, abs=0.6)    # new moon 11.01.2024
    assert moon_age(np.array([t("2024-01-25T17:54:00")]))[0] == pytest.approx(SYNODIC / 2, abs=1.0)  # full moon
