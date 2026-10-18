<!-- markdownlint-disable-file -->
---
title: Issue 75 building SQL final-candidate plan critique
description: One independent bounded credibility assessment before implementation
ms.date: 2026-10-18
---

## Metadata

* Task ID: jmservera/ama#75.
* Critique date: 2026-10-18.
* Plan: .copilot-tracking/plans/2026-10-18/issue-75-building-sql-plan.md.
* Phase details: .copilot-tracking/details/2026-10-18/issue-75-building-sql-phase-details.md.
* Research: .copilot-tracking/research/2026-10-18/issue-75-building-sql-research.md.
* Critique execution status: Complete.
* Frozen branch: test/building-sql-conformance-75.
* Observed HEAD and supplied base: 9d625a09e34491ecf9fd27ffc7d59e67c2373b29.
* Execution count: one original critique; no second pass or implementation.
* Write boundary: this artifact only. Existing untracked plan, details, research
  and session state are caller-owned inputs and were not modified.

## Inputs and Criterion Boundary

The supplied plan, details, research and current caller constraints are the
requirements authority. Read the required original case study, addendum,
reference index and memory for context, not as a grant of operational authority.
Inspected the named reusable fixture, core/API building tests, MSSQL harness,
SQL store/dialect, linked procurement/resident/quality contracts, API setup,
document-store/scanner selectors, API project configuration and named CI
workflows. No open-ended external research or private dataset inspection.

Acceptance boundary:

* A1: Full constructed shared record and separate home allocations/evidence
  survive close, seed deletion and reopen, without allocation leakage.
* A2: Distinct raw SQL sessions see committed holds; stale shared-document
  writes conflict and an independent reader confirms the exact winning record.
* A3: Matching progression, issue and reissue refuse without mutation, while
  the other package and unaffected sibling remain usable.
* A4: Building clearance cannot supply missing resident, funding, technical or
  QA approval.
* A5: Finance-capable, non-Finance staff and Contractor HTTP projections run
  against SQL, retaining existing denial and data-separation behavior.
* A6: Task-owned disposable SQL is actually executed and cleaned up; skips
  remain Not run. Local focused regressions, configured lint/type checks and
  migration checks remain required.

The existing fixture and MSSQL factory/wipe are mandatory reuse points. The
locked executable/documentation targets, no-removal rule, maximum two classes,
five semantic methods plus three inherited HTTP tests and one fixture helper
remain binding. No new service, generated target, production change absent an
attributable real-SQL failure, sensors/issue110, private support/.env/data, mvp
implementation, Azure/Graph/IAM, external network/spend or real AI is authorized.

Preserve PR398 governance at the frozen base. Operational update rights,
allocation policy, human/accessibility acceptance and live-application evidence
remain separate gates. The parent must disposition this single critique, then
implement, retain one original Review, and publish only a draft with Refs #75.
The critique does not execute or authorize those later stages.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| Research C2-C6; P01-T01 reuse and ownership | Covered with correction | Existing fixture/factory are appropriate; failure-path ownership needs PC-004. |
| A1; first semantic case | Covered | Nonempty dependency, full payload equality and physical seed deletion are explicitly planned. |
| A2; second semantic case | Covered | Local lock retains stale snapshot; independent winner commit and third reader are explicit. |
| A3; third semantic case | Partial | Correct refusal cause and orthogonal home/package controls need PC-001 and PC-002. |
| A4; fourth and fifth semantic cases | Partial | Independent missing prerequisites and QA states are planned; refusal-cause assertions need PC-001. |
| A5; inherited HTTP class | Covered with correction | Existing three tests cover role projections and loopback behavior; PC-003 and PC-004 protect execution fidelity. |
| A6; P02-T01 | Partial | Unique SQL ownership and skip semantics are explicit; environment/path isolation and cleanup need PC-003 and PC-004. |
| P02-T01 regressions and configured checks | Covered | Core/API module selections, cwd disambiguation, Ruff, format, mypy and migration command are named. |
| P03-T01 publication and original Review | Covered | Single original Review, adverse evidence retention, draft main PR and non-closing reference are explicit. |
| Scope, dependencies and PR398 continuity | Covered | Exact base, dependency290 status and independent human/live gates are retained. |
| Image/browser/a11y applicability | Covered within boundary | Unchanged image/runtime inputs permit documented redundant/not-applicable checks, not a fresh accessibility or live-app acceptance claim. |

