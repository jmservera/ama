"""Offline human-review effectiveness test (AC-070). No network, no model, no human participants.

Seeded wrong, stale, unsupported and incomplete proposals, plus correct controls, go through
the real ``Store.ai_run`` and ``Store.review_ai``. Every proposal cites a label that resolves
in the case, so citation validity alone cannot find a defect. A controlled gate is satisfied
for a proposal only when a reviewer has answered it and:

* a defect was edited or rejected with a reason that names a source label resolving in the case;
* a control was accepted or edited, never rejected without cause.

Scripted reviewer panels stand in for people: a competent panel that compares each claim with
the source, a default-accept panel and an automation-bias panel that trusts confident, cited
output. The test passes only if the competent panel passes the gate and both others fail it.
The panels prove the gate and the measurement, not human competence; OQ-017 reviewer authority
and authorised participants remain open, and the report says so.

Run: python3 -m zava_forward.agents.review_effectiveness [--json]
"""

import json
import os
import sys
import tempfile
from collections.abc import Callable
from pathlib import Path
from typing import Any

from zava_forward.core import ai_tasks
from zava_forward.core.store import Store

from zava_forward.agents.ai_eval import OTHER, OWNER, build_case

GOLDEN = Path(
    os.environ.get("ZF_REVIEW_GOLDEN")
    or Path(__file__).resolve().parents[3] / "evals" / "review_effectiveness_golden.json"
)
SOURCE_TAG = "[source: "

Proposal = dict[str, Any]
Decision = tuple[str, str, str | None, int]  # action, reason, replacement text, effort units
Panel = Callable[[Proposal, dict[str, str], dict[str, Any], list[str]], Decision]

OPEN_ITEMS = (
    "no authorised competent human reviewers have run this test; scripted panels are not people",
    "reviewer authority and meaningful-oversight evidence remain OQ-017 owner decisions",
    "effort is scripted comparison units, not measured reviewer time",
    "thresholds and sample sizes are not approved; the seeded set is a demonstration slice",
)


def _facts(labels: list[str]) -> dict[str, str]:
    facts: dict[str, str] = {}
    for k, _, v in (x.partition(": ") for x in labels):
        # a repeated label keeps its first value; later values stay addressable as "<topic> detail"
        facts.setdefault(k if k not in facts else f"{k} detail", v)
    return facts


def _origin(topic: str) -> str:
    """The citable case label behind a topic alias such as 'Extra support detail'."""
    while topic.endswith(" detail") and topic != "detail":
        topic = topic[: -len(" detail")]
    return topic


def _findings(
    prop: Proposal, facts: dict[str, str], required: list[str]
) -> list[tuple[str, str, str]]:
    """Source comparison: (class, topic, source label) for each defect a careful reviewer finds."""
    found = []
    covered = {c["topic"] for c in prop["claims"]}
    for c in prop["claims"]:
        topic = c["topic"]
        if topic not in facts:
            found.append(("unsupported", topic, c["cite"]))
        elif facts[topic] != c["asserted"]:
            found.append(("mismatch", topic, f"{_origin(topic)}: {facts[topic]}"))
    found += [
        ("incomplete", t, f"{_origin(t)}: {facts[t]}")
        for t in required
        if t not in covered and t in facts
    ]
    return found


def _corrected(prop: Proposal, facts: dict[str, str], required: list[str]) -> str:
    """Full replacement: every supported claim at its source value plus each required topic."""
    topics = [c["topic"] for c in prop["claims"] if c["topic"] in facts]
    topics += [t for t in required if t in facts and t not in topics]
    return "; ".join(f"{t} is {facts[t]}" for t in topics)


def replacement_effective(
    prop: Proposal, rec: dict[str, Any], facts: dict[str, str], required: list[str]
) -> bool:
    """An edit corrects a defect only if the final text states source facts and drops the error."""
    text = rec.get("override_text") or ""
    statements = {x.strip() for x in text.split(";") if x.strip()}
    topics = {c["topic"] for c in prop["claims"] if c["topic"] in facts} | {
        t for t in required if t in facts
    }
    expected = {f"{t} is {facts[t]}" for t in topics}
    return bool(statements) and statements == expected


