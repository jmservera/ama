---
title: Resident SQL fixture window independent Review
description: Original bounded independent Review for pr-479-resident-sql-fixture-window
ms.date: 2026-10-27
---

## Opening Review State

* Interpreted review goal: independently assess the November SQL fixture window correction without accepting the parent live resident work or pending publication.
* Review scope: P01 research and P02 implementation/validation; reconcile deliberately later P03 publication without executing it.
* Evidence readiness: one exact-slug dated research, plan, phase details, critique and changes set is present; source diff, new tests, unchanged SQL constraint and supplied external logs are available for comparison.
* Acceptance basis: owner requires an independent November SQL endpoint, unchanged December application cap and SQL constraint, same grep value, explicit worktree PYTHONPATH and scoped local evidence.
* First comparison boundary: reconcile current plan/detail/critique/change markers, then compare the two Python files and SQL/image import contract with actual supplied logs.
* Active read-only boundaries: write only this canonical Review record; no source/artifact mutation, delegation, repeated Review, Docker/full gate, commit, synchronization, push or thread mutation.
* Initial blockers: none identified before substantive comparison. Heavy lock execution is not needed for read-only evidence inspection.

## Scope and Evidence

* Task ID: pr-479-resident-sql-fixture-window.
* Review date: 2026-10-27.
* Assessment count: one original independent Review, performed directly without delegation.
* Assessed boundary: P01 implementation and completed P02 checks, including current planning, critique dispositions, import isolation, actual SQL insert regression and validation evidence. Reconcile P03 as pending active work, not completed publication.
* Research: .copilot-tracking/research/2026-10-27/resident-sql-fixture-window-research.md.
* Plan: .copilot-tracking/plans/2026-10-27/resident-sql-fixture-window-plan.md.
* Phase details: .copilot-tracking/details/2026-10-27/resident-sql-fixture-window-phase-details.md.
* Critique: .copilot-tracking/reviews/plans/2026-10-27/resident-sql-fixture-window-plan-critique.md.
* Changes: .copilot-tracking/changes/2026-10-27/resident-sql-fixture-window-changes.md.
* Source: complete tracked diff for src/api/checks/resident_demo_browser_check.py and complete new src/api/tests/test_resident_demo_check.py.
* Unchanged dependencies: infra/sql/resident-showcase.sql; src/api/checks/resident_demo_image_check.py; src/core/src/zava_forward/core/resident_showcase.py; relevant cap coverage in src/core/tests/test_resident_showcase.py and SQL fixture endpoints in src/core/tests/test_resident_showcase_sql.py; related resident sensor-check cap uses.
* Policy/context: src/README.md, Local RPI gate; required case-study original/addendum and knowledge-base index/memory read. No new regulatory, UX or live-service acceptance is assessed.
* External evidence supplied by the parent: fixture-red.log, fixture-api-resident-tests.log, fixture-core-tests.log and fixture-browser-image.log, under the parent session files directory identified in the changes record and task request. These are execution logs, not repository artifacts or publication receipts.
* Observed branch: chore/resident-live-acceptance, tracking origin/chore/resident-live-acceptance. Observed HEAD: 88c7e6bb2f0dd16e557a673328169185614183aa; local origin/main: 864a502126ee0dfedf13eaf54f08a10f2339279c. Neither reference was fetched or synchronized during Review.
* Candidate state: source correction modified and new test/artifacts untracked, as expected before P03. The image log reports the same HEAD, but that HEAD alone does not identify the uncommitted source bytes. This Review assesses the inspected working diff, not a clean committed publication candidate.

### Reviewed Source Fingerprints

SHA-256 values bind this read-only assessment to the inspected bytes; they are not a gate receipt.

| Workspace-relative path | SHA-256 |
| --- | --- |
| src/api/checks/resident_demo_browser_check.py | bafc5cc1f06135f02ef488c6ea2f92eb49db44164905e20ca13de3ce7b2eeee8 |
| src/api/tests/test_resident_demo_check.py | 10e9d7308176ac072db6e555ed84a3008dfaf4d7a56841901058d6420a7bb005 |
| infra/sql/resident-showcase.sql | 7621d6535debb2763d39d9e59d8f4e88df8d1584c6990f0dc42bedd32a69be15 |
| src/api/checks/resident_demo_image_check.py | 2896ca56254554c471aa0e6d479b0769a203ceabd65bc8cf1a9b2caf5b065242 |

## Execution Status

* Review execution status: Complete.
* Evidence: all five exact-slug dated input artifacts compared; complete two-file source boundary inspected; SQL constraint and shared image import inspected; supplied red/green, core, browser and image results examined; cheap read-only diff hygiene, related cap search and assertion counts checked.
* Implementation execution is separate: P01 is complete; P02 checks were complete at intake and this record supplies its original Review; P03 remains unexecuted by this reviewer.

