from calendar import timegm

import numpy as np
import pytest

from smc.data.bars import resample
from smc.data.histdata import M1_DTYPE
from smc.pipeline import TFS, build_symbol
from smc.strategy_c import Inputs


def synthetic_m1(weeks=104, seed=1):
    """Random walk plus a slow (4-week) and a fast (~2-day) swing, so that H1 counter swings
    inside H4 trends occur often enough. Five 24-hour days per week."""
    rng = np.random.default_rng(seed)
    t0 = timegm((2021, 1, 3, 22, 0, 0))          # Sunday 17:00 New York
    t = np.concatenate([t0 + w * 7 * 86400 + 60 * np.arange(5 * 1440) for w in range(weeks)])
    x = np.arange(len(t))
    c = (1.10 + np.cumsum(rng.normal(0, 5e-5, len(t))) + 0.02 * np.sin(2 * np.pi * x / 28_800)
         + 0.006 * np.sin(2 * np.pi * x / 3_000))
    o = np.r_[c[0], c[:-1]]
    wick = np.abs(rng.normal(0, 2.5e-5, (2, len(t))))
    m1 = np.empty(len(t), M1_DTYPE)
    m1["t"], m1["o"], m1["c"] = t, o, c
    m1["h"], m1["l"] = np.maximum(o, c) + wick[0], np.minimum(o, c) - wick[1]
    return m1


def synthetic_features(m1):
    return Inputs.from_features(build_symbol("EURUSD", bars={tf: resample(m1, tf) for tf in TFS}))


@pytest.fixture(scope="session")
def synthetic_inputs():
    """Model inputs of the synthetic EURUSD market, built from all data and from data cut on a
    Saturday (so no bar is cut in half); used for the history-invariance tests of the models."""
    m1 = synthetic_m1()
    cut = timegm((2022, 2, 26, 12, 0, 0))
    return synthetic_features(m1), synthetic_features(m1[m1["t"] < cut]), cut
