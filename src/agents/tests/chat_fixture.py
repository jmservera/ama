"""Synthetic per-user chat and memory test fixtures (ADR 0004, backlog #172).

Wholly synthetic (ADR 0005): every row carries is_synthetic=true and turn text comes from a
fixed set of labelled templates, never from real conversations. Case IDs come from the
60,000-home stock (scale_fixture), personas map to the eleven PRD perspectives and to the
existing Entra app-role display names in ROLE_NAMES (kept equal to auth.DEFAULT_ROLE_MAP by a mvp test until M5). One seed gives identical bytes.

Expected outcomes are fixture expectations for the future chat store (#160 to #164); they are
not evidence that a runtime enforces them. The retention period is an illustrative parameter,
not an approved policy (BRD OD-45/OD-46 stay open).

    PYTHONPATH=src/agents/tests python3 -m chat_fixture [--out DIR] [--seed N]
"""
import argparse
import hashlib
import json
import random
from datetime import date, timedelta
from pathlib import Path

from zava_forward.core.synthetic import output_dir, scale_fixture
from zava_forward.core.assistants import REGISTRY as ASSISTANTS

VERSION = "chat-fixture-v1"
SEED = 172
AS_OF = date(2026, 10, 15)
RETENTION_DAYS = 90
SOURCE = "SYNTHETIC-DEMO"
USERS_PER_PERSPECTIVE = 2

# PRD "Users and Personas" perspectives with the app role each fixture persona is mapped to.
PERSPECTIVES = [
    ("asset-investment", "Asset and investment", "ZavaForward.ProgrammeManager"),
    ("programme-coordinator", "Programme coordinator", "ZavaForward.Coordinator"),
    ("retrofit-case-team", "Retrofit case team", "ZavaForward.SupportOfficer"),
    ("assessor-designer", "Retrofit Assessor, designer and Coordinator", "ZavaForward.Coordinator"),
    ("housing-resident-engagement", "Housing and Resident Engagement", "ZavaForward.LiaisonOfficer"),
    ("repairs-building-safety", "Repairs and Building Safety", "ZavaForward.SafetyLiaison"),
    ("procurement-contracts", "Procurement and contract manager", "ZavaForward.ProgrammeManager"),
    ("provider-contractor", "Provider / contractor contact", "ZavaForward.Contractor"),
    ("quality-assurance", "Quality and assurance", "ZavaForward.QualityInspector"),
    ("finance-grants", "Finance and Grants", "ZavaForward.GrantsOfficer"),
    ("digital-auditor", "Digital operator and auditor", "ZavaForward.SupportOfficer"),
]
NAMES = ["Alex Example", "Bo Sample", "Cy Fiction", "Dee Imaginary", "Eli Placeholder", "Fay Notreal",
         "Gus Pretend", "Hal Mockup", "Ivy Testcase", "Jo Constructed", "Kit Dummy"]
SURNAME_TAGS = ["Alpha", "Beta"]
THREAD_STATES = ["active", "active", "active", "expired", "deleted_by_owner"]
MEMORY_OPT_IN = ["not_opted_in", "opted_in", "opted_in", "withdrawn"]
MEMORY_CATEGORIES = ["working_preference", "terminology", "task_context"]
# Categories the PRD (FR-057) says must never be stored; these seed negative probes only.
EXCLUDED_CATEGORIES = ["health", "safeguarding", "vulnerability", "special_category", "consent"]
USER_TURNS = [
    "[SYNTHETIC] Which evidence is still missing for this home?",
    "[SYNTHETIC] Summarise the open handoff and name its owner.",
    "[SYNTHETIC] Draft a short query for the data owner about the conflicting value.",
]
ASSISTANT_TURNS = [
    "[SYNTHETIC SCRIPTED AI SUGGESTION] Proposed only; a named human must review. Unknown: source age.",
    "[SYNTHETIC SCRIPTED AI SUGGESTION] Proposed only; evidence gaps listed, no decision made.",
]
MEMORY_TEXT = {
    "working_preference": "[SYNTHETIC] Prefers short bullet summaries.",
    "terminology": "[SYNTHETIC] Uses the team's own abbreviation list.",
    "task_context": "[SYNTHETIC] Reviewing a constructed package this week.",
}
EXCLUDED_TEXT = "[SYNTHETIC PROBE] Seeded value that must be rejected, not stored."


ROLE_NAMES = {
    "ZavaForward.Coordinator": "Retrofit Coordinator",
    "ZavaForward.LiaisonOfficer": "Resident Liaison Officer",
    "ZavaForward.SafetyLiaison": "Building Safety Liaison",
    "ZavaForward.GrantsOfficer": "Grants and Evidence Officer",
    "ZavaForward.QualityInspector": "Quality Inspector",
    "ZavaForward.ProgrammeManager": "Retrofit Programme Manager",
    "ZavaForward.SupportOfficer": "Programme Support Officer",
    "ZavaForward.Contractor": "Contractor",
}


