from datetime import date

from preh.model import events


def test_events_2023():
    ev = {h: (p, q) for h, p, q in events(date(2023, 1, 1), date(2023, 12, 31))}
    assert len(ev) == 10                                              # incl. Juneteenth since 2022
    assert ev[date(2023, 1, 2)] == (date(2022, 12, 30), date(2022, 12, 29))   # New Year observed Monday
    assert ev[date(2023, 7, 4)] == (date(2023, 7, 3), date(2023, 6, 30))      # p is a half day
    assert ev[date(2023, 11, 23)] == (date(2023, 11, 22), date(2023, 11, 21))
    assert ev[date(2023, 4, 7)] == (date(2023, 4, 6), date(2023, 4, 5))       # Good Friday


def test_special_closures_excluded():
    assert date(2018, 12, 5) not in {h for h, _, _ in events(date(2018, 1, 1), date(2018, 12, 31))}