## Plan-to-Change Reconciliation

| Current plan scope | Changes-record summary | Current-state reconciliation | Gap or rationale |
| --- | --- | --- | --- |
| P01 / P01-T01 | Independent SQL constant, lazy Playwright import, two behavioral tests | Reconciled | Both inserts use November 1 naive UTC; no SQL, image or application policy changes |
| P02 / P02-T01 | Red failures, unit results, lint/type report, real browser/image evidence; Review pending | Reconciled | Open checkbox correctly includes the not-yet-produced original Review at intake; this record completes that assessment, without mutating upstream artifacts |
| P03 / P03-T01 | Publication pending | Reconciled | No commit, pull/rebase, fresh candidate/base binding, push or thread-resolution completion is claimed |
| Follow-Up Items | Parent live SQL/secret renewal and credential-bearing acceptance blockers excluded | Reconciled | Not added to correction scope or implied cleared |

## Completed Work Assessment

| Related marker | Files | What changed and why | Completion evidence | Validation | Assessment |
| --- | --- | --- | --- | --- | --- |
| P01-T01 | src/api/checks/resident_demo_browser_check.py | SQL_AUTHORIZATION_END is explicitly November 1 UTC; only allowed_case insertion uses its naive conversion | Full diff and unchanged ck_allowed_case_window inspected | Actual insert-argument regression and real SQL-backed checks | Conformant; independent December application ceiling preserved |
| P01-T01 | src/api/checks/resident_demo_browser_check.py | Page imported only for type checking; sync_playwright imported in main; finite SQL window documented | Postponed annotations retained; shared image imports only fixture helpers | Fresh-process import blocker regression passes in supplied API log | Directly coupled import-isolation adjustment, not unrelated refactoring |
| P01-T01 | src/api/tests/test_resident_demo_check.py | Two tests, no removals: execute actual database setup/yield/cleanup with mocked SQL boundary; substitute January application cap; reject Playwright import in subprocess | Checks both resident insert calls, exact case IDs, exact start/end and valid ordering; checks DROP DATABASE and connection close; patches restore automatically | Both tests fail for the intended reasons in red log and pass in API log | Conformant; not a source-string proxy; preserves existing core ownership of application expiry semantics |
| P02-T01 | External execution logs named above | Focused resident API/core and real browser/image checks | Counts and terminal statuses inspected; browser/image completion and owned SQL cleanup present | API 108 with 7 skips; core 77 with 19 skips; browser 55 and image 22 assertions | Evidence supports the fixture-only correction, not universal SQL/browser coverage or live acceptance |

The same-value search confirms the pre-existing core SQL fixture uses
2026-11-01T00:00:00 and its constraint-rejection test covers a one-second-later
endpoint. Related sensor browser references are in-memory application-cap uses,
not another SQL-bound fixture requiring correction. The image harness still
imports database() from the changed shared module; its application expiry
continues to use min(current time plus one hour, rs.AUTHORITY_END).
The unchanged core cap test explicitly asserts 2026-12-31T23:59:59 UTC and is
reported passing in the supplied core log.

The fixture intentionally does not renew SQL authorization after November 1.
Its moving start and SQL/application admission controls may make later checks
fail closed; this is the accepted finite-window boundary, not a defect to fix
by extending the constraint.

## Implementation-Time Plan and Detail Update Assessment

| Affected marker | What changed and why | Triggering evidence and user decision | Reconciliation performed | Planning and critique state | Assessment |
| --- | --- | --- | --- | --- | --- |
| P01-T01 | Lazy browser import and two tests | Runtime-only discovery must not import optional Playwright; owner-approved dependency isolation | Plan, details and changes describe matching implementation and test ownership | Included in original critique coverage | No divergent decision |
| P01-T01 / P02-T01 | Direct core imports and import sorting in test | Ruff/mypy implementation-time diagnostics reported by parent and changes record | Final test imports use core modules directly; changes disclose initial failures and corrections | Within accepted direction; no material replanning needed | Reconciled; no hidden scope expansion |
| P02-T01 | Restore missing pinned tools in external environment | Missing-tool failures reported before restoration | Plan/details/changes agree; no manifest change in diff | Explicitly planned fallback | Conformant scope; raw tool transcript limitation below |
| P03-T01 | Fresh synchronized candidate checks and independent exact-head publication assessment | PC-001; preserve owner scoped-only direction | Plan and details now require final HEAD, freshly fetched base, new scoped evidence and assessment before push, invalidated by later changes | Original critique remains Complete / Revise; disposition applied, no replacement critique | Correct prospective safeguard; execution pending |
| P03-T01 | Dynamic privacy-safe identity derivation | PC-002 and repository identity rule | Plan/details derive current authenticated id/login, repository-local author and committer | Original finding disposition applied | No fixed identity remains in executable details; execution pending |

