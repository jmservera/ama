"""Hash-chained audit ledger: entry hashing, chain verification and digests.

An entry holds its full content. Its hash covers every field except the hash
itself, including the previous entry's hash, so changing, removing or
reordering any entry breaks the chain from that point on. A digest records the
entry count and head hash at a moment in time. Stored somewhere the application
cannot rewrite (in Azure, an immutable Blob container), it also exposes a
truncation or a whole-chain rewrite that the chain alone cannot show.
"""
import hashlib
import json
import os
import sys
from datetime import datetime, timezone

GENESIS = "0" * 64
FIELDS = ("at", "who", "action", "case", "detail", "prev")


def entry_hash(entry):
    body = {k: v for k, v in entry.items() if k != "hash"}
    return hashlib.sha256(json.dumps(body, sort_keys=True).encode()).hexdigest()


def make_entry(who, action, case_id, detail, prev, at=None):
    e = dict(at=at or datetime.now().isoformat(timespec="seconds"), who=who, action=action,
             case=case_id, detail=detail, prev=prev)
    e["hash"] = entry_hash(e)
    return e


def verify_entries(entries, digests=(), start=GENESIS):
    """Walk the chain. Returns a report; never raises on a broken chain."""
    prev, n, hashes = start, 0, []
    problem = None
    for n, e in enumerate(entries, start=1):
        if e.get("prev") != prev:
            problem = dict(entry=n, reason="previous hash does not match the entry before it")
            break
        if entry_hash(e) != e.get("hash"):
            problem = dict(entry=n, reason="content does not match its hash")
            break
        prev = e["hash"]
        hashes.append(prev)
    else:
        n = len(hashes)
    checked, bad = 0, []
    for d in digests:
        checked += 1
        cnt = d.get("count", 0)
        if problem is None and (cnt > len(hashes) or (cnt and hashes[cnt - 1] != d.get("head"))):
            bad.append(dict(digest_count=cnt, reason="chain is shorter than the digest" if cnt > len(hashes)
                            else "chain differs from the digest"))
    return dict(intact=problem is None and not bad, entries=len(hashes) if problem is None else n - 1,
                head=prev, problem=problem, digests_checked=checked, digest_mismatches=bad)


def _year(e):
    return str(e.get("at", ""))[:4]


def make_year_digest(year, entries, chain="main"):
    """Seal one calendar year: its entries link to the year before through first_prev."""
    return dict(chain=chain, algorithm="sha256", year=year, count=len(entries), first_prev=entries[0]["prev"],
                head=entries[-1]["hash"])


def year_digests(entries, before=None):
    """One digest per year present in the chain, only for years earlier than `before` when given (sealed years)."""
    by = {}
    for e in entries:
        by.setdefault(_year(e), []).append(e)
    return [make_year_digest(y, es) for y, es in sorted(by.items()) if before is None or y < str(before)]


def verify_years(entries, digests=()):
    """Verify each year on its own, then the links between years, then each sealed year digest.

    A year verifies from its own first_prev, so one year can be audited without reading the others."""
    by = {}
    for e in entries:
        by.setdefault(_year(e), []).append(e)
    sealed = {d["year"]: d for d in digests}
    years, prev_head, ok = {}, GENESIS, True
    for y, es in sorted(by.items()):
        rep = verify_entries(es, start=es[0].get("prev"))
        problems = []
        if es[0].get("prev") != prev_head:
            problems.append("first entry does not link to the previous year")
        if not rep["intact"]:
            problems.append(rep["problem"]["reason"])
        d = sealed.get(y)
        if d and (d["count"], d["head"], d["first_prev"]) != (len(es), es[-1].get("hash"), es[0].get("prev")):
            problems.append("year differs from its sealed digest")
        years[y] = dict(entries=len(es), head=es[-1].get("hash"), sealed=d is not None, intact=not problems, problems=problems)
        ok &= not problems
        prev_head = es[-1].get("hash")
    missing = sorted(y for y in sealed if y not in by)
    return dict(intact=ok and not missing, years=years, missing_years=missing)


def make_digest(count, head, chain="main"):
    return dict(chain=chain, algorithm="sha256", count=count, head=head,
                at=datetime.now(timezone.utc).isoformat(timespec="seconds"))


def write_digest(directory, digest):
    os.makedirs(directory, exist_ok=True)
    path = os.path.join(directory, f"digest-{digest['count']:010d}.json")
    if os.path.exists(path):
        return path
    with open(path, "x", encoding="utf-8") as f:
        json.dump(digest, f, sort_keys=True)
    return path


def write_year_digest(directory, digest):
    os.makedirs(directory, exist_ok=True)
    path = os.path.join(directory, f"year-{digest['year']}.json")
    if not os.path.exists(path):
        with open(path, "x", encoding="utf-8") as f:
            json.dump(digest, f, sort_keys=True)
    return path


def read_year_digests(directory):
    out = []
    if directory and os.path.isdir(directory):
        for name in sorted(os.listdir(directory)):
            if name.startswith("year-") and name.endswith(".json"):
                with open(os.path.join(directory, name), encoding="utf-8") as f:
                    out.append(json.load(f))
    return out


def read_digests(directory):
    out = []
    if directory and os.path.isdir(directory):
        for name in sorted(os.listdir(directory)):
            if name.startswith("digest-") and name.endswith(".json"):
                with open(os.path.join(directory, name), encoding="utf-8") as f:
                    out.append(json.load(f))
    return out


def main(argv=None):
    """python -m zava_forward.core.ledger [--digest] [--seal-years] [--by-year] : verify the configured ledger, exit 1 if broken."""
    from .factory import open_store
    argv = sys.argv[1:] if argv is None else argv
    store = open_store()
    if "--digest" in argv:
        print("digest written:", store.write_digest())
    if "--seal-years" in argv:
        print("year digests written:", store.write_year_digests())
    rep = store.verify_ledger_by_year() if "--by-year" in argv else store.verify_ledger()
    print(json.dumps(rep, indent=2))
    return 0 if rep["intact"] else 1


if __name__ == "__main__":
    sys.exit(main())
