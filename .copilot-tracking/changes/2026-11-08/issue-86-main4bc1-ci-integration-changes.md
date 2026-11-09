---
title: Issue 86 Main 4bc1 CI integration changes
ms.date: 2026-11-08
---

Scope: issue86 only (Refs #86). Bounded CI dependency integration; no application change.

## Changes

* Prospective records committed at `cfa7beb6` before the merge.
* Ordinary merge `371665f9a8d6427aa2ff922f943c1c796184f9b5` (parents `cfa7beb6`, Main `4bc1e3f3`), tree `4b9f3e1013fa8662c79bca78a8bc5dd299fbd839`. Conflict-free.
* `src/` tree identical before and after. First-parent diff contains only the incoming tooling, workflow, infra README, Main knowledge-base log and Main tracking files. `git diff --check HEAD^1 HEAD` exit 0. `.github`, `tools` and `infra` trees equal Main `4bc1e3f3`.

## Focused checks on the merged source (raw output under external scratch g86-main4bc1-ci)

| Check | Result |
| --- | --- |
| `test_rpi_checks.py` | 86 tests OK, exit 0 (the earlier "FAILED required group" lines are expected test-fixture output) |
| `test_ci_affected.py` run 1 | exit 1, 19 run, 3 errors: `ModuleNotFoundError: yaml` (missing dependency). Preserved as `test_ci_affected.run1-missing-yaml.out` |
| `test_ci_affected.py` run 2 | 19 tests OK after installing PyYAML with pip into the scratch `--target` only; PYTHONPATH pointed only at that scratch dir |
| `test_install_actionlint.py` | 12 tests OK |
| `test_backlog_sync.py` | 17 tests OK |
| ruff check (isolated, CI flags, 7 files) | exit 0 |
| ruff format --check | exit 0 |
| mypy --strict runner and installer pairs | no issues in 2 source files each |

Counts match the known Main counts (12 installer, 19 CI-selection, 86 runner). Tool versions came from an existing scratch venv and were not verified against the CI pins (ruff 0.17.1, mypy 2.4.0); hosted CI remains the authority.

## Not run

* actionlint and the installer network download: not run locally; hosted CI covers it. No download pass is claimed.
* SQL, browser, images, scans, FULL: not applicable because no application behaviour changed (`src/` identical) and the owner CI-first policy applies.

## Drift disclosed

Origin Main moved to `9d035ee9e4fa34c783571f69e878ffb88ecf0259` after the reviewed `4bc1e3f3`. It was not integrated (out of scope). Target `feat/controlled-lifecycle-integration-81` is still `c5edb320`; origin child ref is still `fb7231c7`.

## Unchanged

Original adverse records, the old FULL SIGTERM, #1238, receiver, approver and human approvals, and the unmet fourth criterion.
