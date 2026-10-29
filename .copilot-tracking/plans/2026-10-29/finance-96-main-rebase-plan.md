<!-- markdownlint-disable-file -->
# RPI Plan: finance-96-main-rebase

Task ID / slug: finance-96-main-rebase. Date: 2026-10-29.

## Executive Summary

Replay the two finance commits onto fetched main, resolving additive conflicts
without losing current-main behavior or original finance evidence. Validate
the combined local source with project-wide lint/types and relevant synthetic
regressions; independently review once, commit and leave unpushed.
Fresh hosted CI and remote mergeability remain coordinator-owned after push.

## Sources

.copilot-tracking/research/2026-10-29/finance-96-main-rebase-research.md
(C1-C6, W1-W2); PR #510; caller requirements 2026-10-29.

## User Decisions and Requirements

* Run all four RPI phases and preserve dated evidence.
* Fetch and rebase docs/finance-96 on origin/main; preserve both conflict intents.
* Keep both append-only log and index entries; main owns rubric and manifest.
* Source in src/ only; tests outside package directories; no legacy code.
* Use /tmp/mv; local/sibling src and tests paths must win over editable installs.
* Run Ruff check/format, applicable core/API mypy and relevant unittest modules.
* Full API discovery requires successful flock -n /tmp/ama-rpi-heavy.lock true.
* No Azure/resource changes; commit conventionally with Copilot trailer.
* Refs only; no push, remote mutation or issue acceptance claim.

## Goals

Remove local ancestry conflicts and catch regressions caused by integration.

## Scope and Non-Goals

Existing draft PR integration only. Preserve original RV-001/002 findings,
not financial-feature acceptance, new financial authority, UI redesign,
workflow bypass, remote scoring, deployment or remote publication.

## Functional Requirements

Retain finance endpoint/projection/private-state intent with current-main
routes and private keys. Retain all additive docs and typing overrides.
Take main rubric and scenario manifest verbatim; rerun pinned-source tests.

## Non-Functional Requirements

Explicit import provenance, no shared venv mutation unless missing dependency
requires it, no test skips invented, clean final commit and no push.

## Acceptance Criteria

* Fetched main is an ancestor of local HEAD; no unresolved conflict markers.
* Main's rubric/manifest copies are unchanged in the combined candidate.
* Original finance changes/critique/Review remain byte-preserved.
* Required local checks pass or exact blockers are recorded without false CI
  success claims. Full project lint and mypy, focused core/API regressions.
* One critique and one independent post-implementation Review are retained.
* Changes artifact records commands, outcomes, skips and validation limits.
* Commit contains requested trailer and privacy-safe author/committer.
* No push, Azure operations or alteration of remote PR/issue state.

## Phase Checklist

<!-- P01 -->
### P01: Rebase and preserve integration

* [x] P01-T01: Rebase onto origin/main and resolve actual conflicts.
* [x] P01-T02: Verify additive semantics, protected files and historical evidence.

<!-- P02 -->
### P02: Validate and prepare local handoff

* [x] P02-T01: Run project lint/types and relevant unittest regressions.
* [x] P02-T02: Reconcile evidence; commit implementation and original RPI evidence.

## Test Ownership and Coverage Lock

Canonical tests: existing src/core/tests and src/api/tests. Removals: none.
Maximum additions: no new test files; at most two regression methods only if a
specific integration defect cannot be covered by existing selectors.
No generated tests. Existing manifest test is canonical hash-binding proof.
Focused selectors: core form_review, form_staging, finance_match_controls,
finance_signoffs, grant_lifecycle_controls, change_provenance, document_rescan,
scenario_manifest and dependency_rule; API form_staging_api, finance_match_api,
role_endpoint_inventory and dependency_rule. Tests from all siblings remain
outside packages. Full API discovery is optional, not needed when focused
checks cover this integration; if selected, hold the heavy lock throughout.

## Critique Disposition

Execution Complete; verdict Pass, zero findings, by independent
finance-rebase-critique worker. No second critique. No dispositions required.

## Follow-Up Items

Coordinator pushes and observes fresh hosted CI, including externally
controlled rubric AIC budget. Original finance RV-001/002 and missing actual
Finance/Board approvals remain distinct existing work, not new rebase tasks.

## Handoff

Details: .copilot-tracking/details/2026-10-29/finance-96-main-rebase-phase-details.md.
Critique: .copilot-tracking/reviews/plans/2026-10-29/finance-96-main-rebase-plan-critique.md.
Changes: .copilot-tracking/changes/2026-10-29/finance-96-main-rebase-changes.md.
Readiness: implementation complete; local evidence committed as 50c5c4b6.
Ready for the single independent integration Review, not publication approval.