def role_name(app_role):
    return ROLE_NAMES[app_role]


def eligible_tasks(app_role):
    return sorted(k for k, v in ASSISTANTS.items() if role_name(app_role) in v["roles"])


def personas():
    rows = []
    for i, (pid, label, app_role) in enumerate(PERSPECTIVES):
        for j, tag in enumerate(SURNAME_TAGS[:USERS_PER_PERSPECTIVE]):
            rows.append(dict(user_key=f"U-SYN-{i:02d}{j}", persona_id=pid, perspective=label,
                             display_name=f"{NAMES[i]} {tag}", app_role=app_role, role=role_name(app_role),
                             eligible_tasks=eligible_tasks(app_role), is_synthetic=True))
    return rows


def _days(d):
    return d.isoformat()


def threads_and_turns(people, seed=SEED):
    rnd = random.Random(f"{seed}-threads")
    threads, turns, ledger = [], [], []
    for p in people:
        tasks = p["eligible_tasks"]
        if not tasks:
            continue
        for n in range(3):
            tid = f"THR-SYN-{p['user_key'][-3:]}-{n}"
            state = rnd.choice(THREAD_STATES)
            created = AS_OF - timedelta(days=rnd.randint(1, 120))
            if state == "active" and (AS_OF - created).days > RETENTION_DAYS:
                state = "expired"
            expires = created + timedelta(days=RETENTION_DAYS)
            purged = state in ("expired", "deleted_by_owner")
            threads.append(dict(
                thread_id=tid, user_key=p["user_key"], role=p["role"], case_id=f"ZF-{rnd.randrange(scale_fixture.HOMES):05d}",
                task=tasks[n % len(tasks)], created=_days(created), expires=_days(expires), state=state,
                content_present=not purged, is_synthetic=True))
            for k in range(rnd.randint(1, 3)):
                turns.append(dict(
                    turn_id=f"{tid}-T{k}", thread_id=tid, user_key=p["user_key"], seq=k,
                    user_text=None if purged else USER_TURNS[(n + k) % len(USER_TURNS)],
                    assistant_text=None if purged else ASSISTANT_TURNS[(n + k) % len(ASSISTANT_TURNS)],
                    is_synthetic=True))
            ledger.append(dict(event_id=f"LED-SYN-{tid}-C", thread_id=tid, user_key=p["user_key"],
                               event="thread_created", at=_days(created), content=None, is_synthetic=True))
            if purged:
                ledger.append(dict(event_id=f"LED-SYN-{tid}-D", thread_id=tid, user_key=p["user_key"],
                                   event="thread_deleted" if state == "deleted_by_owner" else "thread_expired",
                                   at=_days(min(AS_OF, expires) if state == "expired" else AS_OF), content=None,
                                   is_synthetic=True))
    return threads, turns, ledger


def memory(people, seed=SEED):
    rnd = random.Random(f"{seed}-memory")
    states, items = [], []
    for idx, p in enumerate(people):
        opt = MEMORY_OPT_IN[idx % len(MEMORY_OPT_IN)]
        states.append(dict(user_key=p["user_key"], role=p["role"], memory_state=opt,
                           global_switch_off=opt != "opted_in", per_task_off=sorted(p["eligible_tasks"][:1]) if opt == "opted_in" and idx % 3 == 0 else [],
                           is_synthetic=True))
        if opt == "not_opted_in":
            continue
        for n in range(3):
            created = AS_OF - timedelta(days=rnd.randint(1, 120))
            expires = created + timedelta(days=rnd.choice([30, 60, 90]))
            cat = MEMORY_CATEGORIES[n]
            state = "deleted" if opt == "withdrawn" else rnd.choice(["active", "active", "edited", "deleted"])
            if state in ("active", "edited") and expires < AS_OF:
                state = "expired"
            items.append(dict(
                item_id=f"MEM-SYN-{p['user_key'][-3:]}-{n}", user_key=p["user_key"], role=p["role"], category=cat,
                text=None if state in ("deleted", "expired") else MEMORY_TEXT[cat],
                source="user_stated", created=_days(created), expires=_days(expires), state=state, is_synthetic=True))
    return states, items


def exclusion_probes(people):
    """One seeded attempt per excluded category per sampled user; every one must be rejected."""
    rows = []
    for p in people[::USERS_PER_PERSPECTIVE]:
        for cat in EXCLUDED_CATEGORIES:
            rows.append(dict(probe_id=f"EXC-SYN-{p['user_key'][-3:]}-{cat}", user_key=p["user_key"], category=cat,
                             text=EXCLUDED_TEXT, expected="rejected_not_stored", is_synthetic=True))
    return rows


