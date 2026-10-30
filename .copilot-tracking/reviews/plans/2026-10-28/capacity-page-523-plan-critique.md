---
title: Capacity page 523 final-candidate plan critique
description: One-pass assessment of test ownership, safety, acceptance coverage and readiness
ms.date: 2026-10-28
---

## Metadata

* Task ID: #523, capacity-page-523
* Critique date: 2026-10-28
* Plan: .copilot-tracking/plans/2026-10-28/capacity-page-523-plan.md
* Phase details: .copilot-tracking/details/2026-10-28/capacity-page-523-phase-details.md
* Critique execution status: Complete
* Assessment: Exactly one final-candidate critique; no implementation or validation execution.

## Inputs and Criterion Boundary

* Caller requirements: ordered Research, Plan, Implement and Review; local SQL-backed generated-demo reproduction; regression and browser coverage; other manager pages; no Azure, secrets, environment files or private datasets.
* Inputs: the supplied plan, phase details and research, including C1-C7; issue #523 title/body; relevant appointment/procurement projection, route error handling, procurement API fixtures, inherited SQL Server fixture, existing procurement browser check and local gate configuration.
* Repository context: docs/case_study_48_original.md, docs/case_study_48_addendum.md, docs/reference/README.md, docs/reference/memory.md and docs/reference/research/sector/housing-association-primer.md, read selectively for this bounded technical assessment.
* Dependencies: P01 before meaningful seeded capacity success checks; P02 before error/retry checks; explicit heavy-resource coordination and nonblocking admission before SQL Server, browser or full-gate execution. PID 4053825 ownership is supplied intake evidence, not a current lock probe.
* Decisions: optional null projection rather than fabricated authority; existing route retry; no generator rewrite or deployment. SQLite source reproduction does not establish real SQL Server or live-site causality.
* Assessment boundary: planning credibility and source-supported gaps, not completed acceptance, fresh runtime proof, accessibility conformance or publication approval. No heavy checks, polling, foreign resource reuse, private data reads or source edits were performed.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| C1-C4, C7 / root cause / P01-T01 | Covered | Recorded generated-980-case SQLite traceback matches direct contract_version indexing; actual live causality remains unverified. |
| C5 / authority safety / P01-T01 | Covered | Null projection and rejected appointment write are explicit; _contract_authority already requires a truthy version. |
| Regression ownership / P01-T01 | Covered | ProcurementApi owns canonical cases; JsonProcurementApi and MssqlProcurementApi inherit them. No parallel test hierarchy is needed. |
| SQL-backed generated demo / P02-T01, P03-T01 | Partial | Generated browser setup is proposed and runtime block is explicit; inherited SQL fixture destruction needs a safe ownership boundary, PC-002. |
| C6 / plain-language failure and retry / P02-T01 | Partial | Both 503s and retry are planned; transport, structured errors, cancellation and session-expiry assertions are unspecified, PC-004. |
| Empty states / P01-T01, P02-T01 | Covered | Known-empty API tests, empty browser data and explicit no-packages state complement existing no-work-orders rendering. |
| Other manager pages / P02-T01 | Partial | Adjacent navigation is not a defined acceptance inventory or result matrix, PC-003. |
| Validation and check ownership / P03-T01 | Partial | New browser check has no exact invocation or gate execution path, PC-005. |
| Ordered Review and publication / P03-T02 | Partial | Explicit publication block is sound; blanket deferral of review findings and missing post-gate exact-head assessment need correction, PC-001. |
| Live verification / follow-up | Covered | Owner-owned pending verification is allowed by the issue; no deployment or live closure is implied. |

## Verdict

* Verdict: Revise
* Rationale: The bounded source repair is credible and implementation need not wait for heavy admission. Five direct planning corrections are required to make safety, acceptance and final review enforceable. Publication remains Blocked without real SQL Server, browser and complete exact-head gate evidence; a passing planning assessment would not clear those gates.
* Severity counts: Critical 0; High 2; Medium 3; Low 0.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: Review findings cannot be deferred indiscriminately before publication

* Related IDs: P03-T02; ordered RPI; publication readiness.
* Evidence: .copilot-tracking/details/2026-10-28/capacity-page-523-phase-details.md, P03-T02 says "route findings to later work, never claim closure in this task." It places one independent review before commit/gate, without explicitly assigning independent exact-head assessment after receipt verification. src/README.md, Local RPI gate, requires retained original Review evidence, final commit/gate and verification immediately before independent exact-head review and push.
* Concern: The blanket deferral includes defects introduced by this repair and unmet acceptance criteria. One pre-commit review does not establish assessment of the final gated commit.
* Impact: An actionable correctness or safety defect could survive the stated workflow, or an amended candidate could be published without independent final-head assessment.
* Smallest useful change: Preserve the original one-pass Review unchanged, but classify its findings. Fix in-scope blocking defects before eligibility; defer only explicitly nonblocking/out-of-scope work with rationale. After the final implementation/evidence commit, full gate, refreshed main and receipt verification, require independent assessment of that exact head. Any subsequent correction invalidates the gate and requires fresh gate/verification. This does not request another plan critique.
* Action owner: Planning parent; implementation/review coordinator executes the corrected sequence.
* Exact resolving evidence: Revised P03-T02 specifies finding disposition and both review boundaries. Later publication evidence names reviewed HEAD/base, retained original findings, dispositions, full receipt and final exact-head assessment; until then publication is blocked.
* Decision route: Direct planner correction. Existing user direction already requires the gates; no user decision is needed.

