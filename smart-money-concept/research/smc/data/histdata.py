"""HistData.com M1 bars: polite downloader and parser.

Files are Bid-based M1 bars with timestamps in EST *without* daylight saving
(fixed UTC-5), see https://www.histdata.com/f-a-q/. Completed years come as one
zip per symbol and year; the current year comes as one zip per month.
"""
from __future__ import annotations

import io
import re
import time
import urllib.parse
import urllib.request
import zipfile
from pathlib import Path

import numpy as np

BASE = "https://www.histdata.com"
USER_AGENT = "smcea-research/0.1 (personal non-commercial backtesting)"
EST_TO_UTC_SECONDS = 5 * 3600
_TOKEN_RE = re.compile(r'name="tk" id="tk" value="([0-9a-f]+)"')


def file_name(symbol: str, period: str) -> str:
    return f"HISTDATA_COM_ASCII_{symbol}_M1_{period}.zip"


def _page_url(symbol: str, year: int, month: int | None) -> str:
    tail = f"{symbol.lower()}/{year}" + (f"/{month}" if month else "")
    return f"{BASE}/download-free-forex-historical-data/?/ascii/1-minute-bar-quotes/{tail}"


def _request(url: str, data: bytes | None = None, referer: str | None = None, timeout: int = 120) -> bytes:
    headers = {"User-Agent": USER_AGENT}
    if referer:
        headers.update({"Referer": referer, "Origin": BASE})
    req = urllib.request.Request(url, data=data, headers=headers, method="POST" if data else "GET")
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read()


def download(symbol: str, year: int, month: int | None, out_dir: Path) -> Path | None:
    """Download one zip; returns its path, or None if HistData has no file for that period."""
    period = f"{year}{month:02d}" if month else str(year)
    target = out_dir / file_name(symbol, period)
    if target.exists() and zipfile.is_zipfile(target):
        return target
    page_url = _page_url(symbol, year, month)
    page = _request(page_url).decode("utf-8", "replace")
    if file_name(symbol, period) not in page:
        return None
    token = _TOKEN_RE.search(page)
    if not token:
        raise RuntimeError(f"no download token on {page_url}")
    form = urllib.parse.urlencode({
        "tk": token.group(1), "date": str(year), "datemonth": period,
        "platform": "ASCII", "timeframe": "M1", "fxpair": symbol,
    }).encode()
    payload = _request(f"{BASE}/get.php", data=form, referer=page_url)
    tmp = target.with_suffix(".part")
    tmp.write_bytes(payload)
    if not zipfile.is_zipfile(tmp) or not any(n.endswith(".csv") for n in zipfile.ZipFile(tmp).namelist()):
        tmp.unlink()
        raise RuntimeError(f"invalid zip for {symbol} {period} ({len(payload)} bytes)")
    tmp.rename(target)
    return target


def download_all(symbols, years, current_year: int, current_months, out_dir: Path,
                 delay_s: float = 3.0, retries: int = 3, log=print) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    jobs = [(s, y, None) for s in symbols for y in years] + \
           [(s, current_year, m) for s in symbols for m in current_months]
    for i, (s, y, m) in enumerate(jobs, 1):
        period = f"{y}{m:02d}" if m else str(y)
        if (out_dir / file_name(s, period)).exists():
            continue
        for attempt in range(1, retries + 1):
            try:
                path = download(s, y, m, out_dir)
                log(f"[{i}/{len(jobs)}] {s} {period}: " + (f"{path.stat().st_size / 1e6:.1f} MB" if path else "not available"))
                break
            except Exception as exc:  # network hiccups: back off and retry
                log(f"[{i}/{len(jobs)}] {s} {period}: attempt {attempt} failed: {exc}")
                time.sleep(delay_s * 5 * attempt)
        time.sleep(delay_s)


def read_zip(path: Path) -> np.ndarray:
    """Parse one HistData ASCII M1 zip into a structured array with UTC epoch seconds."""
    with zipfile.ZipFile(path) as zf:
        name = next(n for n in zf.namelist() if n.endswith(".csv"))
        raw = zf.read(name)
    return parse_csv(raw)


M1_DTYPE = np.dtype([("t", "i8"), ("o", "f8"), ("h", "f8"), ("l", "f8"), ("c", "f8")])


def parse_csv(raw: bytes) -> np.ndarray:
    """Rows look like `20160103 170000;1.087010;1.087130;1.087010;1.087130;0` (EST, no DST)."""
    lines = raw.decode("ascii").split()
    # split() breaks "YYYYMMDD HHMMSS;..." into date and "HHMMSS;o;h;l;c;v" tokens
    dates, rest = lines[0::2], lines[1::2]
    n = len(rest)
    out = np.empty(n, dtype=M1_DTYPE)
    ts = np.empty(n, dtype="datetime64[s]")
    o = np.empty(n); h = np.empty(n); l = np.empty(n); c = np.empty(n)
    for i, (d, r) in enumerate(zip(dates, rest)):
        f = r.split(";")
        hm = f[0]
        ts[i] = np.datetime64(f"{d[:4]}-{d[4:6]}-{d[6:8]}T{hm[:2]}:{hm[2:4]}:{hm[4:6]}")
        o[i] = float(f[1]); h[i] = float(f[2]); l[i] = float(f[3]); c[i] = float(f[4])
    out["t"] = ts.astype("i8") + EST_TO_UTC_SECONDS
    out["o"], out["h"], out["l"], out["c"] = o, h, l, c
    return out
