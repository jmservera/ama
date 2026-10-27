<!-- markdownlint-disable-file -->
# Review: rebuild-148

## Scope and Evidence

* Task ID: 148
* Review date: 2026-10-27
* Review scope: full authored P01/P01-T01/P01-T02 local-only boundary.
* Assessed boundary: fixed-contract sequencing, checked inventory teardown,
  synthetic SQLite control-plane adapter, external tests, component runbooks,
  critique dispositions and honest partial issue evidence. Not Azure automation
  acceptance or application-store integration.
* Candidate: unstaged/new work on feat/rebuild-148, supplied base
  f183ba391de10fb7bcfc6157cbcbb2290b9cf4fc. This is not a committed exact-head
  publication assessment.
* Plan: .copilot-tracking/plans/2026-10-27/rebuild-148-plan.md
* Phase details: .copilot-tracking/details/2026-10-27/rebuild-148-phase-details.md
* Plan critique: .copilot-tracking/reviews/plans/2026-10-27/rebuild-148-plan-critique.md
* Changes: .copilot-tracking/changes/2026-10-27/rebuild-148-changes.md
* Research: .copilot-tracking/research/2026-10-27/rebuild-148-research.md
* Source: src/orchestrator/src/zava_forward/orchestrator/rebuild.py
* Tests: src/orchestrator/tests/test_rebuild.py
* Documentation: changed infra/README.md and src/orchestrator/README.md,
  including the unchanged historical seven-step from-empty sequence.
* Context: original case study, addendum/index opening context, owner memory
  and src/orchestrator/pyproject.toml validation configuration. No fresh issue
  lookup was needed; supplied research W1 and caller define the four criteria.

## Opening Review State

* Interpreted review goal: independently assess source/local correctness and
  evidence, without upgrading partial #148 delivery into live acceptance.
* Review scope: the complete supplied P01 authoring boundary.
* Evidence readiness: supplied artifact set exists in the unstaged/new
  feat/rebuild-148 worktree. Reconciliation was pending at opening. The parent
  reported 68 tests, zero skips, and passing project Ruff/format/mypy; those
  results were not independently rerun at opening.
* Acceptance basis: current plan requirements, local delivery criteria, four
  partial issue criteria, critique dispositions and explicit owner boundaries.
* First comparison boundary: fixed stages/checks, inventory safety, persisted
  local readback and documentation against the no-Azure execution scope.
* Active read-only boundaries: only this record may change; no source or prior
  artifact mutation, agents, cloud operations, secrets/private datasets,
  deployment or deletion of RG ama; exactly one Review.
* Initial blockers: none to source assessment; live integration is residual.

## Execution Status

* Execution status: Complete
* Review execution evidence: one independent source/artifact comparison on
  2026-10-27, with bounded file-free regression execution and a mocked
  failure-path reproduction. All supplied artifacts were assessed.
* Implementation execution: P01 and both tasks are marked complete and have
  corresponding source/docs/validation evidence. Complete execution does not
  establish conformance; RV-001 remains.

## Plan-to-Change Reconciliation

| Current plan scope | Descriptive changes-record summary | Current-state reconciliation | Gap or rationale |
| --- | --- | --- | --- |
| P01/P01-T01 fixed sequencing | 17 stage/check contracts and halt-on-failure tests | Reconciled | Exact stage list covers the current contract, not execution of named infrastructure helpers. |
| P01-T01 canonical inventory | Scope/type/safety checks, both inventories and exact before/after readback | Reconciled | Separate budget validation, deterministic child/dependency order and drift failures are implemented. |
| P01-T01 local SQL | Generated case/staff/audit rows checked through new connections | Reconciled | Real fixture SQL persistence, expressly not core Store, tenant, workload identity or serving restart proof. |
| P01-T01 failure preservation | Changes claim failures stop without cleanup masking failure | Partial | Engine stops, but CLI destroys the failed rehearsal workspace and emits no failed-stage/partial-state evidence; RV-001. |
| P01-T02 documentation/validation | Two runbooks and reported project checks | Reconciled | No cloud success or issue completion claimed; historical live observations remain historical. |
| Follow-Up Items | Authorized helper integration, preservation/retention/tenant decisions, disposable Azure test | Reconciled | Distinct deferred work, not an unchecked active task or a defect merely because it remains open. |

