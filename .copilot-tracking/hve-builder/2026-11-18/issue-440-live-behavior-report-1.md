---
title: "HVE Artifact Test Report: AMA Backlog Delivery Coordinator at d7d7fdee3"
description: "Simulation-fidelity behavior test of the coordinator agent after #1903, #1843 and #1821"
ms.date: 2026-11-18
---

* Tested profile: Medium (inferred; the agent omits `model:`). The executor `hve-core-all:hve-artifact-tester` was dispatched without an explicit model, so it inherited the invoking session model. The profile and model are therefore a disclosed proxy, not intended-profile evidence.
* Run type: full
* Behavior gate: Executed
* Fidelity: simulation
* Execution status: Complete (5 of 5 scenarios traced)
* Verdict: Pass, provisional. The grading was done by the lead, not a fresh-context grader, because the parent task disallowed nested general-purpose delegation. Treat the verdict as `Pass` pending an independent grading rerun.
* Sandbox: cleaned up (`.copilot-tracking/sandbox/2026-11-18-issue-440-live-1/`)
* Target identity: HEAD `d7d7fdee3`, sha256 `b688648e2761d09ba03fb33a12fc729e0028202e3a66d8e27fda4768eb211dce`

## Scenarios and results

| Scenario | Requirement | Observed behavior (simulated) | Result |
| --- | --- | --- | --- |
| S1 idle tick with 30 unclassified issues, 2 green PRs lacking receipts, a linkless blocker | REQ-01 | Refused to post "nothing changed", classified every issue, treated the cached blocker as inspection work, routed receipt work, launched ready issues, rendered the table first, validated the note with `check-coordinator-handoff.py` | As intended |
| S2 restart with a delivery recurrence referencing cleanup `#2` and live cleanup `#11` | REQ-02 | Kept cleanup `#11`, replaced the non-matching delivery by create, verify, stop, read-back, substituted only the cleanup handle | As intended |
| S3 launch docs-only issue 1700 | REQ-03 | Focused tier, fresh brief, witness `record launch` with `--claim-model gemini-4-carbon`, qualified agent, tmux route, watch armed; no silent model fallback | As intended; see finding F2 (model fallback versus retry) |
| S4 watcher exit 2 for finished `rpi-1800` | REQ-04 | Inspected log and exit, classified finished, ran witness verify, refilled 3 ready issues, re-armed the watch | As intended; see behavior adjustment B5 |
| S5 green MERGEABLE SQL PR without a full receipt | REQ-05 | Refused merge; routed receipt production; no human blocker | As intended; see behavior adjustment B2 |

## Findings (behavior evidence)

| # | Action | Mapped dimension | Severity | Evidence | Resolving change |
| --- | --- | --- | --- | --- | --- |
| B1 | adjustment | Workflow contract | Medium | S3: "no silent fallback" versus "retried once"; executor had to infer. Same as static F2 | Static F2 change |
| B2 | adjustment | Workflow contract | Low | S5: receipt production for an already-published PR has two possible owners (step 5 versus step 8) | State that the coordinator or a continuation session may run it (step 8 wording already allows both); cross-reference from step 5 |
| B3 | adjustment | Workflow contract | Low | S1, S5: "run opened or adopted" undefined. Same as static F3 | Static F3 change |
| B4 | improvement | Context handling | Low | S1: no batch bound for classifying many open issues in one tick | Allow a classification to span the tick, each unclassified issue needing a named inspection action |
| B5 | improvement | Workflow contract | Low | S4: `exit=0` with missing artifacts is not explicitly the "exits without them" case | Name that case in the retry-once rule |

No Critical or High behavior findings.

## Fidelity and limitations

* Observed: reading the target and run-state; the executor wrote no files (post-run `git status` shows only the two pre-existing untracked files plus this run's evidence and sandbox).
* Simulated: every coordinator decision in S1 to S5.
* Emulated: all `gh`, `tmux`, `python3 tools/*`, `manage_schedule` and `git` results.
* Proxy and tier limit: the executor model was inherited rather than selected for the Medium profile, and a Medium or higher simulator may repair ambiguity a lower tier would expose. This run does not establish behavior at the artifact's lowest-tier use, native-host behavior, live board or schedule behavior, or tmux process creation.
* Prior behavior evidence (2026-11-15 and 2026-11-05/06) was not reused; source identity differs, so this is a full run.

## Untested behavior

Live GitHub, project board, `manage_schedule`, tmux and Azure actions; full-tier gates; native `/agent` discovery.

## Human review

* [ ] Reviewed and validated by a qualified human reviewer
