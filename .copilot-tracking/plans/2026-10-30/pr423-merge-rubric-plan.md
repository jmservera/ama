<!-- markdownlint-disable-file -->
# RPI Plan: PR423 merge and rubric diagnosis

## Task Metadata

* Task ID: pr423-merge-rubric-2026-10-30
* Task slug: pr423-merge-rubric
* Plan date: 2026-10-30
* Planning status: Ready; original critique Revise, compatible findings resolved
* Phase details: .copilot-tracking/details/2026-10-30/pr423-merge-rubric-phase-details.md
* Critique: .copilot-tracking/reviews/plans/2026-10-30/pr423-merge-rubric-plan-critique.md

## Executive Summary

Merge current main without rewriting either history, preserve the offline
private Blob transport and DN1-DN5, and retain main's current src, IoT and
release work. Resolve four conflicts explicitly and recompute the combined
CI workflow fingerprint. Add exact malformed-D1 regressions and concise,
traceable transport evidence without changing the scoring contract.

### What You May Not Know

The failed run did not record a low score: D1 had an extra `evidence2` field.
A diagnostic replay removing only that field gives 77 versus 77, not a new
assessment. The existing preflight already prohibits it. Only A1/A3/A5 were
open, already at 5; rehearsal, publication and live transport cannot be
invented to raise the total.

### Unresolved Decisions or Blockers

No implementation decision outstanding. The full local gate was attempted
after the merge/evidence commit but the shared heavy-resource lock timed out
after 600 seconds. Publication remains blocked; no successful receipt exists.
Requested local implementation and one-pass RPI evidence are complete.

## User Decisions and Requirements

* Full research, plan, implement, review in that order, with dated evidence.
* Use this existing fix branch only; do not touch any other worktree.
* Merge/rebase main preserving both sides; keep append-only entries and DN1-DN4.
* Investigate rubric workflow, scorer and capstone definitions; implement only
  honest in-scope improvements and record cause, changes and remaining work.
* No Azure, deploys, secrets, live sign-in, warming or push.
* Commit locally with Copilot coauthor trailer and `Refs #360`, no closing keyword.

## Goals

* An integration candidate containing both original head and fetched main.
* A reproducible distinction between invalid submission and numerical score.
* Navigable implementation evidence and preservation of historical limitations.

## Scope and Non-Goals

In scope: four textual conflicts; semantic auto-merge checks; exact D1
regressions; infra runbook/evidence pack, rubric incident documentation and
KB index/log; relevant existing local tests and full gate attempt.

Non-goals: changing grades, floors, registry, workflow permissions or generated
lock; modifying thought-leadership/pitch artifacts to imply missing delivery;
live activity, publishing, issue closure and unrelated main fixes.

## Functional Requirements

* Keep private Blob codec/controller/worker/RBAC/image/test changes while
  retaining main's current infrastructure and namespace contracts.
* Reject exact D1 extra-key input at adapter and existing jq preflight.
* Explain evidence, rationale and change_reason separately; document what
  actually ran and what did not.

## Non-Functional Requirements

* No removed tests, original RPI evidence or historical log entries.
* No score/default coercion, broad permission fallback or restored mvp path.
* Derived workflow hashes must match actual combined files byte for byte.
* Validation is local/synthetic; unavailable integration evidence stays blocked.

## Acceptance Criteria

* AC1: origin/main 5634f9a0 and original head 46968668 are ancestors of final
  HEAD, no unresolved conflicts, and all four resolution decisions recorded.
* AC2: DN1-DN5 and both histories' docs/tests preserved; current worker imports
  installed src namespace and image includes staff_blob. A two-parent ledger
  accounts for differing paths, source/test/function/assertion losses, original
  RPI evidence and both appended log sequences; ancestry alone is insufficient.
* AC3: exact extra evidence2 regression and valid-shape control pass at both
  adapter and prompt preflight; scoring files and thresholds unchanged.
* AC4: changes artifact distinguishes no-score failure, 77 counterfactual,
  actual baseline and remaining live/panel/publication gaps.
* AC5: relevant existing tests executed, full local gate attempted after
  committing original Review evidence, adverse results retained externally.
  Success is not claimed when checks fail or are blocked.
* AC6: local commits have privacy-safe author/committer and required trailer;
  no push or cloud operation performed.

