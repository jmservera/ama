---
title: Indoor derived bounds implementation plan
description: Issue 179 model correction and acceptance audit
ms.date: 2026-10-27
---

Task ID: 179. Slug: indoor-derived-bounds-179. Task status: Complete.
Planning readiness was implementation-ready after direct PC-001 disposition.
Research: executed / Ready. Single Review: Complete / Conformant.

## Executive Summary

Replace the fixed 8 C and 15..98% indoor limits in both projection paths with
per-outdoor-row, dwelling-model-derived envelopes. Retain the existing
noiseless temperature/vapour equations and two Gaussian draws in their order,
but cap their residuals at three exercise standard deviations. RH remains
within its physical 0..100% domain. Version both changed models, prove the
envelopes on actual pinned public records, and audit all #179 criteria.

## Sources

Research: .copilot-tracking/research/2026-10-27/indoor-derived-bounds-179-research.md
(C1--C7). Details:
.copilot-tracking/details/2026-10-27/indoor-derived-bounds-179-phase-details.md.

## User Decisions and Requirements

* Deliver #179 criterion 3 using outdoor-record and dwelling-derived bounds;
  keep exercise labels, add tests and re-evaluate every criterion.
* Run research, plan, implement, review in order; commit dated evidence.
* Reuse the existing branch; one PR to main. No private data/secrets/Azure/uv.
* Local relevant tests only; no full gate. A small model correction does not
  justify spending the one authorized large-change scoped heavy gate.
* Close #179 only if all three story criteria are evidenced; do not close #177
  or equate synthetic engineering results with live PRD acceptance.

## Goals

Finite causal model-consistent nominal series; reproducible exercise metadata;
explicit acceptance evidence with no physical-calibration claim.

## Scope and Non-Goals

Change indoor_projection, its tests and directly related core README/knowledge
base. Existing generator callers already supply the required outdoor rows.
No new dataset, architecture, API schema, ingestion thresholds, consent policy,
model inference, faulty-packet semantics, dependencies or infrastructure.

## Functional Requirements

FR1: derive noiseless temperature B and vapour V from each actual outdoor pair
and validated dwelling/schedule or household/dated-measure inputs.
FR2: temperature = B + bounded Normal(0,0.3); residual in [-0.9,0.9].
Humidity = clip(100*V/sat(temperature) + bounded Normal(0,1.5), 0,100);
residual in [-4.5,4.5]. Thus whole nominal RH envelope is
clip([100*V/sat(B+0.9)-4.5, 100*V/sat(B-0.9)+4.5],0,100).
The cap factor 3 and both scales remain explicitly exercise assumptions.
FR3: common projection math; preserve validation, UTC/home matching and RNG
draw order. New versions distinguish changed seeded values; no snapshot rewrite.

## Non-Functional Requirements

No unbounded extra passes/memory over histories. Deterministic output, explicit
errors and type safety; public source hashes unchanged. Bound claims apply to
nominal signals, not intentionally corrupted observations. No scientific,
healthy-home, operational or legal validation claim.

## Acceptance Criteria

* #179.1: versioned inputs/equations/parameters documented in code, README and
  manifest and tested for model-version/fingerprint binding.
* #179.2: every coefficient/domain/noise cap labelled exercise, except the
  physical definition of RH 0..100%; no fabricated source/calibration.
* #179.3: both projection paths obey algebraically derived per-record envelopes;
  actual retained hourly history, dwelling and weather sensitivity, saturation,
  extreme inputs and forced Gaussian tails exercise them.

## Test Ownership and Validation Contract

Canonical tests: src/core/tests/test_indoor_projection.py. Amend its two
fixed-legacy-output tests rather than deleting them. Retain invalid-input and
fingerprint tests. Maximum 12 additional test methods in this file. No test
files removed; no generated tests. Integration is exercised through existing
sensor/history/consumer tests. Public climate pack is read-only and hash-pinned.
Independent test equations must not merely call the production bound helper.
Include hot/humid saturation, cold/dry below former floors, baseline/composed
fabric/household/date sensitivity, RNG state and repeated byte determinism.
PC-001: reserve a composed independent exact-equation/state test and recording
Gaussian stub checks for two calls in the prescribed order/scales, including
non-unit ventilation, active dated loss, tail and saturation cases.
Run canonical tests, existing relevant core synthetic/sensor tests, relevant
API discovery and changed-file ruff/mypy using installed packages. Do not
replay 60,000 homes or change workflow/check names.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Model and regression implementation

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Share bounded projection math, version and document parameters

<!-- rpi:task id=P01-T02 -->
#### [x] P01-T02: Add independent envelopes, tails and public-record/composed tests

<!-- rpi:phase id=P02 -->
### [x] P02: Evidence, validation and publication

<!-- rpi:task id=P02-T01 -->
#### [x] P02-T01: Update core README, synthesis, index and append-only log

<!-- rpi:task id=P02-T02 -->
#### [x] P02-T02: Run local checks and record exact results and criterion audit

<!-- rpi:task id=P02-T03 -->
#### [x] P02-T03: Obtain one Review, commit, push and open one evidenced PR

## Critique Disposition

Execution: Complete. Original verdict: Revise; one Medium finding PC-001.
Artifact: .copilot-tracking/plans/2026-10-27/indoor-derived-bounds-179-critique.md.
Directly applied PC-001: P01-T02 now requires composed exact numeric equality
and Gaussian two-call/order/state coverage within the 12-method budget.
No divergent user decision and no second critique. Final readiness: Ready.

## Follow-Up Items