## Critique and Material Revision Assessment

* PC-001 and PC-002 have explicit direct dispositions and matching current plan/detail corrections. The original Complete / Revise verdict is preserved rather than rewritten as a retrospective pass.
* Technical implementation follows the critiqued independent-endpoint and import-isolation direction. No significant or divergent implementation decision requiring new user acceptance or research was found.
* The supplied changes record states dispositions preceded implementation; current artifacts contain the expected corrections and no conflicting continuation direction.
* Dependent P03 publication remains paused pending completion of P02 and its own synchronization/fresh-evidence sequence. This original working-diff Review must not be reused as the later independent exact-head publication assessment.

## Plan Follow-Up Assessment

| Follow-up item | Why outside immediate scope | Owner or next action | Assessment and route |
| --- | --- | --- | --- |
| Parent live SQL/secret renewal and credential-bearing acceptance blockers | Fixture correction does not renew live authority, supply credentials or satisfy original parent acceptance | Parent live-acceptance workstream retains its existing blocker-clearing actions and human authority gates | Remains distinct follow-up; original parent Review remains Not accepted; no new correction task or defect |

## Findings

* Complete substantive RV finding set for the assessed boundary: none.
* Severity summary: Critical 0; High 0; Medium 0; Low 0.
* Pending planned P03 work and disclosed evidence limitations below are not represented as implementation defects or already-completed acceptance.

## Defects

* None identified within the supplied correction boundary.

## Routed Findings

| Finding | Destination | Owner or next action | Reason |
| --- | --- | --- | --- |
| None | None | No rpi-implement, rpi-plan or rpi-research correction required by this Review | No substantive defect, decision gap or material research gap found |

## Residual Work

* No newly discovered correction residual work.
* Existing parent live acceptance remains a distinct workstream, not a newly invented RV finding or active child task.

## Blockers and Remaining Work

* Review blockers: none.
* P02 closeout: parent may record this original Review and reconcile P02 completion in its existing artifacts after this reviewer stops.
* Remaining active work: P03 commit of implementation and dated original evidence, normal synchronization, final HEAD/fetched-base identification, fresh scoped checks, independent exact-head publication assessment, normal push, then reply/resolve PR 479 thread PRRT_kwDOUU8JX86wuntn only after confirmed remote publication.
* No publication, hosted approval, thread resolution, merge, live authorization or parent acceptance was performed or inferred here.

## Validation Evidence

| Command or recorded check | Scope | Status | Summary |
| --- | --- | --- | --- |
| New regression against original implementation, fixture-red.log | Two new fixture tests | Failed as expected | Two failures: eager Playwright import; substituted January cap inserted instead of November SQL endpoint |
| API resident unittest discovery, fixture-api-resident-tests.log | Resident API tests including both new tests | Passed with skips | 108 tests, OK, 7 opt-in skips: 6 isolated SQL accounting tests and 1 separate resident browser test |
| Core showcase unittest discovery, fixture-core-tests.log | Core admission, application configuration/session behavior and SQL suite discovery | Passed with skips | 77 tests, OK, 19 opt-in loopback SQL tests skipped; December-cap test explicitly passes |
| Changed-Python Ruff, format and mypy | Two changed Python files | Reported passed; raw terminal evidence unavailable in supplied logs | Parent request and changes record attest corrected direct imports/sorting and final success; not independently rerun or represented as a fresh retained tool transcript |
| python -m checks.resident_demo_browser_check, fixture-browser-image.log | Shared fixture with real local SQL and Chromium | Passed | 55 PASS assertions, completion marker, real SELECT 1 readiness; no Docker/browser rerun in Review |
| python -m checks.resident_demo_image_check, fixture-browser-image.log | Exact Dockerfile.resident-demo build and actual hardened runtime | Passed | 22 PASS assertions, completion marker, source HEAD reported, final exact-owned SQL container removal |
| Explicit worktree source/test PYTHONPATH and foreground flock -w 0 -E 75 /tmp/ama-rpi-heavy.lock | Prior focused implementation validation | Reported executed | Details/changes and parent attest absolute API/core/agents source roots plus core/tests and agents/tests, zero-wait foreground lock and task-owned loopback SQL. Result logs do not echo the literal launch command or full environment; no stronger independent invocation claim is made |
| git diff --check | Current tracked correction diff | Passed during Review | No whitespace errors |
| Scoped same-value/cap grep, unchanged-dependency git diff and read-only log assertion count | Shared fixture, SQL endpoint, image import, core cap coverage and sensor references | Passed during Review | Confirms independent ceilings and 55/22 assertion totals, excluding readiness/cleanup PASS lines |
| Full matrix, fresh synchronized candidate gate, hosted checks and live acceptance | Outside this original Review | Not run | Owner limits this Review to supplied evidence and cheap scoped reads; P03 owns fresh exact-head publication evidence; no full receipt or live approval claimed |