## Sources

* .copilot-tracking/research/2026-10-30/pr423-merge-rubric-research.md:
  C1-C10 and W1-W2 provide integration and schema evidence.
* src/README.md: full local RPI gate and exact-head receipt boundary.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Preserve integration and improve evidence

Dependencies: complete research and one critique.

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Merge and reconcile conflicts

Merge origin/main with no automatic commit. Keep latest metadata plus both
index bodies, concatenate both append-only log sides, recompute src-ci hash.
Inspect semantic auto-merges, including IoT role matrix and Blob writer.

<!-- rpi:task id=P01-T02 -->
#### [x] P01-T02: Add exact regression and honest evidence navigation

Depends on P01-T01. Update existing adapter/preflight tests and transport/
rubric docs, KB index/log. Retain all original statements as dated history.

<!-- rpi:phase id=P02 -->
### [x] P02: Validate and deliver local candidate

Depends on P01.

<!-- rpi:task id=P02-T01 -->
#### [x] P02-T01: Run targeted local validation

Run infra tests with offline Bicep required, rubric adapter/gate/prepare and
record-workflow tests, gate orchestration tests and migration regressions.
Run corresponding lint/type/workflow checks.

<!-- rpi:task id=P02-T02 -->
#### [x] P02-T02: Reconcile evidence, Review once, commit and attempt full gate

Depends on P02-T01. Original Review is independent, read-only and once only.
Classify findings as acceptance-blocking or deferrable; preserve the original
outcome. Unresolved acceptance violations mean Not accepted/Blocked handoff,
not successful completion. Route findings to later work rather than repeat
Review or restart implementation in this one-pass task. Commit
candidate and original evidence; run full gate externally and verify only
a successful exact-head receipt. Leave push to coordinator.

## Test Ownership and Change Budget

* Canonical test target: .github/rubric/scripts/test_scorecard_adapter.py.
* Exact removals: none. Maximum additions: two D1 `evidence2` rejection
  parameter cases (adapter and jq), using existing valid-card controls.
* Semantic integration covered by existing infra/namespace/matrix suites;
  regression coverage does not claim model compliance or live behavior.
* Generated target: none. No prompt or lock edit planned; existing preflight
  already rejects the observed defect. No saved scorecard is repaired/published.
* Full gate owns isolated dependency installs and disposable local resources;
  it may not access Azure or private datasets.

## Dependencies

* Fetch of main completed; reviewed main pinned at 5634f9a0.
* Repository-local privacy-safe identity resolved using `gh api user`.
* Local dependencies/tools may need restoration only after missing failures.

## Critique Disposition

One critique executed, original verdict Revise, preserved unchanged.

| Finding | Disposition | Resolving evidence |
| --- | --- | --- |
| PC-001 | Applied | AC2 and phase details now require two-parent content/test/evidence/log/DN preservation ledger and semantic selectors |
| PC-002 | Rejected, unsupported premise | Critic asserts a runtime prohibition on /tmp operations which is not present in the parent's active instructions. A fixed local serialization lock is not prohibited here. Preserve normal full gate and never touch other worktrees; record actual prerequisites/failures |
| PC-003 | Applied with lifecycle constraint | Distinguish blocking findings from deferrable risks. Preserve original Review; unresolved blockers prevent acceptance and route to later work, without a second Review or in-task implementation loop |

## Follow-Up Items

* Coordinator must obtain the shared local heavy-resource lock and run a new
  full exact-head gate before publication. The actual 600-second lock timeout
  is preserved; no lock was removed, bypassed or another worktree touched.
* Rubric/test maintainers should repair the eight independently reproduced
  inherited fixture/registry failures separately, without relaxing scoring.
* Fresh hosted rubric submission after coordinator push; local checks cannot
  establish hosted output compliance or replace exact-head assessment.
* Real private transport, production action-name/size verification, signed
  attestation and actual pitch/dissemination evidence require separate authority.

## Handoff

Implementation changes record:
.copilot-tracking/changes/2026-10-30/pr423-merge-rubric-changes.md.
All P01/P02 execution tasks are complete, including the failed full-gate
attempt; this is not full-gate acceptance. Original Review remains Complete /
Residual work. Coordinator owns the blocked final exact-head publication gate.
