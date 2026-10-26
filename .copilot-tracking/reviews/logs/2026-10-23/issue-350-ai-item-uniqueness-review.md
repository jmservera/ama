---
title: Issue 350 AI item uniqueness original RPI Review
description: One postimplementation review of bounded second correction
ms.date: 2026-10-23
---

## Scope and Evidence

Task ID/slug: issue-350-ai-item-uniqueness. Review date: 2026-10-23.
Review boundary: complete bounded correction, not whole issue #350.
Canonical compared artifacts:

* .copilot-tracking/research/2026-10-23/issue-350-ai-item-uniqueness-research.md
* .copilot-tracking/plans/2026-10-23/issue-350-ai-item-uniqueness-plan.md
* .copilot-tracking/details/2026-10-23/issue-350-ai-item-uniqueness-phase-details.md
* .copilot-tracking/reviews/plans/2026-10-23/issue-350-ai-item-uniqueness-plan-critique.md
* .copilot-tracking/changes/2026-10-23/issue-350-ai-item-uniqueness-changes.md

Implementation: tools/check-demo-feedback.py, tools/test_check_demo_feedback.py.
Authority: src/core/src/zava_forward/core/ai_tasks.py, priority_items.
Logs: /tmp/ama-350-ai-item-uniqueness-20261023-evidence-wZJWUQhM/.

## Opening Review State

Goal: assess FR1-FR3, NFR1-NFR3, AC1-AC5 and P01-P03 evidence.
P01 complete and evidence synchronized; P02 original Review precedes commit
and P03 by explicit sequence. First comparison: guard safety/raw uniqueness,
then regression evidence and offline boundaries. Only this Review record is
review-writable; no source changes or second Review. Initial implementation
blocker: none. Publication lineage remains a coordinator-owned blocker.
This is implementer self-review, not independent coordinator acceptance.

## Execution Status

Complete. Exactly one original postimplementation RPI Review performed.
No source edits or repeated Review; no delegated lens was needed for this
small, directly inspectable diff. Outcome: Residual work.

## Plan-to-Change Reconciliation and Completed Work

| Basis | Assessment | Evidence |
| --- | --- | --- |
| FR1 / P01-T01/T02 | Satisfied | Set-cardinality elif rejects equal IDs regardless of payload or position; six red subtests cover both accepted origin labels |
| FR2 / AC3 | Satisfied | Distinct, case-varied and space-varied ID pairs pass without normalization; original two-item runtime-validator positive remains |
| FR3 / NFR1 | Satisfied | Structural predicate guards set construction; existing malformed/unhashable-ID tests retained; no import, network, credentials, write, count or source rule added |
| AC1 | Satisfied | Actual 18-method red has six PASS != FAIL subtest failures; distinct matrix and other methods green |
| AC2 | Satisfied | Final full module 72 tests passes, all original 70 retained; Ruff lint/format and whitespace pass |
| AC3 | Satisfied | Explicit component FAIL/diagnostic for duplicates; positive tests retain SQL blocked, spend/admin not-run, overall blocked, acceptance not-accepted |
| AC4 | Satisfied | Source diff: two guard lines plus one documentation clarification; 42 added test lines; only seven new correction artifacts, prior history untouched |
| NFR2 | Satisfied for focused execution | Existing editable namespace packages, -B/no-cache; pre-existing ignored bytecode requires pre-gate hygiene, RV-001 |
| NFR3 | Satisfied to current phase | One critique with dispositions and this one Review; one complete gate remains downstream |
| P02-T02 / P03 / AC5 | Pending by sequence | Original Review must precede commit and gate; no premature gate/verifier result claimed |

The existing malformed-ID matrix includes lists/dicts. The `elif` is reached
only after every ID is proven a nonempty string, so it cannot introduce
unhashable-input exceptions or mask existing cited-item failures. Equal raw
strings are compared without stripping or case folding, matching the bounded
runtime uniqueness rule while deliberately omitting runtime membership,
citation resolution and count rules.

Tests distinguish same-ID/different-payload repetition from whole-object
duplication and nonadjacent repetition from adjacent-only detection. Both
accepted evidence-origin labels are tested using synthetic fixtures; the
`deployed-capture` string is not proof of an actual capture or deployment.

## Implementation-Time Update Assessment

Plan/detail updates only mark genuine red/green completion and reconcile
remaining P02/P03 work. The formatter's one assertion-line reflow is ordinary
local judgment, not a requirement change. Executive summary, current user
direction, source boundary, test ownership and two-method ceiling agree.
No significant divergence, paused dependent source work or new decision gap.

## Critique Disposition Assessment

