---
title: Issue 176 src determinism final-candidate plan critique
description: Independent bounded assessment of implementation readiness and resolving evidence
ms.date: 2026-10-15
---

## Metadata

* Task ID: #176; delivery reference: Refs #176.
* Critique date: 2026-10-15.
* Plan: .copilot-tracking/plans/2026-10-15/issue-176-src-determinism-plan.md
* Phase details: .copilot-tracking/details/2026-10-15/issue-176-src-determinism-phase-details.md
* Critique execution status: Complete.
* This is one independent final-candidate assessment, not implementation,
  another research cycle, or the post-implementation RPI review.

## Inputs and Criterion Boundary

* Caller requirements: full RPI, new code/tests in src, no mvp edits,
  ZF_DATA/private synthetic outputs only, SQL portability, preserved AI-on
  smoke and human/consent gates, no invented acceptance or owner decisions.
* Supplied research:
  .copilot-tracking/research/2026-10-15/issue-176-src-determinism-research.md.
  Its W1-W3 remote claims were treated as supplied evidence, not independently
  retrieved or expanded.
* Direct technical evidence:
  src/core/src/zava_forward/core/synthetic/scale_fixture.py,
  src/core/src/zava_forward/core/synthetic/sensor_backfill.py,
  src/core/src/zava_forward/core/synthetic/__init__.py,
  src/core/src/zava_forward/core/insights.py,
  src/core/tests/test_sensor_backfill.py,
  src/core/tests/test_sensor_plausibility.py,
  src/core/tests/test_generated_dataset.py and src/core/pyproject.toml.
* Architecture and operating evidence: docs/adrs/0006-src-layout-and-cutover.md,
  docs/architecture/mvp-to-src-parity-matrix.md,
  src/core/README.md, .github/workflows/src-ci.yml and the
  "Determinism, manifests and refresh policy (2026-10-15)" section in
  docs/reference/research/retrofit-synthetic-data/README.md.
* Project context: docs/case_study_48_original.md,
  docs/case_study_48_addendum.md, docs/reference/README.md and
  docs/reference/memory.md. Memory is context, not acceptance evidence.
* Assessed decisions: reuse moved generators; explicit end-date semantics;
  stable source revisions; fresh/empty destinations without overwrite;
  exact directory-byte tests; no replacement private stock generator.
* Assessed dependencies: P01 contract and regression work precede P02
  documentation/validation; their evidence precedes P03 review/delivery.
  Missing private source and policy approval remain outside engineering
  closure, not implicit prerequisites that this implementation can fabricate.
* Boundary: implementation credibility of this engineering slice, including
  compatibility, fingerprint closure, typing, test semantics and refresh
  safeguards. This cannot establish private-register reproduction, actual
  Azure/model execution, full-scale storage feasibility or owner acceptance
  of issue AC3.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| Caller src/ADR/SQL/consent constraints; C1-C2 | Covered | Core-only changes and unchanged portable loader preserve the bounded architecture. |
| W1; issue AC1 and AC2 | Partial, explicitly disclosed | Fictional scale and sensor coverage cannot prove the unavailable private stock generator. Do not tick full issue acceptance. |
| C3; P01-T01 explicit sensor as-of | Partial | Generation paths are named, but the independently sampled estimator is omitted; PC-003. |
| C3-C4; P01-T01 source revisions | Partial | Stable source hashing is sound; exact dependency inventory needs closure; PC-002. |
| P01-T01 fail-before-write and refresh refusal | Partial | Good no-overwrite intent; derived date-window validity must precede writes; PC-005. |
| P01-T02 exact bytes and historical compatibility | Partial | Whole-directory reruns are strong but not an old-versus-new compatibility oracle; PC-004. |
| NFR strict typing; P01-T02; P02-T02 | Partial | New strict tests call untyped moved APIs without a specified boundary; PC-001. |
| C5-C7 existing regressions and portable SQL | Covered | Keep existing support-generator and loader tests; no need to edit support generators or introduce a SQL dialect. |
| C6; P02-T01; issue AC3 | Covered as a proposal only | Cadence, approver and versioning remain unapproved; fresh paths do not confer refresh/reset authority. |
| P02-T02 local suites, AI-on smoke and Docker probe | Covered as planned evidence | Honest missing-model and privilege boundaries are retained; execution outcomes are not yet available. |
| P03-T01 review disposition | Partial | Unqualified future-work routing can defer an in-scope blocking defect; PC-006. |
| P03-T02 delivery | Covered | Explicit paths, privacy-safe identity, Refs #176, topic PR to main and no merge. |

