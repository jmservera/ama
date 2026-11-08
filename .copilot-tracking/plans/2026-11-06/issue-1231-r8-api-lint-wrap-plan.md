---
title: Issue 1231 r8 plan (wrap two overlong API test lines)
ms.date: 2026-11-06
---

## Chronology statement (prospective)

Written 2026-11-06 about 16:51Z, before any edit. Governing design stays the existing R5 research, plan and details; no new investigation is claimed. Trigger: failed FULL receipt `/mnt/ama-gates/g1231-r7-1106/receipt.json` (sha256 `d0f1b3a215e8a351e600d0ac31496f62132d202976b9c426dc7b8dce3db1ea0e`), group `project-api`, Ruff E501 at `src/api/tests/test_ranking_publication_wiring.py` lines 87 and 111, introduced by the R5 tests. The R5 and R6 Ruff runs covered only four core files (a recorded scope omission). The r7 runner was launched with nohup as a diagnostic launch (a recorded deviation). The failed receipt and logs are preserved unchanged.

## Start identity

Branch `fix/ranking-archive-concurrent-writer-metadata`, head `9f303e0f3ecb79a3f06d15f16c4ff2615db25101`, tree `44b56b0209bcae7dde600da5924873e99c38c092`, ignored-inclusive clean. Target stays the #79 parent. Base main `bb3a3b03cb94eef6c06ae4b12d07cfe7bbdef43f`.

## Scope

* Wrap the two overlong lines with existing style, identical values and assertions. No assertion removal, ignore, baseline, lint limit change or refactor. No new tests.
* Checks: Ruff check and format --check across all of `src/api`, and the `test_ranking_publication_wiring` module, in the shared read-only `/tmp/zf79venv` with `PYTHONPATH` bound to this worktree and import proof (not isolated, unpinned tools), outputs under `/mnt/ama-gates/restart-1106-1231/r8/`. No SQL, browser, images, scanners or FULL.
* After checks: Changes, separate author Review, state, commit. A later fresh FULL on the new head remains required; r7 cannot be resumed or reused.
