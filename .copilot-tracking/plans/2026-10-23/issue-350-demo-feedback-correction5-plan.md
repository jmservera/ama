---
title: Issue 350 feedback checker correction 5 plan
description: Reject float overflow and require an integer schema version
ms.date: 2026-10-23
---

## Task Metadata

Task ID/slug: issue-350-demo-feedback-correction5.
Planning status: local correction and one Review complete; atomic local commit
handoff. Publication checks remain coordinator-owned.
All paths use this slug and date 2026-10-23.

## Executive Summary

Reject JSON exponent overflow before evidence checks using a typed finite-float
decoder callback. Require schema_version's exact type to be int before value
comparison. Add red-first regressions and finite-float controls. Preserve every
offline acceptance limit and retain earlier RPI evidence unchanged.
Implemented and locally validated: 77 tests and targeted quality checks pass.
One local Review executed Complete, outcome Conformant within this boundary.
No in-scope findings; no publication or broader acceptance is inferred.

### What You May Not Know

JSON 1.0 equals integer 1 in Python too; the exact-type requirement rejects it
as well as true. False already blocks, but remains explicitly tested.
Earlier plan's pending gate/publication markers predate the owner-supplied
passing receipt and are not rewritten. This correction invalidates reuse of
that receipt for the new head. No scope change or new full gate here.

## Sources

* Research: .copilot-tracking/research/2026-10-23/issue-350-demo-feedback-correction5-research.md, C1-C5.
* Details: .copilot-tracking/details/2026-10-23/issue-350-demo-feedback-correction5-phase-details.md.
* Critique: .copilot-tracking/reviews/plans/2026-10-23/issue-350-demo-feedback-correction5-plan-critique.md.
* Changes: .copilot-tracking/changes/2026-10-23/issue-350-demo-feedback-correction5-changes.md.
* Prior correction4 plan/details/Review read; original adverse outcomes retained.

## User Decisions and Requirements

* Execute one ordered full RPI loop for the two independent P2 findings.
* Only this worktree and existing branch; minimal typed checker/tests edits and
  dated correction artifacts. Preserve prior evidence and unrelated markers.
* Red-first focused tests, then green, Ruff lint/format and whitespace checks.
* No SQL durability, deployed acceptance, actual inference or whole-issue
  acceptance claims; original criteria remain untouched and issue open.
* Commit locally after resolving privacy-safe identity using gh api user and
  repository-local configuration; no push/amend/merge/PR or issue edits.
* Stop after local source checks and RPI review. Coordinator owns full gate,
  new receipt verification and independent assessment before publication.

## Goals

Eliminate non-finite JSON numeric evidence and bool-as-version false positives
at the input boundary without adding component field-content rules.

## Scope and Non-Goals

Canonical code targets: tools/check-demo-feedback.py and
tools/test_check_demo_feedback.py. Generated targets/removals: none.
Only correction5 tracking files may otherwise change. No dependency/schema/
runtime/web/tooling changes. No full gate, remote write or delivery acceptance.

## Functional Requirements

* FR1: every non-finite float produced by a JSON number is rejected with an
  explicit invalid-JSON BLOCKED reason before component checks.
* FR2: schema_version requires exact int and supported value; bool, float and
  unsupported values block with a schema diagnostic.
* FR3: finite floats retain scope-dependent behavior: unchecked rank remains
  accepted, nonnegative latency accepted, negative latency fails. Numeric
  strings are not treated as JSON numbers by the decoder.
* FR4: preserve synthetic case-write BLOCKED, gaps NOT-RUN, overall BLOCKED
  for otherwise valid fixtures, offline_only true and acceptance not-accepted.

## Non-Functional Requirements

Typed parse_float callback `(value: str) -> float`, math.isfinite, ValueError
and existing specific handling only. No recursive schema framework, coercion,
Decimal, broad catch, dependencies or unrelated cleanup.

## Acceptance Criteria

* Red-first raw JSON 1e999/-1e999/decimal overflow tokens block globally in
  latency, nested unchecked rank and another unchecked nested location.
  Error reason identifies invalid JSON/non-finite value, not only aggregate
  BLOCKED from the pre-existing SQL cap.
