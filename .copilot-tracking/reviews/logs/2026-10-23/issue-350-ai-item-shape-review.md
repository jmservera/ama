---
title: Offline feedback AI item shape original RPI Review
description: One postimplementation review of bounded correction and residual gates
ms.date: 2026-10-23
---

## Scope and Evidence

Task ID/slug: issue-350-ai-item-shape. Review date: 2026-10-23.
Boundary: complete bounded correction, not whole issue #350 acceptance.

* Plan: .copilot-tracking/plans/2026-10-23/issue-350-ai-item-shape-plan.md
* Details: .copilot-tracking/details/2026-10-23/issue-350-ai-item-shape-phase-details.md
* Critique: .copilot-tracking/reviews/plans/2026-10-23/issue-350-ai-item-shape-plan-critique.md
* Changes: .copilot-tracking/changes/2026-10-23/issue-350-ai-item-shape-changes.md
* Research: .copilot-tracking/research/2026-10-23/issue-350-ai-item-shape-research.md
* Implementation: tools/check-demo-feedback.py, tools/test_check_demo_feedback.py
* Runtime authority: ai_tasks.priority_items, Store.ai_priority/_rec_view, API POST.
* Actual validation logs: /tmp/ama-350-ai-item-shape-20261023-evidence-0752/

## Opening Review State

Goal: compare FR1-FR4, NFR1-NFR3, AC1-AC5, P01 completion and P02/P03 remaining
delivery with actual code/tests and one critique disposition set. Evidence is
current and reviewable. First boundary: captured structural fields versus actual
runtime/API output, then regression coverage and acceptance limits.
Only this Review record is review-writable. No in-scope blocker known at opening.
Full gate, commit and publication are pending by approved sequence; independent
coordinator assessment is later and not part of this self-review.

## Execution Status

Complete. Exactly one original postimplementation self-review executed against
the current bounded implementation and canonical evidence. No source edits in
Review; this is not the coordinator's independent exact-head assessment.

## Plan-to-Change Reconciliation

| Scope | Assessment | Evidence |
| --- | --- | --- |
| FR1/FR2, P01-T02 | Satisfied | Existing predicate now checks nonempty string case_id/reason and all cite elements; list/object checks and Verdict FAIL unchanged |
| FR3, AC4 | Satisfied | Enriched fixture and two genuine runtime-validator items pass component check; no exact key set or length/syntax cap |
| FR4/NFR1 | Satisfied | No change outside item guard/module docs; no new checker import, IO, network, credentials or AI activation |
| AC1/AC3, P01-T01 | Satisfied | Six new methods; genuine pre-fix red has 44 failures across five methods; positive runtime-validator method remains green |
| AC2 | Satisfied | All 70 focused tests, targeted Ruff lint/format and whitespace checks pass |
| NFR2 | Satisfied for tests | Installed namespace packages in isolated external venv, -B and no-cache; task-created install metadata/initial bytecode cleanup remains before gate |
| NFR3 | Satisfied | Prior artifacts untouched; one critique and this one Review |
| P02/P03, AC5 | Pending delivery | Approved sequence requires this original Review and candidate commit before one full gate/receipt/push |

## Completed Work Assessment

Checker diff is nine additions and one deletion: three documentation lines and
the expanded existing predicate. Short-circuit guards reject missing/wrong
types before nested iteration. `nonempty_str` rejects empty/whitespace without
coercion. Requiring strings matches captured runtime output even though runtime
coerces raw model citations before source resolution.

The 44 red failures decompose into missing fields (2), text values (20),
citations (18), mixed item lists (2) and supplied reproductions (2). Other
already-rejected container cases and the positive test did not falsely fail.
All 70 methods then pass, including unchanged safety/overall-verdict tests.
No citation semantics or evidence truth inferred. Both per-component outcomes
and explicit residual acceptance are asserted, not aggregate status alone.

## Implementation-Time Update and Critique Assessment

Plan/detail updates only synchronize P01 markers, execution evidence and package
metadata cleanup; no change of requirements or material divergence. No unrelated
follow-up was introduced. User intent and summary remain synchronized.