## Completed Work Assessment

| Related marker | Files | What changed and why | Completion evidence | Validation | Assessment |
| --- | --- | --- | --- | --- | --- |
| P01-T01 | src/orchestrator/src/zava_forward/orchestrator/rebuild.py | Fixed immutable stages, backend protocol, bounded canonical inventory, checked deletion and local adapter | Source covers parameters through restart, separate budgets and generated SQL witnesses | Parent reports full suite; 16 file-free cases independently pass | Sound bounded architecture; CLI failure evidence defect remains. |
| P01-T01 | src/orchestrator/tests/test_rebuild.py | 22 external tests with operation/check failure subtests, drift and SQL tamper coverage | Test allocation remains below the 30-test limit; no removals | Independent subset passes | Tests assert sanitized error text but do not require failed-stage or partial-state survival. |
| P01-T02 | infra/README.md; src/orchestrator/README.md | Reproducible installed-module commands and explicit simulation limits | Diff preserves historical results and maps residual approvals | Source/link review; whitespace check passed | Accurate source-only/partial issue wording; no application or cloud acceptance inferred. |

## Implementation-Time Plan and Detail Update Assessment

| Affected area or marker | What changed and why | Triggering evidence and user decision | Reconciliation performed | Planning and critique state | Assessment |
| --- | --- | --- | --- | --- | --- |
| P01-T01 stage contract | Enumerated discovery, applicable workload images and identity-bound checks | PC-001; caller confirms fixed-contract source-only delivery | Plan/details/source/tests/changes agree on 17 stages | PC-001 applied before implementation; original critique preserved | Supported direct correction, no cloud authority added. |
| P01-T01 inventory checks | Exact immutable remaining records in both inventories | PC-002 safety concern | Canonical validation and before/after comparison match details | PC-002 applied; original critique preserved | Addressed within local contract; future cloud races remain explicit. |
| P01-T01 fixture schema | SQLite control-plane fixture rather than production application Store | Source-only simulation choice, explicitly confirmed by caller | Details/changes/both runbooks distinguish fixture SQL from application integration | Non-divergent implementation clarification | Justified; no user decision or fresh planning needed. |
| P01-T01 workspace | Owned disposable workspace retained | PC-003 rejection recorded as parent-context premise mismatch | Plan/details/changes record rejection; critique unchanged | Historical Revise verdict preserved | Do not reopen or relabel the original critique. Current review avoids filesystem rehearsal and system-temporary writes. RV-001 is failure-evidence loss, not a revival of PC-003's location claim. |

## Critique and Material Revision Assessment

* Latest critique dispositions: PC-001/PC-002 applied; PC-003 rejected with an
  explicit rationale. The original Complete/Revise critique remains intact.
* Material revisions: no unaccepted expansion into deployment, arbitrary shell
  execution, production data access or tenant authority. The caller explicitly
  confirms the narrowed fixed-contract/local-adapter acceptance basis.
* Dependent-work pause assessment: changes/details record the two direct
  corrections before implementation; no contrary evidence requires a planning
  pause or new user decision.
* Justification assessment: no Azure backend is an intentional partial-delivery
  boundary, not an implementation defect. Fixture SQL is appropriately labelled.
  However, CLI failure cleanup conflicts with the current preservation contract
  and is not documented as an implementation-time exception.

## Plan Follow-Up Assessment

| Follow-up item | Why outside immediate scope | Owner or next action | Assessment and route |
| --- | --- | --- | --- |
| Authorized Azure adapter and disposable cloud exercise | Current task permits authoring/local validation only; real helper, inventory, retention, tenant and credential obligations are not implemented | Owner selects a separate live-integration work item after exact inventory/preservation/retention and tenant authorization | Open distinct follow-up, mirrored in changes. Not a current defect, active P01 task or inferred approval. |

## Findings

<!-- rpi:review id=RV-001 -->
### RV-001 [Medium]: Failed CLI rehearsal loses the partial-state evidence the plan promises to preserve

