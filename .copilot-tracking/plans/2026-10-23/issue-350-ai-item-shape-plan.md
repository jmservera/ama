---
title: Offline feedback AI item shape correction plan
description: Bounded implementation checklist for issue 350 and draft PR 436
ms.date: 2026-10-23
---

## Task Metadata

* Task ID and slug: issue-350-ai-item-shape
* Planning status: Ready; one critique executed and findings disposed
* Phase details: .copilot-tracking/details/2026-10-23/issue-350-ai-item-shape-phase-details.md
* Critique: .copilot-tracking/reviews/plans/2026-10-23/issue-350-ai-item-shape-plan-critique.md

## Executive Summary

Reject captured AI priority items lacking nonempty string case IDs, reasons or
citations. Reuse the existing guard/helper and retain valid runtime-shaped data.
Add red-first tests before the checker change. No semantic citation verification,
new limits, network/AI activation or deployed acceptance is introduced.

### What You May Not Know

Runtime coerces model-input citations before resolving them, but its published
output contains strings. The checker examines that published shape, not model
input. Source truth is not available offline. The original RPI Review must be
committed before the one full exact-HEAD gate; the receipt stays external so no
later evidence commit invalidates it. Coordinator independent review is later.

No implementation decision is unresolved. Full gate/publication are pending.
An unresolved in-scope blocking Review finding stops gate and publication;
excluded live/coordinator acceptance does not become local acceptance.

## Sources

* .copilot-tracking/research/2026-10-23/issue-350-ai-item-shape-research.md:
  C1-C8 establish runtime/API shape, reproductions, test layout and boundaries.
* src/README.md: local RPI gate sequence.
* User request dated 2026-10-23: exact branch/base/candidate and delivery authority.

## User Decisions and Requirements

* Run research, plan, implement, then one Review with dated artifacts.
* Work only here on existing branch `test/deployed-feedback-harness-350` and
  update draft PR #436, preserving prior RPI/critique/Review evidence.
* Reject malformed item shape/citation types against actual runtime contract,
  with red-first focused regressions and retained valid evidence.
* No semantic citation validation, arbitrary limits, unrelated cleanup or cloud work.
* Commit first using resolved GitHub privacy identity and required trailer;
  then exactly one full gate with supplied base and lock-timeout 86400.
* Verify receipt, report exact identities/hash; push normally only on success.
* Keep #350 open/unticked; SQL durability, spend/admin and all deployed acceptance
  remain blocked/not-run; coordinator review and merge are not claimed.

## Goals

* Eliminate the reproduced false component PASS without weakening other checks.
* Make red/green behavior and residual acceptance boundaries reproducible.

## Scope and Non-Goals

In scope: two existing checker/test files; checker module documentation;
this correction's tracking artifacts and existing draft PR description.
No other source, UI, runtime behavior or issue acceptance modification.
No source-label resolution, source snapshot, citation grammar, ID-format or
length restriction, deployment, private datasets, credentials or AI activation.

## Functional Requirements

* FR1: Each captured item is an object with nonempty string case_id and reason.
* FR2: Each cites value is a nonempty list of nonempty strings; any malformed
  entry fails `ai_evidence` through existing Verdict FAIL diagnostics.
* FR3: Runtime-shaped evidence still gives component PASS; additional runtime
  display fields remain allowed.
* FR4: Existing response/release/latency/source checks are unchanged;
  overall acceptance never becomes accepted.

## Non-Functional Requirements

* NFR1: No new imports/dependencies, coercion, broad catches, IO or activation.
* NFR2: Tests use installed namespace distributions in an external isolated
  venv; bytecode/cache output must not dirty the candidate.
* NFR3: Preserve existing evidence and one-pass critique/Review history.

## Acceptance Criteria

