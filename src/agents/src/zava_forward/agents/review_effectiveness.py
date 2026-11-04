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

import hashlib
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
        audit_chain_verifies=all(p["audit_verified"] for p in (*panels.values(), unauthorised)),
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


def worksheet(golden: Path = GOLDEN) -> dict[str, Any]:
    """Blank answer sheet for a human reviewer: proposal text only, no defect hints."""
    spec = load_spec(golden)
    return dict(
        version=spec["version"],
        reviewer_code="",
        workflow_seconds=None,
        instructions="For each proposal answer accept, edit or reject. Name a source as "
        f"'{SOURCE_TAG}<case label>]' in the reason for any change. Record seconds spent. "
        "Complete the manual comparison without AI help.",
        answers={
            p["id"]: dict(
                proposal=p["output"], action="", reason="", replacement=None, seconds=None
            )
            for p in spec["proposals"]
        },
    )


def score_human_session(sheet: dict[str, Any], golden: Path = GOLDEN) -> dict[str, Any]:
    """Score one recorded human answer sheet through the same gate and report as the panels.

    Measured seconds replace scripted effort units. The tool cannot verify who the person is or
    whether they are competent; that remains an OQ-017 owner decision.
    """
    if not isinstance(sheet, dict):
        raise ValueError("answer sheet must be a JSON object")
    spec = load_spec(golden)
    if sheet.get("version") != spec["version"]:
        raise ValueError(
            f"answer sheet is for scenario version {sheet.get('version')!r}, "
            f"not the current {spec['version']!r}; print a fresh worksheet"
        )
    actors = {OWNER["code"]: OWNER, OTHER["code"]: OTHER}
    actor = actors.get(str(sheet.get("reviewer_code")))
    if actor is None:
        raise ValueError("reviewer_code must name an evaluation staff record")
    answers = sheet.get("answers") or {}
    if not isinstance(answers, dict):
        raise ValueError("answers must be an object keyed by proposal id")
    unknown = sorted(set(answers) - {p["id"] for p in spec["proposals"]})
    if unknown:
        raise ValueError(f"answers name proposals outside the scenario: {', '.join(unknown)}")
    for prop in spec["proposals"]:
        a = answers.get(prop["id"]) or {}
        if not isinstance(a, dict):
            raise ValueError(f"proposal {prop['id']} answer must be an object")
        if a.get("action") not in ("accept", "edit", "reject"):
            raise ValueError(f"proposal {prop['id']} has no accept, edit or reject answer")
        seconds = a.get("seconds")
        if isinstance(seconds, bool) or not isinstance(seconds, int | float):
            raise ValueError(f"proposal {prop['id']} has no measured seconds")
        if not 0 < seconds < 1e9:
            raise ValueError(f"proposal {prop['id']} has no measured seconds")

    def human(
        prop: Proposal, facts: dict[str, str], rec: dict[str, Any], required: list[str]
    ) -> Decision:
        a = answers[prop["id"]]
        return a["action"], a.get("reason") or "", a.get("replacement"), int(round(a["seconds"]))

    with tempfile.TemporaryDirectory() as tmp:
        panel = run_panel("human_session", human, spec, tmp, actor)
    workflow = sheet.get("workflow_seconds")
    measured = isinstance(workflow, int | float) and not isinstance(workflow, bool) and workflow > 0
    confident = {p["id"]: p["confident"] for p in spec["proposals"]}
    by_class: dict[str, dict[str, int]] = {}
    for r in panel["rows"]:
        if r["defect"]:
            c = by_class.setdefault(str(r["defect"]), dict(seeded=0, detected=0))
            c["seeded"] += 1
            c["detected"] += bool(r["defect_corrected"])
    trusted = [
        r["proposal"]
        for r in panel["rows"]
        if r["defect"]
        and r["citation_valid"]
        and confident[r["proposal"]]
        and r["action"] == "accept"
    ]
    return dict(
        version=spec["version"],
        panel=panel,
        by_defect_class=by_class,
        automation_bias=dict(
            confident_cited_defects_accepted=trusted,
            note="a defect that carried valid citations and confident wording was accepted"
            if trusted
            else "no confident, cited defect was accepted",
        ),
        effort_comparison=dict(
            same_scenario_reviews=panel["reviews"],
            human_review_seconds=panel["effort_units"],
            workflow_only_seconds=workflow if measured else None,
            difference_seconds=round(panel["effort_units"] - workflow, 1) if measured else None,
        ),
        measured_seconds=panel["effort_units"],
        workflow_only_seconds=workflow if measured else None,
        gate_passed=panel["gate_passed"],
        evidence=dict(
            human_effectiveness="recorded for one session; competence and authorisation of the "
            "person are not verified by this tool",
            open_items=[o for o in OPEN_ITEMS if not o.startswith("effort is scripted")],
            workflow_time_note="workflow-only seconds supplied by the reviewer"
            if measured
            else "workflow-only time not measured for this session",
        ),
    )


