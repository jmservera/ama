"""Deterministic home ranking (PR-006).

rank() is a pure function of the case data and a versioned policy. The same
input and the same policy version always give the same order, whatever order
the cases arrive in, because the last rule is always the case id. A change to
the rules is a new policy version file in policies/; every file is hash-checked
when loaded and old versions stay in POLICIES so their output can be reproduced. AI never reads or changes this module's output.
"""
import hashlib
import json
import os

POLICY_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "policies")


class PolicyError(Exception):
    """A policy file is unreadable, incomplete or does not match its recorded content hash."""


def policy_hash(policy):
    """SHA-256 of the canonical JSON of the policy without its own content_hash field."""
    body = {k: v for k, v in policy.items() if k != "content_hash"}
    return hashlib.sha256(json.dumps(body, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()


def load_policy(path):
    try:
        with open(path, encoding="utf-8") as f:
            p = json.load(f)
    except (OSError, ValueError) as e:
        raise PolicyError(f"Cannot read ranking policy {path}: {e}")
    missing = [k for k in ("policy_id", "version", "owner", "status", "effective_date", "rules", "stage_order", "content_hash") if k not in p]
    if missing:
        raise PolicyError(f"Ranking policy {path} is missing {', '.join(missing)}")
    if policy_hash(p) != p["content_hash"]:
        raise PolicyError(f"Ranking policy {path} does not match its content hash and was refused")
    return p


def load_registry(folder=POLICY_DIR):
    """Load and verify every policy file in the folder, keyed by version. Old versions stay so they can be re-run."""
    reg = {}
    for name in sorted(os.listdir(folder)):
        if name.endswith(".json"):
            p = load_policy(os.path.join(folder, name))
            if p["version"] in reg:
                raise PolicyError(f"Ranking policy version {p['version']} appears twice")
            reg[p["version"]] = p
    if not reg:
        raise PolicyError(f"No ranking policy files in {folder}")
    return reg


def latest(reg):
    return reg[max(reg, key=lambda v: tuple(int(x) for x in v.split(".")))]


POLICIES = load_registry()
CURRENT = latest(POLICIES)
POLICY_V1 = POLICIES["1.0.0"]


def _hazard(c):
    return any(not h["released"] for h in c["hazards"])


def _support(c):
    return bool(c["resident"]["priority_support"] or c["resident"]["adjustment"] != "None")


def _rule_keys(policy):
    order = {s: i for i, s in enumerate(policy["stage_order"])}
    late = len(order)
    table = {
        "safety_open": lambda c: 0 if _hazard(c) else 1,
        "support": lambda c: 0 if _support(c) else 1,
        "waiting_days": lambda c: -c["days_in_stage"],
        "stage_order": lambda c: order.get(c["stage"], late),
        "case_id": lambda c: c["id"],
    }
    codes = [r["code"] for r in policy["rules"]]
    unknown = [k for k in codes if k not in table]
    if unknown:
        raise ValueError(f"Unknown ranking rule: {', '.join(unknown)}")
    if "case_id" not in codes:
        codes.append("case_id")
    return [table[k] for k in codes]


def sql_key(c, policy=CURRENT):
    """Fixed-width text key whose plain string order equals rank() order, so a database can sort and page on it.

    Segments follow the policy's rule order. Days are offset so any realistic value stays positive and 8 digits wide.
    """
    order = {s: i for i, s in enumerate(policy["stage_order"])}
    seg = {
        "safety_open": lambda: "0" if _hazard(c) else "1",
        "support": lambda: "0" if _support(c) else "1",
        "waiting_days": lambda: f"{10 ** 7 - max(-10 ** 6, min(10 ** 7 - 1, c['days_in_stage'])):08d}",
        "stage_order": lambda: f"{order.get(c['stage'], len(order)):04d}",
        "case_id": lambda: c["id"],
    }
    codes = [r["code"] for r in policy["rules"]]
    if "case_id" not in codes:
        codes.append("case_id")
    return "".join(seg[k]() for k in codes)


def reasons(c):
    """Plain-English reasons, paired with a stable code each."""
    out = []
    if _hazard(c):
        out.append(("safety_open", "Safety issue open"))
    if _support(c):
        out.append(("support", "Needs extra support"))
    d = c["days_in_stage"]
    out.append(("waiting_days", f"Waiting {d} {'day' if d == 1 else 'days'} in this stage"))
    out.append(("stage_order", f"At '{c['stage']}'"))
    return out


def rank(cases, policy=CURRENT, as_of=None):
    """as_of is the date the cases' day counts are stated as of. It is passed in, never read from a clock here.

    Return entries ordered by the policy: id, rank (from 1), reasons, reason_codes, policy_version."""
    keys = _rule_keys(policy)
    ordered = sorted(cases, key=lambda c: tuple(k(c) for k in keys))
    out = []
    for n, c in enumerate(ordered, start=1):
        rs = reasons(c)
        out.append(dict(id=c["id"], rank=n, reasons=[t for _, t in rs], reason_codes=[k for k, _ in rs],
                        policy_version=policy["version"]))
    return out


def canonical(entries):
    """Byte-stable serialisation, used to compare and store snapshots."""
    return json.dumps(entries, sort_keys=True, separators=(",", ":"))


def snapshot(cases, policy, as_of):
    """Ranking snapshot: policy version and hash, as_of, and per case rank, reason codes and deciding rule.

    The deciding rule is the first rule in policy order that separates a case from the one ranked above it.
    Nothing here reads a clock, so the same inputs always give byte-identical output.
    """
    keys = _rule_keys(policy)
    codes = [r["code"] for r in policy["rules"]]
    if "case_id" not in codes:
        codes.append("case_id")
    ordered = sorted(cases, key=lambda c: tuple(k(c) for k in keys))
    rows, prev = [], None
    for n, c in enumerate(ordered, start=1):
        mine = [k(c) for k in keys]
        deciding = None if prev is None else next(code for code, a, b in zip(codes, prev, mine) if a != b)
        rows.append(dict(id=c["id"], rank=n, reason_codes=[k for k, _ in reasons(c)], deciding_rule=deciding))
        prev = mine
    snap = dict(policy_id=policy["policy_id"], policy_version=policy["version"], policy_hash=policy["content_hash"],
                as_of=as_of, total=len(rows), entries=rows)
    snap["snapshot_hash"] = hashlib.sha256(canonical(snap).encode("utf-8")).hexdigest()
    return snap


def describe(policy=CURRENT):
    return dict(policy_id=policy["policy_id"], version=policy["version"], owner=policy["owner"], status=policy["status"],
                effective_date=policy["effective_date"], content_hash=policy["content_hash"],
                rules=[dict(order=i, **r) for i, r in enumerate(policy["rules"], start=1)],
                versions=sorted(POLICIES))