* AC1: Before-fix tests fail specifically for formerly accepted malformed items.
* AC2: After-fix focused suite passes; per-component FAIL/PASS asserted directly.
* AC3: Both supplied reproductions fail; missing/wrong-type case_id/reason and
  non-string/empty/whitespace cites covered, including a mixed valid/invalid list.
* AC4: Positive runtime validator output and enriched fixture pass shape checks;
  case_write_reload blocked, spend/admin not-run, acceptance not-accepted.
* AC5: One RPI Review reconciles artifacts/tests before commit. One complete
  full gate, exact receipt verification and normal push/PR update follow.
  Full-gate evidence is external, never claimed before actual completion.

## Test Ownership and Locked Scope

* Canonical tests: tools/test_check_demo_feedback.py, class AiEvidence.
* Removals: none. Maximum additions: six test methods; existing positive method
  may be renamed to avoid claiming a real model ran.
* Generated targets: none.
* Coverage: structural runtime contract/regression only, no semantic verification.
* Validation: installed-package unittest (red selector then full focused module),
  targeted Ruff lint/format, diff check; one full gate after Review and commit.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Red-first tests and bounded checker correction

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Add focused negative and runtime-shaped positive tests; record red

<!-- rpi:task id=P01-T02 -->
#### [x] P01-T02: Extend item guard/module docs; run focused green and targeted lint

<!-- rpi:phase id=P02 -->
### [ ] P02: One Review and clean candidate commit

<!-- rpi:task id=P02-T01 -->
#### [x] P02-T01: Reconcile plan/details/changes; perform one original RPI Review

<!-- rpi:task id=P02-T02 -->
#### [ ] P02-T02: Resolve GitHub identity; commit candidate and original evidence

<!-- rpi:phase id=P03 -->
### [ ] P03: Exact-head full gate and authorized delivery

<!-- rpi:task id=P03-T01 -->
#### [ ] P03-T01: Run one complete gate, fetch main and verify receipt

<!-- rpi:task id=P03-T02 -->
#### [ ] P03-T02: Push existing branch and update draft PR with evidence/blockers

## Dependencies

P01-T02 depends on recorded red P01-T01. P02-T01 follows implementation validation.
P02-T02 follows Review and resolved privacy identity. P03-T01 follows commit
and requires no unresolved in-scope blocking Review finding;
P03-T02 requires focused/full-gate success and valid receipt/current base.
If main moves or the gate fails, stop publication and report; no automatic rerun,
rebase, force push or protection change.

## Critique Disposition

One final-candidate critique executed; original Revise verdict retained.

| Finding | Owner/disposition | Resolving evidence |
| --- | --- | --- |
| PC-001 | Parent: rejected as inapplicable | No parent execution restriction forbids /tmp; caller explicitly requires new external gate output, and src/README.md uses /tmp. Worker-local restrictions do not govern parent execution. Dedicated external venv/probes already ran. No other session/worktree used. |
| PC-002 | Parent: applied | Dependencies and P02/P03 details now require no unresolved in-scope blocking Review finding before gate/publication. One Review and known excluded residuals preserved. |

No repeat critique; compatible correction applied before implementation.

## Implementation Context Record

Research Ready; checklist/details are finalized after critique. Changes record:
.copilot-tracking/changes/2026-10-23/issue-350-ai-item-shape-changes.md.
Review: .copilot-tracking/reviews/logs/2026-10-23/issue-350-ai-item-shape-review.md.
After commit, gate/receipt/delivery status is recorded externally and in PR, not
by altering committed artifacts and invalidating the exact-head receipt.

## Follow-Up Items

* None newly discovered; known coordinator/live acceptance boundaries are excluded.

## Handoff

P01/P02-T01 complete: 70 focused tests and targeted Ruff pass after genuine red;
one Review Complete / Residual work, no blocking in-scope defect. P02-T02/P03
remain pending at this committed snapshot. Next: parent privacy-safe commit,
one full gate/verifier and authorized normal push/PR update. Later completion
must be external to avoid invalidating the receipt; no source rework/re-Review.
