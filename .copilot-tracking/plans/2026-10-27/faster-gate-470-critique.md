---
title: Faster local gate issue 470 final-candidate plan critique
ms.date: 2026-10-27
---

## Metadata

* Task ID: #470 / faster-gate-470
* Critique date: 2026-10-27
* Plan: .copilot-tracking/plans/2026-10-27/faster-gate-470-plan.md
* Phase details: .copilot-tracking/details/2026-10-27/faster-gate-470-phase-details.md
* Critique execution status: Complete
* Assessment count: One independent final-candidate critique.

## Inputs and Criterion Boundary

* Caller requirements: fail-closed --changed mapping; bounded independent
  --jobs groups under the existing host lock; shared-environment, SQL and image
  serialization; same-identity --resume of failed/unrun groups through trusted
  dispatch; partial receipts rejected as full by default.
* Owner decisions already settled: unit tests plus a measured changed tier,
  no full gate, no Azure, topic PR using Refs #470 only. These decisions are
  constraints, not questions for reconsideration.
* Inputs assessed: the supplied plan, phase details and
  .copilot-tracking/research/2026-10-27/faster-gate-470-research.md, including
  research C1-C4 and the qualified historical timing claim W1.
* Contract evidence: tools/rpi-checks.py, especially clean_identity,
  environment_identity, required_groups, required_checks, verify_commands,
  verify_results, Runner.install, Runner.namespace_static_infra,
  Runner.browser, Runner.sql, Runner.image, Runner.cleanup, Runner.run,
  verify and main. Existing regression-test contracts were inspected in
  tools/test_rpi_checks.py.
* Repository context: original case study, addendum purpose/status, knowledge
  base index and owner memory. None expands this tooling task into application,
  regulatory or cloud implementation.
* Boundary: assess whether the plan is implementation-ready against the supplied
  contracts, not whether an implementation passes. No implementation was reviewed
  or edited; no tests, gate, browser, scanner, Docker or Azure execution occurred.
  Historical benchmark W1 was not independently retrieved or remeasured.
* Branch inspection found feat/faster-gate-470 tracking origin/main and no
  matching PR. Supplied planning inputs were already untracked; they were not
  moved, committed or changed.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| --changed; C2; P01-T01 | Partial | Fail-closed intent and rename handling are explicit; concrete mapping and bootstrap closure are missing. PC-001. |
| Receipt scope; C2; P01-T01/T02 | Partial | Default full rejection is correct; existing full-only artifact and command construction must become scope-aware. PC-002. |
| --resume; C2/C3; P01-T02 | Partial | Trusted dispatch and exact identity are explicit; failed-run checkpoints, shared-state baselines and immutable attempts are underspecified. PC-003. |
| --jobs; C1/C3; P01-T02 | Partial | Host lock and SQL/image exclusion are retained; snapshot readers/writers and concrete dependency/resource admission need definition. PC-004/005. |
| Existing full matrix; P01-T03 | Covered in intent | Preserve every check, scan freshness and existing mutation tests; no full run is authorized here. |
| Tests; P01-T03/P02-T01 | Partial | Unit-first validation and subtests are appropriate; findings identify required cases, not a request for a full benchmark. |
| Measured changed tier; W1; P02-T01/T02 | Partial | Historical versus measured timing is separated; full-fallback execution needs an explicit stop guard. PC-006. |
| Coordinator policy; C4; P01-T03 | Covered in intent | Parent/sub-issue stacks, risk-tiered tests and image retention are expressly required. |
| Publication; P02-T02 | Covered in intent | Exact final candidate, independent Review, ordinary topic push, Refs #470 only, hosted checks and owner merge remain separate. |

## Verdict

* Verdict: Revise
* Severity counts: Critical 0; High 5; Medium 1; Low 0.
* Rationale: The safety direction is credible, but the plan leaves unresolved
  contracts at the points where full-only verification, failed evidence and
  shared mutable execution must become selective. These are planner-owned
  corrections; no unresolved owner decision blocks revision.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: Specify executable path mappings and their setup closure

