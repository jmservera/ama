<!-- markdownlint-disable-file -->
---
title: Issue 75 building SQL changes and full phase log
description: Ordered execution, validation and publication evidence
ms.date: 2026-10-18
---

## Metadata

Task 75 / issue-75-building-sql, 2026-10-18.
Plan: `.copilot-tracking/plans/2026-10-18/issue-75-building-sql-plan.md`.
Details: `.copilot-tracking/details/2026-10-18/issue-75-building-sql-phase-details.md`.
Frozen base: `9d625a09e34491ecf9fd27ffc7d59e67c2373b29`.

## Execution Status

Full approved plan. Implement P01/P02 complete; one original Review complete.
Completed: Research; Plan/details plus one independent critique and dispositions.
Completed P01/P01-T01: tests and README, source-only diff is two files.
Completed P02/P02-T01: focused regressions, actual SQL, cleanup fault probes,
configured static checks and migration. Original Review: execution Complete,
outcome Conformant within bounded local constructed SQL conformance only.
Remaining: P03 publication bookkeeping, no source corrections or second Review.

## Full Ordered Phase Log

1. Research executed on exact base, Wider -> Deeper -> Contrarian inline;
   Planning Readiness Ready. Research artifact existed before substantive tracing.
2. Plan and phase details created before implementation; one independent
   final-candidate critique returned Revise (2 High, 2 Medium), preserved.
3. Parent accepted PC-001-PC-004 directly: exact refusal cause and bindings,
   orthogonal scope matrix, sanitized local environment and failure cleanup.
   Plan Ready before Implement. No second critique.
4. Implement started after finalized plan; no source edits preceded this entry.
5. P01 complete: five semantic tests plus three inherited HTTP cases. First SQL
   run exposed two actor-index fixture mistakes, retained and corrected in tests.
6. Second actual SQL execution: eight tests passed, zero skips, in 9.621s;
   exact owned SQL resources removed. Static/migration rerun exposed two
   mypy cache/path errors; fresh configured analysis passed.
7. Three contained real-SQL lifecycle probes passed: fixture setup, HTTP
   post-thread-start failure and wipe failure. Final configured migration,
   Ruff, format and mypy all passed. P02 complete, original Review ready.
8. ONE original Review completed directly, no independent lens required for
   this compact diff. Execution Complete, outcome Conformant within bounded
   scope; no substantive defect. Original record frozen, no second Review.
   Parent moves to authorized publication only, then stops.

## Approved Implementation Boundary

`src/api/tests/test_mssqlstore.py`: five semantic tests, three inherited HTTP
regressions, bounded fixture/lifecycle helpers, short-lived wipe connection
closure. No wipe table additions, no issue110 sensor files.
`src/api/README.md`: test command and honest limits. No production change.

## Implementation-Time Plan and Detail Updates

Verified environment selector names against source before invocation:
ZF_DOC_STORE=local, ZF_SCANNER=local, ZF_AUTH=password, ZF_ENV=test.
Prospective guessed labels in details were corrected before executing any run.
This is an immediately relevant factual command refinement, not changed intent.

## Validation Record

Initial system-Python prerequisite probe failed import, one loader error:
ModuleNotFoundError: No module named zava_forward. No conformance test executed.
Dependency restoration now permitted in isolated task virtualenv with pip.
Docker responsive; existing local SQL2022 image is available.

### First actual SQL execution: adverse original retained

`issue-75-sql-execution.txt` preserves first actual run: eight tests executed,
six passed, two errors, zero skips. Owned container
`d7c3bfb08eaa1a76f839662171e509d4ff5e3dc2ee883031a7c7e586c6b1d26e`
removed successfully; exact-ID lookup empty.
Errors were test-fixture actor selection: MSSQL reload orders staff differently
from seed order, so `store.data["staff"][1]` was not Pam. One setup issue call
raised manager PermissionError; one projection correctly omitted restricted costs.
This is not a demonstrated production defect. Replace positional actor lookup
with existing registry `store.staff["pam@example.test"]`. No runtime amendment.
This is an ordinary local test correction within the approved five methods.

### Initial static execution: dependency and invocation evidence retained

`issue-75-static-execution.txt`: Ruff and configured format passed; migration
had seven import errors for missing Pillow/python-pptx, mypy lacked Playwright.
Mypy also inherited runtime-only PYTHONPATH causing release_support to be seen
as an untyped installed module instead of the configured missing-import boundary.
Restore missing tools with pip; run static with no runtime PYTHONPATH, matching
CI step scoping. The subsequent standard invocation reused that stale cache.
Exact-base archived configured analysis passed; current-tree
`mypy --no-incremental` also passed all 58 files. Thus these were invocation/cache
artifacts, not a pre-existing source defect. No source/config change or exemption.

### Focused regressions and successful actual SQL execution

`issue-75-local-execution.txt`: core buildings + quality/procurement 117 passed;
API buildings/procurement/role matrix/portable SQL plus opt-in-off class selection
55 total, 47 passed and eight SQL tests skipped = Not run in this invocation.
Expected failure-injection logs are retained; inherited HTTP writes log unavailable
law store as explicit Unknown, not regulatory acceptance.