Competent building-physics calibration and OD-43 activation approval remain
outside this exercise story. Future live-use work: Assets/Building Safety
commission competent calibration; Assets/Building Safety/DPO/data owners
resolve OD-43. Parent/live PRD acceptance is not inferred.

## Handoff

Implementation changes record:
.copilot-tracking/changes/2026-10-27/indoor-derived-bounds-179-changes.md.
All P01/P02 tasks are complete. Single Review is Complete / Conformant with no
findings. Implementation/original evidence commit 3d24537a was pushed and one
PR to main opened: https://github.com/jmservera/ama/pull/502.
The API's original missing-dependency failure and successful affected-module
retry are both retained. Source edits and PC-001 test evidence are complete;
no new critique, source work or Review is planned. Final evidence-only
bookkeeping preserves the assessed source fingerprints. Owner merge/hosted
checks remain separate from this completed manual full-loop task.

## Correction cycle 1 plan (2026-10-27)

Task identity remains 179 / indoor-derived-bounds-179. This user-requested
correction is a new ordered cycle, not a rewrite of the original critique or
Review. Research C8/C9: executed / Ready. Candidate readiness: ready for one
correction-cycle critique. No owner decision is unresolved.

Executive summary: the v2 projection intentionally changes new snapshot rows.
Advance containing snapshot versions and bind the replacement golden to
literal model/snapshot versions; never alter published datasets. Retain the
unchanged scale/sensor-register goldens and the historical sensor digest in
dated evidence. Gate new readers on their current versions, update stock
privacy recognition, and run exact full core CI commands.

User requirements: fix hosted src-core, run research/plan/implement/review in
order, append existing artifacts, use pip only, preserve branch/PR and
Closes #179 only while all criteria remain evidenced. No heavy gate.
Goals: version-honest snapshot output, strong byte determinism and green full
core CI. Scope: sensor snapshot writer/readers, privacy version recognition,
canonical determinism/integration tests and related documentation. Non-goals:
legacy algorithm support, schema/fault-algorithm changes, source datasets,
live seeding or operational authority.

Functional requirements: bump default v2 to v3, stock v1 to v2, integrated v1
to v2; distinguish fault snapshot v2 from unchanged packet algorithm v1.
Use shared writer constants for readers/privacy; preserve old stock recognition
for historical privacy auditing without permitting old-version loader replay.
Pin current sensor digest with literal default and model versions. Reject
old snapshot versions at admission. Non-functional requirements: unchanged
RNG, equations, schemas, identifiers and monitoring/approval boundaries;
Python 3.12 and existing dev pins, no new dependencies.

Acceptance: reproduce the exact hosted mismatch, prove its cause with the
independent v1 equations; pass default/stock/fault/composed version and stale
admission checks; pass all CI core tests, lint, formatting and mypy. Preserve
the original #179 criterion proof via existing full-record projection tests.

Test ownership: src/core/tests/test_synthetic_determinism.py owns versioned
goldens; existing stock/history/privacy tests own integration. No file or test
removals; rename the misleading historical-equality method. Maximum four
additional methods, no generated tests. Separate semantic v2 envelope evidence
from byte-level regression goldens. No API/cloud/full-gate rerun is necessary
for this scoped synthetic snapshot correction.

<!-- rpi:phase id=P03 -->
### [x] P03: Correction cycle 1 implementation

<!-- rpi:task id=P03-T01 -->
#### [x] P03-T01: Version snapshots, wire readers/privacy and regression goldens

<!-- rpi:task id=P03-T02 -->
#### [x] P03-T02: Document intentional change and run exact core CI checks

<!-- rpi:phase id=P04 -->
### [x] P04: Correction cycle 1 review and publication

<!-- rpi:task id=P04-T01 -->
#### [x] P04-T01: Independent Review, append evidence, commit and same-PR push

Follow-ups remain future building-physics calibration/OD-43, not part of this
correction. Details: existing phase-details artifact, correction-cycle section.

### Correction cycle 1 critique disposition

Execution Complete; original verdict Revise, one Medium PC-C1-001. Directly
applied: stale-version tests mutate only `version` on valid current snapshots
with current revision/payload hashes. Parameterize default/stock/composed;
assert version-specific refusal before replay/write/consumer/schema/SQL calls.
Positive current-version load tests remain the controls. No extra methods
beyond the locked maximum four, no divergent decision, no repeat critique.
Final planning readiness Ready.

### Correction cycle 1 implementation handoff

P03 complete. Final exact CI core discovery: 1,437 run, 1,251 passes,
186 existing optional skips, no failures/errors, 433.719 seconds on Python
3.12.3. Full core ruff check/format and mypy pass (100 formatted files,
153 typed files). New snapshot versions/golden, isolated stale-admission
regressions and both historical/current stock privacy classification pass.
All #179 criteria remain supported by the unchanged ten canonical projection
tests, including pinned full-record traversal. No source edits remain.
P04-T01 Review/publication remains; no human/hosted/live approval is inferred.

Correction-cycle independent Review now Complete / Conformant, no findings.
Its independent 13-pass/nine destination-guard-error selector and causal/
static evidence are recorded honestly; supplied final full discovery confirms
the affected methods. P04-T01 remains unchecked until actual publication.
No source changes follow Review.

Correction-cycle publication complete: commit 13042a9b pushed to the existing
branch without force; PR #502 description updated and its head verified.
All P03/P04 markers complete. Final evidence-only bookkeeping changes no
assessed source/test bytes. Owner review/merge and hosted checks remain.