* Normal finite floats (fraction, large finite exponent, finite underflow) pass
  the loader and preserve component-specific verdicts.
* True/False/1.0 plus unsupported integer 2 block explicitly for schema version;
  integer 1 retains passing component checks and all offline caps.
* Entire focused module green, isolated cache-free Ruff lint and format green,
  git diff --check clean; no hidden ignored inputs introduced.
* One preimplementation critique and one postimplementation RPI Review are
  recorded separately; coordinator's independent exact-head review is later.
  Local completion requires no unresolved in-scope acceptance finding;
  otherwise preserve the Review and mark this handoff blocked, not complete.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Red-first regressions and minimal correction

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Add raw JSON regressions and finite/type controls; run red

<!-- rpi:task id=P01-T02 -->
#### [x] P01-T02: Add finite float decoder and exact integer schema guard

<!-- rpi:phase id=P02 -->
### [x] P02: Local validation and evidence

<!-- rpi:task id=P02-T01 -->
#### [x] P02-T01: Run green focused suite, Ruff lint/format and whitespace checks

<!-- rpi:phase id=P03 -->
### [x] P03: Review and local handoff

<!-- rpi:task id=P03-T01 -->
#### [x] P03-T01: Execute one RPI Review and route publication prerequisites

<!-- rpi:task id=P03-T02 -->
#### [x] P03-T02: Resolve privacy-safe identity and commit locally; stop

Privacy-safe identity resolved from gh api user and repository-local email
configured. This final marker/state is included atomically in the local commit;
the containing commit object, not this preparatory text, is the evidence that
the commit executed. If commit fails, local handoff is incomplete. No gate or
publication is authorized by this marker.

## Test Ownership and Validation Lock

Primary implementer owns the existing test module; no deletions or replacement.
Maximum additions: five test methods, with subtests. Regression coverage:
raw overflow and schema booleans. Semantic controls: finite floats in checked
and unchecked fields, exact schema integer, unchanged offline caps.
Use raw numeric-token replacement with an exact expected replacement count;
never serialize float("inf") as a proxy for exponent overflow.
Assert all CHECKS BLOCKED and no runtime loader invocation on invalid input.
Use `PYTHONDONTWRITEBYTECODE=1 /tmp/fh350-venv/bin/python -B -m unittest
tools.test_check_demo_feedback -q`; red selects only new InputSafety methods.
Ruff 0.17.1: `check --isolated --no-cache --select E,F,W,B,BLE,I --ignore E501`
and `format --isolated --no-cache --check` on both tools.
Use git diff --check and status including ignored inputs. No dependency
installation unless missing-dependency failure. Keep transient logs in the
session workspace outside the worktree and record actual counts in artifacts.

## Critique Disposition

One independent preimplementation critique executed Complete, verdict Revise.
Original artifact retained with both findings:

* PC-001, applied directly: local completion depends on no unresolved in-scope
  acceptance findings. Route out-of-scope residuals only; an unresolved in-scope
  finding blocks completion without re-running this task's Review.
* PC-002, rejected: the worker cites an execution-local prohibition on /tmp and
  /var/tmp absent from this primary's instructions. Do not impose that worker
  restriction or change established tempfile helpers. Code and evidence edits
  stay in this worktree; test-owned transient tempfiles use existing behavior;
  session logs stay external and no other worktree is modified.

No extra planner assignment: this compact candidate is primary-authored;
the independent critique owns the required planning challenge.

## Follow-Up Items

* Coordinator: fresh full gate and receipt for the new exact head, then
  independent exact-head assessment before publication. Outside local scope.

## Handoff

P01/P02 complete: 77 focused tests pass, Ruff lint/format and whitespace pass.
P03 local Review Complete, bounded outcome Conformant, no in-scope findings.
Authenticated privacy-safe identity configured; commit these final artifacts
and correction atomically, then stop. Coordinator owns follow-up items and
the exact final commit identity. No earlier plan markers or outcomes changed.
Historical plan markers are preserved; update only correction5 markers.