`issue-75-sql-rerun-execution.txt`: actual Microsoft SQL Server 2022
RTM-CU27-GDR 16.0.4305.5, Linux Developer edition; image
sha256:cf8f0ab2ebe61feec2eed2629061a07d247f791c2a8ddda74a4ac9f06a291718.
Eight selected building tests passed, no skips. Container
`e36e9fb1059966ed892268f96f0e33921c90e2b32910809ca18180914e2ab98d`,
database `issue75_1d6c6df9eb6f41a883fedb507799707c`, port 32852 loopback.
Exact-ID removal exit 0 and no remaining ID. No mounts, configured datasets,
private support, .env, production resources, real AI or Azure used.

`issue-75-static-rerun-execution.txt`: 25 migration tests pass after restoring
Pillow/python-pptx/PyYAML; configured Ruff and format pass. Missing Playwright
restored at project-pinned 1.64.0. This rerun retained two cached
`test_continuity_epoch_export.py` errors (release_support import typing and
unused ignore). Both disappear with a fresh analysis, matching archived base;
see `issue-75-base-mypy-execution.txt` and `issue-75-fresh-mypy-execution.txt`.

### Cleanup fault probe invocation

First probe invocation failed before execution because running a script outside
cwd lacks the implicit `.` path that unittest has; `tests.test_mvp` could not
import. `issue-75-sql-fault-execution.txt` retains the error and exact cleanup:
container f64e6ff5a9e7f431969d5c655bfff28d730a7c0c17c31d173a40c829707654b9
removed, remaining ID empty. Refine probe-only PYTHONPATH to include `.`.
No committed source change and no conformance outcome inferred from loader error.

### Final static and failure-cleanup evidence

`issue-75-static-final-execution.txt`: 25 migration tests pass, Ruff check pass,
configured format pass, standard configured mypy pass (58 source files).
Earlier adverse outputs remain unchanged and are not presented as passing.

`issue-75-sql-fault-final-execution.txt`: three contained lifecycle probes pass
against another task-owned SQL database. Inject OSError in supplied contract
setup after factory construction, run unittest cleanups, assert connection
raw handle cleared and patch/tmp restored. Inject OSError immediately after
actual HTTP thread start, run cleanups, assert thread dead, server socket closed,
SQL handle cleared and tmp gone. Inject wipe execute failure, assert close called
once and original OSError retained. These are probes, not three new committed
test methods. Container
`3d4f4160c790130e8814da02d89c1dfc3c9bf48c02140588025420e64a6211bd`
removed by exact ID with exit 0 and empty remaining-ID lookup.

All four task-owned container/database attempts were cleaned immediately by
finally; there are no retained SQL resources from this task. Database files
were on container writable layers, no host data mounts or reusable volume.
Safe launch shape: docker run --detach --name zf-issue75-UUID
--publish 127.0.0.1::1433 --env ACCEPT_EULA=Y --env MSSQL_SA_PASSWORD
--memory 3g --cpus 2 mcr.microsoft.com/mssql/server:2022-latest.
Password generated per attempt, passed only via subprocess environment and never
written to artifacts. All Python subprocesses used allowlisted local environment,
workspace TMPDIR/docs/digests, no inherited ZF/AI/Azure configuration.

### Applicability and inventory

Production source, schema, shared fixtures, manifests, Dockerfiles, web assets,
workflows and PR398 governance are unchanged. App Docker/nonroot/image/browser
and accessibility reruns are redundant/not applicable for this test-only patch,
not reported passed. Local MSSQL container is a database test resource, not an
application image acceptance run. No all-engine or full operational claim.

## Pre-Review Reconciliation

Ready. Plan P01/P02 markers checked and details current. P03 intentionally
unchecked until one original Review and publication complete. Full implementation
diff: test harness and direct README only, no production change or schema/table
addition. All six bounded criteria mapped to tests and actual evidence; broader
human/operational/live acceptance remains outside scope, not a hidden blocker
or completed approval. This paragraph records the pre-Review gate; Review later
completed as phase log entry8. No second critique or Review ran.

## Original Review and Publication Boundary

Original Review:
`.copilot-tracking/reviews/logs/2026-10-18/issue-75-building-sql-review.md`.
Assessed executable blob: `351c81ab24c09811a4e3195b9d88482456482b01`;
README blob: `3c8b48ae6c6a37d38100a9c860768727fa162073`.
No source edits after that Review. Commit/push/draft metadata may be appended
by the parent; this is not another Review or source correction.

Task-owned workspace scratch (virtualenv, constructed document bytes, digests,
temporary fixtures and archived baseline) removed by exact resolved path after
Review. Absence verified. No working data staged. Authenticated GitHub identity
resolved immediately before commit; repository-local noreply configured for both
author and committer. Available host has no get_changed_files tool; the complete
two-file source diff and tracked/untracked issue inventory were inspected with
Git before staging, without inventing a missing-tool result.

## Blockers

None requiring coordinator intent/authority.

## Follow-Up Items

Operational register/update rights, allocation policy, human/accessibility
acceptance and live application evidence remain coordinator-owned and outside
this synthetic SQL slice. Issue75 remains open, no review checkboxes ticked.
