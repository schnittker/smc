from datetime import date, datetime
from zoneinfo import ZoneInfo

import pytest

from mer import events

LONDON = ZoneInfo("Europe/London")


@pytest.mark.parametrize("year, expected", [(2018, date(2018, 4, 1)), (2024, date(2024, 3, 31)),
                                            (2025, date(2025, 4, 20)), (2016, date(2016, 3, 27))])
def test_easter(year, expected):
    assert events.easter(year) == expected


@pytest.mark.parametrize("ym, expected", [
    ((2021, 5), date(2021, 5, 28)),    # 31.05.2021 Spring Bank Holiday
    ((2015, 8), date(2015, 8, 28)),    # 31.08.2015 Summer Bank Holiday
    ((2020, 8), date(2020, 8, 28)),
    ((2018, 3), date(2018, 3, 29)),    # 30.03.2018 Good Friday, 31.03. Saturday
    ((2024, 3), date(2024, 3, 28)),    # 29.03.2024 Good Friday
    ((2023, 12), date(2023, 12, 29)),  # 31.12.2023 Sunday
    ((2019, 6), date(2019, 6, 28)),
    ((2022, 5), date(2022, 5, 31)),
    ((2025, 10), date(2025, 10, 31)),
])
def test_last_business_day(ym, expected):
    assert events.last_business_day(*ym) == expected


def test_next_business_day_skips_weekend_and_holidays():
    assert events.next_business_day(date(2023, 12, 29)) == date(2024, 1, 2)
    assert events.next_business_day(date(2024, 3, 28)) == date(2024, 4, 2)


def test_event_days_are_consecutive_months():
    d = events.event_days((2015, 11), (2016, 2))
    assert [events.to_date(x) for x in d] == [date(2015, 11, 30), date(2015, 12, 31), date(2016, 1, 29),
                                             date(2016, 2, 29)]


@pytest.mark.parametrize("dt", [(2023, 6, 30), (2023, 1, 31), (2024, 3, 28), (2025, 10, 31)])
@pytest.mark.parametrize("hhmm", [(14, 55), (16, 0), (8, 0)])
def test_london_utc_matches_zoneinfo(dt, hhmm):
    day = events.day_number(date(*dt))
    assert int(events.london_utc(day, *hhmm)) == int(datetime(*dt, *hhmm, tzinfo=LONDON).timestamp())
