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

VERSION = "1.1.0"
HOMES = 60000
EVENTS = 600000
EVENTS_PER_HOME = EVENTS // HOMES
NAMES = ["Alex Example", "Bo Sample", "Cy Fiction", "Dee Imaginary", "Eli Placeholder", "Fay Notreal"]
AREAS = ["North", "South", "East", "West"]
KINDS = ["contact", "appointment", "stage_change", "hazard_check", "decision"]
SEED = 174
CHANNELS = ["Phone", "Text message", "Letter", "Email"]
ADJUSTMENTS = ["None", "Large print", "Interpreter", "BSL", "Advocate or representative", "Communication support"]
TENANCY_TYPES = ["Assured", "Secure", "Starter", "Shared ownership", "Leasehold"]
CONSENT_STATES = ["Not requested", "Pending", "Given", "Declined", "Withdrawn"]
REP_STATES = ["None recorded", "Claimed - unverified", "Authorised - evidence on file"]


def homes(n=HOMES, seed=SEED):
    rnd = random.Random(seed)
    for i in range(n):
        yield dict(id=f"ZF-{i:05d}", area=rnd.choice(AREAS), stage=rnd.choice(STAGE_ORDER),
                   resident=rnd.choice(NAMES), priority_support=rnd.random() < 0.08,
                   address=f"{i} Test Road", postcode=f"TE{i % 9} 1ST",
                   lat=round(50 + (i % 250) * 0.001, 4), lon=round(-1 + (i // 250) * 0.001, 4),
                   open_safety_issue=rnd.random() < 0.02)


def households(n=HOMES, seed=SEED):
    """One synthetic household per home. Consent and representative states are drawn,
    never derived from each other except where a consent given by a representative
    requires an authorised representative to be on file."""
    rnd = random.Random(f"{seed}-households")
    for h in homes(n, seed):
        i = int(h["id"][3:])
        adj = rnd.choices(ADJUSTMENTS, [85, 4, 3, 0.5, 3.5, 4])[0]
        rep = "Authorised - evidence on file" if adj == "Advocate or representative" else \
            rnd.choices(REP_STATES, [95, 2, 3])[0]
        consent = rnd.choices(CONSENT_STATES, [40, 20, 30, 5, 5])[0]
        by = None
        if consent in ("Given", "Declined", "Withdrawn"):
            by = "Representative" if rep == "Authorised - evidence on file" and rnd.random() < 0.5 else "Resident"
        yield dict(household_ref=f"HH-SYN-{i:05d}", home_id=h["id"], resident_ref=f"R-SYN-{i:05d}",
                   tenancy_ref=f"TEN-SYN-{i:05d}", tenancy_type=rnd.choices(TENANCY_TYPES, [50, 30, 5, 5, 10])[0],
                   tenancy_start=f"{rnd.randint(1995, 2025)}-{rnd.randint(1, 12):02d}-01",
                   household_size=rnd.choices([1, 2, 3, 4, 5], [35, 30, 17, 12, 6])[0],
                   lead_resident=h["resident"], preferred_channel=rnd.choices(CHANNELS, [50, 25, 15, 10])[0],
                   adjustment=adj, adjustment_recorded=adj != "None" and rnd.random() < 0.7,
                   priority_support=h["priority_support"], representative_state=rep,
                   representative_ref=f"REP-SYN-{i:05d}" if rep != REP_STATES[0] else None,
                   works_consent_state=consent, works_consent_given_by=by, is_synthetic=True)


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
    for name, rows in (("homes.jsonl", homes(n, seed)), ("households.jsonl", households(n, seed)), ("events.jsonl", events(n, per_home, seed))):
        count = 0
        with open(out / name, "w", encoding="utf-8") as f:
            for row in rows:
                line = json.dumps(row, sort_keys=True) + "\n"
                digest.update(line.encode())
                f.write(line)
                count += 1
        counts[name] = count
    manifest = dict(version=VERSION, seed=seed, homes=counts["homes.jsonl"], households=counts["households.jsonl"], events=counts["events.jsonl"],
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
