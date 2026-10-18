<!-- markdownlint-disable-file -->
# RPI Changes: Scoped consultation hold

## Metadata

Task ID 92; slug issue-92-scoped-consultation-hold; date 2026-10-18.
Plan: .copilot-tracking/plans/2026-10-18/issue-92-scoped-consultation-hold-plan.md.
Details: .copilot-tracking/details/2026-10-18/issue-92-scoped-consultation-hold-phase-details.md.

## Execution Status

Implementation complete; declared scope full plan P01/P02. All markers complete.
Approved writes: five procurement call removals, truthful refusal/audit wording,
coupled tests and documentation. No shared server/SQL/schema/role/web changes.
Remaining active implementation markers: none. One original Review complete.
No safe-implementation blocker. Authorized integration onto a86282c4 is complete
locally. Coordinator now authorizes exact ab0613f3 integration/publication;
the prior main-movement stop below remains historical evidence.

## Execution Summary

Integration: 9fb84836e3e3ad24a17e142bd6a3e9d1a68d70e7 onto
9c648b2006e8b2e563823ea7d5aabdf7f1ac7096 -> d276d4ce8e8acfd72c3eebded58959b24c534a1c.
All seven original RPI digests verified identical. Main appointment commitments
and both knowledge histories retained. Exact initial lease remains owner-specified.

## Implementation-Time Plan and Detail Updates

PC-001 directly applied before implementation: package-aware instruction isolation
is distinct from retained case-wide advance. Original critique verdict Revise
remains unchanged; no second critique. Three-way scope test matrix locked.

## Validation Record

* Before source changes: `PYTHONPATH=src/core/tests:src/api:src/api/tests:src/agents/tests
  .venv/bin/python -m unittest test_mvp test_workflows -q`: 40 run, three
  consultation errors (StoreTests and JSON/SQLite safety-flow paths).
* Original-main component reproduction: same 40 selectors after executing verbatim
  `git show 9c648b2:src/core/src/zava_forward/core/procurement.py` in the isolated
  process module before Store import: 40 pass. Not a full original-main suite.
* Initial guessed fourth SqlStoreTests method selector was absent, loader error;
  corrected full selectors above. No claim that supplied four-path CI count was
  locally reproduced as four errors.
* Subsequent semantic tests, configured checks, local owned SQL, manifest and
  non-root HTTP pending. Existing unknown law-store diagnostics are explicit.

## Blockers and Remaining Work

No implementation blocker. Actual Legal approval and true let/renew remain unmet.
P01/P02 complete and reconciled. Original Review complete; publication waits for coordinator.

## Completed Work

### P01-T01 scoped implementation

Removed precisely five blanket consultation calls; changed audit/refusal text to
consultation-dependent scope. Source provenance/effective unknown and explicit
denial unchanged in meaning. All independent main control logic stays intact.
Removed consultation-only bypass setups in six affected regression modules.
Retained provenance, forged identity, source bytes/version, stale writer, failed
save/audit and current-recorder transaction tests. Updated ordinary lifecycle
expectation and added two scoped core methods plus one HTTP method, within lock.

The existing building dependency mechanism supplies the explicit dependent
boundary, not an invented Legal classifier. Unknown/Open scoped work stays held;
positive supplied records do not release it; unrelated case/package service
operations pass; same-case final advance retains its case-wide hold (PC-001).
No genuine let/renew route exists; HTTP let/renew remain 404, not exact acceptance.

### Implementation-time local test refinements

First new tests failed before production edits: four executions, three unknown-
consultation errors and one HTTP 400-versus-200 failure. Initial combined run
exposed test-harness mistakes, not reasons to weaken main: SQL fixture edits
needed `_case` dirty tracking; main completion required a real synthetic appointment
agreement; Completed orders cannot be withdrawn; HTTP GateError is 409 with
`reasons`, unsupported routes 404; typed callable list required an annotation.
Corrected the owned tests coherently, with no unrelated expectation changes.
Separate fresh-scenario PC-001 method avoids removing a completed order or
pretending it can be withdrawn. No source correction cycle was needed.

### P02-T01 validation executed so far

Common root selectors use
`PYTHONPATH=src/core/tests:src/api:src/api/tests:src/agents/tests .venv/bin/python -m unittest`.