Critique executed once with original Revise verdict preserved. PC-001 correctly
rejected: parent has explicit external-output authority and no /tmp prohibition;
the worker-local restriction is not a parent constraint. PC-002 applied before
source edits: new unresolved in-scope blocking Review findings would stop gate
and publication. No such defect found in this assessment. No repeated critique
or Review is requested or performed.

## Findings

<!-- rpi:review id=RV-001 -->
### RV-001 [Low]: Exact-head gate and publication remain pending at Review time

* Scope: P02-T02/P03.
* Evidence: original Review precedes candidate commit by explicit approved
  sequence. Full gate/receipt/normal push/PR update have not run yet.
* Impact: focused success is not publication evidence or exact-head acceptance.
* Destination: parent delivery continuation P02-T02/P03, not source rework.
* Next action: commit reviewed candidate, run exactly one full gate with fixed
  base/lock timeout, verify receipt and publish only if it passes.

<!-- rpi:review id=RV-002 -->
### RV-002 [Low]: Independent coordinator and live acceptance remain separate

* Scope: excluded whole-issue acceptance; no local source defect.
* Evidence: user reserves coordinator assessment after this report. Offline
  fixtures never prove SQL durability, actual AI execution or deployment;
  current issue #350 is open with ten unticked criteria.
* Impact: no merge/approval, real tenant/staff, spend/admin or feature acceptance
  can be inferred from this correction or later local gate.
* Destination: distinct coordinator and owner-governed acceptance follow-ups.
* Next action: coordinator assesses exact delivered head/receipt; owner handles
  excluded deployed prerequisites without changing issue criteria here.

## Defects and Routing

No in-scope implementation defect, material research gap or unresolved user
decision found. RV-001 is expected delivery continuation, not a second RPI loop.
RV-002 stays outside active correction acceptance. No plan follow-up was added.
Known excluded live criteria remain open; no human approval box is ticked.

## Validation Evidence

| Check | Result | Boundary |
| --- | --- | --- |
| Red unittest AiEvidence | Expected failure | 16 tests, 44 failing subtests before checker edit |
| Focused unittest full module | Passed | 70 tests; installed packages, -B |
| Ruff 0.17.1 lint | Passed | Both changed tools; E,F,W,B,BLE,I, E501 ignored |
| Ruff format and diff check | Passed | Both tools; isolated/no cache; no whitespace errors |
| Full gate/receipt verifier | Not run yet | Requires original Review and committed clean candidate |
| SQL/live model/Azure/paid/deployed acceptance | Not run | Explicitly excluded; not implied by synthetic output |
| Independent coordinator/human/hosted acceptance | Not run | Later, distinct authority |

External log hashes (SHA-256):

* red.log: 06c380f6c4140e14d9794a07f725b173e3a94a60d6288fcd36e7a3c2a16455b0
* green.log: d0e63356e5ca3a40a487f786ec193e768c5f94693a54351fa734c7629e00e1e8

Pre-commit parent HEAD: 5f14378c383f35bffe91abdda7730045baaecb1d.
Fetched main/base: 140d8f494482c78e84d15f3d46b9223d3c487af0.

## Outcome and Closeout Routing

Execution: Complete. Outcome: Residual work. Bounded source correction and
focused evidence satisfy FR1-FR4; full publication is not yet accepted because
RV-001 is pending. No unresolved in-scope blocking Review finding prevents
authorized candidate commit/gate. No overall or independent conformance claim.

| Finding class | Destination | Owner/action |
| --- | --- | --- |
| Implementation defect | None | No source rework |
| Decision gap | None | Current user sequence is explicit |
| Material evidence gap | None in bounded contract | No new research |
| Delivery residual | RV-001 | Parent commit/gate/verification/push/PR update |
| Independent/live residual | RV-002 | Coordinator then owner-governed acceptance |

Original Review remains unchanged after commit. Later gate receipt and delivery
outcome must be recorded externally and in PR rather than an evidence commit
that invalidates the exact-head receipt. No second Review to verify closure.
