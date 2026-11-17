---
title: "Phase Details: resident-integration-462"
description: "Step details for the Issue #462 continuation plan"
ms.date: 2026-11-17
---

Plan: [plan](../../plans/2026-11-17/resident-integration-462-plan.md)

## Phase 1: Non-rewriting merge

* Precondition: `git rev-parse HEAD` is exactly `926b20a8856622515c60948bf9ed890b241fc1fc`; `implement-start` witness recorded and the changes artifact persisted; worktree clean apart from `.copilot-tracking/` continuation files.
* Steps: `git merge --no-commit --no-ff 1c9ac230be1dad9a4ecc21975f9ffe0845309fc4`; `git status --short`; list unmerged paths.
* Expected: no conflicts (read-only `merge-tree` predicted tree `16faf2ec`). On conflict, resolve only by preserving both intents; if not reconcilable, abort with `git merge --abort` only on this fresh merge and record the exact blocker (not a reset of retained work).
* Verify: `git rev-parse MERGE_HEAD` equals the pin; `git diff --cached --stat` against `926b20a8` contains main's changes only plus nothing from this worker.

## Phase 2: Documentation update

* Files: new `docs/reference/research/resident-demo-threat-model-update-2026-11-17.md`; `docs/reference/log.md` (append) and `docs/reference/README.md` (index link); `src/api/README.md` only for a documentation-only qualification if the merged README overstates the resident sensor status badge or source line (empty history returns before both; the badge is suppressed for stale history). The 2026-11-16 threat model is not edited.
* Claims allowed: observed code facts with `file` references. Not allowed: acceptance, live behaviour, current-score claims, certified provenance.

## Phase 3: Light validation

* Venv: `<evidence>/venv`, `pip install` the `src/core`, `src/agents`, `src/api` distributions from this worktree (existing dependency manifests; install only for the missing venv).
* Tests (unittest; exact commands recorded in the changes artifact):
  * core (cwd `src/core`): `test_resident_showcase`, `test_resident_showcase_verifier`, `test_resident_access`, `test_resident_sensors`, `test_home_case`, `test_indoor_projection`, `test_resident_summary`, `test_resident_documents`. `test_resident_showcase_sql` needs SQL: any skip must be the expected SQL-unavailable skip and is reported as a gap, never a pass.
  * api (cwd `src/api`, `PYTHONPATH=../core/tests:../agents/tests` as the repository guide states): `test_resident_demo_api`, `test_resident_demo_check`, `test_resident_demo_script`, `test_resident_api`.
  * infra: `test_resident_demo_deploy`, `test_resident_demo_secrets` (no Docker or Azure).
  * Unrun coverage (SQL parity, Docker image, browser, full API suite) is listed separately.
* Lint: `ruff check` and `ruff format --check` on the resident modules and tests; `mypy` on `src/core/.../resident_showcase*.py` and `src/api/.../resident_demo`.
* Record command, exit code, test count and skip count; unexpected skips are failures of the record, not passes.

## Phase 4: Heavy checks

* Wrap the whole browser command: `flock -n /tmp/ama-rpi-heavy.lock <command>`. A non-zero exit from flock itself (lock busy) means `pending: lock held by the coordinator FULL run`; the lock is held for the command's duration, never taken and released early.
* If obtained: set `ZF_BROWSER_SCRATCH` to the evidence directory, synthetic loopback, intercept external requests, pinned axe. Docker image and SQL parity stay missing (no socket, no SQL).

## Phase 5: Web review

* Fetch `https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md` immediately before reviewing `src/api/src/zava_forward/api/resident_demo/web/demo.js` (changed on main by #1826). Report `file:line` findings. A fetch failure is recorded as partial, not as a pass.

## Phase 6: Review and commit

* One independent review of the final source snapshot (merged tree and continuation artifacts staged before review). Corrections after the review are limited to documentation and are stated as post-review qualifications in the review record; no second review.
* Final commit: merge commit including artifacts, repo-local privacy-safe identity, `Co-authored-by: Copilot` trailer. Then `commit-complete --claim-commit <sha>`.
