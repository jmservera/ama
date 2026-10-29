---
title: Safety consent PR 509 rebase plan
ms.date: 2026-10-29
---

Task ID: pr-509-rebase-2026-10-29. Status: complete for local unpublished handoff.

## Executive Summary

Rebase the existing draft onto fetched main, resolve actual conflicts without
losing either implementation, then run component checks and focused regressions.
Commit the local candidate and original dated RPI evidence; never push.
Hosted CI and final publication approval remain coordinator responsibilities.

## Sources

`.copilot-tracking/research/2026-10-29/safety-consent-130-rebase-research.md`,
evidence C1-C5, existing core/API pyprojects and source CI.

## User Decisions and Requirements

* Update draft #509 on its current branch; Refs #130; no issue-closing keywords.
* Fetch and rebase main, explicitly preserving both sides of real conflicts.
* Take main's `.github/rubric/*` and scenario manifest, retaining append-only
  log and README index entries on both sides.
* Source remains in `src/`; tests stay outside packages; no legacy code.
* Use `/tmp/mv` Ruff, formatting, core/API mypy and relevant unittests with
  sibling source/test imports. Full API discovery requires the nonblocking
  `/tmp/ama-rpi-heavy.lock` check.
* No Azure resource changes. Conventional Commit and required Copilot trailer.
* Do not push. Record all execution commands and results in changes evidence.
* Execute all four RPI phases, including independent critique and Review.

## Goals

Preserve the intake contract and newer main functionality with a clean,
main-descendant candidate and reproducible local evidence.

## Scope and Non-Goals

Only rebase integration and tightly coupled test/CI repair. No web changes,
new business authority, original-evidence rewrites, Azure or remote writes.

## Functional Requirements

Retain original referral evidence, correction history, explicit staff rights,
unresolved tenure holds and independent hazard handling. Keep newer main
store behavior and documentation. Main's controlled rubric/manifest copies
must remain byte-identical.

## Non-Functional Requirements

Use the existing project check configurations and test owners. No check renames,
weakened assertions, synthetic approvals, secret/private data reads or skips
misrepresented as passes. Authenticate privacy-safe author/committer identity.

## Acceptance Criteria

1. Rebase finishes; `origin/main` is an ancestor; no conflict markers remain.
2. Both sides' README and runtime intent survive; controlled paths equal main.
3. Full-project core/API Ruff and format checks and mypy pass; relevant resident,
   hazard, consultation, procurement, dependency and manifest tests pass.
4. Dated research/plan/details/critique/changes/Review/state are retained, and
   the clean local candidate has a Conventional Commit plus required trailer.
5. Any unexecuted CI/full-publication/human gates are explicitly identified,
   with no push or Azure modification.
6. Material in-scope Review defects or failed required checks block a ready
   handoff. Evidence may still be committed, but must be labelled blocked and
   returned to the coordinator without claiming acceptance or repeating Review.

## Phase Checklist

<!-- P01 -->
### P01: Rebase integration

* [x] P01-T01: Execute rebase, inspect each conflict, compose resolutions and continue.
* [x] P01-T02: Verify controlled files, ancestry, original evidence and path ownership.

<!-- P02 -->
### P02: Validation and bounded repair

* [x] P02-T01: Run project Ruff/format/mypy and focused component unittest selectors.
* [x] P02-T02: Run scenario manifest and dependency regressions; repair only coupled failures.

<!-- P03 -->
### P03: Independent Review and local handoff

* [x] P03-T01: Record commands/results and reconcile plan/details/changes evidence.
* [x] P03-T02: Execute one independent Review and route residual work.
* [x] P03-T03: Commit implementation/evidence with authenticated identity; verify clean
  main-descendant head and leave push to coordinator.

## Locked Test Ownership and Coverage

Canonical owners: `src/core/tests` for domain/store, `src/api/tests` for HTTP.
Removals: none. Maximum additions: two tightly coupled regression methods if
a conflict-resolution bug is exposed; otherwise none. No generated targets
will be authored; controlled scenario manifest remains main's version.
Semantic coverage: intake privacy, hold persistence and source identity.
Regression coverage: existing resident, hazard, consultation and procurement
modules, dependency rule and `test_scenario_manifest`.
Main-side store coverage: `src/api/tests/test_ai_tasks.py`, module
`test_ai_tasks`, explicitly covers denied roles, programme/assigned selection,
projected status minimisation and entitlement-sensitive cache keys.
Full API discovery is optional, not needed when focused coverage passes; if
selected, both the caller's `flock -n ... true` probe and a held nonblocking lock
must succeed. Do not disturb another worker or mutate its shared environment.

## Critique Disposition

Exactly one independent critique: execution Complete, original verdict Revise,
at `.copilot-tracking/reviews/plans/2026-10-29/safety-consent-130-rebase-plan-critique.md`.

* PC-001 (Medium): applied directly. Add existing `test_ai_tasks` module to
  P02-T01; briefing authorization/scope/minimisation/cache tests are present in
  fetched main. No additional test methods are needed.
* PC-002 (High): applied directly. Acceptance 6 and P03 details distinguish
  blocking integration findings from excluded human/operational residuals.
  An adverse original Review is preserved, not repeated or upgraded.

Neither finding requires a new user decision; no second critique will run.

## Follow-Up Items

Hosted CI, final publication gate and formal human acceptance are outside this
local unpublished integration task. Historical operational blockers remain.
RV-001 (Low): coordinator establishes current-base/final-head publication
evidence, any required complete gate/receipt and hosted CI before owner merge.
RV-002 (Medium): original named human resident/tenure/privacy decisions remain
unaccepted; no operational activation or issue closure follows this rebase.

## Handoff

Details: `.copilot-tracking/details/2026-10-29/safety-consent-130-rebase-phase-details.md`.
Changes: `.copilot-tracking/changes/2026-10-29/safety-consent-130-rebase-changes.md`.
No unresolved implementation decision is currently identified.
One independent Review executed Complete / Residual work at `edfed594`;
no local integration blockers. Final evidence-only reconciliation is not a
second Review or an assessment/receipt for a later publication head.