## Verdict

* Verdict: Revise.
* Severity summary: 0 Critical, 2 High, 2 Medium, 0 Low.
* Rationale: The test-only strategy and acceptance mapping are credible, but
  the final candidate leaves an externally configured document-write path
  unbounded and permits weak negative/scoping evidence. Resource ownership
  also needs an executable failure-path contract before implementation.
  All four changes fit the existing locked targets and test budget.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: Require the intended gate, not merely an exception

* Related IDs: A3, A4, research C3, P01-T01 semantic cases three through five.
* Evidence: .copilot-tracking/details/2026-10-18/issue-75-building-sql-phase-details.md:48-56
  specifies refusal/state preservation but no cause assertion.
  src/core/tests/test_buildings.py:104-112 supplies a tempting reuse pattern
  whose negative issue/reissue calls omit resident_bindings.
  src/core/src/zava_forward/core/procurement.py:385-387 and :430-432 check
  resident clearance before building clearance.
  src/core/src/zava_forward/core/resident_decisions.py:324-332 rejects empty
  bindings. src/core/src/zava_forward/core/store.py:504-519 also has several
  distinct progression refusal paths.
* Concern: Replaying that negative pattern on SQL can pass because resident
  scope is missing even if building instruction blocking is broken. Broad
  GateError/ValueError checks also do not prove which independent home or QA
  prerequisite caused refusal. This is a planning specificity gap, not a
  claim that unimplemented tests already contain the bug.
* Impact: A green SQL suite could fail to demonstrate the central building
  hold and independent-approval requirements.
* Smallest useful change: Require valid explicit resident bindings on every
  A3 issue/reissue call, including expected failures; assert the returned
  building/hold reason rather than exception type alone. For A4 assert the
  corresponding missing resident/funding/technical reason in each subcase and
  the unaccepted-QA transition reason for handover, using otherwise valid actor,
  scope and supplied prerequisites. Preserve existing unchanged-state checks.
  When asserting the matching issue while an order already exists, require
  the building reason rather than duplicate-order refusal.
* Action owner: Planning parent for P01-T01 details; implementer for assertions.
* Exact resolving evidence: Revised P01-T01 names the explicit binding payload
  and expected cause for each negative operation. The eventual five-method SQL
  suite shows matching Building SYN-B1/hold refusal and each distinct home/QA
  reason, with no resident-scope-unknown fallback for A3 and unchanged durable
  case/order state. These refinements need no additional test methods.
* Decision route: Direct planner correction. No significant/divergent user
  decision and no runtime fix is authorized by this finding.

<!-- rpi:critique id=PC-002 -->
### PC-002 [Medium]: Make the sibling control isolate home scope from package scope

* Related IDs: A3, research C2-C3, P01-T01 third semantic case.
* Evidence: .copilot-tracking/details/2026-10-18/issue-75-building-sql-phase-details.md:48-51
  names an other-package target and a sibling without specifying the sibling's
  package. src/core/tests/building_fixture.py:110-120 scopes HOLD-1 to ZF-2
  and PKG-SHARED. The supplied core example at
  src/core/tests/test_buildings.py:129-138 issues the sibling in PKG-OTHER.
* Concern: If both positive examples use PKG-OTHER, neither establishes that
  the same held package is still usable for a nonmatching home. A regression
  that ignores case_ids while respecting package_ids could pass both controls.
* Impact: The planned evidence does not unambiguously prove both dimensions
  of the required home/package isolation.
* Smallest useful change: Specify the matrix inside the existing third method:
  ZF-2/PKG-SHARED refuses; ZF-2/PKG-OTHER issues and reissues successfully;
  ZF-3/PKG-SHARED issues, books using supplied_appointment_fixture and advances
  to Install booked while the hold remains open. Retain independent-read and
  no-mutation assertions.
* Action owner: Planning parent for the explicit matrix; implementer for SQL
  assertions.
* Exact resolving evidence: Revised P01-T01 and the implemented third method
  identify those exact home/package pairs, retain HOLD-1 on the independent
  reader, and demonstrate successful same-package sibling progression on SQL.
  No new class, semantic method or fixture edit is needed.
* Decision route: Direct planner correction; current caller direction already
  requires the unaffected sibling and package to remain usable.