| Command / selector | Result |
| --- | --- |
| test_consultation_controls test_procurement_api test_quality_procurement test_buildings test_hazard_referral test_resident_decisions test_mvp test_workflows test_role_matrix test_scenario_manifest test_stock_reconciliation test_grant_lifecycle_controls test_finance_match_controls -q | 519 run, 424 passed, 95 explicit skips; final repeat 232.687 seconds |
| `(cd src/api && PYTHONPATH=../core/tests:../agents/tests ../../.venv/bin/python -m unittest discover -s tests -q)` | 794 run, 542 passed, 252 explicit skips, 436.730 seconds; actual unit selectors used by failed test/validate/src-api jobs, not CI-first |
| `(cd src/core && ../../.venv/bin/ruff check . && ../../.venv/bin/ruff format --check . && ../../.venv/bin/mypy)` | Pass; 72 already formatted; 125 typed source files |
| `(cd src/api && ../../.venv/bin/ruff check . && ../../.venv/bin/ruff format --check . && ../../.venv/bin/mypy)` | Pass; 24 already formatted; 56 typed source files |
| `.venv/bin/python tools/rename-zava-tests.py` | 25 passed; expected malformed-PPTX diagnostic |
| Initial `python3 tools/rename-zava-tests.py` | Failed: system interpreter missing dependencies including PIL; retry with existing venv passed, no package installation |
| Five isolated in-memory procurement mutants, each reintroducing one removed call | All five killed by real ordinary-lifecycle test; no persistent source mutation |
| `git diff --check` and original seven-artifact SHA256 check | Pass |

Complete discovery outcome above is observed, not inferred. Final focused/
combined runs additionally cover the exact finished assertions. No new
dependencies were installed.

### Actual task-owned SQL Server parity

Existing image `mcr.microsoft.com/mssql/server:2022-latest`; unique loopback-only
container `ama-issue92-scoped-165474b4addd`, owned `zf_issue92_scoped` database.
Fresh ephemeral credentials generated only in process; never read shared credentials.
First container `ama-issue92-scoped-53ce5b125fe1` reached readiness log before
authenticated readiness and failed sa login; removed in finally. Retry waited for
actual authenticated SQL response (15 attempts), then created database.

With `ZF_SQL_SERVER=127.0.0.1`, unique published port, password test authentication,
`ZF_SQL_TRUST_CERT=1`, `ZF_TEST_MSSQL=1`, ran:
`test_consultation_controls.MssqlConsultation test_mssqlstore.MssqlProcurement
test_mssqlstore.MssqlProcurementApi test_mssqlstore.MssqlHazardReferral
test_mssqlstore.MssqlStockDecisions test_mssqlstore.MssqlFinanceSignoffs
test_mssqlstore.MssqlStoreTests -q`.
136 run, 135 passed, one intentional skip, 273.620 seconds. Fault-probe recovery
diagnostics are expected assertions, not swallowed application failures. New
scoped/lifecycle/provenance/source/recorder tests execute on actual SQL Server.
Owned container removed in finally, including database; active #76 container
untouched. No sqlstore, queues, release/export or server implementation edit.

All HTTP executions use actual installed editable src distributions as UID/GID
1000, authenticated loopback server and temporary synthetic data. This is non-root
installed-API evidence, not rebuilt-image or deployed acceptance. No browser,
screen-reader, human, live Legal, Azure, IAM, Graph, spend or model checks run.
Optional backend/browser skips remain skips, not acceptance; real SQL above
supplies separate parity. Full core discovery also passed:
`(cd src/core && PYTHONPATH=tests:../api:../api/tests:../agents/tests
../../.venv/bin/python -m unittest discover -s tests -q)`: 1117 run,
984 passed, 133 explicit skips, 350.531 seconds.

### P02 documentation and preservation

Core/API guides and existing profile synthesis/index now distinguish ordinary
service scope from missing Legal/let authority. Dated append-only log retains
both original consultation entries after exact upstream 418574-byte prefix.
SHA256 checks preserve all seven old task artifacts. No fixture/manifest bytes
changed; test_scenario_manifest passed within combined and core checks.

## Pre-Review Reconciliation

P01/P01-T01/P02/P02-T01 complete for bounded engineering. Plan/details, actual
validation, historical evidence, known gaps and this handoff reconciled.
Ready for ONE original Review. No new Legal/let/live acceptance claim.
Publication remains blocked by moved main; no second integration attempted.

## Original Review and Final Routing

