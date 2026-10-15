---
title: Sensor backfill 177 final-candidate plan critique
description: One bounded assessment of register-backed backfill readiness
ms.date: 2026-10-15
---

## Metadata

* Task ID: 177 / sensor-backfill-177.
* Critique date: 2026-10-15.
* Plan: .copilot-tracking/plans/2026-10-15/sensor-backfill-177-plan.md.
* Phase details: .copilot-tracking/details/2026-10-15/sensor-backfill-177-phase-details.md.
* Research: .copilot-tracking/research/2026-10-15/sensor-backfill-177-research.md.
* Critique execution status: Complete.
* Candidate assessed: final candidate, before implementation.
* Assessment count: exactly one; no delegated assessment or critique loop.

## Inputs and Criterion Boundary

The supplied plan, details and research define a partial Refs #177 delivery:
an optional synthetic-register adapter, merged stock-fabric-v1 reuse,
deterministic two-year generation, explicit monitoring choices and bounded
local evidence. Open children and owner evidence remain open, not implicitly
deferred or accepted.

The assessment covers all functional/non-functional requirements, acceptance
criteria, P01-T01 through P02-T02, test ownership/addition limits, legacy
compatibility, dependencies, safety boundaries and delivery claims.

Implementation evidence inspected:

* src/core/src/zava_forward/core/synthetic/sensor_backfill.py:
  writer, estimate, CLI defaults, projection, DDL and portable loader.
* src/core/src/zava_forward/core/synthetic/stock_fabric.py:
  v1 seed, opaque IDs, fabric draws and destination checks.
* src/core/src/zava_forward/core/synthetic/provenance.py and
  src/core/src/zava_forward/core/synthetic/__init__.py:
  fingerprints, nonempty/symlink protection and output defaults.
* src/core/tests/test_synthetic_determinism.py,
  src/core/tests/test_sensor_backfill.py,
  src/core/tests/test_sensor_plausibility.py and
  src/core/tests/test_stock_fabric.py:
  existing byte, source, window, plausibility, loading and destination contracts.
* src/core/pyproject.toml, src/core/README.md, src/api/README.md and
  src/api/tests/test_assistants.py:
  strict typing boundaries, ownership and actual HTTP release smoke.
* docs/adrs/0006-src-layout-and-cutover.md,
  docs/architecture/mvp-to-src-parity-matrix.md, the case-study original and
  relevant addendum sections, reference index, memory and sector primer:
  src placement, migration continuity and human/resident authority.

No external research, private register access, implementation, test execution,
issue mutations or approval decisions were performed. Research W1-W5 are
assessed as supplied dated evidence, not independently refreshed GitHub state.
No changes to the supplied plan, details, research or existing implementation
are part of this critique.

## Coverage Assessment

| Requirement, research, phase or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| Full RPI, src-only new code/tests, pip and protected paths | Covered | P01/P02 preserve layout and full-loop artifacts; this critique writes only its requested artifact |
| Partial Refs #177; children and owner evidence open | Covered | Research W1-W5 and Follow-Up Items explicitly reject full closure |
| Register identity and stock-fabric reuse | Partial | Fixed v1 fabric reuse is credible; SQL identifier compatibility requires PC-001 |
| Synthetic-only input and minimized output | Covered | Allowlist, is_synthetic marker, source digest and sanitized snapshot are explicit |
| Sorted subset and monitoring choice exclusions | Partial | Denied/unknown and all-excluded contracts are explicit; invocation defaults and subset bounds require PC-003 |
| Determinism, source hashes and legacy payload compatibility | Covered | Existing golden payload hashes remain; only dependency expectations may change |
| 730-day UTC boundaries and sharding | Covered | Existing half-open window machinery is reused; P01-T02 adds new-mode coverage |
| Actual-sensor estimate before payload generation | Covered | Prepared selection is explicitly shared by estimate/writer; zero case is specified |
| New-mode destination safety | Partial | Production restrictions are appropriate; validation execution must respect PC-002 |
| SQL portability and idempotent loading | Partial | Portable conditional insert exists; SQLite alone will not expose PC-001 |
| Core test ownership, no removals, one new module, maximum 16 tests | Covered | Explicit lock is coherent; use grouped subtests for permutations and findings below |
| Strict typing and migrated untyped calls | Covered | Typed adapter/test requirement and narrowly scoped call allowance avoid new blanket exemptions |
| P02-T01 local suites, lint/types, App and container evidence | Partial | Existing App smoke is suitable; forbidden output operations need preflight disposition under PC-002 |
| P02-T02 review, commit, PR and no merge | Covered | Verified noreply, required trailer, main-targeted PR and honest pending-CI status are explicit |
| AI/human approval and resident consent | Covered | No new authority; existing HTTP smoke proves bounded scripted proposal admission, not live AI or resident approval |

## Verdict

