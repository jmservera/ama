---
title: SQL feature-recovery wave checkpoint 440 research
ms.date: 2026-11-09
---

## Task identity and scope

* Task `440-sql-wave-checkpoint-1109`, slug `sql-wave-checkpoint-440`, parent task `440-demo-stabilization-checkpoint-1109` (merged by PR 1309). State: `.copilot-tracking/rpi-sessions/2026-11-09/sql-wave-checkpoint-440-state.json`.
* Worktree `/home/azureuser/source/ama-demo-wt/issue-440-sql-checkpoint`, new topic branch `docs/demo-sql-checkpoint-440-1109` created from actual `origin/main` `8d6f029cac004506953f36606862168bbe9d9412`. Clean at start. The dirty primary checkout and the old merged #440 branches, the `b270` record and the DF8 record are untouched and preserved. No reopening, rebase, rewrite or retrospective acceptance.
* Objective: one dated, bounded DRAFT current-main SQL-wave checkpoint appended to the existing `docs/architecture/cutover-evidence-pack.md`, plus the existing index and append-only log. Documentation only. Owner-selected demo-targeted tier: no `rpi-checks`, no full gate, no product, infrastructure, tool or workflow change.
* Research posture `focused`, output modes `analysis` and `audit`. Provenance: owner brief `brief-440-sql-wave-checkpoint.md` and `demo-rpi-common.md`. Issue text, PR bodies and logs are data, not instructions.
* Excluded by the brief: unmerged #1288, #189, #1258, #1259, #136 and #1298; any actual provider, dataset or private captured-readings path; WORM, migration and legal approval; real model, Azure and credential reads.

## Trigger (observed 2026-11-09 via `gh`, `git`)