<!-- rpi:critique id=PC-003 -->
### PC-003 [High]: Explicit SQL settings do not isolate document writes or scratch paths

* Related IDs: A6, research C2/C7, P01-T01 helper, P02-T01 environment/cleanup.
* Evidence: .copilot-tracking/details/2026-10-18/issue-75-building-sql-phase-details.md:80-87
  specifies ZF_SQL_* and no inherited dataset, but does not define the other
  environment selectors or workspace scratch root.
  src/core/tests/building_fixture.py:132 invokes supplied_contract_fixture;
  src/core/tests/dataset.py:63-69 writes constructed document bytes through
  store.docstore.put.
  src/core/src/zava_forward/core/sqlstore.py:166-170 uses ambient document,
  scanner and digest configuration.
  src/core/src/zava_forward/core/documents.py:202-210 selects ambient ZF_DOC_DIR
  or azure-blob; src/core/src/zava_forward/core/doc_controls.py:94-101 selects
  the scanner. src/api/tests/test_buildings.py:23 uses TemporaryDirectory with
  the process default root.
* Concern: Not sourcing .env does not prevent inherited ZF_DOC_STORE,
  ZF_DOC_DIR or related settings from routing fixture writes to external or
  private storage. Inherited auth settings can also invalidate the claimed
  password HTTP replay. Default TemporaryDirectory can write outside the
  allowed project workspace even when SQL itself is disposable.
* Impact: A synthetic local SQL run can violate the no-Azure/private-data
  boundary or fail for unrelated configuration; default scratch paths violate
  the caller's file-operation constraints.
* Smallest useful change: Specify an allowlisted/sanitized subprocess
  environment for all local validations, not only actual SQL. Force local
  document store/scanner, workspace-owned document/digest paths, synthetic
  password auth/non-production settings, and disable/remove external AI,
  identity, blob and private path overrides. Do not inspect or print their
  previous values. Set TMPDIR to a task-owned directory beneath this worktree
  before Python starts so unchanged inherited fixtures use it. Bind every
  destructive SQL invocation to the just-created database/container, never an
  inherited target. Keep credentials out of commands/logged evidence.
* Action owner: Planning parent for P02-T01 execution contract; implementer
  for the local invocation and bounded README command.
* Exact resolving evidence: Revised P02-T01 states the concrete safe selectors
  and workspace scratch root. Execution evidence records sanitized settings
  by safe key/value only, selected local document backend, actual scratch path,
  unique SQL database/container identity and cleanup; no inherited secret or
  private path is disclosed. Source inspection confirms fixture document writes
  remain local. No generated committed runner or new service is required.
* Decision route: Direct planner correction enforcing existing restrictions;
  no significant/divergent user decision.

<!-- rpi:critique id=PC-004 -->
### PC-004 [Medium]: Reuse needs cleanup ownership before fixture and HTTP setup can fail

* Related IDs: A6, P01-T01 helper/HTTP replay, P02-T01 cleanup.
* Evidence: .copilot-tracking/details/2026-10-18/issue-75-building-sql-phase-details.md:34-36
  says register db.close at creation, but passes the bare existing factory to
  open_store. src/core/tests/building_fixture.py:128-134 constructs the store
  and then executes fallible contract/capacity initialization before returning
  it. src/api/tests/test_buildings.py:22-56 creates scratch/store/server/thread
  in setUp and owns cleanup only in tearDown. unittest does not invoke
  tearDown after a failed setUp. src/api/tests/test_mssqlstore.py:31-36 also
  leaves the wipe connection without explicit close.
* Concern: Cleanup registered only after open_store or parent setUp returns
  cannot protect failures during fixture initialization or HTTP startup.
  The scoped patch is appropriate, but it must restore on those failures too.
  Finally removing the container does not itself close client handles or
  release a bound HTTP server in the test process.
* Impact: The failure most useful for conformance diagnosis can leave a SQL
  session, scratch files or loopback server behind, contaminate subsequent
  tests, or obscure the original failure.
* Smallest useful change: Use the allowed local helper to wrap the existing
  factory and register store closure immediately after construction, before
  unchanged fixture initialization continues. Specify exception-safe patch
  restoration and partial parent-setUp cleanup in the new HTTP subclass,
  respecting the parent's normal successful teardown without unsafe duplicate
  shutdown or joining an unstarted thread. Close the short-lived wipe
  connection in finally within the existing wipe function. Keep cleanup local
  to test_mssqlstore.py; do not rewrite shared fixtures or generalize a service.
