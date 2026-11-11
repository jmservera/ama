---
title: Inventory-managed staff intake and independent QA 132 extension E3 changes
ms.date: 2026-11-11
---

Same E3 (E1, E2, E3 spent, two remain; no E4). Refs #132, #131, #440. Forward adoption and verification of the unchanged draft `3c395740`; the draft itself was authored before any plan (E2 history stands). No application or test source was edited in E3.

## Divergence from the E3 plan (Root's prospective amendment)

Plan Phases 2 and 3 called for validating the old source and a disposable scratch merge. Root admitted one ordinary committed merge of actual main first. The note [amendment](./inventory-qa-132-e3-amendment.md) was committed (`83b0a050`) before the merge. Phases 1 to 4 otherwise ran as planned; Phase 5 browser ran because the lock was free.

## Integration and identity

* Main pin `3dbb79e90c96b03d4b4a7059d3299a769c934836` (1428, 1426, 1423), fetched read-only, merged once with `git merge --no-ff` (no conflict, no rebase, amend or reset). Pre-merge head `83b0a0508df0c00ef735ef605b6fad9229b63ea7`, merge commit `9ccd7b858be519ae462ca5d37aff6feecc3b248f`, tree `d64219f01267c436c30982974d3802b603db1d28`.
* After merge: `test_staff_intake_api.py` blob `50fb4ec4c452b1b77a45d0bd071df8c9027319b2` (unchanged); `git diff 3dbb79e90 HEAD -- src` is only `src/api/tests/test_staff_intake_api.py` with 53 insertions, SHA-256 `2472c5af61e64651ebf73a221e0336184aa06b5bd24edb3c37c7e78e2c4ec44f`, identical to `git diff 7e2744cf 3c395740 -- src`.
* Import origins (`origins.txt`): `zava_forward.core`, `.agents`, `.api`, `resident_decisions`, `quality`, and the test and helper modules `test_staff_intake_api`, `test_procurement_api`, `test_resident_api` and `dataset` all load from this worktree. `pip check` clean. Existing venv `/tmp/venv-132-inv-qa-1111`; no pip install was needed.

## Commands and results (raw logs in `/tmp/ev132-e3`, copied to ROOT)

| Check | Exit | Result |
| --- | --- | --- |
| API `-v test_staff_intake_api` | 0 | 96 run, OK, 36 skipped |
| New cases `-k inventory_hold test_staff_intake_api` | 0 | 6 run, OK, 2 skipped; SQLite base and JSON subclass `ok` for both cases, MSSQL class skipped |
| API `-k inventory test_resident_api` | 0 | 1 run, OK |
| API `test_role_endpoint_inventory test_dependency_rule` | 0 | 26 run, OK |
| Core `-k inventory test_resident_decisions` | 0 | 48 run, OK, 17 skipped |
| Core two gate tests via `-k` over `test_resident_decisions test_quality_procurement` | 0 | 6 run, OK, 2 skipped |
| `ruff check .`, `ruff format --check .`, `mypy` (api) | 0 | clean |
| `git diff --check 3dbb79e90 HEAD` (our range) | 0 | clean |
| `git diff --check 7e2744cf HEAD` | 2 | one `new blank line at EOF` in main-owned `.copilot-tracking/changes/2026-11-10/issue-144-extension2-attribution-changes.md:44`, merged unchanged from main; not ours; retained, not fixed |
| Browser/axe `test_staff_intake_browser` (`flock -n` admitted, axe 4.10.3, SHA-256 `880970c0...8a68bb`) | 0 | 2 run, OK, 5 states with no violations; observation only |

Skips (unobserved, not passes): MSSQL class `needs the task-owned loopback SQL Server (ZF_STAFF_INTAKE_MSSQL=1)`, SQL-store-contract tests on JSON, Core opt-in loopback SQL Server. No zero-test selector was counted as a pass; none of the E2 guessed selectors were repeated.

## Sensitivity diagnostic (`/tmp/diag132e3/diag.py`, `diag.log`, not committed)

Mixin `Bypass` overrides `declare_inventory` (real inventory setup first) then patches only `Store.require_resident_clear` to a counting no-op; `DiagSql` and `DiagJson` built from it; two cases each. Patch invoked 6 times (SQLite 4, JSON 2), so not inconclusive.

| Class | Case | Result |
| --- | --- | --- |
| SQLite | after capture | sensitive: held accept returned 200, assertion `200 != 409` |
| SQLite | after acceptance | sensitive: held handover returned 200, `200 != 409` |
| JSON | after capture | sensitive: held accept 200 |
| JSON | after acceptance | sensitive: held handover 200 |

Limits kept: the first failing assertion stops each case, so restart and later-capture assertions are unobserved under the bypass. The diagnostic shows the held accept and handover assertions depend on the resident-clear guard; it is not a general mutation-test claim. The E2 `_inventory_managed=False` control stays recorded as weak. No fixture weakening.

## Unobserved

MSSQL, hosted CI, cloud or model, live or private data, human QA, resident consent, Legal tenure interpretation, named approvals. Whole #132, #131 and #440 remain open; no ticks, issue or 1420 expansion.