* Related IDs: --changed; C2/C3; P01-T01/T03; P02-T01.
* Evidence: phase details lines 8-12 assign documentation/tracking/agent Markdown
  to static and tooling to focused lint/types. tools/rpi-checks.py:required_groups
  has no tooling group; Runner.namespace_static_infra uses the namespace Python
  for static, while the pinned Ruff/mypy installation is currently in infra.
  Project dependency installs and shared src image context are explicit in
  required_checks and Runner.install/image.
* Concern: The proposed tiers have no concrete path-to-group or prerequisite
  table. Selecting current static requires namespace setup; selecting focused
  tooling checks needs a bootstrap outside the unrelated infra execution.
  Broadly treating all tooling as focused would also under-test other tools.
* Impact: Implementation could produce missing interpreters/tools, silently omit
  transitive consumers, or unintentionally execute heavyweight prerequisites.
* Smallest useful change: Add the ordered mapping and dependency table to phase
  details. Identify the exact runner/test tooling allowlist, trusted bootstrap
  and commands, application/dependency/image-context consumers, special build
  and workflow inputs, and unknown-path fallback. Define union behavior for mixed
  paths, additions/deletions/renames, empty changes and unusual Git path names.
  Preserve every current full-tier command when extracting focused checks.
* Action owner: Planning parent.
* Exact resolving evidence: A concrete mapping/closure table with expected group
  lists for this branch's planned runner, test, coordinator, README and tracking
  changes; planned subtests cover core/agents dependencies, requirements/build
  inputs, rename/deletion, mixed known/unknown paths and tooling outside the
  allowlist. The focused tier names its pinned bootstrap and trusted commands.
* Decision route: Direct planner correction; no owner response required.

<!-- rpi:critique id=PC-002 -->
### PC-002 [High]: Make all verifier inputs conditional on trusted selection

* Related IDs: Receipt scope; C2; P01-T01/T02.
* Evidence: tools/rpi-checks.py:required_checks accesses SQL ownership and MSSQL
  image identity before constructing any group's commands.
  environment_identity requires all six environments; verify_results requires
  browser, image and workflow evidence; Runner.run and verify require Trivy
  metadata and full image coverage. Plan lines 36-39 mention selection and scope
  but do not identify these mandatory full-only inputs.
* Concern: Filtering the existing command matrix by group is insufficient.
  A valid tooling-only receipt has no SQL/image/browser evidence with which to
  construct that matrix, and should not need unrelated venvs or scanner state.
* Impact: Partial verification either fails despite valid selected work or
  requires fabricated placeholder resources. Overbroad relaxation could weaken
  full verification.
* Smallest useful change: Define scope-aware trusted command construction,
  environment/tool requirements, required files, result checks and live-image
  checks, evaluated only after selection is independently recomputed. Specify
  explicit partial opt-in, rejected missing/invalid scope, legacy schema handling
  and when changed selection genuinely constitutes complete full coverage.
* Action owner: Planning parent.
* Exact resolving evidence: Phase details enumerate per-group verifier inputs.
  Planned fixtures accept a real minimal tooling/static partial receipt only
  with partial opt-in, reject scope/selection tampering and missing selected
  evidence, and retain every existing full-matrix mutation rejection.
* Decision route: Direct planner correction; no owner response required.

<!-- rpi:critique id=PC-003 -->
### PC-003 [High]: Define failed-run checkpoints and immutable resume attempts

* Related IDs: --resume; C2/C3; P01-T02; resume acceptance criteria.
* Evidence: plan lines 40-43 and phase details lines 22-27 require unchanged
  successful environments, immutable receipts/logs and reuse of the original
  output directory. In tools/rpi-checks.py:Runner.run, environment and scanner
  identities are captured only if no prior failure occurred. Runner.cleanup
  removes a clean snapshot. Runner.browser and Runner.sql mutate the API venv;
  infra/migration mutate namespace. Image reports and scanner metadata use
  fixed shared paths.
* Concern: The plan does not specify which failed receipts contain sufficient
  sealed state to resume, how successful groups bind the final shared-state
  baseline after a later group fails, or how reruns avoid overwriting evidence
  referenced by previous attempts. Preserving command logs alone is not enough.
* Impact: Early failure may make legitimate resume impossible; incomplete or
  altered state may be reused; rerunning fixed report paths can invalidate the
  supposedly immutable parent receipt.
