from datetime import date

from nws.model import nfp_date, nfp_dates


def test_known_release_dates():
    assert nfp_date(2023, 9) == date(2023, 10, 6)
    assert nfp_date(2023, 12) == date(2024, 1, 5)
    assert nfp_date(2015, 12) == date(2016, 1, 8)          # 01.01.2016 holiday -> one week later
    assert nfp_date(2020, 12) == date(2021, 1, 8)
    assert nfp_date(2015, 6) == date(2015, 7, 2)           # 03.07.2015 observed holiday -> Thursday
    assert nfp_date(2020, 6) == date(2020, 7, 2)
    assert nfp_date(2019, 2) == date(2019, 3, 8)


def test_count_per_year():
    assert len(nfp_dates(date(2015, 1, 1), date(2023, 12, 31))) == 108
