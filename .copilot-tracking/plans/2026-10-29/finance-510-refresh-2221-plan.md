<!-- markdownlint-disable-file -->
---
title: Finance 510 current-main refresh plan
description: Rebase, preservation proofs, focused validation and local-only delivery
ms.date: 2026-10-29
---

Task ID / slug: `finance-510-refresh-2221`.

## Executive Summary

Replay the current finance topic on immutable fetched main
`129808b3d0a2a5ab88bdcf631d2722362de9e857`, retaining the remote bot commit
before applying main's authoritative rubric. Resolve additive documentation
and store integration without feature redesign. Validate all core/API static
checks and relevant finance/resident/scenario regression selectors. Complete
one independent Review, commit the original dated evidence, and hand off
without pushing. Hosted CI and financial/human acceptance are separate gates.
Closeout amendment: main moved after the one Review to
`719e76e50b9f54b71514ee7b90833005f9bb4be8`. Replay onto that refreshed main,
retain original Review's prior assessed boundary, revalidate unchanged Python
integration, and route fresh exact-head publication assessment to coordinator.

## User Decisions and Requirements

* Full dated Research, Plan, Implement, Review loop; references #510/#96 only.
* Fetch/rebase origin/main; preserve both sides, append-only log and index.
* Main's `.github/rubric/*` and scenario manifest are authoritative.
* Source only in `src/`; tests outside packages; no legacy application code.
* `/tmp/mv`, explicit source/test PYTHONPATH, core/API Ruff/format/mypy and
  relevant tests. No full API discovery without nonblocking heavy admission.
* No Azure resource changes or push. Conventional Commit and Copilot trailer.
* Actual commands/results belong in the changes artifact.

## Goals

G1: locally mergeable, main-descended finance branch with retained intent.
G2: reproducible relevant local CI evidence and truthful remaining boundaries.

## Scope and Non-Goals

Scope: upstream synchronization, actual conflict resolutions, regression checks
and dated evidence. No financial redesign, issue/PR mutation, remote publication,
approval invention, source formatting sweep or removal of historical evidence.

## Functional Requirements

FR1: Fast-forward the single known upstream score commit, then rebase main.
FR2: Preserve nonoverlapping finance and safety store/docs changes, all original
RPI records, full main log prefix and all index entries. Protected files equal main.
FR3: Check actual module origins, manifest pins, dependency layout and conflict
markers. New inherited source must not be erased by blanket old-tree restoration.
FR4: Record failures, fixes and skips, including any hosted/publication blocker.

## Non-Functional Requirements

NFR1: no secrets/private fixtures/cloud actions; no shared venv mutation unless
a required dependency actually fails missing.
NFR2: use no-cache tools and transient synthetic fixtures; retain current tests.
NFR3: obtain one fresh critique and one separate independent final Review.
NFR4: preserve original evidence and use explicit staging/local noreply identity.

## Acceptance Criteria

AC1: fetched main is ancestor; no unmerged paths or unresolved conflict markers.
AC2: main protected files match; both sides' doc/store intent and evidence survive.
AC3: complete core/API Ruff, format and mypy pass in existing `/tmp/mv`.
AC4: relevant finance, source-freshness, dependency, scenario and inherited
resident-decision/API checks pass with explicit current-worktree imports.
AC5: full API only under actual `flock -n` ownership; busy means blocked, not pass.
AC6: independent critique/Review persisted, local attributed commit, clean final
tree, no push. Hosted CI remains unverified until coordinator publishes.
Material integration or validation findings in the single Review prevent a
ready/accepted handoff; preserve its adverse outcome and route owned follow-up.

## Validation and Test Ownership Lock

Canonical source: owning `src/*/src/zava_forward/*`; tests: owning external
`src/*/tests`. No generated code targets. Test removals: none. Planned additions:
zero; only a demonstrated rebase-caused defect can justify a bounded regression.
Semantic checks: source preservation, main ancestry, docs additive retention,
protected-file hashes, import origins, pinned sources. Regression checks:
existing finance/resident/scenario/dependency tests. No assertion weakening.

## Phase Checklist

<!-- P01 -->
### P01: Integrate fetched main

* [x] P01-T01: fast-forward remote bot commit and rebase immutable main.
* [x] P01-T02: resolve actual conflicts and prove both sides/protected preservation.

<!-- P02 -->
### P02: Validate and deliver locally

* [x] P02-T01: static checks and relevant core/API regression selectors.
* [ ] P02-T02: one independent Review, final evidence reconciliation, local commit.

## Dependencies and Risks

P01-T02 depends on P01-T01; P02-T01 depends on P01; P02-T02 depends on P02-T01.
Shared heavy lock was free at research probe but must be reacquired and held
for API discovery or complete gate. `/tmp/mv` editables point at another worktree;
explicit paths and import assertions prevent testing it by accident.
Hosted Source CI on remote `011f6a6e` is `action_required`, not passing.
No push is authorized to generate fresh hosted evidence.

## Critique Disposition

Execution Complete; original verdict Revise, Medium 2. Original preserved.
PC-001 adopted: material Review findings block ready/accepted handoff; route
findings without repeating or rewriting Review.
PC-002 adopted as fixture hygiene: set project-local TMPDIR and assert its
resolved root. No broader prohibition on external scratch storage is inferred.
Both are direct compatible corrections; no outstanding critique finding.
Planning Readiness: Ready.
Critique output:
`.copilot-tracking/reviews/plans/2026-10-29/finance-510-refresh-2221-plan-critique.md`.

## Follow-Up Items

* Coordinator publication with exact-head/current-main gate and fresh hosted CI.
  Main moved after the single Review; its original prior-base outcome is not
  final exact-head approval. Coordinator owns that assessment.
* Existing Finance/Board inputs and whole-issue acceptance remain outside scope.

## Sources and Handoff

Research: `.copilot-tracking/research/2026-10-29/finance-510-refresh-2221-research.md`,
C1-C8. Details:
`.copilot-tracking/details/2026-10-29/finance-510-refresh-2221-phase-details.md`.
Changes target:
`.copilot-tracking/changes/2026-10-29/finance-510-refresh-2221-changes.md`.
Parent proceeds after critique disposition; no routine approval needed.