* Verdict: Revise.
* Severity summary: 0 Critical, 1 High, 2 Medium, 0 Low.
* Rationale: the bounded slice is credible, but its new identifier contract
  conflicts with the existing SQL contract. Selection defaults and permitted
  validation execution also need explicit planner corrections before handoff.
  These are not reasons to expand scope into open child stories or to request
  already-settled owner decisions.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: Opaque IDs and full-digest sensor IDs exceed the existing SQL contract

* Related IDs: opaque identity functional requirement; portable SQL and legacy
  compatibility non-functional requirements; P01-T01; P01-T02.
* Evidence: src/core/src/zava_forward/core/synthetic/sensor_backfill.py,
  SQL_DDL declares sensor_id VARCHAR(20), home_id VARCHAR(12) and reading_id
  VARCHAR(40). readings constructs reading_id from sensor_id plus a timestamp.
  stock_fabric accepts arbitrary nonblank, unpadded opaque strings.
  P01-T01 requires a full-ID digest and P01-T02 requires portable load
  idempotency, while the plan excludes schema migrations.
* Concern: the plan does not reconcile these widths with the new identity
  format. A full SHA-256 hex digest alone is 64 characters, before any prefix
  or timestamp; valid opaque home IDs can also exceed 12 characters. SQLite
  TEXT loading and current conditional-insert syntax tests will not detect a
  SQL Server width failure. This is a new-mode compatibility gap, not a request
  to repair unrelated legacy SQL.
* Impact: the new mode could pass local loading and determinism checks but
  produce files that cannot be loaded under its advertised Azure SQL schema.
  Truncating IDs to fit would undermine exact reconciliation and uniqueness.
* Smallest useful change: define the new-mode identifier/reading-ID format and
  a matching explicit SQL schema contract before implementation. Prefer an
  additive, versioned stock-mode DDL contract with declared supported bounds
  and preflight rejection beyond those bounds; retain the legacy DDL/API and
  payloads unchanged. Do not silently migrate an existing database or truncate
  home IDs/digests. Document how callers select the matching schema with the
  existing loader hook.
* Action owner: planning parent, then P01 implementation owner.
* Exact resolving evidence: P01-T01 names the format, supported lengths,
  schema/version selection and rejection timing. Within the existing new-test
  budget, P01-T02 checks long opaque IDs, full sensor/reading lengths,
  rejection before payload writes and parameter-preserving portable loading
  with create_schema=None. Existing golden legacy hashes still pass. Real
  SQL Server execution remains explicitly unverified unless actually run.
* Decision route: direct planner correction. A separately requested migration
  of existing databases would require a new scope decision; it is not needed
  for the recommended additive contract.

<!-- rpi:critique id=PC-002 -->
### PC-002 [Medium]: Validation has no execution-safe output-location disposition

* Related IDs: worktree-only execution boundary; new stock destination
  requirement; Test Ownership and Validation Lock; P01-T02; P02-T01.
* Evidence: the plan specifies temporary generated targets outside the
  repository and a real register-mode CLI exercise. stock_fabric._destination
  rejects every repository destination. Existing core tests use
  tempfile.TemporaryDirectory without an explicit location. The supplied
  execution constraints forbid /tmp and temporary-directory operations and
  require file operations to remain project-relative in this worktree.
* Concern: the validation task cannot simply inherit the current test recipes
  or default ZF_DATA destination in this session. Redirecting temporary output
  inside the checkout also cannot make a real stock-backed write succeed,
  because the production guard correctly rejects it. This is an execution
  constraint, not permission to weaken the destination guard.
* Impact: unqualified execution of the proposed commands could violate the
  session boundary; bypassing the guard to get a green smoke would invalidate
  the safety evidence. Merely recording a failure afterwards is insufficient
  for an operation known beforehand to be prohibited.
* Smallest useful change: add an output-location preflight before validation.
  Classify commands by their file effects, run only permitted commands, and
  record restricted real-writer/full-suite checks as Not run with the exact
  constraint rather than attempting them. Use mocks/in-memory checks for
  eligible logic without calling them real destination/CLI proof. Keep
  acceptance for unavailable writer evidence unticked; do not create an
  external workspace, change global temp settings or relax production safety
  in order to complete this session.
* Action owner: planning parent and P02 validation owner.
* Exact resolving evidence: revised P02-T01 explicitly distinguishes permitted
  execution from restricted checks and names where command output/artifacts
  may be written. The changes/review evidence records each restricted command
  as Not run, not failed/passed, and preserves the outstanding real-writer
  acceptance gap until an independently authorized environment supplies it.
* Decision route: direct planner correction for this partial slice. Running
  those checks elsewhere needs separate authorization; no such authorization
  is inferred or required to record the gap honestly.

<!-- rpi:critique id=PC-003 -->
### PC-003 [Medium]: Register-mode defaults can silently choose the wrong workload

* Related IDs: declared sorted subset functional requirement; estimate
  requirement; full-stock storage follow-up; P01-T01; P01-T02.
* Evidence: sensor_backfill.main currently defaults to 1000 homes for writes
  and 60000 for estimate-only; write defaults homes to SHARD_HOMES and estimate
  defaults to scale_fixture.HOMES. The candidate says --homes selects a sorted
  subset but does not specify omitted --homes, an oversized request, or
  whether consent filtering precedes or follows subset selection. Full-stock
  storage approval is expressly open.
