"""Seeded, wholly fictional stock-scale fixture: 60,000 homes and 600,000 events.

No real people, addresses or map anchors are used: names come from a fixed fictional
list, addresses are numbered "Test Road" lines and coordinates are a made-up grid.
Output goes to mvp/data/ by default, which is ignored by Git; the fixture is rebuilt
from the seed rather than committed.

    PYTHONPATH=. python3 -m zavaforward_mvp.scale_fixture [--out DIR] [--seed N]
"""
import argparse
import hashlib
import json
import random
from pathlib import Path

from .insights import STAGE_ORDER

VERSION = "1.0.0"
HOMES = 60000
EVENTS = 600000
EVENTS_PER_HOME = EVENTS // HOMES
NAMES = ["Alex Example", "Bo Sample", "Cy Fiction", "Dee Imaginary", "Eli Placeholder", "Fay Notreal"]
AREAS = ["North", "South", "East", "West"]
KINDS = ["contact", "appointment", "stage_change", "hazard_check", "decision"]
SEED = 174


def homes(n=HOMES, seed=SEED):
    rnd = random.Random(seed)
    for i in range(n):
        yield dict(id=f"ZF-{i:05d}", area=rnd.choice(AREAS), stage=rnd.choice(STAGE_ORDER),
                   resident=rnd.choice(NAMES), priority_support=rnd.random() < 0.08,
                   address=f"{i} Test Road", postcode=f"TE{i % 9} 1ST",
                   lat=round(50 + (i % 250) * 0.001, 4), lon=round(-1 + (i // 250) * 0.001, 4),
                   open_safety_issue=rnd.random() < 0.02)


def events(n=HOMES, per_home=EVENTS_PER_HOME, seed=SEED):
    rnd = random.Random(f"{seed}-events")
    for i in range(n):
        for k in range(per_home):
            yield dict(case=f"ZF-{i:05d}", seq=k, kind=rnd.choice(KINDS),
                       day=f"2026-{rnd.randint(1, 12):02d}-{rnd.randint(1, 28):02d}")


def write(out, n=HOMES, per_home=EVENTS_PER_HOME, seed=SEED):
    out = Path(out)
    out.mkdir(parents=True, exist_ok=True)
    digest = hashlib.sha256()
    counts = {}
    for name, rows in (("homes.jsonl", homes(n, seed)), ("events.jsonl", events(n, per_home, seed))):
        count = 0
        with open(out / name, "w", encoding="utf-8") as f:
            for row in rows:
                line = json.dumps(row, sort_keys=True) + "\n"
                digest.update(line.encode())
                f.write(line)
                count += 1
        counts[name] = count
    manifest = dict(version=VERSION, seed=seed, homes=counts["homes.jsonl"], events=counts["events.jsonl"],
                    sha256=digest.hexdigest())
    (out / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    return manifest


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--out", default=str(Path(__file__).resolve().parents[1] / "data" / "scale-fixture"))
    ap.add_argument("--seed", type=int, default=SEED)
    a = ap.parse_args(argv)
    print(json.dumps(write(a.out, seed=a.seed), indent=2))


if __name__ == "__main__":
    main()
