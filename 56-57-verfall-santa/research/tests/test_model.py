from datetime import date

from cal.model import opex_day, windows


def test_opex_third_friday_and_good_friday():
    assert opex_day(2019, 10) == date(2019, 10, 18)
    assert opex_day(2022, 4) == date(2022, 4, 14)          # 15.04.2022 Good Friday -> Thursday


def test_windows_opex_and_post():
    w = dict(windows("K-OPEX", 2019, 2019))
    assert w[date(2019, 10, 11)] == date(2019, 10, 18)      # five trading days before
    p = [x for x in windows("K-POST", 2019, 2019) if x[0] == date(2019, 10, 18)]
    assert p == [(date(2019, 10, 18), date(2019, 10, 25))]
    assert len(windows("K-OPEX", 2015, 2023)) == 108


def test_windows_santa():
    s = windows("K-SANTA", 2019, 2019)
    assert s == [(date(2018, 12, 21), date(2019, 1, 3))]   # last five December days: 24, 26, 27, 28, 31
    assert len(windows("K-SANTA", 2015, 2023)) == 9