One independent final-candidate critique executed, original Revise retained.
PC-001/PC-002 are both explicitly rejected in the plan: they assume a temporary
path prohibition not present in parent instructions. Actual baseline/import
and package metadata establish the named interpreter, and the caller expressly
requires the unchanged runner/shared lock. Rejection preserves confirmed
direction; no bypass or gate patch is proposed. No repeated critique required.

## Plan Follow-Up Assessment

| Follow-up | Boundary and route |
| --- | --- |
| PR lineage | Existing local/remote divergence is not a uniqueness defect; coordinator resolves separately, no push/rewrite here |
| Independent exact-head assessment | Later coordinator authority, not this implementer's self-review or local gate |
| Original deployed acceptance | Original issue remains OPEN with all ten criteria unticked; owner-governed live prerequisites remain outside this correction |

These are retained distinct follow-ups, not added source work or accepted
original issue criteria.

## Findings

<!-- rpi:review id=RV-001 -->
### RV-001 [Low]: Committed-head gate and receipt remain pending

* Scope: P02-T02/P03/AC5.
* Evidence: by required order this Review precedes candidate commit and gate.
  Ignored bytecode exists in tools, core and API `__pycache__` directories;
  file mtimes are 08:34:22-23 UTC, before this task's 08:35:45 intake.
* Impact: focused green is not complete exact-head validation. Pre-existing
  generated cache inputs must be preserved externally/removed from candidate
  before the unchanged gate, not treated as authored source or committed.
* Destination: parent authorized delivery continuation, no source rework.
* Next action: preserve generated cache contents externally, clean only those
  known bytecode files, commit reviewed correction/evidence, run exactly one
  gate with fixed base/86400 timeout, explicit official verifier and hash.

<!-- rpi:review id=RV-002 -->
### RV-002 [Low]: Publication lineage and independent/live acceptance remain unresolved

* Scope: excluded publication and whole-issue acceptance.
* Evidence: read-only PR query shows #436 OPEN on requested branch. Current
  remote-tracking comparison is 11 local-only / six remote-only commits at
  pre-correction head. Read-only issue query confirms #350 OPEN, ten unticked
  criteria. No push, PR-body edit or issue mutation was performed.
* Impact: no normal/force push, rewritten lineage, independent approval,
  hosted result, merge or deployed/actual AI/SQL acceptance follows from this
  correction or its later local gate.
* Destination: distinct coordinator lineage resolution and independent
  exact-head assessment; owner retains governed live acceptance.
* Next action: stop after local validation and report exact commit/receipt.

## Validation Evidence

| Check | Status | Observed result |
| --- | --- | --- |
| Installed-package baseline | Passed | 70 tests |
| Pre-fix AiEvidence red | Failed as expected | 18 methods, six duplicate subtest failures, exit 1 |
| Final focused full module | Passed | 72 tests, exit 0 |
| Ruff 0.17.1 lint / final format | Passed | Two changed tools, isolated/no-cache |
| git diff --check | Passed | No whitespace errors |
| Complete gate / receipt verifier | Not run yet | Requires reviewed commit and pre-gate hygiene |
| Actual SQL/AI/deployed acceptance, cloud/paid actions | Not run | Excluded; local synthetic contracts cannot establish these |
| Independent coordinator/human/hosted approval | Not run | Separate authority |

Original log SHA-256 values checked against changes evidence:

* red.log: 5cece406e45e11e50da8015bb2e2afb6adfe65da29ad8aa6f639a8941e8c1db4.
* green-final.log: 43bbd46ccefbb17c904be1676ef4f9820635c53206d91d77437e38fa3cad3e27.

Pre-commit head: a01b36f86e36092cbe4d90a1b9db87a95a34531d.
Fetched main matches fixed base: 140d8f494482c78e84d15f3d46b9223d3c487af0.
GitHub account resolved: id 8036360, login jmservera; parent must configure
repository-local privacy-safe author/committer identity before commit.

## Outcome and Closeout Routing

Execution Complete; outcome Residual work. No in-scope implementation defect,
material research gap or unresolved direction prevents authorized commit/gate.
Do not claim full task validation before RV-001 delivery completes. Preserve
this original Review unchanged; downstream receipt/status belongs externally.
No second Review or source closure-verification cycle is authorized here.

| Finding class | Destination | Owner |
| --- | --- | --- |
| Implementation defect | None | No source rework |
| Decision gap | None | Current explicit direction sufficient |
| Material evidence gap | None for bounded uniqueness | No additional research |
| Delivery residual, RV-001 | Existing P02-T02/P03 continuation | Parent |
| Publication/independent/live residual, RV-002 | Separate follow-ups | Coordinator then owner |