* Smallest useful change: Define failed-attempt sealing and eligibility,
  selected successful-group manifests, shared-environment checkpoint ownership,
  clean exact-path snapshot restoration and handling of dirty/partial setup.
  Namespace new reports/logs/receipts per attempt and preserve referenced prior
  files. State how final verification combines only trusted successful reused
  groups and new successful executions, excluding failed historical commands.
  Validate provenance and state before starting any resumed child.
* Action owner: Planning parent.
* Exact resolving evidence: A resume state/attempt layout and planned subtests
  cover early preflight/setup failure, successful project-api followed by failed
  browser/SQL mutation, successful namespace followed by failed infra/migration,
  rerun image report paths, absent checkpoints, missing live images, dirty
  snapshots, repeated resume and parent-evidence tampering. Original receipt
  and referenced evidence hashes stay unchanged; receipt argv is never executed.
* Decision route: Direct planner correction; no owner response required.

<!-- rpi:critique id=PC-004 -->
### PC-004 [High]: Resource exclusions must cover shared snapshot readers

* Related IDs: --jobs; C3; P01-T02.
* Evidence: phase details lines 14-20 specify an install lock, namespace/API
  ordering and a Docker-resource exclusion. tools/rpi-checks.py:Runner.install
  performs editable builds and metadata_cleanup across all projects.
  Runner.image reads the shared src context or copies it for logo-0600.
  Namespace, static, infra, migration and extras also consume installed sources.
* Concern: Serializing installers with each other and images with SQL does not
  by itself exclude an image build or src copy while another installer writes
  or removes editable metadata in that same snapshot. The dependency/resource
  graph is not specified sufficiently to establish group independence.
* Impact: Parallel builds can consume transient generated inputs or fail
  nondeterministically; cleanup or a failed prerequisite can leave dependents
  executing against incomplete setup.
* Smallest useful change: Enumerate group prerequisites and resource read/write
  ownership. Place all mutable snapshot setup before its readers, or use an
  explicit reader/writer exclusion. Include extras and logo-copy work, shared
  venv mutations, SQL/image/scanner exclusion and cancellation/join-before-cleanup
  behavior. Distinguish blocked/unrun dependents from successful groups.
* Action owner: Planning parent.
* Exact resolving evidence: A dependency/resource table plus planned
  barrier-based scheduler tests demonstrate independent overlap, installer versus
  src-reader exclusion, namespace/API ordering, Docker exclusion, failed
  prerequisite propagation and all-child termination before cleanup/receipt
  sealing. Per-group trusted order remains invariant under shuffled completion.
* Decision route: Direct planner correction; no owner response required.

<!-- rpi:critique id=PC-005 -->
### PC-005 [Medium]: Define resource admission rather than only worker count

* Related IDs: --jobs; non-functional requirements; P01-T02/T03.
* Evidence: plan lines 50-52 and phase details lines 19-20 require conservative
  CPU/memory bounds and explicit insufficient-resource failure.
  tools/rpi-checks.py:image_build_argv reserves a 3 GiB/two-CPU Docker build;
  Runner.sql uses a 3 GiB/two-CPU container while running API-side checks.
* Concern: No admission formula, per-group reservation, safety headroom or
  invalid/unavailable-limit behavior is specified. A bounded worker count does
  not ensure that even one heavy group fits available cgroup/host resources.
* Impact: --jobs can remain numerically bounded yet overcommit memory, or
  silently clamp to an unusable one-worker run instead of failing explicitly.
* Smallest useful change: Specify positive --jobs validation, CPU quota/affinity
  calculation, host/cgroup available-memory calculation, conservative group
  reservations and headroom, and fallback/error behavior for unreadable or
  unlimited limits. Admit only fitting ready groups; fail if none can fit.
* Action owner: Planning parent.
* Exact resolving evidence: A documented deterministic admission rule and planned
  subtests for fractional CPU quotas, affinity restriction, constrained cgroup
  memory, missing/unlimited limits, invalid job counts and a single oversized
  ready group; execution never exceeds admitted reservations.
* Decision route: Direct planner correction; no owner response required.

<!-- rpi:critique id=PC-006 -->
### PC-006 [High]: Prevent fail-closed fallback from running the prohibited full gate

