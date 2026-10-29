<!-- markdownlint-disable-file -->
# RPI Plan: Refresh IoT PR #508

## Task Metadata

* Task ID: pr-508-refresh-2026-10-29
* Task slug: iot-consumer-110-refresh
* Plan date: 2026-10-29
* Planning status: Ready; single critique completed and all findings disposed
* Phase details: .copilot-tracking/details/2026-10-29/iot-consumer-110-refresh-phase-details.md
* Plan critique: .copilot-tracking/reviews/plans/2026-10-29/iot-consumer-110-refresh-plan-critique.md

## Executive Summary

Rebase the existing draft onto current main, retaining bounded IoT source and current-main model/UX contracts. Validate the integrated core/API packages and manifest, preserve original evidence, then perform one independent Review and commit locally. Coordinator owns publication; no hosted green result or mergeability is claimed before that.

### What You May Not Know

Historical rubric failure includes a missing verdict and HTTP 403 while commenting, not a failing source unit test. Main's model version/noise bounds and manifest pins changed; old passing counts are not current compatibility evidence. Static inspection proves the complete gate invokes az bicep outside this task's cost-lookup-only permission, so the complete gate/receipt and exact-head publication assessment are deferred, not passed.

## User Decisions and Requirements

* Run the full dated Research, Plan, Implement, Review loop for PR #508; Refs #110 #184 #185 #187 #188 #189.
* Fetch and rebase origin/main; preserve both sides, with main owning .github/rubric/* and scenario manifest, recomputing hashes only when needed.
* Source in src/ only; tests outside installed packages; no legacy application code.
* Use /tmp/mv for Ruff lint/format, applicable core/API mypy and relevant unittests with sibling source/test paths. Full API only after successful nonblocking heavy-lock admission.
* No Azure resource changes or paid Hub. Read-only estimate only in PR notes.
* Conventional Commit with required Copilot co-author trailer. Do not push.

## Goals

* Produce a conflict-free descendant of fetched main without losing topic safeguards or main behavior.
* Provide exact command/results and honest remaining-gate evidence.

## Scope and Non-Goals

In scope: four topic commits, conflicts, coupled source/dependency compatibility, manifest pins, local checks and dated RPI records.

Non-goals: new features, visual redesign, CI permission/protection changes, deployment, paid services, issue closure, push, merge, or replacing earlier review outcomes.

## Functional Requirements

* Retain finite opt-in receive/publish behavior, provenance, admission/cleanup safety and synthetic-only replay.
* Preserve main model/version changes, updated UI files and typing overrides.
* Preserve main's rubric bytes and scenario contract, except strictly required source-digest refresh.

## Non-Functional Requirements

* Ruff, formatting, strict configured mypy, relevant unit modules and manifest validation exit zero.
* No private working datasets or cloud credentials used in tests.
* Full API suite holds the heavy lock throughout; unavailable admission means focused tests only and explicit evidence.
* Keep original RPI evidence and source/test locations unchanged.

## Acceptance Criteria

* origin/main is an ancestor; no conflict markers; changed source is under src/ and no packaged tests introduced.
* Current manifest validates pinned bytes; rubric tree matches origin/main.
* Affected lint/format/types/units pass, or concrete blockers are recorded without a green claim.
* Exactly one final-plan critique and one post-implementation independent Review exist.
* Changes artifact records commands, failures, remedies and final results.
* Local commit uses authenticated account noreply author/committer and co-author trailer; remote branch is not pushed.
* Publication gate remains distinct: this task's complete-gate execution is blocked because it invokes forbidden non-cost az commands; record the reason and hand off to coordinator without a receipt or publication-ready claim.
* Coordinator must obtain independent exact-head assessment after fresh-base receipt verification before publication. Missing/adverse original Review, full gate, receipt verification or exact-head assessment blocks publication; any later commit/base/tool/input change invalidates prior receipt.

## Implementation Context Record

| Item | Artifact |
| --- | --- |
| Research | .copilot-tracking/research/2026-10-29/iot-consumer-110-refresh-research.md |
| Details | .copilot-tracking/details/2026-10-29/iot-consumer-110-refresh-phase-details.md |
| Changes, owned by implementation | .copilot-tracking/changes/2026-10-29/iot-consumer-110-refresh-changes.md |
| Review, owned by Review | .copilot-tracking/reviews/logs/2026-10-29/iot-consumer-110-refresh-review.md |
| Continuation | Explicit caller authorization for all four phases; no automatic follow-up session |

## Sources

* Research C1-C7/W1-W2 and user request.
* Current src project READMEs, pyproject files and Source projects CI.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Integrate main

Dependency: Ready plan and critique.

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Rebase and resolve

Resolve authenticated privacy-safe committer identity first, then git fetch origin main, record full before/base SHAs and git rebase origin/main, preserving intent in documentation/config conflicts. Main's rubric and scenario manifest are authoritative. Replayed commit authors remain untouched; new commit uses authenticated identity.

<!-- rpi:task id=P01-T02 -->
#### [x] P01-T02: Reconcile contracts and pins

Verify main ancestor, rubric equality, manifest hashes and source/test placement. Fix only demonstrated integration defects.

<!-- rpi:phase id=P02 -->
### [x] P02: Validate integrated source

Dependency: P01.

<!-- rpi:task id=P02-T01 -->
#### [x] P02-T01: Run lint, types and units

Install observed missing declared dependencies in /tmp/mv. Run core/API ruff check ., ruff format --check ., mypy, core sensor/backfill/privacy/manifest selectors and API IoT/ingestion selectors. Full API permitted only while flock -n /tmp/ama-rpi-heavy.lock succeeds and remains held. Record skips separately from live acceptance.

<!-- rpi:phase id=P03 -->
### [ ] P03: Review, commit and hand off

Dependency: P02.

<!-- rpi:task id=P03-T01 -->
#### [x] P03-T01: Freeze source and perform one Review

Reconcile plan/details/changes; independent reviewer assesses actual integrated diff and conflict resolutions, recording one outcome. Findings route to later work, never a repeated Review in this task.

<!-- rpi:task id=P03-T02 -->
#### [ ] P03-T02: Commit and publication-gate handoff

Resolve gh api user, configure repository-local noreply email, commit all intended evidence and implementation with Conventional Commit/trailer. Record the demonstrated complete-gate az-permission blocker; coordinator owns execution in an authorized environment and external receipt. Prepare local PR notes, including dated official-price estimate and caveats only there. No push or remote PR edit.

## Test Ownership and Change Budget

* Canonical source: src/core/src and src/api/src; tests: owning src/<project>/tests directories.
* Canonical metadata: main's scenario-manifest.json; no generated runtime outputs.
* Exact test removals: none. Maximum additions: two tightly scoped integration regressions only if demonstrated failures require them; no speculative tests.
* Semantic evidence: compare replay against main generator; regression evidence: existing send admission, cleanup, provenance, ingestion and manifest suites.
* Existing assertions and exemptions must not be weakened to make checks pass.

## Dependencies

* /tmp/mv and declared SDK/dev dependencies; pip installation justified by missing SDK detection.
* Shared heavy lock and full-gate local tools; no Azure fallback.
* Hosted rubric verdict and current-head CI depend on coordinator publication.

## Critique Disposition

Exactly one critique executed, verdict Revise; no second critique. All five findings disposed in this final plan:

| Finding | Disposition | Evidence / resolution |
| --- | --- | --- |
| PC-001 | Applied | Acceptance and P03 handoff require coordinator's separate post-gate independent exact-head assessment; original Review is not rewritten or repeated. |
| PC-002 | Rejected as inapplicable to parent runtime | This parent has no prohibition on /tmp operations; caller explicitly mandates /tmp/mv and shared lock. Child execution restrictions cannot establish parent restrictions. No path substitution or gate bypass is used. |
| PC-003 | Applied | P01 explicitly fetches main again and captures full SHAs immediately before rebase. |
| PC-004 | Applied | Details include installed-distribution checks and complete focused selectors/path variables. |
| PC-005 | Applied | Authenticated repository-local committer configuration precedes rebase; historical authors remain unchanged. |

## Follow-Up Items

* Coordinator must publish rebased branch and obtain current-head hosted/rubric results; no source change can prove a hosted verdict locally.
* Coordinator must clear complete-gate authorization, generate and verify the external full receipt against fresh main, and obtain independent exact-head assessment before publication. This task does not run az bicep or bypass runner controls.
* Existing live Hub/credential/SQL/budget/OD-43 gates remain outside this refresh.

## Handoff

P01/P02 and P03-T01 complete. One original Review: Complete / Conformant with justified divergence, no source defects; RV-001/RV-002 route already disclosed publication/hosted gaps to coordinator. P03-T02 local evidence commit remains. Preserve original 2026-10-27 outcomes. Coordinator owns publication only after acceptable original Review, clean committed candidate, full external gate, fresh-base receipt verification and independent exact-head assessment. No push is authorized in this task.
