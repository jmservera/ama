"""Hash-chained audit ledger: entry hashing, chain verification and digests.

An entry holds its full content. Its hash covers every field except the hash
itself, including the previous entry's hash, so changing, removing or
reordering any entry breaks the chain from that point on. A digest records the
entry count and head hash at a moment in time. Stored somewhere the application
cannot rewrite (in Azure, an immutable Blob container), it also exposes a
truncation or a whole-chain rewrite that the chain alone cannot show.
"""
import errno
import hashlib
import json
import os
import re
import sys
import tempfile
from datetime import datetime, timezone

GENESIS = "0" * 64
FIELDS = ("at", "who", "action", "case", "detail", "prev")
ASCII_YEAR_RE = re.compile(r"^(?!0000)[0-9]{4}$")
HEX64_RE = re.compile(r"^[0-9a-f]{64}$")
YEAR_DIGEST_FILE_RE = re.compile(r"^year-([0-9]{4})\.json$")
ROOT_DIGEST_FILE_RE = re.compile(r"^digest-([0-9]{10})\.json$")


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


DIGEST_KEYS = ("year", "count", "head", "first_prev")


def _year(e):
    return str(e.get("at", ""))[:4]


def make_year_digest(year, entries, chain="main"):
    """Seal one calendar year: its entries link to the year before through first_prev."""
    return dict(chain=chain, algorithm="sha256", year=year, count=len(entries), first_prev=entries[0]["prev"],
                head=entries[-1]["hash"])


def year_digests(entries, before=None):
    """One digest per year present in the chain, only for years earlier than `before` when given (sealed years)."""
    cutoff = None if before is None else (f"{before:04d}" if type(before) is int else str(before))
    by = {}
    for e in entries:
        by.setdefault(_year(e), []).append(e)
    return [make_year_digest(y, es) for y, es in sorted(by.items()) if cutoff is None or y < cutoff]


def verify_years(entries, digests=()):
    """Verify each year on its own, then the links between years, then each sealed year digest.

    A year verifies from its own first_prev, so one year can be audited without reading the others."""
    by = {}
    for e in entries:
        by.setdefault(_year(e), []).append(e)
    sealed, bad_digests = {}, []
    for d in digests:
        if isinstance(d, dict) and all(k in d for k in DIGEST_KEYS) and str(d["year"]) not in sealed:
            sealed[str(d["year"])] = d
        else:
            bad_digests.append(d.get("unreadable", d.get("year")) if isinstance(d, dict) else None)
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
    return dict(intact=ok and not missing and not bad_digests, years=years, missing_years=missing,
                sealed_years=sorted(sealed), bad_digests=bad_digests)


def make_digest(count, head, chain="main"):
    return dict(chain=chain, algorithm="sha256", count=count, head=head,
                at=datetime.now(timezone.utc).isoformat(timespec="seconds"))


def _write_json_once(path, payload):
    directory = os.path.dirname(path) or "."
    os.makedirs(directory, exist_ok=True)
    if os.path.exists(path):
        return path
    fd, tmp = tempfile.mkstemp(prefix=".digest-", suffix=".tmp", dir=directory)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(payload, f, sort_keys=True)
            f.flush()
        try:
            os.link(tmp, path)
        except FileExistsError:
            pass
        except OSError as exc:
            if exc.errno not in (errno.EXDEV, errno.EPERM, errno.ENOTSUP, errno.EACCES):
                raise
            try:
                with open(path, "x", encoding="utf-8") as out:
                    json.dump(payload, out, sort_keys=True)
            except FileExistsError:
                pass
    finally:
        try:
            os.unlink(tmp)
        except FileNotFoundError:
            pass
    return path


def write_digest(directory, digest):
    path = os.path.join(directory, f"digest-{digest['count']:010d}.json")
    return _write_json_once(path, digest)


def write_year_digest(directory, digest):
    path = os.path.join(directory, f"year-{digest['year']}.json")
    return _write_json_once(path, digest)


