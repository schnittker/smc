import io
import zipfile
from datetime import date

import numpy as np
import pytest

from smc.swaps import RateTable
from cot.model import EPOCH, cot_index, load_cot, run_model_c, signals, targets


def dn(y, m, d):
    return (date(y, m, d) - EPOCH).days


def test_cot_index_range_and_window():
    net = np.r_[np.arange(156, dtype=float), [1000.0, -1000.0]]
    idx = cot_index(net)
    assert np.isnan(idx[154]) and idx[155] == 1.0 and idx[156] == 1.0 and idx[157] == 0.0
    assert cot_index(np.ones(200))[-1] == 0.5


def test_signals_exec_monday_and_shutdown_skip():
    days = np.array([dn(2012, 1, 3) + 7 * k for k in range(200)])            # ends before the 2018 shutdown
    net = np.r_[np.zeros(155), np.linspace(1, 10, 45)]        # rising to new highs -> extreme long
    sig = signals(days, net)
    assert sig[0][0] == days[155] + 6 and date.fromordinal(EPOCH.toordinal() + sig[0][0]).weekday() == 0
    assert all(s == 1 for _, s in sig[1:])
    days2 = np.array([dn(2016, 1, 5) + 7 * k for k in range(170)])
    days2[-5:] = [dn(2019, 1, 8), dn(2019, 1, 15), dn(2019, 2, 26), dn(2019, 3, 5), dn(2019, 3, 12)]
    got = {d - 6 for d, _ in signals(days2, np.arange(170, dtype=float))}
    assert dn(2019, 1, 8) not in got and dn(2019, 2, 26) not in got and dn(2019, 3, 5) in got


def _px(n=400, start=dn(2016, 1, 4)):
    days = np.array([d for d in range(start, start + 2 * n) if (d + 3) % 7 < 5][:n])
    p = 1.1 * np.exp(np.cumsum(np.random.default_rng(1).normal(0, 0.005, n)))
    return {"day": days, "p_sig": p, "p_mark": p, "exact": np.ones(n, bool), "lo": p * 0.999, "hi": p * 1.001}


def test_targets_direction_and_only_on_change():
    px = _px()
    sig = [(int(px["day"][100]), 1), (int(px["day"][105]), 1), (int(px["day"][110]), 0), (int(px["day"][120]), -1)]
    t_k = targets(px, sig, -1, -1)        # C-KONTRA on USDJPY: specs extremely long JPY -> short JPY = long USDJPY
    days = sorted(t_k)
    assert len(days) == 3 and t_k[days[0]] > 0 and t_k[days[1]] == 0.0 and t_k[days[2]] < 0
    t_f = targets(px, sig, 1, 1)          # C-FOLGE on EURUSD: with the specs
    assert t_f[sorted(t_f)[0]] > 0


def test_load_cot_from_zip(tmp_path):
    hdr = ["Market and Exchange Names", "As of Date in Form YYMMDD", "As of Date in Form YYYY-MM-DD",
           "CFTC Contract Market Code", "Noncommercial Positions-Long (All)", "Noncommercial Positions-Short (All)"]
    rows = [hdr, ["EURO FX", "160105", "2016-01-05", "099741", "100", "40"],
            ["EURO FX", "160112", "2016-01-12", "099741", "90", "60"], ["WHEAT", "160105", "2016-01-05", "001602", "1", "2"]]
    buf = io.StringIO()
    for r in rows:
        buf.write(",".join(f'"{x}"' for x in r) + "\n")
    p = tmp_path / "deacot2016.zip"
    with zipfile.ZipFile(p, "w") as z:
        z.writestr("annual.txt", buf.getvalue())
    cot = load_cot([p])
    days, net = cot["099741"]
    assert list(net) == [60.0, 30.0] and days[0] == dn(2016, 1, 5)


def test_run_model_c_gold_has_no_rate_swap_beyond_markup():
    px = _px()
    days = np.array([int(px["day"][0]) - 7 * k for k in range(200)][::-1])
    cot = {"088691": (days[-170:], np.r_[np.zeros(156), np.linspace(1, 9, 14)])}
    rows = run_model_c("C-FOLGE", "088691", px, cot, RateTable.constant({"USD": 0.05}))
    held = rows["w"] != 0
    if held.any():
        assert (rows["swap"][held] < 0).all()
