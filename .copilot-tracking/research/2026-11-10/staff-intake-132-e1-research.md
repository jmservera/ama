---
title: Staff intake 132 extension E1 research
ms.date: 2026-11-10
---

Extension E1 of five (new finite owner grant dated 2026-11-10 after 23:08: "Authorize up to five additional corrections for this existing scope"). Original C1 to C5 stay spent and preserved; this is not a reset. Parent task `staff-intake-132-c5`. Research disposition: executed. Planning Readiness: Ready.

## Inputs read

* Brief `brief-132-extension1-2312.txt` (coordinator root) and `132-c5-project-mypy-1109.log`: two errors, `tests/test_staff_intake_api.py:66` (missing type arguments for generic `dict`) and `:72` (returning Any from a function declared to return `dict[str, Any]`).
* Clean original candidate `6fd5106a72c8aeef1fa3e0a58288cc050a2d8736`, independent functional Approve 0 findings (recorded by the coordinator; preserved, not edited here).

## Reproduction

* The recorded log's two errors were reproduced with the project command `cd src/api && mypy` (pyproject `strict = true`) from an own venv `/tmp/zf132-e1-venv` holding editable installs of the core, agents and api distributions and the pinned dev tools `mypy==2.4.0`, `ruff==0.17.1`, `playwright==1.64.0` (python package only, no browser).
* An earlier attempt without `playwright` failed with 59 `import-not-found` errors and two unrelated unused-ignore or Any-return errors in other files. These came from the missing pinned dev dependency, not from this scope, and vanished once the pinned dependency was installed. Raw logs: `/tmp/zf132-e1-mypy-red.log` (final, exactly the two introduced errors, 228 files).
* A mypy run with `MYPYPATH` pointing at the agents source gave two extra unused-ignore errors in `test_ai_consumption_api.py`; that run is not the project command and is discarded.

## Ancestry

`origin/main` moved to `6d4cd62475ba89a214055f761b8e3276ef063d44` (62 commits ahead of the previous parent base `a8593a7a`). An ordinary `git merge --no-ff` produced three additive text conflicts, resolved by keeping both intents (merge commit `173cd9ff7`, tree `91389618b25f13758a7afc89c4ba4cc0429bc78c`, author and committer the repo-local noreply identity):

* `projection.py` STAFF_GET tuple: main added `aftercare`, this branch added `field_intake`. Both kept.
* `test_role_endpoint_inventory.py`: main added the form-review held-export GET route, this branch added the three intake POST routes. Both kept.
* `src/core/README.md`: this branch's staff intake section and main's learning-test section were adjacent additions. Both kept in order.

## Cause of the two errors

Both are in the C4 `correction` and `view` test helpers: `-> dict` is an unparameterised generic, and `view` returns the untyped second element of `self.call`. Test-only; no runtime or source behaviour is involved.

## Decision

Smallest fix: annotate `correction` as `dict[str, Any]` and have `view` bind the response to a typed local before returning it. No source, UI or unrelated test change. No SQL, browser, model or cloud is needed for the type fix; the affected intake tests are re-run as a targeted unit check, and the SQLite store path is covered by them. MSSQL and the browser are not re-run because no behaviour changed (stated as unobserved, not waived; the earlier SQL pass is not current live acceptance).

## Limits carried forward

Legacy staff-code receipts, no JSON-store cross-process guard, AC5 escalation gap, and synthetic approvals are not QA, legal, resident, live or assistive-technology acceptance. No new accounts, permissions, consent or contract authority.