## Verdict

* Verdict: Revise.
* Severity summary: 0 Critical, 1 High, 5 Medium, 0 Low.
* Execution is Complete: all supplied criterion areas were assessed once.
  Readiness is not Pass because six actionable planner-owned gaps remain.
* No significant or divergent user decision is needed to correct these gaps.
  The unavailable private generator and unapproved refresh policy remain
  explicitly open; this verdict does not demand their resolution or approve
  alternative acceptance criteria.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: Specify a strict typed boundary for the new regression tests

* Related IDs: NFR strict checks; P01-T01; P01-T02; P02-T02.
* Evidence: src/core/pyproject.toml sets strict mypy for src and tests.
  Moved scale_fixture and sensor_backfill have ignore_errors overrides, but
  their write, estimate and lower-level generator functions are unannotated.
  The plan forbids new exemptions and requires a new strictly checked test file.
* Concern: ignore_errors inside a moved module does not make calls to its
  untyped functions legal inside a newly typed test. Merely annotating the
  test methods will expose no-untyped-call errors. Leaving tests untyped
  instead conflicts with strict no-untyped-def. The plan names no bridge.
* Impact: The specified implementation can complete functional coverage yet
  fail its mandatory type gate, encouraging an unauthorized exemption or a
  wider typing rewrite.
* Smallest useful change: Choose and document a narrow typed interface for
  exactly the legacy functions the new tests need. For example, annotate
  their public signatures with concrete return structures, or provide
  localized typed callable adapters/casts without disabling checks. Keep the
  moved-module exemptions unchanged and avoid a general typing migration.
* Action owner: Planning parent; implementation owner supplies the evidence.
* Exact resolving evidence: P01 details name the chosen boundary and affected
  signatures/adapters; the new test methods and helper are annotated; existing
  core mypy passes including the new test file with no added ignore entries,
  command-line exclusions or new lint/type suppressions.
* Decision route: Direct planner correction; no user response required.

<!-- rpi:critique id=PC-002 -->
### PC-002 [Medium]: Close the explicit source-fingerprint dependency inventory

* Related IDs: Research Q2/C3-C4; P01-T01; P01-T02.
* Evidence: P01 details explicitly name scale, the new helper and the
  STAGE_ORDER source, then refer generally to sensor's "shared dependencies".
  Both writers also import output_dir from
  src/core/src/zava_forward/core/synthetic/__init__.py. That module is supplied
  evidence but is not explicitly assigned to either fingerprint.
* Concern: The inventory is not unambiguously closed. An implementation can
  hash only the named files and miss the shared package initializer while
  claiming all shared generator source is tracked. A generic helper
  sensitivity test would not detect that omission.
* Impact: A changed shared generator dependency could leave a provenance
  revision unchanged. This weakens the source-change visibility promised by
  the plan even if a particular output_dir change affects location only.
* Smallest useful change: Enumerate stable logical names for each writer's
  dependency set: its own module, the new helper, synthetic/__init__.py,
  insights.py, and scale_fixture.py additionally for sensor. State the
  intended boundary as project generator source, not the Python standard
  library or every import in core. Hash the new helper itself and preserve
  deterministic ordering and unambiguous name/content boundaries.
* Action owner: Planning parent; implementation owner supplies the evidence.
* Exact resolving evidence: P01 details contain the complete per-writer
  inventory; tests show that changing each included dependency's supplied
  source bytes changes the appropriate revision, including initializer and
  transitive scale/insights dependencies for sensor, while physical path or
  input enumeration order does not. Tests use controlled bytes/mocks, not
  edits to live repository files.
* Decision route: Direct planner correction; no user response required.

<!-- rpi:critique id=PC-003 -->
### PC-003 [Medium]: Propagate the requested sensor window into estimation

* Related IDs: C3; P01-T01 explicit as-of; P01-T02; P02-T01 CLI recipe.
* Evidence: sensor_backfill.py:129-150 independently samples outdoor_series
  and readings inside estimate, then writes estimate.json before the actual
  series. P01 details require passing start through outdoor/readings from
  write, but do not mention estimate or the --estimate-only branch.
* Concern: Passing a new start only to the actual output generation leaves
  the measured estimate on the historical START window. Its sampled byte
  widths and potentially fault/series behavior then describe another window.
  CLI estimation may also ignore or fail to accept the same as-of contract.
* Impact: A deterministic, hashed estimate.json can still be semantically
  wrong for the requested generation window. Hash verification alone cannot
  detect this.