def competent(
    prop: Proposal, facts: dict[str, str], rec: dict[str, Any], required: list[str]
) -> Decision:
    effort = len(prop["claims"]) + 1
    found = _findings(prop, facts, required)
    if not found:
        return "accept", "", None, effort
    kind, topic, source = found[0]
    reason = f"{kind}: {topic} differs from the case {SOURCE_TAG}{source}]"
    if kind == "unsupported":
        return "reject", reason, None, effort + 1
    return "edit", reason, _corrected(prop, facts, required), effort + 1


def default_accept(
    prop: Proposal, facts: dict[str, str], rec: dict[str, Any], required: list[str]
) -> Decision:
    return "accept", "", None, 1


def automation_bias(
    prop: Proposal, facts: dict[str, str], rec: dict[str, Any], required: list[str]
) -> Decision:
    """Trusts output that is cited and sounds confident; checks only hedged output."""
    if rec["verified"] and prop["confident"]:
        return "accept", "", None, 1
    return competent(prop, facts, rec, required)


PANELS: dict[str, Panel] = {
    "competent": competent,
    "default_accept": default_accept,
    "automation_bias": automation_bias,
}


def gate_satisfied(
    prop: Proposal,
    rec: dict[str, Any],
    labels: list[str],
    facts: dict[str, str] | None = None,
    required: list[str] | None = None,
    authority: dict[str, Any] | None = None,
) -> tuple[bool, str]:
    """Controlled gate: only an evidenced human answer satisfies it, never over a defect."""
    ev = rec.get("review_evidence")
    if not ev or not ev.get("reviewer") or rec["status"] == "Not reviewed":
        return False, "no recorded human review"
    if authority is not None:
        if ev["reviewer"] not in authority["authorised_reviewers"]:
            return False, "reviewer holds no defined authority for this task"
        if not authority.get("task") or authority["task"] != rec.get("task"):
            return False, "authority does not cover the reviewed task"
        held = {
            "reviewer": bool(ev.get("reviewer")),
            "source_hashes": bool(ev.get("source_hashes")),
            # Correct controls have no discrepancy to cite, so a source reason is exempt for them.
            "source_reason": not prop["defect"] or SOURCE_TAG in rec["reviewer_reason"],
        }
        for need in authority.get("required_evidence", []):
            if not held.get(need):
                if need == "source_hashes":
                    return False, "review evidence lacks the source version reviewed"
                return False, f"required evidence missing or unsupported: {need}"
    action, reason = rec["reviewer_action"], rec["reviewer_reason"]
    if prop["defect"]:
        if action == "accept":
            return False, "seeded defect accepted"
        source = reason.partition(SOURCE_TAG)[2].rstrip("]")
        if not reason or source not in labels:
            return False, "reason does not name a source that resolves in the case"
        if facts is not None:
            found = _findings(prop, facts, required or [])
            if not any(source == src and t in reason for _, t, src in found):
                return False, "reason does not identify the seeded discrepancy and its source"
        if action == "edit" and not replacement_effective(prop, rec, facts or {}, required or []):
            return False, "edit does not correct the defect or omits required facts"
        return True, "defect corrected or rejected with source and reason"
    if action == "reject":
        return False, "correct control rejected"
    if action == "edit" and not replacement_effective(prop, rec, facts or {}, required or []):
        return False, "edited control no longer matches source facts"
    return True, "control accepted"


def _store(workdir: str, spec: dict[str, Any], output: list[str]) -> Store:
    p = Path(workdir) / "eval.json"
    p.write_text(json.dumps(dict(staff=[OWNER, OTHER], cases=[build_case(spec["case"])])))  # type: ignore[no-untyped-call]
    store = Store(str(p), os.path.join(workdir, "live.json"), os.path.join(workdir, "audit.jsonl"))
    store.ai.endpoint = "http://scripted-model.invalid"
    store.release_block = lambda *a, **k: None
    store.release_context = lambda task, dep=None: dict(
        id=f"offline-review-test:{task}", version="scripted-v1", digest="0"
    )
    store.ai.release = store.release_context
    store.release_current = lambda *a, **k: True
    store.ai._chat = lambda *a, **k: output[0]
    return store


