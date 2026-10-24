import numpy as np
import pytest

from smc.data.bars import BAR_DTYPE
from smc.timez import server_to_utc
from pa.model import signals

DAY0 = 19002


def _bars(ohlc, step=14400):
    ts0 = DAY0 * 86400
    rows = [(int(server_to_utc(ts0 + step * j)), ts0 + step * j, o, h, l, c, 1) for j, (o, h, l, c) in enumerate(ohlc)]
    return np.array(rows, dtype=BAR_DTYPE)


def _flat(n, x=1.10, w=0.0005):
    return [[x, x + w, x - w, x] for _ in range(n)]


def test_pin_bar_at_support_zone():
    b = _flat(200)
    for j in (100, 140):
        b[j][2] = 1.0950                                                   # two swing lows -> support zone 1.0950
    b[190] = [1.0995, 1.1000, 1.0952, 1.0998]                               # long lower wick into the zone
    sig, stop, a, tgt = signals("PA-PIN", _bars(b))
    assert sig[190] == 1 and stop[190] == pytest.approx(1.0952 - 0.25 * a[190])


def test_engulfing_at_resistance():
    b = _flat(200)
    for j in (100, 140):
        b[j][1] = 1.1050                                                   # resistance zone 1.1050
    b[189] = [1.1010, 1.1030, 1.1005, 1.1028]                               # bullish
    b[190] = [1.1032, 1.1049, 1.0995, 1.1000]                               # bearish engulfing touching the zone
    sig, stop, a, tgt = signals("PA-ENG", _bars(b))
    assert sig[190] == -1 and stop[190] == pytest.approx(1.1049 + 0.25 * a[190])


def test_double_bottom_breaks_neckline():
    b = _flat(200)
    b[150][2], b[165][2] = 1.0900, 1.0902                                    # two equal lows 15 bars apart
    for j in range(151, 165):
        b[j] = [1.10, 1.1005, 1.0995, 1.10]
    b[158][1] = 1.1060                                                      # neckline
    for j in range(166, 185):
        b[j] = [1.105, 1.1055, 1.1045, 1.105]
    b[185] = [1.105, 1.1070, 1.1050, 1.1065]                                # close above the neckline
    sig, stop, a, tgt = signals("PA-DT", _bars(b))
    assert sig[185] == 1 and tgt[185] == pytest.approx(1.1060 + (1.1060 - 1.0900))


def test_demand_zone_first_retest():
    b = _flat(80, w=0.0010)
    b[40] = [1.1000, 1.1004, 1.0996, 1.1002]                                # base (small range)
    b[41] = [1.1002, 1.1110, 1.1000, 1.1100]                                # impulse body 0.0098
    for j in range(42, 60):
        b[j] = [1.1100, 1.1110, 1.1090, 1.1100]
    b[60] = [1.1050, 1.1055, 1.1001, 1.1010]                                # first retest into the zone, holds
    sig, stop, a, tgt = signals("PA-SD", _bars(b))
    assert sig[60] == 1 and stop[60] == pytest.approx(1.0996 - 0.25 * a[60])
    assert not sig[61:].any()
