---
title: Issue 80 stack integration changes
description: Prospective and actual record for the integration validation
ms.date: 2026-11-11
---

## Prospective (written before implement-start)

* No source, test, checker or README edit is planned. The only repository changes are this chain's own tracking files.
* Integration: parent fast-forwarded to `adbca56e` (already done at research time, ff-only). Trial merge of `origin/main` `b8394cd5` is uncommitted in the owned scratch worktree `/tmp/ama-80-stack-scratch-1111` (tree `93f5a0c9`); no merge commit in the parent branch because no real conflict exists.
* Checks listed in the plan; results appended after execution.

## Actual (after implement-start)

Combined tree tested: scratch worktree detached at parent `adbca56e` plus uncommitted merge of `origin/main` `b8394cd5` (tree `93f5a0c927f0fc6cedcc1aa121b353ae06915e2c`); venv `/tmp/ama-80-stack-venv-1111` with editable installs from the scratch tree; import origins asserted under the scratch tree (server.py, resident_decisions.py); `ZF_DATA` set to an owned temp path; no default data. Evidence: `phase80-stack-integration-evidence-1111/` (direct exits in `*.exit`, raw logs). No source, test or checker edit; no merge commit.

Direct exits (all 0):

* Child CSV API 13; handoff read guidance 9 (browser class run with `ZF_BROWSER_TESTS=1`, 0 skips); `test_handoff_api`; parent case journey 31; list export 11; static 60; role endpoint inventory; resident API; Atlas checker test (its 3 browser tests are opt-in and skipped: not run).
* Child UI 6 real Chromium, 0 skips (`ui6-r2`).
* Whole `capacity_browser_check --axe` once on the combined tree, exit 0, no skips, both delayed-401 iterations, mutation-refresh and empty-capacity controls printed PASS. Pre-run hashes in `capacity-pre-hashes.txt`: checker `59b3e44c...f7a1` and `ops.js` `93b32aa2...4972` are unchanged from `2cc34027`; `app.js` differs (child `pendingHandoffs` hunk), so the earlier 84 s PASS is historical only.
* Ruff check and format on `src/api` (145 files), mypy configured (228 files), Node syntax `app.js` and `ops.js`, core `test_resident_decisions` (149 skipped: opt-in SQL, not run).

Adverse or qualified, preserved:

* `preflight0-namespace-pkg-attr-error.log`: my first import-origin probe used namespace-package `__file__` (None); rerun by module file passed.
* `ui6.log` exit 0 but the browser class SKIPPED ('heavy lock busy') because I wrapped the test in `flock -n` and the test takes the same lock itself; rerun `ui6-r2` without the wrapper ran all 6. The first run is not a pass of the browser class.
* mypy and playwright were installed into the new owned venv as part of its setup, not after a failure.
* Skips left unrun and not claimed: guidance browser in the first non-browser pass, Atlas browser 3, resident browser 1, core SQL 149.