def run_panel(
    name: str,
    panel: Panel,
    spec: dict[str, Any],
    workdir: str,
    actor: dict[str, str] = OWNER,
) -> dict[str, Any]:
    output = [""]
    store = _store(workdir, spec, output)
    case = store.cases[spec["case"]["id"]]
    labels = ai_tasks.source_labels(case, True)
    facts = _facts(labels)
    rows, effort = [], 0
    for prop in spec["proposals"]:
        output[0] = prop["output"]
        rec_view = store.ai_run(actor, spec["case"]["id"], spec["task"])
        if rec_view["source"] != "ai":
            raise RuntimeError(
                f"seeded proposal {prop['id']} was not served as AI output "
                f"(source={rec_view['source']}); check ZF_AI"
            )
        action, reason, text, units = panel(prop, facts, rec_view, spec["required_topics"])
        store.review_ai(actor, rec_view["record_id"], action, reason, text)
        rec = next(r for r in store.data["recommendations"] if r["id"] == rec_view["record_id"])
        ok, why = gate_satisfied(
            prop, rec, labels, facts, spec["required_topics"], spec.get("reviewer_authority")
        )
        effective = (
            bool(prop["defect"])
            and ok
            and (
                action == "reject"
                or (
                    action == "edit"
                    and replacement_effective(prop, rec, facts, spec["required_topics"])
                )
            )
        )
        effort += units
        rows.append(
            dict(
                proposal=prop["id"],
                defect=prop["defect"],
                citation_valid=rec_view["verified"],
                action=action,
                reviewer=rec["review_evidence"]["reviewer"],
                reason=rec["reviewer_reason"],
                source_case=rec["case_ids"],
                source_hashes=rec["review_evidence"]["source_hashes"],
                replacement=rec["override_text"],
                defect_corrected=effective,
                gate_satisfied=ok,
                gate_note=why,
                effort_units=units,
            )
        )
    defects = [r for r in rows if r["defect"]]
    controls = [r for r in rows if not r["defect"]]
    detected = [r for r in defects if r["defect_corrected"]]
    return dict(
        panel=name,
        rows=rows,
        effort_units=effort,
        reviews=len(rows),
        defects=len(defects),
        detected=len(detected),
        detection_rate=round(len(detected) / len(defects), 3) if defects else None,
        corrections=sum(r["action"] == "edit" and r["defect_corrected"] for r in defects),
        rejections=sum(r["action"] == "reject" for r in defects),
        false_rejects=sum(r["action"] == "reject" for r in controls),
        uncorrected_defects_through_gate=sum(
            r["gate_satisfied"] and not r["defect_corrected"] for r in defects
        ),
        uncorrected_defects=sum(not r["defect_corrected"] for r in defects),
        gate_passed=all(r["gate_satisfied"] for r in rows),
        audit_verified=bool(store.verify_audit()),
    )


def workflow_only(spec: dict[str, Any], workdir: str) -> dict[str, Any]:
    """The same case and workload in workflow-only mode, counted with the panel effort model."""
    output = [""]
    store = _store(workdir, spec, output)
    effort, verified, source, mode = 0, True, "", ""
    for _ in spec["proposals"]:
        view = store.ai_run(OWNER, spec["case"]["id"], spec["task"], mode="workflow")
        effort += max(len(view.get("citations") or []), 1) + 1
        verified, source, mode = verified and view["verified"], view["source"], view["mode"]
    return dict(
        source=source,
        mode=mode,
        verified=verified,
        seeded_defects=0,
        reviews=len(spec["proposals"]),
        effort_units=effort,
    )