* Related scope: P01-T01; Functional Requirements failure preservation.
* Evidence: src/orchestrator/src/zava_forward/orchestrator/rebuild.py:343-361
  wraps rebuild and teardown in TemporaryDirectory, whose exceptional exit
  removes the owned SQLite state. The outer handler emits only a generic
  REBUILD_FAILED message; it reports neither the failing stage/resource nor
  the last completed checkpoints. The plan requires immediate stop, preservation
  of partial operations and no automatic cleanup masking failure; details repeat
  that requirement. The library itself correctly stops without rollback.
* Reproduction: a file-free mocked workspace/backend run of
  main(["--synthetic-local"]) failed at verify:seed, entered workspace cleanup
  on the RebuildError, returned 1, emitted no stdout and printed only
  "REBUILD_FAILED: local checkpoint failed; no Azure operation was attempted".
  No real workspace was created by this reproduction.
* Impact: a genuine local operation/readback failure discards the database
  needed to inspect partial state while withholding even a safe checkpoint
  trace. Operators cannot distinguish the failed contract or inspect persisted
  witnesses. A nonzero exit is correct but does not fulfill the explicitly
  promised diagnostic/preservation behavior.
* Destination: rpi-implement.
* Smallest useful next action: in later implementation, preserve a safely
  inspectable, exclusively owned failed-rehearsal artifact and sanitized
  checkpoint identifier, without exposing raw exceptions or arbitrary cleanup
  paths. Add CLI failure tests proving partial evidence survives and subsequent
  stages/deletes do not run. Successful disposable cleanup can remain.

## Defects

* RV-001: medium implementation defect in the CLI failure path, routed only to
  later rpi-implement. No fix is made during this Review.

## Routed Findings

| Finding | Destination | Owner or next action | Reason for route |
| --- | --- | --- | --- |
| RV-001 | rpi-implement | Parent schedules failure-evidence preservation and regression tests in later implementation | Fits current accepted no-cloud contract; no source-scope decision or research gap. |

Later implementation of this finding does not require another Review.

## Residual Work

* The canonical plan follow-up remains a separate owner-selected Azure adapter/
  disposable-environment task. Existing deployment/SQL/auth/staff helpers,
  exact resource preservation/destruction and retention/tenant permissions must
  be addressed there, not by executing cloud operations in this Review.
* All four #148 criteria remain Partial: real checked scripted rebuild/no-secret
  argv integration; dependency teardown/budgets/empty cloud inventory; real
  synthetic seed/staff reconciliation; disposable Azure dry-run/rebuild evidence.
  Local contracts, SQL fixture checks and dry-run are useful but insufficient.
  No issue box is ticked; Refs #148 remains appropriate.

## Blockers and Remaining Work

* Review blockers: none.
* Remaining active plan markers: none; completion claims describe authored work,
  not defect-free acceptance. RV-001 is routed later work.
* No user decision is required for independent authoring or this handoff.
  Inventory/retention/tenant approvals remain outside scope.
* Publication: no commit, push, gate receipt, hosted checks, human approval or
  live acceptance is established by this source review. No heavy gate was run.

## Validation Evidence

