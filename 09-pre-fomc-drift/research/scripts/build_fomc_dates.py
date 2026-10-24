#!/usr/bin/env python3
"""Scheduled FOMC announcement days 2013-2026 from the Federal Reserve calendar pages.

Inputs (downloaded HTML, parsed as text only): data/raw/fomchistorical<year>.htm(l) for 2013-2020 and
data/raw/fomccalendars.html for 2021 onwards. Output: research/fomc_dates.csv with the second (announcement)
day of every scheduled meeting. Unscheduled meetings, cancelled meetings and notation votes are dropped.
"""
import csv
import re
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RAW = ROOT / "data" / "raw"
MONTHS = {m: i for i, m in enumerate(["January", "February", "March", "April", "May", "June", "July", "August",
                                      "September", "October", "November", "December"], 1)}
H5 = re.compile(r'<h5 class="panel-heading[^"]*">([^<]*)</h5>')
SPAN = re.compile(r"^([A-Za-z/]+)\s+(\d+)(?:-(\d+))?\s+Meeting - (\d{4})$")
ABBR = {m[:3]: v for m, v in MONTHS.items()}


def historical(year: int) -> list[tuple[date, str]]:
    text = (RAW / f"fomchistorical{year}.html").read_text(encoding="utf-8", errors="replace")
    out = []
    for head in H5.findall(text):
        head = head.strip()
        m = SPAN.match(head)
        if not m:
            if "Meeting" in head or "notation" in head:
                print(f"übersprungen: {head}", file=sys.stderr)
            continue
        months, d1, d2, y = m.groups()
        out.append((date(int(y), ABBR[months.split("/")[-1][:3]], int(d2 or d1)), head))
    return out


def current() -> list[tuple[date, str]]:
    text = (RAW / "fomccalendars.html").read_text(encoding="utf-8", errors="replace")
    out = []
    for block in re.split(r'<h4><a id="\d+">', text)[1:]:
        year = int(block[:4])
        rows = re.findall(r'fomc-meeting__month[^>]*><strong>([^<]*)</strong>.*?fomc-meeting__date[^>]*>([^<]*)<',
                          block, flags=re.S)
        for month_txt, day_txt in rows:
            raw = f"{year} {month_txt} {day_txt}"
            if "unscheduled" in raw.lower() or "cancel" in raw.lower() or "notation" in raw.lower():
                print(f"übersprungen: {raw}", file=sys.stderr)
                continue
            months = month_txt.split("/")
            days = re.findall(r"\d+", day_txt)
            month = ABBR[months[-1].strip()[:3]]
            out.append((date(year, month, int(days[-1])), raw.strip()))
    return out


def main():
    rows = [r for y in range(2013, 2021) for r in historical(y)] + [r for r in current() if r[0].year >= 2021]
    rows.sort()
    path = ROOT / "research" / "fomc_dates.csv"
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["announcement_day", "source_label"])
        for d, label in rows:
            w.writerow([d.isoformat(), label])
    by_year = {}
    for d, _ in rows:
        by_year[d.year] = by_year.get(d.year, 0) + 1
    print(f"{len(rows)} Termine -> {path}")
    print(by_year)


if __name__ == "__main__":
    main()
