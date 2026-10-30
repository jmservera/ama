<!-- markdownlint-disable-file -->
# RPI Plan Critique: rebuild-148

## Metadata

* Task ID: 148
* Critique date: 2026-10-27
* Plan: .copilot-tracking/plans/2026-10-27/rebuild-148-plan.md
* Phase details: .copilot-tracking/details/2026-10-27/rebuild-148-phase-details.md
* Critique execution status: Complete
* Assessment: exactly one final-candidate critique; no subsequent critique requested.

## Inputs and Criterion Boundary

* Caller direction: ordered Research, Plan, Implement and Review with dated
  evidence; authoring and local validation only. No deployment, resource-group
  deletion, private datasets, secrets, environment files or uv. New implementation
  belongs in installed src packages with tests outside the package.
* Test ownership: src/orchestrator/tests/test_rebuild.py only for new tests,
  at most 30 tests, no removals. One draft PR to main must use Refs #148.
* Primary evidence:
  .copilot-tracking/research/2026-10-27/rebuild-148-research.md, C1-C7 and W1;
  infra/README.md, deployment-wrapper guidance and the complete seven-step
  "From-empty rebuild observed on 2026-10-12" sequence;
  infra/modules/storage.bicep; docs/adrs/0006-src-layout-and-cutover.md;
  src/orchestrator/README.md; src/orchestrator/pyproject.toml.
* Context read: docs/case_study_48_original.md,
  docs/case_study_48_addendum.md, docs/reference/README.md and
  docs/reference/memory.md. The cited BRD/PRD acceptance distinction was checked
  against the supplied requirement pointers. Memory is context, not evidence.
* Issue boundary supplied by the caller: checked scripted rebuild without secrets
  on argv; dependency teardown including budgets and empty inventory; synthetic
  seed/staff; dry-run and disposable-environment testing. The candidate expressly
  implements only local sequencing contracts and a SQLite rehearsal.
* Decisions respected: no Azure adapter or arbitrary shell hooks; existing
  deployment/auth/SQL helpers remain authoritative integration points. #138/#136
  acceptance is not assumed. No Azure completion or application acceptance can
  follow from this assessment.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| Ordered RPI loop and dated records | Covered | Research, plan/details and a future changes record/independent Review are identified. This critique does not execute later stages. |
| Partial issue scope, W1, C7 | Covered | All issue criteria remain partial, no boxes ticked, one draft PR uses Refs #148. |
| No secret argv/cloud execution | Covered | No credentials, subprocesses, shell hooks or Azure apply path; no claim that existing helpers were integrated or verified. |
| C1-C3, P01-T01 rebuild contract | Partial | Broad stage ordering is present, but mandatory discovery and identity-bound verification contracts are not completely specified; PC-001. |
| C3/C5, P01-T01 teardown | Partial | Child/dependency order, separate budgets and terminal emptiness are present; same-ID changes and full revalidation at each destructive boundary are underspecified; PC-002. |
| Synthetic seed/staff and restart | Covered | Generated reserved-domain fixtures and queries through reopened SQLite connections; no private lineage or real Entra/SQL parity claimed. |
| Dry-run | Covered | Declarative sequence only, no backend operations or operational success claims. Ordinary CLI output is not treated as forbidden I/O. |
| Disposable local workspace | Partial | Default TemporaryDirectory use conflicts with the execution environment's file-location restriction; PC-003. |
| ADR 0006, C4, test ownership | Covered | One new production module and one external test module, maximum 30 tests, no removals. |
| P01-T02 validation and documentation | Covered | Existing orchestrator suite, Ruff and mypy; component/runbook limits, original historical results retained, independent Review required. |
| Publication and acceptance | Covered within caller boundary | Local validation only, no heavy execution in this critique; neither publication eligibility nor hosted/human approval is certified. |

## Verdict

* Verdict: Revise
* Severity summary: 0 Critical, 1 High, 2 Medium, 0 Low.
* Rationale: the source-only delivery is useful and honestly bounded. A reusable,
  fail-closed engine with persistence and failure-injection tests can reduce
  later integration risk without an Azure adapter. Its implementation contract
  nevertheless needs the three direct corrections below. None requires new
  cloud authority, expansion of scope or a user decision.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: Specify the complete mandatory rebuild/check contract

