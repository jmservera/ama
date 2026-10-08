"""Deterministic home ranking (PR-006).

rank() is a pure function of the case data and a versioned policy. The same
input and the same policy version always give the same order, whatever order
the cases arrive in, because the last rule is always the case id. A change to
the rules is a new policy version; old versions stay in POLICIES so their
output can be reproduced. AI never reads or changes this module's output.
"""
import json

STAGE_ORDER = ["Home identified", "Checking lease", "Rescheduled", "Contacting resident", "Contact paused",
               "Survey being booked", "Survey booked", "Survey write-up", "Design starting", "Design in progress",
               "Design awaiting approval", "Design being corrected", "Waiting on other works",
               "Waiting for resident decision", "Resident paused works", "Funding check",
               "Final checks before ordering", "Waiting for block programme", "With contractor", "Install booked",
               "Works under way", "Handover to arrange", "Quality check", "Closing down", "Aftercare issue"]

POLICY_V1 = dict(
    policy_id="proper-warm-home-ranking",
    version="1.0.0",
    owner="to be named",
    status="Draft rule order, not yet signed off by an owner",
    rules=[
        dict(code="safety_open", label="Open safety issue first"),
        dict(code="support", label="Residents needing priority support or an adjustment next"),
        dict(code="waiting_days", label="Longest time in the current stage next"),
        dict(code="stage_order", label="Earlier programme stage next"),
        dict(code="case_id", label="Case id as the final fixed tie-break"),
    ],
    stage_order=STAGE_ORDER,
)

POLICIES = {POLICY_V1["version"]: POLICY_V1}
CURRENT = POLICY_V1


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


def rank(cases, policy=CURRENT):
    """Return entries ordered by the policy: id, rank (from 1), reasons, reason_codes, policy_version."""
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


def describe(policy=CURRENT):
    return dict(policy_id=policy["policy_id"], version=policy["version"], owner=policy["owner"], status=policy["status"],
                rules=[dict(order=i, **r) for i, r in enumerate(policy["rules"], start=1)],
                versions=sorted(POLICIES))
