<!-- markdownlint-disable-file -->
---
title: Safety consent PR 509 rebase research
ms.date: 2026-10-29
---

# Task Research: safety-consent-130-rebase

## Research Brief

* Target: reconcile draft PR #509, `docs/safety-consent-130`, with current
  `origin/main`, retaining the bounded unverified referral/tenure implementation.
* Audience: coordinator preparing the next push and hosted CI.
* Scope: branch ancestry, actual conflicts, core/API integration and pinned fixtures.
* Non-goals: new operational authority, web design, Azure, issue acceptance, push.
* Criteria: clean rebase; preservation of both sides; existing lint/type checks
  and relevant tests; dated original evidence; independent critique and Review.
* Output mode: convergence. Posture: focused, selected for this bounded repair.
* Evidence root: `.copilot-tracking/`. No external research is needed.

## Research Parameters and Direction Controls

The caller explicitly authorizes fetch, rebase, conflict resolution and local
commits, requests every RPI phase, and reserves push to the coordinator.
Keep main's rubric files and scenario manifest, append-only entries from both
sides, source under `src/`, and tests outside packages. Use `/tmp/mv`; never
start full API discovery without the nonblocking heavy-lock check. No Azure
resource changes, private datasets or issue-closing keywords.

## Extension Registry and Participation

Repository instructions and component pyprojects/CI define layout and checks.
RPI phase skills govern evidence. Research stays inline because this is one
continuous ancestry/integration trace; separate research workers add no value.
The prior safety-consent artifacts are historical, not fresh approval.
No interaction is needed: the caller supplies the branch, base and resolution
policy and explicitly requests all four phases.

## Research Questions and Prior Knowledge Gate

1. Is this the active clean PR branch, and what conflicts with main?
2. Which checks exercise the retained intake, privacy and hold boundaries?
3. Does upstream pinning require a manifest refresh or another test?

Initial read-only inspection found a clean active topic branch and open draft
PR #509. Existing two commits remain the starting evidence, not proof of
compatibility with the newer main.

## Research Cycle Log

### Cycle 1: Wider

Inspected PR metadata, branch-only commits, changed-file inventory, current
component configuration and source CI. Main advanced through `356a3cfb`.
Reflection: the source delta is confined to core intake/projections/store plus
core/API tests and READMEs; upstream changes overlap store and both READMEs.

### Cycle 1: Deeper

Read the intake delta: strict staff evidence rights, append-only originals and
corrections, case-wide unresolved tenure hold, privacy filtering and independent
hazard route. Existing project configs define full-project Ruff and mypy.
Reflection: preserve the intake and newer store behavior together rather than
choosing one whole store implementation.

### Cycle 1: Contrarian

Challenged the assumption that old green CI proves current readiness. The PR's
historical rubric conclusion failed and score stayed pending; hosted checks at
the rebased unpublished head cannot be observed. Main changed both rubric
score and scenario manifest. Preserve main's copies and run manifest regression,
not an unreviewed digest refresh. A local rebase cannot establish remote
mergeability until the coordinator pushes.

## Evidence Log

| ID | Finding | Location | Confidence |
| --- | --- | --- | --- |
| C1 | Two topic commits implement bounded intake, not operational approval | `.copilot-tracking/reviews/logs/2026-10-27/safety-consent-130-131-review.md:1`; `git log origin/main..HEAD` | High |
| C2 | Source/test layout and local gate distinguish bounded checks from full publication evidence | `src/README.md:10`, `src/README.md:74` | High |
| C3 | Intake prevents implicit approval and filters private fields | `src/core/src/zava_forward/core/resident_decisions.py:103`, `src/core/src/zava_forward/core/projection.py:186`, `src/core/src/zava_forward/core/store.py:368` | High |
| C4 | Hosted jobs use project Ruff, format and mypy with sibling test imports | `.github/workflows/src-ci.yml:72` | High |
| C5 | Main changed store, both READMEs, rubric score and scenario manifest | `git diff --name-only $(git merge-base HEAD origin/main)..origin/main` | High |

No external sources used. No new legal/currentness claims.

## Findings, Alternatives and Parent Dispositions

* Accepted: rebase onto fetched main and resolve hunks compositionally (C1-C5).
* Rejected: whole-file topic preference for store/README; it could lose upstream
  behavior or documentation (C3, C5).
* Rejected: treating historical CI, skipped integrations or draft status as
  final approval (C1, C4).
* Deferred: hosted CI, complete local publication gate and human approval to
  the coordinator's publication boundary; do not claim these passed.

## Planning Readiness

Research disposition: executed. Planning Readiness: Ready.
Questions 1-3 are answered sufficiently to plan; exact conflict hunks will be
observed during the authorized rebase. No second research cycle is indicated:
the remaining uncertainty is execution, not a missing design decision.
Self-check: bounded scope, three ordered waves, evidence IDs, alternatives,
constraints and honest remote-validation limits are recorded.