* Related IDs: C1-C3, Q1, P01-T01, local criterion "all mandatory stages".
* Evidence: .copilot-tracking/plans/2026-10-27/rebuild-148-plan.md,
  Functional Requirements; .copilot-tracking/details/2026-10-27/rebuild-148-phase-details.md,
  P01-T01; infra/README.md, seven-step from-empty sequence, especially
  steps 1-3 and 7.
* Concern: the candidate promises a fixed mandatory stage tuple but enumerates
  only broad bootstrap/images/credential/grants/seed/apps/auth/staff/health/restart
  stages. It does not specify non-secret parameter validation, discovery from
  deployment outputs rather than guessed names, or the distinct acceptance
  contracts for API 401, browser redirection, workload-identity SQL reads/writes
  and both enabled model deployments. "Health" or a SQLite stage witness is not
  a defined substitute. Current deployment guidance also distinguishes API and
  orchestrator images; the historical single-image wording must not silently
  define the new contract.
* Impact: an implementation can pass its own fixed-tuple tests while omitting
  the checks that distinguish a successful rebuild from an exposed placeholder
  or an operator-only connectivity test. This undermines the reusable contract,
  even though no cloud acceptance is claimed.
* Smallest useful change: enumerate stable stage/check IDs and required ordering
  in P01-T01, mapped to all seven runbook steps and current image selection.
  Represent excluded live obligations as explicit integration/check contracts
  with simulated/not-executed local results. Separate historical retained
  lineage/roster requirements from the intentionally generated local fixture.
  Do not add a cloud adapter, real model call, credential input or preservation
  operation.
* Action owner: planning parent.
* Exact resolving evidence: revised plan/details contain the complete ordered
  contract and expected local result classes, including parameter validation,
  output discovery, applicable workload images and identity-bound postchecks.
  The existing test owner allocates parameterized/subtest coverage for exact
  trace, missing/reordered contracts and halt-on-failed-check within 30 tests;
  implementation later records actual results in the changes artifact.
* Decision route: direct planner correction; no human decision required.

<!-- rpi:critique id=PC-002 -->
### PC-002 [Medium]: Revalidate both inventories and safety metadata before every deletion

* Related IDs: C3, C5, Q2, P01-T01, changed-inventory negative tests.
* Evidence: .copilot-tracking/details/2026-10-27/rebuild-148-phase-details.md,
  P01-T01 specifies full validation before writes, then a reread refusing newly
  introduced resources; infra/modules/storage.bicep defines locks and immutable
  audit/digest retention. The plan promises fail-closed changed inventories.
* Concern: rejecting new IDs does not specify rejection of an existing ID whose
  type, scope, lock or retention metadata changes. The reread contract also does
  not explicitly cover both budget and generic inventories at every destructive
  boundary. Unexplained disappearance other than accounted-for descendants is
  not explicitly given a failure outcome.
* Impact: an adapter can satisfy the stated reread rule while operating on stale
  safety assumptions or a changed budget inventory. That would make the local
  rehearsal a weaker contract than its fail-closed claim.
* Smallest useful change: define canonical inventory records and exact expected
  remaining state for both inventories. Before each delete, validate scope,
  known type and available safety metadata again and reject additions,
  unexplained removals or changed safety fields. Only allow explicitly accounted
  descendant removal; absent/unknown required safety evidence must fail closed.
  State that this local check does not eliminate a future cloud race or authorize
  retention/lock bypass.
* Action owner: planning parent.
* Exact resolving evidence: revised P01-T01 states the comparison and rejection
  rules for both inventories. Its test allocation includes same-ID mutation,
  newly locked/protected records, unexplained disappearance and budget drift
  after initial validation, asserting no next deletion after detection. Existing
  dependency/lingering-delete checks remain, within the same 30-test module.
* Decision route: direct planner correction; no human decision required.

<!-- rpi:critique id=PC-003 -->
### PC-003 [Medium]: Replace the default temporary-directory workspace contract

