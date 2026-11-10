---
title: Issue 1292 current-main priority SQL regression validation plan
ms.date: 2026-11-09
task_id: 1292-current-main-sql-1109
---

## Objective and boundary

Run one finite campaign of existing tests against current `main` `ba71894bb1a94d6a24aabf9828312668f88f3ff5` on one task-owned disposable SQL Server, and record the outcome with exact provenance. Validation only: no source, test, fixture or harness change, no Source E5, no retry, no observer experiment, no load simulation, no private data, no cloud, no push, PR, issue or board write. Owner-selected demo-targeted tier; this is not the complete local gate and it waives nothing.

## Phases

* P0 Preconditions (no SQL). Confirm worktree clean at the pinned commit, record versions, confirm no heavy-lock holder (`fuser`), no containers, image digest, memory and disk. Create the own environment and install `-e src/core[sql] -e src/agents`. Verify import paths resolve under this worktree.
* P1 Admission. One non-queued attempt: `flock -n /tmp/ama-rpi-heavy.lock`. If the lock is busy, the image, driver or Docker is unavailable, or a holder exists: record UNADMITTED/BLOCKED with the real reason, run nothing, no wait, no queue, no interrupting others, no cloud fallback, no fake pass. Before any container exists the runner verifies the default local Docker engine (no `DOCKER_HOST`, context `default`), the pinned local image id (no pull: `--pull=never`), no name collision, that `src` is byte-identical to the pinned base tree (`git rev-parse HEAD:src` equals `ba71894bb:src`) and that HEAD differs from the pinned base only under `.copilot-tracking/`. Execution HEAD is therefore the planning commit, not the pinned base commit; both are recorded.
* P2 Disposable server. One labelled container (`ACCEPT_EULA`, memory 3g, `127.0.0.1` published port, random password never logged or committed) from the local image; bounded readiness polling (at most 40 probes, 3 s apart; this is readiness, not a test retry); manifest written with the existing `sqlguard.write_manifest`. Each test creates and drops its own UUID-named database; no existing database is touched.
* P3 Test processes (sequential, each run by `run-redacted.py` with a 600 s total bound including kill grace (TERM at 570 s, KILL by 595 s), the campaign budget 1140 s inside an outer `timeout -k 10 1190` so 60 s remain for cleanup, no automatic retry after any failure; a later process still runs so every outcome is retained, and is labelled independent):
  * A: `test_priority_order` classes JsonPriorityOrder, LegacyMetadata, LoopbackGuard, MssqlBeginRecovery, SqlitePriorityOrder, SqliteLegacyEdges, SqliteC3Corrections, SqliteC4Corrections, MssqlPriorityOrder, MssqlLegacyMetadata, MssqlLegacyEdges, MssqlLockTimeoutBegin. Expected 108 tests, 0 skips, 31 on SQL Server.
  * B: `test_priority_order.MssqlC3Corrections` and `MssqlC4Corrections`. Expected 34 tests, 0 skips, all on SQL Server.
  * C: `test_resident_decisions` methods `test_challenge_source_exact_dependency_manifest_and_original_reviews` and `test_failed_priority_accept_edit_remove_disposition_and_audit` on `MssqlResidentControls` (SQL Server), `SqlResidentDecisions` (SQLite) and `JsonResidentDecisions` (in-memory). Expected 6 tests, 0 skips, 2 on SQL Server.
  * Totals: 3 processes, 148 tests, expected ZERO skips of any kind. B and C run independently of A and each other.
* P4 Cleanup. The trap runs only after a container id was captured, verifies the label and exact name, then removes that container id only; a failed verification removes nothing and is reported. A post-step lists databases matching only the two task prefixes (`zf_priority1292_%`, `zf_resident88_%`) before removal and records the list. Remove only the explicit resolved own `.venv`, manifest and `home` paths after evidence is hashed.
* P5 Redaction and hashing. Test output is redacted while it is written (streaming filter in `run-redacted.py`; other captured output is piped through the same filter), so no unredacted copy is persisted. Raw sanitized outputs stay external in a new directory under the coordinator files directory. SHA-256 of each sanitized output is recorded in the changes record; no raw output, connection string or password enters the repository.
* P6 Records. Changes and Review records, handoff, the existing cutover evidence pack (dated bounded subsection), index entry and append-only log entry, state file. Source blobs, tree, import paths, image id and digest, SQL Server, mssql-python, ODBC and Python versions recorded.

## Acceptance of this lane (not of the issue)

* Success is decided by an external verifier (`verify-1292-cm.py`), not by the runner: all three exits 0, unittest `Ran` counts 108, 34 and 6, `OK`, zero skip lines, exactly 67 SQL Server test lines passing (31, 34, 2), cleanup verified, no leftover databases, and `docker ps -a` showing no owned container afterwards. A runner `DONE` marker is not success.
* Failure of any selected test, timeout, skip, unexpected count, or unadmitted state is reported as the real result with the smallest precise reproduction (class, method, environment), deduplicated against existing owners (#1292 original, E1 to E4 records). No correction is made.
* A pass states only: at current main source blobs listed in the research, 67 of the 148 selected tests exercised the disposable SQL Server 2022 container and passed once; the other 81 are SQLite, in-memory, fake-driver and guard tests that passed in the same processes. It does not state fixed cause for the unknown startup failure, whole-SQL acceptance, full-gate waiver, AC tick or closure.

## Guardrails

* Do not read `.env`, home credentials or private datasets; never print the password, connection string or environment.
* Do not touch other worktrees, containers, images, caches or the dirty primary checkout; no prune, wildcard removal or unresolved recursive deletion.
* If a test needs a code fix, STOP and report the real failing evidence.
* Commit order: research, plan, details, critique and state are committed BEFORE any SQL execution; changes, review, pack, index and log are committed after. The tracking-only commit leaves source identical to the pinned base (checked by the runner).

## Critique dispositions applied before implementation

* C1 to C7 below in the critique record. Runner revised as `sql-1292-current-main-v2.sh` with `run-redacted.py` and `verify-1292-cm.py` (session files, derived from the existing `sql-1292-vc.sh`, not repository content). The first draft was reviewed and never executed.