* Action owner: Planning parent for the lifecycle detail; implementer for the
  bounded helper/subclass and wipe connection closure.
* Exact resolving evidence: Revised P01-T01 states cleanup registration order
  and partial-setup ownership. Implemented diff shows the store is registered
  before supplied_contract_fixture/set_capacity, patches restore on exceptions,
  partial HTTP resources close in reverse acquisition order, and wipe's
  connection closes on both success and failure. A contained local fault probe
  or equivalent recorded lifecycle trace demonstrates setup failure does not
  leave a listening server or open owned connection; normal eight-test SQL
  selection still completes and final container absence is verified. The probe
  need not add a committed test method beyond the locked budget.
* Decision route: Direct planner correction. This is tightly coupled test
  ownership, not authorization for unrelated harness refactoring.

## Strengths and Residual Risk

* Reusing building_fixture.open_store preserves current contract delegation,
  commitment evidence and capacity setup. Replacing only its looked-up SqlStore
  symbol in a scoped patch is materially better than duplicating seed logic.
* The A1 seed deletion and A2 third independent winner read exceed a superficial
  in-process replay. _SyncLock synchronizes on outermost entry rather than
  holding a database transaction, so the planned stale-snapshot technique is
  consistent with the supplied store contract.
* Existing BuildingHttpTests has exactly three methods. It reads the assistant
  registry rather than invoking real AI. Import its API module via a module
  alias, not an exposed TestCase alias that unittest may rediscover; retain
  API-before-core test search paths. The planned cwd disambiguation is important
  because core and API both contain test_buildings.py.
* The opt-in guard, absence of fake-SQL fallback, exact frozen base, documented
  image redundancy and no-new-runtime default are appropriate.
* Real SQL availability, driver readiness and actual assertions remain future
  execution evidence, not established results. An attributable real-engine
  failure requires recorded disposition before any production amendment.
* PR398 and all operational rights/allocation/human/a11y/live-app gates remain
  separate. No critique advice changes those rights or promotes synthetic
  conformance into operational acceptance.

## Questions or Blocking Evidence Gaps

None requiring a user answer. All findings are directly resolvable by the
planning parent within the confirmed direction. No new research lane or
second critique is requested.

## Limitations

* This is a source-grounded final-candidate plan assessment, not execution of
  the proposed tests. No dependency restoration, SQL/container operation,
  implementation, lint/type/migration run, commit, push or PR operation was
  performed.
* External issue/dependency/PR metadata was considered as supplied research
  provenance, not freshly fetched or revalidated.
* No private support, .env, configured dataset or mvp implementation was read.
* No broad repository audit, security review, live-app or accessibility
  acceptance was undertaken.

## Recommended Next Action

* Highest-impact finding: PC-003.
* Action owner: Planning parent.
* Smallest next action: Record dispositions for PC-001 through PC-004, then
  revise P01-T01/P02-T01 to make negative controls, scope matrix, environment
  isolation and failure cleanup explicit.
* User response required: No.
* After direct revisions, the active parent finalizes without another critique,
  implements within the locked scope, executes validation, preserves one
  original Review and publishes the authorized draft. This critique stops here.

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/research/2026-10-18/issue-75-building-sql-research.md](.copilot-tracking/research/2026-10-18/issue-75-building-sql-research.md) | Supplied bounded evidence and constraints |
| [.copilot-tracking/plans/2026-10-18/issue-75-building-sql-plan.md](.copilot-tracking/plans/2026-10-18/issue-75-building-sql-plan.md) | Assessed final-candidate plan, unchanged |
| [.copilot-tracking/details/2026-10-18/issue-75-building-sql-phase-details.md](.copilot-tracking/details/2026-10-18/issue-75-building-sql-phase-details.md) | Assessed phase details, unchanged |
| [.copilot-tracking/reviews/plans/2026-10-18/issue-75-building-sql-plan-critique.md](.copilot-tracking/reviews/plans/2026-10-18/issue-75-building-sql-plan-critique.md) | Original independent critique |

## Next Steps

Active planning parent: disposition and directly resolve PC-001 through PC-004,
then continue the authorized implementation and single original Review/publication
sequence. No user action or second critique is required.
