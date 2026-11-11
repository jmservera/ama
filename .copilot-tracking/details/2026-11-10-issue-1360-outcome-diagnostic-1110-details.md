---
title: Issue 1360 served-transfer outcome diagnostic details
ms.date: 2026-11-10
task_id: 1360-outcome-diagnostic-1110
---

## Paths

* Evidence root `E`: `/home/azureuser/.copilot/session-state/38e61c82-3c44-4b97-af59-9eed5c151ac7/files/phase1360-outcome-diagnostic-evidence-1110/`
* Diagnostic scripts `E/diag/` (`driver.py`, `run_case.py`), fixtures and databases `E/runs/<case>/` (owned, synthetic), raw outputs `E/runs/<case>/*.txt|json`.
* Env: `/tmp/zf-1360-1110/venv`; logs `/tmp/zf-1360-1110/logs`.
* The worktree is not written by diagnostics. `PYTHONDONTWRITEBYTECODE=1` is set for every run.

## Fixture

* A case directory with `import.db` (real `RefusalLedger` SQLite file written by the importer `submit_file` with a non-workbook synthetic file `bad.xlsx`, bytes `not a workbook`), the refused source file, `seed.json` (`{"cases": [], "staff": []}`), `state/zavaforward.sqlite` (served SQLite store).
* Environment for the CLI: `ZF_STORE=sqlite`, `ZF_DATA=<case>/seed.json`, `ZF_STATE=<case>/state`. No default or private data path is referenced.
* Before any run: sha256 of `import.db` and `bad.xlsx`, ledger row counts, served store `meta seq`, `meta import_exceptions`, audit count and head hash.

## Driver (actual CLI process)

The driver runs in a subprocess with `python driver.py transfer <db>`; it installs the hooks and then executes `runpy.run_module("zava_forward.importer", run_name="__main__")`, so the exit code and stderr are those of the real CLI code.

Hooks, installed on the `SqlStore` class:

1. `save` wrapper: on the first call from the transfer target store only, mark that instance as the target, then open a second independent `SqlStore` on the same database and commit a real `save` of the unrelated `form_schemas` document. Record the `meta seq` before and after. Call the original `save`.
2. `_sync` wrapper: log every call (instance role, caller function name, time). Inject only when the instance is the target, the immediate caller is `save`, and a separate read-only `sqlite3` connection shows that `meta import_exceptions` contains the refusal digest, the audit table contains `recorded_import_refusals` and `meta seq` is greater than the value before the transfer save. Write the proof file first and then raise `OSError("synthetic post-commit refresh failure")` (or `ValueError` in the second case). All other `_sync` calls pass through unchanged. The caller test checks both function name `save` and the `sqlstore.py` file of the immediate caller frame.
3. No hook on `open`, read, pre-commit paths or `record_import_refusals`.

## Cases

* C1: OSError at post-commit `_sync` through the CLI (primary counterexample attempt).
* C2: ValueError at the same point (only if C1 ran cleanly; bounded, cheap).
* Negative control N1: same fixture and independent writer, no injection: expect exit 0, no failure message.
* Negative control N2: same injection point condition but the independent writer commits the same `import_exceptions` document, so the save raises `ConflictError` before commit: expect the known conflict message and no retained refusal; proves the injection does not fire pre-commit.
* Existing adjacent branches (conflict rollback, committed reload, partial, driver, pre-commit ValueError, store-open) are covered by running the existing unchanged test module `tests.test_import_exceptions` from `src/importer`.

## After the run

* Independent reopen with a fresh `sqlite3` connection and a fresh `SqlStore`: retained `import_exceptions`, retained audit entry count and chain, independent writer's `form_schemas` retained.
* Repeat the real CLI `transfer` without hooks: exit code, stdout, and audit count unchanged.
* Recompute sha256 of `import.db` and `bad.xlsx`.

## Cleanup

Remove only owned temporary env and fixture directories created by this task after copying logs into the evidence folder. The evidence folder itself is retained for Root.

## Validation of the claim

A result is reproduced only when all of: proof file shows commit confirmed before injection, CLI exit 2 with the generic "Nothing was recorded" text, independent reopen shows retained document and audit, retry adds nothing.
