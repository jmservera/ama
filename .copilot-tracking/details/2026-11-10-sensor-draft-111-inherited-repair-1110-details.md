---
title: Issue 111 inherited sensor draft correction details
ms.date: 2026-11-10
task_id: 111-sensor-draft-inherited-repair-1110
---

## Files and exact edits

| File | Change |
| --- | --- |
| `src/core/src/zava_forward/core/sensor_review_draft.py` | New `DraftAuditError`; `_persist` rewritten with a `committed` flag and `try/finally`; a typed `DraftStore = Store | SqlStore` alias; every function annotated; `dict[str, Any]` is avoided where a concrete shape exists |
| `src/core/tests/test_sensor_review_draft.py` | New JSON regression tests; annotate every function; mixin base `unittest.TestCase` only under `TYPE_CHECKING`; narrowed optionals |
| `src/core/pyproject.toml` | One new `[[tool.mypy.overrides]]` stanza with the two modules (plain and `tests.` names), `disallow_untyped_calls = false`, comment citing the untyped Store boundary |
| `.copilot-tracking/*` | Records only |

Not touched: `store.py`, `sqlstore.py`, `projection.py`, `server.py`, `ops.js`, API tests, browser check, any workflow.

## New JSON regressions (class `JsonDraftCases`)

1. `test_audit_failure_after_committed_save_keeps_the_draft`: patch `store.audit` to raise `OSError("audit disk full")`; `propose()` raises `DraftAuditError`; assert memory list length 1; read `store.live_path` JSON and assert exactly that draft key; the error carries `.draft["task_key"]`; audit entries unchanged.
2. `test_unrelated_save_and_reload_keep_the_draft_after_audit_failure`: after (1), call `store.save()` (unrelated), then `Store(seed)` on the same live path: draft present with identical `created_at` and digest.
3. `test_retry_after_audit_failure_is_idempotent_and_keeps_provenance`: retry with a later `at` and a different caller name; result `created False`, `existing True`; `created_at`, `created_by`, lineage, `draft_digest` equal the first attempt; one draft; no new audit entry (documented residual).
4. `test_non_io_audit_failure_still_keeps_the_committed_draft`: audit raises `ValueError`; the original exception propagates; memory and disk both hold one draft.

Existing `test_write_failure_restores_the_list_and_retry_creates_one` (pre-commit `save` failure) must stay green.

## Frozen-head proof

Extract `d5e7ac2ef:src/core` with `git archive` into an external directory, add the new test file, run only the four new tests with that tree first on `PYTHONPATH`, and assert the imported module origin is the extracted copy. Tests 1 to 4 must fail there (tests 1 to 3 on the divergence; 4 because memory is rolled back). Then pass in the working tree.

## Typing approach (no escapes)

* Parameter types: `store: DraftStore`, `user: Mapping[str, object]`-like `dict[str, Any]` is replaced by a `Person = dict[str, str]` alias where honest; env `Mapping[str, str] | None`; return `dict[str, object]`. Where the Store boundary is untyped the pyproject stanza handles the calls, not `cast`.
* Tests: `-> None` on every method; `_TestBase` alias; `list[bool]` for results; `assert candidate is not None`.
* Validation command, from `src/core` with the private venv: `ruff check .`, `ruff format --check .`, `python -m mypy --no-incremental --cache-dir <external>` (configured `files`), asserted editable import origin for the module.

## Rollback

Revert the working-tree edits before the commit; the frozen head is untouched. No data migration.
