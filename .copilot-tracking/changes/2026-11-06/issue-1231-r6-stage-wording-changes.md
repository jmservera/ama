---
title: Issue 1231 changes r6 (retained-stage wording accuracy)
ms.date: 2026-11-06
---

## Chronology (actual)

* Start 14:10:47Z, head `e5486018168b0cccb281e06be2fc156934a8bb2b`, tree `831f520a1bc1ebf24c26afaeab4fc51d9b756014`, ignored-inclusive clean.
* Research, Plan, Details each created in its own completed call, in that order, then one independent `rubber-duck` critique (Pass, PC-001 no issue), then the prospective commit `d4640358bd5ea7645bea04923a7c058246974a2d` at 14:12:09Z (author and committer `8036360+jmservera@users.noreply.github.com`, resolved fresh from `gh api user`). The two source edits came after that commit.
* Estimated times written inside the Plan (about 14:13Z), Details (about 14:15Z) and critique (about 14:17Z) files are later than the actual commit time 14:12:09Z. They are estimates, are left unaltered, and the commit time is authoritative. The first check ran at about 14:13Z, after the edits.
* R5 qualification (from the root assessment, not changed here): R5 Research, Plan and Details were created in one parallel batch, not as serial phases, though before planning commit, rebase, first test and first source edit. R5 Review and state were created in parallel at 14:00:14Z.

## Changes

* `src/core/src/zava_forward/core/ranking_publication.py`: docstring now says a retained stage kept by the committing writer shares the record's bytes and inode, while a loser's stage was never linked and can differ, so an operator checks it before removing it.
* `src/core/src/zava_forward/core/ranking_publication_runner.py`: `stage_not_removed` warning text now says the file "may share the archived record's bytes, so do not edit it." Code, stage name, next action, status and keys are unchanged.
* No logic, outcome, key, error handling, date, audit, storage, README or test change. `grep "hard-link alias" src` returns nothing.

## Checks (light preparation only)

* Output directory `/mnt/ama-gates/e1231-r6-r68-1106/` (new, caches under `cache/`, bytecode disabled).
* Interpreter: read-only shared `/tmp/zf79venv` (Python 3.12.3), not isolated or pinned; Ruff 0.17.3 (pin 0.17.1) and mypy 2.4.1 (pin 2.4.0). Its editable package points elsewhere, so `PYTHONPATH` named this worktree's sources; `import-proof.log` shows both modules loaded from this worktree.
* One combined unittest run of `test_ranking_publication`, `test_ranking_publication_runner`, `test_ranking_publication_wiring`: 73 tests OK, exit 0, no skips (`unittest.log`, `unittest.exit`). The full 59 and 49 suites were not rerun.
* Ruff check exit 0 and Ruff format check exit 0 on the two edited sources and two ranking test modules.
* mypy: first invocation from the repository root with the test path exited 2 (`mypy.log`, "No parent module", an invocation error, kept as is). Rerun from `src/core` with the project configuration: success, 4 files, exit 0 (`mypy-fromcore.log`).
* Blob hash comparison of every `.copilot-tracking` file at the pre-commit head against the working tree: no differences. Only the two source files differ in `git diff --stat`.
* No test of the warning wording exists or was added; the tests cover the retained-stage and loser paths, not text.

## Limits

* Light evidence in a shared unpinned environment; not isolated, not FULL. The final combined FULL, independent whole-feature review, hosted CI and publication stay pending with the coordinator. No real unsupported-mount test.