Exactly one new original Review executed at
`.copilot-tracking/reviews/logs/2026-10-18/issue-92-scoped-consultation-hold-review.md`.
Execution Complete; outcome Residual work. No bounded implementation defects;
three Medium residuals: RV-001 moved-main publication boundary, RV-002 missing
verified Legal applicability/approval, RV-003 absent genuine let/renew acceptance.
No second Review, no post-Review source correction or closure verification.

Automatic task delivery is blocked at publication, with engineering/RPI phases
complete locally. State remains automatic/running awaiting coordinator, not a
claim that the full PR publication goal completed or that a new child was selected.
The owner-directed stop boundary prevents any follow-up implementation. Preserve
one local Conventional Commit with all new evidence, privacy-safe authenticated
author/committer and required Copilot trailer; report exact local head to coordinator.
Do not push with the lease against moved main, update PR #389, alter issue/board,
merge, deploy or rebase again. PR closing references were verified empty at intake;
no new body was submitted, and Refs #92 is the only issue reference for the commit.

## Local Persistence Receipt

Reviewed implementation and all seven new task artifacts committed locally as
`afb30d84d45e18de38863f066c5e9cead1c0a856`; clean worktree confirmed.
Author/committer: authenticated GitHub account 8036360/jmservera, repository-local
noreply address; Conventional Commit, Refs #92 only, required Copilot trailer.
This later receipt/state update is metadata-only, not a source correction or
repeat Review. Final local tip is discoverable with `git rev-parse HEAD`.

Read-only final PR check: #389 remains open, base main, remote head unchanged
`9fb84836e3e3ad24a17e142bd6a3e9d1a68d70e7`, closingIssuesReferences empty.
No lease push, subsequent normal push, PR body update or issue/board change
was performed because the explicit moved-main wait condition applies.
Full publication goal is blocked, not complete. Coordinator owns the next action.

## Publication Pause: main moved

Read-only `git ls-remote` after local validation found main
`a86282c4badebc58eabbf9e441410d930a201ac2`, no longer the owner-authorized
`9c648b2006e8b2e563823ea7d5aabdf7f1ac7096`. Topic remote remains exact lease
`9fb84836e3e3ad24a17e142bd6a3e9d1a68d70e7`. Per explicit direction, no second
rebase or publication against moved main will be attempted. Finish bounded local
Review/evidence and preserve a local commit; coordinator must clear publication
and any new integration direction. No PR, issue, board, merge or remote write yet.

## Follow-Up Items

Named Legal/Procurement authority contract and genuine let/renew integration need
separate human/coordinator direction. No live, deployment or issue closure claim.

## Same-task integration/publication authorization

2026-10-18 coordinator superseded the historical publication pause above.
Only integration/publication is in scope: local candidate 7e4aa6ec onto exact
main a86282c4, prior base 9c648b2, initial remote lease 9fb84836. Preserve PR407
queue production/tests and recorder controls; README conflicts additive only.
No new source correction, policy change, critique or original Review. Both old
and new original assessments remain byte-identical. Separate integration receipt
will record full inventories, normalized exact patches, fresh focused/combined
smoke, quality and exact publication boundary. Existing SQL/image evidence stays
historical unless production conflict or persistence change justifies rerun.

### Authorized integration validation

Own-topic rebase onto exact a86282c4 completed without conflicts, source candidate
adc9ad984cd9cd6bcfbd30db6d52485d9506ab47. No source correction or manual
merge. Upstream queue source/tests, SQL recorder controls and all unaffected
tracked paths retained. Both README additions and exact 418574-byte upstream
log prefix plus every historical own append retained.

Separate receipt and generated parity/full-inventory evidence use the
`issue-92-scoped-consultation-hold-integration` prefix beside this changes file.
Owned normalized patch SHA256 a886b897815c534424cad0c7132bd01586cf5192fd9f79755acfc2601b4343cb;
protected upstream patch SHA256 5deef027e5ee3f5dbc9d2b0b6e2072066c984e274cd895fabeb3a2468f7ba386.
Both before/after pairs match exactly; ten original research/assessment/old-task
artifact digests match. No critique or original Review was executed again.

