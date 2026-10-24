"""M1 storage and aggregation into FTMO-server-time bars (M5 ... D1).

Bars are bucketed on the server clock (New York + 7 h), exactly like an MT5
chart on a NY-close server: D1 runs 17:00-17:00 NY, H4 opens at 17/21/01/05/09/13 NY.
No bar spans a DST switch because those happen on Sundays while FX is closed,
so a bar's UTC close time is simply its UTC open time plus the timeframe length.
"""
from __future__ import annotations

from pathlib import Path

import numpy as np
import pyarrow as pa
import pyarrow.parquet as pq

from smc import timez
from smc.config import BARS_DIR, M1_DIR, RAW_HISTDATA_DIR
from smc.data import histdata

TF_SECONDS = {"M1": 60, "M5": 300, "M15": 900, "H1": 3600, "H4": 14400, "D1": 86400}

# t = UTC open time, ts = server open time (both epoch seconds), n = number of M1 bars inside
BAR_DTYPE = np.dtype([("t", "i8"), ("ts", "i8"), ("o", "f8"), ("h", "f8"), ("l", "f8"), ("c", "f8"), ("n", "i4")])


def resample(m1: np.ndarray, tf: str) -> np.ndarray:
    sec = TF_SECONDS[tf]
    srv = timez.utc_to_server(m1["t"])
    bucket = srv // sec * sec
    starts = np.flatnonzero(np.r_[True, bucket[1:] != bucket[:-1]])
    ends = np.r_[starts[1:], len(m1)] - 1
    out = np.empty(len(starts), dtype=BAR_DTYPE)
    out["ts"] = bucket[starts]
    out["t"] = timez.server_to_utc(out["ts"])
    out["o"] = m1["o"][starts]
    out["h"] = np.maximum.reduceat(m1["h"], starts)
    out["l"] = np.minimum.reduceat(m1["l"], starts)
    out["c"] = m1["c"][ends]
    out["n"] = np.diff(np.r_[starts, len(m1)])
    return out


def consolidate_m1(symbol: str, raw_dir: Path = RAW_HISTDATA_DIR) -> tuple[np.ndarray, dict]:
    """Merge all HistData zips of a symbol: sort, de-duplicate, repair inconsistent OHLC."""
    parts = [histdata.read_zip(p) for p in sorted(raw_dir.glob(f"HISTDATA_COM_ASCII_{symbol}_M1_*.zip"))]
    if not parts:
        raise FileNotFoundError(f"no HistData files for {symbol} in {raw_dir}")
    m1 = np.concatenate(parts)
    m1 = m1[np.argsort(m1["t"], kind="stable")]
    keep = np.r_[m1["t"][1:] != m1["t"][:-1], True]  # keep the last row of duplicated timestamps
    dupes = int((~keep).sum())
    m1 = m1[keep]
    hi = np.maximum.reduce([m1["h"], m1["o"], m1["c"]])
    lo = np.minimum.reduce([m1["l"], m1["o"], m1["c"]])
    repaired = int(((hi != m1["h"]) | (lo != m1["l"])).sum())
    m1["h"], m1["l"] = hi, lo
    return m1, {"rows": len(m1), "duplicates": dupes, "repaired_ohlc": repaired}


def _write(arr: np.ndarray, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    pq.write_table(pa.table({name: arr[name] for name in arr.dtype.names}), path, compression="zstd")


def _read(path: Path, dtype: np.dtype) -> np.ndarray:
    table = pq.read_table(path)
    out = np.empty(table.num_rows, dtype=dtype)
    for name in dtype.names:
        out[name] = table.column(name).to_numpy()
    return out


def write_m1(symbol: str, m1: np.ndarray) -> Path:
    path = M1_DIR / f"{symbol}.parquet"
    _write(m1, path)
    return path


def load_m1(symbol: str) -> np.ndarray:
    return _read(M1_DIR / f"{symbol}.parquet", histdata.M1_DTYPE)


def write_bars(symbol: str, tf: str, bars: np.ndarray) -> Path:
    path = BARS_DIR / f"{symbol}_{tf}.parquet"
    _write(bars, path)
    return path


def load_bars(symbol: str, tf: str) -> np.ndarray:
    return _read(BARS_DIR / f"{symbol}_{tf}.parquet", BAR_DTYPE)