* Related IDs: P01-T01, P01-T02, disposable local rehearsal.
* Evidence: .copilot-tracking/details/2026-10-27/rebuild-148-phase-details.md,
  P01-T01 requires a newly created TemporaryDirectory; P01-T02 suggests an
  external venv. The execution context prohibits file operations in /tmp,
  /var/tmp or temporary directories and requires new files relative to the
  working project directory.
* Concern: default TemporaryDirectory placement can use a prohibited system
  location, and the proposed external venv does not identify a permitted
  project-relative location. The implementer should not have to discover this
  conflict during validation or weaken the no-arbitrary-cleanup-path boundary.
* Impact: the proposed rehearsal/validation recipe is not executable as written
  under the supplied environment restrictions.
* Smallest useful change: replace system-temporary-directory use with a uniquely
  named, exclusively owned project-relative rehearsal workspace and specify a
  project-relative untracked validation environment if installation is needed.
  Permit cleanup only of that exact owned workspace; no caller-selected path,
  inherited ZF_DATA or system-temp fallback. Keep generated outputs out of git
  and follow the retention policy for any retained evidence.
* Action owner: planning parent.
* Exact resolving evidence: revised details name the permitted relative workspace
  policy for code, tests and validation commands. The canonical test module
  covers owned creation/cleanup and refusal to access another path; dry-run
  creates no workspace. Later changes evidence reports the actual paths and
  commands without introducing another test module or more than 30 tests.
* Decision route: direct planner correction; no human decision required.

## Strengths and Residual Risk

* Separating declarative contracts, operation and independent verification,
  explicit failure stops, separate budgets and persistent SQLite witnesses
  provides meaningful local value rather than merely printing a runbook.
* The no-Azure-adapter decision is an explicit and acceptable partial-delivery
  boundary. It is not itself a finding or a reason to require live execution.
* Local staff rows are not Entra provisioning, SQLite is not Azure SQL
  acceptance, and stage simulations are not image/model/auth/health evidence.
* Preserved lineage restoration, real helper integration, tenant authority,
  retention/preservation approval, #138 readiness and an authorized disposable
  Azure test remain deferred. Refs #148 must remain; no criterion is completed
  by this critique or rehearsal.

## Questions or Blocking Evidence Gaps

* No unresolved user choice blocks this bounded authoring plan.
* Whole-issue acceptance lacks live integration and disposable Azure evidence
  by design; do not obtain that evidence in this task.

## Limitations

* This is one source-based assessment, not implementation Review or test
  execution. No cloud commands, package installation, deployment, deletion,
  private data access or secret reads were performed.
* Issue/dependency status is assessed from the supplied research and caller
  context, not a fresh remote issue lookup. No current tenant/resource state
  or existing helper's live correctness is certified.
* Only this critique artifact is written. Existing untracked plan, details,
  research and state files are not changed, moved, staged or committed.

## Recommended Next Action

* Highest-impact finding: PC-001.
* Action owner: planning parent.
* Smallest next action: directly revise the mandatory stage/check contract,
  then resolve PC-002 and PC-003 in the same plan/details revision and record
  dispositions without rewriting this original critique.
* User response required: no.

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/plans/2026-10-27/rebuild-148-plan.md](.copilot-tracking/plans/2026-10-27/rebuild-148-plan.md) | Assessed final candidate |
| [.copilot-tracking/details/2026-10-27/rebuild-148-phase-details.md](.copilot-tracking/details/2026-10-27/rebuild-148-phase-details.md) | Task contracts requiring direct correction |
| [.copilot-tracking/research/2026-10-27/rebuild-148-research.md](.copilot-tracking/research/2026-10-27/rebuild-148-research.md) | Supplied evidence and partial-delivery decisions |
| [.copilot-tracking/reviews/plans/2026-10-27/rebuild-148-plan-critique.md](.copilot-tracking/reviews/plans/2026-10-27/rebuild-148-plan-critique.md) | Original single-pass critique |

## Next Steps

The active planning parent should resolve PC-001 through PC-003 directly,
record their dispositions and finalize the plan before implementation. Continue
the authorized ordered RPI loop with local validation and independent
post-implementation Review; do not start another critique. No user action is
required. Keep the delivery partial and the single PR draft with Refs #148.
