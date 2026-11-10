<!-- markdownlint-disable-file -->
# Served import-refusal checkpoint 440 details (2026-11-10)

Task `440-served-checkpoint-1110`. Plan: `.copilot-tracking/plans/2026-11-10-served-checkpoint-440-1110-plan.md`.

## Observation matrix (owned venv `/tmp/i440-served-1110/venv`, `env -i`, scratch `HOME` and `TMPDIR`, explicit `ZF_DATA=/tmp/i440-served-1110/zfdata/zavaforward.json`)

* T1 Core `discover -s tests -p test_import_refusals.py -v` from `src/core` (JSON, SQLite and CLI cases; MSSQL class skips without its opt-in gate).
* T2 Core `test_dependency_rule.py`.
* T3 Importer full `discover -s tests` (includes `test_import_exceptions.py` transfer and failure cases).
* T4 API `test_exception_register*.py` with `PYTHONPATH=../core/tests:../agents/tests` as the project README documents (register, operator, steward, unnamed manager, import-refusal register on JSON and SQLite, endpoint).
* T5 API `test_role_screens*.py`.
* T6 `node --check` of `role-screens.js` (the only API source file changed by 1361).
* T7 to T9 `ruff check`, `ruff format --check` and `mypy` on the Importer at the pinned versions of its own `dev` extra.
* S1 constructed served story: a synthetic refused workbook staged with `python -m zava_forward.importer stage`, `transfer` twice with `ZF_STORE=sqlite`, an explicit owned `ZF_DATA` and `ZF_STATE`, then a read through the API register for a named steward, a named operator and an unnamed manager.
* Static only: the `__main__.py:160-161` generic `(OSError, ValueError)` branch for #1360, read from the pin; not executed.

## Classification vocabulary

Local observed (this run), historical not re-run (af7b, 27dab, 1fab, PR 1361 hosted checks), implemented-unverified, deferred, blocked, unknown. Byte-identical code is never counted as a fresh run.

## Evidence limits to state

Writable local witness is not host or model attestation; the model label is asserted. The matrix is not the full or `--changed` gate. No resident, professional, legal or live approval is observed; no named steward or operator is nominated by the owner (open decision on #135).
