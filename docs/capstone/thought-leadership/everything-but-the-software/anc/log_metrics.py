#!/usr/bin/env python3
"""Recompute the knowledge-base log measures reported in
"Everything but the Software" (Appendix A).

Usage:
    git clone https://github.com/jmservera/ama && cd ama
    git checkout 29c6b512f5e68733bb2cc1882343db39f5eb2cad
    python3 log_metrics.py docs/reference/log.md [--split 2026-10-15] [--json log_daily.json]

The optional --json file holds {date: [entries, words, hedges]} per day and is
the input of make_figures.py.
"""
import argparse
import json
import re
from collections import defaultdict

ENTRY_SPLIT = re.compile(r"\n(?=## \[?\d{4}-\d{2}-\d{2})")
ENTRY_DATE = re.compile(r"## \[?(\d{4}-\d{2}-\d{2})")
HEDGE = re.compile(
    r"\b(unmet|not accepted|not inferred|is inferred|remains? open|remains? unproved|"
    r"remains? unverified|not claimed|no [a-z ,/-]{0,40}(is|was) (claimed|inferred)|not established)\b",
    re.I,
)
SIMPLICITY = re.compile(r"SA-0(0[1-9]|10)|simplicity", re.I)
DEV_PROFILE = re.compile(r"deploymentProfile|development profile|allowPublicNetworkAccess")


def entries(text):
    for part in ENTRY_SPLIT.split(text):
        m = ENTRY_DATE.match(part)
        if m:
            yield m.group(1), part


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("log")
    ap.add_argument("--split", default="2026-10-15", help="first day of the loop period")
    ap.add_argument("--json", help="write per-day [entries, words, hedges] to this file")
    args = ap.parse_args()
    text = open(args.log, encoding="utf-8").read()
    daily = defaultdict(lambda: [0, 0, 0])  # entries, words, hedges
    simplicity, dev = [], []
    for day, body in entries(text):
        d = daily[day]
        d[0] += 1
        d[1] += len(body.split())
        d[2] += len(HEDGE.findall(body))
        if SIMPLICITY.search(body):
            simplicity.append(day)
        if DEV_PROFILE.search(body):
            dev.append(day)
    print("date        entries  words  hedges")
    for day in sorted(daily):
        e, w, h = daily[day]
        print(f"{day}  {e:7d} {w:6d} {h:7d}")
    for label, sel in (("before", lambda k: k < args.split), ("during", lambda k: k >= args.split)):
        e = sum(v[0] for k, v in daily.items() if sel(k))
        w = sum(v[1] for k, v in daily.items() if sel(k))
        h = sum(v[2] for k, v in daily.items() if sel(k))
        print(f"{label}: entries={e} words={w} hedges={h} per1000={1000 * h / w:.2f}" if w else f"{label}: no entries")
    print("entries citing simplicity requirements:", len(simplicity), simplicity)
    print("entries citing the development profile:", len(dev), dev)
    if args.json:
        with open(args.json, "w", encoding="utf-8") as f:
            json.dump({k: daily[k] for k in sorted(daily)}, f)


if __name__ == "__main__":
    main()