Fresh focused command: common installed-package unittest prefix from P02,
selectors `test_consultation_controls test_procurement_api test_quality_procurement
test_mvp test_workflows -q`: 212 run, 199 passed, 13 explicit skips, 80.599s.
Fresh combined command adds `test_taskqueues test_sqlqueues test_task_queue_api
test_buildings test_hazard_referral test_resident_decisions test_role_matrix
test_scenario_manifest test_stock_reconciliation test_grant_lifecycle_controls
test_finance_match_controls -q`: 553 run, 458 passed, 95 explicit skips, 151.838s.
Expected unknown law-store diagnostics remain visible in retained logs.
Configured core/API Ruff check, format --check and mypy pass: 72/24 formatted
files and 125/56 typed source files. Installed editable paths point into this
worktree; UID/GID 1000. Diff check passes.

No production conflict or integration-authored persistence change occurred.
Authorized upstream sqlstore/taskqueues corrections are preserved verbatim;
their historical SQL/image receipts remain upstream. New SQL Server, image,
browser, human, live Legal or genuine let/renew acceptance was not run or claimed.
Original 135 actual SQL passes remain historical engineering evidence only.

### Publication preflight: main moved again, no remote write

Integration receipt and all fresh evidence committed as
ae2bc36b14025f833d449bc12c18873ee65e4b0d; source parity rechecked at that tip.
Immediately before publication, the exact-main guard failed because main became
ab0613f3336109ff9b96560a16758ee842232715, rather than authorized a86282c4.
The chained command stopped before `git push`; the authorized lease was not used.
Read-only confirmation: remote topic remains 9fb84836e3e3ad24a17e142bd6a3e9d1a68d70e7;
PR389 remains open with unchanged body/head and empty closingIssuesReferences.
GitHub PR baseRefOid still reports historical 1a05dfb8 and is not treated as
current remote-main authority; `git ls-remote` supplies the observed main hash.

Per explicit coordinator direction, report and wait. No further fetch/rebase,
push, PR edit, issue/board/merge, source correction or repeated original
assessment is attempted. A final local metadata-only receipt records this stop;
its exact tip is given by git and the caller response. Publication goal remains
blocked, not complete; all authorized integration results remain durable locally.

### Exact ab0613f3 continuation authorized

Coordinator authorizes same-task integration/publication only, from local
c6732027 onto exact fetched ab0613f3 (PR408), prior integration base a86282c4.
No source correction, policy change, second original Review or critique.
Preserve timecapture source/tests, additive API README, queue/recorder changes,
both historical receipts, all old/new original assessments and append-only log.
Fresh minimal focused/timecapture and configured static checks; no repeat broad
suite when exact source parity holds. Historical SQL/image stays historical.

Explicit topic lease remains 9fb84836; unexpected topic advancement stops
publication. Publish on exact authorized ab0613f3 even if main later moves and
report movement for coordinator gate. A new receipt will record this boundary.
Both requested /tmp execution logs read and preserved as byte-identical copies
in session cf6f1706-71c8-48ee-88ca-e30a375524dc/files; hashes in its
inherited-execution-logs.json. Do not edit or truncate originals or copies.

### Exact ab0613f3 integration and minimal validation

Nine owned commits replayed without conflicts; integrated source candidate
aafcd504a4dd402b335bffd8a7a038bc31b29156 on exact authorized ab0613f3.
New receipt `issue-92-scoped-consultation-hold-integration-dpia.md` preserves
the old receipt byte-identically. Complete owned normalized source patch matches
a886b897815c534424cad0c7132bd01586cf5192fd9f79755acfc2601b4343cb;
upstream incremental timecapture source/test patch matches
c7e400c463027b6bed3707eccc6879e440711cec4fbc6ddb09b9686757301582.
All protected upstream queue/DPIA/evidence blobs match, fifteen original/prior
receipt files immutable, ordered README additions retained, old-local log prefix
exact. Full old/base/source-candidate inventories and hashes accompany receipt.

Fresh command: common installed unittest prefix with consultation_controls,
procurement_api, quality_procurement, mvp, workflows and timecapture selectors:
235 run, 222 passed, 13 explicit skips, 69.660s. Expected unknown law-store
diagnostics retained. Configured core/API Ruff check/format/mypy pass: 72/24
formatted and 125/56 typed files. Diff whitespace check passes. No failed
validation check in this continuation; earlier failures remain inherited and
explicitly historical in the unchanged evidence.

No production, packaging or persistence conflict; no source correction. Prior
combined queue smoke and broad/full RPI suites not repeated. Actual 135 SQL
passes and existing image/hardened-runtime evidence remain historical only.
No new Review/critique, private data, cloud, spend or live acceptance.
Current plan/details/state reconciled; exact-lease publication and PR update next.
