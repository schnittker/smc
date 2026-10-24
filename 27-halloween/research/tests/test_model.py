import numpy as np

from hallo.model import targets


def test_targets_first_trading_day_of_november_and_may():
    days = np.array([d for d in range(16374, 16374 + 800) if (d + 3) % 7 < 5])    # from 2014-10-31
    px = {"day": days, "exact": np.ones(len(days), bool)}
    t = targets(px)
    got = [(str(np.datetime64(d, "D")), w) for d, w in sorted(t.items())]
    assert got[0] == ("2014-11-03", 1.0) and got[1] == ("2015-05-01", 0.0) and got[2] == ("2015-11-02", 1.0)