| Command or assessment | Scope | Status | Summary |
| --- | --- | --- | --- |
| Parent-reported full orchestrator unittest discovery with core test support and supplied venv | src/orchestrator | Passed, supplied evidence only | 68 tests, zero skips, recorded in changes and caller context; not independently rerun. |
| Parent-reported Ruff check/format and mypy | Whole orchestrator project | Passed, supplied evidence only | Strict mypy 14 files; earlier failures and dependency restoration preserved in changes. |
| python3 -B inline unittest harness loading only the two supplied Python files | 16 file-free cases from test_rebuild.py | Passed, independently executed | Exact sequencing/failure stops, dependency order, scope/safety, inventory drift/bounds, empty recheck and dry-run/argument cases. No installed-package, SQLite filesystem or whole-project validation claim. |
| First inline harness attempt | Same bounded subset | Failed, harness-only | 15 cases passed; dry-run patch resolution lacked namespace package registration. Corrected isolated namespace registration and reran all 16 successfully; not a product failure. |
| python3 -B inline mocked main failure reproduction | CLI failure lifecycle | Confirmed RV-001 | verify:seed failure invokes workspace exceptional cleanup and leaves generic diagnostic only. Backend and workspace mocked; no files created. |
| git diff --check | Tracked candidate documentation and review whitespace | Passed | No whitespace errors; new source also read directly because untracked files are not included by git diff. |
| Source/diff/link comparison | Supplied artifacts and both runbooks | Complete | Source-only labels, stable markers, dispositions and residual work reconciled; historical runbook retained. |
| Full filesystem/local SQLite/installed CLI repetition | Existing parent evidence | Skipped | Not needed to duplicate the reported suite; current review avoids temporary filesystem operations and writes only this record. |
| Azure, tenant, secrets/private datasets, real model/application checks, heavy gate | Excluded boundary | Skipped | Explicitly unauthorized or disallowed; no cloud fallback, acceptance inference or second Review. |

## Outcome

* Outcome: Not accepted
* Outcome rationale: review execution is complete and the scope narrowing is
  justified, but RV-001 leaves a material failure-evidence requirement unmet.
  This verdict concerns the authored local CLI contract, not the intentional
  absence of an Azure adapter. Whole-issue acceptance independently remains
  partial by design; it is not demanded as a condition of this Review.
* Severity summary: 0 Critical, 0 High, 1 Medium, 0 Low defects.

## Closeout Routing Record

| Finding class | Destination | Owner or next action |
| --- | --- | --- |
| Implementation defect | rpi-implement | Parent owns later RV-001 correction with failure-path evidence. |
| Decision gap or invalid assumption | None | No unresolved authoring decision. |
| Material evidence gap | None | No missing evidence prevents the bounded verdict. |
| Non-blocking residual work | Distinct authorized Azure integration follow-up | Owner selects later scope and obtains live approvals. |

* Execution status: Complete
* Outcome: Not accepted
* Validation coverage: independent 16-case file-free subset and failure-path
  reproduction; supplied 68-test/zero-skip and Ruff/format/mypy evidence.
* Blockers: none to Review completion; RV-001 remains for later implementation.

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/research/2026-10-27/rebuild-148-research.md](.copilot-tracking/research/2026-10-27/rebuild-148-research.md) | Supplied research and partial issue mapping |
| [.copilot-tracking/plans/2026-10-27/rebuild-148-plan.md](.copilot-tracking/plans/2026-10-27/rebuild-148-plan.md) | Canonical completed markers and follow-up |
| [.copilot-tracking/details/2026-10-27/rebuild-148-phase-details.md](.copilot-tracking/details/2026-10-27/rebuild-148-phase-details.md) | Sequencing, safety and failure contracts |
| [.copilot-tracking/reviews/plans/2026-10-27/rebuild-148-plan-critique.md](.copilot-tracking/reviews/plans/2026-10-27/rebuild-148-plan-critique.md) | Preserved original critique |
| [.copilot-tracking/changes/2026-10-27/rebuild-148-changes.md](.copilot-tracking/changes/2026-10-27/rebuild-148-changes.md) | Implementation and validation evidence |
| [src/orchestrator/src/zava_forward/orchestrator/rebuild.py](src/orchestrator/src/zava_forward/orchestrator/rebuild.py) | Reviewed engine and local adapter |
| [src/orchestrator/tests/test_rebuild.py](src/orchestrator/tests/test_rebuild.py) | Reviewed external regression tests |
| [infra/README.md](infra/README.md) | Changed runbook and unchanged historical sequence |
| [src/orchestrator/README.md](src/orchestrator/README.md) | Component commands and evidence boundaries |
| [.copilot-tracking/reviews/logs/2026-10-27/rebuild-148-review.md](.copilot-tracking/reviews/logs/2026-10-27/rebuild-148-review.md) | Canonical one-Review result |

## Next Steps

Return this record to the active parent for later rpi-implement handling of
RV-001. No user action or second Review is required. Keep Azure integration and
its approvals in the distinct follow-up; do not infer acceptance or deploy.