<!-- rpi:critique id=PC-002 -->
### PC-002 [High]: Inherited SQL tests have a destructive setup outside the stated browser safety guard

* Related IDs: Test Ownership; P01-T01; P02-T01; P03-T01; local SQL safety.
* Evidence: src/api/tests/test_mssqlstore.py defines MssqlProcurementApi.make_store with wipe() before factory(). wipe() drops tables/triggers using ambient ZF_SQL_* configuration. The module explicitly assumes a database that may be wiped. The plan selects these inherited tests, while the phase-details loopback/no-existing-DB-wipe rule is stated only for browser mode.
* Concern: ZF_TEST_MSSQL=1 is opt-in, not proof of disposable ownership. Even loopback alone does not distinguish an existing local database from an issue-owned disposable one.
* Impact: A later admitted test invocation could destroy unrelated local data, violating the generated-data-only boundary.
* Smallest useful change: State that inherited real-SQL tests run only through an owned, freshly created disposable SQL resource with newly constructed local connection settings, never ambient or pre-existing database configuration. Apply that ownership rule to browser SQL mode too. Record resource identity and cleanup ownership; do not broaden scope to repair the shared harness.
* Action owner: Planning parent; validation executor owns resource admission and isolation.
* Exact resolving evidence: P03-T01 and the browser setup contract name the disposable-resource invocation/ownership checks and reject existing targets before any wipe. Future execution records owned local target creation, nonblocking admission and cleanup, without connection secrets. No SQL run is authorized by this critique.
* Decision route: Direct planner correction; no user decision or permission to reuse foreign resources.

<!-- rpi:critique id=PC-003 -->
### PC-003 [Medium]: Other-manager-page acceptance lacks a bounded inventory and pass criteria

* Related IDs: Other manager pages acceptance criterion; P02-T01; P03-T01.
* Evidence: The plan says "manager navigation" and phase details say "adjacent navigation checks." Issue #523 requires checking other manager pages and recording results. src/api/src/zava_forward/api/web/app.js routes manager workspaces beyond capacity, and ops.js also exposes a separate work-order read.
* Concern: Neither which pages are covered nor what establishes success is defined. Clicking one adjacent link could satisfy the task prose without testing the requested manager surface or recording shared-failure results.
* Impact: The existing work-order projection defect could be fixed on capacity while acceptance evidence omits another affected route, or a route could render a heading while its data request fails.
* Smallest useful change: Define the check inventory from the generated manager's actual navigation plus identified shared work-order consumers; record route, expected heading/content or legitimate empty state, relevant request outcome and console/page errors. Exclude mutation/deployment actions. Record additional failures without silently repairing unrelated pages, and distinguish unchecked routes from passing ones.
* Action owner: Planning parent; browser-check implementer owns assertions and the validation executor owns results.
* Exact resolving evidence: P02/P03 specify the route-inventory rule and per-route assertions; the later changes/Review evidence contains a route result matrix, with blocked/unperformed entries until admitted browser execution occurs.
* Decision route: Direct planner correction; user scope already requests these checks.

<!-- rpi:critique id=PC-004 -->
### PC-004 [Medium]: The planned 503 cases do not prove the full scoped-error preservation contract

* Related IDs: Functional and non-functional requirements; P02-T01; C6.
* Evidence: Phase details require preserving actionable server messages, cancellation and session expiry, but explicitly schedule only each endpoint's injected 503 and successful retry. src/api/src/zava_forward/api/web/app.js:28-37 distinguishes fetch rejection, unstructured response fallback, structured data.error, abort checking and 401 login. Its route catch also relies on signal/me state and error.reloadWorkspace.
* Concern: A generic 503 fixture can exercise only one of these paths. Broad error wrapping could expose transport jargon, discard useful server text/properties, or replace a legitimate session/navigation transition.
* Impact: The repair can pass its stated browser cases while violating the very existing behavior it promises to preserve.
* Smallest useful change: Add bounded assertions in the new browser harness for each endpoint's unstructured 503 and successful retry; include transport rejection with friendly context, a structured actionable error retained with context, session expiry returning to login, and navigation abort without a stale capacity error. Preserve original error identity/properties where relevant. These are scenario additions, not extra canonical procurement test methods.
* Action owner: Planning parent; browser-check implementer.
* Exact resolving evidence: Revised P02-T01 names the scenarios and expected outcomes; future admitted browser output demonstrates them. Source-only inspection or mocked backend unit success is not a browser result.
* Decision route: Direct planner correction; no user decision.