* Concern: routing through an optional prepared selection is not enough to
  settle those existing numeric defaults. A small register could inherit a
  nonexistent count; estimate-only and write could select different homes.
  Selecting N granted homes rather than selecting N register homes and then
  applying choices would also silently change the declared subset.
* Impact: coverage and pre-generation estimates can disagree, or a routine
  invocation can trigger an unapproved full-stock two-year workload.
* Smallest useful change: define new-mode CLI and Python API selection
  semantics independently of legacy defaults. Require an explicit positive
  subset count for stock writes while full-stock approval remains open;
  specify oversized-count rejection and selection-before-consent filtering.
  Give estimate-only the same resolved selection, and make an all-excluded
  selected subset distinct from an invalid zero-home request.
* Action owner: planning parent, then P01 implementation owner.
* Exact resolving evidence: P01-T01 states omitted/zero/negative/oversized
  count behavior, operation order and estimate/write identity; core README
  shows an explicit bounded invocation. Grouped P01-T02 cases cover those
  defaults/bounds, API/CLI parity, mixed consent at the subset boundary and
  a valid all-excluded subset, without exceeding the 16-test limit.
* Decision route: direct planner correction consistent with the supplied
  bounded-delivery direction; no new owner policy decision is necessary.

## Strengths and Residual Risk

* Reusing stock_fabric.fabric at the fixed v1 seed avoids a second invented
  stock model. Mapping projection age from build_year also avoids equating
  v1 age-band labels with the older backfill coefficient buckets.
* Separate stock mode plus retained historical payload hashes is a credible
  compatibility strategy. Changed source fingerprints are expected metadata,
  not permission to change historical CSV payloads.
* Test ownership and addition limits are explicit and feasible. No removals
  are proposed. Existing byte/plausibility/window tests remain regression
  owners; only their dependency-set expectation should change. The new module
  can group invalid-input, selection and length permutations with subtests;
  findings do not authorize a second module or a larger test count.
* The test budget must retain real assertions for CSV allowlisting, exact
  coverage reconciliation, fixed-seed fabric parity, construction sensitivity,
  seed/date variation, zero estimates and failure-before-payload behavior,
  rather than merely making commands finish successfully.
* The actual existing HTTP target is
  test_assistants.ApiTests.test_release_record_local_http, documented in
  src/api/README.md. It verifies denied calls, released scripted proposal,
  unchanged domain state and revocation; no new API test is needed.
* Synthetic consent is explicitly not real consent. No stock assumption,
  sensor observation or release record gains resident, investment, safety or
  professional approval authority.
* Climate provenance/licence, dated measures, fuller behaviour, complete
  fault/truth classes, consumer integration, storage approval and real
  AI/SQL Server/Azure/human evidence remain deliberately unresolved. They do
  not block this partial slice when its PR and acceptance claims retain
  those limits. They cannot be counted as completed #177 criteria.

## Questions or Blocking Evidence Gaps

No user response is required for the three planner-owned corrections.
No decision-critical evidence gap prevents this bounded critique verdict.
An authorized environment for restricted validation remains unavailable here;
recording that limit is not execution evidence or an approval to work elsewhere.

## Limitations

* This is plan credibility assessment, not implementation acceptance.
* No tests, builds, loaders or live services were run by the critique.
* No private data, source records, credentials or live consent were inspected.
* Current source contracts and supplied research support the findings;
  future implementation correctness and remote CI results are unknown.
* All findings available within the supplied boundary are returned together.
  No further critique pass is requested.

## Recommended Next Action

* Highest-impact finding: PC-001.
* Action owner: planning parent.
* Smallest next action: resolve the additive stock-mode identifier/schema
  contract, then apply PC-002/PC-003 directly and retain the existing test cap.
* User response required: no.
* Handoff: return this Revise verdict to the active planning parent; finalize
  its correction/disposition record without another critique. Implement only
  after the resulting plan gates are satisfied.

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/plans/2026-10-15/sensor-backfill-177-plan.md](.copilot-tracking/plans/2026-10-15/sensor-backfill-177-plan.md) | Final candidate assessed, unchanged |
| [.copilot-tracking/details/2026-10-15/sensor-backfill-177-phase-details.md](.copilot-tracking/details/2026-10-15/sensor-backfill-177-phase-details.md) | Task contracts assessed, unchanged |
| [.copilot-tracking/research/2026-10-15/sensor-backfill-177-research.md](.copilot-tracking/research/2026-10-15/sensor-backfill-177-research.md) | Supplied research, unchanged |
| [.copilot-tracking/plans/2026-10-15/sensor-backfill-177-critique.md](.copilot-tracking/plans/2026-10-15/sensor-backfill-177-critique.md) | Complete one-pass critique and actionable disposition |

## Next Steps

The active planning parent should directly resolve PC-001 through PC-003,
record the dispositions and preserve unavailable evidence as open. No user
action or further critique loop is required.