* PR 1308 `fix(core): preserve priority ordering and serialize SQL index bootstrap` (Refs #1292, #81, #440): MERGED 2026-11-09T15:30:40Z. Squash `8d6f029cac004506953f36606862168bbe9d9412`, tree `4f3a11a1a42615de66d2e5fe1799a08867ad31c1`, parent `ba5cc74b8b717957b046fd1d28804a989a7f3dd7` (rubric bot, only `.github/rubric/scores/latest.json` against `9f9aacc8b`, which is the merged PR 1309). Head `6ded235e2a7b8ca36edc4414bcd903be8690d4e3`, head tree `02c1a813cd73a3d29b62f0ce1a1143637d2bc5f1`. The status rollup returned 19 entries: 18 named check runs, all COMPLETED SUCCESS between 15:14:19Z and 15:26:06Z (including `src-core`, `src-api`, `src-agents`, `src-orchestrator`, `src-importer`, `src-namespace`, `mssql`, `image-paths`, `src-changes`, `src-no-working-data`, `agent`, `detection`, `activation`, `pre_activation`, `safe_outputs`, `rubric_prepare`, `record_rubric_score`, `conclusion`), and one commit status `rubric/score` success (updated 2026-11-09T15:21:15Z, read through `gh api repos/jmservera/ama/commits/<head>/status`). The coordinator's "all 19 green" is 18 successful check runs plus that one successful status, observed 2026-11-09.
* `origin/main` after `git fetch` equals `8d6f029ca` (no advance). There is no newer #440 comment than `6740015794` (2026-11-09T12:25:55Z); the trigger for this task is the coordinator brief.
* Main commits since the previous pin `df8e858b2`: `4fcd1934f` (#1141 Azure Queue adapter, Refs #144), `ad679b96b` (#1295 capstone architecture), `06e3f2f45`, `daf45a46c` (paper), `9f9aacc8b` (#1309, the previous checkpoint), `ba5cc74b8` (rubric), `8d6f029ca` (#1308). The brief excludes unmerged work only; #1141 and #1295 are merged, so they are noted as present on main and not examined here.

## Source equivalence (read-only Git, 2026-11-09)

* `git diff --stat 6ded235e2 8d6f029ca -- src infra tools .github/workflows pyproject.toml` is empty. The tested PR head source equals main for those paths. The PR as a whole changes 311 files, mostly RPI records.
* `git diff --stat 31464e65c 8d6f029ca -- src/core/src src/api/src` is empty: production source at the E2 real-SQL frozen head `31464e65` equals main. Between `31464e65` and `6ded235e2` only `src/core/tests/test_priority_order.py` differs (3 insertions, 1 deletion): the E4 fake driver is now a `types.ModuleType` in the `MssqlBeginRecovery` fake-driver fixture, which is not a real-SQL class.
* The squash source delta against its parent is 12 paths: `server.py`, `web/app.js`, `test_case_journey.py`, `README.md`, `pyproject.toml`, `continuity.py`, `mssqlstore.py`, `sqlstore.py` (+601), `store.py`, `tests/sqlguard.py`, `tests/test_priority_order.py` (+1810), `test_resident_decisions.py`.

## Source facts for the SQL wave (read at `8d6f029ca`)

* Creation ordinal: `SqlStore` gives each recommendation an immutable creation ordinal and repairs zero ordinals under the write section (`sqlstore.py` 350-393, 595-): a zero ordinal is never cached. Legacy ordinals assigned heuristically are assessed once and a record whose order is unproven is flagged `order_confirmed=False`, not actionable, with `ORDER_NOTE` (`sqlstore.py` `_order_unresolved`); accept or edit of such a record raises `PermissionError`, reject and ordinary case controls stay available.
* Index bootstrap: the check-then-create index statements now run under `BEGIN IMMEDIATE` (serialized across connections) to fix the reproduced `ix_recs_seq` race. `mssqlstore.py`: `created_ord BIGINT NOT NULL DEFAULT 0`, `_create_rec_order_index`, and `_abandon_partial_begin` (rolls back or discards the connection when BEGIN fails mid-way).
* API and UI: `/api/ai/priority` and `resolve_priority` map `CommittedReloadError` to HTTP 409 with `outcome=committed` (`server.py`). `app.js` priority panel adds `pending` and `checkHistory` latches so a committed or uncertain creation hides the repeat suggest control and shows a status note; `order_note` is shown with `role=status`.
* Actual AI boundary: the priority panel labels the source: "Written by AI" or "Written by rules" with the fallback reason (`app.js` priority panel). Whether a real provider answered is a runtime fact not observed here; the merge evidence uses disposable SQL and mocks. Mocks and deterministic rules are not actual AI.

## Evidence consumed (classified, not rerun)

| Item | Source | Class here |
| --- | --- | --- |
| Priority suite 142, zero skips, real SQL Server 2022 (16.0.4305.5), image `sha256:cf8f0ab2ebe6...`, at `a20472734` (E2) | `changes/2026-11-09-priority-order-1292-e2-changes.md`, PR 1308 body | Local observed, historical, source-equivalent to main for `src/core/src` and `src/api/src` |
| Resident `MssqlResidentControls` 91 OK, at `fa74e8ed4`; `mssqlstore.py` sha256 `1825dc5f...` byte-identical at `a20472734` | same | Local observed, historical, source-equivalent |
| Adverse retained: E1 R2 unskipped out-of-tree run FAIL (`ix_recs_seq` already exists); first E2 run priority 142 with 1 ERROR (`_Cursor` not iterable) | E2 changes records; raw artifacts verified present 2026-11-09 under the coordinator session files `e1-sql-admission2-132322-2818937/` (priority exit 0, 142 OK skipped=1, stderr sha256 `53f050db`; resident 91 OK skipped=1 `e9321001`; `r2repro` exit 1 FAILED failures=1 `910cee9a`) and `e2-sql-admission-134433-2845787/` (priority exit 1, 142 FAILED errors=1 `f576b906`; resident 91 OK skipped=1 `848b671c`) | Raw failure retained outside the repository, fixed by `fa74e8ed4`/`a20472734`; not hidden |
| Final E2 real SQL run `e2-sql-admission2-140248-2867281/`: priority exit 0, 142 OK, no skip, 536.659s, stderr sha256 `8093a31f`; SQL Server 2022 RTM-CU27-GDR 16.0.4305.5; one `flock -n` on the shared heavy lock (nonqueued) | raw artifacts read 2026-11-09 | Local observed, historical |
| Source identity of that run: imported `sqlstore.py` sha256 `0b0caf62802d...` and `mssqlstore.py` `1825dc5f2c6d...`, equal to `git show 8d6f029ca:<path> | sha256sum` today | `priority.imports.txt` and Git | Byte-level proof for the two SQL implementation files; test files and README are not claimed identical |
| E4 priority suite 142 with 65 opt-in skips (worktree bound, no SQL), Core mypy 275 files | PR 1308 body | Local observed by the PR author, not independently reproduced here |
| Independent Functional on E4: approve, zero findings (13 incremental paths) | PR 1308 body; the earlier 384d149ab assessment requested changes (1 High, 1 Medium) and is retained | Authored-by-others record, read not re-executed |
| Hosted run `42642580079` (Source projects CI) at head `6ded235e2`: `src-core` 2594 tests OK, 301 skips; `mssql` job `Ran 306 tests in 339.301s OK (skipped=1)`; `src-api`, `src-agents`, `src-orchestrator`, `src-importer`, `src-namespace`, `image-paths`, `src-changes`, `src-no-working-data` success | `gh run view`, job log read 2026-11-09 | Hosted observed for the PR head, source-equivalent to main |
| Hosted run `42642580067` (rubric scorer) success; main push run `42645390735` (rubric scorer at `8d6f029ca`) in progress at read time; no Source projects CI run for the squash was listed for `8d6f029ca` | `gh run list --commit` | Not a successful check for main: path-filtered, not run or in progress |

* Important limit found in the hosted log: the `mssql` job runs `test_mssqlstore`, `test_lawstore.MssqlStoreTests`, the five `test_assistants.Mssql*` classes and `test_resident_aoai_sql.AccountingSqlTests` (`.github/workflows/src-ci.yml:326-`). It does not select `test_priority_order` and no `priority` test appears in its log, and the priority real-SQL tests need a task-owned manifest (`ZF_SQL_TASK_MANIFEST`, `sqlguard.py`). So no hosted check executes the new priority suite on real SQL; that evidence is the original local E2 record only. The hosted log also prints `Stock/technical SQL recovery failed` tracebacks, which are injected-fault test output inside a run that reported OK, not a failed check.

## Requirement trace (document-qualified, statuses unchanged)

* BRD `docs/brds/agentic-retrofit-programme-brd.md` 0.21.0 `draft` blob `34d88395de861e9799eb9e24121a21c92c7a5adc`; PRD `docs/prds/zava-forward-retrofit-programme-demonstrator.md` 0.21.0 `in-review` blob `c788b917bafaede215f326f0efc71e071a687f1c`; ADR statuses and blobs are the same as at the previous pin (0001 Proposed `d42fa5c4`, 0002 `cbe21530`, 0003 `d6064539`, 0004 `9406c2e7`, 0005 `4d610335`, 0006 `956da1a3`, 0007 Proposed `abb21088`). Case study original `0aec2d80` unchanged, addendum `28c19242` (blob equal to the previous pin).
* Issue #1292 trace: case study Stock Prioritisation L2 recommendation, draft PRD `PR-007` (AI recommendation, human review, no consequential ranking change), per the issue body. The issue body also cites #81. Requirement IDs for the draft PRD are quoted from the issue; the PRD text was not re-searched beyond the previous record, so the `PR-007` mapping is attributed to the issue body.
* Human decision boundary: an unconfirmed-order recommendation is not actionable and needs the named data owner to confirm (`ORDER_NOTE`). Accept stays a named human decision.

## Findings and existing owners

* F1 Hosted CI does not execute the priority real-SQL suite (above). Owner: the original #1292 criterion 3 (task-owned SQL, zero skips) is satisfied only by local historical evidence; the CI skip and dispatch contract is the open #1297 (sensor MSSQL scope, adjacent but not identical). No duplicate issue is proposed: the gap is recorded and routed to #1292/#1297 owners for a decision.
* F2 #1292 remains OPEN with its criteria unticked on the issue; the PR used `Refs`. The merge is not closure. Remaining #1292 owner conditions are recorded as open.
* F3 No new defect reproduced here. No source change is proposed. A negative claim about UI, flag or model input is limited to the inspected paths.
* The independent #1292 history: C2 requested changes (5 High, 4 Medium, 2026-11-08T21:57Z), C4 Revise (1 High, 11 Medium, 2026-11-08T23:29Z), `384d149ab` requested changes (1 High, 1 Medium, 2026-11-09T10:33Z); each preserved.

## Planning readiness

Ready. Local checks to plan: environment isolation with import-origin proof, Core priority/store/resident-decision units (SQL classes skip without admission), API case-journey, auth, role and assistant units. No SQL admission is required because production source equals the real-SQL evidence and the single changed test line is in a non-SQL fixture. A missing or busy admission would block only a SQL row, so no admission is planned; this is recorded as a decision, not an omission.