<!-- rpi:critique id=PC-005 -->
### PC-005 [Medium]: A new browser file is not automatically executed by the complete gate

* Related IDs: Test Ownership; directly related API guide; P03-T01; P03-T02.
* Evidence: The plan proposes one new check under src/api/checks but names neither its module nor executable command. tools/rpi-checks.py constructs browser commands explicitly for design_system_browser_check and regulatory_ux_check; it does not discover arbitrary new check files. src/api/checks/procurement_browser_check.py is an existing separately invoked pattern.
* Concern: "Full gate" can pass without running the issue-specific seeded capacity/error/navigation check. The plan also lists a related API guide in scope without assigning the check invocation/documentation work.
* Impact: A tracked browser file could be delivered but never exercised on the candidate used for acceptance, making the receipt appear stronger than its actual coverage.
* Smallest useful change: Assign a stable check module and exact repository-supported invocation, including fixture imports and explicit SQLite versus disposable real-SQL modes. Document it in src/api/README.md. Require a separate admitted exact-candidate run/result alongside the unchanged full gate, or deliberately wire it into an existing invoked harness; do not imply automatic discovery or casually expand gate tooling scope. Specify the requested API discovery command and targeted lint/type selectors as well.
* Action owner: Planning parent; check implementer and validation executor.
* Exact resolving evidence: P02/P03 identify the executable entry point, modes, command selectors and evidence owner. Later candidate evidence records the specific check's real exit/result and tested HEAD; full receipt alone is insufficient.
* Decision route: Direct planner correction; no user decision.

## Strengths and Residual Risk

* The read compatibility change is surgical: _appointment_binding reads an absent legacy field optionally, consistent with package projection, without inventing contract authority or rewriting seed data.
* The regression belongs in the existing ProcurementApi ownership hierarchy, retaining JSON, SQLite and opt-in real-SQL inheritance. The proposed three-method ceiling need not prevent browser scenario coverage.
* Testing absent-key package/order reads, null binding, Unknown status and rejected write usefully separates visibility from authorization.
* Explicit empty-package rendering and reuse of the existing Try again control avoid unrelated visual or retry-system changes.
* The research correctly distinguishes the concrete generated SQLite reproduction from unverified live-site causality.
* The recorded foreign-lock block, prohibition on polling/reuse, no-cloud fallback and pending-owner live verification are correct boundaries, not findings to weaken.

## Questions or Blocking Evidence Gaps

* No significant or divergent user decision is needed for PC-001 through PC-005.
* Real SQL Server generated-demo reproduction, browser/manager-page results, complete local gate and final receipt/assessment remain unavailable. They block publication and acceptance claims, not this completed plan critique.
* Resume heavy work only after an explicit coordination event and successful nonblocking admission. No observation in this critique changes the intake lock disposition.

## Limitations

* C7 is supplied research evidence, supported by inspected source; this critique did not rerun or independently reproduce it.
* The issue body was read, not cloud resources or deployment state. No live verification, SQL execution, browser launch, scanner, gate, test run or lock polling occurred.
* Web implementation and its fresh guidelines/accessibility review remain later-stage responsibilities. This is not a standalone UI audit.
* Existing untracked plan/research/session inputs were preserved. Only this caller-specified critique artifact was added.

## Recommended Next Action

* Highest-impact finding: PC-001.
* Action owner: Planning parent.
* Smallest next action: Correct P03-T02's review-finding disposition and final exact-head review sequence, then dispose PC-002 through PC-005 directly in the same planning finalization.
* User response required: No.
* Stop: Return this one complete finding set to the parent; do not run another plan critique or begin implementation here.

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/plans/2026-10-28/capacity-page-523-plan.md](.copilot-tracking/plans/2026-10-28/capacity-page-523-plan.md) | Assessed final-candidate plan |
| [.copilot-tracking/details/2026-10-28/capacity-page-523-phase-details.md](.copilot-tracking/details/2026-10-28/capacity-page-523-phase-details.md) | Assessed phase details |
| [.copilot-tracking/research/2026-10-28/capacity-page-523-research.md](.copilot-tracking/research/2026-10-28/capacity-page-523-research.md) | Supplied reproduction and source evidence |
| [.copilot-tracking/reviews/plans/2026-10-28/capacity-page-523-plan-critique.md](.copilot-tracking/reviews/plans/2026-10-28/capacity-page-523-plan-critique.md) | Complete one-pass finding set |

## Next Steps

The active planning parent corrects and disposes PC-001 through PC-005 without another critique, then finalizes the bounded implementation handoff. No user action is required. Publication remains blocked until real SQL/browser evidence and the full exact-head gate, receipt verification and independent assessment are actually complete.
