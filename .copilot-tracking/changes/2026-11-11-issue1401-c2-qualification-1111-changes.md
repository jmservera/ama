---
title: Issue 1401 cycle 2 requalification changes
ms.date: 2026-11-11
task_id: 1401-c2-qualification-1111
---

## Files

New records only; source, tests and the seven cycle 1 records are unchanged and not moved.

* `.copilot-tracking/research/2026-11-11-issue1401-c2-qualification-1111-research.md`, `plans/...-plan.md`, `details/...-details.md`: committed as `8081abecb4ab1a92635b50330a15bdda9dab80c9` before any cycle 2 verification command.
* `.copilot-tracking/reviews/2026-11-11-issue1401-c1-independent-678c458-1111-original-report.json`: byte-exact copy (cmp and sha256 equal) of the independent report for 678c458.
* This changes record, the critique, the Review and the state file.

## Chronology (cycle 2, prospective)

* Verified clean branch, head 678c458, tree 9951f83, current `origin/main` ea811c2; read the independent report in full.
* Wrote and committed research, plan and details (`8081abe`).
* Ran `/tmp/run_c2_1401.sh` once (no SQL, no installs): every tool wrote noclobber `.out`, `.err` and `.exit` with the direct exit captured first.
* Wrote this changes record. The one critique, one Review and final commit are recorded in their own files and the state file; they were pending when this record was written.

## Cycle 1 process deviation (stated, not repaired)

The cycle 1 research, plan and details files were created after the source and tests were edited and tested; they are retrospective records and the cycle 1 plan checklist was not a prospective plan. Cycle 1 research did occur before editing, and the critique and Review were genuinely later and run once. Cycle 1 history is preserved unchanged. Cycle 2 is the first record of this issue with a prospective plan committed before verification; it does not retroactively make cycle 1 prospective.

## Raw capture limits (cycle 1, carried)

The original wrapper native exit is missing (possible shared-launcher capture artifact; unknown, not 0, not a failure, not recreated). Original API, lint and type exits were piped and collapsed and are not proven. The original SQL script's outer status can hide a failure, but the saved `mssql_exit=0` line is a direct real exit. The original container-count 0 and flock 0 are handoff claims never independently verified, and the manifest was removed and not recreated. Adverse originals are retained: `/tmp/before1401.txt` (7 genuine errors, 4 `StateInvalid`) and `/tmp/after1401.txt` (4 errors from a wrong response key, later corrected), plus the other files listed with sha256 in the research.

## Cycle 2 results

Evidence directory `/tmp/zf1401-c2-1111-20261111T171053Z` (outside the repository; `SHA256SUMS` inside). All direct exit files are 0 and every `.err` is empty except the two unittest runs, which write their progress to stderr.

* head-identity: HEAD 8081abe (tree c31fb84, tracking-only commits on 678c458), clean, `git diff --exit-code 678c458 -- src` exit 0 before and after (head-after).
* Target compatibility (non-mutating): `git merge-tree --write-tree HEAD origin/main` exit 0, result tree 2ef0c5fe29b356ee8f14a2ef9d8faa43cbdc1791 (computed at HEAD 8081abe, so it includes the committed plan records; the earlier pre-plan value at 678c458 was 1e7b0fc2ada17ac4969130ba0d6829832d1dafd5). Only non-tracking path added in main since the base: `src/api/tests/test_permit_sql.py`. The three candidate-changed files differ in main only because main lacks the cycle 1 change; no rebase performed.
* Provenance: separate import probes under the same `PYTHONPATH` as each test run (not inside the test processes) printed `__file__` and sha256 for the aftercare, intake, store, sqlstore, mssqlstore, API server and workbench modules, all under this worktree, and sha256 of the five test files by relative path. Test-module `__file__` values and every transitively imported module were not captured; the unittest tracebacks and relative-path `PYTHONPATH` give plausible, not exhaustive, evidence that no primary-checkout source ran. `aftercare.py` sha256 f803b5c6e5e6d26d58c4f06a3fb0c9def1c1d677aff017c2165b796d1ccf6318.
* Core `tests.test_aftercare`, `tests.test_aftercare_intake`, `tests.test_aftercare_store`: `Ran 104 tests in 130.736s`, `OK (skipped=15)`, exit 0. 89 executed ok (counted in `core-unittest.err`), 15 opt-in SQL Server skips; not 104 passes.
* API `tests.test_aftercare_served`, `tests.test_aftercare_screen`: `Ran 21 tests in 9.189s`, `OK`, exit 0.
* `ruff check`: All checks passed, exit 0. `ruff format --check`: 3 files already formatted, exit 0. `mypy`: no issues in 3 source files, exit 0.

## SQL disposition

No SQL, container or cleanup action in cycle 2. The 15 actual SQL Server C1 results in `/tmp/mssql1401.txt` are reused only as a qualified historical result because the aftercare source, intake, store and the two test file blobs are unchanged from 678c458. No universal SQL failure-path or cleanup conformity is claimed.

## Limits

Synthetic only; no HTTP 503 at 1000, concurrency or performance coverage; not whole #133/#89, not #1402, not production or high-volume approval. #1401 criteria are not ticked and nothing is published. Counter: C2 of 3 used, C3 unadmitted.

## Chronology qualification

The plan was committed before the Phase 2 test, lint and type runs. Read-only identity, merge-tree and report reading were done during research before the plan commit and are recorded in the research record.