The original unit logs retain expected negative-path exceptions while ending
in OK; these are not mistaken for new suite failures. Opt-in skips remain
skips, even though separate browser/image checks exercised this fixture
against actual SQL. No secrets, private data, cloud calls, uv, dependency
installation, heavy workload or new /tmp file operation was performed by
this reviewer.

## Outcome

* Outcome: Conformant.
* Boundary: inspected P01 correction and completed P02 check evidence, with this original independent Review supplied; not a verdict that the entire three-phase plan has completed.
* Rationale: both actual fixture insert endpoints are independent November values compatible with the unchanged constraint, December application semantics remain unchanged and covered, import isolation is directly tested, red/green and real SQL/browser/image evidence agree, critique dispositions are reconciled, and pending publication is accurately reserved to P03.
* Parent live-acceptance outcome remains Not accepted. This child verdict neither replaces nor repairs that original Review.

## Closeout Routing Record

| Finding class | Destination | Owner or next action |
| --- | --- | --- |
| Implementation defect | None | No actionable RV finding |
| Decision gap or invalid assumption | None | No actionable RV finding |
| Material evidence gap | None | No blocking gap for this working-diff Review; fresh final-candidate evidence remains planned P03 work |
| Non-blocking residual work | Existing parent live-acceptance follow-up | Parent retains original blockers and authority gates |
| Remaining active plan work | P03 | Parent commits this original Review, synchronizes, binds fresh scoped evidence to final HEAD/base, obtains independent publication assessment, pushes normally and handles the thread |

* Execution status: Complete.
* Outcome: Conformant within the explicitly assessed P01/P02 boundary.
* Validation coverage: supplied unit/red/browser/image logs inspected; cheap scoped read checks passed; lint/type and invocation controls reported by parent with raw-transcript limitations disclosed; no full gate or publication validation performed.
* Blockers: none for this Review; P03 and parent live acceptance remain uncompleted.

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/research/2026-10-27/resident-sql-fixture-window-research.md](.copilot-tracking/research/2026-10-27/resident-sql-fixture-window-research.md) | C1-C7 research |
| [.copilot-tracking/plans/2026-10-27/resident-sql-fixture-window-plan.md](.copilot-tracking/plans/2026-10-27/resident-sql-fixture-window-plan.md) | Reconciled scope and pending P03 |
| [.copilot-tracking/details/2026-10-27/resident-sql-fixture-window-phase-details.md](.copilot-tracking/details/2026-10-27/resident-sql-fixture-window-phase-details.md) | Execution boundaries |
| [.copilot-tracking/reviews/plans/2026-10-27/resident-sql-fixture-window-plan-critique.md](.copilot-tracking/reviews/plans/2026-10-27/resident-sql-fixture-window-plan-critique.md) | Preserved original critique |
| [.copilot-tracking/changes/2026-10-27/resident-sql-fixture-window-changes.md](.copilot-tracking/changes/2026-10-27/resident-sql-fixture-window-changes.md) | Completed checks and publication handoff |
| [.copilot-tracking/reviews/logs/2026-10-27/resident-sql-fixture-window-review.md](.copilot-tracking/reviews/logs/2026-10-27/resident-sql-fixture-window-review.md) | This original independent Review |
| [src/api/checks/resident_demo_browser_check.py](src/api/checks/resident_demo_browser_check.py) | Reviewed shared SQL fixture correction |
| [src/api/tests/test_resident_demo_check.py](src/api/tests/test_resident_demo_check.py) | Two new behavioral regression tests |
| [infra/sql/resident-showcase.sql](infra/sql/resident-showcase.sql) | Unchanged November SQL constraint |
| [src/api/checks/resident_demo_image_check.py](src/api/checks/resident_demo_image_check.py) | Unchanged shared fixture consumer |
| [src/core/src/zava_forward/core/resident_showcase.py](src/core/src/zava_forward/core/resident_showcase.py) | Unchanged application-cap behavior |
| [src/core/tests/test_resident_showcase.py](src/core/tests/test_resident_showcase.py) | Existing December-cap coverage |
| [src/core/tests/test_resident_showcase_sql.py](src/core/tests/test_resident_showcase_sql.py) | Existing November SQL fixture and constraint coverage |
| [src/api/checks/resident_sensors_browser_check.py](src/api/checks/resident_sensors_browser_check.py) | Related in-memory application-cap uses |
| [src/README.md](src/README.md) | Current scoped-check and publication policy |

## Next Steps

Return this one original Review to the active parent. The parent owns P02
status reconciliation and the already-planned P03 sequence, including fresh
scoped evidence and independent exact-head publication assessment. Preserve
this record and the original parent Not accepted Review. No second RPI Review,
source change, publication action or user response is requested by this
reviewer. Review stops here.