def isolation_cases(people, threads, items):
    """Cross-user, cross-role, revoked-role, spoofed-key and administrator probes (AC-094, AC-102)."""
    rows = []
    by_key = {p["user_key"]: p for p in people}
    owned = {}
    for t in threads:
        owned.setdefault(t["user_key"], []).append(t)
    mem_owned = {}
    for m in items:
        mem_owned.setdefault(m["user_key"], []).append(m)

    def add(kind, actor, target_user, resource, rid, action, expected, note=None):
        rows.append(dict(case_id=f"ISO-SYN-{len(rows):04d}", kind=kind, actor=actor, owner=target_user,
                         resource=resource, resource_id=rid, action=action, expected=expected, note=note, is_synthetic=True))

    for i, (pid, _, _) in enumerate(PERSPECTIVES):
        a, b = f"U-SYN-{i:02d}0", f"U-SYN-{i:02d}1"
        for owner, other in ((a, b), (b, a)):
            for t in owned.get(owner, [])[:1]:
                for action in ("read", "list", "search"):
                    add("same_role_cross_user", other, owner, "thread", t["thread_id"], action, "deny")
                add("owner_access", owner, owner, "thread", t["thread_id"], "export",
                    "deny" if t["state"] != "active" else "allow")
                add("owner_access", owner, owner, "thread", t["thread_id"], "delete",
                    "no_content_remaining" if t["state"] != "active" else "allow_content_removed_ledger_kept")
            for m in mem_owned.get(owner, [])[:1]:
                add("same_role_cross_user", other, owner, "memory", m["item_id"], "read", "deny")
        nxt = f"U-SYN-{(i + 1) % len(PERSPECTIVES):02d}0"
        if by_key[nxt]["role"] != by_key[a]["role"]:
            for t in owned.get(a, [])[:1]:
                add("cross_role", nxt, a, "thread", t["thread_id"], "read", "deny")
        for t in owned.get(a, [])[:1]:
            add("spoofed_user_key", b, a, "thread", t["thread_id"], "read", "deny",
                "client-supplied user key ignored; key derived from the authenticated principal")
            add("role_revoked_mid_thread", a, a, "thread", t["thread_id"], "next_turn", "deny_or_reproject",
                "app role removed or changed after the thread was created (AC-102)")
            add("administrator_access", "U-SYN-ADMIN", a, "thread", t["thread_id"], "read", "deny", "no reason or time limit")
            add("administrator_access", "U-SYN-ADMIN", a, "thread", t["thread_id"], "read",
                "allow_time_limited_audited", "reason recorded, access time-limited and audited")
    return rows


def deletion_and_expiry_cases(threads, items):
    rows = []
    for t in threads:
        if t["state"] in ("deleted_by_owner", "expired"):
            rows.append(dict(case_id=f"DEL-SYN-{len(rows):04d}", resource="thread", resource_id=t["thread_id"],
                             user_key=t["user_key"], trigger=t["state"], expected_content="absent",
                             expected_ledger="metadata_only", is_synthetic=True))
    for m in items:
        if m["state"] in ("deleted", "expired"):
            rows.append(dict(case_id=f"DEL-SYN-{len(rows):04d}", resource="memory", resource_id=m["item_id"],
                             user_key=m["user_key"], trigger=m["state"], expected_content="absent",
                             expected_ledger="metadata_only", is_synthetic=True))
    return rows


def build(seed=SEED):
    people = personas()
    threads, turns, ledger = threads_and_turns(people, seed)
    states, items = memory(people, seed)
    return dict(
        personas=people, threads=threads, turns=turns, ledger_events=ledger, memory_state=states,
        memory_items=items, exclusion_probes=exclusion_probes(people),
        isolation_cases=isolation_cases(people, threads, items),
        deletion_cases=deletion_and_expiry_cases(threads, items))


def write(out, seed=SEED):
    out = Path(out)
    out.mkdir(parents=True, exist_ok=True)
    digest = hashlib.sha256()
    counts = {}
    for name, rows in build(seed).items():
        counts[name] = len(rows)
        with open(out / f"{name}.jsonl", "w", encoding="utf-8") as f:
            for row in rows:
                line = json.dumps(row, sort_keys=True) + "\n"
                digest.update(line.encode())
                f.write(line)
    manifest = dict(version=VERSION, seed=seed, source_type=SOURCE, as_of=_days(AS_OF),
                    retention_days_illustrative=RETENTION_DAYS, counts=counts, sha256=digest.hexdigest(),
                    note="Synthetic only; expectations are fixture targets, not runtime evidence; retention not approved.")
    (out / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    return manifest


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--out", default=str(output_dir("chat-fixture")))
    ap.add_argument("--seed", type=int, default=SEED)
    a = ap.parse_args(argv)
    print(json.dumps(write(a.out, seed=a.seed), indent=2))


if __name__ == "__main__":
    main()
