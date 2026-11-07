---
title: Issue 80 r12 changes, harness test isolation and README correction
description: Original change record for a test-only isolation fix and a current-tense README correction
ms.date: 2026-11-06
---

* Plan: [plan](../plans/2026-11-06-excel-transition-80-r12-test-isolation-plan.md). Prospective records committed as 02ca61914 before any test or README edit.

## Changed paths

* `src/api/tests/test_browser_harness_scratch.py`: `test_default_scratch_parent_is_unchanged` now patches `harness.ROOT` to an owned `tempfile.TemporaryDirectory` with the existing `patch.object`/`patch.dict` pattern. It asserts the legacy `ROOT/.venv` result inside the temporary root, so the actual checkout is not touched.
* `src/api/README.md`: the shared-harness paragraph is now current tense: default legacy scratch under `.venv`; absolute external `ZF_BROWSER_SCRATCH` overrides and unsafe values are refused; configured bytecode controls are passed to the server child.
* New r12 research, plan, details, changes, state; the Review is a separate later commit.

## Light evidence (external caches under `/mnt/ama-gates/e80-r12-r65-1106/`, bytecode disabled, direct exits)

* Four-test harness module: exit 0, 4 tests, 0 skips (`unit-a1.log`).
* Ruff check, Ruff format check and mypy on the test: exit 0, 0, 0 (`ruff-a1.log`, `fmt-a1.log`, `mypy-a1.log`).
* Repo-root `.venv` inode and mtime are identical before and after the run (22110239, 13:37:46.581786316), so the run did not touch the checkout `.venv` (`venv-stat-before.txt`).
* `git diff --stat 5fa44964` over `src/{agents,api,core,importer,orchestrator}/src` and `src/api/checks` is empty: production and harness bytes unchanged.
* No broad 124-test pass was rerun; the r11 124-test, Ruff, format and mypy-188 outcomes remain history.

## Not done

* No deletion, browser, server, SQL, lock, install or FULL. The four ignored inputs are still present, so the worktree is not clean. The r11 archive predates three r11 records; the current-head proof is an external post-commit step after the final Review commit and is recorded in the external handoff, not in this tracked file.
