<!-- markdownlint-disable-file -->
# RPI Plan: Approved sensor backfill integration

## Task Metadata

* Task ID: 177-approved-integration-2026-10-27
* Task slug: sensor-backfill-177-approved-integration
* Plan date: 2026-10-27
* Planning status: Ready; single Revise critique directly dispositioned
* Details: .copilot-tracking/details/2026-10-27/sensor-backfill-177-approved-integration-phase-details.md
* Critique: .copilot-tracking/reviews/plans/2026-10-27/sensor-backfill-177-approved-integration-plan-critique.md

## Executive Summary

Implement the approved source and identity decisions in their existing child
branches, merge all five children into the parent without rewriting ancestry,
and validate one integrated synthetic generator. Keep legacy behavior opt-in
and preserve the existing consumer's independent availability, consent,
calibration, ordering and replay checks.

### What You May Not Know

Full hourly history is over one billion rows. The full-stock local exercise
will declare a supported lower cadence and run the complete two-year window;
the hourly volume is estimated separately. No exact private-register coverage
claim is possible without reading the excluded private data. Source records
are reanalysis, not station observations or calibrated building physics.

### Unresolved Decisions or Blockers

None at planning; failed retrieval, consumer parity, shared lock or gate
prerequisites will be recorded as implementation/publication blockers.

## User Decisions and Requirements

* Owner key owner-approvals-2026-10-27-b approves candidate climate reuse for synthetic demo, existing stock home IDs as canonical, and child integration.
* Run Research, Plan, Implement and one independent Review in order with dated artifacts.
* Reuse parent feat/sensor-backfill-177 / draft #486 and children #481-#485 targeting parent.
* One foreground tools/rpi-checks.py --changed parent gate, lock timeout 0, fresh external output, git clean -fdxq first; supersedes --all.
* Run package unit tests and generator against generated 60,000-home stock; no private data, uv, secrets or main push.
* Use Refs only; tick proven criteria; resolve #178/#183 blocker comments; #486 ready only on passing checks and review; no parent merge.

## Goals

* Deliver reproducible, provenance-bound, canonical-ID synthetic history.
* Make the integrated code and its exact acceptance boundary independently reviewable.

## Scope and Non-Goals

In scope: core synthetic modules, paired climate evidence, child/parent branch
integration, related docs, tests, RPI records and GitHub evidence updates.
Non-goals: production activation, real monitoring authority, private stock,
physical calibration, unrelated PR #425 merge, issue closure and main merge.

## Functional Requirements

* Use genuinely retrieved two-year paired temperature/RH records with UTC alignment, derived bounds, hashes, source/version/retrieval/attribution and owner approval.
* Preserve canonical stock home IDs exactly; deterministic bounded sensor/reading IDs must resolve to their register and detect collisions.
* Wire versioned indoor projection, supplied dated retrofit measures and seeded neutral household conditions; do not infer missing works or consent.
* Export deterministically with separate evaluator fault truth and manifest binding every input/model/seed/window/cadence.
* Reuse actual SensorConsumer admission for compatible observations, never treating legacy load_into as equivalent; preserve availability/control checks and replay.

## Non-Functional Requirements

* Existing default deterministic generator behavior remains covered by regression tests.
* New input validation fails explicitly before output/SQL mutation where feasible.
* Memory bounded by stock metadata, shared climate and one per-home series/shard; output stays external.
* No automated grant of real consent/calibration, and no fabricated acceptance.

## Acceptance Criteria

* Both unblocked children contain implemented behavior and focused tests.
* All five child heads are ancestor merges of parent, with overlapping README content retained.
* Same seed/input produces identical output; canonical IDs, climate coverage, exact measure boundary, exclusions and consumer failures/replay are tested.
* Full 60,000-home generated fixture exercises the complete two-year window at an explicitly recorded cadence; actual rows, bytes and hashes are retained externally and summarized.
* Unit suites, selected static/types and exactly one scoped gate are reported truthfully.
* One post-implementation independent Review has a recorded outcome; ready transition requires passing hosted checks and no material Review findings.

## Implementation Context Record

Research: .copilot-tracking/research/2026-10-27/sensor-backfill-177-approved-integration-research.md
Changes: .copilot-tracking/changes/2026-10-27/sensor-backfill-177-approved-integration-changes.md
Review: .copilot-tracking/reviews/logs/2026-10-27/sensor-backfill-177-approved-integration-review.md
Automatic parent-owned continuation after critique disposition.

## Sources

* Research C1-C8, W1-W3 and user decisions.
* Existing child heads recorded in original 2026-10-27 changes evidence.
* Source #425 candidate at 72f52358; preserve its original adverse/unverified terms independently from approved demo scope.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Approved climate child implementation

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Integrate approved paired climate on #481

Reuse candidate provenance/adapter where appropriate; retrieve genuine second
year; implement a core-owned validated climate input and tests. Do not copy
unrelated candidate history or silently modify #425.

<!-- rpi:phase id=P02 -->
### [x] P02: Canonical identity child implementation

<!-- rpi:task id=P02-T01 -->
#### [x] P02-T01: Adapt canonical identities and consumer boundary on #485