def load_spec(golden: Path = GOLDEN) -> dict[str, Any]:
    """Load the golden spec; reviewer codes resolve to staff emails (none stored publicly)."""
    spec: dict[str, Any] = json.loads(golden.read_text(encoding="utf-8"))
    staff = {OWNER["code"]: OWNER["email"], OTHER["code"]: OTHER["email"]}
    authority = spec["reviewer_authority"]
    authority["authorised_reviewers"] = [
        staff[code] for code in authority.pop("authorised_reviewer_codes")
    ]
    return spec


def run_review_test(golden: Path = GOLDEN) -> dict[str, Any]:
    spec = load_spec(golden)
    panels = {}
    for name, panel in PANELS.items():
        with tempfile.TemporaryDirectory() as tmp:
            panels[name] = run_panel(name, panel, spec, tmp)
    with tempfile.TemporaryDirectory() as tmp:
        unauthorised = run_panel("unauthorised_competent", competent, spec, tmp, OTHER)
    with tempfile.TemporaryDirectory() as tmp:
        wf = workflow_only(spec, tmp)
    authority = spec["reviewer_authority"]
    comp = panels["competent"]
    baselines = [panels["default_accept"], panels["automation_bias"]]
    checks = dict(
        competent_detects_all_seeded_defects=comp["detection_rate"] == 1.0,
        no_uncorrected_defect_satisfies_gate=comp["uncorrected_defects_through_gate"] == 0
        and comp["uncorrected_defects"] == 0
        and comp["gate_passed"],
        default_acceptance_cannot_pass=not panels["default_accept"]["gate_passed"],
        citation_validity_alone_cannot_pass=not panels["automation_bias"]["gate_passed"]
        and all(r["citation_valid"] for p in baselines for r in p["rows"] if r["defect"]),
        automation_bias_misses_confident_cited_defects=panels["automation_bias"]["detected"]
        < panels["automation_bias"]["defects"],
        reviewer_source_reason_retained=all(
            r["reviewer"]
            and isinstance(r["source_hashes"], dict)
            and r["source_hashes"]
            and r["source_case"]
            and (r["reason"] or not r["defect"])
            for r in comp["rows"]
        ),
        reviewer_authority_defined=bool(
            authority["authorised_reviewers"] and authority["required_evidence"]
        ),
        unauthorised_reviewer_cannot_pass=not unauthorised["gate_passed"]
        and [r["action"] for r in unauthorised["rows"]] == [r["action"] for r in comp["rows"]]
        and all(not r["gate_satisfied"] for r in unauthorised["rows"]),
        audit_chain_verifies=all(p["audit_verified"] for p in panels.values()),
    )
    return dict(
        version=spec["version"],
        panels=panels,
        unauthorised_reviewer_control=unauthorised,
        workflow_only=wf,
        checks=checks,
        passed=all(checks.values()),
        effort_note="scripted comparison units, same case and workload (one review per "
        "proposal on both sides); not measured reviewer time",
        evidence=dict(
            provider="scripted",
            human_effectiveness="not evaluated (no authorised competent reviewers)",
            reviewer_authority=authority,
            open_items=list(OPEN_ITEMS),
        ),
    )


def main(argv: list[str] | None = None) -> int:
    rep = run_review_test()
    args = sys.argv[1:] if argv is None else argv
    if "--json" in args:
        print(json.dumps(rep, indent=2))
        return 0 if rep["passed"] else 1
    for name, p in rep["panels"].items():
        print(
            f"{name}: detected {p['detected']} of {p['defects']} seeded defects, "
            f"corrections {p['corrections']}, rejections {p['rejections']}, "
            f"false rejects {p['false_rejects']}, effort {p['effort_units']}, "
            f"gate {'PASS' if p['gate_passed'] else 'FAIL'}"
        )
    wf = rep["workflow_only"]
    print(f"workflow-only, same case: effort {wf['effort_units']}, defects {wf['seeded_defects']}")
    for k, v in rep["checks"].items():
        print(("PASS " if v else "FAIL ") + k)
    print(f"human effectiveness: {rep['evidence']['human_effectiveness']}")
    for o in rep["evidence"]["open_items"]:
        print("open: " + o)
    return 0 if rep["passed"] else 1


if __name__ == "__main__":
    sys.exit(main())
