---
title: Issue 176 implementation review
description: Single offline RPI review with explicit residual acceptance gaps
ms.date: 2026-10-16
---

## Scope and Evidence

Task 176, synthetic-determinism-176. Full requested offline change boundary;
not original-stock or cloud application acceptance. One Review, inline.

* Research: .copilot-tracking/research/2026-10-16/synthetic-determinism-176-research.md
* Plan: .copilot-tracking/plans/2026-10-16/synthetic-determinism-176-plan.md
* Details: .copilot-tracking/details/2026-10-16/synthetic-determinism-176-phase-details.md
* Critique: .copilot-tracking/plans/2026-10-16/synthetic-determinism-176-critique.md
* Changes: .copilot-tracking/changes/2026-10-16/synthetic-determinism-176-changes.md
* Evidence: final source/test/docs diff and recorded targeted validation.

## Opening Review State

Goal: compare implementation, critique dispositions, validation and acceptance
claims. Source implementation P01 and P02-T01/T02 are complete; P02-T03
Review/publication remains in progress. All artifacts agree on that boundary.
Read-only source review; write only this review artifact. Existing original
stock and policy-approval gaps are known, not presumed resolved.
## Execution Status

Execution: Complete. Outcome: Residual work. No introduced correctness,
provenance, privacy or destructive-write defect found in the bounded diff.
This does not mean full issue acceptance.

## Plan-to-Change Reconciliation

| Scope | Evidence | Assessment |
| --- | --- | --- |
| P01-T01 | stock_fabric.py adds --as-of and reads/hash-parses the same raw buffers | Reconciled; all reads precede writes; strict invalid dates become explicit parser errors |
| P01-T02 | Existing repetition assertions plus two new methods in test_stock_fabric.py | Reconciled; no removals/new files, unchanged golden draws |
| P02-T01 | 45 passing tests, two-file Ruff/mypy and installed CLI smoke | Reconciled; local fictional inputs only |
| P02-T02 | Core/synthetic READMEs, reference index and appended log | Reconciled; AC1/AC2 gaps and policy approval boundaries explicit |
| P02-T03 | This single Review; commit/push/PR still pending | Review complete, publication is the remaining delivery operation |

## Completed Work Assessment

The optional date never reads a wall clock or changes generated row data.
Omission remains null, preserving existing commands. The register buffer is
decoded with utf-8-sig and StringIO newline="", matching the prior CSV stream
including quoted CRLF. Case UTF-8 JSON behavior remains consistent. Logical
input digest keys do not expose source paths or content; optional cases are
not assigned a fabricated hash. Source fingerprints necessarily change with
the implementation and continue to cover moved dependencies.

Seeded fabric algorithm, source case history, defaults, source version and
nonempty/output repository guard remain unchanged. Source buffers do use
additional memory proportional to input size; the existing CLI already
materializes all rows and source case JSON, so no new scale claim is made.
No generated snapshot, source evidence or private dataset is committed.

## Implementation-Time Updates and Critique Disposition

PC-001 accepted and satisfied: this record explicitly disposes all findings;
the missing original generator and unapproved policy are residual acceptance
gaps, not new implementation defects. No unresolved in-scope release blocker
was found. Publication must retain partial status.

PC-002 accepted and satisfied: BOM/quoted CRLF parser comparison, independent
raw register/case digest mutation, absent cases, read-once spies, date-only
payload equality, invalid date no-write and full snapshot refusal assertions
all pass within the two-method budget.

The test stream rename fixed a type-check failure before Review. Ruff
formatting changed only touched test additions. Inline Review instead of
delegation follows the bounded-context review rule, not a weakened evidence
gate. No material scope divergence or significant user decision was introduced.

## Findings

### RV-001 [Medium]: Original stock-register reproduction remains unavailable

* Evidence: synthetic-data README stock-register row and acceptance audit;
  research C6, tracked source inventory and absent generator path history.
* Impact: AC1 cannot pass for every generator; AC2 remains partial for the
  original generator receipt. Fictional 60,000-home construction does not
  recover original OSM anchors or their generator revision.
* Destination: distinct follow-up, rpi-research.
* Owner/next action: project owner supplies the original generator, pinned
  input snapshot and runtime; then test original-register replay offline.
* Disposition: disclosed, not fixed or substituted. Prevents full issue
  acceptance, not publication of this independently useful bounded change.

### RV-002 [Low]: Proposed refresh policy lacks recorded owner adoption

* Evidence: synthetic-data README explicitly labels refresh defaults proposed.
* Impact: AC3 is met as a documented cadence/approval/protection definition,
  but neither policy adoption nor a live refresh/reset is authorized.
* Destination: distinct follow-up, rpi-plan with named human decision.
* Owner/next action: Juan Manuel Servera approves or amends trigger cadence,
  snapshot/version rules and authority for each specific publication/reset.
  Legal, Compliance and DPO exercise capacity never implies resident consent,
  safety release or financial authority.
* Disposition: disclosed. No approval or issue checkbox was fabricated.

## Plan Follow-Up Assessment

Both existing plan follow-ups remain outside active source scope for evidenced
reasons. No new source work or deeper discovery is needed to populate a queue.
No second Review or current-task implementation loop is requested.

## Validation Evidence

| Check | Status | Evidence |
| --- | --- | --- |
| Four named core unittest modules with absolute core test PYTHONPATH | Passed | 45 tests, no skips, Python 3.12.3, 10.718 seconds |
| Scoped Ruff check and format check | Passed | Both changed Python files |
| Scoped strict mypy | Passed | No issues in two files |
| Installed CLI smoke | Passed | 30 fictional homes, identical complete snapshots, exact input digest, nonempty refresh refusal leaves bytes unchanged |
| Diff whitespace and newly added Markdown links | Passed | git diff --check; three new local links/anchors |
| Broad historical Markdown anchor scan | Failed, unrelated baseline | Old append-only log link to retired legacy documentation; left untouched, new-link scope passes |
| Private/original register replay | Unavailable | Source generator/pinned OSM inputs missing; no private datasets opened |
| Azure, real SQL/model, human policy approval | Not run | Offline task; no authority inferred |

## Outcome and Closeout Routing

Outcome: Residual work, not Conformant for all of #176. The source improvement
has passing scoped evidence and no identified introduced defect; RV-001/002
must remain visible in the PR. Implementation defects: none. Material evidence
gap routes to rpi-research once original source is supplied; policy decision
routes to a separate owner-approved rpi-plan follow-up. No new work starts
without that direction.

Remaining delivery operation: normal commit/push and Refs #176 PR, no merge,
no issue-body changes. Review execution is complete and is not repeated when
delivery metadata is recorded.