def pool_human_sessions(sheets: list[dict[str, Any]], golden: Path = GOLDEN) -> dict[str, Any]:
    """Score several completed sheets and pool detection and total review effort.

    Each sheet runs through the same gate on its own. The pool never hides a failed session, and a
    repeat reviewer code is not an independent reviewer. A sheet whose content is identical to an
    earlier one is flagged under duplicate_sheets and left out of every total, so effort and
    detection are not double-counted. No sample size or threshold is approved.
    """
    if not isinstance(sheets, list) or not sheets:
        raise ValueError("at least one completed answer sheet is required")
    seen: dict[str, int] = {}
    unique: list[dict[str, Any]] = []
    duplicates: list[dict[str, Any]] = []
    for pos, sh in enumerate(sheets):
        try:
            canon = json.dumps(sh, sort_keys=True, separators=(",", ":"), default=str)
        except (TypeError, ValueError):
            canon = repr(sh)
        digest = hashlib.sha256(canon.encode("utf-8")).hexdigest()
        if digest in seen:
            duplicates.append(
                dict(
                    position=pos,
                    duplicate_of=seen[digest],
                    reviewer_code=str(sh.get("reviewer_code")) if isinstance(sh, dict) else None,
                    fingerprint=digest[:12],
                )
            )
            continue
        seen[digest] = pos
        unique.append(sh)
    sheets = unique
    results = [score_human_session(sh, golden) for sh in sheets]
    by_class: dict[str, dict[str, int]] = {}
    for res in results:
        for name, c in res["by_defect_class"].items():
            t = by_class.setdefault(name, dict(seeded=0, detected=0))
            t["seeded"] += c["seeded"]
            t["detected"] += c["detected"]
    workflow = [r["workflow_only_seconds"] for r in results]
    complete = all(w is not None for w in workflow)
    human = sum(r["measured_seconds"] for r in results)
    codes = [str(sh["reviewer_code"]) for sh in sheets]
    return dict(
        sessions=[
            dict(
                reviewer_code=code,
                gate_passed=r["gate_passed"],
                detected=r["panel"]["detected"],
                defects=r["panel"]["defects"],
                human_review_seconds=r["measured_seconds"],
                workflow_only_seconds=r["workflow_only_seconds"],
                confident_cited_defects_accepted=r["automation_bias"][
                    "confident_cited_defects_accepted"
                ],
            )
            for code, r in zip(codes, results, strict=True)
        ],
        session_count=len(results),
        duplicate_sheets=duplicates,
        duplicate_note=f"{len(duplicates)} identical sheet(s) flagged and excluded from totals"
        if duplicates
        else "no duplicate sheets detected",
        distinct_reviewers=len(set(codes)),
        sessions_passed=sum(r["gate_passed"] for r in results),
        all_sessions_passed=all(r["gate_passed"] for r in results),
        by_defect_class=by_class,
        sessions_with_automation_bias_exposure=sum(
            bool(r["automation_bias"]["confident_cited_defects_accepted"]) for r in results
        ),
        effort_comparison=dict(
            human_review_seconds=human,
            workflow_only_seconds=sum(workflow) if complete else None,
            difference_seconds=round(human - sum(workflow), 1) if complete else None,
            note="workflow-only seconds supplied by every reviewer"
            if complete
            else "workflow-only time missing for at least one session; no pooled comparison",
        ),
        evidence=dict(
            human_effectiveness="recorded for the sessions supplied; identity, competence and "
            "authorisation of each person are not verified by this tool",
            open_items=[
                "no sample size or pass threshold is approved; a pooled result is not conformance",
                *[o for o in OPEN_ITEMS if o.startswith("reviewer authority")],
            ],
        ),
    )


def main(argv: list[str] | None = None) -> int:
    args = sys.argv[1:] if argv is None else argv
    if "--worksheet" in args:
        print(json.dumps(worksheet(), indent=2))
        return 0
    if "--score" in args:
        i = args.index("--score")
        if not [a for a in args[i + 1 :] if not a.startswith("--")]:
            print("--score needs the path of a completed answer sheet", file=sys.stderr)
            return 2
        paths = [a for a in args[i + 1 :] if not a.startswith("--")]
        try:
            sheets = [json.loads(Path(x).read_text(encoding="utf-8")) for x in paths]
            if len(sheets) > 1:
                pooled = pool_human_sessions(sheets)
                print(json.dumps(pooled, indent=2))
                return 0 if pooled["all_sessions_passed"] else 1
            result = score_human_session(sheets[0])
        except (OSError, ValueError) as exc:
            print(f"cannot score session: {exc}", file=sys.stderr)
            return 2
        print(json.dumps(result, indent=2))
        return 0 if result["gate_passed"] else 1
    rep = run_review_test()
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