def inspect_digest_directory(directory):
    """Read and validate root `digest-*.json` and sealed `year-*.json` files without leaking paths."""
    if not directory or not isinstance(directory, str):
        return [], [], [dict(code="digest_store_unreadable", year=None, reason="digest directory is not configured")]
    if not os.path.lexists(directory):
        return [], [], []
    if (os.path.islink(directory) and not os.path.exists(directory)) or not os.path.isdir(directory):
        return [], [], [dict(code="digest_store_unreadable", year=None, reason="digest directory is not a readable directory")]
    try:
        names = sorted(os.listdir(directory))
    except OSError:
        return [], [], [dict(code="digest_store_unreadable", year=None, reason="digest directory could not be listed")]
    roots, years, problems, seen_years = [], [], [], set()
    for name in names:
        full = os.path.join(directory, name)
        if name.startswith("digest-") and name.endswith(".json"):
            m = ROOT_DIGEST_FILE_RE.fullmatch(name)
            try:
                with open(full, encoding="utf-8") as f:
                    d = json.load(f)
            except (OSError, ValueError):
                problems.append(dict(code="root_digest_unreadable", year=None, reason="independent root digest is unreadable"))
                continue
            cnt = d.get("count") if isinstance(d, dict) else None
            head = d.get("head") if isinstance(d, dict) else None
            valid_root = (
                m is not None
                and isinstance(d, dict)
                and type(cnt) is int
                and cnt >= 0
                and int(m.group(1)) == cnt
                and d.get("chain", "main") == "main"
                and d.get("algorithm", "sha256") == "sha256"
                and isinstance(head, str)
                and bool(HEX64_RE.fullmatch(head))
                and (cnt != 0 or head == GENESIS)
            )
            if valid_root:
                roots.append(d)
            else:
                problems.append(dict(code="root_digest_malformed", year=None, reason="independent root digest is malformed"))
        elif name.startswith("year-") and name.endswith(".json"):
            ym = YEAR_DIGEST_FILE_RE.fullmatch(name)
            file_year = ym.group(1) if ym and ASCII_YEAR_RE.fullmatch(ym.group(1)) else None
            try:
                with open(full, encoding="utf-8") as f:
                    d = json.load(f)
            except (OSError, ValueError):
                years.append(dict(unreadable=name))
                problems.append(dict(code="corrupt_year_digest", year=file_year, reason="sealed year digest is unreadable"))
                continue
            valid_year = (
                file_year is not None
                and isinstance(d, dict)
                and all(k in d for k in DIGEST_KEYS)
                and isinstance(d.get("year"), str)
                and d["year"] == file_year
                and bool(ASCII_YEAR_RE.fullmatch(d["year"]))
                and type(d.get("count")) is int
                and d["count"] >= 1
                and d.get("chain", "main") == "main"
                and d.get("algorithm", "sha256") == "sha256"
                and isinstance(d.get("first_prev"), str)
                and bool(HEX64_RE.fullmatch(d["first_prev"]))
                and isinstance(d.get("head"), str)
                and bool(HEX64_RE.fullmatch(d["head"]))
                and file_year not in seen_years
            )
            if valid_year:
                seen_years.add(file_year)
                years.append(d)
            else:
                years.append(dict(unreadable=name))
                problems.append(dict(code="corrupt_year_digest", year=file_year, reason="sealed year digest is malformed or mismatched"))
    return roots, years, problems


def read_year_digests(directory):
    out = []
    if directory and os.path.isdir(directory):
        for name in sorted(os.listdir(directory)):
            if name.startswith("year-") and name.endswith(".json"):
                try:
                    with open(os.path.join(directory, name), encoding="utf-8") as f:
                        digest = json.load(f)
                except (OSError, ValueError):
                    digest = None
                out.append(digest if isinstance(digest, dict) else dict(unreadable=name))
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