* Smallest useful change: Thread the same resolved UTC start/end, days and
  cadence through estimation and generation. Preserve existing low-level
  default behavior when no new argument is supplied. Define the as-of option
  consistently for write and estimate-only CLI routes.
* Action owner: Planning parent; implementation owner supplies the evidence.
* Exact resolving evidence: P01 details name the estimator propagation and
  CLI behavior; a non-default-as-of regression verifies the estimator sample
  uses the resolved window, estimate.json equals the manifest estimate, and
  estimate-only honors that same requested window. Equality between two
  unchanged historical estimates is not sufficient evidence.
* Decision route: Direct planner correction; no user response required.

<!-- rpi:critique id=PC-004 -->
### PC-004 [Medium]: Add an independent oracle for historical rows and date semantics

* Related IDs: Research "Keep historical default series unchanged";
  P01-T01 compatibility; P01-T02; slice byte-equality acceptance.
* Evidence: P01-T02 names preserved default start, rerun equality, bounds and
  dates, but no captured pre-change payload oracle.
  test_sensor_backfill.py compares one shard between two current runs;
  test_sensor_plausibility.py checks broad distributions using START.
* Concern: Two equally changed outputs can pass all rerun comparisons and
  retain the same first date while changing RNG consumption, sensor fields
  or readings. The planned generic bounds assertion also needs to respect
  deliberate OUTLIER readings already permitted by the plausibility tests.
* Impact: The plan can report historical row preservation without evidence,
  or force an unintended physics change to satisfy an overbroad new test.
* Smallest useful change: Capture small pre-change scale and sensor payload
  byte digests or explicit expected rows before editing, then assert them
  after editing, excluding intentionally changed manifests. Use representative
  fixed inputs and a small full-default-days sensor sample if needed.
  Specify exclusive-end timestamp checks across every shard, verify shifted
  dates affect sensor payload rather than just metadata, and retain the
  documented scale calendar-year event semantics. Apply existing
  fault-qualified bounds, not an unconditional temperature limit.
* Action owner: Planning parent; implementation owner captures the baseline
  before source changes.
* Exact resolving evidence: P01 details require the baseline capture; new
  tests assert the captured old payloads, correct default start, all observed
  timestamps within the requested half-open window, cadence alignment and
  cross-shard file-set equality. Default-call compatibility expectations for
  custom days/cadence are stated explicitly. Hash maps cover exactly every
  non-manifest payload, including headers and estimate.json; sensitivity tests
  distinguish payload changes from metadata-only scale date recording.
* Decision route: Direct planner correction; no user response required.

<!-- rpi:critique id=PC-005 -->
### PC-005 [Medium]: Validate the derived window before preparing a destination

* Related IDs: P01-T01 fail-before-write; P01-T02 invalid-input preservation.
* Evidence: P01 requires positive counts, cadence division and valid ISO
  dates. A valid early ISO date such as 0001-01-01 cannot support subtracting
  730 days. Current sensor write creates its destination before estimate;
  the planned helper combines date validation and destination preparation.
* Concern: A syntactically valid as-of can still produce datetime underflow
  after directory creation or partial output. The sequence and valid
  derived-window domain are not specified. Date parsing success alone is
  therefore insufficient to meet fail-before-write.
* Impact: An invalid request can leave a newly created or partially populated
  output path, contrary to the advertised safety contract.
* Smallest useful change: Resolve and validate the entire requested window,
  including datetime/timedelta representability, before any mkdir/open/write.
  State the CLI date syntax and consistent error behavior. Cover both write
  routes and the estimator where applicable; no transactional guarantee for
  arbitrary disk failures is being added.
* Action owner: Planning parent; implementation owner supplies the evidence.
* Exact resolving evidence: P01 details specify validation-before-preparation;
  tests use valid-but-underflowing dates and invalid cadence/count/date cases,
  asserting a nonexistent destination remains nonexistent, an existing empty
  destination remains empty, and a refused nonempty destination retains its
  complete file set and exact bytes. A normal valid boundary window succeeds.
* Decision route: Direct planner correction; no user response required.

<!-- rpi:critique id=PC-006 -->
### PC-006 [Medium]: Distinguish review blockers from explicitly deferred scope

* Related IDs: P03-T01; P03-T02; full RPI completion.
* Evidence: P03-T01 says "Residual findings are future work" immediately after
  requiring one post-implementation review. It does not distinguish defects
  in delivered guarantees from the already disclosed private-source,
  full-scale, policy and external-evidence limitations.