* Related IDs: Owner validation restriction; --changed; P02-T01/T02.
* Evidence: plan lines 18 and 22 require both unmapped-to-full fallback and no
  full execution. Phase details lines 35-36 call for an actual --changed run
  without an explicit pre-execution selection check. The candidate includes
  policy/documentation and new tracking paths as well as runner changes.
* Concern: --changed is not necessarily a fast run: one unmapped candidate path
  correctly selects the full matrix. An unconditional measured invocation can
  therefore violate the owner's prohibition while the selector behaves correctly.
* Impact: The validation phase could execute an expressly unauthorized full
  gate; treating the fallback as a passing fast measurement would also misstate
  evidence.
* Smallest useful change: Require a non-executing trusted selection inspection
  bound to the committed candidate and reviewed base before measurement.
  Execute only the confirmed partial tier; if selection is full or cannot be
  established, stop and report blocked measurement rather than run or override
  fallback. Fetch/reconcile the base before measurement and reverify the final
  exact HEAD/base before push; later commits/base movement invalidate evidence.
* Action owner: Planning parent.
* Exact resolving evidence: P02 contains an explicit full-selection abort branch,
  the expected partial groups for all final candidate paths, and an external
  measurement record with HEAD/base, selected groups, elapsed time, jobs and
  explicit partial verification. Unit fixtures demonstrate unknown-path full
  selection without executing the full runner. No full gate or Azure is run.
* Decision route: Direct planner correction under existing owner direction;
  no owner response required.

## Strengths and Residual Risk

* The plan correctly rejects arbitrary command replay, cross-commit reuse and
  partial-as-full verification, and retains scan freshness and skip policies.
* Host-wide exclusion and serialization of SQL/image work are appropriate
  foundations; findings refine their resource and dependency boundaries.
* Independent Review, original adverse evidence, hosted approvals and owner
  merge remain separate. Refs #470 must not become an automatic closing keyword.
* Historical 23-26 minute full timings and projected parallel gains are not
  new measured outcomes. Full parallel performance remains intentionally
  unmeasured by owner direction; this critique does not request that benchmark.
* Unit simulations cannot establish real full-matrix concurrent performance.
  That limitation should remain explicit rather than trigger unauthorized work.

## Questions or Blocking Evidence Gaps

* No unresolved owner choice. All PC findings are direct planner corrections.
* W1 is supplied historical context, not independently verified evidence;
  no performance guarantee depends on its reproduction.

## Limitations

* This is one plan critique, not an implementation review, execution result,
  publication approval or full-gate receipt.
* Source contracts were read only to test the plan's feasibility and coverage.
  No new research, benchmark, dependency installation or source change occurred.
* The planning parent should disposition this complete finding set in place;
  this assessment does not require a second critique pass.

## Recommended Next Action

* Highest-impact finding: PC-003, failed-state sealing and immutable resume.
* Action owner: Planning parent.
* Smallest next action: Define resume checkpoint/attempt ownership and complete
  the selection/verifier/resource tables, then disposition PC-001 through
  PC-006 before implementation.
* User response required: No. No recommendation overrides the no-full/no-Azure
  boundary or changes publication authority.

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/plans/2026-10-27/faster-gate-470-plan.md](.copilot-tracking/plans/2026-10-27/faster-gate-470-plan.md) | Assessed final-candidate plan |
| [.copilot-tracking/details/2026-10-27/faster-gate-470-phase-details.md](.copilot-tracking/details/2026-10-27/faster-gate-470-phase-details.md) | Assessed implementation and validation details |
| [.copilot-tracking/research/2026-10-27/faster-gate-470-research.md](.copilot-tracking/research/2026-10-27/faster-gate-470-research.md) | Supplied internal evidence and decisions |
| [.copilot-tracking/plans/2026-10-27/faster-gate-470-critique.md](.copilot-tracking/plans/2026-10-27/faster-gate-470-critique.md) | Complete independent critique and resolving evidence |
| [tools/rpi-checks.py](tools/rpi-checks.py) | Existing trusted runner and verifier contracts |
| [tools/test_rpi_checks.py](tools/test_rpi_checks.py) | Existing regression and mutation contracts |

## Next Steps

The active planning parent revises and records dispositions for all six findings,
then finalizes without another critique. No user action is required. This
critique task stops here; implementation, tests, measured partial validation,
Review and publication remain with the parent under the existing owner limits.