Preserve stock home IDs, bound sensor IDs with collision detection, retain
consumer independent controls and SQL parity, and prove real consumer admission
using explicitly generated synthetic case/home fixtures, not availability bypass.

<!-- rpi:phase id=P03 -->
### [x] P03: Parent integration and aggregate behavior

<!-- rpi:task id=P03-T01 -->
#### [x] P03-T01: Merge children and wire integrated generator

Merge exact children without squash/rebase/force push. Preserve all README
sections. Add opt-in climate/projection/household/dated-effect wiring and manifest
binding. Produce generated public 60,000-home fixture, no private reads.

<!-- rpi:task id=P03-T02 -->
#### [x] P03-T02: Validate package and full-stock generator

Focused tests first, then all relevant src package unit suites. Generate complete
two-year full-stock history with declared cadence, measured pre-generation
estimate, deterministic replay sample, ID reconciliation and fault separation.

<!-- rpi:phase id=P04 -->
### [ ] P04: Review, one gate and truthful publication

<!-- rpi:task id=P04-T01 -->
#### [x] P04-T01: Record one independent Review

Reconcile implementation markers and evidence first; activate rpi-review once.
Route findings as later work, never repeat Review in this task.

<!-- rpi:task id=P04-T02 -->
#### [ ] P04-T02: Commit, clean, gate and publish evidence

Resolve gh user and local noreply identity, commit original RPI evidence with
required trailer. Inspect finite cleanup candidates, archive/restore-verify any
task-created caches/metadata before git clean -fdxq. Unknown inputs block cleanup.
Run exactly one foreground --changed --lock-timeout 0 against fetched main with
fresh external out; runner owns /tmp/ama-rpi-heavy.lock. Verify receipt with
--required-scope partial immediately before push and independent exact-head
assessment. No later source commit. Update child/parent PR bodies and issue
comments. Mark parent ready only after all applicable checks and review pass.

## Dependencies

P01 and P02 are independent whole phases in separate worktrees and may execute
in parallel. P03 depends on P01/P02 and existing #482-#484. P04 depends on
aggregate behavior/evidence. This phase split is execution ownership only;
critique PC references retain their original phase labels as historical evidence.
P03 composition and already-delivered child integration may proceed against
the agreed ClimateHistory.series/manifest seam while P01 acquisition completes;
final climate merge and aggregate validation still require completed P01.

## Locked Test Ownership and Targets

* Exact removals: none. Existing tests remain; update expectations only for intentional stock identity/version behavior.
* Maximum additions: four new test modules and 45 new test methods total for climate, identity/consumer and aggregate contracts.
* Canonical targets: src/core source/tests and source-evidence docs. Generated targets: external climate acquisition files and full-stock output; only approved bounded pinned climate inputs/derived evidence may be committed.
* Semantic coverage: real paired coverage/hash/gaps, stock ID case/length/collision, consent/calibration/home availability/replay, retrofit time boundary, household exclusions and manifest binding.
* Regression coverage: legacy seeded bytes/RNG and existing consumer test suites.
* Evidence: exact commands, counts, result hashes, window/cadence/stock lineage and independently assessed candidate boundaries.

## Critique Disposition

Critique execution Complete, original verdict Revise; not rescored or repeated.

| Finding | Owner/disposition | Resolving plan evidence |
| --- | --- | --- |
| PC-001 High | Planner, resolved directly | P01-T02 details separate 128-unit export from existing 64-unit SQL cases; no shared schema expansion |
| PC-002 Medium | Planner, resolved directly | P01-T02 fault namespace must yield UNMAPPED, not IDENTITY, with compact collision-checked sensor keys |
| PC-003 High | Planner, resolved directly | P02-T01 explicitly versions composed projection with independent loss/household inputs, not legacy whitelist misuse |
| PC-004 Medium | Planner, resolved directly | P02-T02 includes synthesis/index/log reconciliation before original Review and sole gate |

Acceptance qualifications: export preserves every supported canonical stock key,
but actual consumer availability remains bounded by the existing store (SQL
case keys <=64 UTF-16 units). Unsupported/unavailable keys fail without aliasing,
truncation or synthetic case invention by the loader. Public fixture admission
does not establish full private-stock admission.

## Follow-Up Items

* RV-001 Medium: later rpi-implement must validate composed replay's manifest count against actual granted sensors and enforce the row budget before write. Original Review execution Complete, outcome Not accepted; keep parent draft. This routed defect is not fixed or re-reviewed in this completed loop.
* GATE-BASE: sole authorized scoped gate attempt blocked before checks because fresh main2e031c89 is not an ancestor of candidate1b3f623f. Coordinator to authorize normal main integration and another scoped gate after correction; no push, stale-base retry or successful receipt.
* Production physical/source/regional qualification and real monitoring approval remain outside this synthetic exercise.

## Handoff

P01-P03 complete; P04-T01 original Review Complete / Not accepted at
263e1dbf, with one Medium RV-001 routed to later implementation. Original
critique and Review remain unchanged. P04-T02 publication is blocked: the sole gate
invocation rejected current-base ancestry before any checks or receipt.
Status-only closeout records the failed attempt, without claiming a passing
gate. All new child/parent commits remain local; PR evidence must say so.
Do not mark the parent ready.