* Concern: The literal disposition can route an in-scope determinism,
  overwrite, typing or gate-preservation failure to future work and proceed
  to delivery. One review is an execution count, not permission to accept
  whatever it finds.
* Impact: Full-RPI evidence may look complete while the agreed engineering
  guarantees remain broken.
* Smallest useful change: Explicitly gate ready-for-delivery claims on fixing
  in-scope blocking findings and rerunning affected validation. Route only
  declared out-of-scope items to follow-up. Preserve exactly one formal
  post-implementation review; record fixes and validation as dispositions,
  not another critique/review pass. If unresolved, report blocked/not ready
  rather than fabricate acceptance.
* Action owner: Planning parent; implementation/review owner records
  dispositions.
* Exact resolving evidence: P03 details separate in-scope blockers from
  accepted scope limits and name the delivery gate; the eventual review and
  changes artifacts map each actionable review finding to a fix and test
  result, an explicit authorized disposition, or a readiness blocker.
* Decision route: Direct planner correction; no user response required.

## Strengths and Residual Risk

* Reusing the migrated generators is consistent with ADR 0006. No core
  workload imports, mvp edits, support-generator rewrites or private-register
  replacement are needed.
* Whole-directory comparisons, multiple shards, file-set equality and hashes
  of all payloads substantially improve the current single-shard evidence.
* Refusing nonempty output without a force option prevents silent overwrite
  and stale-shard ingestion. It is not live database protection by itself;
  unchanged append/idempotence and reset-authority boundaries still apply.
* The plan keeps the SQL loader unchanged and retains its Azure-portable
  conditional-insert tests. Local SQLite evidence is not Azure SQL execution.
* AI-on local configuration, actual inference and deployment evidence are
  correctly distinguished. Missing real-model evidence must stay visible;
  deterministic data work does not relax resident consent or human approval.
* Issue AC1/AC2 stay unticked for the unavailable private register. The scale
  fixture is wholly fictional and is not an OSM-anchored reproduction route.
* The refresh cadence, per-refresh approver and versioning rules in the
  synthesis are proposals. Preserve that status and distinguish generator
  code-version bumps from any future approved dataset-version policy.
  Neither a source digest nor a new output path authorizes a refresh,
  discards prior manifests or authorizes replacing live SQL/staff records.
* Full-scale sensor generation, climate/device evidence and a named dataset
  owner remain outside the supplied implementation slice.

## Questions or Blocking Evidence Gaps

* No user question is necessary for this bounded revision. The six findings
  can be resolved directly by the planning parent.
* Private generator availability and owner policy approval remain required
  for full issue acceptance, but the plan already discloses both gaps. They
  are not new scope or invented acceptance decisions.

## Limitations

* Static plan critique only: no generator execution, type-check invocation,
  tests, private-data access, local app startup, Docker probe, deployment or
  GitHub mutations were performed.
* The typing concern follows directly from strict configuration and untyped
  public functions; no current failing mypy run is claimed.
* No new numerical physics, regulatory, product-acceptance or ownership
  criteria were introduced. Boundary tests above operationalize the supplied
  date, compatibility, provenance and fail-before-write requirements.
* The candidate plan, phase details, research and all source files were left
  unchanged. Only this critique artifact is written.

## Recommended Next Action

* Highest-impact finding: PC-001.
* Action owner: Planning parent.
* Smallest next action: Specify the strict typed legacy-call boundary, then
  reconcile all six findings in the plan and phase details before starting
  implementation.
* User response required: No.

## Artifacts

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/research/2026-10-15/issue-176-src-determinism-research.md](.copilot-tracking/research/2026-10-15/issue-176-src-determinism-research.md) | Supplied bounded research. |
| [.copilot-tracking/plans/2026-10-15/issue-176-src-determinism-plan.md](.copilot-tracking/plans/2026-10-15/issue-176-src-determinism-plan.md) | Final candidate assessed, unchanged. |
| [.copilot-tracking/details/2026-10-15/issue-176-src-determinism-phase-details.md](.copilot-tracking/details/2026-10-15/issue-176-src-determinism-phase-details.md) | Phase details assessed, unchanged. |
| [.copilot-tracking/reviews/2026-10-15/issue-176-src-determinism-critique.md](.copilot-tracking/reviews/2026-10-15/issue-176-src-determinism-critique.md) | Complete independent critique; Revise verdict. |

## Next Steps

Return to the active planning parent for direct reconciliation of PC-001
through PC-006. Finalize without another plan critique. Proceed to
implementation only after planner-owned dispositions are recorded; preserve
the later single post-implementation RPI review. No user action is required.
