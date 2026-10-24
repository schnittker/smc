import numpy as np

from brk.model import channels, targets


def _px(c):
    c = np.asarray(c, float)
    days = np.arange(len(c))
    return {"day": days, "p_sig": c, "p_mark": c * (1 + 0.003 * np.sin(days)), "exact": np.ones(len(c), bool)}


def test_channels_exclude_today():
    hi, lo = channels(np.array([1.0, 3.0, 2.0, 5.0]), 2)
    assert np.isnan(hi[1]) and hi[2] == 3.0 and lo[2] == 1.0 and hi[3] == 3.0


def test_long_breakout_then_exit_on_short_channel():
    c = [100.0] * 80 + [103, 104, 105] + [104, 103, 100, 98]
    t = targets(_px(c), 55, 20)
    days = sorted(t)
    assert t[days[0]] > 0 and days[0] == 80
    # day 85 (100) does not break the 20-day low (100); day 86 (98) exits and, below the 55-day low, reverses short
    assert days[1] == 86 and t[days[1]] < 0


def test_short_breakout_and_reverse():
    c = [100.0] * 80 + [97, 96] + [110]
    t = targets(_px(c), 55, 20)
    days = sorted(t)
    assert t[days[0]] < 0 and t[days[-1]] > 0                   # exit short and go long the same day
