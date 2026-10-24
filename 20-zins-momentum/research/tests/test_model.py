from smc.swaps import RateTable
from zmom.model import ranking


class Table(RateTable):
    """Rates that change linearly per month with a currency-specific slope."""
    def __init__(self, level, slope):
        self.level, self.slope = level, slope

    def rate(self, ccy, month):
        return self.level[ccy] + self.slope[ccy] * month


LEVEL = {"USD": 0.05, "EUR": 0.02, "GBP": 0.04, "JPY": 0.0, "AUD": 0.03, "CAD": 0.03, "NZD": 0.04, "CHF": 0.01}


def test_ranking_by_change_not_level():
    slope = {"USD": 0.0, "EUR": 0.002, "GBP": 0.0, "JPY": 0.001, "AUD": -0.001, "CAD": 0.0, "NZD": -0.002, "CHF": 0.0}
    r = ranking(Table(LEVEL, slope), 600, 12)
    assert r[:2] == ["EUR", "JPY"] and r[-2:] == ["AUD", "NZD"]
    # equal change: higher level first, then alphabetical
    assert r[2:6] == ["USD", "GBP", "CAD", "CHF"]


def test_ranking_lag_matters():
    class Step(RateTable):
        def __init__(self):
            pass

        def rate(self, ccy, month):
            if ccy == "EUR":
                return 0.02 + (0.01 if month >= 598 else 0.0)        # hike 2 months ago
            if ccy == "GBP":
                return 0.04 + (0.02 if month >= 592 else 0.0)        # larger hike 8 months ago
            return LEVEL[ccy]
    assert ranking(Step(), 600, 3)[0] == "EUR"                       # only the EUR hike is within 3 months
    assert ranking(Step(), 600, 12)[:2] == ["GBP", "EUR"]            # both within 12 months, GBP larger
