---
title: Changes, issue 153 document-control retention and hold refusals
ms.date: 2026-11-06
---

* Scope: issue153 only. Branch `fix/document-control-wording-153`, base `bb3a3b03cb94eef6c06ae4b12d07cfe7bbdef43f`, declared child target `test/ux-evidence-149`. Local only; nothing pushed.
* `src/core/src/zava_forward/core/doc_controls.py`: two string literals in `approve_retention_deletion` (legal-hold `PermissionError`, not-due `ValueError`). Types, predicates, the `retention_delete_blocked_legal_hold` audit call, `_remove_document` and all stored statuses unchanged.
* `src/api/tests/test_document_controls.py`: `test_retention_refusals_explain_reason_owner_next_action_and_change_nothing` (JSON and SQL store classes) covers no-trigger, future-trigger and held cases; asserts phrases, document and blob retained, audit count (one blocked-hold event only for the hold), `verify_audit()`, and that exact due-day deletion still succeeds after release.
* `src/api/tests/test_content_standard.py`: `test_document_control_refusals_use_plain_wording` (old literals absent, new literals present).
* `docs/reference/research/ux/content-standard.md` (slice 4, `ms.date` 2026-11-06), `docs/reference/README.md` (index sentence), `docs/reference/log.md` (appended entry).
* Amendments: critique finding 1 (impossible next step) changed the draft next action; findings 2 to 5 refined authority, term and test scope. Dispositions in `challenges/2026-11-06/issue153-document-control-refusals-critique.md`.
* Divergences: none from the revised details file. During implementation a test fixture issue (mutating the store's case object did not persist under the SQL store) was fixed by building cases before store creation; one transient syntax error from an import edit was fixed before any run passed.

## Validation (scratch venv `/mnt/ama-gates/restart-1106-153-wording/venv`, pip editable installs of this worktree's `src/core`, `src/agents`, `src/api`)

| Check | Result |
| --- | --- |
| Import identity | `zava_forward.core.doc_controls` resolves to this worktree. The system Python's installed copy resolves to another checkout (`/home/azureuser/source/ama`), so its results were not used as evidence |
| Baseline before change (venv) | `test_document_controls` 15 tests OK; `test_content_standard` 17 tests OK |
| First direct `-m unittest tests.test_content_standard` runs, `test_mvp` import and `-m unittest test_document_controls ...` | Failed with ModuleNotFoundError (module path invocation); preserved in scratch `baseline/` and not hidden. Re-run via `unittest discover` |
| New tests against old source | Both fail (exit 1), proving they detect the old wording |
| After change | `test_document_controls` 17 tests OK; `test_content_standard` 18 tests OK |
| `ruff check` (core, api) | All checks passed |
| `ruff format --check` | Files already non-conformant at HEAD (same result before and after); not reformatted, unrelated churn avoided |
| `py_compile`, `git diff --check` | Pass |

Not run: mypy, the native focused gate (`python3 tools/rpi-checks.py --changed`), any SQL service, browser, Docker, scanner or Blob call. Pending coordinator admission.
